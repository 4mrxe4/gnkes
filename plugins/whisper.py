from helpers.context import get_global_r, get_global_dev, get_global_k
r = get_global_r()
Dev_FINAL = get_global_dev()
k = get_global_k()
import re
import pytz
import html
import uuid
import time
import asyncio
from threading import Thread as th
from compat import Client, filters, enums

async def _safe_incoming(_, __, m):
    return not getattr(m, "outgoing", False)

async def _safe_outgoing(_, __, m):
    return bool(getattr(m, "outgoing", False))

filters.incoming = filters.create(_safe_incoming, "IncomingFilter")
filters.outgoing = filters.create(_safe_outgoing, "OutgoingFilter")
from compat import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InlineQueryResultCachedPhoto,
    InlineQueryResultCachedVideo,
    InlineQueryResultCachedAudio,
    InlineQueryResultCachedVoice,
    InlineQueryResultCachedSticker,
    InlineQueryResultCachedAnimation,
    InputTextMessageContent,
    InlineQueryResultArticle
)
from datetime import datetime

from helpers.ranks import *
from .buttons import register_buttons, get_button_custom, get_button_color, create_button_raw
from helpers.replies_store import (
    REPLIES,
    plugins_whisper_194,
    plugins_whisper_196,
    plugins_whisper_197,
    plugins_whisper_248,
    plugins_whisper_282,
)

pending = {}
whispers = {}
media_store = {}

# عند اختيار (إرسال) نتيجة الوسائط من وضع inline، تيليجرام كانت ترسل الملف
# الحقيقي كرسالة كاملة داخل المحادثة الحالية (والتي غالباً مجموعة) فتصبح
# مرئية للجميع لا للمستهدف فقط. لمنع هذا التسريب نمرّر input_message_content
# ثابت لكل نتيجة: تيليجرام يستخدم file_id فقط لعرض المعاينة الخاصة في قائمة
# نتائج inline (يراها المستخدم وحده قبل الإرسال)، لكن عند الاختيار الفعلي
# يُرسَل هذا النص الثابت بدل الوسائط الحقيقية.
WHISPER_MEDIA_SEND_BLOCKED_TEXT = "حسيت انك ارسلتها بالخطا"

# نص التنبيه الذي يُضاف أسفل أي وسائط تُرسل عبر "رابط اهمس"، حتى لو كانت
# موصوفة بنص من المرسل، ومدة الحذف التلقائي بعدها.
WHISPER_LINK_AUTO_DELETE_SECONDS = 60
WHISPER_LINK_AUTO_DELETE_NOTICE = "هذي الوسائط بتنحذف تلقائياً بعد دقيقة وحدة"

# نص يظهر عند محاولة فتح رابط "رابط اهمس" لوسائط سبق عرضها مرة واحدة —
# الوسائط تُعرض مرة واحدة فقط بغض النظر عن مرور الدقيقة (auto-delete) أم لا.
WHISPER_LINK_ALREADY_VIEWED_TEXT = "لقد تم حذف الهمسة لايمكن عرضها مجددا"

# اسم بديل يُستخدم عندما يكون اسم المستخدم غير قابل للعرض (فارغ أو مكوّن
# بالكامل من رموز/إيموجي بلا أي حرف أو رقم مقروء) بدل رمي أي خطأ لاحقاً.
INVALID_NAME_FALLBACK = "الاسم سبام"

BUTTONS_DEFINITIONS = {
    "whisper": {
        "name": "أزرار الهمسة",
        "buttons": [
            {"id": "show_whisper", "default": "• عرض الهمسة"},
            {"id": "view_media", "default": "• رؤية الوسائط"},
            {"id": "view_media_link", "default": "• رؤية الوسائط"},
            {"id": "whisper_back", "default": "• اهمس لـ"},
            {"id": "whisper_any", "default": "اهمس لـ"},
        ]
    }
}

register_buttons(BUTTONS_DEFINITIONS)



def get_str(data, key, default=""):
    val = data.get(key, default)
    if isinstance(val, bytes):
        return val.decode("utf-8")
    return str(val)

