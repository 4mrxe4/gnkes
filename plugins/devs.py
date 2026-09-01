import html
from helpers.context import get_global_r, get_global_dev, get_global_k, get_current_bot_id, get_redis, get_dev_final, set_current_bot_id
from helpers.context import get_config, get_current_bot_id, set_current_bot_id, _bot_contexts
from helpers.context import get_current_bot_id, get_bot_from_client, get_redis, get_config_from_client, set_current_bot_id
from helpers.assistant import assistant_manager
from cluster import bot_manager
from helpers.emoji import render_custom_emoji_entities
@property
def r():
    return get_global_r()

@property
def Dev_FINAL():
    return get_global_dev()

@property
def k():
    return get_global_k()

import random, re, time, json, html, httpx
from helpers.http import http_get_text
import urllib.parse
import os
import uuid
import sys
import traceback
import psutil
import platform
import socket
import builtins
from threading import Thread
from compat import *
from compat import *
from compat import *
from helpers.ranks import *
from io import StringIO
from pytio import Tio, TioRequest
from datetime import datetime, timedelta
from helpers.utils import *
from meval import meval
from httpx import HTTPError
import asyncio
from compat import errors
from helpers.context import get_current_bot_id, get_redis, get_dev_final, set_current_bot_id
from cluster import bot_manager
from helpers.redis import RedisFake

from plugins.games.devgames import (
    get_public_categories,
    save_public_categories,
    move_game_to_category,
    get_games_by_category,
    get_public_game_meta,
    get_public_button_game_data,
    is_public_game_admin,
    handle_play_public_game,
    handle_play_public_button_game
)

from plugins.confess import _has_whisper_pending

from plugins.replies import global_reply, global_multi_reply, global_special_reply

from plugins.games.addgame import (
    handle_social_games,
    get_all_custom_games,
    get_custom_game_meta,
    get_button_game_data,
    CUSTOM_BUTTON_GAMES_KEY,
)

from helpers.ranks import (
    admin_pls,
    mod_pls,
    owner_pls,
    gowner_pls,
    dev_pls,
    dev2_pls,
    devp_pls,
    pre_pls,
    get_rank,
    check_and_guard_locked_command,
    is_service_enabled,
    register_bot_service,
    get_bot_registered_services,
    get_bot_service_lock_map,
)
from helpers.context import get_config, get_current_bot_id, set_current_bot_id, _bot_contexts
from helpers.context import (
    get_current_bot_id,
    get_bot_from_client,
    get_redis,
    get_config_from_client,
    set_current_bot_id,
)
from compat import FloodWait, UserIsBlocked, InputUserDeactivated, PeerIdInvalid, ChatWriteForbidden

import importlib.util
from helpers.replies_store import (
    REPLIES,
    plugins_devs_1041,
    plugins_devs_1050,
    plugins_devs_1114,
    plugins_devs_1116,
    plugins_devs_1138,
    plugins_devs_1140,
    plugins_devs_1150,
    plugins_devs_1157,
    plugins_devs_1173,
    plugins_devs_1189,
    plugins_devs_1191,
    plugins_devs_1215,
    plugins_devs_1262,
    plugins_devs_1343,
    plugins_devs_1374,
    plugins_devs_1378,
    plugins_devs_1380,
    plugins_devs_1385,
    plugins_devs_1387,
    plugins_devs_1427,
    plugins_devs_1437,
    plugins_devs_1440,
    plugins_devs_1445,
    plugins_devs_1448,
    plugins_devs_1453,
    plugins_devs_1456,
    plugins_devs_1461,
    plugins_devs_1466,
    plugins_devs_1468,
    plugins_devs_1473,
    plugins_devs_1478,
    plugins_devs_1480,
    plugins_devs_1485,
    plugins_devs_1488,
    plugins_devs_1491,
    plugins_devs_1496,
    plugins_devs_1505,
    plugins_devs_1509,
    plugins_devs_1511,
    plugins_devs_1514,
    plugins_devs_1518,
    plugins_devs_1520,
    plugins_devs_1523,
    plugins_devs_1527,
    plugins_devs_1529,
    plugins_devs_1532,
    plugins_devs_1536,
    plugins_devs_1538,
    plugins_devs_1541,
    plugins_devs_1545,
    plugins_devs_1548,
    plugins_devs_1562,
    plugins_devs_1565,
    plugins_devs_1583,
    plugins_devs_1586,
    plugins_devs_1604,
    plugins_devs_1607,
    plugins_devs_1618,
    plugins_devs_1621,
    plugins_devs_1647,
    plugins_devs_1648,
    plugins_devs_1652,
    plugins_devs_1654,
    plugins_devs_1657,
    plugins_devs_1661,
    plugins_devs_1663,
    plugins_devs_1670,
    plugins_devs_1673,
    plugins_devs_1681,
    plugins_devs_1683,
    plugins_devs_1687,
    plugins_devs_1689,
    plugins_devs_1693,
    plugins_devs_1695,
    plugins_devs_1699,
    plugins_devs_1701,
    plugins_devs_1705,
    plugins_devs_1707,
    plugins_devs_1711,
    plugins_devs_1713,
    plugins_devs_1717,
    plugins_devs_1719,
    plugins_devs_1723,
    plugins_devs_1725,
    plugins_devs_1729,
    plugins_devs_1732,
    plugins_devs_1736,
    plugins_devs_1739,
    plugins_devs_1743,
    plugins_devs_1746,
    plugins_devs_1750,
    plugins_devs_1751,
    plugins_devs_1757,
    plugins_devs_1771,
    plugins_devs_1792,
    plugins_devs_1832,
    plugins_devs_1838,
    plugins_devs_1842,
    plugins_devs_1846,
    plugins_devs_1850,
    plugins_devs_1854,
    plugins_devs_1883,
    plugins_devs_1894,
    plugins_devs_1907,
    plugins_devs_1913,
    plugins_devs_1917,
    plugins_devs_1935,
    plugins_devs_1941,
    plugins_devs_1948,
    plugins_devs_1952,
    plugins_devs_1954,
    plugins_devs_1959,
    plugins_devs_2001,
    plugins_devs_2079,
    plugins_devs_2109,
    plugins_devs_2113,
    plugins_devs_2118,
    plugins_devs_2120,
    plugins_devs_259,
    plugins_devs_261,
    plugins_devs_454,
    plugins_devs_478,
    plugins_devs_482,
    plugins_devs_485,
    plugins_devs_488,
    plugins_devs_505,
    plugins_devs_509,
    plugins_devs_527,
    plugins_devs_536,
    plugins_devs_543,
    plugins_devs_547,
    plugins_devs_551,
    plugins_devs_566,
    plugins_devs_568,
    plugins_devs_598,
    plugins_devs_607,
    plugins_devs_613,
    plugins_devs_672,
    plugins_devs_679,
    plugins_devs_689,
    plugins_devs_728,
    plugins_devs_754,
    plugins_devs_794,
    plugins_devs_904,
    plugins_devs_912,
    plugins_devs_919,
    plugins_devs_923,
    plugins_devs_927,
    plugins_devs_931,
    plugins_devs_936,
    plugins_devs_939,
    plugins_devs_945,
    plugins_devs_997,
)

def get_current_dev_final():
    return get_current_bot_id()

def get_current_dev_final_from_client(client):
    return getattr(client, 'bot_id', None)

def get_bot_redis_from_client(client):
    return getattr(client, 'redis', None)

def get_bot_config_from_client(client):
    return getattr(client, 'bot_config', None)

async def is_super_owner(user_id: int) -> bool:
    return user_id == 5434703779

async def is_main_dev(user_id: int, client=None) -> bool:
    if await is_super_owner(user_id):
        return True
    
    from helpers.ranks import _get_bot_data_async
    data = await _get_bot_data_async(client)
    bot_id = data['bot_id']
    r = data['redis']
    
    if not bot_id:
        return False
    
    owner = await r.get(f'{bot_id}botowner')
    if owner:
        return user_id == int(owner)
    
    try:
        cfg = _bot_contexts.get(bot_id, {}).get('config') if bot_id else None
        if cfg is not None and getattr(cfg, 'OWNER_ID', None):
            return user_id == cfg.OWNER_ID
    except Exception:
        pass
    try:
        from settings import OWNER_ID
        return user_id == OWNER_ID
    except:
        return False

async def is_dev2(user_id: int, client=None) -> bool:
    if await is_main_dev(user_id, client):
        return True
    
    from helpers.ranks import _get_bot_data_async
    data = await _get_bot_data_async(client)
    bot_id = data['bot_id']
    r = data['redis']
    
    if not bot_id:
        return False
    
    return await r.get(f'{user_id}:rankDEV2:{bot_id}') is not None

async def is_dev(user_id: int, client=None) -> bool:
    if await is_dev2(user_id, client):
        return True
    
    from helpers.ranks import _get_bot_data_async
    data = await _get_bot_data_async(client)
    bot_id = data['bot_id']
    r = data['redis']
    
    if not bot_id:
        return False
    
    return await r.get(f'{user_id}:rankDEV:{bot_id}') is not None

async def get_devs_br():
    try:
        bot_id = get_current_dev_final()
        if not bot_id:
            return []

        devs_list = []
        r = RedisFake(bot_id=bot_id)

        try:
            owner = await r.get(f'{bot_id}botowner')
            if owner:
                devs_list.append(int(owner))
            else:
                devs_list.append(5434703779)
            if await r.get(f'dev2_notif_enabled:{bot_id}'):
                if await r.smembers(f'{bot_id}DEV2'):
                    for dev2 in await r.smembers(f'{bot_id}DEV2'):
                        devs_list.append(int(dev2))
        except:
            pass
        return list(dict.fromkeys(devs_list))
    except:
        return []

async def is_bot_owner_of(user_id: int, current_bot_id) -> bool:
    r = get_global_r()
    bot_owner = await r.get(f'{current_bot_id}botowner')
    return bool(bot_owner) and int(bot_owner) == int(user_id)

DEV_PANEL_BUTTONS = {
    'الإحصائيات', 'الاحصائيات',
    'اشتراكي', 'أوامر التواصل', 'التواصل',
    'تعطيل البوت الخدمي', 'تفعيل البوت الخدمي',
    'ترحيب البوت',
    'اضف صورة الترحيب', 'مسح صورة الترحيب',
    'اضف رسالة الترحيب', 'حذف رسالة الترحيب',
    'أوامر الألعاب',
    'أوامر الردود',
    'أوامر الإذاعة',
    'أوامر الحظر والكتم',
    'إعدادات أخرى',
    'ضع اسم البوت', 'تعيين اسم البوت', 'مسح اسم البوت',
    'ضع رمز السورس', 'وضع رمز السورس', 'مسح رمز السورس',
    'تعيين قناة السورس', 'حذف قناة السورس',
    'تعيين الاشتراك الاجباري', 'مسح الاشتراك الاجباري',
    'تعيين كليشة الايدي عام', 'مسح كليشة الايدي عام',
    'نسخة المشتركين', 'نسخة المجموعات',
    'الاشتراكات',
    'اذاعة بالخاص', 'اذاعة بالخاص تثبيت',
    'اذاعة بالمجموعات', 'اذاعة بالمجموعات تثبيت',
    'المحظورين عام', 'مسح المحظورين عام',
    'المكتومين عام', 'مسح المكتومين عام',
    'تعطيل التواصل', 'تفعيل التواصل',
    'تعطيل الردود', 'تفعيل الردود',
    'محظورين التواصل', 'مسح رد تواصل', 'اضف رد تواصل',
    'الحساب المساعد',
    'اضف حساب مساعد', 'مسح حساب مساعد',
    'العودة', 'عودة', 'رجوع', 'الغاء',
}

def is_dev_panel_button(text: str) -> bool:
    return bool(text) and text.strip() in DEV_PANEL_BUTTONS

async def build_dev_panel_rows(user_id: int, current_bot_id):
    is_owner_of_this_bot = await is_bot_owner_of(user_id, current_bot_id)
    dev2 = await is_dev2(user_id)
    is_super = await is_super_owner(user_id)
    rows = []
    rows.append(['الإحصائيات'])
    rows.append(['تعطيل البوت الخدمي', 'تفعيل البوت الخدمي'])
    rows.append(['ترحيب البوت', 'أوامر الألعاب'])
    rows.append(['أوامر الردود', 'أوامر الإذاعة'])
    rows.append(['أوامر الحظر والكتم', 'إعدادات أخرى'])
    rows.append(['ضع اسم البوت', 'ضع رمز السورس'])
    rows.append(['أوامر التواصل'])
    if dev2 and is_owner_of_this_bot:
        rows.append(['الحساب المساعد', 'اشتراكي'])
    else:
        if is_super:
            rows.append(['الاشتراكات'])
        else:
            rows.append(['اشتراكي'])
    rows.append(['الغاء'])
    return rows

async def get_bot_welcome_text(current_bot_id, name):
    r = get_global_r()
    custom = await r.get(f'{current_bot_id}:StartWelcomeText')
    if custom:
        return custom
    return plugins_devs_794(name)

async def send_bot_welcome(c, m, current_bot_id, name, bot_username, channel, extra_markup_rows=None):
    r = get_global_r()
    text = await get_bot_welcome_text(current_bot_id, name)
    photo = await r.get(f'{current_bot_id}:StartWelcomePhoto')
    buttons = [
        [InlineKeyboardButton('ضيفني لـ مجموعتك', url=f'https://t.me/{bot_username}?startgroup=Commands&admin=ban_users+restrict_members+delete_messages+add_admins+change_info+invite_users+pin_messages+manage_call+manage_chat+manage_video_chats+promote_members')],
        [InlineKeyboardButton(f'تحديثات {name}', url=f'https://t.me/{channel}')]
    ]
    if photo:
        return await m.reply_photo(photo=photo, caption=text, reply_markup=InlineKeyboardMarkup(buttons))
    return await m.reply(text=text, reply_markup=InlineKeyboardMarkup(buttons))

