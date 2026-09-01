# Plugins1/FinalMusic/fm_plugins/playback-controls/seek.py

from helpers.context import is_sudoer, get_current_bot_id, set_current_bot_id, get_global_k, redis_proxy as r, dev_final_proxy as Dev_FINAL, k_proxy as k
from compat import Client, filters
from compat import Message
from plugins.FinalMusic import tune, queue
from helpers.ranks import *
from plugins.FinalMusic.fm_core.lang import lang

_current_bot_id = get_current_bot_id

@Client.on_message(filters.group & ~filters.bot, group=513)
async def seek_handler(client, m: Message):
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
        if not text.startswith("تقديم ") and not text.startswith("تأخير "):
            return
        if not await can_manage_vc_check(m.from_user.id, m.chat.id):
            return await m.reply(f"• عذراً لا تملك الصلاحية")
        try:
            await m.delete()
        except:
            pass
        parts = text.split()
        if len(parts) < 2:
            return await m.reply(_lang.get("play_seek_usage", "الاستخدام: تقديم [عدد الثواني] أو تأخير [عدد الثواني]"))
        try:
            to_seek = int(parts[1])
        except ValueError:
            return await m.reply(_lang.get("play_seek_usage", "يرجى إدخال عدد صحيح من الثواني"))
        if to_seek < 10:
            return await m.reply(_lang.get("play_seek_min", "الحد الأدنى 10 ثواني"))
        if not await r.get(f"call_active:{m.chat.id}:{Dev_FINAL}"):
            return await m.reply(_lang.get("not_playing", "لا يوجد تشغيل حالياً"))
        playing_status = await r.get(f"playing:{m.chat.id}:{Dev_FINAL}")
        if not playing_status or playing_status == "paused":
            return await m.reply(_lang.get("play_already_paused", "التشغيل متوقف حالياً"))
        media = queue.get_current(m.chat.id)
        if not media.duration_sec:
            return await m.reply(_lang.get("play_seek_no_dur", "لا يمكن التقديم في هذا المقطع"))
        sent = await m.reply(_lang.get("play_seeking", "جاري التقديم..."))
        current_time = getattr(media, 'time', 0)
        if parts[0] == "تأخير":
            start_from = max(1, current_time - to_seek)
            stype = _lang.get("backward", "تأخير")
        else:
            start_from = min(current_time + to_seek, media.duration_sec - 5)
            stype = _lang.get("forward", "تقديم")
        success = await tune.seek_stream(m.chat.id, int(start_from))
        if success:
            await sent.edit(_lang.get("play_seeked", "تم {} إلى {} ثانية بواسطة {}").format(stype, start_from, m.from_user.mention))
        else:
            await sent.edit(f"• فشل في {stype}")
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