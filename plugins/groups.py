from helpers.context import get_global_r, get_global_dev, get_global_k
r = get_global_r()
Dev_FINAL = get_global_dev()
k = get_global_k()
import random
import asyncio
import html
import os
import re
import time
from datetime import datetime, timedelta
from io import BytesIO
from threading import Thread

from compat import Client, filters
from compat import *
from compat import FileId, FileType, ThumbnailSource
from helpers.quran import *
from helpers.memes import *
from helpers.ranks import *
from .buttons import register_buttons, get_button_custom, get_button_color, create_button_raw, send_telegram_api
from helpers.replies_store import (
    REPLIES,
    plugins_groups_125,
    plugins_groups_127,
    plugins_groups_418,
    plugins_groups_423,
    plugins_groups_427,
    plugins_groups_454,
    plugins_groups_455,
    plugins_groups_524,
)

BUTTONS_DEFINITIONS = {
    "groups": {
        "name": "أزرار المجموعات",
        "buttons": [
            {"id": "owner_btn", "default": "التفعيل"},
            {"id": "group_btn", "default": "المجموعه"},
            {"id": "leave_btn", "default": "مغادرة"},
            {"id": "dev_btn", "default": "🧚‍♀️"},
            {"id": "commands_btn", "default": "التفعيل"},
            {"id": "group_link", "default": "رابط المجموعة"},
            {"id": "msg_link", "default": "رابط الرسالة"},
        ]
    }
}

register_buttons(BUTTONS_DEFINITIONS)


async def get_group_invite_link(c, chat):
    """جلب رابط المجموعة بشكل مضمون سواء كانت عامة أو خاصة"""
    if chat.username:
        return f"https://t.me/{chat.username}"
    if chat.invite_link:
        return chat.invite_link
    try:
        full_chat = await c.get_chat(chat.id)
        if full_chat.invite_link:
            return full_chat.invite_link
    except Exception:
        pass
    try:
        return await c.export_chat_invite_link(chat.id)
    except Exception:
        return None


async def send_dev_notification(c, text, reply_markup=None):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    
    if await r.get(f'disable_join_notif:{Dev_FINAL}'):
        return

    dev_group = await r.get(f'DevGroup:{Dev_FINAL}')
    if dev_group:
        try:
            await c.send_message(int(dev_group), text, reply_markup=reply_markup, disable_web_page_preview=True)
        except Exception:
            pass
    else:
        owner = await r.get(f'{Dev_FINAL}botowner')
        if owner:
            try:
                await c.send_message(int(owner), text, reply_markup=reply_markup, disable_web_page_preview=True)
            except Exception:
                pass


async def get_chat_owner_info(c, chat_id):
    owner_id, owner_name, owner_username = None, "المالك", None
    try:
        admins = await c.get_chat_administrators(chat_id)
        for member in admins:
            if member.status == ChatMemberStatus.OWNER:
                owner_user = member.user
                owner_id = owner_user.id
                owner_username = owner_user.username
                owner_name = owner_user.first_name[:20] + "..." if len(owner_user.first_name) > 20 else owner_user.first_name
                break
    except Exception as e:
        print(f"[GROUPS] Error getting owner info: {e}")
    return owner_id, owner_name, owner_username


async def sync_group_admins(c, chat_id, Dev_FINAL):
    """مزامنة المالك والمشرفين فوراً وتخزينهم في الداتا بيس"""
    r = get_global_r()
    try:
        admins = await c.get_chat_administrators(chat_id)
        for member in admins:
            if member.user.is_bot or getattr(member.user, "is_deleted", False):
                continue
                
            if member.status == ChatMemberStatus.OWNER:
                await r.set(f'{chat_id}:rankGOWNER:{member.user.id}{Dev_FINAL}', 1)
                await r.sadd(f'{chat_id}:listGOWNER:{Dev_FINAL}', member.user.id)
                await r.sadd(f'{member.user.id}:groups', chat_id)
            elif member.status == ChatMemberStatus.ADMINISTRATOR:
                await r.set(f'{chat_id}:rankADMIN:{member.user.id}{Dev_FINAL}', 1)
                await r.sadd(f'{chat_id}:listADMIN:{Dev_FINAL}', member.user.id)
                
    except Exception as e:
        print(f"[GROUPS] Direct Sync Error: {e}")


