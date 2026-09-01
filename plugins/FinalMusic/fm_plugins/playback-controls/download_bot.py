import os
import re
import json
import asyncio
import urllib.request
import urllib.parse
from compat import Client, filters
from compat import InputMediaAudio, Message

from helpers.context import redis_proxy as r, dev_final_proxy as Dev_FINAL, k_proxy as k
from helpers.ranks import *
from plugins.FinalMusic.fm_core.lang import lang
from plugins.FinalMusic import app, yt, config
from plugins.FinalMusic.fm_core.l1_cache import (
    clean_title,
    get_real_bot_id,
)

COOKIE_PATH = "plugins/FinalMusic/cookies/cookies.txt"
ARCHIVE_CHANNEL_ID = -1001828975467
CHANNEL_USERNAME = "@xxzhp0"

async def is_youtube_enabled(chat_id: int) -> bool:
    res = True
    if await r.get(f'{chat_id}:disableYT:{Dev_FINAL}') or await r.get(f':disableYT:{Dev_FINAL}'):
        res = False
    return res

def extract_yt_id(query: str) -> str:
    yt_regex = r'(?:v=|\/|be\/|shorts\/)([\w-]{11})'
    match = re.search(yt_regex, query)
    if match:
        return match.group(1)
    try:
        encoded_query = urllib.parse.quote(query)
        url = f'https://www.youtube.com/results?search_query={encoded_query}'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req, timeout=5).read().decode()
        found = re.search(r'/watch\?v=([\w-]{11})', html)
        if found:
            return found.group(1)
    except Exception:
        pass
    return None

async def get_cached_video_id_by_query(query: str) -> str | None:
    normalized_query = query.strip().lower()
    return await r.get(f"query_map:{normalized_query}")

async def set_cached_video_id_by_query(query: str, video_id: str):
    normalized_query = query.strip().lower()
    await r.setex(f"query_map:{normalized_query}", 86400 * 30, video_id)

def download_yt_audio_fast(video_id: str) -> dict:
    import yt_dlp
    os.makedirs("downloads", exist_ok=True)
    out_template = f"downloads/%(title)s.%(ext)s"
    opts = {
        'cookiefile': COOKIE_PATH,
        'outtmpl': out_template,
        'noplaylist': True,
        'format': 'ba/bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
            'preferredquality': '0'
        }],
        'concurrent_fragment_downloads': 16,
        'cachedir': False,
        'nocheckcertificate': True,
        'quiet': True,
        'no_warnings': True,
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'ios', 'mweb']
            }
        }
    }
    url = f"https://www.youtube.com/watch?v={video_id}"
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
            if file_path and not file_path.endswith('.m4a'):
                base_name = os.path.splitext(file_path)[0]
                file_path = base_name + '.m4a'
            if not os.path.exists(file_path):
                base_name, _ = os.path.splitext(file_path)
                for ext in ['.m4a', '.webm', '.mp3']:
                    if os.path.exists(base_name + ext):
                        file_path = base_name + ext
                        break
            return {
                'file_path': file_path,
                'title': info.get('title', 'Audio Track'),
                'duration': int(info.get('duration', 0))
            }
    except Exception:
        raise

@Client.on_message(filters.group & ~filters.bot, group=500)
async def youtube_toggle_handler(c, m: Message):
    if not m.text or not m.from_user or m.from_user.is_bot:
        return
    if "يوت" not in m.text:
        return
    if not await check_global_restrictions(c, m, k):
        return

    name = await r.get(f'{Dev_FINAL}:BotName')
    text = m.text
    if name and text.startswith(f'{name} '):
        text = text.replace(f'{name} ', '')

    commands = {
        "تفعيل اليوتيوب": (f'{m.chat.id}:disableYT:{Dev_FINAL}', None, "• تم تفعيل أمر التحميل للجميع"),
        "تعطيل اليوتيوب": (f'{m.chat.id}:disableYT:{Dev_FINAL}', 'True', "• تم تعطيل أمر التحميل عن المجموعة"),
        "تفعيل يوت المميزين": (f'{m.chat.id}:yt_restriction:{Dev_FINAL}', 'vip', "• تم تقييد الأمر للمميزين فما فوق"),
        "تعطيل يوت المميزين": (f'{m.chat.id}:yt_restriction:{Dev_FINAL}', None, "• تم إلغاء تقييد المميزين"),
        "تفعيل يوت الادمن": (f'{m.chat.id}:yt_restriction:{Dev_FINAL}', 'admin', "• تم تقييد الأمر للادمن والمشرفين فقط"),
        "تعطيل يوت الادمن": (f'{m.chat.id}:yt_restriction:{Dev_FINAL}', None, "• تم إلغاء تقييد الادمن")
    }

    if text in commands:
        if not await admin_pls(m.from_user.id, m.chat.id):
            return await m.reply("• عذراً الامر لـ 「 الادمن 」 فقط")
        key, val, response = commands[text]
        if val is None:
            await r.delete(key)
        else:
            await r.set(key, val)
        return await m.reply(response)