def safe_display_name(name):
    """يعيد اسماً صالحاً للعرض في الأزرار/الرسائل. إن كان الاسم فارغاً أو
    مكوّناً بالكامل من رموز/إيموجي بلا حرف أو رقم واحد مقروء (بأي لغة)،
    يُستبدل باسم بديل ثابت بدل أن يتسبب لاحقاً بأي عطل."""
    if not name:
        return INVALID_NAME_FALLBACK
    name = str(name).strip()
    if not name:
        return INVALID_NAME_FALLBACK
    if any(ch.isalpha() or ch.isdigit() for ch in name):
        return name
    return INVALID_NAME_FALLBACK

async def get_bot_username(c):
    """يعيد يوزر البوت بشكل موثوق. c.me قد لا يكون محمّلاً بعد في سياق هذا
    البوت داخل الكلاستر، فإن كان فارغاً نجلبه فعلياً عبر get_me() بدل ترك
    الرابط يُبنى بقيمة None."""
    me = getattr(c, "me", None)
    if me and getattr(me, "username", None):
        return me.username
    try:
        me = await c.get_me()
        if me and me.username:
            return me.username
    except Exception:
        pass
    
    try:
        bot_info = await c.get_chat("me")
        if bot_info and bot_info.username:
            return bot_info.username
    except Exception:
        pass
    
    return None

def chunk_text(text, max_chunks=6):
    max_chars_per_alert = 180  
    chunks = []
    
    text = " ".join(text.split())
    
    while text and len(chunks) < max_chunks:
        if len(text) <= max_chars_per_alert:
            chunks.append(text)
            break
            
        cut_index = text.rfind(' ', 0, max_chars_per_alert)
        
        if cut_index == -1:
            cut_index = max_chars_per_alert
            
        chunks.append(text[:cut_index].strip())
        text = text[cut_index:].strip()
        
    if text and len(chunks) == max_chunks:
        chunks[-1] = (chunks[-1] + " " + text)[:max_chars_per_alert].strip()
        
    return chunks if chunks else [text]

@Client.on_inline_query(group=423)
async def whisper_inline_handler(c, inline_query):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    q = inline_query.query
    if not q.startswith("W/"):
        return await inline_query.answer([], cache_time=0)

    wid = q.split("/", 1)[1]
    key = f"{Dev_FINAL}:whisper_data:{wid}"

    if not await r.exists(key):
        return await inline_query.answer([], cache_time=0)

    data = await r.hgetall(key)
    target_id = get_str(data, "target_id")

    if str(inline_query.from_user.id) != target_id:
        return await inline_query.answer([], cache_time=0)

    if get_str(data, "type") != "media":
        return await inline_query.answer([], cache_time=0)

    file_id = get_str(data, "file_id")
    media_type = get_str(data, "media_type").lower()

    if not file_id:
        return await inline_query.answer([], cache_time=0)

    results = []
    blocked_imc = InputTextMessageContent(WHISPER_MEDIA_SEND_BLOCKED_TEXT)

    if media_type == "photo":
        results = [InlineQueryResultCachedPhoto(id=wid, photo_file_id=file_id, title="معاينة الصورة", input_message_content=blocked_imc)]
    elif media_type == "video":
        results = [InlineQueryResultCachedVideo(id=wid, video_file_id=file_id, title="معاينة الفيديو", input_message_content=blocked_imc)]
    elif media_type == "audio":
        results = [InlineQueryResultCachedAudio(id=wid, audio_file_id=file_id, title="معاينة الصوت", input_message_content=blocked_imc)]
    elif media_type == "voice":
        results = [InlineQueryResultCachedVoice(id=wid, voice_file_id=file_id, title="معاينة البصمة", input_message_content=blocked_imc)]
    elif media_type == "animation":
        results = [InlineQueryResultCachedAnimation(id=wid, animation_file_id=file_id, title="معاينة المتحركة", input_message_content=blocked_imc)]
    elif media_type == "sticker":
        results = [
            InlineQueryResultCachedSticker(
                id=wid,
                sticker_file_id=file_id,
                input_message_content=blocked_imc,
            )
        ]
    await inline_query.answer(results=results, cache_time=0, is_personal=True)

