from helpers.context import get_redis, get_dev_final
import asyncio
import time
from helpers.http import telegram_api_post
from collections import defaultdict
from compat import Client, filters
from compat import MessageDeleteForbidden, FloodWait
from compat import MessageEntityType, ParseMode
from compat import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from helpers.ranks import *
from .protect import run_async_in_thread
from .buttons import register_buttons, get_button_custom, get_button_color, create_button_raw
import settings
from helpers.replies_store import (
    REPLIES,
    plugins_cleanup_593,
    plugins_cleanup_601,
    plugins_cleanup_608,
    plugins_cleanup_613,
    plugins_cleanup_619,
    plugins_cleanup_625,
    plugins_cleanup_631,
    plugins_cleanup_634,
    plugins_cleanup_638,
    plugins_cleanup_640,
    plugins_cleanup_644,
    plugins_cleanup_646,
    plugins_cleanup_650,
    plugins_cleanup_653,
    plugins_cleanup_656,
    plugins_cleanup_666,
    plugins_cleanup_669,
    plugins_cleanup_672,
    plugins_cleanup_678,
    plugins_cleanup_684,
    plugins_cleanup_687,
    plugins_cleanup_693,
    plugins_cleanup_696,
    plugins_cleanup_701,
    plugins_cleanup_705,
    plugins_cleanup_708,
    plugins_cleanup_725,
    plugins_cleanup_727,
)

BUTTONS_DEFINITIONS = {
    "clean": {
        "name": "أزرار التنظيف",
        "buttons": [
            {"id": "toggle_clean", "default": "التنظيف"},
            {"id": "toggle_smart", "default": "التنظيف الذكي"},
            {"id": "toggle_auto", "default": "التلقائي"},
            {"id": "toggle_channel", "default": "القنوات"},
            {"id": "toggle_gifs", "default": "القيفات"},
            {"id": "toggle_videos", "default": "الفيديوهات"},
            {"id": "toggle_photos", "default": "الصور"},
            {"id": "toggle_stickers", "default": "الملصقات"},
            {"id": "toggle_custom_emoji", "default": "الملصقات المميزه"},
            {"id": "toggle_audio", "default": "الاغاني"},
            {"id": "toggle_urls", "default": "المواقع"},
            {"id": "toggle_voice", "default": "الفويسات"},
            {"id": "toggle_files", "default": "الملفات"},
            {"id": "toggle_links_users", "default": "الروابط واليوزرات"},
            {"id": "toggle_contacts", "default": "الجهات"},
            {"id": "toggle_channels", "default": "القنوات"},
            {"id": "toggle_video_note", "default": "بصمات الفيديو"},
            {"id": "toggle_edited", "default": "الرسائل المعدّلة"},
            {"id": "set_count", "default": "عدد التنظيف"},
            {"id": "set_interval", "default": "وقت التنظيف"},
            {"id": "toggle_notify", "default": "اشعارات التنظيف"},
            {"id": "clean_close", "default": "اخفاء الاوامر"},
        ]
    }
}

register_buttons(BUTTONS_DEFINITIONS)

def _k(chat_id, field):
    Dev_FINAL = get_dev_final()
    return f"{Dev_FINAL}:clean:{chat_id}:{field}"

async def _get_settings(chat_id):
    r = get_redis()
    keys = [
        "gifs", "videos", "video_note", "photos", "stickers",
        "custom_emoji", "audio", "urls", "voice",
        "files", "links_users", "contacts", "channels", "edited",
        "auto_clean", "smart_clean", "channel_clean",
        "count", "interval", "notify",
        "disabled",
    ]
    raw = await asyncio.gather(*[r.get(_k(chat_id, k)) for k in keys])
    d = dict(zip(keys, raw))

    def b(v): 
        if v is None:
            return False
        if isinstance(v, bytes):
            v = v.decode()
        return str(v) != "0"

    return {
        "gifs":          b(d["gifs"]),
        "videos":        b(d["videos"]),
        "video_note":    b(d["video_note"]),
        "photos":        b(d["photos"]),
        "stickers":      b(d["stickers"]),
        "custom_emoji":  b(d["custom_emoji"]),
        "audio":         b(d["audio"]),
        "urls":          b(d["urls"]),
        "voice":         b(d["voice"]),
        "files":         b(d["files"]),
        "links_users":   b(d["links_users"]),
        "contacts":      b(d["contacts"]),
        "channels":      b(d["channels"]),
        "edited":        b(d["edited"]),
        "auto_clean":    b(d["auto_clean"]),
        "smart_clean":   b(d["smart_clean"]),
        "channel_clean": b(d["channel_clean"]),
        "count":    int(d["count"])    if d["count"]    else 10,
        "interval": int(d["interval"]) if d["interval"] else 300,
        "notify":   b(d["notify"]) if d["notify"] is not None else True,
        "disabled": b(d["disabled"]) if d["disabled"] is not None else True,
    }

