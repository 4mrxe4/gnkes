from helpers.context import get_global_r, get_global_dev, get_global_k
r = get_global_r()
Dev_FINAL = get_global_dev()
k = get_global_k()
import random, re, time, pytz
import html
from datetime import datetime
from threading import Thread
from compat import *
from compat import *
from compat import *
# NOTE: compat.py does `import datetime` (the module) and its __all__
# doesn't exclude that name, so "from compat import *" above re-exports
# the module and overwrites the class imported by
# "from datetime import datetime" earlier in this file. That's what made
# datetime.now(...) fail with "module 'datetime' has no attribute 'now'" —
# it was actually calling module.now() instead of class.now().
# Re-import the class last so it wins.
from datetime import datetime
from helpers.ranks import *
from .buttons import register_buttons, get_button_custom, get_button_color, create_button_raw
from helpers.http import telegram_api_post
from helpers.emoji import render_custom_emoji_entities
from helpers.replies_store import (
    plugins_welcome_101,
    plugins_welcome_104,
    plugins_welcome_108,
    plugins_welcome_110,
    plugins_welcome_114,
    plugins_welcome_116,
    plugins_welcome_119,
    plugins_welcome_123,
    plugins_welcome_126,
    plugins_welcome_130,
    plugins_welcome_133,
    plugins_welcome_137,
    plugins_welcome_141,
    plugins_welcome_145,
    plugins_welcome_150,
    plugins_welcome_154,
    plugins_welcome_173,
    plugins_welcome_175,
    plugins_welcome_189,
    plugins_welcome_193,
    plugins_welcome_212,
    plugins_welcome_214,
    plugins_welcome_228,
    plugins_welcome_233,
    plugins_welcome_238,
    plugins_welcome_242,
    plugins_welcome_244,
    plugins_welcome_248,
    plugins_welcome_250,
    plugins_welcome_95,
    plugins_welcome_98,
)

WELCOME_BUTTONS_DEFINITIONS = {
    "welcome_smart": {
        "name": "أزرار الترحيب والتوديع الذكي",
        "buttons": [
            {"id": "owner_btn", "default": "المالك"},
            {"id": "group_btn", "default": "رابط المجموعة"},
        ]
    }
}

register_buttons(WELCOME_BUTTONS_DEFINITIONS)



DEFAULT_SMART_WELCOME = """⁣⁣ᯓ˹𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐓𝐎 #المجموعة 𝐆𝐑𝐎𝐔𝐏  ᯤ˼
°•——————#المجموعة —————•°
°︙ نورت قروبنا يـ  『#المنشن』 🥂✨. 
°︙ اسمك ⇚『#الاسم』 
°︙ ايديك ⇚『#الايدي』 
°︙ يوزرك ⇚『#اليوزر』

<blockquote expandable>°︙ تاريخ انضمامك ☜ #التاريخ 
°︙ الساعة ☜ #الوقت.</blockquote>
°•——————#المجموعة —————•°"""

DEFAULT_SMART_GOODBYE = """⁣⁣ᯓ˹ 𝐆𝐎𝐎𝐃 𝐁𝐘𝐄 ᯤ˼
°•——————#المجموعة —————•°
°︙ في امان الله يالحبيب 『#المنشن』 . 
°︙ متى ماحبيت اهلا فيك بمجموعتنا 
°︙ لو احد ازعجك تقدر تتواصل مع المالك

<blockquote expandable>°︙ تاريخ المغادرة ☜ #التاريخ 
°︙ الساعة ☜ #الوقت.</blockquote>
°•——————#المجموعة —————•°"""

@Client.on_message(filters.group & filters.text, group=-43)
async def setWelcomeSmartHandler(c, m):
    if m.chat.type == enums.ChatType.CHANNEL:
        return
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    k = await r.get(f"{Dev_FINAL}:botkey")
    await welcomeSmartFunc(c, m, k)

