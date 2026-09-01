# Plugins1/FinalMusic/fm_plugins/callbacks.py

from helpers.context import is_sudoer, redis_proxy as r, dev_final_proxy as Dev_FINAL, k_proxy as k
import re
import os
import sqlite3
import asyncio
from functools import wraps
from compat import Client, filters
from compat import CallbackQuery
from compat import FloodWait, QueryIdInvalid
from plugins.FinalMusic import tune, config, logger, queue, tg, yt
from plugins.FinalMusic.fm_helpers import buttons
from helpers.ranks import *

def safe_callback(func):
    @wraps(func)
    async def wrapper(client, query: CallbackQuery):
        try:
            return await func(client, query)
        except QueryIdInvalid:
            return
        except Exception as e:
            logger.error(f"Error in callback {func.__name__}: {e}", exc_info=True)
            try:
                await query.answer("❌ حدث خطأ ما. يرجى المحاولة مرة أخرى.", show_alert=True)
            except:
                pass
    return wrapper

async def can_manage_vc_check(user_id: int, chat_id: int) -> bool:
    # التحقق من رتب البوت أولاً
    if await admin_pls(user_id, chat_id):
        return True
    
    if await is_sudoer(user_id):
        return True
    if await r.sismember(f"auth_users:{chat_id}:{Dev_FINAL}", str(user_id)):
        return True
    admins = await r.smembers(f"chat_admins:{chat_id}:{Dev_FINAL}")
    if user_id in [int(a) for a in admins] if admins else []:
        return True
    return False

async def get_cmode_channel(chat_id: int):
    cmode = await r.get(f"cmode:{chat_id}:{Dev_FINAL}")
    if cmode:
        return int(cmode)
    return None

@Client.on_callback_query(filters.regex("^stargdhdhdhhdhdhdhdht"), group=-100)
@safe_callback
async def _start_callback(client, query: CallbackQuery):
    await query.answer()
    _text = f"مرحباً {query.from_user.first_name}!\nأنا بوت تشغيل الموسيقى.\nاستخدم الأوامر النصية للتحكم بي."
    try:
        await query.edit_message_caption(caption=_text)
    except:
        try:
            await query.edit_message_text(text=_text)
        except:
            pass

@Client.on_callback_query(filters.regex("cancel_dl"), group=-99)
@safe_callback
async def cancel_dl(client, query: CallbackQuery):
    await query.answer()
    await tg.cancel(query)

