from helpers.context import get_global_r, get_global_dev, get_global_k
r = get_global_r()
Dev_FINAL = get_global_dev()
k = get_global_k()
import html
import requests
import time
import random
import os
import re
from aiogram.types import FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton, ChatMemberOwner


import pytz
from threading import Thread
from compat import *
from compat import *
from compat import *
from compat import UserNotParticipant, FloodWait
from helpers.ranks import *
from helpers.persian import persianInformation
from helpers.cache import cached_fetch
from .protect import *
from .locks import handle_lock_commands
from .features import handle_feature_toggles
from .media import handle_games_and_media
from .welcome import *
from .buttons import register_buttons, get_button_custom, get_button_color, create_button_raw
from helpers.replies_store import (
    REPLIES,
    plugins_handlers_1068,
    plugins_handlers_1072,
    plugins_handlers_1076,
    plugins_handlers_1078,
    plugins_handlers_1082,
    plugins_handlers_1087,
    plugins_handlers_1089,
    plugins_handlers_1093,
    plugins_handlers_1095,
    plugins_handlers_1099,
    plugins_handlers_1101,
    plugins_handlers_1104,
    plugins_handlers_1106,
    plugins_handlers_1110,
    plugins_handlers_1112,
    plugins_handlers_1116,
    plugins_handlers_1118,
    plugins_handlers_114,
    plugins_handlers_201,
    plugins_handlers_208,
    plugins_handlers_236,
    plugins_handlers_249,
    plugins_handlers_278,
    plugins_handlers_294,
    plugins_handlers_344,
    plugins_handlers_352,
    plugins_handlers_361,
    plugins_handlers_394,
    plugins_handlers_408,
    plugins_handlers_416,
    plugins_handlers_426,
    plugins_handlers_434,
    plugins_handlers_444,
    plugins_handlers_454,
    plugins_handlers_462,
    plugins_handlers_472,
    plugins_handlers_481,
    plugins_handlers_490,
    plugins_handlers_498,
    plugins_handlers_508,
    plugins_handlers_516,
    plugins_handlers_524,
    plugins_handlers_532,
    plugins_handlers_546,
    plugins_handlers_588,
    plugins_handlers_600,
    plugins_handlers_647,
    plugins_handlers_701,
    plugins_handlers_729,
    plugins_handlers_763,
    plugins_handlers_765,
    plugins_handlers_767,
    plugins_handlers_781,
    plugins_handlers_785,
    plugins_handlers_788,
    plugins_handlers_792,
    plugins_handlers_800,
    plugins_handlers_808,
    plugins_handlers_831,
    plugins_handlers_843,
    plugins_handlers_847,
    plugins_handlers_852,
    plugins_handlers_854,
    plugins_handlers_869,
    plugins_handlers_874,
    plugins_handlers_882,
    plugins_handlers_886,
    plugins_handlers_89,
    plugins_handlers_890,
    plugins_handlers_901,
    plugins_handlers_903,
    plugins_handlers_928,
    plugins_handlers_934,
    plugins_handlers_954,
    plugins_handlers_972,
    plugins_handlers_977,
    plugins_handlers_981,
    plugins_handlers_984,
    plugins_handlers_988,
    plugins_handlers_990,
    plugins_handlers_992,
    plugins_handlers_995,
    plugins_handlers_997,
)

BUTTONS_DEFINITIONS = {
    "handlers": {
        "name": "أزرار المعالجات",
        "buttons": [
            {"id": "join_channel", "default": "اضغط هنا"},
            {"id": "report_btn", "default": "⚠️"},
            {"id": "whisper_text", "default": "همسة نصية"},
            {"id": "whisper_media", "default": "همسة وسائط"},
            {"id": "whisper_any", "default": "اهمس لـ"},
            {"id": "pin_confirm", "default": "✅"},
            {"id": "cancel_mention", "default": "ايقاف"},
            {"id": "done_mention", "default": "تم"},
        ]
    }
}

register_buttons(BUTTONS_DEFINITIONS)


@Client.on_message(filters.group, group=-1111111111111)
async def on_zbi(c: Client, m: Message):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()

    # -- تسجيل الأعضاء لاستخدامهم لاحقاً في "@all" --
    # تيليجرام لا يوفر لأي بوت (سواء عبر aiogram أو Pyrogram في وضع Bot Token)
    # ميثود لجلب كامل قائمة أعضاء القروب دفعة واحدة، الوسيلة الوحيدة المتاحة
    # هي بناء القائمة تدريجياً من الرسائل الفعلية التي يرسلها الأعضاء وتخزينها.
    if m.from_user and not m.from_user.is_bot:
        try:
            await r.hset(
                f"{m.chat.id}:GroupMembersData:{Dev_FINAL}",
                str(m.from_user.id),
                m.from_user.first_name or str(m.from_user.id),
            )
        except Exception:
            pass

    name = await r.get(f"{Dev_FINAL}:BotName") if await r.get(f"{Dev_FINAL}:BotName") else "فاينل"
    text = m.text
    if text is not None and text.startswith(f"{name} "):
        text = text.replace(f"{name} ", "")
    if await r.get(f"{m.chat.id}:Custom:{m.chat.id}{Dev_FINAL}&text={text}"):
        text = await r.get(f"{m.chat.id}:Custom:{m.chat.id}{Dev_FINAL}&text={text}")
    if await r.get(f"Custom:{Dev_FINAL}&text={text}"):
        text = await r.get(f"Custom:{Dev_FINAL}&text={text}")

    if await r.get(f"inDontCheck:{Dev_FINAL}"):
        return m.continue_propagation()

    if m.from_user and m.chat and await dev_pls(m.from_user.id, m.chat.id):
        return

    # ملاحظة: منطق الاشتراك الاجباري القديم (العالمي forceChannel:{Dev_FINAL})
    # تمت إزالته بالكامل وإعادة بناؤه في plugins/force_subscribe.py كميزة
    # لكل قروب على حدة (وليس عالمياً لكل بوتات Dev_FINAL). راجع ذلك الملف.
    return m.continue_propagation()


@Client.on_chat_member_updated(filters.group, group=-9999)
async def track_group_members_on_status_change(c: Client, u: ChatMemberUpdated):
    """
    تكملة لنظام رصد الأعضاء الخاص بـ '@all':
    نستخدم حدث ChatMemberUpdated لإضافة العضو فور انضمامه (بدل انتظار أول
    رسالة يرسلها)، وحذفه فوراً عند مغادرته/حظره حتى لا يتم منشنته لاحقاً.
    """
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    try:
        member = u.new_chat_member.user if u.new_chat_member else None
        new_status = u.new_chat_member.status if u.new_chat_member else None
        if not member or member.is_bot:
            return

        active_statuses = {
            ChatMemberStatus.MEMBER,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER,
            ChatMemberStatus.RESTRICTED,
        }
        if new_status in active_statuses:
            await r.hset(
                f"{u.chat.id}:GroupMembersData:{Dev_FINAL}",
                str(member.id),
                member.first_name or str(member.id),
            )
        elif new_status in {ChatMemberStatus.LEFT, ChatMemberStatus.BANNED}:
            await r.hdel(f"{u.chat.id}:GroupMembersData:{Dev_FINAL}", str(member.id))
    except Exception:
        pass


async def get_mentionable_members(c, chat_id):
    """
    يبني قائمة الأعضاء القابلين للمنشن (id + منشن HTML) من قائمة الأعضاء
    المحفوظة دائماً في Redis (مفتاح GroupMembersData)، مع استثناء:
      - المشرفين (يُستثنون دائماً من أي عملية منشن جماعي)
      - البوتات (تُستثنى أصلاً عند التسجيل)
      - أي حساب لم يعد بالإمكان التأكد من وجوده (نتجاهله بصمت عند الخطأ)
    القائمة نفسها لا تُحذف أو تنتهي صلاحيتها؛ تبقى محفوظة للبوت في نفس
    المفتاح إلى الأبد وتُحدَّث تلقائياً من رسائل/انضمام/مغادرة الأعضاء.
    """
    r = get_global_r()
    Dev_FINAL = get_global_dev()

    admin_ids = set()
    try:
        Dev_FINAL_local = get_global_dev()

        async def _fetch_admin_ids():
            admins = await c.get_chat_administrators(chat_id)
            return [adm.user.id for adm in admins if adm.user]

        # قائمة الأدمنية شبه ثابتة (لا تتغيّر مع كل رسالة)، فتُكاش بضع دقائق
        # بدل نداء تيليجرام (get_chat_administrators) في كل مرة يُستخدم فيها
        # المنشن الجماعي بنفس المجموعة.
        cached_ids = await cached_fetch(
            key=f"{chat_id}:mentionAdminIds:{Dev_FINAL_local}",
            fetch=_fetch_admin_ids,
            ttl=120,
        )
        admin_ids = set(cached_ids or [])
    except Exception:
        pass

    result = []
    try:
        members_data = await r.hgetall(f"{chat_id}:GroupMembersData:{Dev_FINAL}")
        for uid_str, uname in members_data.items():
            uid = int(uid_str)
            if uid in admin_ids:
                continue
            mention = f'<a href="tg://user?id={uid}">{html.escape(str(uname))}</a>'
            result.append((uid, mention))
    except Exception:
        pass
    return result