async def _toggle(chat_id, field):
    r = get_redis()
    key = _k(chat_id, field)
    val = await r.get(key)
    if val is not None:
        if isinstance(val, bytes):
            val = val.decode()
        if str(val) != "0":
            await r.set(key, 0)
            return False
    await r.set(key, 1)
    return True

async def _set_val(chat_id, field, value):
    r = get_redis()
    await r.set(_k(chat_id, field), value)

async def _get_botkey():
    r = get_redis()
    Dev_FINAL = get_dev_final()
    k = await r.get(f"{Dev_FINAL}:botkey") or b""
    return k.decode() if isinstance(k, bytes) else k

_TYPE_ALIASES = {
    "الصور":              "photos",
    "الفيديوهات":         "videos",
    "بصمات الفيديو":     "video_note",
    "القيفات":            "gifs",
    "الملصقات":           "stickers",
    "الاغاني":            "audio",
    "الفويسات":           "voice",
    "المواقع":            "urls",
    "الملفات":            "files",
    "الروابط":            "links_users",
    "اليوزرات":           "links_users",
    "الروابط واليوزرات": "links_users",
    "الجهات":             "contacts",
    "القنوات":            "channels",
    "الملصقات المميزه":"custom_emoji",
    "الرسائل المعدلة":   "edited",
    "الرسائل المعدّلة":  "edited",
}

_TYPE_LABELS = {
    "photos":       "الصور",
    "videos":       "الفيديوهات",
    "video_note":   "بصمات الفيديو",
    "gifs":         "القيفات",
    "stickers":     "الملصقات",
    "audio":        "الاغاني",
    "voice":        "الفويسات",
    "urls":         "المواقع",
    "files":        "الملفات",
    "links_users":  "الروابط واليوزرات",
    "contacts":     "الجهات",
    "channels":     "القنوات",
    "custom_emoji": "الملصقات المميزه",
    "edited":       "الرسائل المعدّلة",
}

def _icon(active): return "✓" if active else "✗"

