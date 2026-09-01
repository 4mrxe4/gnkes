import html
import re
import json
from datetime import datetime
from compat import *
from compat import *
from compat import *
# NOTE: compat.py does `import datetime` (the module) and its __all__
# doesn't exclude that name, so "from compat import *" above re-exports
# the module and overwrites the class imported by
# "from datetime import datetime" earlier in this file. That's what made
# datetime.now(...) fail with "module 'datetime' has no attribute 'now'" —
# it was actually calling module.now() instead of class.now().
# Re-import the class last so it wins.
from datetime import datetime
from helpers.context import get_global_r, get_global_dev, get_global_k
from helpers.ranks import *
from .owners import track_admin_action
from helpers.replies_store import (
    REPLIES,
    plugins_restrict_172,
    plugins_restrict_179,
    plugins_restrict_183,
    plugins_restrict_189,
    plugins_restrict_194,
    plugins_restrict_203,
    plugins_restrict_210,
    plugins_restrict_214,
    plugins_restrict_220,
    plugins_restrict_225,
    plugins_restrict_235,
    plugins_restrict_241,
    plugins_restrict_250,
    plugins_restrict_256,
    plugins_restrict_268,
    plugins_restrict_285,
    plugins_restrict_293,
    plugins_restrict_310,
    plugins_restrict_314,
    plugins_restrict_319,
    plugins_restrict_325,
    plugins_restrict_332,
    plugins_restrict_335,
    plugins_restrict_342,
    plugins_restrict_344,
    plugins_restrict_348,
    plugins_restrict_353,
    plugins_restrict_359,
    plugins_restrict_366,
    plugins_restrict_369,
    plugins_restrict_377,
    plugins_restrict_379,
    plugins_restrict_383,
    plugins_restrict_406,
    plugins_restrict_410,
    plugins_restrict_416,
    plugins_restrict_433,
    plugins_restrict_441,
    plugins_restrict_444,
    plugins_restrict_446,
    plugins_restrict_454,
    plugins_restrict_457,
    plugins_restrict_459,
    plugins_restrict_465,
    plugins_restrict_483,
    plugins_restrict_485,
    plugins_restrict_489,
    plugins_restrict_491,
    plugins_restrict_495,
    plugins_restrict_507,
    plugins_restrict_562,
    plugins_restrict_570,
    plugins_restrict_589,
    plugins_restrict_607,
    plugins_restrict_620,
    plugins_restrict_637,
    plugins_restrict_640,
    plugins_restrict_657,
    plugins_restrict_675,
    plugins_restrict_704,
    plugins_restrict_718,
    plugins_restrict_725,
    plugins_restrict_727,
    plugins_restrict_734,
    plugins_restrict_736,
    plugins_restrict_759,
)


def _extract_reply_media(rep):
    """
    compat.py's `.media` property returns the raw content_type STRING
    (e.g. "text", "sticker", "photo"...) — it is truthy for *every* message,
    including plain text, unlike Pyrogram's `.media` which is None for
    non-media messages. Code below used to gate on `if rep.media:` before
    `elif rep.text:`, so a text-only reply still entered the media branch;
    none of the sticker/animation/photo/video/voice/audio/document checks
    matched, and `file_id` was then used before assignment
    ("cannot access local variable 'file_id' where it is not associated
    with a value"). Check the real attributes directly instead and return
    (file_id, type) or (None, None) when there's no actual media.
    """
    if not rep:
        return None, None
    if rep.sticker:
        return rep.sticker.file_id, "sticker"
    if rep.animation:
        return rep.animation.file_id, "animation"
    if rep.photo:
        return rep.photo.file_id, "photo"
    if rep.video:
        return rep.video.file_id, "video"
    if rep.voice:
        return rep.voice.file_id, "voice"
    if rep.audio:
        return rep.audio.file_id, "audio"
    if rep.document:
        return rep.document.file_id, "document"
    return None, None

async def _notify_blocked_global(m, username: str = None):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    try:
        if username:
            mention = f"<a href='tg://user?id={m.from_user.id}'>{html.escape(str(username))}</a>"
        else:
            mention = m.from_user.mention_html if m.from_user else "المستخدم"
        msg = "• عذراً عزيزي ↤︎「 {} 」\n• هذه الرسالة ممنوعه من قبل المطورين .".format(mention)
        await m.reply(msg, parse_mode="HTML")
    except:
        pass