async def run_multi_mention(c, m):
    """
    كل استدعاء لهذا الأمر = منشن واحد فقط:
      - كلمة عشوائية من قائمة الجمل المعيّنة (اضف منشن متعدد).
      - العضو التالي في القائمة عبر مؤشر دوّار (round-robin) محفوظ في
        Redis؛ عند الوصول لآخر عضو يرجع تلقائياً للعضو الأول ويكمل من جديد.
    لا يوجد قفل تشغيل ولا رسائل بدء/إشغال — كل رسالة "منشن" منفصلة ومستقلة.
    """
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if not await mod_pls(m.from_user.id, m.chat.id):
        return await m.reply(plugins_handlers_882(k))
    if await r.get(f"{m.chat.id}:disableALL:{Dev_FINAL}"):
        return await m.reply(REPLIES['plugins_handlers_794'])

    group_data = get_group_data(m.chat.id)
    mention_messages = group_data.get('multi_mention_messages', [])
    if not mention_messages:
        return await m.reply(plugins_handlers_890(k))

    members = await get_mentionable_members(c, m.chat.id)
    if not members:
        return await m.reply(plugins_handlers_901(k))

    # ترتيب ثابت (حسب الـ id) حتى يكون الدوران منطقياً ومتسلسلاً بين الاستدعاءات
    members.sort(key=lambda x: x[0])

    cursor = await r.incr(f"{m.chat.id}:MultiMentionCursor:{Dev_FINAL}")
    index = (cursor - 1) % len(members)
    _uid, mention = members[index]

    word = random.choice(mention_messages)
    final_message = f"{word} {mention}"
    await c.send_message(m.chat.id, final_message, parse_mode="HTML")



async def restrict_user(c, chat_id, user_id):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    try:
        await c.restrict_chat_member(
            chat_id,
            user_id,
            ChatPermissions(
                can_send_messages=False,
                can_send_media_messages=False,
                can_send_other_messages=False,
                can_send_polls=False,
                can_add_web_page_previews=False,
                can_invite_users=False,
                can_change_info=False,
                can_pin_messages=False
            )
        )
        await r.sadd(f"{chat_id}:listRESTRICTED:{Dev_FINAL}", user_id)
        return True
    except:
        return False