async def welcomeSmartFunc(c, m, k):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    
    if not await check_global_restrictions(c, m, k):
        return
    
    text = m.text
    name = await r.get(f"{Dev_FINAL}:BotName") if await r.get(f"{Dev_FINAL}:BotName") else "فاينل"
    if text.startswith(f"{name} "):
        text = text.replace(f"{name} ", "")
    if await r.get(f"{m.chat.id}:Custom:{m.chat.id}{Dev_FINAL}&text={text}"):
        text = await r.get(f"{m.chat.id}:Custom:{m.chat.id}{Dev_FINAL}&text={text}")
    if await r.get(f"Custom:{Dev_FINAL}&text={text}"):
        text = await r.get(f"Custom:{Dev_FINAL}&text={text}")
    if await check_and_guard_locked_command(c, m, k, text):
        return

    if text == "الغاء":
        if await r.get(f"{m.chat.id}:setWelcome:{m.from_user.id}{Dev_FINAL}"):
            await r.delete(f"{m.chat.id}:setWelcome:{m.from_user.id}{Dev_FINAL}")
            return await m.reply(plugins_welcome_95(k))
        if await r.get(f"{m.chat.id}:setRules:{m.from_user.id}{Dev_FINAL}"):
            await r.delete(f"{m.chat.id}:setRules:{m.from_user.id}{Dev_FINAL}")
            return await m.reply(plugins_welcome_98(k))
        if await r.get(f"{m.chat.id}:setSmartWelcome:{m.from_user.id}{Dev_FINAL}"):
            await r.delete(f"{m.chat.id}:setSmartWelcome:{m.from_user.id}{Dev_FINAL}")
            return await m.reply(plugins_welcome_101(k))
        if await r.get(f"{m.chat.id}:setSmartGoodbye:{m.from_user.id}{Dev_FINAL}"):
            await r.delete(f"{m.chat.id}:setSmartGoodbye:{m.from_user.id}{Dev_FINAL}")
            return await m.reply(plugins_welcome_104(k))

    if text == "ضع صورة الترحيب الذكي" and m.reply_to_message and m.reply_to_message.photo:
        if not await gowner_pls(m.from_user.id, m.chat.id, c):
            return await m.reply(plugins_welcome_108(k))
        await r.set(f"{m.chat.id}:SmartWelcomePhoto:{Dev_FINAL}", m.reply_to_message.photo.file_id)
        return await m.reply(plugins_welcome_110(k))

    if text == "ضع صورة التوديع" and m.reply_to_message and m.reply_to_message.photo:
        if not await gowner_pls(m.from_user.id, m.chat.id, c):
            return await m.reply(plugins_welcome_114(k))
        await r.set(f"{m.chat.id}:SmartGoodbyePhoto:{Dev_FINAL}", m.reply_to_message.photo.file_id)
        return await m.reply(plugins_welcome_116(k))

    if text in ["ضع صورة الترحيب الذكي", "ضع صورة التوديع"] and not m.reply_to_message:
        return await m.reply(plugins_welcome_119(k))

    if text == "تفعيل التوديع":
        if not await gowner_pls(m.from_user.id, m.chat.id, c):
            return await m.reply(plugins_welcome_123(k))
        await r.set(f"{m.chat.id}:SmartGoodbye:{Dev_FINAL}", 1)
        await r.delete(f"{m.chat.id}:disableSmartGoodbye:{Dev_FINAL}")
        return await m.reply(plugins_welcome_126(k))

    if text == "تعطيل التوديع":
        if not await gowner_pls(m.from_user.id, m.chat.id, c):
            return await m.reply(plugins_welcome_130(k))
        await r.set(f"{m.chat.id}:disableSmartGoodbye:{Dev_FINAL}", 1)
        await r.delete(f"{m.chat.id}:SmartGoodbye:{Dev_FINAL}")
        return await m.reply(plugins_welcome_133(k))

    if text == "تفعيل الترحيب الذكي":
        if not await gowner_pls(m.from_user.id, m.chat.id, c):
            return await m.reply(plugins_welcome_137(k))
        await r.set(f"{m.chat.id}:disableWelcome:{Dev_FINAL}", 1)
        await r.set(f"{m.chat.id}:SmartWelcome:{Dev_FINAL}", 1)
        await r.delete(f"{m.chat.id}:disableSmartWelcome:{Dev_FINAL}")
        return await m.reply(plugins_welcome_141(k))
    
    if text == "تعطيل الترحيب الذكي":
        if not await gowner_pls(m.from_user.id, m.chat.id, c):
            return await m.reply(plugins_welcome_145(k))
        await r.set(f"{m.chat.id}:disableSmartWelcome:{Dev_FINAL}", 1)
        await r.delete(f"{m.chat.id}:SmartWelcome:{Dev_FINAL}")
        if await r.get(f"{m.chat.id}:disableWelcome:{Dev_FINAL}"):
            await r.delete(f"{m.chat.id}:disableWelcome:{Dev_FINAL}")
        return await m.reply(plugins_welcome_150(k))

    if text == "ضع التوديع":
        if not await gowner_pls(m.from_user.id, m.chat.id, c):
            return await m.reply(plugins_welcome_154(k))
        await r.set(f"{m.chat.id}:setSmartGoodbye:{m.from_user.id}{Dev_FINAL}", 1)
        reply_text = """تمام عيني  
ارسل رسالة التوديع الحين

الدوال المتاحة للتوديع:
اظهار اسم المجموعه - #المجموعة
اظهار اسم العضو - #الاسم
اظهار منشن العضو - #المنشن
اظهار اليوزر - #اليوزر
اظهار الايدي - #الايدي
اظهار تاريخ المغادرة - #التاريخ
اظهار وقت المغادرة - #الوقت
اظهار قوانين المجموعه - #القوانين
"""
        return await m.reply(reply_text)

    if text == "مسح التوديع":
        if not await gowner_pls(m.from_user.id, m.chat.id, c):
            return await m.reply(plugins_welcome_173(k))
        await r.delete(f"{m.chat.id}:CustomSmartGoodbye:{Dev_FINAL}")
        return await m.reply(plugins_welcome_175(k))

    if await r.get(f"{m.chat.id}:setSmartGoodbye:{m.from_user.id}{Dev_FINAL}"):
        custom_text = m.text
        if m.entities:
            custom_text = render_custom_emoji_entities(custom_text, m.entities)
        await r.set(f"{m.chat.id}:CustomSmartGoodbye:{Dev_FINAL}", custom_text)
        await r.delete(f"{m.chat.id}:setSmartGoodbye:{m.from_user.id}{Dev_FINAL}")
        return await m.reply(plugins_welcome_189(k))

    if text == "ضع الترحيب الذكي":
        if not await gowner_pls(m.from_user.id, m.chat.id, c):
            return await m.reply(plugins_welcome_193(k))
        await r.set(f"{m.chat.id}:setSmartWelcome:{m.from_user.id}{Dev_FINAL}", 1)
        reply_text = """تمام عيني  
ارسل رسالة الترحيب الذكي الحين

الدوال المتاحة للترحيب الذكي:
اظهار اسم المجموعه - #المجموعة
اظهار اسم العضو - #الاسم
اظهار منشن العضو - #المنشن
اظهار اليوزر - #اليوزر
اظهار الايدي - #الايدي
اظهار تاريخ الدخول - #التاريخ
اظهار وقت الدخول - #الوقت
اظهار قوانين المجموعه - #القوانين
"""
        return await m.reply(reply_text)
    
    if text == "مسح الترحيب الذكي":
        if not await gowner_pls(m.from_user.id, m.chat.id, c):
            return await m.reply(plugins_welcome_212(k))
        await r.delete(f"{m.chat.id}:CustomSmartWelcome:{Dev_FINAL}")
        return await m.reply(plugins_welcome_214(k))
    
    if await r.get(f"{m.chat.id}:setSmartWelcome:{m.from_user.id}{Dev_FINAL}"):
        custom_text = m.text
        if m.entities:
            custom_text = render_custom_emoji_entities(custom_text, m.entities)
        await r.set(f"{m.chat.id}:CustomSmartWelcome:{Dev_FINAL}", custom_text)
        await r.delete(f"{m.chat.id}:setSmartWelcome:{m.from_user.id}{Dev_FINAL}")
        return await m.reply(plugins_welcome_228(k))

    if await r.get(f"{m.chat.id}:setRules:{m.from_user.id}{Dev_FINAL}") and await mod_pls(m.from_user.id, m.chat.id, c):
        await r.set(f"{m.chat.id}:CustomRules:{Dev_FINAL}", m.html)
        await r.delete(f"{m.chat.id}:setRules:{m.from_user.id}{Dev_FINAL}")
        return await m.reply(plugins_welcome_233(k))

    if await r.get(f"{m.chat.id}:setWelcome:{m.from_user.id}{Dev_FINAL}") and await mod_pls(m.from_user.id, m.chat.id, c):
        await r.set(f"{m.chat.id}:CustomWelcome:{Dev_FINAL}", m.html)
        await r.delete(f"{m.chat.id}:setWelcome:{m.from_user.id}{Dev_FINAL}")
        return await m.reply(plugins_welcome_238(k))

    if text == "مسح القوانين":
        if not await mod_pls(m.from_user.id, m.chat.id, c):
            return await m.reply(plugins_welcome_242(k))
        await r.delete(f"{m.chat.id}:CustomRules:{Dev_FINAL}")
        return await m.reply(plugins_welcome_244(k))

    if text == "وضع قوانين":
        if not await mod_pls(m.from_user.id, m.chat.id, c):
            return await m.reply(plugins_welcome_248(k))
        await r.set(f"{m.chat.id}:setRules:{m.from_user.id}{Dev_FINAL}", 1)
        return await m.reply(plugins_welcome_250(k))