async def check_text_restrictions(c, m, k):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    if not m.text or not m.from_user or m.from_user.is_bot:
        return False
    
    text_clean = m.text.strip()
    
    global_blocked = await r.smembers(f"GlobalNotAllowedText:{Dev_FINAL}")
    for blocked_word in global_blocked:
        pattern = r'\b' + re.escape(blocked_word) + r'\b'
        if re.search(pattern, text_clean, re.IGNORECASE):
            if await dev2_pls(m.from_user.id, m.chat.id):
                return False
            await m.delete()
            await _notify_blocked_global(m, m.from_user.first_name)
            return True
    
    if await admin_pls(m.from_user.id, m.chat.id):
        return False
    
    local_blocked = await r.smembers(f"{m.chat.id}:NotAllowedListText:{Dev_FINAL}")
    for blocked_word in local_blocked:
        pattern = r'\b' + re.escape(blocked_word) + r'\b'
        if re.search(pattern, text_clean, re.IGNORECASE):
            await m.delete()
            return True
    
    return False

async def check_media_restrictions(c, m, k):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    # See _extract_reply_media() docstring: m.media is always truthy (it's
    # the content_type string), so it can't be used as a "has real media"
    # gate. Check the actual media attributes instead.
    if not (m.sticker or m.animation or m.photo or m.video or m.voice or m.audio or m.document):
        return False
    if not m.from_user or m.from_user.is_bot:
        return False
    
    if m.sticker:
        sticker = m.sticker
        pack_name = sticker.set_name
        
        if pack_name:
            if await r.sismember(f"{m.chat.id}:BlockedPacks:{Dev_FINAL}", pack_name):
                if await admin_pls(m.from_user.id, m.chat.id):
                    return False
                await m.delete()
                return True
        
        file_id = sticker.file_id
        media_id = file_id[-6:]
        
        if await r.get(f"GlobalNotAllow:{media_id}:{Dev_FINAL}"):
            if await dev2_pls(m.from_user.id, m.chat.id):
                return False
            await m.delete()
            await _notify_blocked_global(m, m.from_user.first_name)
            return True
        
        if await admin_pls(m.from_user.id, m.chat.id):
            return False
        
        if await r.get(f"{media_id}:NotAllow:{m.chat.id}{Dev_FINAL}"):
            await m.delete()
            return True
        
        return False
    
    file_id = m.animation.file_id if m.animation else (m.photo.file_id if m.photo else (m.video.file_id if m.video else (m.voice.file_id if m.voice else (m.audio.file_id if m.audio else (m.document.file_id if m.document else None)))))
    if not file_id:
        return False
    media_id = file_id[-6:]
    
    if await r.get(f"GlobalNotAllow:{media_id}:{Dev_FINAL}"):
        if await dev2_pls(m.from_user.id, m.chat.id):
            return False
        await m.delete()
        await _notify_blocked_global(m, m.from_user.first_name)
        return True
    
    if await admin_pls(m.from_user.id, m.chat.id):
        return False
    
    if await r.get(f"{media_id}:NotAllow:{m.chat.id}{Dev_FINAL}"):
        await m.delete()
        return True
    
    return False