@Client.on_callback_query(filters.regex(r"^leave_gp_(-?\d+)$"))
async def leave_group_callback(c, cb):
    """زر (مغادرة) في إشعار المطور: يترك رسائل وداع متتالية ثم يغادر فعلياً"""
    r = get_global_r()
    Dev_FINAL = get_global_dev()

    if not await dev_pls(cb.from_user.id, cb.message.chat.id):
        return await cb.answer("ماعندك صلاحية على هذا الزر", show_alert=True)

    target_chat_id = int(cb.data.split("leave_gp_")[1])
    await cb.answer("جاري المغادرة...")

    try:
        await c.send_message(target_chat_id, "مطوري عطاني امر اغادر  سلام")
        await asyncio.sleep(2)
        await c.send_message(target_chat_id, "وذي مو من مطوري بس عشان ضاله بنفسي")
        await asyncio.sleep(2)
        await c.send_message(target_chat_id, "🖕🏻")
    except Exception:
        pass

    try:
        await c.leave_chat(target_chat_id)
    except Exception as e:
        print(f"[GROUPS] Leave Button Error: {e}")

    # تسجيل وقت المغادرة لمدة 10 دقائق، لإظهار رسالة ترحيبية خاصة إن تمت إعادة الإضافة خلالها
    await r.set(f'left_group_time:{target_chat_id}:{Dev_FINAL}', int(time.time()), ex=600)
    await r.srem(f'enablelist:{Dev_FINAL}', target_chat_id)
    await r.delete(f'{target_chat_id}:enable:{Dev_FINAL}')
    await r.delete(f'{target_chat_id}:manual_disable:{Dev_FINAL}')

    try:
        if cb.message.text:
            await cb.edit_message_text(cb.message.text + "\n\n تم مغادرة المجموعة")
        elif cb.message.caption:
            await cb.edit_message_caption(cb.message.caption + "\n\n تم مغادرة المجموعة")
    except Exception:
        pass


async def handle_banned_group_rejoin(c, chat_id):
    """يتحقق إن كانت المجموعة محظورة، وينفذ رسائل التصعيد المناسبة ثم يغادر. يرجع True اذا كانت محظورة."""
    r = get_global_r()
    Dev_FINAL = get_global_dev()

    if not await r.hexists(f'bannedgroups_info:{Dev_FINAL}', str(chat_id)):
        return False

    stage = int((await r.get(f'{chat_id}:ban_stage:{Dev_FINAL}')) or 0)

    try:
        if stage == 0:
            await c.send_message(chat_id, "خبرتكم قبل بغادر بامر المطور .")
        elif stage == 1:
            await c.send_message(chat_id, "شكلكم ماتفهمون بالكلام الطيب")
            await asyncio.sleep(2)
            await c.send_message(chat_id, "🖕🏻🖕🏻🖕🏻")
        else:
            await c.send_message(chat_id, "🖕🏻🖕🏻")
    except Exception:
        pass

    await r.set(f'{chat_id}:ban_stage:{Dev_FINAL}', min(stage + 1, 2))

    try:
        await c.leave_chat(chat_id)
    except Exception as e:
        print(f"[GROUPS] Banned Group Leave Error: {e}")

    await r.srem(f'enablelist:{Dev_FINAL}', chat_id)
    await r.delete(f'{chat_id}:enable:{Dev_FINAL}')
    await r.delete(f'{chat_id}:manual_disable:{Dev_FINAL}')
    return True