async def build_dev_games_rows(current_bot_id):
    r = get_global_r()
    names = set()
    for g in await get_all_custom_games():
        n = g.get('name') if isinstance(g, dict) else None
        if n:
            names.add(n)
    button_games = await r.hgetall(CUSTOM_BUTTON_GAMES_KEY) or {}
    for n in button_games.keys():
        if isinstance(n, bytes):
            n = n.decode('utf-8')
        if n:
            names.add(n)
    rows = []
    for n in sorted(names):
        rows.append([f'حذف {n}', f'اضف {n}'])
    rows.append(['رجوع'])
    return rows

async def show_dev_panel(c, m, k, current_bot_id, quote=True):
    rows = await build_dev_panel_rows(m.from_user.id, current_bot_id)
    reply_markup = ReplyKeyboardMarkup(rows, resize_keyboard=True, placeholder='Welcome')
    try:
        if await is_super_owner(m.from_user.id):
            rank = 'تاج راسي'
        else:
            rank = await get_rank(m.from_user.id, m.from_user.id, c)
    except Exception:
        rank = 'عضو'
    if not rank:
        rank = 'عضو'
    text = (
        f'• اهلا بك عزيزي {rank} .\n'
        f'- في اوامرك الخاصه .\n'
        f'- يمكنك تحكم في بوت عن طريق الكيبورد ادناه .'
    )
    return await m.reply(quote=quote, text=text, reply_markup=reply_markup)

async def set_service_enabled(bot_id: str, service_name: str, enabled: bool) -> bool:
    try:
        bot_id = str(bot_id)
        r_target = RedisFake(bot_id=bot_id)
        if enabled:
            await r_target.delete(f'PaidServiceDisabled:{service_name}:{bot_id}')
            return True
        else:
            return await r_target.set(f'PaidServiceDisabled:{service_name}:{bot_id}', 1)
    except:
        return False

async def resolve_target_bot_id(c, raw_text: str):
    if not raw_text:
        return None, None
    value = raw_text.strip()
    if not value:
        return None, None

    if value.isdigit():
        bot_id = value
        label = bot_id
        try:
            user = await c.get_users(int(bot_id))
            if user:
                label = f'@{user.username}' if getattr(user, 'username', None) else (user.first_name or bot_id)
        except Exception:
            pass
        return bot_id, label

    username = value.lstrip('@').strip()
    if not username:
        return None, None
    try:
        user = await c.get_users(username)
    except Exception:
        return None, None
    if not user or not getattr(user, 'id', None):
        return None, None
    label = f'@{user.username}' if getattr(user, 'username', None) else (user.first_name or str(user.id))
    return str(user.id), label

DEFAULT_CONTACT_REPLY = 'تم ارسال رسالتك للمطور بنجاح'

async def get_contact_targets(current_bot_id):
    r = get_global_r()
    dev_group = await r.get(f'DevGroup:{current_bot_id}')
    if dev_group:
        return [int(dev_group)]
    return [int(dev) for dev in await get_devs_br()]

async def build_contact_panel_text(k, current_bot_id):
    r = get_global_r()
    contact_on = bool(await r.get(f'ContactEnabled:{current_bot_id}'))
    replies_on = bool(await r.get(f'ContactRepliesEnabled:{current_bot_id}'))
    reply_text = await r.get(f'ContactReplyText:{current_bot_id}') or DEFAULT_CONTACT_REPLY
    banned = await r.smembers(f'ContactBanned:{current_bot_id}')
    banned_count = len(banned) if banned else 0

    return (
        f"{k} لوحة التواصل مع المطورين\n\n"
        f"{k} حالة التواصل: {'مفعل ✓' if contact_on else 'معطل ✗'}\n"
        f"{k} حالة ردود التواصل: {'مفعلة ✓' if replies_on else 'معطلة ✗'}\n"
        f"{k} رد التواصل الحالي: {reply_text}\n"
        f"{k} عدد المحظورين من التواصل: {banned_count}\n\n"
        f"{k} اختر ما تريد من الازرار بالاسفل"
    )

async def show_contact_panel(c, m, k, current_bot_id):
    r = get_global_r()
    await r.set(f'{m.from_user.id}:contact_panel_step', 'waiting_action')
    reply_markup = ReplyKeyboardMarkup(
        [
            ['تعطيل التواصل', 'تفعيل التواصل'],
            ['تعطيل الردود', 'تفعيل الردود'],
            ['محظورين التواصل'],
            ['مسح رد تواصل', 'اضف رد تواصل'],
            ['رجوع']
        ],
        resize_keyboard=True
    )
    return await m.reply(
        quote=True,
        text=await build_contact_panel_text(k, current_bot_id),
        reply_markup=reply_markup
    )

async def execute_broadcast(c, m, k, current_bot_id, mode, pin):
    r = get_global_r()

    if mode == 'pv':
        targets_set = await r.smembers(f'{current_bot_id}:UsersList')
    else:
        targets_set = await r.smembers(f'enablelist:{current_bot_id}')

    try:
        if targets_set:
            try:
                targets = list(targets_set)
            except TypeError:
                targets = []
                for item in targets_set:
                    targets.append(item)
        else:
            targets = []
    except Exception as e:
        print(f"Error converting targets: {e}")
        targets = []

    if not targets:
        return await m.reply(plugins_devs_259(k, "مستخدمين" if mode == "pv" else "مجموعات"))

    status_msg = await m.reply(plugins_devs_261(k, len(targets)))

    success = 0
    blocked = 0
    failed = 0

    has_media = False
    media_file_id = None
    caption_text = m.caption if m.caption else m.text if m.text else ""
    media_type = None

    if m.photo:
        has_media = True
        media_file_id = m.photo.file_id
        media_type = "photo"
    elif m.video:
        has_media = True
        media_file_id = m.video.file_id
        media_type = "video"
    elif m.audio:
        has_media = True
        media_file_id = m.audio.file_id
        media_type = "audio"
    elif m.document:
        has_media = True
        media_file_id = m.document.file_id
        media_type = "document"
    elif m.sticker:
        has_media = True
        media_file_id = m.sticker.file_id
        media_type = "sticker"
    elif m.animation:
        has_media = True
        media_file_id = m.animation.file_id
        media_type = "animation"
    elif m.voice:
        has_media = True
        media_file_id = m.voice.file_id
        media_type = "voice"
    elif m.video_note:
        has_media = True
        media_file_id = m.video_note.file_id
        media_type = "video_note"

    for chat_id in targets:
        try:
            if has_media and media_file_id:
                if media_type == "photo":
                    sent = await c.send_photo(
                        chat_id=int(chat_id),
                        photo=media_file_id,
                        caption=caption_text
                    )
                elif media_type == "video":
                    sent = await c.send_video(
                        chat_id=int(chat_id),
                        video=media_file_id,
                        caption=caption_text
                    )
                elif media_type == "audio":
                    sent = await c.send_audio(
                        chat_id=int(chat_id),
                        audio=media_file_id,
                        caption=caption_text
                    )
                elif media_type == "document":
                    sent = await c.send_document(
                        chat_id=int(chat_id),
                        document=media_file_id,
                        caption=caption_text
                    )
                elif media_type == "sticker":
                    sent = await c.send_sticker(
                        chat_id=int(chat_id),
                        sticker=media_file_id
                    )
                elif media_type == "animation":
                    sent = await c.send_animation(
                        chat_id=int(chat_id),
                        animation=media_file_id,
                        caption=caption_text
                    )
                elif media_type == "voice":
                    sent = await c.send_voice(
                        chat_id=int(chat_id),
                        voice=media_file_id,
                        caption=caption_text
                    )
                elif media_type == "video_note":
                    sent = await c.send_video_note(
                        chat_id=int(chat_id),
                        video_note=media_file_id
                    )
                else:
                    sent = await c.send_message(
                        chat_id=int(chat_id),
                        text=caption_text or "رسالة"
                    )
            else:
                sent = await c.send_message(
                    chat_id=int(chat_id),
                    text=caption_text or m.text or "رسالة"
                )
            
            if pin:
                try:
                    await c.pin_chat_message(chat_id=int(chat_id), message_id=sent.id, disable_notification=True)
                except Exception:
                    pass
            success += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                if has_media and media_file_id:
                    if media_type == "photo":
                        sent = await c.send_photo(
                            chat_id=int(chat_id),
                            photo=media_file_id,
                            caption=caption_text
                        )
                    elif media_type == "video":
                        sent = await c.send_video(
                            chat_id=int(chat_id),
                            video=media_file_id,
                            caption=caption_text
                        )
                    elif media_type == "audio":
                        sent = await c.send_audio(
                            chat_id=int(chat_id),
                            audio=media_file_id,
                            caption=caption_text
                        )
                    elif media_type == "document":
                        sent = await c.send_document(
                            chat_id=int(chat_id),
                            document=media_file_id,
                            caption=caption_text
                        )
                    elif media_type == "sticker":
                        sent = await c.send_sticker(
                            chat_id=int(chat_id),
                            sticker=media_file_id
                        )
                    elif media_type == "animation":
                        sent = await c.send_animation(
                            chat_id=int(chat_id),
                            animation=media_file_id,
                            caption=caption_text
                        )
                    elif media_type == "voice":
                        sent = await c.send_voice(
                            chat_id=int(chat_id),
                            voice=media_file_id,
                            caption=caption_text
                        )
                    elif media_type == "video_note":
                        sent = await c.send_video_note(
                            chat_id=int(chat_id),
                            video_note=media_file_id
                        )
                    else:
                        sent = await c.send_message(
                            chat_id=int(chat_id),
                            text=caption_text or "رسالة"
                        )
                else:
                    sent = await c.send_message(
                        chat_id=int(chat_id),
                        text=caption_text or m.text or "رسالة"
                    )
                if pin:
                    try:
                        await c.pin_chat_message(chat_id=int(chat_id), message_id=sent.id, disable_notification=True)
                    except Exception:
                        pass
                success += 1
            except Exception:
                failed += 1
        except (UserIsBlocked, InputUserDeactivated, PeerIdInvalid, ChatWriteForbidden):
            blocked += 1
        except Exception as e:
            failed += 1
            print(f"Broadcast error for {chat_id}: {e}")
        await asyncio.sleep(0.05)

    try:
        await status_msg.edit(
            f'{k} تمت الاذاعة بنجاح\n\n'
            f'{k} تم الارسال بنجاح: {success}\n'
            f'{k} محظور/محذوف/مغلق: {blocked}\n'
            f'{k} فشل الارسال: {failed}'
        )
    except Exception:
        await m.reply(
            plugins_devs_454(k, k, success, k, blocked, k, failed)
        )


BOT_CREATION_PREFIX = "bot_creation:"

tio = Tio()

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

async def add_assistant_account(c, m, k, current_bot_id):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    
    if not await is_dev2(m.from_user.id):
        return await m.reply(plugins_devs_478(k))
    
    bot_owner = await r.get(f'{current_bot_id}botowner')
    if not bot_owner or int(bot_owner) != m.from_user.id:
        return await m.reply(plugins_devs_482(k))
    
    if await r.get(f'{m.chat.id}:addAssistant:{m.from_user.id}{current_bot_id}'):
        return await m.reply(plugins_devs_485(k))
    
    await r.set(f'{m.chat.id}:addAssistant:{m.from_user.id}{current_bot_id}', 1, ex=600)
    return await m.reply(plugins_devs_488(k, k, k, k, k, k))

async def process_add_assistant(c, m, k, current_bot_id):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    
    if m.text == 'الغاء':
        await r.delete(f'{m.chat.id}:addAssistant:{m.from_user.id}{current_bot_id}')
        return await m.reply(plugins_devs_505(k))
    
    bot_owner = await r.get(f'{current_bot_id}botowner')
    if not bot_owner or int(bot_owner) != m.from_user.id:
        return await m.reply(plugins_devs_509(k))
    
    session_string = m.text.strip()
    
    success, message, user_id = await assistant_manager.add_assistant(current_bot_id, session_string)
    
    if success:
        await r.delete(f'{m.chat.id}:addAssistant:{m.from_user.id}{current_bot_id}')
        
        assistant_client = await assistant_manager.create_assistant_client(current_bot_id)
        if assistant_client:
            if current_bot_id in _bot_contexts:
                _bot_contexts[current_bot_id]['assistant'] = assistant_client
                _bot_contexts[current_bot_id]['assistant_client'] = assistant_client
            
            if current_bot_id in bot_manager.bots:
                bot_manager.bots[current_bot_id]['assistant'] = assistant_client
        
        await m.reply(plugins_devs_527(k, k, message, k, user_id, k))
    else:
        await m.reply(plugins_devs_536(k, message))

async def remove_assistant_account(c, m, k, current_bot_id):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    
    if not await is_dev2(m.from_user.id):
        return await m.reply(plugins_devs_543(k))
    
    bot_owner = await r.get(f'{current_bot_id}botowner')
    if not bot_owner or int(bot_owner) != m.from_user.id:
        return await m.reply(plugins_devs_547(k))
    
    assistant_data = await assistant_manager.get_assistant(current_bot_id)
    if not assistant_data:
        return await m.reply(plugins_devs_551(k))
    
    success, message = await assistant_manager.remove_assistant(current_bot_id)
    
    if success:
        if current_bot_id in _bot_contexts:
            if 'assistant' in _bot_contexts[current_bot_id]:
                del _bot_contexts[current_bot_id]['assistant']
            if 'assistant_client' in _bot_contexts[current_bot_id]:
                del _bot_contexts[current_bot_id]['assistant_client']
        
        if current_bot_id in bot_manager.bots:
            if 'assistant' in bot_manager.bots[current_bot_id]:
                bot_manager.bots[current_bot_id]['assistant'] = None
        
        await m.reply(plugins_devs_566(k, message))
    else:
        await m.reply(plugins_devs_568(k, message))

