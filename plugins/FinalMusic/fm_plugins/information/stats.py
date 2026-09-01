# stats.py
from helpers.context import get_current_bot_id, get_global_k, redis_proxy as r, dev_final_proxy as Dev_FINAL, k_proxy as k
import os
import platform
import sys
import psutil
from compat import Client, filters
from compat import Message
from pytgcalls import __version__ as pytgver
from plugins.FinalMusic import app, config, userbot
from helpers.ranks import *
@Client.on_message(filters.group & ~filters.bot, group=610)
async def stats_handler(c, m: Message):
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
    if text not in ["الاحصائيات", "الاحصائيات"]:
        return
    if m.from_user.id not in app.sudoers:
        return
    try:
        await m.delete()
    except:
        pass
    sent = await m.reply_photo(photo=config.PING_IMG, caption="جاري جلب الإحصائيات...")
    pid = os.getpid()
    cpu_percent = psutil.cpu_percent(interval=0.5)
    cpu_count = psutil.cpu_count()
    mem = psutil.virtual_memory()
    used_mem = round(mem.used / (1024 ** 3), 2)
    total_mem = round(mem.total / (1024 ** 3), 2)
    disk = psutil.disk_usage("/")
    used_disk = round(disk.used / (1024 ** 3), 2)
    total_disk = round(disk.total / (1024 ** 3), 2)
    chats = await r.smembers(f"chats:{Dev_FINAL}") or []
    users = await r.smembers(f"users:{Dev_FINAL}") or []
    blacklisted = await r.smembers(f"blacklist_chats:{Dev_FINAL}") or []
    sudoers = await r.smembers(f"sudoers:{Dev_FINAL}") or []
    from plugins.FinalMusic.fm_plugins import all_modules
    _utext = f"""<b>📊 إحصائيات البوت</b>

<b>👤 البوت:</b> {app.name}
<b>📦 الحسابات المساعدة:</b> {len(userbot.clients)}
<b>🚀 المغادرة التلقائية:</b> {config.AUTO_LEAVE}
<b>🚫 المجموعات المحظورة:</b> {len(blacklisted)}
<b>👥 المستخدمين المحظورين:</b> {len(app.bl_users)}
<b>⭐ المطورين:</b> {len(sudoers)}
<b>💬 المجموعات:</b> {len(chats)}
<b>👤 المستخدمين:</b> {len(users)}

<b>⚙️ النظام:</b>
<b>📚 الملفات:</b> {len(all_modules)}
<b>🖥️ النظام:</b> {platform.system()}
<b>🧠 الذاكرة:</b> {used_mem} GB | {total_mem} GB
<b>💻 المعالج:</b> {cpu_percent}% ({cpu_count} نواة)
<b>💾 التخزين:</b> {used_disk} GB | {total_disk} GB
<b>🐍 بايثون:</b> {sys.version.split()[0]}
<b>📦 PyTgCalls:</b> {pytgver}"""
    try:
        await sent.edit_caption(_utext)
    except AttributeError:
        await sent.edit_message_caption(caption=_utext)