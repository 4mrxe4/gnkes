# channelplay.py
from helpers.context import get_current_bot_id, get_global_k, redis_proxy as r, dev_final_proxy as Dev_FINAL, k_proxy as k
from compat import Client, filters, types
from compat import ChatMemberStatus
from plugins.FinalMusic import app, config
from helpers.ranks import *

@Client.on_message(filters.group & ~filters.bot, group=630)
async def channelplay_handler(c, m: types.Message):
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
    k = await r.get(f'{get_current_bot_id() or Dev_FINAL}:botkey')
    name = await r.get(f'{Dev_FINAL}:BotName')
    text = m.text
    if name and text.startswith(f'{name} '):
        text = text.replace(f'{name} ', '')
    if not text.startswith("channelplay") and not text.startswith("ربط_قناة"):
        return
    try:
        await m.delete()
    except:
        pass
    member = await app.get_chat_member(m.chat.id, m.from_user.id)
    if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
        return await m.reply(f"{k} هذا الأمر مخصص للمشرفين فقط")
    parts = text.split()
    if len(parts) < 2:
        return await m.reply(f"{k} استخدام:\n`channelplay linked` - ربط القناة المرتبطة\n`channelplay [آيدي_القناة]` - ربط قناة معينة\n`channelplay disable` - تعطيل")
    query = " ".join(parts[1:])
    if query.lower() in ["disable", "تعطيييل", "ايقاااااف"]:
        await r.delete(f"cmode:{m.chat.id}:{Dev_FINAL}")
        await r.delete(f"cmode_group:{m.chat.id}:{Dev_FINAL}")
        return await m.reply(f"{k} تم تعطيل وضع تشغيل القنوات")
    if query.lower() in ["linked", "المرتبطة", "المربوطة"]:
        chat = await app.get_chat(m.chat.id)
        if chat.linked_chat:
            channel_id = chat.linked_chat.id
            await r.set(f"cmode:{m.chat.id}:{Dev_FINAL}", str(channel_id))
            await r.set(f"cmode_group:{m.chat.id}:{Dev_FINAL}", str(m.chat.id))
            return await m.reply(f"{k} تم تفعيل تشغيل القنوات لـ: {chat.linked_chat.title}\nآيدي القناة: `{chat.linked_chat.id}`")
        else:
            return await m.reply(f"{k} هذه المجموعة غير مرتبطة بأي قناة")
    if query.lstrip("-").isdigit():
        channel_id = int(query)
    else:
        return await m.reply(f"{k} يجب إدخال آيدي القناة بشكل صحيح")
    try:
        chat = await app.get_chat(channel_id)
    except Exception as e:
        return await m.reply(f"{k} فشل في جلب القناة\nالخطأ: {type(e).__name__}")
    if chat.type != types.ChatType.CHANNEL:
        return await m.reply(f"{k} هذا الأمر يدعم القنوات فقط")
    owner_id = None
    try:
        async for user in app.get_chat_members(chat.id, filter=ChatMemberStatus.ADMINISTRATOR):
            if user.status == ChatMemberStatus.OWNER:
                owner_id = user.user.id
                break
    except:
        return await m.reply(f"{k} فشل في جلب مالك القناة")
    if not owner_id:
        return await m.reply(f"{k} لم يتم العثور على مالك القناة")
    if owner_id != m.from_user.id:
        return await m.reply(f"{k} يجب أن تكون مالك القناة {chat.title} لربطها")
    await r.set(f"cmode:{m.chat.id}:{Dev_FINAL}", str(channel_id))
    await r.set(f"cmode_group:{m.chat.id}:{Dev_FINAL}", str(m.chat.id))
    await m.reply(f"{k} تم تفعيل وضع تشغيل القنوات بنجاح لـ: {chat.title}\nآيدي القناة: `{channel_id}`")