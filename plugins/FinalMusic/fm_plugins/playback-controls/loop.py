# Plugins1/FinalMusic/fm_plugins/playback-controls/loop.py

from helpers.context import is_sudoer, get_current_bot_id, set_current_bot_id, get_global_k, redis_proxy as r, dev_final_proxy as Dev_FINAL, k_proxy as k
from compat import Client, filters
from compat import Message
from helpers.ranks import *
from plugins.FinalMusic.fm_core.lang import lang

_current_bot_id = get_current_bot_id

@Client.on_message(filters.group & ~filters.bot, group=510)
async def loop_handler(client, m: Message):
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
        if text.startswith("تكرار "):
            if not await can_manage_vc_check(m.from_user.id, m.chat.id):
                return await m.reply(f"• عذراً لا تملك الصلاحية")
            try:
                await m.delete()
            except:
                pass
            current_loop = await r.get(f"loop:{m.chat.id}:{Dev_FINAL}")
            parts = text.split()
            if len(parts) > 1:
                mode_arg = parts[1].lower()
                if mode_arg in ["0", "disable", "تعطيل", "ايقاف"]:
                    new_loop = 0
                    text_msg = f"• تم إيقاف وضع التكرار"
                elif mode_arg in ["single", "1", "one", "مفرد", "اغنية"]:
                    new_loop = 1
                    text_msg = f"• تم تفعيل تكرار الأغنية الحالية"
                elif mode_arg in ["queue", "all", "10", "قائمة", "الكل"]:
                    new_loop = 10
                    text_msg = f"• تم تفعيل تكرار قائمة التشغيل بالكامل"
                else:
                    return await m.reply(f"• الاستخدام:\nتكرار - التبديل بين الأوضاع\nتكرار disable - تعطيل\nتكرار single - تكرار أغنية\nتكرار queue - تكرار القائمة")
            else:
                if current_loop == "0" or not current_loop:
                    new_loop = 1
                    text_msg = f"• تم تفعيل تكرار الأغنية الحالية"
                elif current_loop == "1":
                    new_loop = 10
                    text_msg = f"• تم تفعيل تكرار قائمة التشغيل بالكامل"
                else:
                    new_loop = 0
                    text_msg = f"• تم إيقاف وضع التكرار"
            if new_loop == 0:
                await r.delete(f"loop:{m.chat.id}:{Dev_FINAL}")
            else:
                await r.set(f"loop:{m.chat.id}:{Dev_FINAL}", str(new_loop))
            await m.reply(text_msg)

        if text == "تكرار":
            if not await can_manage_vc_check(m.from_user.id, m.chat.id):
                return await m.reply(f"• عذراً لا تملك الصلاحية")
            try:
                await m.delete()
            except:
                pass
            current_loop = await r.get(f"loop:{m.chat.id}:{Dev_FINAL}")
            if current_loop == "0" or not current_loop:
                new_loop = 1
                text_msg = f"• تم تفعيل تكرار الأغنية الحالية"
            elif current_loop == "1":
                new_loop = 10
                text_msg = f"• تم تفعيل تكرار قائمة التشغيل بالكامل"
            else:
                new_loop = 0
                text_msg = f"• تم إيقاف وضع التكرار"
            if new_loop == 0:
                await r.delete(f"loop:{m.chat.id}:{Dev_FINAL}")
            else:
                await r.set(f"loop:{m.chat.id}:{Dev_FINAL}", str(new_loop))
            await m.reply(text_msg)
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