async def send_smart_welcome(c, chat, new_member, chat_title, bot_username):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    
    try:
        welcome = await r.get(f"{chat.id}:CustomSmartWelcome:{Dev_FINAL}") or DEFAULT_SMART_WELCOME
        
        rules_raw = await r.get(f"{chat.id}:CustomRules:{Dev_FINAL}") or f"""{k} ممنوع نشر الروابط 
{k} ممنوع التكلم او نشر صور اباحيه 
{k} ممنوع اعاده توجيه 
{k} ممنوع العنصرية بكل انواعها 
{k} الرجاء احترام المدراء والادمنيه"""
        
        rules = f"<blockquote expandable>{rules_raw}</blockquote>"
        
        TIME_ZONE = "Asia/Riyadh"
        ZONE = pytz.timezone(TIME_ZONE)
        TIME = datetime.now(ZONE)
        clock = TIME.strftime("%I:%M %p")
        date = TIME.strftime("%Y/%m/%d")
        
        name = new_member.first_name
        if new_member.last_name:
            name = f"{new_member.first_name} {new_member.last_name}"
        
        username = f"@{new_member.username}" if new_member.username else f"@{bot_username}"
        mention = f'<a href="tg://user?id={new_member.id}">{html.escape(str(name))}</a>'
        user_id = new_member.id
        
        w = (welcome
             .replace("#القوانين", rules)
             .replace("#المجموعة", chat_title)
             .replace("#الاسم", name)
             .replace("#المنشن", mention)
             .replace("#اليوزر", username)
             .replace("#الايدي", f"<code>{user_id}</code>")
             .replace("#التاريخ", date)
             .replace("#الوقت", clock))
        
        photo = await r.get(f"{chat.id}:SmartWelcomePhoto:{Dev_FINAL}")
        
        owner_id, owner_name = None, "المالك"
        try:
            async for member in chat.get_members(filter=ChatMembersFilter.ADMINISTRATORS):
                if member.status == ChatMemberStatus.OWNER:
                    owner_user = member.user
                    owner_id = owner_user.id
                    owner_name = owner_user.first_name[:20] + "..." if len(owner_user.first_name) > 20 else owner_user.first_name
                    break
        except Exception as e:
            print(f"[WELCOME] Error owner: {e}")
            
        group_link = chat.invite_link or (f"https://t.me/{chat.username}" if chat.username else None)
        if not group_link:
            try:
                group_link = await c.export_chat_invite_link(chat.id)
            except:
                group_link = None
        
        owner_btn = await create_button_raw("welcome_smart", "owner_btn", owner_name, url=f"tg://user?id={owner_id}") if owner_id else await create_button_raw("welcome_smart", "owner_btn", "المالك", callback_data="owner_info")
        group_btn_text = chat_title[:20] + "..." if len(chat_title) > 20 else chat_title
        group_btn = await create_button_raw("welcome_smart", "group_btn", group_btn_text, url=group_link) if group_link else await create_button_raw("welcome_smart", "group_btn", group_btn_text, callback_data="group_info")
        
        reply_markup = {"inline_keyboard": [[owner_btn], [group_btn]]}
        bot_token = c.bot_token
        
        if photo:
            payload = {"chat_id": chat.id, "photo": photo, "caption": w, "parse_mode": "HTML", "reply_markup": reply_markup, "show_caption_above_media": True}
            result = await telegram_api_post(bot_token, "sendPhoto", payload)
            if result.get("ok"): return result

        payload = {"chat_id": chat.id, "text": w, "parse_mode": "HTML", "reply_markup": reply_markup, "disable_web_page_preview": True}
        result = await telegram_api_post(bot_token, "sendMessage", payload)
        return result if result.get("ok") else None
    except Exception as e:
        print(f"[WELCOME] Error: {e}")
        return None