async def handle_ban_commands(c, m, text):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if not await check_global_restrictions(c, m, k):
        return

    if text == "منع" and m.reply_to_message:
        if await admin_pls(m.from_user.id, m.chat.id):
            rep = m.reply_to_message
            file_id, type = _extract_reply_media(rep)
            if file_id:
                id = file_id[-6:]
                if await r.get(f"{id}:NotAllow:{m.chat.id}{Dev_FINAL}"):
                    return await m.reply(plugins_restrict_172(k))
                else:
                    await r.set(f"{id}:NotAllow:{m.chat.id}{Dev_FINAL}", 1)
                    await r.sadd(
                        f"{m.chat.id}:NotAllowedList:{Dev_FINAL}",
                        f"file={id}&by={m.from_user.id}&type={type}&file_id={file_id}",
                    )
                    return await m.reply(plugins_restrict_179(k))
            elif rep.text:
                full_text = rep.text.strip()
                if await r.sismember(f"{m.chat.id}:NotAllowedListText:{Dev_FINAL}", full_text):
                    return await m.reply(
                        plugins_restrict_183(k, full_text),
                        disable_web_page_preview=True,
                    )
                else:
                    await r.sadd(f"{m.chat.id}:NotAllowedListText:{Dev_FINAL}", full_text)
                    return await m.reply(
                        plugins_restrict_189(k, full_text),
                        disable_web_page_preview=True,
                    )
            else:
                return await m.reply(plugins_restrict_194(k))

    if text == "الغاء منع" and m.reply_to_message:
        if await admin_pls(m.from_user.id, m.chat.id):
            rep = m.reply_to_message
            file_id, type = _extract_reply_media(rep)
            if file_id:
                id = file_id[-6:]
                if not await r.get(f"{id}:NotAllow:{m.chat.id}{Dev_FINAL}"):
                    return await m.reply(plugins_restrict_203(k))
                else:
                    await r.delete(f"{id}:NotAllow:{m.chat.id}{Dev_FINAL}")
                    await r.srem(
                        f"{m.chat.id}:NotAllowedList:{Dev_FINAL}",
                        f"file={id}&by={m.from_user.id}&type={type}&file_id={file_id}",
                    )
                    return await m.reply(plugins_restrict_210(k))
            elif rep.text:
                full_text = rep.text.strip()
                if not await r.sismember(f"{m.chat.id}:NotAllowedListText:{Dev_FINAL}", full_text):
                    return await m.reply(
                        plugins_restrict_214(k, full_text),
                        disable_web_page_preview=True,
                    )
                else:
                    await r.srem(f"{m.chat.id}:NotAllowedListText:{Dev_FINAL}", full_text)
                    return await m.reply(
                        plugins_restrict_220(k, full_text),
                        disable_web_page_preview=True,
                    )
            else:
                return await m.reply(plugins_restrict_225(k))

    if text.startswith("منع ") and not text.startswith("منع عام") and not text.startswith("منع حزمة") and not text.startswith("منع حزمه"):
        if await admin_pls(m.from_user.id, m.chat.id):
            noice = text.split(None, 1)[1]
            
            if noice in ["حزمة", "حزمه"]:
                return
            
            if await r.sismember(f"{m.chat.id}:NotAllowedListText:{Dev_FINAL}", noice):
                return await m.reply(
                    plugins_restrict_235(k, noice),
                    disable_web_page_preview=True,
                )
            else:
                await r.sadd(f"{m.chat.id}:NotAllowedListText:{Dev_FINAL}", noice)
                return await m.reply(
                    plugins_restrict_241(k, noice),
                    disable_web_page_preview=True,
                )

    if text.startswith("الغاء منع ") and len(text.split()) > 2 and not text.startswith("الغاء منع عام"):
        if await admin_pls(m.from_user.id, m.chat.id):
            noice = text.split(None, 2)[2]
            if not await r.sismember(f"{m.chat.id}:NotAllowedListText:{Dev_FINAL}", noice):
                return await m.reply(
                    plugins_restrict_250(k, noice),
                    disable_web_page_preview=True,
                )
            else:
                await r.srem(f"{m.chat.id}:NotAllowedListText:{Dev_FINAL}", noice)
                return await m.reply(
                    plugins_restrict_256(k, noice),
                    disable_web_page_preview=True,
                )

    if text in ["قائمه المنع", "قائمة المنع"]:
        text1 = "الكلمات الممنوعة ً:\n"
        text2 = "الوسائط الممنوعة ً:\n"
        count = 1
        count2 = 1
        if await admin_pls(m.from_user.id, m.chat.id):
            if not await r.smembers(f"{m.chat.id}:NotAllowedListText:{Dev_FINAL}") and not await r.smembers(f"{m.chat.id}:NotAllowedList:{Dev_FINAL}"):
                return await m.reply(plugins_restrict_268(k))
            else:
                if not await r.smembers(f"{m.chat.id}:NotAllowedListText:{Dev_FINAL}"):
                    text1 += "لايوجد"
                else:
                    for a in await r.smembers(f"{m.chat.id}:NotAllowedListText:{Dev_FINAL}"):
                        text1 += f"{count} - {a}\n"
                        count += 1
                if not await r.smembers(f"{m.chat.id}:NotAllowedList:{Dev_FINAL}"):
                    text2 += "لايوجد"
                else:
                    for a in await r.smembers(f"{m.chat.id}:NotAllowedList:{Dev_FINAL}"):
                        g = a
                        id = g.split("file=")[1].split("&")[0]
                        by = g.split("by=")[1].split("&")[0]
                        type = g.split("type=")[1].split("&")[0]
                        text2 += f"{count2} - (`{id}`) ࿓ ( <a href='tg://user?id={by}'>{html.escape(str(type))}</a> )\n"
                return await m.reply(plugins_restrict_285(text1, text2), disable_web_page_preview=True)

    if text in ["مسح قائمه المنع", "مسح قائمة المنع"]:
        if await admin_pls(m.from_user.id, m.chat.id):
            texts_exist = await r.smembers(f"{m.chat.id}:NotAllowedListText:{Dev_FINAL}")
            media_exist = await r.smembers(f"{m.chat.id}:NotAllowedList:{Dev_FINAL}")
            
            if not texts_exist and not media_exist:
                return await m.reply(plugins_restrict_293(k))
            else:
                if texts_exist:
                    for txt in texts_exist:
                        await r.srem(f"{m.chat.id}:NotAllowedListText:{Dev_FINAL}", txt)
                    await r.delete(f"{m.chat.id}:NotAllowedListText:{Dev_FINAL}")
                
                if media_exist:
                    for a in media_exist:
                        try:
                            file_id = a.split("file=")[1].split("&by=")[0]
                            await r.delete(f"{file_id}:NotAllow:{m.chat.id}{Dev_FINAL}")
                        except:
                            pass
                        await r.srem(f"{m.chat.id}:NotAllowedList:{Dev_FINAL}", a)
                    await r.delete(f"{m.chat.id}:NotAllowedList:{Dev_FINAL}")
                
                return await m.reply(plugins_restrict_310(k))

    if text == "منع عام" and m.reply_to_message:
        if not await dev2_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_restrict_314(k))
        rep = m.reply_to_message
        if rep.text:
            full_text = rep.text.strip()
            if await r.sismember(f"GlobalNotAllowedText:{Dev_FINAL}", full_text):
                return await m.reply(
                    plugins_restrict_319(k, full_text),
                    disable_web_page_preview=True,
                )
            else:
                await r.sadd(f"GlobalNotAllowedText:{Dev_FINAL}", full_text)
                return await m.reply(
                    plugins_restrict_325(k, full_text),
                    disable_web_page_preview=True,
                )
        elif rep.media:
            file_id, media_type = _extract_reply_media(rep)
            if not file_id:
                return await m.reply(plugins_restrict_332(k))
            media_id = file_id[-6:]
            if await r.get(f"GlobalNotAllow:{media_id}:{Dev_FINAL}"):
                return await m.reply(plugins_restrict_335(k))
            else:
                await r.set(f"GlobalNotAllow:{media_id}:{Dev_FINAL}", 1)
                await r.sadd(
                    f"GlobalNotAllowedList:{Dev_FINAL}",
                    f"file={media_id}&by={m.from_user.id}&type={media_type}&file_id={file_id}",
                )
                return await m.reply(plugins_restrict_342(k))
        else:
            return await m.reply(plugins_restrict_344(k))

    if text == "الغاء منع عام" and m.reply_to_message:
        if not await dev2_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_restrict_348(k))
        rep = m.reply_to_message
        if rep.text:
            full_text = rep.text.strip()
            if not await r.sismember(f"GlobalNotAllowedText:{Dev_FINAL}", full_text):
                return await m.reply(
                    plugins_restrict_353(k, full_text),
                    disable_web_page_preview=True,
                )
            else:
                await r.srem(f"GlobalNotAllowedText:{Dev_FINAL}", full_text)
                return await m.reply(
                    plugins_restrict_359(k, full_text),
                    disable_web_page_preview=True,
                )
        elif rep.media:
            file_id, _media_type = _extract_reply_media(rep)
            if not file_id:
                return await m.reply(plugins_restrict_366(k))
            media_id = file_id[-6:]
            if not await r.get(f"GlobalNotAllow:{media_id}:{Dev_FINAL}"):
                return await m.reply(plugins_restrict_369(k))
            else:
                await r.delete(f"GlobalNotAllow:{media_id}:{Dev_FINAL}")
                global_media = await r.smembers(f"GlobalNotAllowedList:{Dev_FINAL}")
                for media in global_media:
                    if f"file={media_id}" in media:
                        await r.srem(f"GlobalNotAllowedList:{Dev_FINAL}", media)
                        break
                return await m.reply(plugins_restrict_377(k))
        else:
            return await m.reply(plugins_restrict_379(k))

    if text in ["قائمة المنع العام", "قائمه المنع العام"]:
        if not await dev2_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_restrict_383(k))
        text1 = "الكلمات الممنوعة عام:\n"
        text2 = "الوسائط الممنوعة عام:\n"
        count = 1
        count2 = 1
        global_texts = await r.smembers(f"GlobalNotAllowedText:{Dev_FINAL}")
        if not global_texts:
            text1 += "لايوجد\n"
        else:
            for txt in global_texts:
                text1 += f"{count} - {txt}\n"
                count += 1
        global_media = await r.smembers(f"GlobalNotAllowedList:{Dev_FINAL}")
        if not global_media:
            text2 += "لايوجد\n"
        else:
            for media in global_media:
                parts = media.split("&")
                media_id = parts[0].split("=")[1]
                by = parts[1].split("=")[1]
                media_type = parts[2].split("=")[1]
                text2 += f"{count2} - (`{media_id}`) ࿓ ( <a href='tg://user?id={by}'>{html.escape(str(media_type))}</a> )\n"
                count2 += 1
        return await m.reply(plugins_restrict_406(text1, text2), disable_web_page_preview=True)

    if text in ["مسح قائمة المنع العام", "مسح قائمه المنع العام"]:
        if not await dev2_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_restrict_410(k))
        
        texts_exist = await r.smembers(f"GlobalNotAllowedText:{Dev_FINAL}")
        media_exist = await r.smembers(f"GlobalNotAllowedList:{Dev_FINAL}")
        
        if not texts_exist and not media_exist:
            return await m.reply(plugins_restrict_416(k))
        
        if texts_exist:
            for txt in texts_exist:
                await r.srem(f"GlobalNotAllowedText:{Dev_FINAL}", txt)
            await r.delete(f"GlobalNotAllowedText:{Dev_FINAL}")
        
        if media_exist:
            for media in media_exist:
                try:
                    media_id = media.split("file=")[1].split("&")[0]
                    await r.delete(f"GlobalNotAllow:{media_id}:{Dev_FINAL}")
                except:
                    pass
                await r.srem(f"GlobalNotAllowedList:{Dev_FINAL}", media)
            await r.delete(f"GlobalNotAllowedList:{Dev_FINAL}")
        
        return await m.reply(plugins_restrict_433(k))

    if text == "منع حزمه" and m.reply_to_message and m.reply_to_message.sticker:
        if await admin_pls(m.from_user.id, m.chat.id):
            sticker = m.reply_to_message.sticker
            pack_name = sticker.set_name
            
            if not pack_name:
                return await m.reply(plugins_restrict_441(k))
            
            await r.sadd(f"{m.chat.id}:BlockedPacks:{Dev_FINAL}", pack_name)
            return await m.reply(plugins_restrict_444(k, pack_name))
        else:
            return await m.reply(plugins_restrict_446(k))
    
    if text == "فتح الحزمه" and m.reply_to_message and m.reply_to_message.sticker:
        if await admin_pls(m.from_user.id, m.chat.id):
            sticker = m.reply_to_message.sticker
            pack_name = sticker.set_name
            
            if not pack_name:
                return await m.reply(plugins_restrict_454(k))
            
            await r.srem(f"{m.chat.id}:BlockedPacks:{Dev_FINAL}", pack_name)
            return await m.reply(plugins_restrict_457(k, pack_name))
        else:
            return await m.reply(plugins_restrict_459(k))
    
    if text in ["الحزم الممنوعه", "قائمه الحزم الممنوعه"]:
        if await admin_pls(m.from_user.id, m.chat.id):
            packs = await r.smembers(f"{m.chat.id}:BlockedPacks:{Dev_FINAL}")
            if not packs:
                return await m.reply(plugins_restrict_465(k))
            
            text_result = "الحزم الممنوعة:\n"
            for i, pack in enumerate(packs, 1):
                text_result += f"{i} - `{pack}`\n"
            return await m.reply(text_result)

    return None