@Client.on_chat_member_updated()
async def get_bot_status(c, m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = await r.get(f'{Dev_FINAL}:botkey') or get_global_k()
    
    try:
        if not m.new_chat_member:
            return
        
        if m.new_chat_member.status == ChatMemberStatus.MEMBER:
            if m.new_chat_member.user.id == c.id:
                if await handle_banned_group_rejoin(c, m.chat.id):
                    return

                try:
                    await c.send_message(
                        m.chat.id, 
                        f"{k} شوضعك يعني انا بوت خدمي حاطني عضو ؟\n{k} خل بوتاتك المخيسه تنفعك عن اذنك ."
                    )
                except:
                    pass
                
                await c.leave_chat(m.chat.id)
                
                await r.srem(f'enablelist:{Dev_FINAL}', m.chat.id)
                await r.delete(f'{m.chat.id}:enable:{Dev_FINAL}')
                await r.delete(f'{m.chat.id}:manual_disable:{Dev_FINAL}')
                
                text = f'{k} من「 {m.from_user.mention()} 」\n'
                usrr = '@' + m.from_user.username if m.from_user.username else 'مافيه'
                text += f'{k} يوزره : {usrr}\n'
                text += f'{k} ايديه : `{m.from_user.id}`\n\n'
                text += f'{k} تم تنزيل البوت أو إضافته كعضو، فغادر تلقائياً :\n\n'
                text += f'{k} اسم المجموعة : {m.chat.title}\n'
                chatusr = '@' + m.chat.username if m.chat.username else 'مافيه'
                text += f'{k} يوزر المجموعة : {chatusr}\n'
                text += f'{k} ايدي المجموعة : `{m.chat.id}`'
                
                if await r.smembers(f'enablelist:{Dev_FINAL}'):
                    text += f'\n{k} عدد المجموعات الآن : {len(await r.smembers(f"enablelist:{Dev_FINAL}"))}\n'
                text += '\n\n'
                
                await send_dev_notification(c, text)
                return

        elif m.new_chat_member.status == ChatMemberStatus.ADMINISTRATOR:
            if m.new_chat_member.user.id == c.id:
                if await handle_banned_group_rejoin(c, m.chat.id):
                    return

                if await r.get(f'{m.chat.id}:enable:{Dev_FINAL}') or await r.get(f'{m.chat.id}:manual_disable:{Dev_FINAL}'):
                    return
                if await r.get(f'DisableBot:{Dev_FINAL}'):
                    return await c.send_message(m.chat.id, f'{k} تم تعطيل البوت الخدمي من المطور')

                left_time = await r.get(f'left_group_time:{m.chat.id}:{Dev_FINAL}')
                if left_time and (time.time() - float(left_time)) <= 600:
                    await r.delete(f'left_group_time:{m.chat.id}:{Dev_FINAL}')
                    try:
                        await c.send_message(m.chat.id, "اي بوت كلب حاط تصبيعه فوق")
                        await asyncio.sleep(2)
                        await c.send_message(m.chat.id, "ذا مو انا اكيد")
                    except Exception:
                        pass
                    # يكمل التنفيذ بعدها ليتم التفعيل التلقائي بشكل طبيعي

                priv = m.new_chat_member
                is_channel = m.chat.type == ChatType.CHANNEL

                if is_channel:
                    # القنوات (مثل قناة التخزين/الأرشيف) لا تحتاج صلاحيات
                    # المجموعات (إدارة/حظر/تثبيت/دعوة) — فقط صلاحية نشر
                    # الرسائل، لأن كل ما يفعله البوت هناك هو حفظ ملفات صوتية.
                    permissions_ok = bool(priv.can_post_messages)
                else:
                    permissions_ok = bool(priv.can_manage_chat and priv.can_delete_messages and priv.can_restrict_members and priv.can_pin_messages and priv.can_invite_users)

                if not permissions_ok:
                    incomplete_msg = (
                        f"{k} الصلاحيات غير مكتملة!\n"
                        f"{k} أعطني صلاحية 「 نشر الرسائل 」 فقط ثم رجعني\n"
                        f"{k} سلام بغادر عن اذنك"
                        if is_channel else
                        f"{k} الصلاحيات غير مكتملة!\n"
                        f"{k}بعد ماتفكر تعطيني كل الصلاحيات رجعني\n"
                        f"{k} سلام بغادر عن اذنك"
                    )
                    await c.send_message(m.chat.id, incomplete_msg)
                    await c.leave_chat(m.chat.id)
                    
                    await r.srem(f'enablelist:{Dev_FINAL}', m.chat.id)
                    await r.delete(f'{m.chat.id}:enable:{Dev_FINAL}')
                    await r.delete(f'{m.chat.id}:manual_disable:{Dev_FINAL}')
                    
                    text = f'{k} من「 {m.from_user.mention()} 」\n'
                    usrr = '@' + m.from_user.username if m.from_user.username else 'مافيه'
                    text += f'{k} يوزره : {usrr}\n'
                    text += f'{k} ايديه : `{m.from_user.id}`\n\n'
                    text += f'{k} تم رفع البوت أدمن بصلاحيات ناقصة، فغادر تلقائياً :\n\n'
                    text += f'{k} اسم المجموعة : {m.chat.title}\n'
                    chatusr = '@' + m.chat.username if m.chat.username else 'مافيه'
                    text += f'{k} يوزر المجموعة : {chatusr}\n'
                    text += f'{k} ايدي المجموعة : `{m.chat.id}`'
                    
                    if await r.smembers(f'enablelist:{Dev_FINAL}'):
                        text += f'\n{k} عدد المجموعات الآن : {len(await r.smembers(f"enablelist:{Dev_FINAL}"))}\n'
                    text += '\n\n'
                    
                    await send_dev_notification(c, text)
                    return
                
                # تفعيل المجموعة
                await r.set(f'{m.chat.id}:enable:{Dev_FINAL}', 1)
                await r.sadd(f'enablelist:{Dev_FINAL}', m.chat.id)
                await r.set(f'{m.chat.id}:rankOWNER:{m.from_user.id}{Dev_FINAL}', 1)
                await r.sadd(f'{m.chat.id}:listOWNER:{Dev_FINAL}', m.from_user.id)

                # مزامنة المشرفين والمالك فوراً عند التفعيل
                await sync_group_admins(c, m.chat.id, Dev_FINAL)

                owner_id, owner_name, owner_username = await get_chat_owner_info(c, m.chat.id)
                chat_title = m.chat.title or "المجموعة"
                group_link = await get_group_invite_link(c, m.chat)
                
                if owner_username:
                    owner_url = f"https://t.me/{owner_username}"
                elif owner_id:
                    owner_url = f"tg://user?id={owner_id}"
                else:
                    owner_url = None

                owner_btn = await create_button_raw("groups", "owner_btn", owner_name, url=owner_url) if owner_url else await create_button_raw("groups", "owner_btn", owner_name, callback_data="owner_info")
                group_btn_text = chat_title[:20] + "..." if len(chat_title) > 20 else chat_title
                group_btn = await create_button_raw("groups", "group_btn", group_btn_text, url=group_link) if group_link else await create_button_raw("groups", "group_btn", group_btn_text, callback_data="group_info")
                
                reply_markup = {"inline_keyboard": [[owner_btn], [group_btn]]}
                user_mention = f'<a href="tg://user?id={m.from_user.id}">{html.escape(m.from_user.first_name)}</a>'
                text_msg = f"{k} من 「 {user_mention} 」\n{k} تم تفعيل المجموعة تلقائياً\n_"
                
                if not await r.get(f'disable_join_notif:{Dev_FINAL}'):
                    payload = {
                        "chat_id": m.chat.id,
                        "text": text_msg,
                        "parse_mode": "HTML",
                        "reply_markup": reply_markup
                    }
                    await send_telegram_api(c, "sendMessage", payload)
                
                usrr = '@' + m.from_user.username if m.from_user.username else 'مافيه'
                text = f'{k} من「 {m.from_user.mention()} 」\n'
                text += f'{k} يوزره : {usrr}\n'
                text += f'{k} ايديه : `{m.from_user.id}`\n\n'
                text += f'{k} تم تفعيل البوت بمجموعة جديدة :\n\n'
                text += f'{k} اسم المجموعة : {m.chat.title}\n'
                chatusr = '@' + m.chat.username if m.chat.username else 'مافيه'
                text += f'{k} يوزر المجموعة : {chatusr}\n'
                text += f'{k} ايدي المجموعة : `{m.chat.id}`'
                
                if await r.smembers(f'enablelist:{Dev_FINAL}'):
                    text += f'\n{k} عدد المجموعات الآن : {len(await r.smembers(f"enablelist:{Dev_FINAL}"))}\n'
                text += '\n\n'
                
                dev_buttons = []
                if group_link:
                    dev_buttons.append([InlineKeyboardButton(**(await create_button_raw("groups", "group_link", m.chat.title, url=group_link)))])
                leave_btn_raw = await create_button_raw("groups", "leave_btn", "مغادرة", callback_data=f"leave_gp_{m.chat.id}")
                dev_buttons.append([InlineKeyboardButton(**leave_btn_raw)])
                
                dev_reply_markup = InlineKeyboardMarkup(dev_buttons)
                await send_dev_notification(c, text, reply_markup=dev_reply_markup)

    except Exception as e:
        print(f"[GROUPS] ChatMemberUpdate Error: {e}")


@Client.on_message(filters.text & filters.group, group=1)
async def globalHandler(c, m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    await global_filter(c, m)


async def global_filter(c, m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if not await check_global_restrictions(c, m, k):
        return
    text = m.text
    name = await r.get(f'{Dev_FINAL}:BotName') if await r.get(f'{Dev_FINAL}:BotName') else 'فاينل'

    # معالجة أمر: الاسم مغادرة (مثل: فاينل مغادرة)
    if text == f'{name} مغادرة':
        if await dev_pls(m.from_user.id, m.chat.id) or await dev_pls(m.from_user.id, m.chat.id):
            await r.set(f'wait_leave_id:{m.from_user.id}:{Dev_FINAL}', 1)
            return await m.reply(f"{k} حسناً أرسل ID المجموعة")

    # استلام ID المجموعة وتنفيذ المغادرة
    if await r.get(f'wait_leave_id:{m.from_user.id}:{Dev_FINAL}'):
        if text.replace("-", "").isdigit():
            await r.delete(f'wait_leave_id:{m.from_user.id}:{Dev_FINAL}')
            target_chat_id = int(text)
            try:
                await r.set(f'{target_chat_id}:manual_disable:{Dev_FINAL}', 1)
                await r.delete(f'{target_chat_id}:enable:{Dev_FINAL}')
                await r.srem(f'enablelist:{Dev_FINAL}', target_chat_id)
                await c.leave_chat(target_chat_id)
                return await m.reply(f"{k} تمت مغادرة المجموعة")
            except Exception as e:
                return await m.reply(f"{k} حدث خطأ أو لم أتمكن من مغادرة المجموعة: {e}")

    # حظر مجموعة
    if text == 'حظر مجموعة':
        if await dev_pls(m.from_user.id, m.chat.id):
            await r.set(f'wait_ban_id:{m.from_user.id}:{Dev_FINAL}', 1)
            return await m.reply(f"{k} حسناً أرسل ID المجموعة")

    if await r.get(f'wait_ban_id:{m.from_user.id}:{Dev_FINAL}'):
        if text.replace("-", "").isdigit():
            await r.delete(f'wait_ban_id:{m.from_user.id}:{Dev_FINAL}')
            target_chat_id = int(text)

            try:
                chat_info = await c.get_chat(target_chat_id)
                chat_name = chat_info.title or str(target_chat_id)
            except Exception:
                chat_name = str(target_chat_id)

            await r.hset(f'bannedgroups_info:{Dev_FINAL}', str(target_chat_id), chat_name)
            await r.delete(f'{target_chat_id}:ban_stage:{Dev_FINAL}')

            try:
                await c.get_chat_member(target_chat_id, c.id)
                in_group = True
            except Exception:
                in_group = False

            if in_group:
                try:
                    await c.send_message(target_chat_id, "سيتم مغادرة المجموعة بأمر من المطور .")
                except Exception:
                    pass
                try:
                    await c.leave_chat(target_chat_id)
                except Exception as e:
                    print(f"[GROUPS] Ban Leave Error: {e}")
                await r.srem(f'enablelist:{Dev_FINAL}', target_chat_id)
                await r.delete(f'{target_chat_id}:enable:{Dev_FINAL}')
                await r.delete(f'{target_chat_id}:manual_disable:{Dev_FINAL}')

            return await m.reply(f"{k} تم حظر المجموعة")
        else:
            return await m.reply(f"{k} أرسل ID صحيح للمجموعة")

    # الغاء حظر مجموعة
    if text == 'الغاء حظر مجموعة':
        if await dev_pls(m.from_user.id, m.chat.id):
            await r.set(f'wait_unban_id:{m.from_user.id}:{Dev_FINAL}', 1)
            return await m.reply(f"{k} حسناً أرسل ID المجموعة")

    if await r.get(f'wait_unban_id:{m.from_user.id}:{Dev_FINAL}'):
        if text.replace("-", "").isdigit():
            await r.delete(f'wait_unban_id:{m.from_user.id}:{Dev_FINAL}')
            target_chat_id = int(text)
            await r.hdel(f'bannedgroups_info:{Dev_FINAL}', str(target_chat_id))
            await r.delete(f'{target_chat_id}:ban_stage:{Dev_FINAL}')
            return await m.reply(f"{k} تم الغاء حظر المجموعة")
        else:
            return await m.reply(f"{k} أرسل ID صحيح للمجموعة")

    # المجموعات المحظورة
    if text == 'المجموعات المحظورة':
        if await dev_pls(m.from_user.id, m.chat.id):
            banned = await r.hgetall(f'bannedgroups_info:{Dev_FINAL}')
            if not banned:
                return await m.reply(f"{k} لا توجد مجموعات محظورة حالياً")
            list_text = f"{k} جميع المجموعات المحظورة :\n\n"
            for gid, gname in banned.items():
                list_text += f"• {gname}\n-`{gid}`\n\n"
            return await m.reply(list_text)

    if text.startswith(f'{name} '):
        text = text.replace(f'{name} ', '')

    if text == 'المطور':
        id = int((await r.get(f'{Dev_FINAL}botowner')) or 0)
        try:
            get = await c.get_chat(id)
        except PeerIdInvalid:
            return await m.reply(plugins_groups_125(k))
        except Exception:
            return await m.reply(plugins_groups_127(k))
        bio = get.bio if get.bio else None

        try:
            owner = await c.get_users(id)
            owner_name = owner.first_name
            if owner.last_name:
                owner_name = f"{owner.first_name} {owner.last_name}"
            if len(owner_name) > 20:
                owner_name = owner_name[:20] + "..."
        except:
            owner_name = "🧚‍♀️"

        dev_btn = await create_button_raw("groups", "dev_btn", owner_name, user_id=id)
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(**dev_btn)]])

        if not get.photo:
            return await m.reply_animation('https://telegra.ph/file/d9127c65922817d127f04.mp4', caption=bio, reply_markup=reply_markup)
        else:
            async for photo in c.get_chat_photos(id, limit=1):
                return await m.reply_photo(photo.file_id, caption=bio, reply_markup=reply_markup)


