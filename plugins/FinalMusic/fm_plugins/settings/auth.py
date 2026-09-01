# auth.py
from helpers.context import get_current_bot_id, get_global_k, redis_proxy as r, dev_final_proxy as Dev_FINAL, k_proxy as k
import time
from compat import Client, filters, types
from plugins.FinalMusic import app, lang
from helpers.ranks import *

@Client.on_message(filters.group & ~filters.bot, group=620)
async def auth_handler(c, m: types.Message):
    if not m.text:
        return
    if not m.from_user:
        return
    if hasattr(m.from_user, 'is_bot') and m.from_user.is_bot:
        return
    if not await check_global_restrictions(c, m, get_global_k()):
        return
    if await r.get(f'{m.from_user.id}:mute:{m.chat.id}{Dev_FINAL}'):
        return
    if await r.get(f'{m.from_user.id}:mute:{Dev_FINAL}'):
        return
    if await r.get(f'{m.chat.id}:mute:{Dev_FINAL}') and not await admin_pls(m.from_user.id, m.chat.id):
        return
    if await r.get(f'{m.from_user.id}:gban:{Dev_FINAL}'):
        try:
            await m.chat.ban_member(m.from_user.id)
        except:
            pass
        return
    k = await r.get(f'{get_current_bot_id() or Dev_FINAL}:botkey')
    name = await r.get(f'{Dev_FINAL}:BotName')
    text = m.text
    if name and text.startswith(f'{name} '):
        text = text.replace(f'{name} ', '')
    if text not in ["رفع مشغل", "تنزيل مشغل", "المشغلين", "restadmin"]:
        return
    try:
        await m.delete()
    except:
        pass
    if text == "رفع مشغل":
        if not await admin_pls(m.from_user.id, m.chat.id):
            return await m.reply(f"{k} عذراً الامر لـ 「 الادمن 」 فقط")
        if not m.reply_to_message:
            return await m.reply(f"{k} قم بالرد على العضو")
        user = m.reply_to_message.from_user
        if not user:
            return await m.reply(f"{k} العضو غير موجود")
        if user.is_bot:
            return await m.reply(f"{k} لا يمكن رفع بوت")
        if await admin_pls(user.id, m.chat.id):
            return await m.reply(f"{k} هذا العضو لديه رتبة اعلى من المشغل")
        await r.sadd(f"auth_users:{m.chat.id}:{Dev_FINAL}", str(user.id))
        return await m.reply(f"{k} تم رفع {user.mention} كمشغل")
    if text == "تنزيل مشغل":
        if not await admin_pls(m.from_user.id, m.chat.id):
            return await m.reply(f"{k} عذراً الامر لـ 「 الادمن 」 فقط")
        if not m.reply_to_message:
            return await m.reply(f"{k} قم بالرد على العضو")
        user = m.reply_to_message.from_user
        if not user:
            return await m.reply(f"{k} العضو غير موجود")
        if await admin_pls(user.id, m.chat.id):
            return await m.reply(f"{k} هذا العضو لديه رتبة اعلى من المشغل")
        await r.srem(f"auth_users:{m.chat.id}:{Dev_FINAL}", str(user.id))
        return await m.reply(f"{k} تم تنزيل {user.mention} من المشغلين")
    if text == "المشغلين":
        if not await admin_pls(m.from_user.id, m.chat.id):
            return await m.reply(f"{k} عذراً الامر لـ 「 الادمن 」 فقط")
        auth_users = await r.smembers(f"auth_users:{m.chat.id}:{Dev_FINAL}")
        if not auth_users:
            return await m.reply(f"{k} لا يوجد مشغلين")
        auth_txt = f"📋 قائمة المشغلين في {m.chat.title}\n"
        for idx, user_id in enumerate(sorted(auth_users), start=1):
            try:
                user = await app.get_users(int(user_id))
                auth_txt += f"\n{idx}. {user.mention}"
            except:
                auth_txt += f"\n{idx}. <a href=\"tg://user?id={user_id}\">{user_id}</a>"
        await m.reply(auth_txt)
    if text == "restadmin":
        if not await admin_pls(m.from_user.id, m.chat.id):
            return await m.reply(f"{k} عذراً الامر لـ 「 الادمن 」 فقط")
        await r.delete(f"chat_admins:{m.chat.id}:{Dev_FINAL}")
        await m.reply(f"{k} تم تحديث قائمة المشرفين")