# maintenance.py
from helpers.context import get_current_bot_id, get_global_k, redis_proxy as r, dev_final_proxy as Dev_FINAL, k_proxy as k
from compat import Client, filters
from compat import Message
from plugins.FinalMusic import app, lang
from helpers.ranks import *
@Client.on_message(filters.group & ~filters.bot, group=600)
async def maintenance_handler(c, m: Message):
    if not m.text:
        return
    if not m.from_user:
        return
    if m.from_user.is_bot:
        return
    if not await check_global_restrictions(c, m, get_global_k()):
        return
    if await r.get(f'{m.from_user.id}:mute:{m.chat.id}{Dev_FINAL}'):
        return
    if await r.get(f'{m.from_user.id}:mute:{Dev_FINAL}'):
        return
    if await r.get(f'{m.chat.id}:mute:{Dev_FINAL}') and not await admin_pls(m.from_user.id, m.chat.id):
        return
    k = await r.get(f'{get_current_bot_id() or Dev_FINAL}:botkey')
    name = await r.get(f'{Dev_FINAL}:BotName')
    text = m.text
    if name and text.startswith(f'{name} '):
        text = text.replace(f'{name} ', '')
    if not text.startswith("صيانة"):
        return
    if m.from_user.id not in app.sudoers:
        return
    try:
        await m.delete()
    except:
        pass
    parts = text.split()
    if len(parts) < 2:
        status = await r.get(f"maintenance:{Dev_FINAL}")
        status_text = "🔴 مفعل" if status else "🟢 معطل"
        await m.reply(f"<blockquote><u><b>🔧 حالة وضع الصيانة</b></u>\n\n<b>الحالة الحالية:</b> {status_text}\n\n<b>الاستخدام:</b>\n<code>صيانة تفعيل</code> - تفعيل الوضع\n<code>صيانة تعطيل</code> - تعطيل الوضع</blockquote>")
        return
    mode = parts[1]
    if mode in ["تفعيل", "enable", "on"]:
        await r.set(f"maintenance:{Dev_FINAL}", "1")
        await m.reply("<blockquote><u><b>🔴 تم تفعيل وضع الصيانة</b></u>\n\nيمكن لمستخدمي المطور (sudo) فقط استخدام البوت الآن.\nسيظهر للمستخدمين العاديين رسالة صيانة.</blockquote>")
    elif mode in ["تعطيل", "disable", "off"]:
        await r.delete(f"maintenance:{Dev_FINAL}")
        await m.reply("<blockquote><u><b>🟢 تم تعطيل وضع الصيانة</b></u>\n\nالبوت الآن متاح لجميع المستخدمين.</blockquote>")
    else:
        await m.reply("<blockquote>❌ <b>خيار غير صالح</b>\n\n<b>الاستخدام:</b>\n<code>صيانة تفعيل</code>\n<code>صيانة تعطيل</code></blockquote>")