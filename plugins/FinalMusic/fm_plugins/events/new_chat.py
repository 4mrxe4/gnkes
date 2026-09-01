# new_chat.py
from helpers.context import redis_proxy as r, dev_final_proxy as Dev_FINAL, k_proxy as k
from compat import Client, filters, types
from compat import ChatAdminRequired
from plugins.FinalMusic import app, config
FALLBACK_THUMB = "https://files.catbox.moe/8czm1s.png"

@Client.on_message(filters.new_chat_members & filters.group, group=18)
async def new_chat_member(_, message: types.Message):
    if message.new_chat_members:
        for member in message.new_chat_members:
            if member.id == app.me.id:
                chat = message.chat
                chat_name = chat.title
                chat_id = chat.id
                chat_username = f"@{chat.username}" if chat.username else "مجموعة خاصة"
                members_count = await app.get_chat_members_count(chat_id)
                added_by = message.from_user
                added_by_name = added_by.mention if added_by else "غير معروف"
                text = f"""<blockquote>🟢 <b>تم إضافة البوت إلى مجموعة جديدة</b></blockquote>
<blockquote>
🔖 <b>اسم المجموعة:</b> {chat_name}
🆔 <b>آيدي المجموعة:</b> <code>{chat_id}</code>
👤 <b>معرف المجموعة:</b> {chat_username}
🔗 <b>رابط المجموعة:</b> {f"https://t.me/{chat.username}" if chat.username else "لا يوجد"}
👥 <b>عدد الأعضاء:</b> {members_count}
🤵 <b>أُضيف بواسطة:</b> {added_by_name}
</blockquote>"""
                try:
                    photo_to_send = config.START_IMG or FALLBACK_THUMB
                    await app.send_photo(chat_id=config.LOGGER_ID, photo=photo_to_send, caption=text)
                except:
                    pass
                break

@Client.on_message(filters.left_chat_member & filters.group, group=17)
async def left_chat_member(_, message: types.Message):
    if message.left_chat_member and message.left_chat_member.id == app.me.id:
        chat = message.chat
        chat_name = chat.title
        chat_id = chat.id
        chat_username = f"@{chat.username}" if chat.username else "مجموعة خاصة"
        removed_by = message.from_user
        removed_by_name = removed_by.mention if removed_by else "غير معروف"
        text = f"""<blockquote>🔴 <b>تم طرد/مغادرة البوت من المجموعة</b></blockquote>
<blockquote>
🔖 <b>اسم المجموعة:</b> {chat_name}
🆔 <b>آيدي المجموعة:</b> <code>{chat_id}</code>
👤 <b>معرف المجموعة:</b> {chat_username}
🔗 <b>رابط المجموعة:</b> {f"https://t.me/{chat.username}" if chat.username else "لا يوجد"}
🚫 <b>بواسطة:</b> {removed_by_name}</blockquote>"""
        try:
            photo_to_send = config.START_IMG or FALLBACK_THUMB
            await app.send_photo(chat_id=config.LOGGER_ID, photo=photo_to_send, caption=text)
        except:
            pass