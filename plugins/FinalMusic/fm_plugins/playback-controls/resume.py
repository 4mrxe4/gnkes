# Plugins1/FinalMusic/fm_plugins/playback-controls/resume.py

from helpers.context import is_sudoer, get_current_bot_id, set_current_bot_id, get_global_k, redis_proxy as r, dev_final_proxy as Dev_FINAL, k_proxy as k
import logging
from compat import Client, filters
from compat import Message
from compat import ChatSendPlainForbidden, ChatWriteForbidden
from plugins.FinalMusic import tune
from plugins.FinalMusic.fm_helpers import buttons
from helpers.ranks import *
from plugins.FinalMusic.fm_core.lang import lang

logger = logging.getLogger(__name__)
_current_bot_id = get_current_bot_id

@Client.on_message(filters.group & ~filters.bot, group=512)
async def resume_handler(client, m: Message):
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
        if text not in ["كمل", "استئناف"]:
            return
        if not await can_manage_vc_check(m.from_user.id, m.chat.id):
            return await m.reply(f"• عذراً لا تملك الصلاحية")
        try:
            await m.delete()
        except:
            pass
        if not await r.get(f"call_active:{m.chat.id}:{Dev_FINAL}"):
            try:
                return await m.reply(_lang.get("not_playing", "لا يوجد تشغيل حالياً"))
            except:
                return
        playing_status = await r.get(f"playing:{m.chat.id}:{Dev_FINAL}")
        if playing_status and playing_status != "paused":
            try:
                return await m.reply(_lang.get("play_not_paused", "التشغيل ليس متوقفاً"))
            except:
                return
        await tune.resume(m.chat.id)
        try:
            sent = await m.reply(text=_lang.get("play_resumed", "تم الاستئناف").format(m.from_user.mention))
            await buttons.edit_controls_markup(client, m.chat.id, sent.id)
        except:
            logger.warning("Cannot send text in media-only chat")
    finally:
        if old_bot_id:
            set_current_bot_id(old_bot_id)

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