async def _build_keyboard(s, user_id):
    enabled = not s["disabled"]

    toggle_clean = await create_button_raw("clean", "toggle_clean", "التنظيف", callback_data=f"clean_toggle:disabled:{user_id}")
    toggle_smart = await create_button_raw("clean", "toggle_smart", "التنظيف الذكي", callback_data=f"clean_toggle:smart_clean:{user_id}")
    toggle_auto = await create_button_raw("clean", "toggle_auto", "التلقائي", callback_data=f"clean_toggle:auto_clean:{user_id}")
    toggle_channel = await create_button_raw("clean", "toggle_channel", "القنوات", callback_data=f"clean_toggle:channel_clean:{user_id}")
    toggle_gifs = await create_button_raw("clean", "toggle_gifs", "القيفات", callback_data=f"clean_toggle:gifs:{user_id}")
    toggle_videos = await create_button_raw("clean", "toggle_videos", "الفيديوهات", callback_data=f"clean_toggle:videos:{user_id}")
    toggle_photos = await create_button_raw("clean", "toggle_photos", "الصور", callback_data=f"clean_toggle:photos:{user_id}")
    toggle_stickers = await create_button_raw("clean", "toggle_stickers", "الملصقات", callback_data=f"clean_toggle:stickers:{user_id}")
    toggle_custom_emoji = await create_button_raw("clean", "toggle_custom_emoji", "الملصقات المميزه", callback_data=f"clean_toggle:custom_emoji:{user_id}")
    toggle_audio = await create_button_raw("clean", "toggle_audio", "الاغاني", callback_data=f"clean_toggle:audio:{user_id}")
    toggle_urls = await create_button_raw("clean", "toggle_urls", "المواقع", callback_data=f"clean_toggle:urls:{user_id}")
    toggle_voice = await create_button_raw("clean", "toggle_voice", "الفويسات", callback_data=f"clean_toggle:voice:{user_id}")
    toggle_files = await create_button_raw("clean", "toggle_files", "الملفات", callback_data=f"clean_toggle:files:{user_id}")
    toggle_links_users = await create_button_raw("clean", "toggle_links_users", "الروابط واليوزرات", callback_data=f"clean_toggle:links_users:{user_id}")
    toggle_contacts = await create_button_raw("clean", "toggle_contacts", "الجهات", callback_data=f"clean_toggle:contacts:{user_id}")
    toggle_channels = await create_button_raw("clean", "toggle_channels", "القنوات", callback_data=f"clean_toggle:channels:{user_id}")
    toggle_video_note = await create_button_raw("clean", "toggle_video_note", "بصمات الفيديو", callback_data=f"clean_toggle:video_note:{user_id}")
    toggle_edited = await create_button_raw("clean", "toggle_edited", "الرسائل المعدّلة", callback_data=f"clean_toggle:edited:{user_id}")
    set_count = await create_button_raw("clean", "set_count", "عدد التنظيف", callback_data=f"clean_set:count:{user_id}")
    set_interval = await create_button_raw("clean", "set_interval", "وقت التنظيف", callback_data=f"clean_set:interval:{user_id}")
    toggle_notify = await create_button_raw("clean", "toggle_notify", "اشعارات التنظيف", callback_data=f"clean_toggle:notify:{user_id}")
    clean_close = await create_button_raw("clean", "clean_close", "اخفاء الاوامر", callback_data=f"clean_close:{user_id}")

    iv = s["interval"]
    interval_label = f"{iv // 60}د" if iv >= 60 and iv % 60 == 0 else f"{iv}ث"

    keyboard = [
        [
            {"text": f"{_icon(enabled)} {toggle_clean['text']}", "callback_data": toggle_clean["callback_data"], "style": toggle_clean.get("style", "default")},
            {"text": f"{_icon(s['smart_clean'])} {toggle_smart['text']}", "callback_data": toggle_smart["callback_data"], "style": toggle_smart.get("style", "default")}
        ],
        [
            {"text": f"{_icon(s['auto_clean'])} {toggle_auto['text']}", "callback_data": toggle_auto["callback_data"], "style": toggle_auto.get("style", "default")},
            {"text": f"{_icon(s['channel_clean'])} {toggle_channel['text']}", "callback_data": toggle_channel["callback_data"], "style": toggle_channel.get("style", "default")}
        ],
        [
            {"text": f"{_icon(s['gifs'])} {toggle_gifs['text']}", "callback_data": toggle_gifs["callback_data"], "style": toggle_gifs.get("style", "default")},
            {"text": f"{_icon(s['videos'])} {toggle_videos['text']}", "callback_data": toggle_videos["callback_data"], "style": toggle_videos.get("style", "default")}
        ],
        [
            {"text": f"{_icon(s['photos'])} {toggle_photos['text']}", "callback_data": toggle_photos["callback_data"], "style": toggle_photos.get("style", "default")},
            {"text": f"{_icon(s['stickers'])} {toggle_stickers['text']}", "callback_data": toggle_stickers["callback_data"], "style": toggle_stickers.get("style", "default")}
        ],
        [
            {"text": f"{_icon(s['custom_emoji'])} {toggle_custom_emoji['text']}", "callback_data": toggle_custom_emoji["callback_data"], "style": toggle_custom_emoji.get("style", "default")},
            {"text": f"{_icon(s['audio'])} {toggle_audio['text']}", "callback_data": toggle_audio["callback_data"], "style": toggle_audio.get("style", "default")}
        ],
        [
            {"text": f"{_icon(s['urls'])} {toggle_urls['text']}", "callback_data": toggle_urls["callback_data"], "style": toggle_urls.get("style", "default")},
            {"text": f"{_icon(s['voice'])} {toggle_voice['text']}", "callback_data": toggle_voice["callback_data"], "style": toggle_voice.get("style", "default")}
        ],
        [
            {"text": f"{_icon(s['files'])} {toggle_files['text']}", "callback_data": toggle_files["callback_data"], "style": toggle_files.get("style", "default")},
            {"text": f"{_icon(s['links_users'])} {toggle_links_users['text']}", "callback_data": toggle_links_users["callback_data"], "style": toggle_links_users.get("style", "default")}
        ],
        [
            {"text": f"{_icon(s['contacts'])} {toggle_contacts['text']}", "callback_data": toggle_contacts["callback_data"], "style": toggle_contacts.get("style", "default")},
            {"text": f"{_icon(s['channels'])} {toggle_channels['text']}", "callback_data": toggle_channels["callback_data"], "style": toggle_channels.get("style", "default")}
        ],
        [
            {"text": f"{_icon(s['video_note'])} {toggle_video_note['text']}", "callback_data": toggle_video_note["callback_data"], "style": toggle_video_note.get("style", "default")},
            {"text": f"{_icon(s['edited'])} {toggle_edited['text']}", "callback_data": toggle_edited["callback_data"], "style": toggle_edited.get("style", "default")}
        ],
        [
            {"text": f"{set_count['text']} {s['count']}", "callback_data": set_count["callback_data"], "style": set_count.get("style", "default")},
            {"text": f"{set_interval['text']} {interval_label}", "callback_data": set_interval["callback_data"], "style": set_interval.get("style", "default")}
        ],
        [
            {"text": f"{_icon(s['notify'])} {toggle_notify['text']}", "callback_data": toggle_notify["callback_data"], "style": toggle_notify.get("style", "default")}
        ],
        [
            {"text": clean_close['text'], "callback_data": clean_close["callback_data"], "style": clean_close.get("style", "default")}
        ],
    ]
    
    return keyboard

def _build_main_text(s, k):
    auto  = _icon(s["auto_clean"])
    smart = _icon(s["smart_clean"])
    ch    = _icon(s["channel_clean"])
    enabled = not s["disabled"]
    status = "مفعل" if enabled else "معطل"
    return (
        f"{k} أهلاً بك عزيزي في قسم التنظيف لقروبك\n\n"
        f"• حالة التنظيف ↤︎ {status}\n"
        f"• التنظيف التلقائي ↤︎{auto}\n"
        f"• التنظيف الذكي ↤︎{smart}\n"
        f"• التنظيف للقنوات ↤︎{ch}\n\n"
        f"-لـ مسح اي نوع ↤︎ مسح + اسم النوع\n"
        f"-لـ استثناء شخص  ↤︎ وضع استثناء\n"
        f"-لـ لحذف المستثنى ↤︎ ازاله استثناء (بالرد)\n"        
        f"-لـ استثناء رسالة ↤︎ استثناء تنظيف (بالرد)"
    )