async def handle_aktomoh_commands(c, m, text):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if not await check_global_restrictions(c, m, k):
        return

    if text == "تفعيل اكتموه":
        if not await admin_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_restrict_483(k))
        await r.set(f"{m.chat.id}:AktomohEnabled:{Dev_FINAL}", 1)
        return await m.reply(plugins_restrict_485(k))

    if text == "تعطيل اكتموه":
        if not await admin_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_restrict_489(k))
        await r.delete(f"{m.chat.id}:AktomohEnabled:{Dev_FINAL}")
        return await m.reply(plugins_restrict_491(k))

    if text == "اكتموه":
        if not await r.get(f"{m.chat.id}:AktomohEnabled:{Dev_FINAL}"):
            return await m.reply(plugins_restrict_495(k))
        
        if not await mod_pls(m.from_user.id, m.chat.id):
            return
        
        if not m.reply_to_message or not m.reply_to_message.from_user:
            return
        
        target_user = m.reply_to_message.from_user
        
        if await admin_pls(target_user.id, m.chat.id):
            rank = await get_rank(target_user.id, m.chat.id)
            return await m.reply(plugins_restrict_507(k, rank))
        
        if target_user.is_bot or target_user.id == m.from_user.id:
            return
        
        target_mention = f"<a href='tg://user?id={target_user.id}'>{html.escape(str(target_user.first_name))}</a>"
        
        msg_text = f"{k} المستخدم ↤︎「 {target_mention} 」\n{k} هل يستاهل الكتم ؟\n\n{k} التصويت من 3 اشخاص\n_"
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("موافق اكتموه 0", callback_data=f"aktomoh_yes:{target_user.id}")],
            [InlineKeyboardButton("لاتكتموه 0", callback_data=f"aktomoh_no:{target_user.id}")]
        ])
        
        await m.reply_to_message.reply(msg_text, reply_markup=keyboard, parse_mode=ParseMode.HTML)
        return True

    return None