@Client.on_callback_query(filters.regex("controls"), group=-918)
@safe_callback
async def _controls(client, query: CallbackQuery):
    args = query.data.split()
    action = args[1]
    chat_id = int(args[2])
    button_user_id = 0
    qaction = False
    if len(args) >= 4:
        if args[3] == "q":
            qaction = True
            if len(args) == 5:
                button_user_id = int(args[4])
        else:
            try:
                button_user_id = int(args[3])
            except ValueError:
                pass
    user = query.from_user.mention
    if action == "close":
        if button_user_id != 0:
            if query.from_user.id != button_user_id and not await is_sudoer(query.from_user.id):
                return await query.answer("الامر مو الك يبعدي !", show_alert=True)
        elif query.message.reply_to_message:
            original_user_id = query.message.reply_to_message.from_user.id
            if query.from_user.id != original_user_id and not await is_sudoer(query.from_user.id):
                return await query.answer("الامر مو الك يبعدي !", show_alert=True)
        await query.answer()
        try:
            await query.message.delete()
        except:
            pass
        return
    user_id = query.from_user.id
    if not await can_manage_vc_check(user_id, chat_id):
        return await query.answer("⚠️ عذراً، ليس لديك صلاحية لاستخدام هذا التحكم.", show_alert=True)
    if not await r.get(f"call_active:{chat_id}:{Dev_FINAL}"):
        return await query.answer("لا يوجد تشغيل حالياً", show_alert=True)
    if action == "status":
        return await query.answer()
    if action.startswith("seek_"):
        media = queue.get_current(chat_id)
        if not media or media.is_live:
            return await query.answer("⚠️ لا يمكن التقديم أو التأخير في البث المباشر!", show_alert=True)
        if not media.duration_sec or media.duration_sec == 0:
            return await query.answer("⚠️ لا يمكن التقديم أو التأخير في هذا المسار!", show_alert=True)
        if action == "seek_back_10":
            seconds = -10
        elif action == "seek_back_30":
            seconds = -30
        elif action == "seek_forward_10":
            seconds = 10
        elif action == "seek_forward_30":
            seconds = 30
        else:
            return await query.answer("⚠️ إجراء تقديم/تأخير غير صالح!", show_alert=True)
        current_time = getattr(media, 'time', 0)
        new_time = max(0, min(current_time + seconds, media.duration_sec - 5))
        if new_time == 0 and seconds < 0:
            return await query.answer(f"⏮️ أنت بالفعل في بداية المسار!", show_alert=True)
        if new_time >= media.duration_sec - 5 and seconds > 0:
            return await query.answer(f"⏭️ وقت التقديم قريب جداً من نهاية المسار!", show_alert=True)
        success = await tune.seek_stream(chat_id, int(new_time))
        if success:
            action_word = "تقديم" if seconds > 0 else "تأخير"
            await query.answer(f"✅ تم {action_word}", show_alert=False)
            try:
                sent_msg = await query.message.reply_text(f"• تم {action_word} {abs(seconds)} بواسطة {user}", quote=False)
                await asyncio.sleep(5)
                try:
                    await sent_msg.delete()
                except:
                    pass
            except:
                pass
        return
    if action == "loop":
        current_loop = await r.get(f"loop:{chat_id}:{Dev_FINAL}")
        if current_loop == "0" or not current_loop:
            new_loop = 1
            text_msg = "🔂 التكرار: مسار واحد"
            message = f"🔂 تم ضبط وضع التكرار على: <b>مسار واحد فقط</b>"
        elif current_loop == "1":
            new_loop = 10
            text_msg = "🔁 التكرار: قائمة الانتظار"
            message = f"🔁 تم ضبط وضع التكرار على: <b>قائمة الانتظار بالكامل</b>"
        else:
            new_loop = 0
            text_msg = "➡️ التكرار: معطل"
            message = f"➡️ تم <b>تعطيل</b> وضع التكرار."
        if new_loop == 0:
            await r.delete(f"loop:{chat_id}:{Dev_FINAL}")
        else:
            await r.set(f"loop:{chat_id}:{Dev_FINAL}", str(new_loop))
        await query.answer(text_msg, show_alert=False)
        await query.message.reply_text(message, quote=False)
        return
    if action == "shuffle":
        import random
        items = queue.get_queue(chat_id)
        if not items or len(items) <= 1:
            return await query.answer("⚠️ قائمة الانتظار فارغة أو تحتوي على مسار واحد فقط!", show_alert=True)
        current = items[0] if items else None
        remaining = items[1:] if len(items) > 1 else []
        if not remaining:
            return await query.answer("⚠️ لا توجد مسارات لخلطها!", show_alert=True)
        random.shuffle(remaining)
        queue.clear(chat_id)
        if current:
            queue.add(chat_id, current)
        for item in remaining:
            queue.add(chat_id, item)
        await query.answer("🔀 تم خلط قائمة الانتظار!", show_alert=False)
        await query.message.reply_text(f"🔀 تم <b>خلط</b> قائمة الانتظار ({len(remaining)} مسار)", quote=False)
        return
    await query.answer("جاري المعالجة...", show_alert=True)
    if action == "pause":
        playing_status = await r.get(f"playing:{chat_id}:{Dev_FINAL}")
        if not playing_status or playing_status == "paused":
            return await query.answer("التشغيل متوقف بالفعل", show_alert=True)
        if not await tune.pause(chat_id):
            return await query.answer("لا يوجد تشغيل", show_alert=True)
        if qaction:
            await buttons.edit_queue_markup(client, chat_id, query.message.id, "متوقف", False, user_id=button_user_id)
            return
        reply = f"⏸️ تم الإيقاف المؤقت بواسطة {user}"
    elif action == "resume":
        playing_status = await r.get(f"playing:{chat_id}:{Dev_FINAL}")
        if playing_status and playing_status != "paused":
            return await query.answer("التشغيل ليس متوقفاً", show_alert=True)
        if not await tune.resume(chat_id):
            return await query.answer("لا يوجد تشغيل", show_alert=True)
        if qaction:
            await buttons.edit_queue_markup(client, chat_id, query.message.id, "تشغيل", True, user_id=button_user_id)
            return
        reply = f"▶️ تم الاستئناف بواسطة {user}"
    elif action == "skip":
        await tune.play_next(chat_id)
        reply = f"⏭️ تم التخطي بواسطة {user}"
    elif action == "force":
        pos, media = queue.check_item(chat_id, args[3])
        if not media or pos == -1:
            return await query.edit_message_text("انتهت صلاحية هذا المسار")
        current = queue.get_current(chat_id)
        m_id = current.message_id if current else None
        queue.force_add(chat_id, media, remove=pos)
        try:
            await client.delete_messages(chat_id=chat_id, message_ids=[m_id, media.message_id], revoke=True)
            media.message_id = None
        except:
            pass
        msg = await client.send_message(chat_id=chat_id, text="⏩ جاري تشغيل التالي...")
        is_live_track = getattr(media, "is_live", False)
        is_video_track = getattr(media, "video", False)
        if not is_live_track and not is_video_track:
            try:
                def _check_sqlite_cache(v_id):
                    conn = sqlite3.connect("songs.db")
                    cursor = conn.cursor()
                    cursor.execute("SELECT msg_id FROM songs WHERE yt_id = ?", (v_id,))
                    row = cursor.fetchone()
                    conn.close()
                    return bool(row)
                if await asyncio.to_thread(_check_sqlite_cache, media.id):
                    media.file_path = f"downloads/{media.id}.mp3"
            except:
                pass
        if not media.file_path or not os.path.exists(media.file_path):
            media.file_path = await yt.download(media.id, is_live=is_live_track, video=is_video_track)
        media.message_id = msg.id
        return await tune.play_media(chat_id, msg, media)
    elif action == "replay":
        media = queue.get_current(chat_id)
        media.user = user
        await tune.replay(chat_id)
        reply = f"🔄 تم إعادة التشغيل بواسطة {user}"
    elif action == "stop":
        await tune.stop(chat_id)
        reply = f"⏹️ تم الإيقاف بواسطة {user}"
    try:
        if action in ["skip", "replay", "stop"]:
            sent_msg = None
            try:
                sent_msg = await query.message.reply_text(reply, quote=False)
            except:
                pass
            await query.message.delete()
            if sent_msg:
                await asyncio.sleep(5)
                try:
                    await sent_msg.delete()
                except:
                    pass
        else:
            mtext = query.message.caption.html or query.message.text.html
            await query.edit_message_text(f"{mtext}\n\n<blockquote>{reply}</blockquote>")
            await buttons.edit_controls_markup(client, chat_id, query.message.id, user_id=button_user_id)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        try:
            mtext = query.message.caption.html or query.message.text.html
            await query.edit_message_text(f"{mtext}\n\n<blockquote>{reply}</blockquote>")
            await buttons.edit_controls_markup(client, chat_id, query.message.id, user_id=button_user_id)
        except:
            pass
    except:
        pass
        