async def _send_clean_message(client, chat_id, text, keyboard=None, reply_to_message_id=None):
    bot_token = client.bot_token if hasattr(client, "bot_token") else settings.TOKEN
    
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
    }
    
    if reply_to_message_id:
        payload["reply_to_message_id"] = reply_to_message_id
    
    if keyboard:
        payload["reply_markup"] = {"inline_keyboard": keyboard}
    
    await telegram_api_post(bot_token, "sendMessage", payload)

async def _edit_clean_message(client, chat_id, message_id, text, keyboard=None):
    bot_token = client.bot_token if hasattr(client, "bot_token") else settings.TOKEN
    
    payload = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text,
        "parse_mode": "HTML",
    }
    
    if keyboard:
        payload["reply_markup"] = {"inline_keyboard": keyboard}
    
    await telegram_api_post(bot_token, "editMessageText", payload)

async def _delete_batch(client, chat_id, msg_ids: list[int]):
    deleted = failed = 0
    for i in range(0, len(msg_ids), 100):
        batch = msg_ids[i:i + 100]
        try:
            await client.delete_messages(chat_id, batch)
            deleted += len(batch)
            await asyncio.sleep(0.3)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                await client.delete_messages(chat_id, batch)
                deleted += len(batch)
            except Exception:
                failed += len(batch)
        except MessageDeleteForbidden:
            failed += len(batch)
        except Exception:
            failed += len(batch)
    return deleted, failed

async def _send_notify(client, chat_id, mode_label: str, counts: dict[str, int], total: int):
    k = await _get_botkey()

    media_count = sum(v for key, v in counts.items() if key != "stickers")
    lines = [f" • {_TYPE_LABELS.get(t, t)} ↤︎ {c}" for t, c in counts.items() if c > 0]
    details = "\n".join(lines) if lines else " • —"

    text = (
        f"{k} تم المسح بالتنظيف {mode_label} بنجاح :\n\n"
        f"<b><u>الرسائل المحذوفة:</u></b>\n"
        f"<blockquote>{details}\n\n"
        f"• مجموع الرسائل ↤︎ {total}\n"
        f"• وسائط  ↤︎ {media_count}</blockquote>\n\n"
        f"-<code> تعطيل التنظيف التلقائي</code>\n"
        f"-<code> اخفاء رسائل التنظيف</code>"
    )

    await client.send_message(
        chat_id,
        text,
        parse_mode=ParseMode.HTML,
    )

def _message_type(message) -> str | None:
    m = message
    if m.animation:  return "gifs"
    if m.video:      return "videos"
    if m.video_note: return "video_note"
    if m.photo:      return "photos"
    if m.sticker:    return "stickers"
    if m.audio:      return "audio"
    if m.voice:      return "voice"
    if m.document:   return "files"
    if m.contact:    return "contacts"
    if m.location:   return "urls"
    if m.forward_from_chat: return "channels"
    if m.entities:
        for ent in m.entities:
            if ent.type == MessageEntityType.CUSTOM_EMOJI:
                return "custom_emoji"
            if ent.type in (MessageEntityType.URL, MessageEntityType.TEXT_LINK):
                return "urls"
            if ent.type in (MessageEntityType.MENTION, MessageEntityType.TEXT_MENTION):
                return "links_users"
    return None

def _is_allowed_type(msg_type: str | None, s: dict, smart: bool) -> bool:
    if not msg_type:
        return False
    if not smart:
        return msg_type in {"photos", "stickers", "gifs"}
    return s.get(msg_type, False)

_pending: dict[int, dict[int, str]] = {}
_first_pending_time: dict[int, float] = {}
_interval_tasks: dict[int, asyncio.Task] = {}

async def _is_excluded(chat_id, message) -> bool:
    r = get_redis()
    Dev_FINAL = get_dev_final()
    if await r.get(f"{Dev_FINAL}:clean_exclude:{chat_id}:{message.id}"):
        return True
    if message.from_user:
        if await r.get(f"{Dev_FINAL}:clean_exclude_user:{chat_id}:{message.from_user.id}"):
            return True
    if message.sender_chat:
        if await r.get(f"{Dev_FINAL}:clean_exclude_user:{chat_id}:{message.sender_chat.id}"):
            return True
    return False