@Client.on_message(filters.group, group=27)
async def guardLocksResponse(c, m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    k = await r.get(f"{Dev_FINAL}:botkey")
    channel = (
        await r.get(f"{Dev_FINAL}:BotChannel") if await r.get(f"{Dev_FINAL}:BotChannel") else ''
    )
    await guardResponseFunction(c, m, k, channel)

@Client.on_edited_message(filters.group, group=27)
async def guardLocksResponse2(c, m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    k = await r.get(f"{Dev_FINAL}:botkey")
    channel = (
        await r.get(f"{Dev_FINAL}:BotChannel") if await r.get(f"{Dev_FINAL}:BotChannel") else ''
    )
    await guardResponseFunction2(c, m, k, channel)

async def guardResponseFunction2(c, m, k, channel):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if not await r.get(f"{m.chat.id}:enable:{Dev_FINAL}"):
        return
    warner = """
「 {} 」
{} ممنوع {}

"""
    warn = False
    reason = False

    if m.sender_chat:
        id = m.sender_chat.id
        mention = f'<a href="tg://user?id={id}">{html.escape(str(m.sender_chat.title))}</a>'
    if m.from_user:
        id = m.from_user.id
        mention = m.from_user.mention()

    if await r.get(f"{m.chat.id}:lockEdit:{Dev_FINAL}") and m.text and not await pre_pls(id, m.chat.id):
        await m.delete()
        warn = True
        reason = "التعديل"
        if await r.get(f"{m.chat.id}:BotNotifications:{Dev_FINAL}"):
            await m.reply(plugins_handlers_201(mention, k, reason), disable_web_page_preview=True)

    if await r.get(f"{m.chat.id}:lockEditM:{Dev_FINAL}") and m.media and not await pre_pls(id, m.chat.id):
        await m.delete()
        warn = True
        reason = "تعديل الميديا"
        if await r.get(f"{m.chat.id}:BotNotifications:{Dev_FINAL}"):
            await m.reply(plugins_handlers_208(mention, k, reason), disable_web_page_preview=True)

async def guardResponseFunction(c, m, k, channel):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if not await r.get(f"{m.chat.id}:enable:{Dev_FINAL}"):
        return
    warner = """
「 {} 」
{} ممنوع {}

"""
    warn = False
    reason = False
    
    id = None
    mention = None

    if await r.get(f"{m.chat.id}:lockNot:{Dev_FINAL}") and m.service:
        await m.delete()

    if await r.get(f"{m.chat.id}:lockText:{Dev_FINAL}") and (m.text or m.caption):
        if m.from_user and not await pre_pls(m.from_user.id, m.chat.id):
            await m.delete()
            reason = "تكتب"
            if await r.get(f"{m.chat.id}:BotNotifications:{Dev_FINAL}"):
                mention = m.from_user.mention()
                await m.reply(plugins_handlers_236(mention, k, reason), disable_web_page_preview=True)
        return False

    if await r.get(f"{m.chat.id}:lockaddContacts:{Dev_FINAL}") and m.from_user and m.new_chat_members:
        if await pre_pls(m.from_user.id, m.chat.id):
            return
        for me in m.new_chat_members:
            if not me.id == m.from_user.id:
                mention = m.from_user.mention()
                await m.chat.ban_member(me.id)
                reason = "تضيف حد هنا"
                await m.delete()
                if await r.get(f"{m.chat.id}:BotNotifications:{Dev_FINAL}"):
                    await m.reply(plugins_handlers_249(mention, k, reason), disable_web_page_preview=True)

    if m.sender_chat:
        id = m.sender_chat.id
        mention = f'<a href="tg://user?id={id}">{html.escape(str(m.sender_chat.title))}</a>'
    elif m.from_user:
        id = m.from_user.id
        mention = m.from_user.mention()
    else:
        return False

    if c.me and id == c.me.id:
        return False

    if m.from_user and m.from_user.id == 5434703779:
        return False

    if m.from_user and await dev_pls(m.from_user.id, m.chat.id):
        return False

    if m.from_user and await r.get(f"{m.from_user.id}:mute:Global{Dev_FINAL}"):
        custom_name = await r.get(f"{Dev_FINAL}:BotName") or "فاينل"
        real_name = c.me.first_name if c.me else custom_name
        user_fullname = f"{str(m.from_user.first_name)} {str(m.from_user.last_name or '')}"
        is_impersonator = custom_name in user_fullname or (real_name and real_name in user_fullname)
        if not is_impersonator:
            await r.delete(f"{m.from_user.id}:mute:Global{Dev_FINAL}")
            await r.delete(f"{m.from_user.id}:fake_muted:Global{Dev_FINAL}")
            if await r.get(f"{m.chat.id}:BotNotifications:{Dev_FINAL}"):
                await m.reply(plugins_handlers_278(k, mention, k))
            return True
        else:
            await m.delete()
            return False

    if m.from_user and await r.get(f"lockFakeName:Global:{Dev_FINAL}"):
        custom_name = await r.get(f"{Dev_FINAL}:BotName") or "فاينل"
        real_name = c.me.first_name if c.me else custom_name
        user_fullname = f"{str(m.from_user.first_name)} {str(m.from_user.last_name or '')}"
        is_impersonator = custom_name in user_fullname or (real_name and real_name in user_fullname)
        if is_impersonator:
            await r.set(f"{m.from_user.id}:mute:Global{Dev_FINAL}", 1)
            await r.set(f"{m.from_user.id}:fake_muted:Global{Dev_FINAL}", 1)
            await m.delete()
            if await r.get(f"{m.chat.id}:BotNotifications:{Dev_FINAL}"):
                await m.reply(plugins_handlers_294(k, mention, k, k))
            return False

    if await pre_pls(id, m.chat.id):
        return False

    if m.media:
        rep = m
        file_id = None
        if rep.sticker:
            file_id = rep.sticker.file_id
        if rep.animation:
            file_id = rep.animation.file_id
        if rep.photo:
            file_id = rep.photo.file_id
        if rep.video:
            file_id = rep.video.file_id
        if rep.voice:
            file_id = rep.voice.file_id
        if rep.audio:
            file_id = rep.audio.file_id
        if rep.document:
            file_id = rep.document.file_id
        if file_id:
            idd = file_id[-6:]
            if await r.get(f"{idd}:NotAllow:{m.chat.id}{Dev_FINAL}"):
                if not await admin_pls(id, m.chat.id):
                    await m.delete()
                    return False

    if m.text and await r.smembers(f"{m.chat.id}:NotAllowedListText:{Dev_FINAL}"):
        if not await admin_pls(id, m.chat.id):
            for word in await r.smembers(f"{m.chat.id}:NotAllowedListText:{Dev_FINAL}"):
                if word in m.text:
                    await m.delete()
                    return False

    if await r.get(f"{id}:mute:{m.chat.id}{Dev_FINAL}") or await r.get(f"{id}:mute:{Dev_FINAL}"):
        return False

    if await r.get(f"{m.chat.id}:mute:{Dev_FINAL}"):
        if not await admin_pls(id, m.chat.id):
            await m.delete()
            return False

    if await r.get(f"{m.chat.id}:lockQuote:{Dev_FINAL}") and (m.quote or getattr(m, "reply_to_story", None)):
        if m.from_user and not await admin_pls(m.from_user.id, m.chat.id):
            await m.delete()
            reason = "ترسل اقتباس"
            if await r.get(f"{m.chat.id}:BotNotifications:{Dev_FINAL}"):
                await m.reply(plugins_handlers_344(mention, k, reason), disable_web_page_preview=True)
        return False

    if await r.get(f"{m.chat.id}:lockDash:{Dev_FINAL}") and m.text and "-" in m.text:
        if m.from_user and not await admin_pls(m.from_user.id, m.chat.id):
            await m.delete()
            reason = "ترسل شارحه"
            if await r.get(f"{m.chat.id}:BotNotifications:{Dev_FINAL}"):
                await m.reply(plugins_handlers_352(mention, k, reason), disable_web_page_preview=True)
        return False

    if await r.get(f"{m.chat.id}:lockPremiumEmoji:{Dev_FINAL}") and m.entities:
        if any(entity.type == MessageEntityType.CUSTOM_EMOJI for entity in m.entities):
            if m.from_user and not await admin_pls(m.from_user.id, m.chat.id):
                await m.delete()
                reason = "ترسل ايموجيات مميزة"
                if await r.get(f"{m.chat.id}:BotNotifications:{Dev_FINAL}"):
                    await m.reply(plugins_handlers_361(mention, k, reason), disable_web_page_preview=True)
            return False

    if await r.get(f"{m.chat.id}:lockBots:{Dev_FINAL}") and m.new_chat_members:
        if m.from_user and not await admin_pls(m.from_user.id, m.chat.id):
            for mem in m.new_chat_members:
                if mem.is_bot:
                    await m.chat.ban_member(mem.id)

    if await r.get(f"{m.chat.id}:lockJoin:{Dev_FINAL}") and m.new_chat_members:
        for mem in m.new_chat_members:
            if not await admin_pls(mem.id, m.chat.id):
                await m.chat.ban_member(mem.id)
                await m.chat.unban_member(mem.id)
                if await r.get(f"{m.chat.id}:lockJoinRestrict:{Dev_FINAL}"):
                    if m.from_user and not await admin_pls(m.from_user.id, m.chat.id):
                        await restrict_user(c, m.chat.id, m.from_user.id)
                return False

    if await r.get(f"{m.chat.id}:lockChannels:{Dev_FINAL}") and m.sender_chat:
        if not m.sender_chat.id == m.chat.id:
            await m.chat.ban_member(m.sender_chat.id)
            return False

    if await r.get(f"{m.chat.id}:lockSpam:{Dev_FINAL}"):
        if not await r.get(f"{id}in_spam:{m.chat.id}{Dev_FINAL}"):
            await r.set(f"{id}in_spam:{m.chat.id}{Dev_FINAL}", 1, ex=10)
        else:
            if int((await r.get(f"{id}in_spam:{m.chat.id}{Dev_FINAL}")) or 0) == 10:
                if m.from_user and not await admin_pls(m.from_user.id, m.chat.id):
                    await r.delete(f"{id}in_spam:{m.chat.id}{Dev_FINAL}")
                    await m.delete()
                    if await r.get(f"{m.chat.id}:BotNotifications:{Dev_FINAL}"):
                        await m.reply(plugins_handlers_394(mention, k))
                    return False
                if m.sender_chat:
                    await m.chat.ban_member(m.sender_chat)
                    return False
            else:
                get = int((await r.get(f"{id}in_spam:{m.chat.id}{Dev_FINAL}")) or 0)
                await r.set(f"{id}in_spam:{m.chat.id}{Dev_FINAL}", get + 1, ex=10)

    if await r.get(f"{m.chat.id}:lockInline:{Dev_FINAL}") and m.via_bot:
        if m.from_user and not await admin_pls(m.from_user.id, m.chat.id):
            await m.delete()
            reason = "ترسل انلاين"
            if await r.get(f"{m.chat.id}:BotNotifications:{Dev_FINAL}"):
                await m.reply(plugins_handlers_408(mention, k, reason), disable_web_page_preview=True)
        return False

    if await r.get(f"{m.chat.id}:lockForward:{Dev_FINAL}") and m.forward_date:
        if m.from_user and not await admin_pls(m.from_user.id, m.chat.id):
            await m.delete()
            reason = "ترسل توجيه"
            if await r.get(f"{m.chat.id}:BotNotifications:{Dev_FINAL}"):
                await m.reply(plugins_handlers_416(mention, k, reason), disable_web_page_preview=True)
            if await r.get(f"{m.chat.id}:lockForwardRestrict:{Dev_FINAL}"):
                await restrict_user(c, m.chat.id, m.from_user.id)
        return False

    if await r.get(f"{m.chat.id}:lockAudios:{Dev_FINAL}") and m.audio:
        if m.from_user and not await admin_pls(m.from_user.id, m.chat.id):
            await m.delete()
            reason = "ترسل صوت"
            if await r.get(f"{m.chat.id}:BotNotifications:{Dev_FINAL}"):
                await m.reply(plugins_handlers_426(mention, k, reason), disable_web_page_preview=True)
        return False

    if await r.get(f"{m.chat.id}:lockVideo:{Dev_FINAL}") and m.video:
        if m.from_user and not await admin_pls(m.from_user.id, m.chat.id):
            await m.delete()
            reason = "ترسل فيديوهات"
            if await r.get(f"{m.chat.id}:BotNotifications:{Dev_FINAL}"):
                await m.reply(plugins_handlers_434(mention, k, reason), disable_web_page_preview=True)
            if await r.get(f"{m.chat.id}:lockVideoRestrict:{Dev_FINAL}"):
                await restrict_user(c, m.chat.id, m.from_user.id)
        return False
    
    if await r.get(f"{m.chat.id}:lockPhoto:{Dev_FINAL}") and m.photo:
        if m.from_user and not await admin_pls(m.from_user.id, m.chat.id):
            await m.delete()
            reason = "ترسل صور"
            if await r.get(f"{m.chat.id}:BotNotifications:{Dev_FINAL}"):
                await m.reply(plugins_handlers_444(mention, k, reason), disable_web_page_preview=True)
            if await r.get(f"{m.chat.id}:lockPhotoRestrict:{Dev_FINAL}"):
                await restrict_user(c, m.chat.id, m.from_user.id)
        return False

    if await r.get(f"{m.chat.id}:lockStickers:{Dev_FINAL}") and m.sticker:
        if m.from_user and not await admin_pls(m.from_user.id, m.chat.id):
            await m.delete()
            reason = "ترسل ملصقات"
            if await r.get(f"{m.chat.id}:BotNotifications:{Dev_FINAL}"):
                await m.reply(plugins_handlers_454(mention, k, reason), disable_web_page_preview=True)
        return False

    if await r.get(f"{m.chat.id}:lockAnimations:{Dev_FINAL}") and m.animation:
        if m.from_user and not await admin_pls(m.from_user.id, m.chat.id):
            await m.delete()
            reason = "ترسل متحركات"
            if await r.get(f"{m.chat.id}:BotNotifications:{Dev_FINAL}"):
                await m.reply(plugins_handlers_462(mention, k, reason), disable_web_page_preview=True)
            if await r.get(f"{m.chat.id}:lockAnimationsRestrict:{Dev_FINAL}"):
                await restrict_user(c, m.chat.id, m.from_user.id)
        return False

    if await r.get(f"{m.chat.id}:lockFiles:{Dev_FINAL}") and m.document:
        if m.from_user and not await admin_pls(m.from_user.id, m.chat.id):
            await m.delete()
            reason = "ترسل ملفات"
            if await r.get(f"{m.chat.id}:BotNotifications:{Dev_FINAL}"):
                await m.reply(plugins_handlers_472(mention, k, reason), disable_web_page_preview=True)
        return False

    if await r.get(f"{m.chat.id}:lockPersian:{Dev_FINAL}") and m.text:
        if "ه‍" in m.text or "ی" in m.text or "ک" in m.text or "چ" in m.text:
            if m.from_user and not await admin_pls(m.from_user.id, m.chat.id):
                await m.delete()
                reason = "ترسل فارسي"
                if await r.get(f"{m.chat.id}:BotNotifications:{Dev_FINAL}"):
                    await m.reply(plugins_handlers_481(mention, k, reason), disable_web_page_preview=True)
            return False

    if await r.get(f"{m.chat.id}:lockPersian:{Dev_FINAL}") and m.caption:
        if "ه‍" in m.caption or "ی" in m.caption or "ک" in m.caption or "چ" in m.caption:
            if m.from_user and not await admin_pls(m.from_user.id, m.chat.id):
                await m.delete()
                reason = "ترسل فارسي"
                if await r.get(f"{m.chat.id}:BotNotifications:{Dev_FINAL}"):
                    await m.reply(plugins_handlers_490(mention, k, reason), disable_web_page_preview=True)
            return False

    if await r.get(f"{m.chat.id}:lockUrls:{Dev_FINAL}") and m.text and len(Find(m.html)) > 0:
        if m.from_user and not await admin_pls(m.from_user.id, m.chat.id):
            await m.delete()
            reason = "ترسل روابط"
            if await r.get(f"{m.chat.id}:BotNotifications:{Dev_FINAL}"):
                await m.reply(plugins_handlers_498(mention, k, reason), disable_web_page_preview=True)
            if await r.get(f"{m.chat.id}:lockUrlsRestrict:{Dev_FINAL}"):
                await restrict_user(c, m.chat.id, m.from_user.id)
        return False

    if await r.get(f"{m.chat.id}:lockHashtags:{Dev_FINAL}") and m.text and len(re.findall(r"#(\w+)", m.text)) > 0:
        if m.from_user and not await admin_pls(m.from_user.id, m.chat.id):
            await m.delete()
            reason = "ترسل هاشتاق"
            if await r.get(f"{m.chat.id}:BotNotifications:{Dev_FINAL}"):
                await m.reply(plugins_handlers_508(mention, k, reason), disable_web_page_preview=True)
        return False

    if await r.get(f"{m.chat.id}:lockMessages:{Dev_FINAL}") and m.text and len(m.text) > 150:
        if m.from_user and not await admin_pls(m.from_user.id, m.chat.id):
            await m.delete()
            reason = "ترسل كلام كثير"
            if await r.get(f"{m.chat.id}:BotNotifications:{Dev_FINAL}"):
                await m.reply(plugins_handlers_516(mention, k, reason), disable_web_page_preview=True)
        return False

    if await r.get(f"{m.chat.id}:lockVoice:{Dev_FINAL}") and m.voice:
        if m.from_user and not await admin_pls(m.from_user.id, m.chat.id):
            await m.delete()
            reason = "ترسل فويس"
            if await r.get(f"{m.chat.id}:BotNotifications:{Dev_FINAL}"):
                await m.reply(plugins_handlers_524(mention, k, reason), disable_web_page_preview=True)
        return False

    if await r.get(f"{m.chat.id}:lockTags:{Dev_FINAL}") and '"type": "MessageEntityType.MENTION"' in str(m):
        if m.from_user and not await admin_pls(m.from_user.id, m.chat.id):
            await m.delete()
            reason = "ترسل منشنات"
            if await r.get(f"{m.chat.id}:BotNotifications:{Dev_FINAL}"):
                await m.reply(plugins_handlers_532(mention, k, reason), disable_web_page_preview=True)
        return False

    if await r.get(f"{m.chat.id}:lockSHTM:{Dev_FINAL}") and (m.caption or m.text):
        if m.caption:
            txt = m.caption
        if m.text:
            txt = m.text
        for a in list_UwU:
            if txt == a or f" {a} " in txt or a in txt:
                if m.from_user and not await admin_pls(m.from_user.id, m.chat.id):
                    await m.delete()
                    reason = "السب هنا"
                    if await r.get(f"{m.chat.id}:BotNotifications:{Dev_FINAL}"):
                        await m.reply(plugins_handlers_546(mention, k, reason), disable_web_page_preview=True)
                return False

    if await r.get(f"{m.chat.id}:lockJoinPersian:{Dev_FINAL}") and m.new_chat_members:
        if m.from_user.first_name:
            if (
                m.from_user.first_name in persianInformation["names"]
                or m.from_user.id in persianInformation["ids"]
                or "ه‍" in m.from_user.first_name
                or "ی" in m.from_user.first_name
                or "ک" in m.from_user.first_name
                or "چ" in m.from_user.first_name
                or "👙" in m.from_user.first_name
                and not await admin_pls(m.from_user.id, m.chat.id)
            ):
                if await r.get(f"{m.chat.id}:BotNotifications:{Dev_FINAL}"):
                    await m.reply(plugins_handlers_647(m.from_user.mention(), k))
                await c.ban_chat_member(m.chat.id, m.from_user.id)
                return True

        if m.from_user.last_name:
            if (
                m.from_user.last_name in persianInformation["last_names"]
                or m.from_user.id in persianInformation["ids"]
                or "ه‍" in m.from_user.last_name
                or "ی" in m.from_user.last_name
                or "ک" in m.from_user.last_name
                or "چ" in m.from_user.last_name
                or "👙" in m.from_user.last_name
                and not await admin_pls(m.from_user.id, m.chat.id)
            ):
                if await r.get(f"{m.chat.id}:BotNotifications:{Dev_FINAL}"):
                    await m.reply(plugins_handlers_647(m.from_user.mention(), k))
                await c.ban_chat_member(m.chat.id, m.from_user.id)
                return True

    if await r.get(f"{m.chat.id}:lockGamthon:{Dev_FINAL}") and m.text:
        if m.text.startswith("."):
            if m.from_user and not await admin_pls(m.from_user.id, m.chat.id):
                await m.delete()
                reason = "تستخدم جمثون"
                if await r.get(f"{m.chat.id}:BotNotifications:{Dev_FINAL}"):
                    await m.reply(plugins_handlers_588(mention, k, reason), disable_web_page_preview=True)
                await restrict_user(c, m.chat.id, m.from_user.id)
            return False

    if await r.get(f"{m.chat.id}:enableVerify:{Dev_FINAL}") and m.new_chat_members:
        for me in m.new_chat_members:
            if not await admin_pls(me.id, m.chat.id):
                await c.restrict_chat_member(m.chat.id, me.id, ChatPermissions(can_send_messages=False))
                get_random = get_for_verify(me)
                question = get_random["question"]
                reply_markup = get_random["key"]
                if await r.get(f"{m.chat.id}:BotNotifications:{Dev_FINAL}"):
                    return await m.reply(plugins_handlers_600(k, question), reply_markup=reply_markup)
                else:
                    return await m.reply(question, reply_markup=reply_markup)

    if m.media and await r.get(f"{m.chat.id}:lockNSFW:{Dev_FINAL}"):
        if not await admin_pls(id, m.chat.id):
            if m.sticker:
                id = m.sticker.thumbs[0].file_id
            if m.photo:
                id = m.photo.file_id
            if m.video:
                id = m.video.thumbs[0].file_id
            if m.animation:
                id = m.animation.thumbs[0].file_id
            file = await c.download_media(id)
            await scanR(c, m, id, file)

@Client.on_chat_join_request(filters.group, group=100)
async def antiPersian(c, m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if await r.get(f"{m.chat.id}:lockJoinPersian:{Dev_FINAL}"):
        k = await r.get(f"{Dev_FINAL}:botkey")
        if not await admin_pls(m.from_user.id, m.chat.id):
            if m.from_user.first_name:
                if (
                    m.from_user.first_name in persianInformation["names"]
                    or m.from_user.id in persianInformation["ids"]
                    or "ه‍" in m.from_user.first_name
                    or "ی" in m.from_user.first_name
                    or "ک" in m.from_user.first_name
                    or "چ" in m.from_user.first_name
                    or "👙" in m.from_user.first_name
                ):
                    await c.decline_chat_join_request(m.chat.id, m.from_user.id)
                    if await r.get(f"{m.chat.id}:BotNotifications:{Dev_FINAL}"):
                        await c.send_message(m.chat.id, """「 {} 」\n{} تم رفض طلب انضمامه لاشتباهه ببوت إيراني\n""".format(m.from_user.mention(), k))
                    return True
            if m.from_user.last_name:
                if (
                    m.from_user.last_name in persianInformation["last_names"]
                    or m.from_user.id in persianInformation["ids"]
                    or "ه‍" in m.from_user.last_name
                    or "ی" in m.from_user.last_name
                    or "ک" in m.from_user.last_name
                    or "چ" in m.from_user.last_name
                    or "👙" in m.from_user.last_name
                ):
                    await c.decline_chat_join_request(m.chat.id, m.from_user.id)
                    if await r.get(f"{m.chat.id}:BotNotifications:{Dev_FINAL}"):
                        await c.send_message(m.chat.id, """「 {} 」\n{} تم رفض طلب انضمامه لاشتباهه ببوت إيراني\n""".format(m.from_user.mention(), k))
                    return True

@Client.on_message(filters.group & filters.text, group=28)
async def guardCommandsHandler(c, m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if not await check_global_restrictions(c, m, k):
        return
    k = await r.get(f"{Dev_FINAL}:botkey")
    channel = (
        await r.get(f"{Dev_FINAL}:BotChannel") if await r.get(f"{Dev_FINAL}:BotChannel") else ''
    )
    await guardCommands(c, m, k, channel)

async def guardCommands(c, m, k, channel):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if not await r.get(f"{m.chat.id}:enable:{Dev_FINAL}"):
        return False
    
    if await r.get(f"{m.chat.id}:mute:{Dev_FINAL}") or await r.get(f"{m.chat.id}:lockText:{Dev_FINAL}"):
        if not await pre_pls(m.from_user.id, m.chat.id):
            await m.delete()
            return False
    
    if await r.get(f"{m.from_user.id}:mute:{m.chat.id}{Dev_FINAL}"):
        return False
    if await r.get(f"{m.from_user.id}:mute:{Dev_FINAL}"):
        return False
    if await r.get(f"{m.chat.id}:addCustom:{m.from_user.id}{Dev_FINAL}"):
        return False
    if await r.get(f"{m.chat.id}addCustomG:{m.from_user.id}{Dev_FINAL}"):
        return False
    if await r.get(f"{m.chat.id}:delCustom:{m.from_user.id}{Dev_FINAL}") or await r.get(f"{m.chat.id}:delCustomG:{m.from_user.id}{Dev_FINAL}"):
        return False
    text = m.text
    name = await r.get(f"{Dev_FINAL}:BotName") if await r.get(f"{Dev_FINAL}:BotName") else "فاينل"
    if text.startswith(f"{name} "):
        text = text.replace(f"{name} ", "")
    if await r.get(f"{m.chat.id}:Custom:{m.chat.id}{Dev_FINAL}&text={text}"):
        text = await r.get(f"{m.chat.id}:Custom:{m.chat.id}{Dev_FINAL}&text={text}")
    if await r.get(f"Custom:{Dev_FINAL}&text={text}"):
        text = await r.get(f"Custom:{Dev_FINAL}&text={text}")

    if await check_and_guard_locked_command(c, m, k, text):
        return False

    if await r.get(f"{m.chat.id}:waiting_report_group:{m.from_user.id}"):
        await r.delete(f"{m.chat.id}:waiting_report_group:{m.from_user.id}")
        target_group_input = text.strip()
        try:
            target_chat = await c.get_chat(target_group_input)
            report_group_id = target_chat.id
            report_group_title = target_chat.title
            current_chat_title = m.chat.title or "المجموعة"
            await r.set(f"{m.chat.id}:linked_report_group", report_group_id)
            await r.set(f"{report_group_id}:linked_origin_group", m.chat.id)
            
            resp_text = f"{k} تم ربط قروب المشرفين للمساعدة بنجاح\n{k} قروب المشرفين ↤︎ {report_group_title}\n{k}قروب الاعضاء ↤︎ {current_chat_title}\n_"
            return await m.reply(resp_text)
        except Exception:
            return await m.reply("عذراً، لم أستطيع العثور على المجموعة.")

    if text == "اوامر الربط":
        if not await gowner_pls(m.from_user.id, m.chat.id):
            return await m.reply("• عذراً الامر لـ 「 المالك الاساسي 」 فقط")
        await r.set(f"{m.chat.id}:waiting_report_group:{m.from_user.id}", 1, ex=300)
        return await m.reply("• حسناً عزيزي ارسل ايدي او يوزر قروب المشرفين\n_")

    if text == "الساعه" or text == "الساعة" or text == "الوقت":
        TIME_ZONE = "Asia/Riyadh"
        ZONE = pytz.timezone(TIME_ZONE)
        TIME = datetime.now(ZONE)
        clock = TIME.strftime("%I:%M %p")
        return await m.reply(plugins_handlers_701(k, clock))

    if text == "القوانين":
        if await r.get(f"{m.chat.id}:CustomRules:{Dev_FINAL}"):
            rules = await r.get(f"{m.chat.id}:CustomRules:{Dev_FINAL}")
        else:
            rules = f"""{k} ممنوع نشر الروابط\n{k} ممنوع التكلم او نشر صور اباحيه\n{k} ممنوع اعاده توجيه\n{k} ممنوع العنصرية بكل انواعها\n{k} الرجاء احترام المدراء والادمنيه"""
        return await m.reply(rules, disable_web_page_preview=True)

    if text == "التاريخ":
        b = Hijri.today().isoformat()
        a = b.split("-")
        year = int(a[0])
        month = int(a[1])
        day = int(a[2])
        hijri = Hijri(year, month, day)
        hijri_date = str(b).replace("-", "/")
        hijri_month = hijri.month_name("ar")

        b = Gregorian.today().isoformat()
        a = b.split("-")
        year = int(a[0])
        month = int(a[1])
        day = int(a[2])
        geo = Gregorian(year, month, day)
        geo_date = str(b).replace("-", "/")
        geo_month = geo.month_name("en")[:3]

        return await m.reply(plugins_handlers_729(k, hijri_date, hijri_month, k, geo_date, geo_month))


    if text == "اطردني":
        if await r.get(f"{m.chat.id}:enableKickMe:{Dev_FINAL}"):
            # التحقق مما إذا كان العضو يمتلك رتبة أدمن أو أعلى
            if await admin_pls(m.from_user.id, m.chat.id):
                user_rank = await get_rank(m.from_user.id, m.chat.id)
                return await m.reply(f"{k} ياليت اقدر اطردك والله بس رتبتك {user_rank}")
            else:
                await m.reply(plugins_handlers_767())
                try:
                    # الطرد وإلغاء الحظر باستخدام m.bot لتفادي مشاكل CompatChat
                    await m.bot.ban_chat_member(chat_id=m.chat.id, user_id=m.from_user.id)
                    await asyncio.sleep(0.5)
                    await m.bot.unban_chat_member(chat_id=m.chat.id, user_id=m.from_user.id)
                except Exception as e:
                    print(f"Failed to kick user: {e}")
                    return False

                try:
                    chat_info = await m.bot.get_chat(m.chat.id)
                    link = chat_info.invite_link
                    if link:
                        await m.bot.send_message(m.from_user.id, f"{k} حبيبي النفسية رابط القروب الي طردتك منه: {link}")
                except Exception as e:
                    print(f"Failed to send invite link: {e}")

                return False



    if text == "الرابط":
        if not await r.get(f"{m.chat.id}:disableLINK:{Dev_FINAL}"):
            try:
                link = (await c.get_chat(m.chat.id)).invite_link
                chat_title = m.chat.title or "المجموعة"
                
                link_button = InlineKeyboardButton(text=chat_title, url=link)
                reply_markup = InlineKeyboardMarkup([[link_button]])
                chat_mention = f'<a href="{link}">{chat_title}</a>'
                caption = f"""{chat_mention} \n\n_"""
                
                await m.reply(
                    caption,
                    reply_markup=reply_markup,
                    disable_web_page_preview=False,
                    parse_mode="HTML"
                )
            except Exception as e:
                await m.reply(f"حدث خطأ: {str(e)}")

    if text == "انشاء رابط":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_handlers_785(k))
        link = (await c.get_chat(m.chat.id)).invite_link
        await c.revoke_chat_invite_link(m.chat.id, link)
        return await m.reply(plugins_handlers_788(k))

    if text.startswith("@all"):
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_handlers_792(k))
        if await r.get(f"{m.chat.id}:disableALL:{Dev_FINAL}"):
            return await m.reply(REPLIES['plugins_handlers_794'])
        if await r.get(f"{m.chat.id}:inMention:{Dev_FINAL}"):
            return False
        else:
            if len(text.split()) > 1:
                reason = text.split(None, 1)[1]
            else:
                reason = ""
            await r.set(f"{m.chat.id}:inMention:{Dev_FINAL}", 1)

            members = await get_mentionable_members(c, m.chat.id)
            users_list = [mention for (_uid, mention) in members]

            if not users_list:
                await r.delete(f"{m.chat.id}:inMention:{Dev_FINAL}")
                return await m.reply(plugins_handlers_901(k))

            BATCH_SIZE = 20
            final_list = [users_list[x : x + BATCH_SIZE] for x in range(0, len(users_list), BATCH_SIZE)]
            ftext = f"{reason}\n\n"
            for a in final_list:
                for i in a:
                    if not await r.get(f"{m.chat.id}:inMention:{Dev_FINAL}"):
                        return False
                    ftext += f"{i} , "
                await c.send_message(m.chat.id, ftext, parse_mode="HTML")
                ftext = f"{reason}\n\n"
            await r.delete(f"{m.chat.id}:inMention:{Dev_FINAL}")

    if text.lower() == "/cancel" or text == "ايقاف المنشن":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_handlers_831(k))
        else:
            stopped_anything = False
            if await r.get(f"{m.chat.id}:inMention:{Dev_FINAL}"):
                await r.delete(f"{m.chat.id}:inMention:{Dev_FINAL}")
                stopped_anything = True
            if await r.get(f"{m.chat.id}:inMultiMention:{Dev_FINAL}"):
                await r.delete(f"{m.chat.id}:inMultiMention:{Dev_FINAL}")
                stopped_anything = True
            if stopped_anything:
                return await m.reply(REPLIES['plugins_handlers_841'])
            else:
                return await m.reply(plugins_handlers_843(k))

    if text == "منشن":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_handlers_847(k))
        return await run_multi_mention(c, m)

    if text == 'اضف منشن متعدد':
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_handlers_852(k))
        else:
            await m.reply(plugins_handlers_854(k), parse_mode=ParseMode.MARKDOWN)
            await r.set(f'{m.chat.id}:addingMultiMentionMessages:{m.from_user.id}{Dev_FINAL}', 1)
            return

    if await r.get(f'{m.chat.id}:addingMultiMentionMessages:{m.from_user.id}{Dev_FINAL}'):
        if await dev2_pls(m.from_user.id, m.chat.id):
            done_btn = await create_button_raw("handlers", "done_mention", "تم", callback_data=None)
            if text.lower() == 'تم':
                await r.delete(f'{m.chat.id}:addingMultiMentionMessages:{m.from_user.id}{Dev_FINAL}')
                group_data = get_group_data(m.chat.id)
                if 'multi_mention_messages' not in group_data:
                    group_data['multi_mention_messages'] = []
                temp_messages_key = f'{m.chat.id}:tempMultiMentionMessages:{m.from_user.id}{Dev_FINAL}'
                stored_temp_messages = await r.lrange(temp_messages_key, 0, -1)
                if not stored_temp_messages:
                    return await m.reply(plugins_handlers_869(k))
                decoded_messages = [msg for msg in stored_temp_messages]
                group_data['multi_mention_messages'] = decoded_messages
                save_group_data(m.chat.id, group_data)
                await r.delete(temp_messages_key)
                listed = "\n".join(decoded_messages)
                return await m.reply(f"{plugins_handlers_874(len(decoded_messages))}\n\nعينت:\n{listed}")
            else:
                temp_messages_key = f'{m.chat.id}:tempMultiMentionMessages:{m.from_user.id}{Dev_FINAL}'
                await r.rpush(temp_messages_key, m.html)
                return

    if text == "منشن متعدد":
        return await run_multi_mention(c, m)


    if text == "ابلاغ" and m.reply_to_message:
        # التحقق من حالة البلاغات
        if await r.get(f"{m.chat.id}:disable_reports:{Dev_FINAL}"):
            return await m.reply("• عذراً البلاغات معطله من قبل المالك الاساسي")
        
        target_msg = m.reply_to_message
        target_user = target_msg.from_user
        
        if not target_user:
            return
        if target_user.is_bot:
            return
        if target_user.id == m.from_user.id:
            return
        if await admin_pls(target_user.id, m.chat.id):
            return
    
        linked_group_id = await r.get(f"{m.chat.id}:linked_report_group")
        
        if linked_group_id:
            linked_group_id = int(linked_group_id)
            await m.reply("• شكراً لتعاونك تم رفع بلاغك للمشرفين سيتم الرد قريباً\n_")
            
            reporter_id = m.from_user.id
            current_title = m.chat.title or "المجموعة"
            target_username = f"@{target_user.username}" if target_user.username else target_user.mention()
            target_id = target_user.id
            
            msg_link = target_msg.link if hasattr(target_msg, "link") and target_msg.link else (f"https://t.me/{m.chat.username}/{target_msg.id}" if m.chat.username else "")
            
            notif_text = f"{k} اشعار!\n{k} [{reporter_id} ]\n{k} يحتاج إلى مساعدة المشرفين في مجموعة ”{current_title}”\n\n{k}المستخدم المُبلغ عنه : {target_username}\n{k} [{target_id} ]\n\n{k} إذهب للرسالة <a href='{msg_link}'>هنا</a>"
            
            try:
                await c.send_message(linked_group_id, notif_text, disable_web_page_preview=True)
            except Exception:
                pass
        else:
            reports_count = await r.incr(f"{m.chat.id}:reports_count:{target_user.id}")
            
            owners_lines = []
            idx = 1
            try:
                # جلب المالكين من Redis أولاً
                owners_ids = await r.smembers(f'{m.chat.id}:listGOWNER:{Dev_FINAL}')
                
                if owners_ids:
                    for owner_id in owners_ids:
                        try:
                            owner_id = int(owner_id)
                            try:
                                owner = await c.get_users(owner_id)
                                if owner:
                                    u_str = f"@{owner.username}" if owner.username else owner.mention()
                                    owners_lines.append(f"{idx} - {u_str}")
                                    idx += 1
                            except:
                                owners_lines.append(f"{idx} - [{owner_id}]")
                                idx += 1
                        except:
                            pass
                else:
                    # إذا لم يوجد مالكين في Redis، نستخدم get_chat_administrators كحل احتياطي
                    admins = await c.get_chat_administrators(m.chat.id)
                    async for mm in admins:
                        if mm.status == ChatMemberStatus.OWNER:
                            if mm.user and not mm.user.is_bot and not mm.user.is_deleted:
                                u_str = f"@{mm.user.username}" if mm.user.username else mm.user.mention()
                                owners_lines.append(f"{idx} - {u_str}")
                                idx += 1
            except Exception:
                pass
            
            owners_formatted = "\n".join(owners_lines) if owners_lines else "1 - لا يوجد"
            
            report_text = f"{k} للمالكين الاساسين \n ━━━━━━━━━━━━\n{owners_formatted}\n{k} شخص قام بالابلاغ على رسالة \n{k} عدد بلاغاته : {reports_count}\n_"
            return await m.reply(report_text, reply_to_message_id=m.id)
    
    # أوامر تفعيل وتعطيل البلاغات
    if text == "تعطيل البلاغات":
        if not await gowner_pls(m.from_user.id, m.chat.id):
            return await m.reply("• عذراً الامر لـ 「 المالك الاساسي 」 فقط")
        await r.set(f"{m.chat.id}:disable_reports:{Dev_FINAL}", 1)
        return await m.reply("• ابشر عطلت بلاغات الاعضاء بنجاح .")
    
    if text == "تفعيل البلاغات":
        if not await gowner_pls(m.from_user.id, m.chat.id):
            return await m.reply("• عذراً الامر لـ 「 المالك الاساسي 」 فقط")
        await r.delete(f"{m.chat.id}:disable_reports:{Dev_FINAL}")
        return await m.reply("• ابشر فعلت بلاغات الاعضاء بنجاح .")
    
    
    if text == "تثبيت" and m.reply_to_message:
        if await mod_pls(m.from_user.id, m.chat.id):
            await m.reply_to_message.pin(disable_notification=False)
            await m.reply(plugins_handlers_972(k))

    if text == "الغاء التثبيت" and m.reply_to_message:
        if await mod_pls(m.from_user.id, m.chat.id):
            await m.reply_to_message.unpin()
            await m.reply(plugins_handlers_977(k))

    if text == "مسح قائمة التثبيت":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_handlers_981(k))
        else:
            await c.unpin_all_chat_messages(m.chat.id)
            return await m.reply(plugins_handlers_984(k))

    if text == "دمج ازرار الهمسه":
        if not await dev_pls(m.from_user.id, m.chat.id):
            return await m.reply(f"{k} عذراً الامر لـ 「 Dev🎖 」 فقط")
        if await r.get(f"{Dev_FINAL}:whisper_merged"):
            return await m.reply(f"{k} ازرار الهمسة مدمجة اصلاً")
        await r.set(f"{Dev_FINAL}:whisper_merged", "1")
        return await m.reply(f"{k} ابشر صارو زر واحد للوسائط والنصوص")

    if text == "فصل ازرار الهمسه":
        if not await dev_pls(m.from_user.id, m.chat.id):
            return await m.reply(f"{k} عذراً الامر لـ 「 Dev🎖 」 فقط")
        if not await r.get(f"{Dev_FINAL}:whisper_merged"):
            return await m.reply(f"{k} ازرار الهمسة منفصلة اصلاً")
        await r.delete(f"{Dev_FINAL}:whisper_merged")
        return await m.reply(f"{k} ابشر رجعتهم زرين للوسائط و والنصوص")

    if text == "تفعيل رابط اهمس":
        if not await dev_pls(m.from_user.id, m.chat.id):
            return await m.reply(f"{k} عذراً الامر لـ 「 Dev🎖 」 فقط")
        if await r.get(f"{Dev_FINAL}:whisper_link_mode"):
            return await m.reply(f"{k} رابط اهمس مفعل اصلاً")
        await r.set(f"{Dev_FINAL}:whisper_link_mode", "1")
        return await m.reply(f"{k} تم تفعيل رابط اهمس")

    if text == "تعطيل رابط اهمس":
        if not await dev_pls(m.from_user.id, m.chat.id):
            return await m.reply(f"{k} عذراً الامر لـ 「 Dev🎖 」 فقط")
        if not await r.get(f"{Dev_FINAL}:whisper_link_mode"):
            return await m.reply(f"{k} رابط اهمس معطل اصلاً")
        await r.delete(f"{Dev_FINAL}:whisper_link_mode")
        return await m.reply(f"{k} تم تعطيل رابط اهمس")

    if text in ["اهمس", "همسة", "همسه"] and m.reply_to_message and m.reply_to_message.from_user:
        if await r.get(f"{Dev_FINAL}:whisper_{m.chat.id}") == "off":
            return await m.reply(plugins_handlers_988(k))
        if await r.get(f"{m.from_user.id}:mute:{m.chat.id}{Dev_FINAL}"):
            return await m.reply(plugins_handlers_990(k))
        if await r.get(f"{m.from_user.id}:mute:{Dev_FINAL}"):
            return await m.reply(plugins_handlers_992(k))
        user_id = m.reply_to_message.from_user.id
        if user_id == m.from_user.id:
            return await m.reply(plugins_handlers_995(k))
        if m.reply_to_message.from_user.is_bot:
            return await m.reply(plugins_handlers_997(k))
        import uuid
        key = uuid.uuid4().hex[:10]
        await r.hset(f"{Dev_FINAL}:whisper_pending:{key}", mapping={
            "chat_id": str(m.chat.id),
            "sender_id": str(m.from_user.id),
            "sender_name": m.from_user.first_name,
            "target_id": str(user_id),
            "target_name": m.reply_to_message.from_user.first_name
        })
        await r.expire(f"{Dev_FINAL}:whisper_pending:{key}", 600)
        bot = await c.get_me()
        target_name = m.reply_to_message.from_user.first_name
        mention_html = f'<a href="tg://user?id={user_id}">{html.escape(str(target_name))}</a>'
        msg_text = f"{k}تم تحديد الهمسه لـ ↤︎ {mention_html}\n{k}اضغط الزر لكتابة الهمسة .\n_"

        if await r.get(f"{Dev_FINAL}:whisper_merged"):
            url_any = f"https://t.me/{bot.username}?start=w_{key}_a"
            whisper_any_btn = await create_button_raw("handlers", "whisper_any", f"اهمس لـ {target_name}", url=url_any)
            await c.send_message(
                m.chat.id,
                msg_text,
                parse_mode="HTML",
                reply_to_message_id=m.id,
                reply_markup={
                    "inline_keyboard": [
                        [whisper_any_btn]
                    ]
                },
            )
            return True

        url_text = f"https://t.me/{bot.username}?start=w_{key}_t"
        url_media = f"https://t.me/{bot.username}?start=w_{key}_m"
        whisper_text_btn = await create_button_raw("handlers", "whisper_text", "همسة نصية", url=url_text)
        whisper_media_btn = await create_button_raw("handlers", "whisper_media", "همسة وسائط", url=url_media)
        await c.send_message(
            m.chat.id,
            msg_text,
            parse_mode="HTML",
            reply_to_message_id=m.id,
            reply_markup={
                "inline_keyboard": [
                    [whisper_text_btn],
                    [whisper_media_btn]
                ]
            },
        )
        return True

    if await r.get(f"{m.from_user.id}:promote:{m.chat.id}"):
        if await owner_pls(m.from_user.id, m.chat.id):
            id = int((await r.get(f"{m.from_user.id}:promote:{m.chat.id}")) or 0)
            if text.startswith("*"):
                await r.delete(f"{m.from_user.id}:promote:{m.chat.id}")
                if text.startswith("**"):
                    can_promote_members = True
                    type = 1
                else:
                    can_promote_members = False
                    type = 0
                if len(text.split()) > 1:
                    title = text.split(None, 1)[1][:15:]
                else:
                    title = None
                await c.promote_chat_member(
                    m.chat.id,
                    id,
                    privileges=ChatPrivileges(
                        can_manage_chat=True,
                        can_delete_messages=True,
                        can_manage_video_chats=True,
                        can_restrict_members=True,
                        can_promote_members=can_promote_members,
                        can_change_info=True,
                        can_invite_users=True,
                        can_pin_messages=True,
                    ),
                )
                if title:
                    try:
                        await c.set_administrator_title(m.chat.id, id, title)
                    except:
                        pass
                get = await m.chat.get_member(id)
                if type == 1:
                    await r.set(f"{m.chat.id}:rankADMIN:{get.user.id}{Dev_FINAL}", 1)
                    await r.sadd(f"{m.chat.id}:listADMIN:{Dev_FINAL}", get.user.id)
                    return await m.reply(plugins_handlers_1068(get.user.mention(), k))
                else:
                    await r.set(f"{m.chat.id}:rankADMIN:{get.user.id}{Dev_FINAL}", 1)
                    await r.sadd(f"{m.chat.id}:listADMIN:{Dev_FINAL}", get.user.id)
                    return await m.reply(plugins_handlers_1072(get.user.mention(), k))

    # أوامر "قناة الاشتراك" / "وضع قناة @..." القديمة (عالمية لكل بوتات
    # Dev_FINAL) أُزيلت بالكامل. البديل الجديد هو أوامر "اضف اشتراك @..." و
    # "حذف الاشتراك الاجباري" لكل قروب على حدة — راجع plugins/force_subscribe.py

    if text == "تفعيل اشعارات البوت":
        if not await owner_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_handlers_1093(k))
        await r.set(f"{m.chat.id}:BotNotifications:{Dev_FINAL}", 1)
        return await m.reply(plugins_handlers_1095(k))

    if text == "تعطيل اشعارات البوت":
        if not await owner_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_handlers_1099(k))
        await r.delete(f"{m.chat.id}:BotNotifications:{Dev_FINAL}")
        return await m.reply(plugins_handlers_1101(k))
    # "تعطيل/تفعيل الاشتراك الإجباري" و "حذف قناة الاشتراك" (القديمة، العالمية)
    # أُزيلت أيضاً — الحذف الآن عبر "حذف الاشتراك الاجباري" في force_subscribe.py


    lock_result = await handle_lock_commands(c, m, k, text)
    if lock_result is not None:
        return lock_result

    toggle_result = await handle_feature_toggles(c, m, k, text, channel)
    if toggle_result is not None:
        return toggle_result

    games_result = await handle_games_and_media(c, m, k, text, channel)
    if games_result is not None:
        return games_result
        
    # بعد معالجة الأوامر الأساسية وقبل lock_result
    owner_result = await handle_owner_commands(m, text, r, Dev_FINAL)
    if owner_result is not None:
        return owner_result