async def handle_whisper_view_link(c, m, data):
    """يُستدعى عند فتح رابط 'رابط اهمس' (wv_<whisper_id>) — يرسل الوسائط
    الفعلية مباشرة للمتلقي في الخاص بدل المعاينة عبر inline، بنفس شروط
    الوصول المطبّقة على زر 'عرض الهمسة' النصي تماماً (المرسل والمستقبل
    فقط)، ويحذفها تلقائياً بعد دقيقة واحدة."""
    r = get_global_r()
    Dev_FINAL = get_global_dev()

    wid = data[len("wv_"):]
    whisper_key = f"{Dev_FINAL}:whisper_data:{wid}"

    if not await r.exists(whisper_key):
        return await m.reply(REPLIES['plugins_whisper_336'])

    data_row = await r.hgetall(whisper_key)
    target_id = get_str(data_row, "target_id")
    sender_id = get_str(data_row, "sender_id")

    # نفس شرط الهمسة الأساسي: المرسل والمستقبل فقط، وإلا يُبلَّغ المرسل
    # بمحاولة تطفّل (تماماً كزر عرض الهمسة النصي).
    if str(m.from_user.id) != target_id and str(m.from_user.id) != sender_id:
        try:
            user_name = safe_display_name(m.from_user.first_name or m.from_user.username or "شخص")
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton(text=user_name, user_id=m.from_user.id)]
            ])
            await c.send_message(
                int(sender_id),
                f"• الحق الحق\n• ذا ↤︎ {user_name} حاول يقرأ همستك بس ماخليته\n_",
                reply_markup=reply_markup
            )
        except Exception:
            pass
        return await m.reply(REPLIES['plugins_whisper_358'])

    if get_str(data_row, "type") != "media":
        return await m.reply(REPLIES['plugins_whisper_336'])

    if get_str(data_row, "viewed") == "1":
        return await m.reply(WHISPER_LINK_ALREADY_VIEWED_TEXT)

    file_id = get_str(data_row, "file_id")
    media_type = get_str(data_row, "media_type").lower()
    caption = get_str(data_row, "caption", "")

    if not file_id:
        return await m.reply(REPLIES['plugins_whisper_336'])

    # التنبيه يُضاف أسفل الميديا دائماً، حتى لو كانت موصوفة بنص من المرسل.
    full_caption = f"{caption}\n\n{WHISPER_LINK_AUTO_DELETE_NOTICE}" if caption else WHISPER_LINK_AUTO_DELETE_NOTICE

    sent = None
    extra_messages = []
    try:
        if media_type == "photo":
            sent = await c.send_photo(m.chat.id, file_id, caption=full_caption)
        elif media_type == "video":
            sent = await c.send_video(m.chat.id, file_id, caption=full_caption)
        elif media_type == "audio":
            sent = await c.send_audio(m.chat.id, file_id, caption=full_caption)
        elif media_type == "voice":
            sent = await c.send_voice(m.chat.id, file_id, caption=full_caption)
        elif media_type == "animation":
            sent = await c.send_animation(m.chat.id, file_id, caption=full_caption)
        elif media_type == "sticker":
            # الملصقات لا تدعم caption عبر Bot API، فنرسل التنبيه كرسالة
            # منفصلة أسفلها وتُحذف معها.
            sent = await c.send_sticker(m.chat.id, file_id)
            try:
                warn_msg = await c.send_message(m.chat.id, WHISPER_LINK_AUTO_DELETE_NOTICE)
                extra_messages.append(warn_msg)
            except Exception:
                pass
        else:
            return
    except Exception:
        return await m.reply(REPLIES['plugins_whisper_336'])

    if not sent:
        return

    # الوسائط تُعرض مرة واحدة فقط للمستهدف — فتح المرسل للرابط (للمراجعة)
    # لا يُستهلك به العرض، فقط عرض المستهدف الفعلي يُغلق الرابط لاحقاً.
    if str(m.from_user.id) == target_id:
        await r.hset(whisper_key, "viewed", "1")
        try:
            reader_name = safe_display_name(m.from_user.first_name or m.from_user.username or "الشخص")
            await c.send_message(int(sender_id), f"• قام {reader_name} بقراءة الهمسة\n_")
        except Exception:
            pass

    async def _auto_delete(main_msg, extras):
        await asyncio.sleep(WHISPER_LINK_AUTO_DELETE_SECONDS)
        try:
            await main_msg.delete()
        except Exception:
            pass
        for extra in extras:
            try:
                await extra.delete()
            except Exception:
                pass

    asyncio.create_task(_auto_delete(sent, extra_messages))