async def run_bot_in_background(token, owner_id, days, bot_id, m):
    try:
        r = RedisFake()
        
        success, message = await bot_manager.start_bot(token, owner_id, days)
        
        if success:
            cluster_id = bot_manager.bots[bot_id]['cluster_id']
            
            bot_data = await r.hget('subscribed_bots', bot_id)
            if bot_data:
                data = json.loads(bot_data)
                data['cluster_id'] = cluster_id
                await r.hset('subscribed_bots', bot_id, json.dumps(data))
            
            bot_r = RedisFake(bot_id=bot_id)
            bot_data = await bot_r.hget('subscribed_bots', bot_id)
            if bot_data:
                data = json.loads(bot_data)
                data['cluster_id'] = cluster_id
                await bot_r.hset('subscribed_bots', bot_id, json.dumps(data))
            
            set_current_bot_id(bot_id)
            
            await bot_r.set(f'{owner_id}:rankDEV:{bot_id}', '1')
            await bot_r.sadd(f'{bot_id}DEV2', owner_id)
            
            try:
                await m.reply(
                    plugins_devs_598(cluster_id, bot_id)
                )
            except Exception as e:
                print(f"Error sending response: {e}")
        else:
            try:
                await m.reply(plugins_devs_607(message))
            except Exception as e:
                print(f"Error sending response: {e}")
                
    except Exception as e:
        try:
            await m.reply(plugins_devs_613(str(e)))
        except Exception as e2:
            print(f"Error sending response: {e2}")
        print(f"Error in run_bot_in_background: {e}")
        import traceback
        traceback.print_exc()

@Client.on_message(filters.private, group=-14)
async def dev_games_content_handler(c, m):
    if not m.from_user:
        return
    r = get_global_r()
    current_bot_id = get_current_dev_final_from_client(c) or get_current_dev_final()
    if not current_bot_id:
        return
    if not await is_dev2(m.from_user.id, c):
        return
    k = await r.get(f'{current_bot_id}:botkey') or get_global_k()
    uid, cid = m.from_user.id, m.chat.id

    text = m.text or ''

    if is_dev_panel_button(text):
        return
    if await r.get(f'{cid}:addAssistant:{uid}{current_bot_id}'):
        return
    welcome_or_id_flags = [
        f'{cid}:setWelcomePhoto:{uid}{current_bot_id}',
        f'{cid}:setWelcomeText:{uid}{current_bot_id}',
        f'{cid}:setBotChannel:{uid}{current_bot_id}',
        f'{cid}:addCustomIDG:{uid}{current_bot_id}',
        f'{cid}:setBotName:{uid}{current_bot_id}',
        f'{cid}:setBotKey:{uid}{current_bot_id}',
    ]
    if any([await r.get(f) for f in welcome_or_id_flags]):
        return

    has_step = any([
        await r.get(f'{uid}:addMediaStep:{cid}{current_bot_id}'),
        await r.get(f'{uid}:addButtonStep:{cid}{current_bot_id}'),
        await r.get(f'{uid}:deleteMediaStep:{cid}{current_bot_id}'),
        await r.get(f'{uid}:deleteGameStep:{cid}{current_bot_id}'),
    ])

    is_content_cmd = False
    if text.startswith('اضف ') or text.startswith('حذف '):
        parts = text.split(' ', 1)
        if len(parts) == 2:
            game_name = parts[1].strip()
            if game_name and (await get_custom_game_meta(game_name) or await get_button_game_data(game_name)):
                is_content_cmd = True

    if has_step or is_content_cmd:
        await handle_social_games(c, m, k, text)

@Client.on_message(filters.private, group=-15)
async def dev_global_replies_handler(c, m):
    if not m.from_user:
        return
    r = get_global_r()
    current_bot_id = get_current_dev_final_from_client(c) or get_current_dev_final()
    if not current_bot_id:
        return
    if not await is_dev2(m.from_user.id, c):
        return
    k = await r.get(f'{current_bot_id}:botkey') or get_global_k()

    text = m.text or ''
    cid, uid = m.chat.id, m.from_user.id

    special_flags = [
        f'{cid}:addFilterGS:{uid}{current_bot_id}',
        f'{cid}:addFilterGS2:{uid}{current_bot_id}',
        f'{cid}:delFilterGS:{uid}{current_bot_id}',
    ]
    multi_flags = [
        f'{cid}:addFilterGM:{uid}{current_bot_id}',
        f'{cid}:addFilterGM2:{uid}{current_bot_id}',
        f'{cid}:delFilterGM:{uid}{current_bot_id}',
    ]
    plain_flags = [
        f'{cid}:addFilterG:{uid}{current_bot_id}',
        f'{cid}:addFilterG2:{uid}{current_bot_id}',
        f'{cid}:delFilterG:{uid}{current_bot_id}',
        f'{cid}:addInlineStepGlobal:{uid}{current_bot_id}',
    ]

    has_special = any([await r.get(f) for f in special_flags])
    has_multi = any([await r.get(f) for f in multi_flags])
    has_plain = any([await r.get(f) for f in plain_flags])

    if await r.get(f'{m.chat.id}:addAssistant:{m.from_user.id}{current_bot_id}'):
        return

    if text in ('اضف رد مميز عام', 'مسح رد مميز عام') or has_special:
        return await global_special_reply(c, m, k)
    if text in ('اضف رد متعدد عام', 'مسح رد متعدد عام') or has_multi:
        return await global_multi_reply(c, m, k)
    if text in ('اضف رد عام', 'مسح رد عام') or has_plain:
        return await global_reply(c, m, k)

@Client.on_message(filters.private & filters.photo, group=-16)
async def dev_welcome_photo_handler(c, m):
    if not m.from_user:
        return
    r = get_global_r()
    current_bot_id = get_current_dev_final_from_client(c) or get_current_dev_final()
    if not current_bot_id:
        return
    flag_key = f'{m.chat.id}:setWelcomePhoto:{m.from_user.id}{current_bot_id}'
    if not await r.get(flag_key):
        return
    if not await is_dev2(m.from_user.id, c):
        await r.delete(flag_key)
        return
    await r.delete(flag_key)
    await r.set(f'{current_bot_id}:StartWelcomePhoto', m.photo.file_id)
    k = await r.get(f'{current_bot_id}:botkey') or get_global_k()
    await m.reply(quote=True, text=f'{k} تم تعيين صورة الترحيب بنجاح')