async def handle_owner_commands(m, text, r, Dev_FINAL):
    import json
    import asyncio
    import re
    from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ChatMemberOwner

    if await r.get(f"{m.chat.id}:stepSetOwnerUser:{m.from_user.id}{Dev_FINAL}"):
        await r.delete(f"{m.chat.id}:stepSetOwnerUser:{m.from_user.id}{Dev_FINAL}")
        user_input = text.strip()

        target_user = None

        if m.reply_to_message and m.reply_to_message.from_user:
            target_user = m.reply_to_message.from_user

        elif m.entities:
            for entity in m.entities:
                if entity.type == "text_mention" and entity.user:
                    target_user = entity.user
                    break

        if not target_user:
            clean_input = user_input.replace("tg://user?id=", "")
            resolved_id = await resolve_user_id_from_arg(clean_input)
            if resolved_id:
                try:
                    chat_obj = await m.bot.get_chat(resolved_id)
                    if chat_obj:
                        target_user = chat_obj
                except Exception:
                    pass

        if target_user:
            if getattr(target_user, "is_bot", False):
                return await m.reply("• ركز شوي هذا بوت كيف احطه مالك .")

            photo_file_id = None
            try:
                photos = await m.bot.get_user_profile_photos(user_id=target_user.id, limit=1)
                if photos.total_count > 0:
                    photo_file_id = photos.photos[0][-1].file_id
            except Exception:
                pass

            user_bio = getattr(target_user, "bio", "") or ""

            owner_data = {
                "id": target_user.id,
                "username": target_user.username or "",
                "first_name": target_user.first_name or "",
                "last_name": target_user.last_name or "",
                "mention": target_user.html_text if hasattr(target_user, "html_text") else (target_user.first_name or "المالك"),
                "photo": photo_file_id,
                "bio": user_bio
            }

            await r.set(f"{m.chat.id}:customOwnerData:{Dev_FINAL}", json.dumps(owner_data))
            await r.delete(f"{m.chat.id}:customOwnerUser:{Dev_FINAL}")

            cache_key = f"owner_cache_{m.chat.id}_{Dev_FINAL}"
            await r.delete(cache_key)

            return await m.reply("• تم حفظ يوزر المالك بنجاح")
        else:
            return await m.reply(f"ماقدرت القاه ، سورد على رساله منه او ارسل ايديه")

    if await r.get(f"{m.chat.id}:stepSetOwnerButtonText:{m.from_user.id}{Dev_FINAL}"):
        button_text = text.strip()
        await r.delete(f"{m.chat.id}:stepSetOwnerButtonText:{m.from_user.id}{Dev_FINAL}")
        await r.set(f"{m.chat.id}:tempOwnerBtnText:{m.from_user.id}{Dev_FINAL}", button_text)
        await r.set(f"{m.chat.id}:stepSetOwnerButtonUrl:{m.from_user.id}{Dev_FINAL}", "1")
        return await m.reply("• ارسلي رابط قناتك")

    if await r.get(f"{m.chat.id}:stepSetOwnerButtonUrl:{m.from_user.id}{Dev_FINAL}"):
        channel_url = text.strip()
        if not re.match(r'^https?://[^\s]+', channel_url) and not channel_url.startswith("t.me/"):
            return 

        if channel_url.startswith("t.me/"):
            channel_url = f"https://{channel_url}"

        btn_text = await r.get(f"{m.chat.id}:tempOwnerBtnText:{m.from_user.id}{Dev_FINAL}")
        btn_text_str = btn_text.decode('utf-8') if isinstance(btn_text, bytes) else str(btn_text) if btn_text else "قناة المالك"

        await r.delete(f"{m.chat.id}:stepSetOwnerButtonUrl:{m.from_user.id}{Dev_FINAL}")
        await r.delete(f"{m.chat.id}:tempOwnerBtnText:{m.from_user.id}{Dev_FINAL}")

        await r.set(f"{m.chat.id}:ownerChannelText:{Dev_FINAL}", btn_text_str)
        await r.set(f"{m.chat.id}:ownerChannelUrl:{Dev_FINAL}", channel_url)

        reply_msg = (
            "• تم حفظ الزر بنجاح \n"
            "• لتجربتة اكتب ↤︎المالك\n"
            "• لتعديلة اكتب ↤︎اضف زر المالك\n"
            "• لحذفة اكتب ↤︎حذف زر المالك"
        )
        return await m.reply(reply_msg)

    if await r.get(f"{m.chat.id}:stepSetOwnerReply:{m.from_user.id}{Dev_FINAL}"):
        await r.delete(f"{m.chat.id}:stepSetOwnerReply:{m.from_user.id}{Dev_FINAL}")
        await r.set(f"{m.chat.id}:ownerCustomReply:{Dev_FINAL}", text)
        return await m.reply("• تم حفظ رد المالك بنجاح")

    if text in ["تغير يوزر المالك", "تغيير يوزر المالك"]:
        if not await gowner_pls(m.from_user.id, m.chat.id):
            return await m.reply("•  عذراً الامر لـ 「 المالك الاساسي 」 فقط  ")
        await r.set(f"{m.chat.id}:stepSetOwnerUser:{m.from_user.id}{Dev_FINAL}", "1")
        return await m.reply("• ارسل يوزر المالك الان أو قم بالرد على رسالته")

    if text == "مسح يوزر المالك":
        if not await gowner_pls(m.from_user.id, m.chat.id):
            return await m.reply("• عذراً الامر لـ 「 المالك الاساسي 」 فقط")
        await r.delete(
            f"{m.chat.id}:ownerCustomReply:{Dev_FINAL}",
            f"{m.chat.id}:customOwnerData:{Dev_FINAL}",
            f"{m.chat.id}:customOwnerUser:{Dev_FINAL}",
            f"{m.chat.id}:ownerChannelUrl:{Dev_FINAL}",
            f"{m.chat.id}:ownerChannelText:{Dev_FINAL}",
            f"owner_cache_{m.chat.id}_{Dev_FINAL}"
        )
        return await m.reply("• تم مسح يوزر المالك وإعادة كل شيء للافتراضي")

    if text in ["اضف زر المالك", "أضف زر المالك", "تعيين زر المالك", "تغير زر المالك", "تغيير زر المالك"]:
        if not await gowner_pls(m.from_user.id, m.chat.id):
            return await m.reply("• عذراً الامر لـ 「 المالك الاساسي 」 فقط")

        await r.set(f"{m.chat.id}:stepSetOwnerButtonText:{m.from_user.id}{Dev_FINAL}", "1")
        return await m.reply("• ارسلي النص الظاهر لزر المالك")

    if text == "حذف زر المالك":
        if not await gowner_pls(m.from_user.id, m.chat.id):
            return await m.reply("• عذراً الامر لـ 「 المالك الاساسي 」 فقط")
        await r.delete(f"{m.chat.id}:ownerChannelUrl:{Dev_FINAL}", f"{m.chat.id}:ownerChannelText:{Dev_FINAL}")
        return await m.reply("• تم حذف زر المالك")

    if text in ["اضف رد المالك", "أضف رد المالك", "تعيين رد المالك"]:
        if not await gowner_pls(m.from_user.id, m.chat.id):
            return await m.reply("• عذراً الامر لـ 「 المالك الاساسي 」 فقط")
        await r.set(f"{m.chat.id}:stepSetOwnerReply:{m.from_user.id}{Dev_FINAL}", "1")
        return await m.reply("• ارسل رد المالك")

    if text == "حذف رد المالك":
        if not await gowner_pls(m.from_user.id, m.chat.id):
            return await m.reply("• عذراً الامر لـ 「 المالك الاساسي 」 فقط")
        await r.delete(f"{m.chat.id}:ownerCustomReply:{Dev_FINAL}")
        return await m.reply("• تم  حذف رد المالك  .")

    if text == "المالك":
        custom_reply = await r.get(f"{m.chat.id}:ownerCustomReply:{Dev_FINAL}")
        if custom_reply:
            reply_text = custom_reply.decode('utf-8') if isinstance(custom_reply, bytes) else str(custom_reply)
            return await m.reply(reply_text)

        owner_data = None
        owner_id = None

        saved_data = await r.get(f"{m.chat.id}:customOwnerData:{Dev_FINAL}")
        if saved_data:
            # يوجد كاش صالح (لم تنتهِ صلاحيته بعد عبر TTL) — نستخدمه مباشرة
            # بدون أي استعلام حي لتيليجرام. بيانات المالك (الاسم/الصورة)
            # نادراً ما تتغير، فلا داعي لإعادة الجلب في كل استدعاء لهذا
            # الأمر؛ بمجرد انتهاء صلاحية الكاش (86400 ثانية) سيُعاد جلبها
            # وتخزينها من جديد تلقائياً عبر المسار الاحتياطي أدناه.
            try:
                data_str = saved_data.decode('utf-8') if isinstance(saved_data, bytes) else saved_data
                owner_data = json.loads(data_str)
                owner_id = owner_data.get("id")
            except Exception:
                owner_data = None

        if not owner_data:
            try:
                admins = await m.bot.get_chat_administrators(m.chat.id)
                for mm in admins:
                    if isinstance(mm, ChatMemberOwner) or getattr(mm, "status", "") == "creator":
                        owner_user = mm.user
                        owner_id = owner_user.id

                        photo_file_id = None
                        try:
                            photos = await m.bot.get_user_profile_photos(user_id=owner_id, limit=1)
                            if photos.total_count > 0:
                                photo_file_id = photos.photos[0][-1].file_id
                        except Exception:
                            pass

                        owner_data = {
                            "id": owner_user.id,
                            "username": owner_user.username or "",
                            "first_name": owner_user.first_name or "",
                            "last_name": owner_user.last_name or "",
                            "mention": owner_user.html_text if hasattr(owner_user, "html_text") else (owner_user.first_name or "المالك"),
                            "photo": photo_file_id,
                            "bio": getattr(owner_user, "bio", "") or ""
                        }
                        await r.set(f"{m.chat.id}:customOwnerData:{Dev_FINAL}", json.dumps(owner_data), ex=86400)
                        break
            except Exception as e:
                print(f"Error fetching administrators: {e}")

        if not owner_data:
            return await m.reply("• لم أتمكن من العثور على المالك")

        bio_text = owner_data.get("bio", "")
        if not bio_text and owner_id:
            try:
                full_owner_info = await m.bot.get_chat(owner_id)
                bio_text = getattr(full_owner_info, "bio", "") or ""
                owner_data["bio"] = bio_text
                await r.set(f"{m.chat.id}:customOwnerData:{Dev_FINAL}", json.dumps(owner_data))
            except Exception:
                pass

        first_name = owner_data.get("first_name", "المالك")
        mention = owner_data.get("mention", first_name)

        caption = f"• Owner  ↦ {mention}\n\n• Bio  ↦ {bio_text}"

        keyboard_rows = [
            [InlineKeyboardButton(text=first_name, url=f"tg://user?id={owner_id}")]
        ]

        owner_channel = await r.get(f"{m.chat.id}:ownerChannelUrl:{Dev_FINAL}")
        if owner_channel:
            channel_url_str = owner_channel.decode('utf-8') if isinstance(owner_channel, bytes) else str(owner_channel)
            saved_btn_text = await r.get(f"{m.chat.id}:ownerChannelText:{Dev_FINAL}")
            if saved_btn_text:
                btn_label = saved_btn_text.decode('utf-8') if isinstance(saved_btn_text, bytes) else str(saved_btn_text)
            else:
                btn_label = "قناة المالك"
            keyboard_rows.append([InlineKeyboardButton(text=btn_label, url=channel_url_str)])

        button = InlineKeyboardMarkup(inline_keyboard=keyboard_rows)

        photo_file_id = owner_data.get("photo")
        if photo_file_id:
            try:
                await m.reply_photo(photo=photo_file_id, caption=caption, reply_markup=button)
                return
            except Exception as e:
                print(f"Error sending photo: {e}")
                try:
                    photos = await m.bot.get_user_profile_photos(user_id=owner_id, limit=1)
                    if photos.total_count > 0:
                        new_photo_id = photos.photos[0][-1].file_id
                        owner_data["photo"] = new_photo_id
                        await r.set(f"{m.chat.id}:customOwnerData:{Dev_FINAL}", json.dumps(owner_data))
                        await m.reply_photo(photo=new_photo_id, caption=caption, reply_markup=button)
                        return
                except Exception:
                    pass

        await m.reply(caption, reply_markup=button)

    return None