async def check_all_restrictions(c, m, k):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    if not m.from_user:
        return False
    if m.from_user.is_bot:
        return False
    
    if await r.sismember(f"{m.chat.id}:listMUTE:{Dev_FINAL}", m.from_user.id):
        await m.delete()
        return True
    
    if m.text:
        return await check_text_restrictions(c, m, k)
    
    if m.sticker or m.animation or m.photo or m.video or m.voice or m.audio or m.document:
        return await check_media_restrictions(c, m, k)
    
    return False

async def handle_warn_commands(c, m, text):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if not await check_global_restrictions(c, m, k):
        return

    if text == "انذار" and m.reply_to_message:
        if not await admin_pls(m.from_user.id, m.chat.id):
            return
        
        target_user = m.reply_to_message.from_user
        if not target_user or target_user.is_bot:
            return

        if await admin_pls(target_user.id, m.chat.id):
            return await m.reply(plugins_restrict_562(k))
        
        warn_key = f"{m.chat.id}:WarnCount:{target_user.id}"
        current_warns = await r.incr(warn_key)
        
        if current_warns < 4:
            remaining = 4 - current_warns
            await track_admin_action(m.chat.id, m.from_user.id, "warn")
            return await m.reply(
                plugins_restrict_570(k, k, remaining)
            )
        else:
            admin_key = f"{m.chat.id}:warn_admin:{target_user.id}"
            await r.set(admin_key, m.from_user.id)
            
            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("حظر", callback_data=f"warn_ban:{target_user.id}"),
                    InlineKeyboardButton("تقييد", callback_data=f"warn_res:{target_user.id}")
                ],
                [
                    InlineKeyboardButton("سماح", callback_data=f"warn_allow:{target_user.id}")
                ]
            ])
            await r.set(warn_key, 4)
            await track_admin_action(m.chat.id, m.from_user.id, "warn")
            return await m.reply(
                plugins_restrict_589(k, k),
                reply_markup=keyboard
            )
    
    if text == "انذاراته" and m.reply_to_message:
        if not await admin_pls(m.from_user.id, m.chat.id):
            return
        
        target_user = m.reply_to_message.from_user
        if not target_user or target_user.is_bot:
            return
            
        warn_key = f"{m.chat.id}:WarnCount:{target_user.id}"
        current_warns = await r.get(warn_key) or 0
        current_warns = int(current_warns)
        
        return await m.reply(
            plugins_restrict_607(k, target_user.mention(), k, current_warns)
        )

    if text == "انذاراتي":
        if not m.from_user:
            return
            
        warn_key = f"{m.chat.id}:WarnCount:{m.from_user.id}"
        current_warns = await r.get(warn_key) or 0
        current_warns = int(current_warns)
        
        return await m.reply(
            plugins_restrict_620(k, m.from_user.mention(), k, current_warns)
        )

    if text == "مسح انذاراته" and m.reply_to_message:
        if not await admin_pls(m.from_user.id, m.chat.id):
            return
        
        target_user = m.reply_to_message.from_user
        if not target_user or target_user.is_bot:
            return
            
        warn_key = f"{m.chat.id}:WarnCount:{target_user.id}"
        
        current_warns = await r.get(warn_key)
        if not current_warns or int(current_warns) == 0:
            return await m.reply(plugins_restrict_637(k, target_user.mention()))
            
        await r.delete(warn_key)
        return await m.reply(plugins_restrict_640(k, target_user.mention()))

    return None