@Client.on_message(filters.private & filters.text, group=-16)
async def bot_creation_handler(c, m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    user_id = m.from_user.id
    
    if not await is_super_owner(user_id):
        return
    
    text = m.text
    r = get_redis()
    step_data = await r.hgetall(f'{BOT_CREATION_PREFIX}{user_id}')
    
    if text == 'اضف اشتراك' and not step_data:
        await r.hset(f'{BOT_CREATION_PREFIX}{user_id}', 'step', 'waiting_token')
        await m.reply(
            REPLIES['plugins_devs_636']
        )
        return
    
    if not step_data:
        return
    
    step = step_data.get('step')
    
    if step == 'waiting_token':
        if ':' not in text:
            await m.reply(REPLIES['plugins_devs_649'])
            return
        
        try:
            from aiogram import Bot as _AiogramBot
            test_bot = _AiogramBot(token=text)
            try:
                bot_info = await test_bot.get_me()
            finally:
                await test_bot.session.close()

            await r.hset(f'{BOT_CREATION_PREFIX}{user_id}', 'token', text)
            await r.hset(f'{BOT_CREATION_PREFIX}{user_id}', 'bot_username', bot_info.username)
            await r.hset(f'{BOT_CREATION_PREFIX}{user_id}', 'step', 'waiting_owner')
            await r.expire(f'{BOT_CREATION_PREFIX}{user_id}', 600)
            
            await m.reply(
                plugins_devs_672(bot_info.first_name, bot_info.username)
            )
        except Exception as e:
            await m.reply(plugins_devs_679(str(e)))
            await r.delete(f'{BOT_CREATION_PREFIX}{user_id}')
        return
    
    if step == 'waiting_owner':
        try:
            owner_id = int(text)
            await r.hset(f'{BOT_CREATION_PREFIX}{user_id}', 'owner_id', owner_id)
            await r.hset(f'{BOT_CREATION_PREFIX}{user_id}', 'step', 'waiting_days')
            
            await m.reply(
                plugins_devs_689(owner_id)
            )
        except ValueError:
            await m.reply(REPLIES['plugins_devs_694'])
        return
    
    if step == 'waiting_days':
        try:
            days = int(text)
            if days < 1:
                await m.reply(REPLIES['plugins_devs_701'])
                return
            
            token = await r.hget(f'{BOT_CREATION_PREFIX}{user_id}', 'token')
            owner_id = int(await r.hget(f'{BOT_CREATION_PREFIX}{user_id}', 'owner_id'))
            bot_username = await r.hget(f'{BOT_CREATION_PREFIX}{user_id}', 'bot_username')
            Dev_FINAL_new = token.split(':')[0]
            
            from zoneinfo import ZoneInfo
            baghdad_tz = ZoneInfo('Asia/Baghdad')
            expiry_date = datetime.now(baghdad_tz) + timedelta(days=days)
            
            bot_data = {
                'token': token,
                'owner_id': owner_id,
                'bot_username': bot_username,
                'created_at': datetime.now(baghdad_tz).isoformat(),
                'expiry_date': expiry_date.isoformat(),
                'days': days,
                'created_by': m.from_user.id
            }
            
            await r.hset('subscribed_bots', Dev_FINAL_new, json.dumps(bot_data))
            
            bot_r = RedisFake(bot_id=Dev_FINAL_new)
            await bot_r.hset('subscribed_bots', Dev_FINAL_new, json.dumps(bot_data))
            
            await m.reply(
                plugins_devs_728(Dev_FINAL_new, bot_username, days, expiry_date.strftime("%Y-%m-%d %H:%M"))
            )
            
            asyncio.create_task(run_bot_in_background(token, owner_id, days, Dev_FINAL_new, m))
            
            try:
                await c.send_message(
                    owner_id,
                    f'تم تفعيل بوتك\n\n'
                    f'المدة: {days} يوم\n'
                    f'ينتهي: {expiry_date.strftime("%Y-%m-%d %H:%M")}\n\n'
                    f'رتبتك: Dev'
                )
            except:
                pass
            
            await r.delete(f'{BOT_CREATION_PREFIX}{user_id}')
            
        except ValueError:
            await m.reply(REPLIES['plugins_devs_752'])
        except Exception as e:
            await m.reply(plugins_devs_754(str(e)))
            await r.delete(f'{BOT_CREATION_PREFIX}{user_id}')
        return

@Client.on_message(filters.text & filters.private, group=1)
async def delRanksHandler(c, m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    user_id = m.from_user.id
    r = get_redis()
    if await r.exists(f'{BOT_CREATION_PREFIX}{user_id}'):
        return
    
    k = await r.get(f'{get_current_dev_final()}:botkey')
    await private_func(c, m, k)

async def private_func(c, m, k):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    r = get_redis()
    current_bot_id = get_current_dev_final()
    
    bot_username = await r.get(f'{current_bot_id}:bot_username')
    if not bot_username:
        try:
            me = await c.get_me()
            bot_username = me.username
            await r.set(f'{current_bot_id}:bot_username', bot_username)
        except:
            bot_username = 'unknown_bot'
    
    if await r.get(f'{m.from_user.id}:sarhni'):
        return
    text = m.text

    if text in ('العودة', 'عودة') and await is_dev(m.from_user.id, c):
        return await show_dev_panel(c, m, k, current_bot_id)

    name = await r.get(f'{current_bot_id}:BotName') if await r.get(f'{current_bot_id}:BotName') else 'فاينل'
    channel = await r.get(f'{current_bot_id}:BotChannel') if await r.get(f'{current_bot_id}:BotChannel') else ''
    
    if text == '/start' and not await is_dev(m.from_user.id, c):
        await send_bot_welcome(c, m, current_bot_id, name, bot_username, channel)
        
        categories = await get_public_categories()

        main_buttons = []
        row = []

        for i, game_name in enumerate(categories.get('الرئيسية', [])):
            game_meta = await get_public_game_meta(game_name)
            if game_meta and game_name and len(game_name) <= 64:
                row.append(game_name)
                if len(row) == 2:
                    main_buttons.append(row.copy())
                    row = []

        if row:
            main_buttons.append(row)

        row = []
        for category_name, games in categories.items():
            if category_name != 'الرئيسية' and games and category_name and len(category_name) <= 64:
                row.append(f'•• {category_name}')
                if len(row) == 2:
                    main_buttons.append(row.copy())
                    row = []

        if row:
            main_buttons.append(row)

        if not main_buttons:
            main_buttons = [
                ["القائمة الرئيسية"],          
            ]

        reply_markup = ReplyKeyboardMarkup(
            main_buttons,
            resize_keyboard=True
        )

        await m.reply(
            REPLIES['plugins_devs_842'],
            reply_markup=reply_markup
        )
        
        if not await r.sismember(f'{current_bot_id}:UsersList', m.from_user.id):
            await r.sadd(f'{current_bot_id}:UsersList', m.from_user.id)
            if m.from_user.username:
                username = f'@{m.from_user.username}'
            else:
                username = 'ماعنده يوزر'
            text = '''
شخص جديد دخل للبوت
اسمه : {}
ايديه : `{}`
معرفه : {}

عدد المستخدمين صار {}
'''.format(m.from_user.mention(), m.from_user.id, username, len(await r.smembers(f'{current_bot_id}:UsersList')))
            btn_name = (m.from_user.first_name or username or "مستخدم").strip()
            if not btn_name:
                btn_name = "مستخدم"
            btn_name = btn_name[:64]
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton(btn_name, callback_data=f"user_{m.from_user.id}")]
            ])
            if await r.get(f'DevGroup:{current_bot_id}'):
                await c.send_message(
                    int((await r.get(f'DevGroup:{current_bot_id}')) or 0),
                    text, reply_markup=reply_markup)
            else:
                for dev in await get_devs_br():
                    try:
                        await c.send_message(int(dev), text, disable_web_page_preview=True)
                    except:
                        pass
        
        return
    
    if text.startswith('•• '):
        category_name = text.replace('•• ', '')
        games = await get_games_by_category(category_name)
        
        game_buttons = []
        row = []
        
        for i, game_name in enumerate(games):
            row.append(game_name)
            if len(row) == 2:
                game_buttons.append(row.copy())
                row = []
        
        if row:
            game_buttons.append(row)
        
        game_buttons.append(['رجوع'])
        
        reply_markup = ReplyKeyboardMarkup(
            game_buttons,
            resize_keyboard=True
        )
        
        await m.reply(
            plugins_devs_904(category_name),
            reply_markup=reply_markup
        )
        return
    
    if text == 'التواصل' or text == 'أوامر التواصل':
        if not await is_dev(m.from_user.id, c):
            return await m.reply(quote=True, text=plugins_devs_912(k))

        return await show_contact_panel(c, m, k, current_bot_id)

    if text == 'ترحيب البوت':
        if not await is_dev(m.from_user.id, c):
            return await m.reply(quote=True, text=plugins_devs_912(k))
        await send_bot_welcome(c, m, current_bot_id, name, bot_username, channel)
        reply_markup = ReplyKeyboardMarkup(
            [
                ['اضف صورة الترحيب', 'مسح صورة الترحيب'],
                ['اضف رسالة الترحيب', 'حذف رسالة الترحيب'],
                ['الغاء'],
                ['رجوع'],
            ],
            resize_keyboard=True
        )
        return await m.reply(quote=True, text=f'{k} هذه رسالة /start الحالية لبوتك، اختر ما تريد تعديله بالاسفل', reply_markup=reply_markup)

    if text == 'اضف صورة الترحيب':
        if not await is_dev2(m.from_user.id):
            return await m.reply(quote=True, text=plugins_devs_1647(k))
        await r.set(f'{m.chat.id}:setWelcomePhoto:{m.from_user.id}{current_bot_id}', 1, ex=600)
        return await m.reply(quote=True, text=f'{k} ارسل الصورة التي تريدها لترحيب /start الآن\n{k} او اكتب الغاء')

    if text == 'مسح صورة الترحيب':
        if not await is_dev2(m.from_user.id):
            return await m.reply(quote=True, text=plugins_devs_1647(k))
        await r.delete(f'{current_bot_id}:StartWelcomePhoto')
        return await m.reply(quote=True, text=f'{k} تم مسح صورة الترحيب')

    if text == 'اضف رسالة الترحيب':
        if not await is_dev2(m.from_user.id):
            return await m.reply(quote=True, text=plugins_devs_1647(k))
        await r.set(f'{m.chat.id}:setWelcomeText:{m.from_user.id}{current_bot_id}', 1, ex=600)
        return await m.reply(quote=True, text=f'{k} ارسل نص رسالة الترحيب الجديدة الآن\n{k} او اكتب الغاء')

    if text == 'حذف رسالة الترحيب':
        if not await is_dev2(m.from_user.id):
            return await m.reply(quote=True, text=plugins_devs_1647(k))
        await r.delete(f'{current_bot_id}:StartWelcomeText')
        return await m.reply(quote=True, text=f'{k} تم حذف رسالة الترحيب المخصصة، رجعت للرسالة الافتراضية')

    if await r.get(f'{m.chat.id}:setWelcomePhoto:{m.from_user.id}{current_bot_id}'):
        if text == 'الغاء':
            await r.delete(f'{m.chat.id}:setWelcomePhoto:{m.from_user.id}{current_bot_id}')
            return await m.reply(quote=True, text=f'{k} تم الالغاء')
        if not m.photo:
            return await m.reply(quote=True, text=f'{k} ارسل صورة فعلا، او اكتب الغاء')
        return

    if await r.get(f'{m.chat.id}:setWelcomeText:{m.from_user.id}{current_bot_id}'):
        if text == 'الغاء':
            await r.delete(f'{m.chat.id}:setWelcomeText:{m.from_user.id}{current_bot_id}')
            return await m.reply(quote=True, text=f'{k} تم الالغاء')
        await r.delete(f'{m.chat.id}:setWelcomeText:{m.from_user.id}{current_bot_id}')
        await r.set(f'{current_bot_id}:StartWelcomeText', m.text)
        return await m.reply(quote=True, text=f'{k} تم تعيين رسالة الترحيب الجديدة بنجاح')

    if text == 'إعدادات أخرى':
        if not await is_dev(m.from_user.id, c):
            return await m.reply(quote=True, text=plugins_devs_912(k))
        reply_markup = ReplyKeyboardMarkup(
            [
                ['نسخة المشتركين', 'نسخة المجموعات'],
                ['تعيين كليشة الايدي عام', 'مسح كليشة الايدي عام'],
                ['تعيين قناة السورس', 'حذف قناة السورس'],
                ['تعيين الاشتراك الاجباري', 'مسح الاشتراك الاجباري'],
                ['العودة'],
            ],
            resize_keyboard=True
        )
        return await m.reply(quote=True, text=f'{k} اختر ما تريد من الاعدادات الاخرى', reply_markup=reply_markup)

    if text == 'نسخة المشتركين':
        if not await is_main_dev(m.from_user.id):
            return await m.reply(quote=True, text=plugins_devs_1894(k))
        lst = [int(chat) for chat in await r.smembers(f'{current_bot_id}:UsersList')]
        with open('users_backup.json', 'w+') as w:
            w.write(json.dumps({"botUsername": bot_username, "botID": c.id, "Users": lst}, indent=4, ensure_ascii=False))
        await m.reply_document('users_backup.json', quote=True)
        os.remove('users_backup.json')
        return

    if text == 'نسخة المجموعات':
        if not await is_main_dev(m.from_user.id):
            return await m.reply(quote=True, text=plugins_devs_1883(k))
        lst = [int(chat) for chat in await r.smembers(f'enablelist:{current_bot_id}')]
        with open('chats_backup.json', 'w+') as w:
            w.write(json.dumps({"botUsername": bot_username, "botID": c.id, "Chats": lst}, indent=4, ensure_ascii=False))
        await m.reply_document('chats_backup.json', quote=True)
        os.remove('chats_backup.json')
        return

    if text == 'تعيين قناة السورس':
        if not await is_dev2(m.from_user.id):
            return await m.reply(quote=True, text=plugins_devs_1693(k))
        await r.set(f'{m.chat.id}:setBotChannel:{m.from_user.id}{current_bot_id}', 1, ex=600)
        return await m.reply(quote=True, text=plugins_devs_1695(k))

    if text == 'حذف قناة السورس':
        if not await is_dev2(m.from_user.id):
            return await m.reply(quote=True, text=plugins_devs_1699(k))
        await r.delete(f'{current_bot_id}:BotChannel')
        return await m.reply(quote=True, text=plugins_devs_1701(k))

    if text == 'تعيين كليشة الايدي عام':
        if not await is_dev2(m.from_user.id):
            return await m.reply(quote=True, text=plugins_devs_1693(k))
        reply = '''
تمام , الحين ارسل شكل الايدي العام الجديد

- الاختصارات:

#الاسم ↼ يطلع اسم الشخص
#الايدي ↼ يطلع ايدي الشخص
#اليوزر ↼ يطلع يوزر الشخص
#الرتبه ↼ يطلع رتبته الشخص
#التفاعل ↼ يطلع تفاعل الشخص
#الرسائل ↼ يطلع كم رسالة عند الشخص
#التعديل ↼ يطلع كم مره عدل الشخص
#البايو ↼ يطلع البايو اللي كاتبه
#تعليق ↼ يطلع تعليق عشوائي
#الانشاء ↼ يطلع انشاء الحساب
#الهدايا ↼ يطلع عدد هدايا الشخص
#المستوى ↼ يطلع مستوى الشخص (نظام الهدايا بتليجرام)

او اكتب الغاء
'''
        await r.set(f'{m.chat.id}:addCustomIDG:{m.from_user.id}{current_bot_id}', 1, ex=600)
        return await m.reply(quote=True, text=reply)

    if text == 'مسح كليشة الايدي عام':
        if not await is_dev2(m.from_user.id):
            return await m.reply(quote=True, text=plugins_devs_1699(k))
        if not await r.get(f'customID:{current_bot_id}'):
            return await m.reply(quote=True, text=f'{k} لا توجد كليشة ايدي عامة محفوظة اصلا')
        await r.delete(f'customID:{current_bot_id}')
        return await m.reply(quote=True, text=f'{k} تم مسح كليشة الايدي العامة')

    if await r.get(f'{m.chat.id}:addCustomIDG:{m.from_user.id}{current_bot_id}'):
        if text == 'الغاء':
            await r.delete(f'{m.chat.id}:addCustomIDG:{m.from_user.id}{current_bot_id}')
            return await m.reply(quote=True, text=f'{k} تم الالغاء')
        custom_text = m.text
        if m.entities:
            custom_text = render_custom_emoji_entities(custom_text, m.entities)
        await r.delete(f'{m.chat.id}:addCustomIDG:{m.from_user.id}{current_bot_id}')
        await r.set(f'customID:{current_bot_id}', custom_text)
        return await m.reply(quote=True, text=f'{k} تم تعيين كليشة الايدي العامة بنجاح')

    if text == 'أوامر الألعاب':
        if not await is_dev2(m.from_user.id):
            return await m.reply(quote=True, text=plugins_devs_1647(k))
        rows = await build_dev_games_rows(current_bot_id)
        reply_markup = ReplyKeyboardMarkup(rows, resize_keyboard=True)
        if len(rows) == 1:
            return await m.reply(
                quote=True,
                text=f'{k} لا توجد العاب مضافة بعد في بوتك\n{k} انشئ لعبة اولاً بالامر ( اضف لعبه ) من داخل مجموعة',
                reply_markup=reply_markup
            )
        return await m.reply(quote=True, text=f'{k} اختر اللعبة التي تريد اضافة او حذف محتواها', reply_markup=reply_markup)

    if text == 'أوامر الردود':
        if not await is_dev(m.from_user.id, c):
            return await m.reply(quote=True, text=plugins_devs_912(k))
        reply_markup = ReplyKeyboardMarkup(
            [
                ['اضف رد مميز عام', 'مسح رد مميز عام'],
                ['اضف رد متعدد عام', 'مسح رد متعدد عام'],
                ['اضف رد عام', 'مسح رد عام'],
                ['العودة'],
            ],
            resize_keyboard=True
        )
        return await m.reply(quote=True, text=f'{k} اختر نوع الرد العام الذي تريد اضافته او مسحه', reply_markup=reply_markup)

    if text == 'أوامر الإذاعة':
        if not await is_dev(m.from_user.id, c):
            return await m.reply(quote=True, text=plugins_devs_912(k))
        reply_markup = ReplyKeyboardMarkup(
            [
                ['اذاعة بالخاص', 'اذاعة بالخاص تثبيت'],
                ['اذاعة بالمجموعات', 'اذاعة بالمجموعات تثبيت'],
                ['رجوع'],
            ],
            resize_keyboard=True
        )
        return await m.reply(
            quote=True,
            text=f'{k} اختر نوع الاذاعة التي تريدها من الازرار بالاسفل',
            reply_markup=reply_markup
        )

    if text == 'الحساب المساعد':
        if not await is_dev2(m.from_user.id) or not await is_bot_owner_of(m.from_user.id, current_bot_id):
            return await m.reply(quote=True, text=plugins_devs_478(k))
        reply_markup = ReplyKeyboardMarkup(
            [
                ['اضف حساب مساعد', 'مسح حساب مساعد'],
                ['رجوع'],
            ],
            resize_keyboard=True
        )
        return await m.reply(
            quote=True,
            text=f'{k} تحكم بالحساب المساعد لهذا البوت من الازرار بالاسفل',
            reply_markup=reply_markup
        )

    if await r.get(f'{m.from_user.id}:contact_panel_step') == 'waiting_action':
        if text == 'تفعيل التواصل':
            await r.set(f'ContactEnabled:{current_bot_id}', 1)
            return await m.reply(plugins_devs_919(k))
        elif text == 'تعطيل التواصل':
            await r.delete(f'ContactEnabled:{current_bot_id}')
            return await m.reply(plugins_devs_923(k))
        elif text == 'تفعيل الردود':
            await r.set(f'ContactRepliesEnabled:{current_bot_id}', 1)
            return await m.reply(plugins_devs_927(k))
        elif text == 'تعطيل الردود':
            await r.delete(f'ContactRepliesEnabled:{current_bot_id}')
            return await m.reply(plugins_devs_931(k))
        elif text == 'اضف رد تواصل':
            await r.set(f'{m.chat.id}:setContactReply:{m.from_user.id}{current_bot_id}', 1, ex=600)
            await r.delete(f'{m.from_user.id}:contact_panel_step')
            return await m.reply(plugins_devs_936(k, k))
        elif text == 'مسح رد تواصل':
            await r.delete(f'ContactReplyText:{current_bot_id}')
            return await m.reply(plugins_devs_939(k))
        elif text == 'محظورين التواصل':
            banned = await r.smembers(f'ContactBanned:{current_bot_id}')
            if not banned:
                return await m.reply(plugins_devs_945(k))
            txt = f'{k} المحظورين من التواصل:\n\n'
            count = 1
            for uid in banned:
                try:
                    user = await c.get_users(int(uid))
                    mention = f'@{user.username}' if user.username else user.mention()
                except Exception:
                    mention = f'<a href="tg://user?id={uid}">{html.escape(str(uid))}</a>'
                txt += f'{count}) {mention} ~ (`{uid}`)\n'
                count += 1
            return await m.reply(txt)
        elif text == 'رجوع':
            await r.delete(f'{m.from_user.id}:contact_panel_step')

    if text == 'رجوع':
        if await is_dev(m.from_user.id, c):
            return await show_dev_panel(c, m, k, current_bot_id)
        else:
            categories = await get_public_categories()
            main_buttons = []
            row = []
            
            for i, game_name in enumerate(categories.get('الرئيسية', [])):
                game_meta = await get_public_game_meta(game_name)
                if game_meta:
                    row.append(game_name)
                    if len(row) == 2:
                        main_buttons.append(row.copy())
                        row = []
            
            if row:
                main_buttons.append(row)
            
            row = []
            for category_name, games in categories.items():
                if category_name != 'الرئيسية' and games:
                    row.append(f'•• {category_name}')
                    if len(row) == 2:
                        main_buttons.append(row.copy())
                        row = []
            
            if row:
                main_buttons.append(row)
            
            reply_markup = ReplyKeyboardMarkup(
                main_buttons,
                resize_keyboard=True
            )
            
            await m.reply(
                REPLIES['plugins_devs_1034'],
                reply_markup=reply_markup
            )
        return
    
    if text == f'تحديثات {name}':
        await m.reply(
            plugins_devs_1041(channel),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(f'تحديثات {name}', url=f'https://t.me/{channel}')]
            ])
        )
        return
    
    if text == 'ضيفني لـ مجموعتك':
        await m.reply(
            plugins_devs_1050(),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton('ضيفني لـ مجموعتك', url=f'https://t.me/{bot_username}?startgroup=Commands&admin=ban_users+restrict_members+delete_messages+add_admins+change_info+invite_users+pin_messages+manage_call+manage_chat+manage_video_chats+promote_members')]
            ])
        )
        return
    
    if text == 'الاشتراكات' and await is_super_owner(m.from_user.id):
        reply_markup = ReplyKeyboardMarkup(
            [
                ['عرض البوتات', 'ايقاف بوت'],
                ['حذف بوت', 'اضف اشتراك'],
                ['رجوع']
            ],
            resize_keyboard=True
        )
        await m.reply(
            REPLIES['plugins_devs_1067'],
            reply_markup=reply_markup
        )
        return
    
    if text == 'عرض البوتات' and await is_super_owner(m.from_user.id):
        status = bot_manager.get_status()
        
        if status['total_bots'] == 0:
            await m.reply(REPLIES['plugins_devs_1077'])
            return
        
        text_msg = f'البوتات النشطة: {status["total_bots"]}\n'
        text_msg += f'الكلاسترز: {status["total_clusters"]}\n\n'
        
        for bot_id, info in status['bots'].items():
            bot_r = RedisFake(bot_id=bot_id)
            bot_data = await bot_r.hget('subscribed_bots', bot_id)
            if bot_data:
                bot_info = json.loads(bot_data)
                from zoneinfo import ZoneInfo
                baghdad_tz = ZoneInfo('Asia/Baghdad')
                expiry = datetime.fromisoformat(bot_info['expiry_date'])
                remaining = (expiry - datetime.now(baghdad_tz)).days
                if remaining < 0:
                    remaining = 0
                text_msg += f'ايدي: {bot_id}\n'
                text_msg += f'يوزر: @{info.get("bot_username", bot_info.get("bot_username", "غير معروف"))}\n'
                text_msg += f'المالكه: {bot_info["owner_id"]}\n'
                text_msg += f'المتبقي: {remaining} يوم\n'
                text_msg += f'الكلاستر: {info["cluster"]}\n'
                text_msg += f'الحالة: {info["status"]}\n\n'
        
        await m.reply(text_msg)
        return
    
    if text == 'ايقاف بوت' and await is_super_owner(m.from_user.id):
        await r.set(f'{m.from_user.id}:stop_bot_step', 'waiting_bot_id')
        await m.reply(REPLIES['plugins_devs_1106'])
        return
    
    if await r.get(f'{m.from_user.id}:stop_bot_step') == 'waiting_bot_id':
        if await is_super_owner(m.from_user.id):
            bot_id = text.strip()
            success, message = await bot_manager.stop_bot(bot_id, delete_permanent=False)
            if success:
                await m.reply(plugins_devs_1114(bot_id))
            else:
                await m.reply(plugins_devs_1116(message))
            await r.delete(f'{m.from_user.id}:stop_bot_step')
        return
    
    if text == 'حذف بوت' and await is_super_owner(m.from_user.id):
        await r.set(f'{m.from_user.id}:delete_bot_step', 'waiting_bot_id')
        await m.reply(REPLIES['plugins_devs_1122'])
        return
    
    if await r.get(f'{m.from_user.id}:delete_bot_step') == 'waiting_bot_id':
        if await is_super_owner(m.from_user.id):
            bot_id = text.strip()
            
            r_global = RedisFake()
            await r_global.hdel('subscribed_bots', bot_id)
            
            bot_r = RedisFake(bot_id=bot_id)
            await bot_r.hdel('subscribed_bots', bot_id)
            
            if bot_id in bot_manager.bots:
                success, message = await bot_manager.stop_bot(bot_id, delete_permanent=True)
                if success:
                    await m.reply(plugins_devs_1138(bot_id))
                else:
                    await m.reply(plugins_devs_1140(message))
            else:
                bot_dir = f"bots_data/{bot_id}"
                if os.path.exists(bot_dir):
                    import shutil
                    shutil.rmtree(bot_dir)
                
                for key in await bot_r.keys('*'):
                    await bot_r.delete(key)
                
                await m.reply(plugins_devs_1150(bot_id))
            
            await r.delete(f'{m.from_user.id}:delete_bot_step')
        return
    
    
    if text == 'اشتراكي':
        user_id = m.from_user.id
        bot_found = False
        bot_r = RedisFake(bot_id=current_bot_id)
        all_bots = await bot_r.hgetall('subscribed_bots')
        
        for bot_id, data in all_bots.items():
            bot_info = json.loads(data)
            if bot_info.get('owner_id') == user_id:
                bot_found = True
                from zoneinfo import ZoneInfo
                baghdad_tz = ZoneInfo('Asia/Baghdad')
                expiry = datetime.fromisoformat(bot_info['expiry_date'])
                remaining = (expiry - datetime.now(baghdad_tz)).days
                if remaining < 0:
                    remaining = 0
                
                status = 'يعمل'
                if bot_id not in bot_manager.bots:
                    status = 'متوقف'
                
                await m.reply(
                    plugins_devs_1215(bot_id, bot_info.get("bot_username", "غير معروف"), remaining, status, expiry.strftime("%Y-%m-%d %H:%M"))
                )
                break
        
        if not bot_found:
            await m.reply(REPLIES['plugins_devs_1226'])
        return
    
    if text == 'رجوع' and await is_dev(m.from_user.id, c):
        return await show_dev_panel(c, m, k, current_bot_id)

    game_meta = await get_public_game_meta(text)
    if game_meta:
        await handle_play_public_game(c, m, k, text)
        return
    
    button_game = await get_public_button_game_data(text)
    if button_game:
        await handle_play_public_button_game(c, m, k, text)
        return
    
    if text == '/start rules':
         await m.reply(text=REPLIES['plugins_devs_1279'],reply_markup=InlineKeyboardMarkup ([[InlineKeyboardButton (f"تحديثات {name}", url=f't.me/{channel}')]]))
    
    if text == '/start' and await is_dev(m.from_user.id, c):
        return await show_dev_panel(c, m, k, current_bot_id)
    
    if text == 'اضف حساب مساعد':
        return await add_assistant_account(c, m, k, current_bot_id)
    
    if await r.get(f'{m.chat.id}:addAssistant:{m.from_user.id}{current_bot_id}'):
        return await process_add_assistant(c, m, k, current_bot_id)
    
    if text == 'مسح حساب مساعد':
        return await remove_assistant_account(c, m, k, current_bot_id)
    
    if text.startswith(". "):
         text = text.split(None,1)[1]
         msg = await m.reply(REPLIES['plugins_devs_1360'], quote=True)
         try:
             await m.reply_chat_action(ChatAction.TYPING)
         except Exception as e:
             print(e)
         rep = await http_get_text(f"https://gptzaid.zaidbot.repl.co/1/text={text}")
         try:
             await m.reply_chat_action(ChatAction.TYPING)
         except Exception as e:
             print(e)
         await msg.edit(rep)
    
    if text == 'تحديث البوت':
        if not await is_dev2(m.from_user.id):
            return await m.reply(plugins_devs_1374(k))
        
        bot_owner = await r.get(f'{current_bot_id}botowner')
        if not bot_owner or int(bot_owner) != m.from_user.id:
            return await m.reply(plugins_devs_1378(k))
        
        await m.reply(plugins_devs_1380(k))
        
        success, message = await bot_manager.reload_bot(current_bot_id)
        
        if success:
            await m.reply(plugins_devs_1385(k))
        else:
            await m.reply(plugins_devs_1387(k, message))