async def _flush_pending(client, chat_id: int, mode_label: str, s: dict):
    bucket = _pending.pop(chat_id, {})
    _first_pending_time.pop(chat_id, None)

    if not bucket:
        return

    task = _interval_tasks.pop(chat_id, None)
    if task and not task.done():
        task.cancel()

    counts: dict[str, int] = defaultdict(int)
    for mid, mtype in bucket.items():
        counts[mtype] += 1

    msg_ids = list(bucket.keys())
    deleted, _ = await _delete_batch(client, chat_id, msg_ids)

    if s["notify"] and deleted:
        await _send_notify(client, chat_id, mode_label, dict(counts), deleted)

async def _interval_trigger(client, chat_id: int, interval: int):
    await asyncio.sleep(interval)
    s = await _get_settings(chat_id)
    if s["disabled"]:
        _pending.pop(chat_id, None)
        _first_pending_time.pop(chat_id, None)
        return
    mode = "الذكي" if s["smart_clean"] else "العادي"
    await _flush_pending(client, chat_id, mode, s)

async def _handle_incoming(client, message, edited=False):
    try:
        r = get_redis(client)
        Dev_FINAL = get_dev_final(client)
        chat_id = message.chat.id

        if not await r.get(f"{chat_id}:enable:{Dev_FINAL}"):
            return
        if message.from_user and await r.get(f"{message.from_user.id}:mute:{chat_id}{Dev_FINAL}"):
            return
        if await r.get(f"{chat_id}:mute:{Dev_FINAL}") and not await admin_pls(message.from_user.id if message.from_user else None, chat_id):
            return
        if message.from_user and await r.get(f"{message.from_user.id}:mute:{Dev_FINAL}"):
            return
        if message.from_user and await r.get(f'{chat_id}:addCustom:{message.from_user.id}{Dev_FINAL}'):
            return
        if message.from_user and await r.get(f'{chat_id}addCustomG:{message.from_user.id}{Dev_FINAL}'):
            return
        if message.from_user and (await r.get(f'{chat_id}:delCustom:{message.from_user.id}{Dev_FINAL}') or await r.get(f'{chat_id}:delCustomG:{message.from_user.id}{Dev_FINAL}')):
            return

        text = message.text or message.caption or ""
        
        name = await r.get(f'{Dev_FINAL}:BotName')
        if isinstance(name, bytes):
            name = name.decode("utf-8")
        if not name:
            name = 'فاينل'
        if text.startswith(f'{name} '):
            text = text.replace(f'{name} ', '')
        
        if await r.get(f'{chat_id}:Custom:{chat_id}{Dev_FINAL}&text={text}'):
            val = await r.get(f'{chat_id}:Custom:{chat_id}{Dev_FINAL}&text={text}')
            if isinstance(val, bytes):
                val = val.decode("utf-8")
            text = val
        if await r.get(f'Custom:{Dev_FINAL}&text={text}'):
            val = await r.get(f'Custom:{Dev_FINAL}&text={text}')
            if isinstance(val, bytes):
                val = val.decode("utf-8")
            text = val

        if message.from_user and message.from_user.is_bot:
            me = await client.get_me()
            if message.from_user.id == me.id:
                return

        s = await _get_settings(chat_id)
        if s["disabled"]:
            return

        if message.sender_chat and not s["channel_clean"]:
            return

        if await _is_excluded(chat_id, message):
            return

        smart = s["smart_clean"]
        mode  = "الذكي" if smart else "العادي"

        if edited:
            if s["edited"] and smart:
                await _delete_batch(client, chat_id, [message.id])
                if s["notify"]:
                    await _send_notify(client, chat_id, mode, {"edited": 1}, 1)
            return

        msg_type = _message_type(message)
        if not _is_allowed_type(msg_type, s, smart):
            return

        _pending.setdefault(chat_id, {})[message.id] = msg_type

        if chat_id not in _first_pending_time:
            _first_pending_time[chat_id] = time.monotonic()
            task = asyncio.create_task(_interval_trigger(client, chat_id, s["interval"]))
            _interval_tasks[chat_id] = task

        if len(_pending[chat_id]) >= s["count"]:
            task = _interval_tasks.pop(chat_id, None)
            if task and not task.done():
                task.cancel()
            await _flush_pending(client, chat_id, mode, s)
    except Exception as e:
        print(f"Error in _handle_incoming: {e}")
        return

async def _manual_flush_type(client, chat_id: int, type_key: str | None, s: dict):
    if type_key is None:
        bucket = dict(_pending.pop(chat_id, {}))
        _first_pending_time.pop(chat_id, None)
        task = _interval_tasks.pop(chat_id, None)
        if task and not task.done():
            task.cancel()
    else:
        bucket_all = _pending.get(chat_id, {})
        bucket = {mid: t for mid, t in bucket_all.items() if t == type_key}
        for mid in bucket:
            _pending[chat_id].pop(mid, None)
        if not _pending[chat_id]:
            _first_pending_time.pop(chat_id, None)
            task = _interval_tasks.pop(chat_id, None)
            if task and not task.done():
                task.cancel()

    if not bucket:
        return 0

    counts: dict[str, int] = defaultdict(int)
    for mid, mtype in bucket.items():
        counts[mtype] += 1

    deleted, _ = await _delete_batch(client, chat_id, list(bucket.keys()))
    if s["notify"] and deleted:
        mode = "الذكي" if s["smart_clean"] else "العادي"
        await _send_notify(client, chat_id, mode, dict(counts), deleted)
    return deleted