async def send_smart_goodbye_dm(c, chat, left_member, chat_title, bot_username):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    
    try:
        goodbye = await r.get(f"{chat.id}:CustomSmartGoodbye:{Dev_FINAL}") or DEFAULT_SMART_GOODBYE
        
        rules_raw = await r.get(f"{chat.id}:CustomRules:{Dev_FINAL}") or f"""{k} ممنوع نشر الروابط 
{k} ممنوع التكلم او نشر صور اباحيه 
{k} ممنوع اعاده توجيه 
{k} ممنوع العنصرية بكل انواعها 
{k} الرجاء احترام المدراء والادمنيه"""
        
        rules = f"<blockquote expandable>{rules_raw}</blockquote>"
        
        TIME_ZONE = "Asia/Riyadh"
        ZONE = pytz.timezone(TIME_ZONE)
        TIME = datetime.now(ZONE)
        clock = TIME.strftime("%I:%M %p")
        date = TIME.strftime("%Y/%m/%d")
        
        name = left_member.first_name
        if left_member.last_name:
            name = f"{left_member.first_name} {left_member.last_name}"
        
        username = f"@{left_member.username}" if left_member.username else f"@{bot_username}"
        mention = f'<a href="tg://user?id={left_member.id}">{html.escape(str(name))}</a>'
        user_id = left_member.id
        
        w = (goodbye
             .replace("#القوانين", rules)
             .replace("#المجموعة", chat_title)
             .replace("#الاسم", name)
             .replace("#المنشن", mention)
             .replace("#اليوزر", username)
             .replace("#الايدي", f"<code>{user_id}</code>")
             .replace("#التاريخ", date)
             .replace("#الوقت", clock))
        
        photo = await r.get(f"{chat.id}:SmartGoodbyePhoto:{Dev_FINAL}")
        
        owner_id, owner_name = None, "المالك"
        try:
            async for member in chat.get_members(filter=ChatMembersFilter.ADMINISTRATORS):
                if member.status == ChatMemberStatus.OWNER:
                    owner_user = member.user
                    owner_id = owner_user.id
                    owner_name = owner_user.first_name[:20] + "..." if len(owner_user.first_name) > 20 else owner_user.first_name
                    break
        except Exception as e:
            print(f"[GOODBYE] Error owner: {e}")
            
        group_link = chat.invite_link or (f"https://t.me/{chat.username}" if chat.username else None)
        if not group_link:
            try:
                group_link = await c.export_chat_invite_link(chat.id)
            except:
                group_link = None
        
        owner_btn = await create_button_raw("welcome_smart", "owner_btn", owner_name, url=f"tg://user?id={owner_id}") if owner_id else await create_button_raw("welcome_smart", "owner_btn", "المالك", callback_data="owner_info")
        group_btn_text = chat_title[:20] + "..." if len(chat_title) > 20 else chat_title
        group_btn = await create_button_raw("welcome_smart", "group_btn", group_btn_text, url=group_link) if group_link else await create_button_raw("welcome_smart", "group_btn", group_btn_text, callback_data="group_info")
        
        reply_markup = {"inline_keyboard": [[owner_btn], [group_btn]]}
        bot_token = c.bot_token
        
        if photo:
            payload = {"chat_id": left_member.id, "photo": photo, "caption": w, "parse_mode": "HTML", "reply_markup": reply_markup, "show_caption_above_media": True}
            result = await telegram_api_post(bot_token, "sendPhoto", payload)
            if result.get("ok"): return result

        payload = {"chat_id": left_member.id, "text": w, "parse_mode": "HTML", "reply_markup": reply_markup, "disable_web_page_preview": True}
        result = await telegram_api_post(bot_token, "sendMessage", payload)
        return result if result.get("ok") else None
    except Exception as e:
        print(f"[GOODBYE] Error sending DM (User might have blocked the bot): {e}")
        return None