@Client.on_message(filters.group & ~filters.bot, group=501)
async def youtube_download_handler(c, m: Message):
    if not m.text or not m.from_user or m.from_user.is_bot:
        return
    if "يوت" not in m.text:
        return

    check_rest = await check_global_restrictions(c, m, k)
    if not check_rest:
        return

    _lang = await lang.get_lang(m.chat.id)
    name = await r.get(f'{Dev_FINAL}:BotName')
    text = m.text
    if name and text.startswith(f'{name} '):
        text = text.replace(f'{name} ', '')

    if text.startswith("يوت "):
        restriction = await r.get(f'{m.chat.id}:yt_restriction:{Dev_FINAL}') or ""
        if restriction == "admin":
            if not await admin_pls(m.from_user.id, m.chat.id):
                return await m.reply("• عذراً أمر التحميل مقيد للأدمن والمشرفين فقط")
        elif restriction == "vip":
            if not await pre_pls(m.from_user.id, m.chat.id):
                return await m.reply("• عذراً هذا الأمر متاح للمميزين والمشرفين فقط")
        else:
            if not await is_youtube_enabled(m.chat.id):
                return await m.reply("• أمر التحميل معطل في هذه المجموعة")

        query = text.split(" ", 1)[1].strip() if len(text.split()) > 1 else ""
        if not query:
            return await m.reply("• الاستخدام:\n يوت [اسم المقطع أو رابط اليوتيوب]")

        try:
            video_id = await get_cached_video_id_by_query(query)
            if not video_id:
                video_id = await asyncio.to_thread(extract_yt_id, query)
                if video_id:
                    await set_cached_video_id_by_query(query, video_id)

            if not video_id:
                return await m.reply(_lang.get("yt_download_usage", "فشل في معالجة الطلب"))

            cached_data = await yt.get_cached_track(video_id)

            if cached_data and cached_data.get("msg_id"):
                msg_id = cached_data["msg_id"]
                target_chat = CHANNEL_USERNAME if CHANNEL_USERNAME.startswith("@") else ARCHIVE_CHANNEL_ID
                try:
                    await c.copy_message(
                        chat_id=m.chat.id,
                        from_chat_id=target_chat,
                        message_id=int(msg_id),
                        reply_to_message_id=m.id,
                    )
                    return
                except Exception:
                    await yt.mark_track_as_broken(video_id)

            msg = await m.reply("🎶")

            data = await asyncio.to_thread(download_yt_audio_fast, video_id)
            file_path = data['file_path']
            title = data['title']
            duration_sec = data['duration']

            if duration_sec > 3600:
                if os.path.exists(file_path):
                    os.remove(file_path)
                return await msg.edit("• اعذرني حجم الملف اكبر من ساعة مااقدر احمله")

            if not file_path or not os.path.exists(file_path):
                return await msg.edit("• فشل التحميل الملف غير موجود")

            await msg.edit_media(media=InputMediaAudio(
                media=file_path,
                title=clean_title(title),
                duration=duration_sec if duration_sec > 0 else None
            ))

            exists_in_cache = await yt.track_exists_in_cache(video_id)
            if not exists_in_cache:
                try:
                    sent_msg = await c.send_audio(
                        chat_id=CHANNEL_USERNAME,
                        audio=file_path,
                        title=clean_title(title),
                        duration=duration_sec if duration_sec > 0 else None,
                        performer="YouTube"
                    )
                    sent_id = getattr(sent_msg, 'id', getattr(sent_msg, 'message_id', None))
                    if sent_msg and sent_id:
                        await yt.save_track_to_cache(video_id, sent_id)
                except Exception:
                    pass

            if file_path and os.path.exists(file_path):
                os.remove(file_path)

        except Exception:
            try:
                if 'msg' in locals():
                    await msg.edit("• فشل في معالجة طلبك حالياً")
                else:
                    await m.reply("• فشل في معالجة طلبك حالياً")
            except Exception:
                pass