@Client.on_message(filters.text & filters.group, group=2)
async def filtersHandler(c, m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    await get_filter(c, m)


async def get_filter(c, m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if not await check_global_restrictions(c, m, k):
        return


@Client.on_message(filters.text & filters.group, group=3)
async def randomfiltersHandler(c, m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    await get_rn_filter(c, m)


async def get_rn_filter(c, m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if not await check_global_restrictions(c, m, k):
        return
    text = m.text
    name = await r.get(f'{Dev_FINAL}:BotName') if await r.get(f'{Dev_FINAL}:BotName') else 'فاينل'
    if text.startswith(f'{name} '):
        text = text.replace(f'{name} ', '')

    if text == 'نادي المطور':
        await m.reply(REPLIES['plugins_groups_186'])
        k = await r.get(f'{Dev_FINAL}:botkey')
        dev_id = int((await r.get(f'{Dev_FINAL}botowner')) or 0)

        # جلب رابط المجموعة الحقيقي (سواء كانت عامة أو خاصة)
        chat_link = await get_group_invite_link(c, m.chat)

        chat_username = m.chat.username
        if chat_username:
            msg_link = f"https://t.me/{chat_username}/{m.id}"
        else:
            chat_id_str = str(m.chat.id).replace("-100", "")
            msg_link = f"https://t.me/c/{chat_id_str}/{m.id}"

        dev_text = f"{k} المستخدم {m.from_user.mention()} محتاجك بسرعة\n"
        dev_text += f"{k} اسم المجموعة : {m.chat.title}\n"
        dev_text += f"{k} ايدي المجموعة : `{m.chat.id}`"

        buttons = []
        if chat_link:
            group_link_btn = await create_button_raw("groups", "group_link", "رابط المجموعة", url=chat_link)
            buttons.append([InlineKeyboardButton(**group_link_btn)])

        msg_link_btn = await create_button_raw("groups", "msg_link", "رابط الرسالة", url=msg_link)
        buttons.append([InlineKeyboardButton(**msg_link_btn)])

        markup = InlineKeyboardMarkup(buttons)

        if await r.get(f'DevGroup:{Dev_FINAL}'):
            try:
                await c.send_message(int((await r.get(f'DevGroup:{Dev_FINAL}')) or 0), dev_text, reply_markup=markup, disable_web_page_preview=True)
            except:
                pass
        else:
            try:
                await c.send_message(dev_id, dev_text, reply_markup=markup, disable_web_page_preview=True)
            except:
                pass
        return


@Client.on_message(filters.left_chat_member)
async def kick_from_gp(c, m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if m.left_chat_member is None:
        return
    if m.left_chat_member.id == int(Dev_FINAL):
        k = await r.get(f'{Dev_FINAL}:botkey')
        text = f'{k} من「 {m.from_user.mention()} 」\n'
        usrr = '@' + m.from_user.username if m.from_user.username else 'مافيه'
        text += f'{k} يوزره : {usrr}\n'
        text += f'{k} ايديه : `{m.from_user.id}`\n'
        text += f'\n{k} قام بطرد البوت من المجموعة :\n\n'
        text += f'{k} اسم المجموعة : {m.chat.title}\n'
        chatusr = '@' + m.chat.username if m.chat.username else 'مافيه'
        text += f'{k} يوزر المجموعة : {chatusr}\n'
        text += f'{k} ايدي المجموعة : `{m.chat.id}`'
        await r.srem(f'enablelist:{Dev_FINAL}', m.chat.id)
        await r.delete(f'{m.chat.id}:enable:{Dev_FINAL}')
        if await r.smembers(f'enablelist:{Dev_FINAL}'):
            text += f'\n{k} عدد المجموعات الآن : {len(await r.smembers(f"enablelist:{Dev_FINAL}"))}\n'
        text += f'\n{k} تم مسح جميع بيانات المجموعة\n\n'
        await send_dev_notification(c, text)


@Client.on_message(filters.text & filters.group, group=5)
async def EnableAndDisablegroup(c, m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    text = m.text
    k = await r.get(f'{Dev_FINAL}:botkey')
    
    if text == 'تعطيل اشعارات الدخول':
        if await dev_pls(m.from_user.id, m.chat.id):
            await r.set(f'disable_join_notif:{Dev_FINAL}', 1)
            return await m.reply(plugins_groups_418(k))

    if text == 'تفعيل اشعارات الدخول':
        if await dev_pls(m.from_user.id, m.chat.id):
            await r.delete(f'disable_join_notif:{Dev_FINAL}')
            return await m.reply(plugins_groups_423(k))

    if text == 'تفعيل':
        if await r.get(f'{m.chat.id}:enable:{Dev_FINAL}'):
            return await m.reply(plugins_groups_427(k))
        if not (await m.chat.get_member(m.from_user.id)).status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR] and not await owner_pls(m.from_user.id, m.chat.id):
            return await m.reply(REPLIES['plugins_groups_429'])
        
        is_channel = m.chat.type == ChatType.CHANNEL
        if await r.get(f'{m.chat.id}:enable:{Dev_FINAL}'):
            return await m.reply(f'{k} القناة مفعلة من قبل يالطيب' if is_channel else f'{k} المجموعة مفعلة من قبل يالطيب')
            
        if await r.get(f'DisableBot:{Dev_FINAL}'):
            return await c.send_message(m.chat.id, f'{k} تم تعطيل البوت الخدمي من المطور')
            
        get = await c.get_chat_member(m.chat.id, c.id)
        priv = get
        if is_channel:
            missing_privileges = not priv.can_manage_chat or not priv.can_delete_messages
        else:
            missing_privileges = not priv.can_manage_chat or not priv.can_delete_messages or not priv.can_pin_messages or not priv.can_invite_users
            
        if missing_privileges:
            if is_channel:
                return await m.reply(plugins_groups_454(k))
            return await m.reply(plugins_groups_455(k))
        else:
            await r.delete(f'{m.chat.id}:manual_disable:{Dev_FINAL}')
            await r.set(f'{m.chat.id}:enable:{Dev_FINAL}', 1)
            await r.sadd(f'enablelist:{Dev_FINAL}', m.chat.id)
            await r.set(f'{m.chat.id}:rankOWNER:{m.from_user.id}{Dev_FINAL}', 1)
            await r.sadd(f'{m.chat.id}:listOWNER:{Dev_FINAL}', m.from_user.id)
            
            # مزامنة المالك والمشرفين فوراً
            await sync_group_admins(c, m.chat.id, Dev_FINAL)

            owner_id, owner_name, owner_username = await get_chat_owner_info(c, m.chat.id)
            chat_title = m.chat.title or "المجموعة"
            group_link = await get_group_invite_link(c, m.chat)
            
            if owner_username:
                owner_url = f"https://t.me/{owner_username}"
            elif owner_id:
                owner_url = f"tg://user?id={owner_id}"
            else:
                owner_url = None

            owner_btn = await create_button_raw("groups", "owner_btn", owner_name, url=owner_url) if owner_url else await create_button_raw("groups", "owner_btn", owner_name, callback_data="owner_info")
            group_btn_text = chat_title[:20] + "..." if len(chat_title) > 20 else chat_title
            group_btn = await create_button_raw("groups", "group_btn", group_btn_text, url=group_link) if group_link else await create_button_raw("groups", "group_btn", group_btn_text, callback_data="group_info")
            
            reply_markup = {"inline_keyboard": [[owner_btn], [group_btn]]}
            
            user_mention = f'<a href="tg://user?id={m.from_user.id}">{html.escape(m.from_user.first_name)}</a>'
            text_msg = f"{k} من 「 {user_mention} 」\n{k} تم تفعيل المجموعة\n_"
            
            payload = {
                "chat_id": m.chat.id,
                "text": text_msg,
                "parse_mode": "HTML",
                "reply_markup": reply_markup,
                "reply_to_message_id": m.id
            }
            await send_telegram_api(c, "sendMessage", payload)
                        
            text = f'{k} من「 {m.from_user.mention()} 」\n'
            usrr = '@' + m.from_user.username if m.from_user.username else 'مافيه'
            text += f'{k} يوزره : {usrr}\n'
            text += f'{k} ايديه : `{m.from_user.id}`\n'
            text += f'\n{k} تم تفعيل البوت بمجموعة جديدة :\n\n'
            text += f'{k} اسم المجموعة : {m.chat.title}\n'
            chatusr = '@' + m.chat.username if m.chat.username else 'مافيه'
            text += f'{k} يوزر المجموعة : {chatusr}\n'
            text += f'{k} ايدي المجموعة : `{m.chat.id}`'
            if await r.smembers(f'enablelist:{Dev_FINAL}'):
                text += f'\n{k} عدد المجموعات الآن : {len(await r.smembers(f"enablelist:{Dev_FINAL}"))}\n'
            text += '\n\n'
            
            dev_buttons = []
            if group_link:
                dev_buttons.append([InlineKeyboardButton(**(await create_button_raw("groups", "group_link", m.chat.title, url=group_link)))])
            leave_btn_raw = await create_button_raw("groups", "leave_btn", "مغادرة", callback_data=f"leave_gp_{m.chat.id}")
            dev_buttons.append([InlineKeyboardButton(**leave_btn_raw)])
            
            dev_reply_markup = InlineKeyboardMarkup(dev_buttons)
            await send_dev_notification(c, text, reply_markup=dev_reply_markup)

    if text == 'تعطيل':
        if not (await m.chat.get_member(m.from_user.id)).status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR] and not await owner_pls(m.from_user.id, m.chat.id):
            return await m.reply(REPLIES['plugins_groups_516'])
        else:
            if not await r.get(f'{m.chat.id}:enable:{Dev_FINAL}'):
                return False
            else:
                await r.set(f'{m.chat.id}:manual_disable:{Dev_FINAL}', 1)
                await r.delete(f'{m.chat.id}:enable:{Dev_FINAL}')
                await r.srem(f'enablelist:{Dev_FINAL}', m.chat.id)
                await m.reply(plugins_groups_524(k, m.from_user.mention(), k))
                
                text = f'{k} من「 {m.from_user.mention()} 」\n'
                usrr = '@' + m.from_user.username if m.from_user.username else 'مافيه'
                text += f'{k} يوزره : {usrr}\n'
                text += f'{k} ايديه : `{m.from_user.id}`\n'
                text += f'\n{k} تم تعطيل البوت بمجموعة جديدة :\n\n'
                text += f'{k} اسم المجموعة : {m.chat.title}\n'
                chatusr = '@' + m.chat.username if m.chat.username else 'مافيه'
                text += f'{k} يوزر المجموعة : {chatusr}\n'
                text += f'{k} ايدي المجموعة : `{m.chat.id}`'
                if await r.smembers(f'enablelist:{Dev_FINAL}'):
                    text += f'\n{k} عدد المجموعات الآن : {len(await r.smembers(f"enablelist:{Dev_FINAL}"))}\n'
                text += '\n\n'
                
                await send_dev_notification(c, text)

    name = await r.get(f'{Dev_FINAL}:BotName') if await r.get(f'{Dev_FINAL}:BotName') else 'فاينل'
    if text == f'{name} غادري' or text == f'{name} غادر':
        if await dev_pls(m.from_user.id, m.chat.id):
            await r.set(f'{m.chat.id}:manual_disable:{Dev_FINAL}', 1)
            await r.delete(f'{m.chat.id}:enable:{Dev_FINAL}')
            await r.srem(f'enablelist:{Dev_FINAL}', m.chat.id)
            
            text = f'{k} من「 {m.from_user.mention()} 」\n'
            usrr = '@' + m.from_user.username if m.from_user.username else 'مافيه'
            text += f'{k} يوزره : {usrr}\n'
            text += f'{k} ايديه : `{m.from_user.id}`\n'
            text += f'\n{k} طلعت من المجموعة بأمر منه :\n\n'
            text += f'{k} اسم المجموعة : {m.chat.title}\n'
            chatusr = '@' + m.chat.username if m.chat.username else 'مافيه'
            text += f'{k} يوزر المجموعة : {chatusr}\n'
            text += f'{k} ايدي المجموعة : `{m.chat.id}`'
            if await r.smembers(f'enablelist:{Dev_FINAL}'):
                text += f'\n{k} عدد المجموعات الآن : {len(await r.smembers(f"enablelist:{Dev_FINAL}"))}\n'
            text += '\n\n'
            
            await c.leave_chat(m.chat.id)
            await send_dev_notification(c, text)