_CLEAN_TYPES_PATTERN = "|".join(_TYPE_ALIASES.keys())
_TEXT_CMDS = (
    r"^(\u0627\u0644\u062a\u0646\u0638\u064a\u0641"
    r"|\u062a\u0641\u0639\u064a\u0644 \u0627\u0644\u062a\u0646\u0638\u064a\u0641|\u062a\u0639\u0637\u064a\u0644 \u0627\u0644\u062a\u0646\u0638\u064a\u0641"
    r"|\u062a\u0641\u0639\u064a\u0644 \u0627\u0644\u062a\u0646\u0638\u064a\u0641 \u0627\u0644\u0630\u0643\u064a|\u062a\u0639\u0637\u064a\u0644 \u0627\u0644\u062a\u0646\u0638\u064a\u0641 \u0627\u0644\u0630\u0643\u064a"
    r"|\u062a\u0639\u0637\u064a\u0644 \u0627\u0644\u062a\u0646\u0638\u064a\u0641 \u0627\u0644\u062a\u0644\u0642\u0627\u0626\u064a"
    r"|\u0627\u062e\u0641\u0627\u0621 \u0631\u0633\u0627\u0626\u0644 \u0627\u0644\u062a\u0646\u0638\u064a\u0641|\u0627\u0638\u0647\u0627\u0631 \u0631\u0633\u0627\u0626\u0644 \u0627\u0644\u062a\u0646\u0638\u064a\u0641"
    r"|\u0627\u0645\u0633\u062d"
    r"|\u0645\u0633\u062d (" + _CLEAN_TYPES_PATTERN + r")"
    r"|\u0648\u0636\u0639 \u0627\u0633\u062a\u062b\u0646\u0627\u0621|\u062d\u0630\u0641 \u0627\u0633\u062a\u062b\u0646\u0627\u0621|\u0627\u0632\u0627\u0644\u0647 \u0627\u0633\u062a\u062b\u0646\u0627\u0621|\u0625\u0632\u0627\u0644\u0629 \u0627\u0633\u062a\u062b\u0646\u0627\u0621"
    r"|\u0627\u0633\u062a\u062b\u0646\u0627\u0621 \u062a\u0646\u0638\u064a\u0641"
    r"|\u062a\u0641\u0639\u064a\u0644 \u0627\u0644\u062a\u0638\u064a\u0641|\u062a\u0639\u0637\u064a\u0644 \u0627\u0644\u062a\u0638\u064a\u0641"
    r"|\u062a\u0641\u0639\u064a\u0644 \u0627\u0644\u062a\u0638\u064a\u0641 \u0627\u0644\u0630\u0643\u064a|\u062a\u0639\u0637\u064a\u0644 \u0627\u0644\u062a\u0638\u064a\u0641 \u0627\u0644\u0630\u0643\u064a)$"
)

@Client.on_message(filters.text & filters.group, group=-475)
async def clean_command_handler(c, m):
    r = get_redis(c)
    Dev_FINAL = get_dev_final(c)
    k = '⇜'
    k = await r.get(f"{Dev_FINAL}:botkey")
    if isinstance(k, bytes):
        k = k.decode("utf-8")
    await clean_func(c, m, k)