async def handle_general_commands(c, m, text):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if not await check_global_restrictions(c, m, k):
        return

    if text.startswith("مسح ") and len(text.split()) == 2 and re.findall("[0-9]+", text):
        count = int(re.findall("[0-9]+", text)[0])
        if not await admin_pls(m.from_user.id, m.chat.id) and not await fake_rank_pls(m.from_user.id, m.chat.id, 'delete'):
            return await m.delete()
        else:
            if count > 400:
                return await m.reply(plugins_restrict_657(k))
            else:
                for msg in range(m.id, m.id - count, -1):
                    try:
                        await c.delete_messages(m.chat.id, msg)
                    except:
                        pass

    if text == "مسح" and m.reply_to_message:
        if await admin_pls(m.from_user.id, m.chat.id) or await fake_rank_pls(m.from_user.id, m.chat.id, 'delete'):
            await m.reply_to_message.delete()
            await m.delete()
        else:
            await m.delete()

    if text == "مين ضافني":
        get = (await m.chat.get_member(m.from_user.id)).invited_by
        if not get:
            return await m.reply(plugins_restrict_675(k))
        else:
            return await m.reply(get.mention())

    return None
    
    
@Client.on_callback_query(filters.regex(r"^warn_"), group=-132)
async def handle_warn_buttons(c, cb: CallbackQuery):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if not cb.message: return
    chat_id = cb.message.chat.id
    parts = cb.data.split(":")
    if len(parts) < 2 or not parts[1].isdigit():
        return await cb.answer(REPLIES['plugins_owners_399'], show_alert=True)
    action = parts[0]
    target_id = int(parts[1])
    admin_key = f"{chat_id}:warn_admin:{target_id}"
    expected_admin_id = await r.get(admin_key)
    if not expected_admin_id:
        return await cb.answer(REPLIES['plugins_restrict_697'], show_alert=True)
    if cb.from_user.id != int(expected_admin_id):
        try:
            admin_user = await c.get_users(int(expected_admin_id))
            admin_name = admin_user.first_name
        except:
            admin_name = "مشرف"
        return await cb.answer(plugins_restrict_704(admin_name), show_alert=True)
    if not await admin_pls(cb.from_user.id, chat_id):
        return await cb.answer(REPLIES['plugins_restrict_706'], show_alert=True)
    warn_key = f"{chat_id}:WarnCount:{target_id}"
    try:
        target_member = await cb.message.chat.get_member(target_id)
        target_mention = target_member.user.mention()
    except:
        target_mention = "العضو"

    if action == "warn_allow":
        await r.delete(warn_key)
        await r.delete(admin_key)
        await cb.answer(REPLIES['plugins_restrict_717'])
        await cb.message.edit_text(plugins_restrict_718(k, target_mention, k))
    elif action == "warn_ban":
        try:
            await cb.message.chat.ban_member(target_id)
            await r.delete(warn_key)
            await r.delete(admin_key)
            await cb.answer(REPLIES['plugins_restrict_724'])
            await cb.message.edit_text(plugins_restrict_725(k, target_mention, k))
        except Exception as e:
            await cb.answer(plugins_restrict_727(e), show_alert=True)
    elif action == "warn_res":
        try:
            await c.restrict_chat_member(chat_id, target_id, ChatPermissions(can_send_messages=False))
            await r.delete(warn_key)
            await r.delete(admin_key)
            await cb.answer(REPLIES['plugins_restrict_733'])
            await cb.message.edit_text(plugins_restrict_734(k, target_mention, k))
        except Exception as e:
            await cb.answer(plugins_restrict_736(e), show_alert=True)