@Client.on_chat_member_updated(group=-44)
async def chatMemberUpdateHandler(c: Client, u: ChatMemberUpdated):
    if u.chat.type == enums.ChatType.CHANNEL:
        return
    
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    
    try:
        if not await check_global_restrictions(c, u, k):
            return
    except:
        pass
        
    bot_username = await r.get(f"{Dev_FINAL}:BotChannel") or "eFFb0t"
    
    old_status = u.old_chat_member.status if u.old_chat_member else None
    new_status = u.new_chat_member.status if u.new_chat_member else None
    
    was_member = old_status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER, ChatMemberStatus.RESTRICTED]
    is_member = new_status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER, ChatMemberStatus.RESTRICTED]
    
    if (not was_member or old_status in [ChatMemberStatus.LEFT, ChatMemberStatus.BANNED]) and is_member:
        new_member = u.new_chat_member.user if u.new_chat_member else u.from_user
        if not new_member or new_member.id == int(Dev_FINAL):
            return
        
        if await r.get(f"{u.chat.id}:enableVerify:{Dev_FINAL}") and not await pre_pls(new_member.id, u.chat.id, c):
            return
        
        chat_title = u.chat.title
        is_smart_enabled = await r.get(f"{u.chat.id}:SmartWelcome:{Dev_FINAL}")
        is_smart_disabled = await r.get(f"{u.chat.id}:disableSmartWelcome:{Dev_FINAL}")
        
        if is_smart_enabled and not is_smart_disabled:
            try:
                await send_smart_welcome(c, u.chat, new_member, chat_title, bot_username)
            except Exception as e:
                print(f"[WELCOME UPDATE] Error: {e}")

    elif was_member and (not is_member or new_status in [ChatMemberStatus.LEFT, ChatMemberStatus.BANNED]):
        left_member = u.old_chat_member.user if u.old_chat_member else u.from_user
        if not left_member or left_member.id == int(Dev_FINAL):
            return
        
        is_goodbye_enabled = await r.get(f"{u.chat.id}:SmartGoodbye:{Dev_FINAL}")
        is_goodbye_disabled = await r.get(f"{u.chat.id}:disableSmartGoodbye:{Dev_FINAL}")
        
        if is_goodbye_enabled and not is_goodbye_disabled:
            try:
                await send_smart_goodbye_dm(c, u.chat, left_member, u.chat.title, bot_username)
            except Exception as e:
                print(f"[GOODBYE UPDATE] Error: {e}")