async def clean_func(c, m, k):
    r = get_redis(c)
    Dev_FINAL = get_dev_final(c)
    k = '⇜'
    
    if not await check_global_restrictions(c, m, k):
        return

    text = m.text
    
    name = await r.get(f'{Dev_FINAL}:BotName')
    if isinstance(name, bytes):
        name = name.decode("utf-8")
    if not name:
        name = 'فاينل'
    if text.startswith(f'{name} '):
        text = text.replace(f'{name} ', '')
    
    if await r.get(f'{m.chat.id}:Custom:{m.chat.id}{Dev_FINAL}&text={text}'):
        val = await r.get(f'{m.chat.id}:Custom:{m.chat.id}{Dev_FINAL}&text={text}')
        if isinstance(val, bytes):
            val = val.decode("utf-8")
        text = val
    if await r.get(f'Custom:{Dev_FINAL}&text={text}'):
        val = await r.get(f'Custom:{Dev_FINAL}&text={text}')
        if isinstance(val, bytes):
            val = val.decode("utf-8")
        text = val

    k = await _get_botkey()
    chat_id = m.chat.id
    user_id = m.from_user.id if m.from_user else None

    if text == "التنظيف":
        if not await mod_pls(user_id, chat_id):
            return await m.reply(plugins_cleanup_593(k))
        s = await _get_settings(chat_id)
        keyboard = await _build_keyboard(s, user_id)
        await _send_clean_message(c, chat_id, _build_main_text(s, k), keyboard, m.id)
        return

    if text in ("تفعيل التنظيف", "تعطيل التنظيف", "تفعيل التظيف", "تعطيل التظيف"):
        if not await mod_pls(user_id, chat_id):
            return await m.reply(plugins_cleanup_601(k))
        disable = text.startswith("تعطيل")
        current = await r.get(_k(chat_id, "disabled"))
        if current is not None and isinstance(current, bytes):
            current = current.decode()
        cur_disabled = str(current) != "0" if current is not None else True
        if cur_disabled == disable:
            return await m.reply(
                plugins_cleanup_608(k, 'معطل' if disable else 'مفعل')
            )
        await _set_val(chat_id, "disabled", 1 if disable else 0)
        action = "عطّلت" if disable else "فعّلت"
        return await m.reply(
            plugins_cleanup_613(k, m.from_user.mention(), k, action)
        )

    if text in ("تفعيل التنظيف الذكي", "تعطيل التنظيف الذكي"):
        if not await mod_pls(user_id, chat_id):
            return await m.reply(plugins_cleanup_619(k))
        enable = text.startswith("تفعيل")
        await _set_val(chat_id, "smart_clean", 1 if enable else 0)
        if enable:
            await _set_val(chat_id, "disabled", 0)
        action = "فعّلت" if enable else "عطّلت"
        return await m.reply(
            plugins_cleanup_625(k, m.from_user.mention(), k, action)
        )

    if text == "تعطيل التنظيف التلقائي":
        if not await mod_pls(user_id, chat_id):
            return await m.reply(plugins_cleanup_631(k))
        await _set_val(chat_id, "auto_clean", 0)
        await _set_val(chat_id, "smart_clean", 0)
        return await m.reply(plugins_cleanup_634(k))

    if text in ("اخفاء رسائل التنظيف", "إخفاء رسائل التنظيف"):
        if not await mod_pls(user_id, chat_id):
            return await m.reply(plugins_cleanup_638(k))
        await _set_val(chat_id, "notify", 0)
        return await m.reply(plugins_cleanup_640(k))

    if text == "اظهار رسائل التنظيف":
        if not await mod_pls(user_id, chat_id):
            return await m.reply(plugins_cleanup_644(k))
        await _set_val(chat_id, "notify", 1)
        return await m.reply(plugins_cleanup_646(k))

    if text == "امسح":
        if not await mod_pls(user_id, chat_id):
            return await m.reply(plugins_cleanup_650(k))
        s = await _get_settings(chat_id)
        if s["disabled"]:
            return await m.reply(plugins_cleanup_653(k))
        deleted = await _manual_flush_type(c, chat_id, None, s)
        if not deleted:
            return await m.reply(plugins_cleanup_656(k))
        return

    if text.startswith("مسح "):
        type_name = text[4:].strip()
        type_key = _TYPE_ALIASES.get(type_name)
        if not type_key:
            return
        s = await _get_settings(chat_id)
        if s["disabled"]:
            return await m.reply(plugins_cleanup_666(k))
        
        if not await mod_pls(user_id, chat_id):
            return await m.reply(plugins_cleanup_669(k))
        
        if s["smart_clean"] and not s.get(type_key, False):
            return await m.reply(
                plugins_cleanup_672(k, type_name)
            )
        
        deleted = await _manual_flush_type(c, chat_id, type_key, s)
        if not deleted:
            return await m.reply(plugins_cleanup_678(k, type_name))
        
        return

    if text in ("وضع استثناء", "استثناء تنظيف"):
        if not await mod_pls(user_id, chat_id):
            return await m.reply(plugins_cleanup_684(k))
        replied = m.reply_to_message
        if not replied:
            return await m.reply(plugins_cleanup_687(k))
        
        if text == "وضع استثناء":
            target_id = (replied.from_user.id if replied.from_user
                         else replied.sender_chat.id if replied.sender_chat else None)
            if not target_id:
                return await m.reply(plugins_cleanup_693(k))
            rkey = f"{Dev_FINAL}:clean_exclude_user:{chat_id}:{target_id}"
            await r.set(rkey, 1)
            return await m.reply(plugins_cleanup_696(k))
        else:
            rkey = f"{Dev_FINAL}:clean_exclude:{chat_id}:{replied.id}"
            await r.set(rkey, 1)
            _pending.get(chat_id, {}).pop(replied.id, None)
            return await m.reply(plugins_cleanup_701(k))

    if text in ("حذف استثناء", "ازاله استثناء", "إزالة استثناء"):
        if not await mod_pls(user_id, chat_id):
            return await m.reply(plugins_cleanup_705(k))
        replied = m.reply_to_message
        if not replied:
            return await m.reply(plugins_cleanup_708(k))
        
        target_id = (replied.from_user.id if replied.from_user
                     else replied.sender_chat.id if replied.sender_chat else None)
        
        rkey_user = f"{Dev_FINAL}:clean_exclude_user:{chat_id}:{target_id}" if target_id else None
        rkey_msg = f"{Dev_FINAL}:clean_exclude:{chat_id}:{replied.id}"
        
        removed = False
        if rkey_user and await r.get(rkey_user):
            await r.delete(rkey_user)
            removed = True
        if await r.get(rkey_msg):
            await r.delete(rkey_msg)
            removed = True
            
        if removed:
            return await m.reply(plugins_cleanup_725(k))
        else:
            return await m.reply(plugins_cleanup_727(k))