@Client.on_callback_query(filters.regex(r"^aktomoh_"), group=-135)
async def handle_aktomoh_buttons(c, cb: CallbackQuery):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if not cb.message:
        return
    chat_id = cb.message.chat.id
    data = cb.data.split(":")
    if len(data) < 2 or not data[1].isdigit():
        return await cb.answer(REPLIES['plugins_owners_399'], show_alert=True)
    action = data[0]
    target_id = int(data[1])
    user_id = cb.from_user.id
    
    if user_id == target_id:
        return await cb.answer(REPLIES['plugins_restrict_754'], show_alert=True)
    
    try:
        if await admin_pls(target_id, chat_id):
            rank = await get_rank(target_id, chat_id)
            return await cb.answer(plugins_restrict_759(rank), show_alert=True)
    except:
        pass
    
    vote_key = f"{chat_id}:aktomoh_vote:{cb.message.id}:{user_id}"
    if await r.get(vote_key):
        return await cb.answer(REPLIES['plugins_restrict_765'], show_alert=True)
    
    vote_type = "yes" if action == "aktomoh_yes" else "no"
    await r.set(vote_key, vote_type)
    
    yes_count_key = f"{chat_id}:aktomoh_yes_count:{cb.message.id}"
    no_count_key = f"{chat_id}:aktomoh_no_count:{cb.message.id}"
    
    if vote_type == "yes":
        yes_count = await r.incr(yes_count_key)
        no_count = int(await r.get(no_count_key) or 0)
    else:
        no_count = await r.incr(no_count_key)
        yes_count = int(await r.get(yes_count_key) or 0)
    
    try:
        target_member = await c.get_users(target_id)
        target_mention = f"<a href='tg://user?id={target_id}'>{html.escape(str(target_member.first_name))}</a>"
    except:
        target_mention = "المستخدم"
    
    if yes_count >= 3:
        await r.set(f"{target_id}:mute:{chat_id}{Dev_FINAL}", 1)
        await r.sadd(f"{chat_id}:listMUTE:{Dev_FINAL}", target_id)
        
        now = datetime.now()
        date_str = now.strftime("%Y/%m/%d")
        time_str = now.strftime("%I:%M%p")
        await r.set(f"{target_id}:mute_admin:{chat_id}{Dev_FINAL}", cb.from_user.id)
        await r.set(f"{target_id}:mute_msg:{chat_id}{Dev_FINAL}", cb.message.id)
        await r.set(f"{target_id}:mute_date:{chat_id}{Dev_FINAL}", date_str)
        await r.set(f"{target_id}:mute_time:{chat_id}{Dev_FINAL}", time_str)
        
        await r.delete(vote_key)
        final_text = f"• المستخدم ↤︎「 {target_mention} 」 \n•  تم كتمه\n_"
        await cb.message.edit_text(final_text, parse_mode=ParseMode.HTML, reply_markup=None)
        return await cb.answer(REPLIES['plugins_restrict_801'])
        
    elif no_count >= 3:
        await r.delete(vote_key)
        final_text = f"• المستخدم ↤︎「 {target_mention} 」 \n• لم يتم كتمه\n_"
        await cb.message.edit_text(final_text, parse_mode=ParseMode.HTML, reply_markup=None)
        return await cb.answer(REPLIES['plugins_restrict_807'])
    else:
        updated_text = f"{k} عدد التصويت ضد ↤︎「 {target_mention} 」\n_"
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"موافق اكتموه {yes_count}", callback_data=f"aktomoh_yes:{target_id}")],
            [InlineKeyboardButton(f"لاتكتموه {no_count}", callback_data=f"aktomoh_no:{target_id}")]
        ])
        await cb.message.edit_text(updated_text, reply_markup=keyboard, parse_mode=ParseMode.HTML)

@Client.on_message(filters.group & ~filters.bot, group=-134)
async def moderation_handler(c, m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if not m.text:
        return
    
    text = m.text
    
    if await check_all_restrictions(c, m, k):
        return
    
    if await handle_aktomoh_commands(c, m, text):
        return
    
    if await handle_warn_commands(c, m, text):
        return
    
    if await handle_ban_commands(c, m, text):
        return
    
    await handle_general_commands(c, m, text)