@Client.on_message(filters.text, group=30)
async def sudosCommandsHandler(c, m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    current_bot_id = get_current_dev_final()
    r = get_redis()
    k = await r.get(f'{current_bot_id}:botkey')
    channel = await r.get(f'{current_bot_id}:BotChannel') if await r.get(f'{current_bot_id}:BotChannel') else ''
    await SudosCommandsFunc(c, m, k, r, channel, current_bot_id)

async def SudosCommandsFunc(c, m, k, r, channel, current_bot_id):
   r = get_global_r()
   Dev_FINAL = get_global_dev()
   if not k:
      k = await r.get(f'{current_bot_id}:botkey') or get_global_k()
   if not m.from_user:  return
   if await check_and_guard_locked_command(c, m, k, m.text or ''):
       return
   if not m.chat.type == ChatType.PRIVATE:
      if not await r.get(f'{m.chat.id}:enable:{current_bot_id}'):
        return
   else:
     if await r.get(f'{m.from_user.id}:sarhni'):  return 
   if await r.get(f'{m.from_user.id}:mute:{m.chat.id}{current_bot_id}'):  return 
   if await r.get(f'{m.chat.id}:mute:{current_bot_id}') and not await admin_pls(m.from_user.id, m.chat.id):  return
   if await r.get(f'{m.from_user.id}:mute:{current_bot_id}'):  return 
   
   if await r.get(f'{m.chat.id}addCustomG:{m.from_user.id}{current_bot_id}'):  return
   if await r.get(f'{m.chat.id}:addCustom:{m.from_user.id}{current_bot_id}'):  return 
   if await r.get(f'{m.chat.id}:delCustom:{m.from_user.id}{current_bot_id}') or await r.get(f'{m.chat.id}:delCustomG:{m.from_user.id}{current_bot_id}'):  return 
   text = m.text

   
   name = await r.get(f'{current_bot_id}:BotName') if await r.get(f'{current_bot_id}:BotName') else 'فاينل'
   if text.startswith(f'{name} '):
      text = text.replace(f'{name} ','')
   if await r.get(f'{m.chat.id}:Custom:{m.chat.id}{current_bot_id}&text={text}'):
       text = await r.get(f'{m.chat.id}:Custom:{m.chat.id}{current_bot_id}&text={text}')
   if await r.get(f'Custom:{current_bot_id}&text={text}'):
       text = await r.get(f'Custom:{current_bot_id}&text={text}')

   paid_step_key = f'{m.chat.id}:paidLockStep:{m.from_user.id}{current_bot_id}'
   paid_target_key = f'{m.chat.id}:paidLockTarget:{m.from_user.id}{current_bot_id}'
   paid_label_key = f'{m.chat.id}:paidLockLabel:{m.from_user.id}{current_bot_id}'
   paid_pending_key = f'PaidLockPending:{m.chat.id}:{m.from_user.id}:{current_bot_id}'
   paid_unlock_list_key = f'{m.chat.id}:paidUnlockList:{m.from_user.id}{current_bot_id}'

   paid_step = await r.get(paid_step_key)

   if paid_step and text.strip() == 'الغاء':
      await r.delete(paid_step_key)
      await r.delete(paid_target_key)
      await r.delete(paid_label_key)
      await r.delete(paid_unlock_list_key)
      await r.delete(paid_pending_key)
      await m.reply(f'{k} تم الالغاء')
      return

   if text.strip() in ('قفل خدمه', 'قفل خدمة') and await is_super_owner(m.from_user.id):
      await r.delete(paid_pending_key)
      await r.set(paid_step_key, 'lock_waiting_target', ex=900)
      await m.reply(f'{k} ارسل ايدي البوت او يوزره')
      return

   if text.strip() in ('فتح خدمه', 'فتح خدمة') and await is_super_owner(m.from_user.id):
      await r.set(paid_step_key, 'unlock_waiting_target', ex=900)
      await m.reply(f'{k} ارسل ايدي البوت او يوزره')
      return

   if paid_step == 'lock_waiting_target' and await is_super_owner(m.from_user.id):
      target_bot_id, target_label = await resolve_target_bot_id(c, text)
      if not target_bot_id:
         await m.reply(f'{k} تعذر تحديد البوت، ارسل ايدي رقمي صحيح او يوزر صحيح، او اكتب "الغاء"')
         return
      await r.set(paid_target_key, target_bot_id, ex=900)
      await r.set(paid_label_key, target_label, ex=900)
      await r.set(paid_step_key, 'lock_collecting', ex=900)
      await m.reply(
         f'{k} حسنا ارسل الخدمات التي تود قفلها\n'
         f'{k} يمكن ارسال اكثر من خدمه معا\n'
         f'{k} عند الانتهاء ارسل تم\n'
         f'{k} او للالغاء اكتب الغاء'
      )
      return

   if paid_step == 'lock_collecting' and await is_super_owner(m.from_user.id):
      target_bot_id = await r.get(paid_target_key)
      if not target_bot_id:
         await r.delete(paid_step_key)
         return

      if text.strip() == 'تم':
         pending = await r.smembers(paid_pending_key)
         if not pending:
            await m.reply(f'{k} لم يتم ارسال اي خدمة بعد، ارسل اسم الخدمة اولا او اكتب "الغاء"')
            return
         for service_name in pending:
            await register_bot_service(target_bot_id, service_name)
            await set_service_enabled(target_bot_id, service_name, False)
         await r.delete(paid_step_key)
         await r.delete(paid_target_key)
         await r.delete(paid_label_key)
         await r.delete(paid_pending_key)
         await m.reply(f'{k} تم حفظ قفل الخدمات')
         return

      lines = [line.strip() for line in text.splitlines() if line.strip()]
      if not lines:
         return
      await r.sadd(paid_pending_key, *lines)
      await r.expire(paid_pending_key, 900)
      return

   if paid_step == 'unlock_waiting_target' and await is_super_owner(m.from_user.id):
      target_bot_id, target_label = await resolve_target_bot_id(c, text)
      if not target_bot_id:
         await m.reply(f'{k} تعذر تحديد البوت، ارسل ايدي رقمي صحيح او يوزر صحيح، او اكتب "الغاء"')
         return

      lock_map = await get_bot_service_lock_map(target_bot_id)
      locked_names = [name for name, is_locked in lock_map.items() if is_locked]
      if not locked_names:
         await r.delete(paid_step_key)
         await m.reply(f'{k} لا توجد اي خدمة مقفولة حاليا لهذا البوت')
         return

      await r.set(paid_target_key, target_bot_id, ex=900)
      await r.set(paid_label_key, target_label, ex=900)
      await r.set(paid_unlock_list_key, '\n'.join(locked_names), ex=900)
      await r.set(paid_step_key, 'unlock_choosing', ex=900)

      txt = f'{k} الخدمات المقفوله للبوت #{target_label} هي :\n\n'
      for i, name in enumerate(locked_names, 1):
         txt += f'{i}. {name}\n'
      txt += (
         f'\n{k} اكتب رقما لفتح القفل\n'
         f'{k} يمكن تحديد اكثر من رقم برسالة واحدة\n'
         f'{k} كل رقم في سطر\n'
         f'{k} او اكتب الغاء'
      )
      await m.reply(txt)
      return

   if paid_step == 'unlock_choosing' and await is_super_owner(m.from_user.id):
      target_bot_id = await r.get(paid_target_key)
      stored_list = await r.get(paid_unlock_list_key)
      if not target_bot_id or not stored_list:
         await r.delete(paid_step_key)
         return

      locked_names = stored_list.split('\n')
      lines = [line.strip() for line in text.splitlines() if line.strip()]
      to_unlock = []
      for line in lines:
         if line.isdigit() and 1 <= int(line) <= len(locked_names):
            name = locked_names[int(line) - 1]
            if name not in to_unlock:
               to_unlock.append(name)

      if not to_unlock:
         await m.reply(f'{k} لم يتم تحديد اي رقم صحيح، حاول مجددا او اكتب "الغاء"')
         return

      for name in to_unlock:
         await set_service_enabled(target_bot_id, name, True)

      await r.delete(paid_step_key)
      await r.delete(paid_target_key)
      await r.delete(paid_label_key)
      await r.delete(paid_unlock_list_key)
      await m.reply(f'{k} تم فتح قفل الخدمات')
      return

   if (await r.get(f'{m.chat.id}:setBotName:{m.from_user.id}{current_bot_id}') or await r.get(f'{m.chat.id}:setBotChannel:{m.from_user.id}{current_bot_id}') or await r.get(f'{m.chat.id}:setBotKey:{m.from_user.id}{current_bot_id}') or await r.get(f'{m.chat.id}:setDevGroup:{m.from_user.id}{current_bot_id}') or await r.get(f'{m.chat.id}:setBotowmer:{m.from_user.id}{current_bot_id}')) and text == 'الغاء':
       await m.reply(quote=True,text=plugins_devs_1427(k))
       await r.delete(f'{m.chat.id}:setBotName:{m.from_user.id}{current_bot_id}')
       await r.delete(f'{m.chat.id}:setBotChannel:{m.from_user.id}{current_bot_id}')
       await r.delete(f'{m.chat.id}:setBotKey:{m.from_user.id}{current_bot_id}')
       await r.delete(f'{m.chat.id}:setDevGroup:{m.from_user.id}{current_bot_id}')
       return await r.delete(f'{m.chat.id}:setBotowmer:{m.from_user.id}{current_bot_id}')

   if await r.get(f'{m.chat.id}:setBotName:{m.from_user.id}{current_bot_id}'):
      if not await is_dev2(m.from_user.id):
         await r.delete(f'{m.chat.id}:setBotName:{m.from_user.id}{current_bot_id}')
         return await m.reply(quote=True,text=plugins_devs_1437(k))
      await r.delete(f'{m.chat.id}:setBotName:{m.from_user.id}{current_bot_id}')
      await r.set(f'{current_bot_id}:BotName', m.text)
      return await m.reply(quote=True,text=plugins_devs_1440(k, m.text))
   
   if await r.get(f'{m.chat.id}:setBotChannel:{m.from_user.id}{current_bot_id}'):
      if not await is_dev2(m.from_user.id):
         await r.delete(f'{m.chat.id}:setBotChannel:{m.from_user.id}{current_bot_id}')
         return await m.reply(quote=True,text=plugins_devs_1445(k))
      await r.delete(f'{m.chat.id}:setBotChannel:{m.from_user.id}{current_bot_id}')
      await r.set(f'{current_bot_id}:BotChannel', m.text.replace('@',''))
      return await m.reply(quote=True,text=plugins_devs_1448(k, m.text))
   
   if await r.get(f'{m.chat.id}:setBotKey:{m.from_user.id}{current_bot_id}'):
      if not await is_dev2(m.from_user.id):
         await r.delete(f'{m.chat.id}:setBotKey:{m.from_user.id}{current_bot_id}')
         return await m.reply(quote=True,text=plugins_devs_1453(k))
      await r.delete(f'{m.chat.id}:setBotKey:{m.from_user.id}{current_bot_id}')
      await r.set(f'{current_bot_id}:botkey', m.text)
      return await m.reply(quote=True,text=plugins_devs_1456(k, m.text))
      
   if await r.get(f'{m.chat.id}:setDevGroup:{m.from_user.id}{current_bot_id}'):
      if not await is_main_dev(m.from_user.id):
         await r.delete(f'{m.chat.id}:setDevGroup:{m.from_user.id}{current_bot_id}')
         return await m.reply(quote=True,text=plugins_devs_1461(k))
      await r.delete(f'{m.chat.id}:setDevGroup:{m.from_user.id}{current_bot_id}')
      try:
        id = int(m.text)
      except:
        return await m.reply(quote=True,text=plugins_devs_1466(k))
      await r.set(f'DevGroup:{current_bot_id}', int(m.text))
      return await m.reply(quote=True,text=plugins_devs_1468(k, m.text))
   
   if await r.get(f'{m.chat.id}:setBotowmer:{m.from_user.id}{current_bot_id}'):
      if not await is_super_owner(m.from_user.id):
         await r.delete(f'{m.chat.id}:setBotowmer:{m.from_user.id}{current_bot_id}')
         return await m.reply(quote=True,text=plugins_devs_1473(k))
      await r.delete(f'{m.chat.id}:setBotowmer:{m.from_user.id}{current_bot_id}')
      target_id = await resolve_user_id_from_arg(m.text)
      if not target_id:
        return await m.reply(quote=True,text=plugins_devs_1478(k))
      try:
        get = await c.get_users(target_id)
      except:
        return await m.reply(quote=True,text=plugins_devs_1478(k))
      await r.set(f'{current_bot_id}botowner', get.id)
      await m.reply(quote=True,text=plugins_devs_1480(k, m.text))
   
   if await r.get(f'{m.chat.id}:setContactReply:{m.from_user.id}{current_bot_id}'):
      if text == 'الغاء':
         await r.delete(f'{m.chat.id}:setContactReply:{m.from_user.id}{current_bot_id}')
         return await m.reply(quote=True, text=plugins_devs_1485(k))
      if not await is_dev(m.from_user.id, c):
         await r.delete(f'{m.chat.id}:setContactReply:{m.from_user.id}{current_bot_id}')
         return await m.reply(quote=True, text=plugins_devs_1488(k))
      await r.delete(f'{m.chat.id}:setContactReply:{m.from_user.id}{current_bot_id}')
      await r.set(f'ContactReplyText:{current_bot_id}', m.text)
      await m.reply(quote=True, text=plugins_devs_1491(k, m.text))
      return await show_contact_panel(c, m, k, current_bot_id)

   if text == 'الاحصائيات' or text == 'الإحصائيات':
      if not await is_main_dev(m.from_user.id):
         return await m.reply(quote=True,text=plugins_devs_1496(k))
      if not await r.smembers(f'{current_bot_id}:UsersList'):
         users = 0
      else:
         users = len(await r.smembers(f'{current_bot_id}:UsersList'))
      if not await r.smembers(f'enablelist:{current_bot_id}'):
         chats = 0
      else:
         chats = len(await r.smembers(f'enablelist:{current_bot_id}'))
      return await m.reply(quote=True,text=plugins_devs_1505(k, k, users, k, chats))
   
   if text == 'تفعيل البوت الخدمي':
      if not await is_main_dev(m.from_user.id):
         return await m.reply(quote=True,text=plugins_devs_1509(k))
      if not await r.get(f'DisableBot:{current_bot_id}'):
         return await m.reply(quote=True,text=plugins_devs_1511(k))
      else:
         await r.delete(f'DisableBot:{current_bot_id}')
         return await m.reply(quote=True,text=plugins_devs_1514(k))
   
   if text == 'تعطيل البوت الخدمي':
      if not await is_main_dev(m.from_user.id):
         return await m.reply(quote=True,text=plugins_devs_1518(k))
      if await r.get(f'DisableBot:{current_bot_id}'):
         return await m.reply(quote=True,text=plugins_devs_1520(k))
      else:
         await r.set(f'DisableBot:{current_bot_id}', 1)
         return await m.reply(quote=True,text=plugins_devs_1523(k))
   
   if text == 'تفعيل التحميل واليوتيوب':
      if not await is_main_dev(m.from_user.id):
         return await m.reply(quote=True,text=plugins_devs_1527(k))
      if not await r.get(f':disableYT:{current_bot_id}'):
         return await m.reply(quote=True,text=plugins_devs_1529(k))
      else:
         await r.delete(f':disableYT:{current_bot_id}')
         return await m.reply(quote=True,text=plugins_devs_1532(k))
   
   if text == 'تعطيل التحميل واليوتيوب':
      if not await is_main_dev(m.from_user.id):
         return await m.reply(quote=True,text=plugins_devs_1536(k))
      if await r.get(f':disableYT:{current_bot_id}'):
         return await m.reply(quote=True,text=plugins_devs_1538(k))
      else:
         await r.set(f':disableYT:{current_bot_id}', 1)
         return await m.reply(quote=True,text=plugins_devs_1541(k))
   
   if text == 'الردود العامه' and m.chat.type == ChatType.PRIVATE:
     if not await is_dev2(m.from_user.id):
        return await m.reply(quote=True,text=plugins_devs_1545(k))
     else:
      if not await r.smembers(f'FiltersList:{current_bot_id}'):
       return await m.reply(quote=True,text=plugins_devs_1548(k))
      else:
       text = 'ردود البوت:\n'
       count = 1
       for reply in await r.smembers(f'FiltersList:{current_bot_id}'):
          rep = reply
          type = await r.get(f'{rep}:filtertype:{current_bot_id}')
          text += f'\n{count} - ( {rep} ) ࿓ ( {type} )'
          count += 1
       text += '\n'
       return await m.reply(quote=True,text=text, disable_web_page_preview=True)
   
   if text == 'المستخدمين المحظورين' or text == 'المحظورين عام':
     if not await is_main_dev(m.from_user.id):
        return await m.reply(quote=True,text=plugins_devs_1562(k))
     else:
        if not await r.smembers(f'listGBAN:{current_bot_id}'):
           return await m.reply(quote=True,text=plugins_devs_1565(k))
        else:
           text = 'الحمير المحظورين عام:\n'
           count = 1
           for user in await r.smembers(f'listGBAN:{current_bot_id}'):
               try:
                  get = await c.get_users(int(user))
                  mention = '@'+get.username if get.username else get.mention()
                  id = get.id
               except:
                  mention = f'<a href="tg://user?id={int(user)}">{html.escape(str(int(user)))}</a>'
                  id = int(user)
               text += f'{count}) {mention} ~ ( `{id}` )\n'
               count += 1
           return await m.reply(quote=True,text=text)

   if text == 'مسح المحظورين عام':
     if not await is_dev(m.from_user.id, c):
        return await m.reply(quote=True,text=plugins_devs_1562(k))
     members = await r.smembers(f'listGBAN:{current_bot_id}')
     if not members:
        return await m.reply(quote=True,text=plugins_devs_1565(k))
     count = 0
     for user in members:
        await r.srem(f'listGBAN:{current_bot_id}', int(user))
        await r.delete(f'{int(user)}:gban:{current_bot_id}')
        count += 1
     return await m.reply(quote=True,text=f'{k} تم مسح {count} من المحظورين عام')

   if text == 'المكتومين عام':
     if not await is_main_dev(m.from_user.id):
        return await m.reply(quote=True,text=plugins_devs_1618(k))
     else:
        if not await r.smembers(f'listMUTE:{current_bot_id}'):
          return await m.reply(quote=True,text=plugins_devs_1621(k))
        else:
          text = '- المكتومين عام:\n\n'
          count = 1
          for PRE in await r.smembers(f'listMUTE:{current_bot_id}'):
             if count == 101: break
             try:
               user = await c.get_users(int(PRE))
               mention = user.mention()
               id = user.id
               username = user.username
               if user.username:
                 text += f'{count} ➣ @{username} ࿓ ( `{id}` )\n'
               else:
                 text += f'{count} ➣ {mention} ࿓ ( `{id}` )\n'
               count += 1
             except:
               mention = f'<a href="tg://user?id={int(PRE)}">@{html.escape(str(channel))}</a>'
               id = int(PRE)
               text += f'{count} ➣ {mention} ࿓ ( `{id}` )\n'
               count += 1
          text += '\n'
          return await m.reply(quote=True,text=text)

   if text == 'مسح المكتومين عام':
     if not await is_dev(m.from_user.id, c):
        return await m.reply(quote=True,text=plugins_devs_1618(k))
     members = await r.smembers(f'listMUTE:{current_bot_id}')
     if not members:
        return await m.reply(quote=True,text=plugins_devs_1621(k))
     count = 0
     for user in members:
        await r.srem(f'listMUTE:{current_bot_id}', int(user))
        await r.delete(f'{int(user)}:mute:{current_bot_id}')
        count += 1
     return await m.reply(quote=True,text=f'{k} تم مسح {count} من المكتومين عام')

   if text == 'أوامر الحظر والكتم':
     if not await is_dev(m.from_user.id, c):
        return await m.reply(quote=True,text=plugins_devs_1562(k))
     reply_markup = ReplyKeyboardMarkup(
        [
           ['المحظورين عام', 'مسح المحظورين عام'],
           ['المكتومين عام', 'مسح المكتومين عام'],
           ['العودة'],
        ],
        resize_keyboard=True
     )
     return await m.reply(quote=True,text=f'{k} اختر ما تريد من ازرار الحظر والكتم العام',reply_markup=reply_markup)

   if text == 'المحظورين من الالعاب':
     if not await is_main_dev(m.from_user.id):
        return await m.reply(quote=True,text=plugins_devs_1583(k))
     else:
        if not await r.smembers(f'listGBANGAMES:{current_bot_id}'):
           return await m.reply(quote=True,text=plugins_devs_1586(k))
        else:
           text = 'الحمير المحظورين عام من الالعاب:\n'
           count = 1
           for user in await r.smembers(f'listGBANGAMES:{current_bot_id}'):
               try:
                  get = await c.get_users(int(user))
                  mention = '@'+get.username if get.username else get.mention()
                  id = get.id
               except:
                  mention = f'<a href="tg://user?id={int(user)}">{html.escape(str(int(user)))}</a>'
                  id = int(user)
               text += f'{count}) {mention} ~ ( `{id}` )\n'
               count += 1
           return await m.reply(quote=True,text=text)
   
   if text == 'المجموعات المحظورة':
     if not await is_main_dev(m.from_user.id):
        return await m.reply(quote=True,text=plugins_devs_1604(k))
     else:
        if not await r.smembers(f':BannedChats:{current_bot_id}'):
           return await m.reply(quote=True,text=plugins_devs_1607(k))
        else:
           text = 'المجموعات المحظورة عام:\n'
           count = 1
           for user in await r.smembers(f':BannedChats:{current_bot_id}'):
               text += f'{count}) {user}\n'
               count += 1
           return await m.reply(quote=True,text=text)
   

   if text == 'رمز السورس':
     if not await is_dev2(m.from_user.id):
        return await m.reply(quote=True,text=plugins_devs_1647(k))
     return await m.reply(quote=True,text=plugins_devs_1648(k))
   
   if text == 'قناة السورس':
     if not await is_dev2(m.from_user.id):
        return await m.reply(quote=True,text=plugins_devs_1652(k))
     if not await r.get(f'{current_bot_id}:BotChannel'):
       return await m.reply(quote=True,text=plugins_devs_1654(k))
     else:
       cha = await r.get(f'{current_bot_id}:BotChannel')
       return await m.reply(quote=True,text=plugins_devs_1657(cha))
   
   if text == 'اسم البوت':
     if not await is_dev2(m.from_user.id):
        return await m.reply(quote=True,text=plugins_devs_1661(k))
     if not await r.get(f'{current_bot_id}:BotName'):
       return await m.reply(quote=True,text=plugins_devs_1663(k))
     else:
       name = await r.get(f'{current_bot_id}:BotName')
       return await m.reply(quote=True,text=name)
   
   if text == 'مجموعة المطور' and m.chat.type == ChatType.PRIVATE:
     if not await is_dev(m.from_user.id):
        return await m.reply(quote=True,text=plugins_devs_1670(k))
     else:
        if not await r.get(f'DevGroup:{current_bot_id}'):
           return await m.reply(quote=True,text=plugins_devs_1673(k))
        else:
           id = int((await r.get(f'DevGroup:{current_bot_id}')) or 0)
           link = (await c.get_chat(id)).invite_link
           return await m.reply(quote=True,text=link, protect_content=True)
   
   if text == 'تعيين اسم البوت' or text == 'ضع اسم البوت':
     if not await is_dev2(m.from_user.id):
        return await m.reply(quote=True,text=plugins_devs_1681(k))
     await r.set(f'{m.chat.id}:setBotName:{m.from_user.id}{current_bot_id}', 1, ex=600)
     return await m.reply(quote=True,text=plugins_devs_1683(k))
   
   if text == 'مسح اسم البوت':
     if not await is_dev2(m.from_user.id):
        return await m.reply(quote=True,text=plugins_devs_1687(k))
     await r.delete(f'{current_bot_id}:BotName')
     return await m.reply(quote=True,text=plugins_devs_1689(k))
   
   if text == 'وضع قناة السورس':
     if not await is_dev2(m.from_user.id):
        return await m.reply(quote=True,text=plugins_devs_1693(k))
     await r.set(f'{m.chat.id}:setBotChannel:{m.from_user.id}{current_bot_id}', 1, ex=600)
     return await m.reply(quote=True,text=plugins_devs_1695(k))
   
   if text == 'مسح قناة السورس':
     if not await is_dev2(m.from_user.id):
        return await m.reply(quote=True,text=plugins_devs_1699(k))
     await r.delete(f'{current_bot_id}:BotChannel')
     return await m.reply(quote=True,text=plugins_devs_1701(k))
   
   if text == 'وضع رمز السورس' or text == 'ضع رمز السورس':
     if not await is_dev2(m.from_user.id):
        return await m.reply(quote=True,text=plugins_devs_1705(k))
     await r.set(f'{m.chat.id}:setBotKey:{m.from_user.id}{current_bot_id}', 1, ex=600)
     return await m.reply(quote=True,text=plugins_devs_1707(k))
   
   if text == 'مسح رمز السورس':
     if not await is_dev2(m.from_user.id):
        return await m.reply(quote=True,text=plugins_devs_1711(k))
     await r.set(f'{current_bot_id}:botkey', '⇜')
     return await m.reply(quote=True,text=plugins_devs_1713(k))
   
   if text == 'وضع مجموعة المطور':
     if not await is_main_dev(m.from_user.id):
        return await m.reply(quote=True,text=plugins_devs_1717(k))
     await r.set(f'{m.chat.id}:setDevGroup:{m.from_user.id}{current_bot_id}', 1, ex=600)
     return await m.reply(quote=True,text=plugins_devs_1719(k))
   
   if text == 'مسح مجموعة المطور':
     if not await is_main_dev(m.from_user.id):
        return await m.reply(quote=True,text=plugins_devs_1723(k))
     await r.delete(f'DevGroup:{current_bot_id}')
     return await m.reply(quote=True,text=plugins_devs_1725(k))
   
   if text == 'تغيير المطور الاساسي':
     if not await is_super_owner(m.from_user.id):
        return await m.reply(quote=True,text=plugins_devs_1729(k))
     else:
        await r.set(f'{m.chat.id}:setBotowmer:{m.from_user.id}{current_bot_id}', 1, ex=600)
        return await m.reply(quote=True,text=plugins_devs_1732(k))

   if text == 'تعطيل ربط القنوات':
       if not await is_dev(m.from_user.id, c):
           return await m.reply(quote=True, text=plugins_devs_1736(k))
       
       await r.set(f'disable_channel_handling:{current_bot_id}', '1')
       return await m.reply(quote=True, text=plugins_devs_1739(k))

   if text == 'تفعيل ربط القنوات':
       if not await is_dev(m.from_user.id, c):
           return await m.reply(quote=True, text=plugins_devs_1743(k))
       
       await r.delete(f'disable_channel_handling:{current_bot_id}')
       return await m.reply(quote=True, text=plugins_devs_1746(k))

   if text == 'تحديث':
     if not await is_super_owner(m.from_user.id):
        return await m.reply(quote=True,text=plugins_devs_1750(k))
     await m.reply(quote=True,text=plugins_devs_1751(k))
     python = sys.executable
     os.execl(python, python, *sys.argv)
   
   if text == 'الملفات':
     if not await is_super_owner(m.from_user.id):
        return await m.reply(quote=True,text=plugins_devs_1757(k))
     text = '——— ملفات السورس ———'
     a = os.listdir('plugins')
     a.sort()
     count = 1
     for file in a:
       if file.endswith('.py'):
         text += f'\n{count}) `{file}`'
         count += 1
     text += f'\n——— @{channel} ———'
     return await m.reply(quote=True,text=text, disable_web_page_preview=True)

   if text in ('نسخة عامة', 'نسخة الميوزك', 'نسخة خاصة'):
     if not await is_super_owner(m.from_user.id):
        return await m.reply(quote=True,text=plugins_devs_1771(k))

     try:
        import zipfile
        import shutil
        import tempfile
        from helpers.redis import export_all, export_bot, export_music_cache

        if text == 'نسخة عامة':
            label = 'النسخة العامة المشتركة'
            file_stub = 'redis_backup_all'
            export_coro = export_all()
        elif text == 'نسخة الميوزك':
            label = 'نسخة الميوزك المشتركة'
            file_stub = 'redis_backup_music'
            export_coro = export_music_cache()
        else:
            label = f'النسخة الخاصة بالبوت {current_bot_id}'
            file_stub = f'redis_backup_bot_{current_bot_id}'
            export_coro = export_bot(current_bot_id)

        status_msg = await m.reply(plugins_devs_1792(k, label))

        data = await export_coro

        if not data:
            await status_msg.edit(f'{k} لا توجد بيانات لتصديرها ({label})')
            return

        from zoneinfo import ZoneInfo
        baghdad_tz = ZoneInfo('Asia/Baghdad')
        current_time = datetime.now(baghdad_tz).strftime("%Y-%m-%d %H:%M")

        temp_dir = tempfile.mkdtemp()
        json_path = os.path.join(temp_dir, f"{file_stub}.json")
        zip_path = os.path.join(temp_dir, f"{file_stub}.zip")

        with open(json_path, 'w', encoding='utf-8') as jf:
            json.dump(data, jf, ensure_ascii=False, indent=2)

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(json_path, os.path.basename(json_path))

        file_size = os.path.getsize(zip_path)
        size_mb = file_size / (1024 * 1024)

        await status_msg.edit(f'{k} جاري رفع {label}...\n{k} عدد المفاتيح: {len(data)}\n{k} الحجم: {size_mb:.2f} ميجابايت')

        await m.reply_document(
            document=zip_path,
            caption=f'{k} {label}\n{k} عدد المفاتيح: {len(data)}\n{k} الحجم: {size_mb:.2f} ميجابايت\n{k} التاريخ: {current_time}'
        )

        try:
            shutil.rmtree(temp_dir)
        except:
            pass

        await status_msg.delete()

     except Exception as e:
        await m.reply(plugins_devs_1832(k, str(e)))
        import traceback
        traceback.print_exc()

   if text in ('اذاعة بالخاص', 'اذاعة بالخاص تثبيت'):
      if not await is_main_dev(m.from_user.id):
         return await m.reply(quote=True,text=plugins_devs_1838(k))
      pin = '1' if text.endswith('تثبيت') else '0'
      await r.delete(f'{m.chat.id}:gpBroadcast:{m.from_user.id}{current_bot_id}')
      await r.set(f'{m.chat.id}:pvBroadcast:{m.from_user.id}{current_bot_id}', pin, ex=300)
      return await m.reply(plugins_devs_1842(k, k, k))

   if text in ('اذاعة بالمجموعات', 'اذاعة بالقروبات', 'اذاعة بالمجموعات تثبيت'):
      if not await is_main_dev(m.from_user.id):
         return await m.reply(quote=True,text=plugins_devs_1846(k))
      pin = '1' if text.endswith('تثبيت') else '0'
      await r.delete(f'{m.chat.id}:pvBroadcast:{m.from_user.id}{current_bot_id}')
      await r.set(f'{m.chat.id}:gpBroadcast:{m.from_user.id}{current_bot_id}', pin, ex=300)
      return await m.reply(plugins_devs_1850(k, k, k))
   
   if text == 'السيرفر' or text == 'معلومات السيرفر':
     if not await is_super_owner(m.from_user.id):
        return await m.reply(quote=True,text=plugins_devs_1854(k))
     text = '——— SYSTEM INFO ———'
     uname = platform.uname()
     try:
         import lsb_release
         version = lsb_release.get_distro_information()['DESCRIPTION']
     except:
         version = "Unknown"
     text += f"\n{k} النظام : {uname.system}"
     text += f"\n{k} الاصدار: `{version}`"
     text += '\n——— R.A.M INFO ———'
     svmem = psutil.virtual_memory()
     text += f"\n{k} رامات السيرفر: ` {get_size(svmem.total)}`"
     text += f"\n{k} المستهلك: ` {get_size(svmem.used)}/{get_size(svmem.available)}`"
     text += f"\n{k} نسبة الاستهلاك: `{svmem.percent}%`"
     text += '\n——— HARD DISK ———'
     hard = psutil.disk_partitions()[0]
     usage = psutil.disk_usage(hard.mountpoint)
     text += f"\n{k} ذاكرة التخزين: `{get_size(usage.total)}`"
     text += f"\n{k} المستهلك: `{get_size(usage.used)}`"
     text += f"\n{k} نسبة الاستهلاك: `{usage.percent}%`"
     text += '\n——— U.P T.I.M.E ———'
     uptime = time.strftime('%dD - %HH - %MM - %Ss', time.gmtime(time.time() - psutil.boot_time()))
     text += f'\n{uptime}'
     text += '\n\n༄'
     return await m.reply(quote=True,text=text, disable_web_page_preview=True)
   
   if text == 'جلب نسخة القروبات':
      if not await is_super_owner(m.from_user.id):
        return await m.reply(quote=True,text=plugins_devs_1883(k))
      lst = []
      for chat in await r.smembers(f'enablelist:{current_bot_id}'):
         lst.append(int(chat))
      with open('chats_backup.json', 'w+') as w:
         w.write(json.dumps({"botUsername": bot_username,"botID":c.id,"Chats":lst},indent=4,ensure_ascii=False))
      await m.reply_document('chats_backup.json',quote=True)
      os.remove('chats_backup.json')
   
   if text == 'جلب نسخة المستخدمين':
      if not await is_super_owner(m.from_user.id):
        return await m.reply(quote=True,text=plugins_devs_1894(k))
      lst = []
      for chat in await r.smembers(f'{current_bot_id}:UsersList'):
         lst.append(int(chat))
      with open('users_backup.json', 'w+') as w:
         w.write(json.dumps({"botUsername": bot_username,"botID":c.id,"Users":lst},indent=4,ensure_ascii=False))
      await m.reply_document('users_backup.json',quote=True)
      os.remove('users_backup.json')

   if text.startswith('رابط ') and await is_main_dev(m.from_user.id):
     try:
        id = int(text.split()[1])
        gg = await c.get_chat(id)
        await m.reply(quote=True,text=plugins_devs_1907(gg.title, gg.invite_link),disable_web_page_preview=True)
     except Exception as e:
        print (e)

   if text == 'نقل الالعاب العامة' or text == 'العاب عامة':
       if not await is_public_game_admin(m.from_user.id):
           return await m.reply(plugins_devs_1913(k))
       
       categories = await get_public_categories()
       if not categories:
           return await m.reply(plugins_devs_1917(k))
       
       txt = f'{k} قائمة الالعاب العامة:\n\n'
       for cat, games in categories.items():
           if cat == 'الرئيسية':
               txt += f'الالعاب في القائمة الرئيسية:\n'
           else:
               txt += f'•• {cat}:\n'
           for game in games:
               txt += f'  • {game}\n'
           txt += '\n'
       
       txt += f'\n{k} لتنقل لعبة اكتب:\n`نقل / اسم اللعبة` للقائمة الرئيسية\n`نقل / اسم اللعبة / اسم الفئة` لنقلها لفئة معينة'
       await m.reply(txt)
       return True

   if text.startswith('نقل /'):
       if not await is_public_game_admin(m.from_user.id):
           return await m.reply(plugins_devs_1935(k))
       
       parts = text.split('/')
       parts = [p.strip() for p in parts if p.strip()]
       
       if len(parts) < 2:
           return await m.reply(plugins_devs_1941(k))
       
       game_name = parts[1]
       category_name = parts[2] if len(parts) > 2 else 'الرئيسية'
       
       game_exists = await get_public_game_meta(game_name) or await get_public_button_game_data(game_name)
       if not game_exists:
           return await m.reply(plugins_devs_1948(k, game_name))
       
       success = await move_game_to_category(game_name, category_name)
       if success:
           await m.reply(plugins_devs_1952(k, game_name, category_name))
       else:
           await m.reply(plugins_devs_1954(k))
       return True

   if text == 'عرض الفئات':
       if not await is_public_game_admin(m.from_user.id):
           return await m.reply(plugins_devs_1959(k))
       
       categories = await get_public_categories()
       txt = f'{k} الفئات الموجودة:\n\n'
       for cat, games in categories.items():
           if cat == 'الرئيسية':
               txt += f'القائمة الرئيسية ({len(games)} لعبة):\n'
           else:
               txt += f'•• {cat} ({len(games)} لعبة):\n'
           for game in games:
               txt += f'  • {game}\n'
           txt += '\n'
       
       await m.reply(txt)
       return True

@Client.on_message(filters.private, group=29)
async def broadcast_catcher(c, m):
    r = get_global_r()
    if not m.from_user:
        return

    current_bot_id = get_current_dev_final()
    if not current_bot_id:
        return

    pv_flag = await r.get(f'{m.chat.id}:pvBroadcast:{m.from_user.id}{current_bot_id}')
    gp_flag = await r.get(f'{m.chat.id}:gpBroadcast:{m.from_user.id}{current_bot_id}')

    if not pv_flag and not gp_flag:
        return

    k = await r.get(f'{current_bot_id}:botkey') or '•'

    if not await is_main_dev(m.from_user.id, c):
        await r.delete(f'{m.chat.id}:pvBroadcast:{m.from_user.id}{current_bot_id}')
        await r.delete(f'{m.chat.id}:gpBroadcast:{m.from_user.id}{current_bot_id}')
        return

    if m.text and m.text.strip() == 'الغاء':
        await r.delete(f'{m.chat.id}:pvBroadcast:{m.from_user.id}{current_bot_id}')
        await r.delete(f'{m.chat.id}:gpBroadcast:{m.from_user.id}{current_bot_id}')
        return await m.reply(plugins_devs_2001(k))

    if pv_flag:
        await r.delete(f'{m.chat.id}:pvBroadcast:{m.from_user.id}{current_bot_id}')
        return await execute_broadcast(c, m, k, current_bot_id, 'pv', pv_flag == '1')

    if gp_flag:
        await r.delete(f'{m.chat.id}:gpBroadcast:{m.from_user.id}{current_bot_id}')
        return await execute_broadcast(c, m, k, current_bot_id, 'gp', gp_flag == '1')

@Client.on_message(filters.private, group=-999999)
async def contact_flow_boundary_snapshot(c, m):
    if not m.from_user:
        return
    current_bot_id = get_current_dev_final()
    if not current_bot_id:
        return
    r = get_global_r()
    reserved = bool(
        await r.get(f"{current_bot_id}:guess_pending:{m.from_user.id}")
        or await _has_whisper_pending(r, current_bot_id, m.from_user.id)
    )
    if reserved:
        await r.set(f"{current_bot_id}:ContactFlowSkip:{m.from_user.id}:{m.id}", 1, ex=15)

@Client.on_message(filters.private, group=120)
async def contact_relay_handler(c, m):
    r = get_global_r()
    if not m.from_user:
        return

    current_bot_id = get_current_dev_final()
    if not current_bot_id:
        return

    if await is_dev(m.from_user.id, c):
        return

    if not await r.get(f'ContactEnabled:{current_bot_id}'):
        return

    if await r.sismember(f'ContactBanned:{current_bot_id}', m.from_user.id):
        return

    text = m.text or ''
    name = await r.get(f'{current_bot_id}:BotName') or 'فاينل'

    if text.startswith('/'):
        return
    if (
        text == 'رجوع'
        or text.startswith('•• ')
        or text == 'ضيفني لـ مجموعتك'
        or text == f'تحديثات {name}'
        or text == 'القائمة الرئيسية'
    ):
        return

    if text.startswith('w_'):
        return
    if await _has_whisper_pending(r, current_bot_id, m.from_user.id):
        return

    if 'sarhni' in text:
        return
    if await r.get(f'{m.from_user.id}:sarhni') or await r.get(f'{m.from_user.id}:sarhnirep'):
        return

    if text and (await get_public_game_meta(text) or await get_public_button_game_data(text)):
        return
    if await r.get(f"{current_bot_id}:guess_pending:{m.from_user.id}"):
        return

    contact_skip_flag = f"{current_bot_id}:ContactFlowSkip:{m.from_user.id}:{m.id}"
    if await r.get(contact_skip_flag):
        await r.delete(contact_skip_flag)
        return

    if await r.get(f"{m.from_user.id}:cleeshe_state:{current_bot_id}"):
        return

    k = await r.get(f'{current_bot_id}:botkey') or '•'
    username = f'@{m.from_user.username}' if m.from_user.username else 'ماعنده يوزر'

    intro_key = f'ContactIntroSent:{current_bot_id}:{m.from_user.id}'
    intro_already_sent = await r.get(intro_key)

    header = (
        f"{k} رسالة جديدة من مستخدم\n\n"
        f"الاسم: {m.from_user.mention()}\n"
        f"المعرف: {username}\n"
        f"الايدي: `{m.from_user.id}`\n\n"
        f"الرد على هذه الرسالة لترد عليه\n"
        f"ارسل 'حظر' لحظر المستخدم\n"
        f"ارسل 'سماح' لالغاء حظر المستخدم"
    )

    targets = await get_contact_targets(current_bot_id)
    sent_any = False

    for target in targets:
        try:
            if not intro_already_sent:
                info_msg = await c.send_message(target, header)
                await r.set(f'ContactMap:{current_bot_id}:{target}:{info_msg.id}', m.from_user.id, ex=2592000)

            fwd_msg = await m.forward(target)
            await r.set(f'ContactMap:{current_bot_id}:{target}:{fwd_msg.id}', m.from_user.id, ex=2592000)

            sent_any = True
        except Exception as e:
            print(f"Contact relay error: {e}")

    if sent_any:
        if not intro_already_sent:
            await r.set(intro_key, '1', ex=86400)
        
        if await r.get(f'ContactRepliesEnabled:{current_bot_id}'):
            reply_text = await r.get(f'ContactReplyText:{current_bot_id}') or DEFAULT_CONTACT_REPLY
            try:
                await m.reply(plugins_devs_2079(k, reply_text))
            except Exception:
                pass

@Client.on_message(filters.private & filters.reply, group=121)
async def contact_dev_reply_handler(c, m):
    r = get_global_r()
    if not m.from_user:
        return

    current_bot_id = get_current_dev_final()
    if not current_bot_id:
        return

    if not await is_dev(m.from_user.id, c):
        return

    if not m.reply_to_message:
        return

    target_user = await r.get(f'ContactMap:{current_bot_id}:{m.chat.id}:{m.reply_to_message.id}')
    if not target_user:
        return

    target_user = int(target_user)
    k = await r.get(f'{current_bot_id}:botkey') or '•'
    text = (m.text or '').strip()

    if text == 'حظر':
        await r.sadd(f'ContactBanned:{current_bot_id}', target_user)
        return await m.reply(plugins_devs_2109(k, target_user))

    if text == 'سماح':
        await r.srem(f'ContactBanned:{current_bot_id}', target_user)
        return await m.reply(plugins_devs_2113(k, target_user))

    try:
        sent = await m.copy(chat_id=target_user)
        await r.set(f'ContactMap:{current_bot_id}:{m.chat.id}:{m.id}', target_user, ex=2592000)
        return await m.reply(plugins_devs_2118(k))
    except Exception as e:
        return await m.reply(plugins_devs_2120(k))

@Client.on_callback_query(filters.regex(r"^(remove_assistant_|cancel_remove_assistant_)"), group=-166)
async def assistant_callback_handler(c, callback_query):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    data = callback_query.data
    
    if data.startswith("remove_assistant_"):
        parts = data.split("_")
        assistant_num = int(parts[2])
        current_bot_id = parts[3]
        k = await r.get(f'{current_bot_id}:botkey') or '•'
        
        if callback_query.message is not None:
            await remove_assistant_account(c, callback_query.message, k, current_bot_id)
        await callback_query.answer()
    
    elif data.startswith("cancel_remove_assistant_"):
        await callback_query.message.delete()
        await callback_query.answer(REPLIES['plugins_devs_2140'])

async def aexec(code, client, message):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {a}" for a in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)