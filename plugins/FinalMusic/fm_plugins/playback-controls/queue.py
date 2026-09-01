# Plugins1/FinalMusic/fm_plugins/playback-controls/queue.py

from helpers.context import get_current_bot_id, set_current_bot_id, get_global_k, redis_proxy as r, dev_final_proxy as Dev_FINAL, k_proxy as k
from compat import Client, filters
from compat import Message, InputMediaPhoto
from plugins.FinalMusic import config, queue
from plugins.FinalMusic.fm_helpers import Track, buttons, thumb
from plugins.FinalMusic.fm_core.lang import lang
from helpers.ranks import *
FALLBACK_THUMB = "https://files.catbox.moe/8czm1s.png"
_current_bot_id = get_current_bot_id

@Client.on_message(filters.group & ~filters.bot, group=530)
async def queue_handler(client, m: Message):
    old_bot_id = _current_bot_id()
    try:
        bot_id = getattr(client, 'bot_id', None) or getattr(client, 'dev_final', None)
        if bot_id:
            set_current_bot_id(bot_id)
        
        if not m.text:
            return
        if not m.from_user:
            return
        if m.from_user.is_bot:
            return
        if not await check_global_restrictions(client, m, get_global_k()):
            return
        if await r.get(f'{m.from_user.id}:mute:{m.chat.id}{Dev_FINAL}'):
            return
        if await r.get(f'{m.from_user.id}:mute:{Dev_FINAL}'):
            return
        if await r.get(f'{m.chat.id}:mute:{Dev_FINAL}') and not await admin_pls(m.from_user.id, m.chat.id):
            return
        _lang = await lang.get_lang(m.chat.id)
        k = await r.get(f'{get_current_bot_id() or Dev_FINAL}:botkey')
        name = await r.get(f'{Dev_FINAL}:BotName')
        text = m.text
        if name and text.startswith(f'{name} '):
            text = text.replace(f'{name} ', '')
        if text != "قائمة الانتظار":
            return
        try:
            await m.delete()
        except:
            pass
        if not await r.get(f"call_active:{m.chat.id}:{Dev_FINAL}"):
            return await m.reply(_lang.get("not_playing", "لا يوجد تشغيل حالياً"))
        _reply = await m.reply(_lang.get("queue_fetching", "جاري جلب القائمة..."))
        _queue = queue.get_queue(m.chat.id)
        if not _queue:
            return await _reply.edit(_lang.get("queue_empty", "قائمة الانتظار فارغة"))
        _media = _queue[0]
        _thumb = await thumb.generate(_media) if isinstance(_media, Track) else getattr(config, 'DEFAULT_THUMB', None)
        if not _thumb:
            _thumb = FALLBACK_THUMB
        _text = _lang.get("queue_curr", "🎵 **{}**\n⏱️ {}\n👤 {}").format(_media.url, _media.title[:50], _media.duration, _media.user)
        _queue.pop(0)
        if _queue:
            _text += "<blockquote expandable>"
            for i, media in enumerate(_queue, start=1):
                if i == 15:
                    break
                _text += _lang.get("queue_item", "<b>{}</b>. {} ({})").format(i, media.title, media.duration)
            _text += "</blockquote>"
        _playing = await r.get(f"playing:{m.chat.id}:{Dev_FINAL}")
        await _reply.edit_media(media=InputMediaPhoto(media=_thumb, caption=_text))
        await buttons.edit_queue_markup(
            client,
            m.chat.id,
            _reply.id,
            _lang.get("playing", "تشغيل") if _playing and _playing != "paused" else _lang.get("paused", "متوقف"),
            _playing and _playing != "paused"
        )
    finally:
        if old_bot_id:
            set_current_bot_id(old_bot_id)