@Client.on_message(filters.private & filters.command("start") & ~filters.bot)
async def whisper_start_handler(c, m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if len(m.command) < 2:
        return
    data = m.command[1]

    if data.startswith("wv_"):
        return await handle_whisper_view_link(c, m, data)

    if not data.startswith("w_"):
        return
        
    w_type = "text"
    key = data.replace("w_", "")
    if key.endswith("_t"):
        w_type = "text"
        key = key[:-2]
    elif key.endswith("_m"):
        w_type = "media"
        key = key[:-2]
    elif key.endswith("_a"):
        w_type = "any"
        key = key[:-2]
    
    if not await r.exists(f"{Dev_FINAL}:whisper_pending:{key}"):
        return await m.reply(REPLIES['plugins_whisper_159'])
    
    pending_data = await r.hgetall(f"{Dev_FINAL}:whisper_pending:{key}")
    
    sender_id = get_str(pending_data, "sender_id")
    target_id = get_str(pending_data, "target_id")
    current_user_id = str(m.from_user.id)
    
    if current_user_id != str(sender_id) and current_user_id != str(target_id):
        return await m.reply(REPLIES['plugins_whisper_168'])
    
    if current_user_id == str(sender_id):
        new_target_id = target_id
        new_target_name = safe_display_name(get_str(pending_data, "target_name", "الشخص"))
    else:
        new_target_id = sender_id
        raw_sender_name = get_str(pending_data, "sender_name", "المرسل")
        new_target_name = safe_display_name(raw_sender_name)
    
    try:
        new_target_user = await c.get_users(int(new_target_id))
        new_target_mention = new_target_user.mention()
    except:
        new_target_mention = new_target_name
    
    await r.hset(f"{Dev_FINAL}:whisper_pending:{key}", mapping={
        "writer": str(m.from_user.id),
        "whisper_type": w_type,
        "target_id": str(new_target_id),
        "target_name": new_target_name,
        "sender_id": str(m.from_user.id),
        "sender_name": safe_display_name(m.from_user.first_name or m.from_user.username or "المستخدم"),
        "chat_id": get_str(pending_data, "chat_id", "0")
    })
    
    if w_type == "media":
        await m.reply(plugins_whisper_194(new_target_mention))
    elif w_type == "any":
        await m.reply(plugins_whisper_197(new_target_mention))
    else:
        await m.reply(plugins_whisper_196(new_target_mention))

@Client.on_message(filters.private & ~filters.command("start"))
async def receive_whisper(c, m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    k = await r.get(f'{Dev_FINAL}:botkey') or "•"
    if await r.get(f'{m.from_user.id}:sarhni') or await r.get(f'{m.from_user.id}:sarhnirep'):
        return
    keys = await r.keys(f"{Dev_FINAL}:whisper_pending:*")
    
    for key in keys:
        key_str = key if isinstance(key, str) else key.decode("utf-8")
            
        data = await r.hgetall(key_str)
        if not data:
            continue
            
        if get_str(data, "writer") != str(m.from_user.id):
            continue
            
        whisper_type = get_str(data, "whisper_type", "text")
        target_id = get_str(data, "target_id")
        target_name = safe_display_name(get_str(data, "target_name"))
        
        target_mention = f'<a href="tg://user?id={target_id}">{html.escape(str(target_name))}</a>'
            
        if whisper_type == "text" and not m.text:
            return await m.reply(REPLIES['plugins_whisper_225'])

        if whisper_type == "media" and m.text:
            return await m.reply(REPLIES['plugins_whisper_228'])

        whisper_id = uuid.uuid4().hex[:8]
        is_text = False
        
        chat_id = int(get_str(data, "chat_id", "0"))
        sender_id = get_str(data, "sender_id")
        sender_name = safe_display_name(get_str(data, "sender_name"))
        
        sender_mention = f'<a href="tg://user?id={sender_id}">{html.escape(str(sender_name))}</a>'
        
        if m.text:
            is_text = True
            await r.hset(f"{Dev_FINAL}:whisper_data:{whisper_id}", mapping={
                "type": "text",
                "text": m.text,
                "target_id": target_id,
                "sender_id": sender_id,
                "sender_name": sender_name
            })
            await m.reply(plugins_whisper_248(target_name))
        elif m.media:
            file_id = None
            media_type = None
            if m.photo:
                file_id = m.photo.file_id
                media_type = "photo"
            elif m.video:
                file_id = m.video.file_id
                media_type = "video"
            elif m.audio:
                file_id = m.audio.file_id
                media_type = "audio"
            elif m.voice:
                file_id = m.voice.file_id
                media_type = "voice"
            elif m.animation:
                file_id = m.animation.file_id
                media_type = "animation"
            elif m.sticker:
                file_id = m.sticker.file_id
                media_type = "sticker"
            else:
                return

            # "وصف نصي" على الميديا مسموح فقط عندما يكون وضع "رابط اهمس"
            # مفعّلاً — يبقى غير مفعل في الوضع الحالي (المعاينة عبر inline)
            # ليطابق تماماً السلوك السابق.
            link_mode = bool(await r.get(f"{Dev_FINAL}:whisper_link_mode"))
            caption = (m.caption or "") if (link_mode and m.caption) else ""

            await r.hset(f"{Dev_FINAL}:whisper_data:{whisper_id}", mapping={
                "type": "media",
                "media_type": media_type,
                "file_id": file_id,
                "caption": caption,
                "target_id": target_id,
                "sender_id": sender_id,
                "sender_name": sender_name
            })
            media_store[whisper_id] = file_id
            await m.reply(plugins_whisper_282(target_name))
        else:
            return
            
        try:
            await m.delete()
        except:
            pass
            
        message_text = (
            f"{k} الهمسه لـ ↤︎ {target_mention}\n"
            f"{k} من ↤︎ {sender_mention}\n_"
        )
        
        clean_key = key_str.split(":")[-1]
        bot_username = await get_bot_username(c)

        # زر "اهمس لـ" الراجع يجب أن يحمل نفس نوع الهمسة الأصلي لهذه
        # الجلسة (whisper_type) لا نوع المحتوى المُرسل فعلاً (is_text) —
        # هذا يضمن أن جلسة "دمج الأزرار" (any) تبقى غير مقيّدة في الرد أيضاً،
        # بينما الجلسات العادية (نصية/وسائط) تحافظ على نفس قيدها كالسابق.
        if whisper_type == "any":
            back_suffix = "_a"
        else:
            back_suffix = "_t" if is_text else "_m"

        inline_keyboard = []
        
        if is_text:
            view_btn = await create_button_raw("whisper", "show_whisper", "• عرض الهمسة", callback_data=f"whisper_view_{whisper_id}")
            whisper_back_btn = await create_button_raw("whisper", "whisper_back", f"• اهمس لـ {sender_name}", url=f"https://t.me/{bot_username}?start=w_{clean_key}{back_suffix}")
            
            inline_keyboard.append([{"text": view_btn["text"], "callback_data": view_btn["callback_data"], "style": view_btn.get("style", "success")}])
            inline_keyboard.append([{"text": whisper_back_btn["text"], "url": whisper_back_btn["url"], "style": whisper_back_btn.get("style", "success")}])
        else:
            whisper_back_btn = await create_button_raw("whisper", "whisper_back", f"• اهمس لـ {sender_name}", url=f"https://t.me/{bot_username}?start=w_{clean_key}{back_suffix}")

            if await r.get(f"{Dev_FINAL}:whisper_link_mode"):
                view_media_btn = await create_button_raw("whisper", "view_media_link", "• رؤية الوسائط", url=f"https://t.me/{bot_username}?start=wv_{whisper_id}")
                inline_keyboard.append([{"text": view_media_btn["text"], "url": view_media_btn["url"], "style": view_media_btn.get("style", "success")}])
            else:
                view_media_btn = await create_button_raw("whisper", "view_media", "• رؤية الوسائط", switch_inline_query_current_chat=f"W/{whisper_id}")
                inline_keyboard.append([{"text": view_media_btn["text"], "switch_inline_query_current_chat": view_media_btn["switch_inline_query_current_chat"], "style": view_media_btn.get("style", "success")}])

            inline_keyboard.append([{"text": whisper_back_btn["text"], "url": whisper_back_btn["url"], "style": whisper_back_btn.get("style", "success")}])
        
        await c.send_message(
            chat_id,
            message_text,
            parse_mode="HTML",
            reply_markup={"inline_keyboard": inline_keyboard},
            protect_content=True,
        )
        
        await r.hset(key_str, "writer", "")
        await r.expire(f"{Dev_FINAL}:whisper_data:{whisper_id}", 86400)
        return

@Client.on_callback_query(filters.regex(r"^(whisper_view_|whisper_page_|whisper_close_)"), group=-4556446)
async def CallbackQueryHandler(c, m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if m.data.startswith("whisper_view_"):
        wid = m.data.split("_", 2)[2]
        whisper_key = f"{Dev_FINAL}:whisper_data:{wid}"
        page_key = f"{Dev_FINAL}:whisper_page:{wid}:{m.from_user.id}"
        
        if not await r.exists(whisper_key):
            return await m.answer(REPLIES['plugins_whisper_336'], show_alert=True)
            
        data = await r.hgetall(whisper_key)
        target_id = get_str(data, "target_id")
        sender_id = get_str(data, "sender_id")
        
        if str(m.from_user.id) != target_id and str(m.from_user.id) != sender_id:
            try:
                user_name = safe_display_name(m.from_user.first_name or m.from_user.username or "شخص")
                
                reply_markup = InlineKeyboardMarkup([
                    [InlineKeyboardButton(text=user_name, user_id=m.from_user.id)]
                ])
                
                await c.send_message(
                    int(sender_id),
                    f"• الحق الحق\n• ذا ↤︎ {user_name} حاول يقرأ همستك بس ماخليته\n_",
                    reply_markup=reply_markup
                )
            except:
                pass
            
            return await m.answer(REPLIES['plugins_whisper_358'], show_alert=True)
            
        if str(m.from_user.id) == target_id:
            try:
                reader_name = safe_display_name(m.from_user.first_name or m.from_user.username or "الشخص")
                await c.send_message(
                    int(sender_id),
                    f"• قام {reader_name} بقراءة الهمسة\n_"
                )
            except:
                pass
            
        if get_str(data, "type") == "text":
            full_text = get_str(data, "text")
            chunks = chunk_text(full_text, max_chunks=6)
            total_pages = len(chunks)
            
            current_page = await r.get(page_key)
            if current_page is None:
                current_page = 0
            else:
                current_page = int(current_page)
                
            if current_page >= total_pages:
                current_page = 0
                
            page_text = chunks[current_page]
            if total_pages > 1:
                display_text = f"📄 [{current_page + 1}/{total_pages}]\n\n{page_text}"
            else:
                display_text = page_text
                
            try:
                await m.answer(display_text, show_alert=True)
            except Exception as e:
                await m.answer(page_text[:150] + "...", show_alert=True)
            
            next_page = (current_page + 1) % total_pages
            await r.set(page_key, next_page, ex=3600)
        else:
            await m.answer(REPLIES['plugins_whisper_398'], show_alert=True)
        return