@Client.on_callback_query(filters.regex(r"^clean_(toggle|set|close):"), group=1)
async def CleanCallbackQueryHandler(c, m):
    r = get_redis(c)
    Dev_FINAL = get_dev_final(c)
    
    k = await r.get(f"{Dev_FINAL}:botkey")
    
    if m.data.startswith("clean_toggle:"):
        await clean_toggle_cb(c, m)
        return

    if m.data.startswith("clean_set:"):
        await clean_set_cb(c, m)
        return

    if m.data.startswith("clean_close:"):
        await clean_close_cb(c, m)
        return

async def clean_toggle_cb(client, cb: CallbackQuery):
    r = get_redis(client)
    Dev_FINAL = get_dev_final(client)
    k = '⇜'
    try:
        parts = cb.data.split(":")
        field = parts[1]
        user_id = int(parts[2])
        chat_id = cb.message.chat.id
        
        if cb.from_user.id != user_id:
            return await cb.answer(REPLIES['plugins_cleanup_759'], show_alert=True)
        
        if not await check_global_restrictions(client, cb.message, k):
            return
        
        if not await mod_pls(user_id, chat_id):
            return await cb.answer(REPLIES['plugins_cleanup_765'], show_alert=True)
        
        if field == "disabled":
            val = await r.get(_k(chat_id, "disabled"))
            if val is not None and isinstance(val, bytes):
                val = val.decode()
            cur_disabled = str(val) != "0" if val is not None else True
            await r.set(_k(chat_id, "disabled"), 0 if cur_disabled else 1)
        else:
            await _toggle(chat_id, field)

        s = await _get_settings(chat_id)
        k = await _get_botkey()
        keyboard = await _build_keyboard(s, user_id)
        await _edit_clean_message(client, chat_id, cb.message.id, _build_main_text(s, k), keyboard)
        await cb.answer()
    except Exception as e:
        print(f"Error in clean_toggle_cb: {e}")
        return

async def clean_set_cb(client, cb: CallbackQuery):
    r = get_redis(client)
    Dev_FINAL = get_dev_final(client)
    k = '⇜'
    try:
        parts = cb.data.split(":")
        field = parts[1]
        user_id = int(parts[2])
        chat_id = cb.message.chat.id
        
        if cb.from_user.id != user_id:
            return await cb.answer(REPLIES['plugins_cleanup_759'], show_alert=True)
        
        if not await check_global_restrictions(client, cb.message, k):
            return
        
        if not await mod_pls(user_id, chat_id):
            return await cb.answer(REPLIES['plugins_cleanup_765'], show_alert=True)
        
        s = await _get_settings(chat_id)
        if field == "count":
            opts = [5, 10, 20, 50, 100]
            cur = s["count"]
            nxt = next((o for o in opts if o > cur), opts[0])
            await _set_val(chat_id, "count", nxt)
        else:
            opts = [30, 60, 120, 300, 600]
            cur = s["interval"]
            nxt = next((o for o in opts if o > cur), opts[0])
            await _set_val(chat_id, "interval", nxt)
        s = await _get_settings(chat_id)
        k = await _get_botkey()
        keyboard = await _build_keyboard(s, user_id)
        await _edit_clean_message(client, chat_id, cb.message.id, _build_main_text(s, k), keyboard)
        await cb.answer()
    except Exception as e:
        print(f"Error in clean_set_cb: {e}")
        return

async def clean_close_cb(client, cb: CallbackQuery):
    r = get_redis(client)
    Dev_FINAL = get_dev_final(client)
    k = '⇜'
    try:
        parts = cb.data.split(":")
        user_id = int(parts[1])
        chat_id = cb.message.chat.id
        
        if cb.from_user.id != user_id:
            return await cb.answer(REPLIES['plugins_cleanup_759'], show_alert=True)
        
        if not await check_global_restrictions(client, cb.message, k):
            return
        
        if not await mod_pls(user_id, chat_id):
            return await cb.answer(REPLIES['plugins_cleanup_765'], show_alert=True)
        
        try:
            await cb.message.delete()
        except Exception:
            pass
        await cb.answer()
    except Exception as e:
        print(f"Error in clean_close_cb: {e}")
        return

@Client.on_message(filters.group & ~filters.regex(_TEXT_CMDS), group=-1552)
async def _incoming_handler_auto(client, message):
    r = get_redis(client)
    Dev_FINAL = get_dev_final(client)
    
    await _handle_incoming(client, message, edited=False)

@Client.on_edited_message(filters.group, group=-1553)
async def _edited_handler_auto(client, message):
    r = get_redis(client)
    Dev_FINAL = get_dev_final(client)
    
    await _handle_incoming(client, message, edited=True)