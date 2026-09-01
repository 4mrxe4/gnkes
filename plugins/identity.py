import html
# في بداية ملف identity.py
from helpers.context import get_global_r, get_global_dev, get_global_k
r = get_global_r()
Dev_FINAL = get_global_dev()
k = get_global_k()
import random, re, time, os, asyncio, json
from helpers.http import telegram_api_post
from helpers.emoji import render_custom_emoji_entities
from threading import Thread
from compat import *
from compat import filters
from helpers.ranks import *
from helpers.creation import get_creation_date
from io import BytesIO
import settings
from compat import FileId, FileType, ThumbnailSource
from .protect import get_emoji_bank, claim_event_once, update_chat_title_cache, record_group_interaction, GLOBAL_TOP_NS
from helpers.redis import r as _shared_r
from helpers.redis import cache_username_id, get_cached_username_id
from plugins.games.utils import is_owner_only
from helpers.ranks import *
from .buttons import register_buttons, get_button_custom, get_button_color, create_button_raw
from helpers.replies_store import (
    REPLIES,
    plugins_identity_1131,
    plugins_identity_1132,
    plugins_identity_1134,
    plugins_identity_1171,
    plugins_identity_1172,
    plugins_identity_1174,
    plugins_identity_1202,
    plugins_identity_1207,
    plugins_identity_1221,
    plugins_identity_1227,
    plugins_identity_1238,
    plugins_identity_1244,
    plugins_identity_1246,
    plugins_identity_1248,
    plugins_identity_1254,
    plugins_identity_1256,
    plugins_identity_1258,
    plugins_identity_1265,
    plugins_identity_1268,
    plugins_identity_1274,
    plugins_identity_1277,
    plugins_identity_1281,
    plugins_identity_1283,
    plugins_identity_1285,
    plugins_identity_1289,
    plugins_identity_1293,
    plugins_identity_1295,
    plugins_identity_1297,
    plugins_identity_1324,
    plugins_identity_1350,
    plugins_identity_1352,
    plugins_identity_1354,
    plugins_identity_1358,
    plugins_identity_1360,
    plugins_identity_1362,
    plugins_identity_1366,
    plugins_identity_1368,
    plugins_identity_1372,
    plugins_identity_1374,
    plugins_identity_1379,
    plugins_identity_1381,
    plugins_identity_1386,
    plugins_identity_1388,
    plugins_identity_1392,
    plugins_identity_1394,
    plugins_identity_1396,
    plugins_identity_1400,
    plugins_identity_1402,
    plugins_identity_1404,
    plugins_identity_1408,
    plugins_identity_1421,
    plugins_identity_1425,
    plugins_identity_1432,
    plugins_identity_1448,
    plugins_identity_1453,
    plugins_identity_1460,
    plugins_identity_1468,
    plugins_identity_1470,
    plugins_identity_1487,
    plugins_identity_1494,
    plugins_identity_1500,
    plugins_identity_1502,
    plugins_identity_1517,
    plugins_identity_1520,
    plugins_identity_1523,
    plugins_identity_1527,
    plugins_identity_1530,
    plugins_identity_1533,
    plugins_identity_1537,
    plugins_identity_1540,
    plugins_identity_1543,
    plugins_identity_1547,
    plugins_identity_1550,
    plugins_identity_1553,
    plugins_identity_1557,
    plugins_identity_1560,
    plugins_identity_1563,
    plugins_identity_1567,
    plugins_identity_1570,
    plugins_identity_1573,
    plugins_identity_1577,
    plugins_identity_1579,
    plugins_identity_1581,
    plugins_identity_1585,
    plugins_identity_1587,
    plugins_identity_1589,
    plugins_identity_1593,
    plugins_identity_1595,
    plugins_identity_1597,
    plugins_identity_1601,
    plugins_identity_1603,
    plugins_identity_1605,
    plugins_identity_1610,
    plugins_identity_1612,
    plugins_identity_1615,
    plugins_identity_1623,
    plugins_identity_499,
    plugins_identity_501,
    plugins_identity_507,
    plugins_identity_509,
    plugins_identity_513,
    plugins_identity_516,
    plugins_identity_520,
    plugins_identity_524,
    plugins_identity_528,
    plugins_identity_582,
    plugins_identity_584,
    plugins_identity_590,
    plugins_identity_592,
    plugins_identity_628,
    plugins_identity_637,
    plugins_identity_658,
    plugins_identity_673,
    plugins_identity_705,
    plugins_identity_707,
    plugins_identity_709,
    plugins_identity_714,
    plugins_identity_718,
    plugins_identity_721,
    plugins_identity_725,
    plugins_identity_727,
    plugins_identity_731,
    plugins_identity_735,
    plugins_identity_769,
    plugins_identity_774,
    plugins_identity_780,
    plugins_identity_786,
    plugins_identity_791,
    plugins_identity_795,
    plugins_identity_806,
    plugins_identity_823,
    plugins_identity_888,
    plugins_identity_907,
    plugins_identity_921,
    plugins_identity_934,
    plugins_identity_936,
    plugins_identity_938,
    plugins_identity_942,
    plugins_identity_944,
    plugins_identity_946,
    plugins_identity_991,
)


BUTTONS_DEFINITIONS = {
    "id": {
        "name": "أزرار الايدي",
        "buttons": [
            {"id": "like_btn", "default": "❤️"},
            {"id": "dislike_btn", "default": "💔"},
        ]
    }
}

register_buttons(BUTTONS_DEFINITIONS)

id_reactions = {}
user_id_messages = {}


async def get_parent_userbot_client():
    """
    ترجع عميل الحساب المساعد (Userbot/Pyrogram) الخاص بالبوت الأب حصراً —
    بغض النظر عن كون البوت الذي يستدعي هذه الدالة هو الأب نفسه أو أي بوت
    فرعي بالكلاستر.

    السبب: كل بوت بالمشروع يملك كائن Userbot خاصاً به منفصلاً تماماً
    (_bot_contexts[bot_id]['userbot']، عبر بروكسي plugins.FinalMusic.userbot
    الذي يتبع سياق البوت الحالي). جلسة الحساب المساعد الفعلية مسجَّلة فقط
    عند بوت الأب، فبوت فرعي يستدعي get_real_pyro_client() العادية يحاول
    تشغيل نسخته الخاصة التي لا تملك أي جلسة أصلاً — فتفشل بصمت دائماً.

    هنا نبحث صراحة عن سياق البوت المعلَّم is_parent=True داخل _bot_contexts
    (يُضبط مرة واحدة عند إقلاع الأب في entry.py ولا يتغيّر)، ونستخدم عميل
    الـ Userbot الخاص بذلك السياق تحديداً، ونُشغّله (إن لم يكن مُشغَّلاً)
    تحت سياق الأب نفسه مؤقتاً لضمان قراءة جلسته الصحيحة، دون أي مساس
    بكائن الـ Userbot الخاص بالبوت المستدعي نفسه أو بأي شيء يخص الموسيقى.
    """
    try:
        from helpers.context import _bot_contexts, get_current_bot_id, set_current_bot_id
    except Exception:
        return None

    parent_bot_id = None
    parent_ctx = None
    for bid, ctx in list(_bot_contexts.items()):
        if ctx.get('is_parent'):
            parent_bot_id = bid
            parent_ctx = ctx
            break

    if not parent_ctx:
        return None

    parent_userbot = parent_ctx.get('userbot')
    if parent_userbot is None:
        return None

    if parent_userbot.clients:
        return parent_userbot.one or parent_userbot.clients[0]

    old_bot_id = get_current_bot_id()
    try:
        set_current_bot_id(parent_bot_id)
        await parent_userbot.boot()
    except Exception:
        pass
    finally:
        if old_bot_id:
            set_current_bot_id(old_bot_id)

    return parent_userbot.one or (parent_userbot.clients[0] if parent_userbot.clients else None)


async def get_user_reactions(user_id):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    key = f'global_reactions:{user_id}'
    data = await r.get(key)
    if data:
        try:
            loaded_data = json.loads(data)
            return set(loaded_data.get('likes', [])), set(loaded_data.get('dislikes', []))
        except json.JSONDecodeError:
            return set(), set()
    return set(), set()


async def save_user_reactions(user_id, likes_set, dislikes_set):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    key = f'global_reactions:{user_id}'
    data = {
        'likes': list(likes_set),
        'dislikes': list(dislikes_set)
    }
    await r.set(key, json.dumps(data))


async def get_user_like_emoji(user_id):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    emoji = await r.get(f'{user_id}:like_emoji:{Dev_FINAL}')
    if not emoji:
        return '❤️'
    return emoji


async def get_user_dislike_emoji(user_id):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    emoji = await r.get(f'{user_id}:dislike_emoji:{Dev_FINAL}')
    if not emoji:
        return '💔'
    return emoji


async def get_user_global_likes(user_id):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    count = await r.get(f'{user_id}:global_likes:{Dev_FINAL}')
    return int(count) if count else 0


async def get_user_global_dislikes(user_id):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    count = await r.get(f'{user_id}:global_dislikes:{Dev_FINAL}')
    return int(count) if count else 0


async def increment_user_global_likes(user_id):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    count = await get_user_global_likes(user_id)
    await r.set(f'{user_id}:global_likes:{Dev_FINAL}', count + 1)
    return count + 1


def _is_valid_reaction_emoji(s: str) -> bool:
    """يتحقق من أن النص المُدخل إيموجي صالح لتعيينه كلايك/دسلايك.
    يعتمد أولاً على مكتبة emoji، وإن لم تتعرف عليه (بسبب قِدَم قاعدة بياناتها
    مقارنة بإيموجي حديثة مثل 🫦 المُضاف في يونيكود 14) يرجع لتحقق احتياطي
    عبر نطاقات يونيكود الرسمية للإيموجي بدل رفضه خطأً."""
    if not s or len(s) > 8:
        return False
    try:
        import emoji as emoji_lib
        if emoji_lib.is_emoji(s):
            return True
    except Exception:
        pass
    import unicodedata
    return all(
        unicodedata.category(ch) in ('So', 'Sk')
        or 0x1F000 <= ord(ch) <= 0x1FFFF
        or ch in ('\u2764', '\uFE0F', '\u200D')
        for ch in s
    )


async def increment_user_global_dislikes(user_id):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    count = await get_user_global_dislikes(user_id)
    await r.set(f'{user_id}:global_dislikes:{Dev_FINAL}', count + 1)
    return count + 1


def format_user_usernames(user, none_text='مافي يوزر', active_usernames=None):
    """
    يبني نص كل يوزرات المستخدم (يدعم عدة يوزرات وليس واحد فقط).

    المصادر بالأولوية:
    1) active_usernames المُمررة صراحة (تُجلب من ChatFullInfo.active_usernames عبر
       get_user_identity_data، لأن كائن User العادي في aiogram/Bot API لا يحمل إلا
       يوزر واحد فقط - وهذا سبب ظهور يوزر واحد بدل الكل).
    2) خاصية active_usernames على الكائن نفسه (لو كان ChatFullInfo تم تمريره مباشرة).
    3) خاصية usernames القديمة (توافقية مع كائنات pyrogram).
    4) خاصية username المفردة كحل أخير.
    """
    seen = set()
    names = []

    def _add(uname):
        if uname and uname not in seen:
            seen.add(uname)
            names.append(f'@{uname}')

    for source in (active_usernames, getattr(user, 'active_usernames', None), getattr(user, 'usernames', None)):
        if not source:
            continue
        for item in source:
            uname = item if isinstance(item, str) else getattr(item, 'username', None)
            _add(uname)

    _add(getattr(user, 'username', None))

    if names:
        return ', '.join(names)
    return none_text


async def get_user_identity_data(c, r, user_id, include_gifts=True):
    """
    يجلب مستوى الحساب (rating.level)، عدد الهدايا (getUserGifts)، كل اليوزرات النشطة
    (active_usernames) والبايو - بأقل عدد ممكن من طلبات الشبكة، مع تخزين مؤقت في Redis.

    ملاحظة مهمة: getUserGifts و ChatFullInfo.rating إضافات حديثة جداً في Bot API
    (9.3 و10.1 على التوالي)، فهي تحتاج aiogram 3.27+ (للهدايا) و3.29+ تقريباً
    (للمستوى) على الأقل. إذا رجعت قيمة 0 دائماً راجع اللوق - الأسباب المطبوعة هنا
    هي السبب الحقيقي، ما نبلعها بصمت بعد الآن.

    يرجع dict: {'level': int, 'gifts': int, 'usernames': list[str], 'bio': str|None}
    """
    cache_key = f'{user_id}:identity_data' if include_gifts else f'{user_id}:identity_data_no_gifts'
    try:
        cached = await r.get(cache_key)
        if cached:
            return json.loads(cached)
    except Exception:
        pass

    async def _fetch_chat_full():
        try:
            return await c.get_chat(user_id)
        except Exception as e:
            print(f"[identity] فشل get_chat({user_id}): {type(e).__name__}: {e}")
            return None

    async def _fetch_gifts():
        if not include_gifts:
            return 0
        bot_obj = getattr(c, 'bot', None)
        get_gifts_fn = getattr(bot_obj, 'get_user_gifts', None)
        if get_gifts_fn is None:
            print(
                f"[identity] c.bot.get_user_gifts غير متوفر لهذا الكائن (نوعه: {type(bot_obj).__name__ if bot_obj is not None else 'None'}). "
                f"تأكد أن: 1) إصدار aiogram المثبت 3.27 أو أحدث (pip show aiogram) "
                f"2) طبقة compat لا تحجب/تعيد تغليف Bot بدون هذه الدالة."
            )
            return 0
        try:
            owned = await get_gifts_fn(user_id=user_id, limit=1)
            return owned.total_count or 0
        except Exception as e:
            print(f"[identity] فشل get_user_gifts({user_id}): {type(e).__name__}: {e}")
            return 0

    chat_full, gifts_count = await asyncio.gather(_fetch_chat_full(), _fetch_gifts())

    level = 0
    usernames_list = []
    bio = None
    if chat_full is not None:
        if not hasattr(chat_full, 'rating'):
            print(
                f"[identity] ChatFullInfo لهذا المستخدم ({user_id}) ما فيها خاصية rating أصلاً - "
                f"هذا يعني إصدار aiogram المثبت أقدم من الإصدار الذي يدعم Bot API 10.1 "
                f"(الحقل rating أُضيف لـ ChatFullInfo فيه). حدّث aiogram."
            )
        rating = getattr(chat_full, 'rating', None)
        if rating is not None:
            level = getattr(rating, 'level', 0) or 0
        active = getattr(chat_full, 'active_usernames', None)
        if active:
            usernames_list = [u for u in active if u]
        bio = getattr(chat_full, 'bio', None)

    data = {'level': level, 'gifts': gifts_count, 'usernames': usernames_list, 'bio': bio}

    try:
        await r.set(cache_key, json.dumps(data), ex=300)
    except Exception:
        pass

    return data



async def get_user_stars_level_and_gifts(c, r, user_id):
    """للتوافقية مع أي استدعاء قديم يحتاج فقط المستوى والهدايا."""
    data = await get_user_identity_data(c, r, user_id)
    return data.get('level', 0), str(data.get('gifts', 0))



def get_top(users):
   users = [tuple(i.items()) for i in users]
   top = sorted(users, key=lambda i: i[-1][-1], reverse=True)
   top = [dict(i) for i in top]
   return top


DEFAULT_ID_FORMAT = '''
𖡋 𝐔𝐒𝐄 ⌯  #اليوزر
𖡋 𝐌𝐒𝐆 ⌯  #الرسائل
𖡋 𝐒𝐓𝐀 ⌯  #الرتبه
𖡋 𝐈𝐃 ⌯  #الايدي
𖡋 𝐄𝐃𝐈𝐓 ⌯  #التعديل
𖡋 𝐂𝐑  ⌯  #الانشاء
𖡋 𝐆𝐅𝐓 ⌯  #الهدايا
𖡋 𝐋𝐕𝐋 ⌯  #المستوى
#البايو'''


def get_tfa3l_label(msg):
   if msg > 10000:
      return 'اسطورة التلي'
   elif msg > 5000:
      return 'اسطورة التفاعل'
   elif msg > 2500:
      return 'متفاعل'
   elif msg > 750:
      return 'تفاعل متوسط'
   elif msg > 500:
      return 'يجي منك'
   elif msg > 50:
      return 'شد حيلك'
   else:
      return 'تفاعل صفر'


async def get_id_format(r, Dev_FINAL, chat_id):
   fmt = await r.get(f'{chat_id}:customID:{Dev_FINAL}')
   if fmt:
      return fmt
   fmt = await r.get(f'customID:{Dev_FINAL}')
   if fmt:
      return fmt
   return DEFAULT_ID_FORMAT


async def build_id_text_msg(c, r, Dev_FINAL, chat_id, target_user, m=None):
    try:
        if target_user and target_user.first_name:
            await r.set(f"{target_user.id}:bankName", target_user.first_name[:25])
    except Exception:
        pass

    # جلب متوازي للمعلومات من Redis و Client
    # ملاحظة: identity_task يجلب المستوى + الهدايا + كل اليوزرات النشطة + البايو
    # بطلب get_chat واحد فقط بدل طلبين منفصلين (تحسين استجابة إضافي).
    fmt_task = get_id_format(r, Dev_FINAL, chat_id)
    identity_task = get_user_identity_data(c, r, target_user.id)
    rank_task = get_rank(target_user.id, chat_id)
    msgs_task = r.get(f'{Dev_FINAL}{chat_id}:TotalMsgs:{target_user.id}')
    edits_task = r.get(f'{chat_id}:TotalEDMsgs:{target_user.id}{Dev_FINAL}')
    create_task = get_creation_date(target_user.id)

    id_format, identity_data, rank, msg_value, edits_value, create = await asyncio.gather(
        fmt_task, identity_task, rank_task, msgs_task, edits_task, create_task,
        return_exceptions=True
    )

    id_format = id_format if isinstance(id_format, str) else DEFAULT_ID_FORMAT
    if isinstance(identity_data, Exception) or not identity_data:
        identity_data = {'level': 0, 'gifts': 0, 'usernames': [], 'bio': None}
    level = identity_data.get('level', 0)
    gifts_count = identity_data.get('gifts', 0)
    username = format_user_usernames(target_user, active_usernames=identity_data.get('usernames'))
    rank = rank if isinstance(rank, str) else "عضو"
    msg = int(msg_value) if msg_value and not isinstance(msg_value, Exception) else 0
    edits = int(edits_value) if edits_value and not isinstance(edits_value, Exception) else 0
    create = create if isinstance(create, str) else "غير معروف"
    bio = identity_data.get('bio') or 'مافي بايو'

    iD = f'<code>{target_user.id}</code>'
    name = target_user.first_name
    if target_user.last_name:
        name = f'{target_user.first_name} {target_user.last_name}'

    tfa3l = get_tfa3l_label(msg)
    comment = random.choice(comments)
    mention_html = f'<a href="tg://user?id={target_user.id}">{html.escape(str(name))}</a>'

    text_msg = (
        id_format
        .replace('#الاسم', mention_html)
        .replace('#اليوزر', username)
        .replace('#الرسائل', str(msg))
        .replace('#التعديل', str(edits))
        .replace('#الانشاء', create)
        .replace('#البايو', f'{bio}')
        .replace('#تعليق', comment)
        .replace('#الايدي', iD)
        .replace('#الرتبه', rank)
        .replace('#التفاعل', tfa3l)
        .replace('#الهدايا', str(gifts_count))
        .replace('#المستوى', str(level))
    )

    # ملاحظة: id_format يُخزَّن بالفعل بصيغة <tg-emoji> صحيحة عند الحفظ
    # (انظر render_custom_emoji_entities في نقطتَي addCustomID/addCustomIDG)،
    # عبر قصّ محسوب بالموضع (offset/length) لا بحثاً نصياً. لذلك لا حاجة
    # لأي معالجة إضافية هنا. كان يوجد سابقاً تمرير ثانٍ يعيد الحقن اعتماداً
    # على m.text/m.entities (رسالة استدعاء الأمر، لا رسالة تعيين الشكل!)
    # عبر text_msg.replace(emoji_char, ...) — وبما أن emoji_char يقع أصلاً
    # داخل الوسم الصحيح الذي بنته render_custom_emoji_entities، كان هذا
    # الاستبدال النصي الساذج يعيد تغليف/تمزيق الوسم القائم فينتج HTML
    # فاسداً (خصوصاً مع تكرار نفس الإيموجي أو تشابهه)، وهو بالضبط النمط
    # الذي حُذّر منه في helpers/emoji.py.
    return text_msg



async def build_id_reply_markup(r, Dev_FINAL, chat_id, owner_id, user_id):
   if await r.get(f'{owner_id}:disableIDLikes:{Dev_FINAL}'):
      return None
   likes_set, dislikes_set = await get_user_reactions(owner_id)
   like_emoji = await get_user_like_emoji(owner_id)
   dislike_emoji = await get_user_dislike_emoji(owner_id)
   like_btn = await create_button_raw("id", "like_btn", f"{like_emoji}{len(likes_set)}", callback_data=f"id_like_{owner_id}")
   dislike_btn = await create_button_raw("id", "dislike_btn", f"{dislike_emoji}{len(dislikes_set)}", callback_data=f"id_dislike_{owner_id}")
   return {"inline_keyboard": [[like_btn, dislike_btn]]}


async def get_owner_media(c, r, owner):
    try:
        photos = [p async for p in c.get_chat_photos(owner.id, limit=1)]
        if photos:
            return 'photo_file_id', photos[0].file_id
    except Exception:
        pass
    return None, None



async def send_id_card(c, m, r, Dev_FINAL, chat_id, owner_id, text_msg, reply_markup, photo_override=None, target_user=None, ignore_disable_photo=False):
    blur, caption_above, disable_photo = await asyncio.gather(
        r.get(f'{Dev_FINAL}:idBlur'),
        r.get(f'{Dev_FINAL}:disableIDCaptionBelow'),
        r.get(f'{chat_id}:disableIDPHOTO:{Dev_FINAL}')
    )

    blur = bool(blur)
    caption_above = bool(caption_above)

    def _register(sent_msg):
        if sent_msg and hasattr(sent_msg, 'id'):
            user_id_messages.setdefault(owner_id, []).append(sent_msg.id)

    if not ignore_disable_photo and disable_photo:
        sent = await c.send_message(
            chat_id=chat_id,
            text=text_msg,
            parse_mode="HTML",
            disable_web_page_preview=True,
            reply_to_message_id=m.id,
            reply_markup=reply_markup
        )
        _register(sent)
        return

    if photo_override is not None:
        kind, data = photo_override
    elif target_user is not None:
        kind, data = await get_owner_media(c, r, target_user)
    else:
        kind, data = None, None

    if kind == 'photo_file_id':
        sent = await c.send_photo(
            chat_id=chat_id,
            photo=data,
            caption=text_msg,
            parse_mode="HTML",
            reply_to_message_id=m.id,
            has_spoiler=blur,
            show_caption_above_media=caption_above,
            reply_markup=reply_markup
        )
        _register(sent)
        return

    if kind == 'video_file_id':
        sent = await c.send_animation(
            chat_id=chat_id,
            animation=data,
            caption=text_msg,
            parse_mode="HTML",
            reply_to_message_id=m.id,
            has_spoiler=blur,
            show_caption_above_media=caption_above,
            reply_markup=reply_markup
        )
        _register(sent)
        return

    sent = await c.send_message(
        chat_id=chat_id,
        text=text_msg,
        parse_mode="HTML",
        disable_web_page_preview=True,
        reply_to_message_id=m.id,
        reply_markup=reply_markup
    )
    _register(sent)



custom_ids = ['''
- ᴜѕᴇʀɴᴀᴍᴇ ➣ #اليوزر .
- ᴍѕɢѕ ➣ #الرسائل .
- ѕᴛᴀᴛѕ ➣ #الرتبه .
- ʏᴏᴜʀ ɪᴅ ➣ #الايدي .
- ᴇᴅɪᴛ ᴍsɢ ➣ #التعديل .
- ᴅᴇᴛᴀɪʟs ➣ #التفاعل .
-  ɢᴀᴍᴇ ➣ #المجوهرات .
#البايو
''','''
• USE 𖦹 #اليوزر
• MSG 𖥳 #الرسائل
• STA 𖦹 #الرتبه
• iD 𖥳 #الايدي
#البايو
''','''
➞: 𝒔𝒕𝒂𓂅 #اليوزر 𓍯
➞: 𝒖𝒔𝒆𝒓𓂅 #المعرف 𓍯
➞: 𝒎𝒔𝒈𝒆𓂅 #الرسائل 𓍯
➞: 𝒊𝒅 𓂅 #الايدي 𓍯
#البايو
''','''
♡ : 𝐼𝐷 𖠀 #الايدي .
♡ : 𝑈𝑆𝐸𝑅 𖠀 #اليوزر .
♡ : 𝑀𝑆𝐺𝑆 𖠀 #الرسائل .
♡ : 𝑆𝑇𝐴𝑇𝑆 𖠀 #الرتبه .
♡ : 𝐸𝐷𝐼𝑇  𖠀 #التعديل .
#البايو
''', '''
- الايـدي || #الايدي.
• الاسـم  || #الاسم.
• المُعرف || #اليوزر.
• الرُتبـه || #الرتبه.
• الرسائل || #الرسائل.
#البايو
''', '''
⌁ NaMe ⇨ #الاسم
⌁ Use ⇨ #اليوزر
⌁ Msg ⇨ #الرسائل
⌁ Sta ⇨ #الرتبه
⌁ iD ⇨ #الايدي
#البايو
''', '''
•¦ ɴᴀᴍᴇ ➺ #الاسم
•¦ ʏᴏᴜʀ ɪᴅ ➺ #الايدي
•¦ ᴜѕᴇʀɴᴀᴍᴇ ➺ #اليوزر
•¦ ѕᴛᴀᴛѕ ➺ #الرتبه
•¦ ᴅᴇᴛᴀɪʟs ➺ #التفاعل
•¦  ᴍѕɢѕ ➺ #الرسائل
•¦ ɢᴀᴍᴇ ➺ #المجوهرات
#البايو
''', '''
✾ 𝐔𝐒𝐄 ⤷ #اليوزر
✾ 𝐌𝐒𝐆 ⤷ #الرسائل
✾ 𝐒𝐓𝐀 ⤷ #الرتبه
✾ 𝐈𝐃 ⤷ #الايدي
✾ 𝐁𝐈𝐎 ⤷ #البايو
''', '''
𓆰 𝑼𝑬𝑺 : #اليوزر
𓆰 𝑺𝑻𝑨 : #الرتبه
𓆰 𝑰𝑫 : #الايدي
𓆰 𝑴𝑺𝑮 : #الرسائل
#البايو'''
]


comments = [
  'تكفى لاتكتب ايدي',
  'ديمم يالفخامة',
  'خياس للامانه',
  'احلى من يكتب ايدي',
  'افخم ايدي',
  'لحد يرسل ايدي من بعده',
  'يلبييه اطلق ايدي',
  'ازق ايدي',
  'لعد تكتب ايدي',
  'للاسف ايديك تلوث بصري ):',
  'بنقول حلو ايديك'
]



@Client.on_edited_message(filters.group, group=-10)
async def addeditedmsgCount(c,m):
   r = get_global_r()
   Dev_FINAL = get_global_dev()
   k = get_global_k()
   if m.from_user and await r.get(f'{m.from_user.id}:mute:{m.chat.id}{Dev_FINAL}'):  return
   if not await r.get(f'{m.chat.id}:TotalEDMsgs:{m.from_user.id}{Dev_FINAL}'):
      await r.set(f'{m.chat.id}:TotalEDMsgs:{m.from_user.id}{Dev_FINAL}', 1)
   else:
      get = int((await r.get(f'{m.chat.id}:TotalEDMsgs:{m.from_user.id}{Dev_FINAL}')) or 0)
      await r.set(f'{m.chat.id}:TotalEDMsgs:{m.from_user.id}{Dev_FINAL}', get+1)

@Client.on_message(filters.text & filters.group, group=-11)
async def rankGetHandler(c,m):
   r = get_global_r()
   Dev_FINAL = get_global_dev()
   k = get_global_k()
   k = await r.get(f'{Dev_FINAL}:botkey')
   await get_my_rank(c,m,k)



async def get_my_rank(c,m,k):
   r = get_global_r()
   Dev_FINAL = get_global_dev()
   k = get_global_k()
   global list

   try:
     del list
   except:
     pass
   if not await check_global_restrictions(c, m, k):
       return
   text = m.text
   name = await r.get(f'{Dev_FINAL}:BotName') if await r.get(f'{Dev_FINAL}:BotName') else 'فاينل'
   if text.startswith(f'{name} '):
      text = text.replace(f'{name} ','')
   if await r.get(f'{m.chat.id}:Custom:{m.chat.id}{Dev_FINAL}&text={text}'):
       text = await r.get(f'{m.chat.id}:Custom:{m.chat.id}{Dev_FINAL}&text={text}')
   if await r.get(f'Custom:{Dev_FINAL}&text={text}'):
       text = await r.get(f'Custom:{Dev_FINAL}&text={text}')
   if await check_and_guard_locked_command(c, m, k, text):
       return

   if text.startswith('تعيين لايك ') and len(text.split()) >= 3:
       emoji = text.split('تعيين لايك ')[1].strip()
       if not _is_valid_reaction_emoji(emoji):
           return await m.reply(plugins_identity_499(k))
       await r.set(f'{m.from_user.id}:like_emoji:{Dev_FINAL}', emoji)
       return await m.reply(plugins_identity_501(k, emoji))

   if text.startswith('تعيين دس لايك ') and len(text.split()) >= 3:
       emoji = text.split('تعيين دس لايك ')[1].strip()
       if not _is_valid_reaction_emoji(emoji):
           return await m.reply(plugins_identity_507(k))
       await r.set(f'{m.from_user.id}:dislike_emoji:{Dev_FINAL}', emoji)
       return await m.reply(plugins_identity_509(k, emoji))

   if text == 'مجموعاتي':
     if m.from_user and not await r.smembers(f'{m.from_user.id}:groups'):
       return await m.reply(plugins_identity_513(k))
     else:
       groups = len(await r.smembers(f'{m.from_user.id}:groups'))
       return await m.reply(plugins_identity_516(k, groups))

   if text == 'انشائي':
      create_date = await get_creation_date(m.from_user.id)
      return await m.reply(plugins_identity_520(k, create_date))

   if text == 'الانشاء' and not m.reply_to_message:
      create_date = await get_creation_date(m.from_user.id)
      return await m.reply(plugins_identity_524(k, create_date))

   if (text == 'الانشاء' or text == 'انشائه') and m.reply_to_message:
      create_date = await get_creation_date(m.reply_to_message.from_user.id)
      return await m.reply(plugins_identity_528(k, create_date))

   if text == 'اسمي':
     return await m.reply(m.from_user.first_name, disable_web_page_preview=True)

   if text == 'معلوماتي':
      msgs = int((await r.get(f'{Dev_FINAL}{m.chat.id}:TotalMsgs:{m.from_user.id}')) or 0)
      if msgs > 50:
        tfa3l = 'شد حيلك'
      if msgs > 500:
        tfa3l = 'يجي منك'
      if msgs > 750:
        tfa3l = 'تفاعل متوسط'
      if msgs > 2500:
        tfa3l = 'متفاعل'
      if msgs > 5000:
        tfa3l = 'اسطورة التفاعل'
      if msgs > 10000:
        tfa3l = 'كنق التلي'
      else:
        tfa3l = 'تفاعل صفر'
      if not await r.get(f'{m.chat.id}:TotalEDMsgs:{m.from_user.id}{Dev_FINAL}'):
         edits = 0
      else:
         edits= int((await r.get(f'{m.chat.id}:TotalEDMsgs:{m.from_user.id}{Dev_FINAL}')) or 0)
      if not await r.get(f'{m.chat.id}TotalContacts{m.from_user.id}{Dev_FINAL}'):
         contacts = 0
      else:
         contacts = int((await r.get(f'{m.chat.id}TotalContacts{m.from_user.id}{Dev_FINAL}')) or 0)
      identity_data = await get_user_identity_data(c, r, m.from_user.id)
      level = identity_data.get('level', 0)
      gifts_count = identity_data.get('gifts', 0)
      username = format_user_usernames(m.from_user, active_usernames=identity_data.get('usernames'))
      rank = await get_rank(m.from_user.id,m.chat.id)
      
      mention_html = f'<a href="tg://user?id={m.from_user.id}">{html.escape(str(m.from_user.first_name))}</a>'
      
      text_msg = f'''
- المعلومات
┄─┅═ـ═┅─┄
{k} الاسم ↼ {mention_html}
{k} اليوزر ↼ {username}
{k} الايدي  ↼ <code>{m.from_user.id}</code>
{k} الرتبه ↼ {rank}
{k} المستوى ↼ {level}
{k} الهدايا ↼ {gifts_count}
{k} الرسايل ↼ {msgs}
{k} التعديل ↼ {edits}
{k} التفاعل ↼ {tfa3l}
'''
      return await m.reply(text_msg)

   if text == 'بايو' and m.reply_to_message and m.reply_to_message.from_user:
      if await r.get(f'{m.chat.id}:disableBio:{Dev_FINAL}'):  return
      get = await c.get_chat(m.reply_to_message.from_user.id)
      if not get.bio:
        return await m.reply(plugins_identity_582(k))
      else:
        return await m.reply(plugins_identity_584(get.bio))

   if text == 'بايو' and not m.reply_to_message:
      if await r.get(f'{m.chat.id}:disableBio:{Dev_FINAL}'):  return
      get = await c.get_chat(m.from_user.id)
      if not get.bio:
        return await m.reply(plugins_identity_590(k))
      else:
        return await m.reply(plugins_identity_592(get.bio))


   if text == 'المجموعه' or text == 'المجموعة':
      get_ch = await c.get_chat(m.chat.id)
      link = get_ch.invite_link or '\u0645\u0627\u0641\u064a \u0631\u0627\u0628\u0637'
      count = get_ch.members_count or 0
      try:
          admins = len(list(await c.bot.get_chat_administrators(m.chat.id)))
      except Exception:
          admins = 0
      kicked = 0
      if m.chat.photo:
        type_photo = 'photo'
        if m.chat.username:
          photo = f'https://t.me/{m.chat.username}'
        else:
          photo = await c.download_media(m.chat.photo.big_file_id)
      else:
        type_photo = 'text'
      text_msg = f'معلومات المجموعة:\n\n{k} الاسم ↢ {m.chat.title}\n{k} الايدي ↢ <code>{m.chat.id}</code>\n{k} عدد الاعضاء ↢ ( {count} )\n{k} عدد المشرفين ↢ ( {admins} )\n{k} عدد المحظورين ↢ ( {kicked} )\n{k} الرابط ↢ {link} '
      if type_photo == 'photo':
         await m.reply_photo(photo, caption=text_msg)
         try:
           os.remove(photo)
         except:
           pass
         return
      else:
         return await m.reply(text_msg, disable_web_page_preview=True)

   if text == 'جهاتي':
     if not await r.get(f'{m.chat.id}TotalContacts{m.from_user.id}{Dev_FINAL}'):
       contacts = 0
     else:
       contacts = int((await r.get(f'{m.chat.id}TotalContacts{m.from_user.id}{Dev_FINAL}')) or 0)
     return await m.reply(plugins_identity_628(k, contacts))

   if text == 'افتاري':
     if await r.get(f'{m.chat.id}:disableAV:{Dev_FINAL}'): return False
     has_photo = False
     async for _p in c.get_chat_photos(m.from_user.id, limit=1):
        has_photo = True
        break
     if not has_photo:
       return await m.reply(plugins_identity_637(k))
     else:
       if m.from_user.username:
         photo = f'http://t.me/{m.from_user.username}'
       else:
         async for p in c.get_chat_photos(m.from_user.id,limit=1):
           photo = p.file_id
       get_bio = (await c.get_chat(m.from_user.id)).bio
       if not get_bio:
         caption=None
       else:
         caption = f'<code>{get_bio}</code>'
       return await m.reply_photo(photo,caption=caption)

   if text == 'افتاره' and m.reply_to_message and m.reply_to_message.from_user:
     if await r.get(f'{m.chat.id}:disableAV:{Dev_FINAL}'): return False
     has_photo = False
     async for _p in c.get_chat_photos(m.reply_to_message.from_user.id, limit=1):
        has_photo = True
        break
     if not has_photo:
       return await m.reply(plugins_identity_658(k))
     else:
       if m.reply_to_message.from_user.username:
         photo = f'http://t.me/{m.reply_to_message.from_user.username}'
       else:
         async for p in c.get_chat_photos(m.reply_to_message.from_user.id,limit=1):
           photo = p.file_id
       get_bio = (await c.get_chat(m.reply_to_message.from_user.id)).bio
       if not get_bio:
         caption=None
       else:
         caption = f'<code>{get_bio}</code>'
       return await m.reply_photo(photo,caption=caption)

   if text == 'ايديي':
     return await m.reply(plugins_identity_673(m.from_user.id))

   if text.startswith('افتار') and len(text.split()) == 2:
     if await r.get(f'{m.chat.id}:disableAV:{Dev_FINAL}'): return False
     resolved_id = await resolve_user_id_from_arg(text.split()[1])
     if not resolved_id:
       return
     try:
       get = await c.get_users(resolved_id)
       if get.photo:
         async for p in c.get_chat_photos(get.id,limit=1):
           photo = p.file_id
           break
         else:
           photo = None
         if get.bio:
           caption = f'<code>{get.bio}</code>'
         else:
           caption = None
         if photo:
            return await m.reply_photo(photo,caption=caption)
       else:
         return
     except Exception as e:
       print (e)
       return

   if text == 'رتبتي':
      rank = await get_rank(m.from_user.id, m.chat.id)
      fun_rank = await r.get(f'{m.chat.id}:funrank:{m.from_user.id}:{Dev_FINAL}')
      if rank != 'عضو':
          await m.reply(plugins_identity_705(k, rank))
      elif fun_rank:
          await m.reply(plugins_identity_707(k, fun_rank))
      else:
          await m.reply(plugins_identity_709(k))

   if text == 'مسح رسائلي' or text == 'مسح رسايلي':
      msgs = int((await r.get(f'{Dev_FINAL}{m.chat.id}:TotalMsgs:{m.from_user.id}')) or 0)
      await r.delete(f'{Dev_FINAL}{m.chat.id}:TotalMsgs:{m.from_user.id}')
      return await m.reply(plugins_identity_714(k, msgs))

   if text == 'مسح تكليجاتي':
      if not await r.get(f'{m.chat.id}:TotalEDMsgs:{m.from_user.id}{Dev_FINAL}'):
        return await m.reply(plugins_identity_718(k))
      msgs = int((await r.get(f'{m.chat.id}:TotalEDMsgs:{m.from_user.id}{Dev_FINAL}')) or 0)
      await r.delete(f'{m.chat.id}:TotalEDMsgs:{m.from_user.id}{Dev_FINAL}')
      return await m.reply(plugins_identity_721(k, msgs))

   if text == 'تكليجاتي' or text == 'تعديلاتي':
      if not await r.get(f'{m.chat.id}:TotalEDMsgs:{m.from_user.id}{Dev_FINAL}'):
        return await m.reply(plugins_identity_725(k))
      msgs = int((await r.get(f'{m.chat.id}:TotalEDMsgs:{m.from_user.id}{Dev_FINAL}')) or 0)
      return await m.reply(plugins_identity_727(k, msgs))

   if text == 'رسايلي' or text == 'رسائلي':
      msgs = int((await r.get(f'{Dev_FINAL}{m.chat.id}:TotalMsgs:{m.from_user.id}')) or 0)
      return await m.reply(plugins_identity_731(k, msgs))

   if (text == 'رسايله' or text == 'رسائلة') and m.reply_to_message and m.reply_to_message.from_user:
      msgs = int((await r.get(f'{Dev_FINAL}{m.chat.id}:TotalMsgs:{m.reply_to_message.from_user.id}')) or 0)
      return await m.reply(plugins_identity_735(k, msgs))

   if text == 'رتبته' and m.reply_to_message and m.reply_to_message.from_user:
       rank = await get_rank(m.reply_to_message.from_user.id, m.chat.id)
       fun_rank_reply = await r.get(f'{m.chat.id}:funrank:{m.reply_to_message.from_user.id}:{Dev_FINAL}')
       
       is_restricted = await r.sismember(f"{m.chat.id}:listRESTRICTED:{Dev_FINAL}", str(m.reply_to_message.from_user.id))
       is_muted = await r.sismember(f"{m.chat.id}:listMUTE:{Dev_FINAL}", str(m.reply_to_message.from_user.id))
       is_banned = await r.get(f"{m.reply_to_message.from_user.id}:ban_admin:{m.chat.id}{Dev_FINAL}")
       
       rank2 = 'عضو'
       
       if is_banned:
           rank2 = 'محظور'
       elif is_restricted:
           rank2 = 'مقيد'
       elif is_muted:
           rank2 = 'مكتوم'
       
       reply_text = f'رتبته ↢ '
       if rank != 'عضو':
           reply_text += f'{rank}'
       elif fun_rank_reply:
           reply_text += f'{fun_rank_reply}'
       else:
           reply_text += f'{rank2}'
       await m.reply(reply_text)



   if text == 'نقل م8855555لكية' or text == 'نقل م5555555لكيه':
     if await r.get(f'{m.chat.id}:rankGOWNER:{m.from_user.id}{Dev_FINAL}'):
       status = (await m.chat.get_member(m.from_user.id)).status
       if status == ChatMemberStatus.OWNER:
          return await m.reply(plugins_identity_769(k))
       else:
          async for member in m.chat.get_members(filter=ChatMembersFilter.ADMINISTRATORS):
            if member.status == ChatMemberStatus.OWNER:
              if member.user.is_deleted:
                return await m.reply(plugins_identity_774(k))
              else:
                await r.delete(f'{m.chat.id}:rankGOWNER:{m.from_user.id}{Dev_FINAL}')
                await r.srem(f'{m.chat.id}:listGOWNER:{Dev_FINAL}', m.from_user.id)
                await r.set(f'{m.chat.id}:rankGOWNER:{member.user.id}{Dev_FINAL}', 1)
                await r.sadd(f'{m.chat.id}:listGOWNER:{Dev_FINAL}', member.user.id)
                return await m.reply(plugins_identity_780(member.user.mention(), k))



   if text == "مسح المتفاعلين" or text == "تصفير المتفاعلين":
     if not await owner_pls(m.from_user.id, m.chat.id):
       return await m.reply(plugins_identity_786(k))
     else:
       keys = await r.keys(f"{Dev_FINAL}{m.chat.id}:TotalMsgs:*")
       for _ in keys: await r.delete(_)
       await r.delete(f'TotalMsgsSorted:{m.chat.id}:{Dev_FINAL}')
       return await m.reply(plugins_identity_791(k))

   if text == "مسح القروبات" or text == "تصفير القروبات":
       if not is_owner_only(m.from_user.id):
           return await m.reply(plugins_identity_795(k))
       else:
           keys = await _shared_r.keys(f"{GLOBAL_TOP_NS}:TotalGroupMsgs:*")
           for key in keys:
               await _shared_r.delete(key)
               try:
                   key_str = key.decode() if isinstance(key, bytes) else key
                   chat_id = key_str.split(":TotalGroupMsgs:")[1]
                   await _shared_r.delete(f'{chat_id}:chat_title:{GLOBAL_TOP_NS}')
               except:
                   pass
           return await m.reply(plugins_identity_806(k))


   if text == "ترتيبي" or text == "تفاعلي":
     users = await r.keys(f"{Dev_FINAL}{m.chat.id}:TotalMsgs:*")
     jj = []
     for user in users:
          try:
            uid = int(user.split("TotalMsgs:")[1])
            msgs = await r.get(user)
            jj.append({"id": uid, "msgs": int(msgs)})
          except:
            pass
     top = get_top(jj)
     ids = [i["id"] for i in top]
     rank = ids.index(m.from_user.id) + 1
     msgs = int((await r.get(f"{Dev_FINAL}{m.chat.id}:TotalMsgs:{m.from_user.id}")) or 0)
     return await m.reply(plugins_identity_823(k, rank, k, msgs))

   if text == "المتفاعلين" or text == "توب المتفاعلين":
       top_users = await r.zrevrange(f'TotalMsgsSorted:{m.chat.id}:{Dev_FINAL}', 0, 19, withscores=True)
       if not top_users:
           return await m.reply(REPLIES['plugins_identity_828'])
       
       text_msg = " • توب اعلى 20 متفاعلين بالقروب\n\n"
       count = 0
       emojis = ["🥇", "🥈", "🥉"]
       mention_enabled = not await r.get(f'{m.chat.id}:disableMentionTop:{Dev_FINAL}')
       
       for uid, score in top_users:
           if count == 20: break
           user_id = int(uid)
           name = await r.get(f"{user_id}:bankName") or str(user_id)
           
           if name.startswith('@'):
               name = "حساب مخالف"
           
           if mention_enabled:
               if name != "حساب مخالف":
                   name = f"<a href='tg://user?id={user_id}'>{html.escape(str(name))}</a>"
           
           emoji = emojis[count] if count < 3 else f"{count+1:>4})"
           text_msg += f"{emoji} {int(score):,} l {name}\n"
           count += 1
       
       my_rank = await r.zrevrank(f'TotalMsgsSorted:{m.chat.id}:{Dev_FINAL}', str(m.from_user.id))
       if my_rank is not None:
           my_msgs = await r.zscore(f'TotalMsgsSorted:{m.chat.id}:{Dev_FINAL}', str(m.from_user.id))
           text_msg += f"\n• مركزك ↤︎ {my_rank+1} \n• رسائلك ↤︎ {int(my_msgs):,}"
       
       return await c.send_message(m.chat.id, text_msg, disable_web_page_preview=True, reply_to_message_id=m.id)

   if text == "القروبات المتفاعله" or text == "القروبات المتفاعلة":
       top_groups = []
       for key_raw in await _shared_r.keys(f"{GLOBAL_TOP_NS}:TotalGroupMsgs:*"):
           key = _decode_if_bytes(key_raw) if hasattr(_shared_r, '_decode_if_bytes') else key_raw
           if isinstance(key, bytes):
               key = key.decode('utf-8')
           try:
               parts = key.split(":TotalGroupMsgs:")
               if len(parts) >= 2:
                   chat_id = int(parts[1])
                   msgs = int(await _shared_r.get(key_raw) or 0)
                   if msgs > 0:
                       title = await _shared_r.get(f'{chat_id}:chat_title:{GLOBAL_TOP_NS}')
                       if title:
                           if isinstance(title, bytes):
                               title = title.decode('utf-8')
                       else:
                           try:
                               chat = await c.get_chat(chat_id)
                               title = chat.title or str(chat_id)
                           except:
                               title = str(chat_id)
                       top_groups.append({"id": chat_id, "msgs": msgs, "name": title})
           except Exception as e:
               pass
       
       top_groups.sort(key=lambda x: x["msgs"], reverse=True)
       top_groups = top_groups[:20]
       
       if not top_groups:
           return await m.reply(plugins_identity_888(k))
       
       response_text = " • توب اكثر 20 قروب متفاعلين\n\n"
       count = 0
       emojis = ["🥇", "🥈", "🥉"]
       
       for group in top_groups:
           if count == 20:
               break
           emoji = emojis[count] if count < 3 else f"{count+1:>4})"
           response_text += f"{emoji} {group['msgs']:,} l {group['name'][:35]}\n"
           count += 1
       
       return await c.send_message(m.chat.id, response_text, disable_web_page_preview=True, reply_to_message_id=m.id)


   if text == "توب الدسلايكات":
       from .games.top import _get_cached, _set_cached
       cache_key = f"top:dislikes:{m.chat.id}:{m.from_user.id}"
       cached = _get_cached(cache_key)
       if cached:
           return await m.reply(cached, disable_web_page_preview=True)

       data = await get_likes_top_global("dislikes", c)
       if not data:
           return await m.reply(plugins_identity_921(k))
       
       text_msg = " • توب اعلى 20 دسلايك في البوت\n\n"
       emojis = ["🥇", "🥈", "🥉"]
       for i, item in enumerate(data[:20]):
           emoji = emojis[i] if i < 3 else f"{i+1:>4})"
           name = item.get("name", "مستخدم")
           user_id = item.get("id")
           
           dislike_emoji = await get_user_dislike_emoji(user_id)
           
           text_msg += f"{emoji} {item['count']:,} {dislike_emoji} l {name}\n"
       
       _set_cached(cache_key, text_msg)
       return await m.reply(text_msg, disable_web_page_preview=True)

   if text == "توب اللايكات":
       from .games.top import _get_cached, _set_cached
       cache_key = f"top:likes:{m.chat.id}:{m.from_user.id}"
       cached = _get_cached(cache_key)
       if cached:
           return await m.reply(cached, disable_web_page_preview=True)

       data = await get_likes_top_global("likes", c)
       if not data:
           return await m.reply(plugins_identity_907(k))
       
       text_msg = " • توب اعلى 20 لايك في البوت\n\n"
       emojis = ["🥇", "🥈", "🥉"]
       for i, item in enumerate(data[:20]):
           emoji = emojis[i] if i < 3 else f"{i+1:>4})"
           name = item.get("name", "مستخدم")
           user_id = item.get("id")
           
           like_emoji = await get_user_like_emoji(user_id)
           
           text_msg += f"{emoji} {item['count']:,} {like_emoji} l {name}\n"
       
       _set_cached(cache_key, text_msg)
       return await m.reply(text_msg, disable_web_page_preview=True)


   if text == 'تفعيل منشن المتفاعلين':
       if not await admin_pls(m.from_user.id, m.chat.id):
           return await m.reply(plugins_identity_934(k))
       if not await r.get(f'{m.chat.id}:disableMentionTop:{Dev_FINAL}'):
           return await m.reply(plugins_identity_936(k))
       await r.delete(f'{m.chat.id}:disableMentionTop:{Dev_FINAL}')
       return await m.reply(plugins_identity_938(k))

   if text == 'تعطيل منشن المتفاعلين':
       if not await admin_pls(m.from_user.id, m.chat.id):
           return await m.reply(plugins_identity_942(k))
       if await r.get(f'{m.chat.id}:disableMentionTop:{Dev_FINAL}'):
           return await m.reply(plugins_identity_944(k))
       await r.set(f'{m.chat.id}:disableMentionTop:{Dev_FINAL}', 1)
       return await m.reply(plugins_identity_946(k))

   if text == 'كشف' and m.reply_to_message and m.reply_to_message.from_user:
       try:
           # كشف بالرد: صاحب الرسالة معروف بالكامل من نفس التحديث الوارد،
           # فنستخدم البوت نفسه (aiogram) فقط بلا أي حاجة لبايروجرام إطلاقاً.
           # استخدام الحساب المساعد هنا كان يسبب أخطاء PEER_ID_INVALID لأن
           # جلسة الحساب المساعد قد لا تكون "قابلت" هذا الآيدي من قبل.
           client_to_fetch = c

           uid = m.reply_to_message.from_user.id
           name = m.reply_to_message.from_user.first_name
           reply_username = getattr(m.reply_to_message.from_user, "username", None)
           if reply_username:
               await cache_username_id(reply_username, uid)

           rank = await get_rank(uid, m.chat.id)
           identity_data = await get_user_identity_data(client_to_fetch, r, uid, include_gifts=False)
           
           try:
               member = await m.chat.get_member(uid)
               status = member.status
           except Exception:
               status = None
           
           rank_map = {
               ChatMemberStatus.OWNER: 'المالك',
               ChatMemberStatus.ADMINISTRATOR: 'مشرف',
               ChatMemberStatus.RESTRICTED: 'مقيد',
               ChatMemberStatus.LEFT: 'طالع',
               ChatMemberStatus.MEMBER: 'عضو',
               ChatMemberStatus.BANNED: 'لاقم حظر'
           }
           rank2 = rank_map.get(status, 'غير معروف')
           
           msgs_val = await r.get(f'{Dev_FINAL}{m.chat.id}:TotalMsgs:{uid}')
           msgs = int(msgs_val) if msgs_val else 0
           
           mention_html = f'<a href="tg://user?id={uid}">{html.escape(str(name))}</a>'
           username = format_user_usernames(m.reply_to_message.from_user, 
                                           active_usernames=identity_data.get('usernames'))
           
           text_msg = f'''
{k} الاسم ↢ {mention_html}
{k} الايدي ↢ <code>{uid}</code>
{k} اليوزر ↢ {username}  
{k} الرتبه ↢ {rank} 
{k} المستوى ↢ {identity_data.get('level', 0)} 
{k} الرسائل ↢ {msgs} 
{k} بالمجموعة ↢ {rank2} 
{k} نوع الكشف ↢ بالرد
-'''
           return await c.send_message(m.chat.id, text_msg, disable_web_page_preview=True, reply_to_message_id=m.id)
           
       except Exception as e:
           print(f"Error in reply kashf: {e}")
           return await m.reply(plugins_identity_991(k))

   if text.startswith('كشف') and len(text.split()) > 1 and m.text and 'tg://user?id=' in m.html:
       try:
           # كشف بالمنشن (Text Mention): تليجرام يرسل بيانات المستخدم كاملة
           # ضمن نفس الرسالة (نفس منطق الرد)، فلا حاجة لبايروجرام هنا أيضاً.
           user = int(re.search(r'href="([^"]+)', m.html).group(1).split('=')[1])
           client_to_fetch = c

           try:
               member = await m.chat.get_member(user)
               uid = member.user.id
               name = member.user.first_name
               user_obj = member.user
               rank = member.status
           except Exception:
               user_obj = await c.get_users(user)
               uid = user_obj.id
               name = user_obj.first_name
               rank = 'طالع'

           if getattr(user_obj, "username", None):
               await cache_username_id(user_obj.username, uid)
           
           rank_map = {
               ChatMemberStatus.OWNER: 'المالك',
               ChatMemberStatus.ADMINISTRATOR: 'مشرف',
               ChatMemberStatus.RESTRICTED: 'مقيد',
               ChatMemberStatus.LEFT: 'طالع',
               ChatMemberStatus.MEMBER: 'عضو',
               ChatMemberStatus.BANNED: 'لاقم حظر'
           }
           rank_text = rank_map.get(rank, 'غير معروف') if rank in rank_map else 'طالع'
           
           msgs_val = await r.get(f'{Dev_FINAL}{m.chat.id}:TotalMsgs:{uid}')
           msgs = int(msgs_val) if msgs_val else 0
           rank2 = await get_rank(uid, m.chat.id)
           identity_data = await get_user_identity_data(client_to_fetch, r, uid, include_gifts=False)
           username = format_user_usernames(user_obj, none_text='ماعنده يوزر', 
                                           active_usernames=identity_data.get('usernames'))
           
           mention_html = f'<a href="tg://user?id={uid}">{html.escape(str(name))}</a>'
           
           text_msg = f'''
{k} الاسم ↢ {mention_html}
{k} الايدي ↢ <code>{uid}</code>
{k} اليوزر ↢ {username} 
{k} الرتبه ↢ {rank2} 
{k} المستوى ↢ {identity_data.get('level', 0)} 
{k} الرسائل ↢ {msgs} 
{k} بالمجموعة ↢ {rank_text} 
{k} نوع الكشف ↢ بالمنشن
-'''
           return await c.send_message(m.chat.id, text_msg, disable_web_page_preview=True, reply_to_message_id=m.id)
           
       except Exception as e:
           print(f"Error in mention kashf: {e}")
           return

   if text.startswith('كشف') and len(text.split()) == 2:
       user_input = text.split()[1]
       is_id_input = user_input.lstrip('-').isdigit()
       is_username_input = user_input.startswith('@') and len(user_input.lstrip('@').strip()) > 0

       # تجاهل صامت تماماً لأي مدخل غير @يوزرنيم أو آيدي رقمي (مثل
       # "كشف احمد")، بدون أي محاولة شبكة أو استثناء.
       if not is_id_input and not is_username_input:
           return

       try:
           is_username = is_username_input
           ks = 'باليوزر' if is_username else 'بالايدي'

           user_obj = None
           uid = None
           rank = 'طالع'

           if is_username:
               uname = user_input.lstrip('@').strip()

               # أولاً: الخريطة المشتركة بين كل بوتات الكلاستر (aiogram
               # فقط، بلا Pyrogram) — لو أي بوت رأى هذا اليوزرنيم من قبل
               # ولو مرة، نكشف بواسطة آيديه المحفوظ مباشرة، لأن aiogram
               # يتعامل مع الآيديات بشكل صحيح وموثوق (بخلاف اليوزرات).
               cached_uid = await get_cached_username_id(uname)
               if cached_uid:
                   uid = cached_uid
                   try:
                       member = await m.chat.get_member(uid)
                       user_obj = member.user
                       rank = member.status
                   except Exception:
                       try:
                           user_obj = await c.get_users(uid)
                           rank = 'طالع'
                       except Exception:
                           user_obj = None
                           uid = None

               # لم يوجد اليوزر المدخل بالكاش (أو تعذّر تأكيده عبر aiogram
               # رغم وجوده) — نلجأ لعملية Pyrogram الحالية، لكن عبر الحساب
               # المساعد الموجود فعلياً عند البوت الأب حصراً (يعمل من أي
               # بوت بالكلاستر، وليس احتكاراً لبوت واحد).
               if uid is None:
                   userbot = await get_parent_userbot_client()
                   if not userbot:
                       return await m.reply(plugins_identity_991(k))
                   try:
                       user_obj = await userbot.get_chat(uname)
                       uid = user_obj.id
                   except Exception as e:
                       print(f"Error resolving username kashf via parent userbot: {e}")
                       return
                   await cache_username_id(uname, uid)
                   try:
                       member = await m.chat.get_member(uid)
                       rank = member.status
                   except Exception:
                       rank = 'طالع'
           else:
               # كشف بالآيدي: أولاً عبر البوت نفسه (موثوق لو المستخدم عضو
               # بهذه المجموعة)، وفقط عند الفشل نجرب الحساب المساعد الخاص
               # بالبوت الأب كخيار أخير.
               uid = await resolve_user_id_from_arg(user_input)
               if not uid:
                   return
               try:
                   member = await m.chat.get_member(uid)
                   user_obj = member.user
                   rank = member.status
               except Exception:
                   try:
                       user_obj = await c.get_users(uid)
                       rank = 'طالع'
                   except Exception:
                       userbot = await get_parent_userbot_client()
                       if not userbot:
                           return await m.reply(plugins_identity_991(k))
                       try:
                           user_obj = await userbot.get_chat(uid)
                           rank = 'طالع'
                       except Exception as e:
                           print(f"Error in id kashf fallback: {e}")
                           return await m.reply(plugins_identity_991(k))

           if user_obj is None or uid is None:
               return

           if getattr(user_obj, "username", None):
               await cache_username_id(user_obj.username, uid)

           name = user_obj.first_name
           rank_map = {
               ChatMemberStatus.OWNER: 'المالك',
               ChatMemberStatus.ADMINISTRATOR: 'مشرف',
               ChatMemberStatus.RESTRICTED: 'مقيد',
               ChatMemberStatus.LEFT: 'طالع',
               ChatMemberStatus.MEMBER: 'عضو',
               ChatMemberStatus.BANNED: 'لاقم حظر'
           }
           rank_text = rank_map.get(rank, 'غير معروف') if rank in rank_map else 'طالع'
           
           msgs_val = await r.get(f'{Dev_FINAL}{m.chat.id}:TotalMsgs:{uid}')
           msgs = int(msgs_val) if msgs_val else 0
           rank2 = await get_rank(uid, m.chat.id)
           identity_data = await get_user_identity_data(c, r, uid, include_gifts=False)
           username = format_user_usernames(user_obj, none_text='ماعنده يوزر',
                                           active_usernames=identity_data.get('usernames'))
           
           mention_html = f'<a href="tg://user?id={uid}">{html.escape(str(name))}</a>'
           
           text_msg = f'''
{k} الاسم ↢ {mention_html}
{k} الايدي ↢ <code>{uid}</code>
{k} اليوزر ↢ {username} 
{k} الرتبه ↢ {rank2} 
{k} المستوى ↢ {identity_data.get('level', 0)} 
{k} الرسائل ↢ {msgs} 
{k} بالمجموعة ↢ {rank_text} 
{k} نوع الكشف ↢ {ks}
-'''
           return await c.send_message(m.chat.id, text_msg, disable_web_page_preview=True, reply_to_message_id=m.id)
           
       except Exception as e:
           print(f"Error in id/username kashf: {e}")
           return




   if text == 'صلاحياته' and m.reply_to_message and m.reply_to_message.from_user:
      target_id = m.reply_to_message.from_user.id
      get = await m.chat.get_member(target_id)
      if not get.status in [ChatMemberStatus.ADMINISTRATOR,ChatMemberStatus.OWNER]:
         fake_holder = await r.get(f'{m.chat.id}:upfakeHolder:{target_id}:{Dev_FINAL}')
         if fake_holder:
            from .upfake import UPFAKE_PERMS
            perms = await get_fake_rank_perms(target_id, m.chat.id)
            lines = []
            for idx, (key, label) in enumerate(UPFAKE_PERMS, start=1):
               state = "✓" if str(perms.get(key, '0')) == '1' else "✗"
               lines.append(f"{idx}) - {label} ↼ ( {state} )")
            perms_block = "\n".join(lines)
            return await m.reply(plugins_identity_1131(fake_holder, perms_block))
         return await m.reply(plugins_identity_1132(k))
      if get.status == ChatMemberStatus.OWNER:
         return await m.reply(plugins_identity_1134(k))
      if get.status == ChatMemberStatus.ADMINISTRATOR:
         p = get  # CompatChatMember exposes can_* directly, no .privileges
         p1 = "✓" if p.can_manage_chat else "✗"
         p2 = "✓" if p.can_delete_messages else "✗"
         p3 = "✓" if p.can_manage_video_chats else "✗"
         p4 = "✓" if p.can_restrict_members else "✗"
         p5 = "✓" if p.can_promote_members else "✗"
         p6 = "✓" if p.can_change_info else "✗"
         p7 = "✓" if p.can_pin_messages else "✗"
         text_msg = f'''
{k} هو مشرف وهذي صلاحياته :

1) - ادارة المجموعة ↼ ( {p1} )
2) - مسح الرسائل ↼ ( {p2} )
3) - ادارة مكالمات ↼ ( {p3} )
4) - تقييد الأعضاء وحظرهم ↼ ( {p4} )
5) - رفع المشرفين ↼ ( {p5} )
6) - تعديل معلومات المجموعة ↼ ( {p6} )
7) - تثبيت الرسايل ↼ ( {p7} )


'''
         return await m.reply(text_msg)

   if text == 'صلاحياتي':
      get = await m.chat.get_member(m.from_user.id)
      if not get.status in [ChatMemberStatus.ADMINISTRATOR,ChatMemberStatus.OWNER]:
         fake_holder = await r.get(f'{m.chat.id}:upfakeHolder:{m.from_user.id}:{Dev_FINAL}')
         if fake_holder:
            from .upfake import UPFAKE_PERMS
            perms = await get_fake_rank_perms(m.from_user.id, m.chat.id)
            lines = []
            for idx, (key, label) in enumerate(UPFAKE_PERMS, start=1):
               state = "✓" if str(perms.get(key, '0')) == '1' else "✗"
               lines.append(f"{idx}) - {label} ↼ ( {state} )")
            perms_block = "\n".join(lines)
            return await m.reply(plugins_identity_1171(fake_holder, perms_block))
         return await m.reply(plugins_identity_1172(k))
      if get.status == ChatMemberStatus.OWNER:
         return await m.reply(plugins_identity_1174(k))
      if get.status == ChatMemberStatus.ADMINISTRATOR:
         p = get  # CompatChatMember exposes can_* directly, no .privileges
         p1 = "✓" if p.can_manage_chat else "✗"
         p2 = "✓" if p.can_delete_messages else "✗"
         p3 = "✓" if p.can_manage_video_chats else "✗"
         p4 = "✓" if p.can_restrict_members else "✗"
         p5 = "✓" if p.can_promote_members else "✗"
         p6 = "✓" if p.can_change_info else "✗"
         p7 = "✓" if p.can_pin_messages else "✗"
         text_msg = f'''
{k} انت مشرف وهذي صلاحياتك :

1) - ادارة المجموعة ↼ ( {p1} )
2) - مسح الرسائل ↼ ( {p2} )
3) - ادارة مكالمات ↼ ( {p3} )
4) - تقييد الأعضاء وحظرهم ↼ ( {p4} )
5) - رفع المشرفين ↼ ( {p5} )
6) - تعديل معلومات المجموعة ↼ ( {p6} )
7) - تثبيت الرسايل ↼ ( {p7} )


'''
         return await m.reply(text_msg)


   if await r.get(f'{m.chat.id}:addCustomID:{m.from_user.id}{Dev_FINAL}') and text == 'الغاء':
      await r.delete(f'{m.chat.id}:addCustomID:{m.from_user.id}{Dev_FINAL}')
      await m.reply(plugins_identity_1202(k))
      return

   if await r.get(f'{m.chat.id}:addCustomIDG:{m.from_user.id}{Dev_FINAL}') and text == 'الغاء':
      await r.delete(f'{m.chat.id}:addCustomIDG:{m.from_user.id}{Dev_FINAL}')
      await m.reply(plugins_identity_1207(k))
      return

   if await r.get(f'{m.chat.id}:addCustomIDG:{m.from_user.id}{Dev_FINAL}') and await dev2_pls(m.from_user.id, m.chat.id):
      custom_text = m.text
      if m.entities:
          custom_text = render_custom_emoji_entities(custom_text, m.entities)
      await r.set(f'customID:{Dev_FINAL}', custom_text)
      await m.reply(plugins_identity_1221(k, k))
      await r.delete(f'{m.chat.id}:addCustomIDG:{m.from_user.id}{Dev_FINAL}')
      return

   if await r.get(f'{m.chat.id}:addCustomID:{m.from_user.id}{Dev_FINAL}') and await mod_pls(m.from_user.id, m.chat.id):
      if await r.get(f'{Dev_FINAL}:disableCustomIDGlobal'):
         return await m.reply(plugins_identity_1227(k))
      custom_text = m.text
      if m.entities:
          custom_text = render_custom_emoji_entities(custom_text, m.entities)
      await r.set(f'{m.chat.id}:customID:{Dev_FINAL}', custom_text)
      await m.reply(plugins_identity_1238(k, k))
      await r.delete(f'{m.chat.id}:addCustomID:{m.from_user.id}{Dev_FINAL}')
      return

   if text == 'مسح الايدي':
      if not await mod_pls(m.from_user.id, m.chat.id):
         return await m.reply(plugins_identity_1244(k))
      if not await r.get(f'{m.chat.id}:customID:{Dev_FINAL}'):
         return await m.reply(plugins_identity_1246(k))
      else:
         await m.reply(plugins_identity_1248(k))
         await r.delete(f'{m.chat.id}:customID:{Dev_FINAL}')
         return

   if text == 'مسح الايدي العام' or text == 'مسح الايدي عام':
      if not await dev2_pls(m.from_user.id, m.chat.id):
         return await m.reply(plugins_identity_1254(k))
      if not await r.get(f'customID:{Dev_FINAL}'):
         return await m.reply(plugins_identity_1256(k))
      else:
         await m.reply(plugins_identity_1258(k))
         await r.delete(f'customID:{Dev_FINAL}')

   if text == 'الايدي':
      if not await mod_pls(m.from_user.id, m.chat.id):
         return
      if not await r.get(f'{m.chat.id}:customID:{Dev_FINAL}'):
         return await m.reply(plugins_identity_1265(k))
      else:
         id_val = await r.get(f'{m.chat.id}:customID:{Dev_FINAL}')
         return await m.reply(plugins_identity_1268(id_val))

   if text == 'الايدي العام':
      if not await dev2_pls(m.from_user.id, m.chat.id):
         return
      if not await r.get(f'customID:{Dev_FINAL}'):
         return await m.reply(plugins_identity_1274(k))
      else:
         id_val = await r.get(f'customID:{Dev_FINAL}')
         return await m.reply(plugins_identity_1277(id_val))

   if text == 'تغيير الايدي':
      if not await mod_pls(m.from_user.id, m.chat.id):
         return await m.reply(plugins_identity_1281(k))
      if await r.get(f'{Dev_FINAL}:disableCustomIDGlobal'):
         return await m.reply(plugins_identity_1283(k))
      if await r.get(f'{m.chat.id}:disableCustomID:{Dev_FINAL}'):
         return await m.reply(plugins_identity_1285(k))
      else:
         id_val = random.choice(custom_ids)
         await r.set(f'{m.chat.id}:customID:{Dev_FINAL}', id_val)
         await m.reply(plugins_identity_1289(k, k))

   if text == 'تعيين الايدي':
      if not await mod_pls(m.from_user.id, m.chat.id):
         return await m.reply(plugins_identity_1293(k))
      if await r.get(f'{Dev_FINAL}:disableCustomIDGlobal'):
         return await m.reply(plugins_identity_1295(k))
      if await r.get(f'{m.chat.id}:disableCustomID:{Dev_FINAL}'):
         return await m.reply(plugins_identity_1297(k))
      reply = '''
تمام , الحين ارسل شكل الايدي الجديد

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


'''
      await m.reply(reply)
      await r.set(f'{m.chat.id}:addCustomID:{m.from_user.id}{Dev_FINAL}', 1)
      return

   if text == 'تعيين الايدي عام':
      if not await dev2_pls(m.from_user.id, m.chat.id):
         return await m.reply(plugins_identity_1324(k))
      reply = '''
تمام , الحين ارسل شكل الايدي الجديد

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

'''
      await m.reply(reply)
      await r.set(f'{m.chat.id}:addCustomIDG:{m.from_user.id}{Dev_FINAL}', 1)
      return True

   if text == 'تفعيل تعيين الايدي':
      if not await dev2_pls(m.from_user.id, m.chat.id):
         return await m.reply(plugins_identity_1350(k))
      if not await r.get(f'{Dev_FINAL}:disableCustomIDGlobal'):
         return await m.reply(plugins_identity_1352(k))
      await r.delete(f'{Dev_FINAL}:disableCustomIDGlobal')
      return await m.reply(plugins_identity_1354(k))

   if text == 'تعطيل تعيين الايدي':
      if not await dev2_pls(m.from_user.id, m.chat.id):
         return await m.reply(plugins_identity_1358(k))
      if await r.get(f'{Dev_FINAL}:disableCustomIDGlobal'):
         return await m.reply(plugins_identity_1360(k))
      await r.set(f'{Dev_FINAL}:disableCustomIDGlobal', 1)
      return await m.reply(plugins_identity_1362(k))

   if text == 'تفعيل اشعارات الايدي':
      if not await r.get(f'{m.from_user.id}:disableIDNotifications:{Dev_FINAL}'):
         return await m.reply(plugins_identity_1366(k))
      await r.delete(f'{m.from_user.id}:disableIDNotifications:{Dev_FINAL}')
      return await m.reply(plugins_identity_1368(k))

   if text == 'تعطيل اشعارات الايدي':
      if await r.get(f'{m.from_user.id}:disableIDNotifications:{Dev_FINAL}'):
         return await m.reply(plugins_identity_1372(k))
      await r.set(f'{m.from_user.id}:disableIDNotifications:{Dev_FINAL}', 1)
      return await m.reply(plugins_identity_1374(k))

   if text == 'تفعيل لايك الايدي':
      if await r.get(f'{m.from_user.id}:disableIDLikes:{Dev_FINAL}'):
         await r.delete(f'{m.from_user.id}:disableIDLikes:{Dev_FINAL}')
         return await m.reply(plugins_identity_1379(k))
      else:
         return await m.reply(plugins_identity_1381(k))

   if text == 'تعطيل لايك الايدي':
      if not await r.get(f'{m.from_user.id}:disableIDLikes:{Dev_FINAL}'):
         await r.set(f'{m.from_user.id}:disableIDLikes:{Dev_FINAL}', 1)
         return await m.reply(plugins_identity_1386(k))
      else:
         return await m.reply(plugins_identity_1388(k))

   if text == 'تفعيل ايدي الاعضاء':
      if not await admin_pls(m.from_user.id, m.chat.id):
        return await m.reply(plugins_identity_1392(k))
      if not await r.get(f'{m.chat.id}:disableMemberID:{Dev_FINAL}'):
         return await m.reply(plugins_identity_1394(k))
      await r.delete(f'{m.chat.id}:disableMemberID:{Dev_FINAL}')
      return await m.reply(plugins_identity_1396(k))

   if text == 'تعطيل ايدي الاعضاء':
      if not await admin_pls(m.from_user.id, m.chat.id):
        return await m.reply(plugins_identity_1400(k))
      if await r.get(f'{m.chat.id}:disableMemberID:{Dev_FINAL}'):
         return await m.reply(plugins_identity_1402(k))
      await r.set(f'{m.chat.id}:disableMemberID:{Dev_FINAL}', 1)
      return await m.reply(plugins_identity_1404(k))

   if text == 'تصفير ايديه':
      if not await dev_pls(m.from_user.id, m.chat.id):
         return await m.reply(plugins_identity_1408(k))
      if m.reply_to_message:
         user_id = m.reply_to_message.from_user.id
         user_mention = f'<a href="tg://user?id={user_id}">{html.escape(str(m.reply_to_message.from_user.first_name))}</a>'
      else:
         user_id = m.from_user.id
         user_mention = f'<a href="tg://user?id={user_id}">{html.escape(str(m.from_user.first_name))}</a>'
      await r.delete(f'{user_id}:global_likes:{Dev_FINAL}')
      await r.delete(f'{user_id}:global_dislikes:{Dev_FINAL}')
      await r.delete(f'global_reactions:{user_id}')
      await r.delete(f'{user_id}:like_emoji:{Dev_FINAL}')
      await r.delete(f'{user_id}:dislike_emoji:{Dev_FINAL}')
      await r.delete(f'{user_id}:disableIDLikes:{Dev_FINAL}')
      return await m.reply(plugins_identity_1421(k, user_mention))

   if text == 'ايديه' or text == 'idh':
      if not m.reply_to_message:
         return await m.reply(plugins_identity_1425(k))

      if await r.get(f'{m.chat.id}:disableID:{Dev_FINAL}'): return

      user_rank = await get_rank(m.from_user.id, m.chat.id)
      is_member = user_rank in ['عضو', 'مميز']
      if is_member and await r.get(f'{m.chat.id}:disableMemberID:{Dev_FINAL}') == '1':
         return await m.reply(plugins_identity_1432(k))

      target_user = m.reply_to_message.from_user

      text_msg = await build_id_text_msg(c, r, Dev_FINAL, m.chat.id, target_user, m)
      reply_markup = await build_id_reply_markup(r, Dev_FINAL, m.chat.id, target_user.id, m.from_user.id)

      await send_id_card(
          c, m, r, Dev_FINAL, m.chat.id, target_user.id,
          text_msg, reply_markup, target_user=target_user
      )
      return


   if text.startswith('ايديه ') and len(text.split()) == 2:
      if not m.reply_to_message:
         return await m.reply(plugins_identity_1448(k))

      try:
         photo_index = int(text.split()[1]) - 1
      except ValueError:
         return await m.reply(plugins_identity_1453(k))

      if await r.get(f'{m.chat.id}:disableID:{Dev_FINAL}'): return

      user_rank = await get_rank(m.from_user.id, m.chat.id)
      is_member = user_rank in ['عضو', 'مميز']
      if is_member and await r.get(f'{m.chat.id}:disableMemberID:{Dev_FINAL}') == '1':
         return await m.reply(plugins_identity_1460(k))

      target_user = m.reply_to_message.from_user

      photos = []
      async for p in c.get_chat_photos(target_user.id, limit=10):
         photos.append(p.file_id)
      if not photos:
         return await m.reply(plugins_identity_1468(k))
      if photo_index >= len(photos):
         return await m.reply(plugins_identity_1470(k, photo_index+1))
      photo = photos[photo_index]

      text_msg = await build_id_text_msg(c, r, Dev_FINAL, m.chat.id, target_user, m)
      reply_markup = await build_id_reply_markup(r, Dev_FINAL, m.chat.id, target_user.id, m.from_user.id)

      await send_id_card(
         c, m, r, Dev_FINAL, m.chat.id, target_user.id,
         text_msg, reply_markup, photo_override=('photo_file_id', photo), ignore_disable_photo=True
      )
      return


   if text.startswith('ايدي ') and len(text.split()) == 2:
      try:
         photo_index = int(text.split()[1]) - 1
      except ValueError:
         return await m.reply(plugins_identity_1487(k))

      if await r.get(f'{m.chat.id}:disableID:{Dev_FINAL}'): return

      user_rank = await get_rank(m.from_user.id, m.chat.id)
      is_member = user_rank in ['عضو', 'مميز']
      if is_member and await r.get(f'{m.chat.id}:disableMemberID:{Dev_FINAL}') == '1':
         return await m.reply(plugins_identity_1494(k))

      photos = []
      async for p in c.get_chat_photos(m.from_user.id, limit=10):
         photos.append(p.file_id)
      if not photos:
         return await m.reply(plugins_identity_1500(k))
      if photo_index >= len(photos):
         return await m.reply(plugins_identity_1502(k, photo_index+1))
      photo = photos[photo_index]

      text_msg = await build_id_text_msg(c, r, Dev_FINAL, m.chat.id, m.from_user, m)
      reply_markup = await build_id_reply_markup(r, Dev_FINAL, m.chat.id, m.from_user.id, m.from_user.id)

      await send_id_card(
         c, m, r, Dev_FINAL, m.chat.id, m.from_user.id,
         text_msg, reply_markup, photo_override=('photo_file_id', photo), ignore_disable_photo=True
      )
      return


   if text == 'تفعيل الايدي':
     if not (await admin_pls(m.from_user.id,m.chat.id) or await fake_rank_pls(m.from_user.id, m.chat.id, 'id')):
       return await m.reply(plugins_identity_1517(k))
     else:
       if not await r.get(f'{m.chat.id}:disableID:{Dev_FINAL}'):
         return await m.reply(plugins_identity_1520(k, m.from_user.mention(), k))
       else:
         await r.delete(f'{m.chat.id}:disableID:{Dev_FINAL}')
         return await m.reply(plugins_identity_1523(k, m.from_user.mention(), k))

   if text == 'تعطيل الايدي':
     if not (await admin_pls(m.from_user.id,m.chat.id) or await fake_rank_pls(m.from_user.id, m.chat.id, 'id')):
       return await m.reply(plugins_identity_1527(k))
     else:
       if await r.get(f'{m.chat.id}:disableID:{Dev_FINAL}'):
         return await m.reply(plugins_identity_1530(k, m.from_user.mention(), k))
       else:
         await r.set(f'{m.chat.id}:disableID:{Dev_FINAL}',1)
         return await m.reply(plugins_identity_1533(k, m.from_user.mention(), k))

   if text == 'تفعيل افتاري':
     if not await admin_pls(m.from_user.id,m.chat.id):
       return await m.reply(plugins_identity_1537(k))
     else:
       if not await r.get(f'{m.chat.id}:disableAV:{Dev_FINAL}'):
         return await m.reply(plugins_identity_1540(k, m.from_user.mention(), k))
       else:
         await r.delete(f'{m.chat.id}:disableAV:{Dev_FINAL}')
         return await m.reply(plugins_identity_1543(k, m.from_user.mention(), k))

   if text == 'تعطيل افتاري':
     if not await admin_pls(m.from_user.id,m.chat.id):
       return await m.reply(plugins_identity_1547(k))
     else:
       if await r.get(f'{m.chat.id}:disableAV:{Dev_FINAL}'):
         return await m.reply(plugins_identity_1550(k, m.from_user.mention(), k))
       else:
         await r.set(f'{m.chat.id}:disableAV:{Dev_FINAL}',1)
         return await m.reply(plugins_identity_1553(k, m.from_user.mention(), k))

   if text == 'تعطيل الايدي بالصوره':
     if not await admin_pls(m.from_user.id,m.chat.id):
       return await m.reply(plugins_identity_1557(k))
     else:
       if await r.get(f'{m.chat.id}:disableIDPHOTO:{Dev_FINAL}'):
         return await m.reply(plugins_identity_1560(k, m.from_user.mention(), k))
       else:
         await r.set(f'{m.chat.id}:disableIDPHOTO:{Dev_FINAL}',1)
         return await m.reply(plugins_identity_1563(k, m.from_user.mention(), k))

   if text == 'تفعيل الايدي بالصوره':
     if not await admin_pls(m.from_user.id,m.chat.id):
       return await m.reply(plugins_identity_1567(k))
     else:
       if not await r.get(f'{m.chat.id}:disableIDPHOTO:{Dev_FINAL}'):
         return await m.reply(plugins_identity_1570(k, m.from_user.mention(), k))
       else:
         await r.delete(f'{m.chat.id}:disableIDPHOTO:{Dev_FINAL}')
         return await m.reply(plugins_identity_1573(k, m.from_user.mention(), k))

   if text == 'تفعيل الايدي مشوش':
      if not await dev2_pls(m.from_user.id, m.chat.id):
         return await m.reply(plugins_identity_1577(k))
      if await r.get(f'{Dev_FINAL}:idBlur'):
         return await m.reply(plugins_identity_1579(k))
      await r.set(f'{Dev_FINAL}:idBlur', 1)
      return await m.reply(plugins_identity_1581(k))

   if text == 'تعطيل الايدي مشوش':
      if not await dev2_pls(m.from_user.id, m.chat.id):
         return await m.reply(plugins_identity_1585(k))
      if not await r.get(f'{Dev_FINAL}:idBlur'):
         return await m.reply(plugins_identity_1587(k))
      await r.delete(f'{Dev_FINAL}:idBlur')
      return await m.reply(plugins_identity_1589(k))

   if text == 'تفعيل الايدي اسفل':
      if not await dev2_pls(m.from_user.id, m.chat.id):
         return await m.reply(plugins_identity_1593(k))
      if not await r.get(f'{Dev_FINAL}:disableIDCaptionBelow'):
         return await m.reply(plugins_identity_1595(k))
      await r.delete(f'{Dev_FINAL}:disableIDCaptionBelow')
      return await m.reply(plugins_identity_1597(k))

   if text == 'تعطيل الايدي اسفل':
      if not await dev2_pls(m.from_user.id, m.chat.id):
         return await m.reply(plugins_identity_1601(k))
      if await r.get(f'{Dev_FINAL}:disableIDCaptionBelow'):
         return await m.reply(plugins_identity_1603(k))
      await r.set(f'{Dev_FINAL}:disableIDCaptionBelow', 1)
      return await m.reply(plugins_identity_1605(k))

   if text == "لقبي":
      title = (await m.chat.get_member(m.from_user.id)).custom_title
      if not title:
         return await m.reply(plugins_identity_1610(k))
      else:
         return await m.reply(plugins_identity_1612(k, title))

   if (text == 'ايدي' or text.lower() == 'ا') and m.reply_to_message and m.reply_to_message.from_user:
      return await m.reply(plugins_identity_1615(m.reply_to_message.from_user.id))

   if (text == 'ايدي' or text.lower() == 'id') and not m.reply_to_message:
       if await r.get(f'{m.chat.id}:disableID:{Dev_FINAL}'): return

       user_rank = await get_rank(m.from_user.id, m.chat.id)
       is_member = user_rank in ['عضو', 'مميز']
       if is_member and await r.get(f'{m.chat.id}:disableMemberID:{Dev_FINAL}') == '1':
          return await m.reply(plugins_identity_1623(k))

       text_msg = await build_id_text_msg(c, r, Dev_FINAL, m.chat.id, m.from_user, m)
       reply_markup = await build_id_reply_markup(r, Dev_FINAL, m.chat.id, m.from_user.id, m.from_user.id)

       await send_id_card(
           c, m, r, Dev_FINAL, m.chat.id, m.from_user.id,
           text_msg, reply_markup, target_user=m.from_user
       )
       return


async def get_likes_top_global(data_type, client=None):
    """جلب توب اللايكات والدسلايكات على مستوى البوت"""
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    result = []
    
    pattern = "global_reactions:*"
    uids = []
    counts_dict = {}
    
    for key_raw in await r.keys(pattern):
        key = _decode_if_bytes(key_raw) if hasattr(r, '_decode_if_bytes') else key_raw
        if isinstance(key, bytes):
            key = key.decode('utf-8')
        try:
            uid = int(key.split("global_reactions:")[1])
            data = await r.get(key)
            if data:
                loaded = json.loads(data) if isinstance(data, str) else json.loads(data.decode('utf-8'))
                if data_type == "likes":
                    count = len(loaded.get('likes', []))
                else:
                    count = len(loaded.get('dislikes', []))
                if count > 0:
                    uids.append(uid)
                    counts_dict[uid] = count
        except Exception as e:
            pass
    
    if uids:
        from .protect import _decode_if_bytes
        names = await get_user_names_batch(uids, client) if hasattr(globals(), 'get_user_names_batch') else {}
        if not names:
            for uid in uids:
                name = await r.get(f"{uid}:bankName")
                if name:
                    if isinstance(name, bytes):
                        name = name.decode('utf-8')
                    names[uid] = name
        
        for uid in uids:
            if uid in names:
                result.append({"name": names[uid][:15], "id": uid, "count": counts_dict[uid]})
    
    result.sort(key=lambda x: x["count"], reverse=True)
    return result[:20]


async def get_user_names_batch(uids, client=None):
    """جلب أسماء المستخدمين دفعة واحدة"""
    r = get_global_r()
    names = {}
    for uid in uids:
        name = await r.get(f"{uid}:bankName")
        if name:
            if isinstance(name, bytes):
                name = name.decode('utf-8')
            names[uid] = name
    return names


@Client.on_message(filters.new_chat_members, group=-12)
async def addContact(c,m):
  r = get_global_r()
  Dev_FINAL = get_global_dev()
  k = get_global_k()
  if m.new_chat_members:
    for me in m.new_chat_members:
      if m.from_user and not m.from_user.id == me.id:
        if not await r.get(f'{m.chat.id}TotalContacts{m.from_user.id}{Dev_FINAL}'):
          await r.set(f'{m.chat.id}TotalContacts{m.from_user.id}{Dev_FINAL}',1)
        else:
          co = int((await r.get(f'{m.chat.id}TotalContacts{m.from_user.id}{Dev_FINAL}')) or 0)
          await r.set(f'{m.chat.id}TotalContacts{m.from_user.id}{Dev_FINAL}',co+1)


@Client.on_callback_query(filters.regex(r"^(id_like_|id_dislike_|id_back_|id_next_|id_close_)"), group=-91)
async def handle_id_reactions(client, callback_query):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    data = callback_query.data
    chat_id = callback_query.message.chat.id
    message_id = callback_query.message.id
    reactor_id = callback_query.from_user.id

    if data.startswith("id_like_"):
        try:
            owner_id = int(data.split("_")[2])
        except ValueError:
            await callback_query.answer(REPLIES['plugins_identity_1725'], show_alert=True)
            return

        try:
            owner_chat = await client.get_chat(owner_id)
            if owner_chat and owner_chat.first_name:
                await r.set(f"{owner_id}:bankName", owner_chat.first_name[:25])
        except Exception:
            pass

        likes_set, dislikes_set = await get_user_reactions(owner_id)

        if reactor_id in likes_set:
            await callback_query.answer(REPLIES['plugins_identity_1738'], show_alert=True)
            return

        if reactor_id in dislikes_set:
            dislikes_set.remove(reactor_id)
            likes_set.add(reactor_id)
            
            current_dislikes = await get_user_global_dislikes(owner_id)
            if current_dislikes > 0:
                await r.set(f'{owner_id}:global_dislikes:{Dev_FINAL}', current_dislikes - 1)
            await increment_user_global_likes(owner_id)
            await save_user_reactions(owner_id, likes_set, dislikes_set)
            
            await callback_query.answer(REPLIES['plugins_identity_1751'], show_alert=False)
        else:
            likes_set.add(reactor_id)
            await increment_user_global_likes(owner_id)
            await save_user_reactions(owner_id, likes_set, dislikes_set)
            await callback_query.answer(REPLIES['plugins_identity_1751'], show_alert=False)

        new_like_count = len(likes_set)
        new_dislike_count = len(dislikes_set)
        like_emoji = await get_user_like_emoji(owner_id)
        dislike_emoji = await get_user_dislike_emoji(owner_id)
        
        like_btn = await create_button_raw("id", "like_btn", f"{like_emoji}{new_like_count}", callback_data=f"id_like_{owner_id}")
        dislike_btn = await create_button_raw("id", "dislike_btn", f"{dislike_emoji}{new_dislike_count}", callback_data=f"id_dislike_{owner_id}")
        
        updated_keyboard = {"inline_keyboard": [[like_btn, dislike_btn]]}
        bot_token = client.bot_token if hasattr(client, "bot_token") else settings.TOKEN

        try:
            await telegram_api_post(bot_token, "editMessageReplyMarkup", {
                    "chat_id": chat_id,
                    "message_id": message_id,
                    "reply_markup": updated_keyboard
                })
        except Exception as e:
            print(f"خطأ: {e}")

        if not await r.get(f'{owner_id}:disableIDNotifications:{Dev_FINAL}'):
            try:
                reactor_name = callback_query.from_user.first_name
                reactor_mention = f'<a href="tg://user?id={reactor_id}">{html.escape(str(reactor_name))}</a>'
                now = time.localtime()
                date_str = time.strftime("%Y/%m/%d", now)
                time_str = time.strftime("%I:%M%p", now)
                
                user_btn = await create_button_raw("id", "user_btn", f" {reactor_name[:15]}", user_id=reactor_id)
                notification_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(**user_btn)]])
                
                notification_text = f"""• وصلك لايك {like_emoji}
• أسمه ↤ {reactor_mention}
• عدد لايكاتك ↤ {new_like_count}
• بتاريخ ↤ {date_str}
• بالساعة ↤ {time_str}

• تقدر تعطل اشعارات الايدي بإمر ↤ ( تعطيل اشعارات الايدي )"""
                
                await client.send_message(
                    owner_id, 
                    notification_text, 
                    disable_web_page_preview=True,
                    reply_markup=notification_keyboard
                )
            except Exception:
                pass

    elif data.startswith("id_dislike_"):
        try:
            owner_id = int(data.split("_")[2])
        except ValueError:
            await callback_query.answer(REPLIES['plugins_identity_1725'], show_alert=True)
            return

        try:
            owner_chat = await client.get_chat(owner_id)
            if owner_chat and owner_chat.first_name:
                await r.set(f"{owner_id}:bankName", owner_chat.first_name[:25])
        except Exception:
            pass

        likes_set, dislikes_set = await get_user_reactions(owner_id)

        if reactor_id in dislikes_set:
            await callback_query.answer(REPLIES['plugins_identity_1826'], show_alert=True)
            return

        if reactor_id in likes_set:
            likes_set.remove(reactor_id)
            dislikes_set.add(reactor_id)
            
            current_likes = await get_user_global_likes(owner_id)
            if current_likes > 0:
                await r.set(f'{owner_id}:global_likes:{Dev_FINAL}', current_likes - 1)
            await increment_user_global_dislikes(owner_id)
            await save_user_reactions(owner_id, likes_set, dislikes_set)
            
            await callback_query.answer(REPLIES['plugins_identity_1839'], show_alert=False)
        else:
            dislikes_set.add(reactor_id)
            await increment_user_global_dislikes(owner_id)
            await save_user_reactions(owner_id, likes_set, dislikes_set)
            await callback_query.answer(REPLIES['plugins_identity_1839'], show_alert=False)

        new_like_count = len(likes_set)
        new_dislike_count = len(dislikes_set)
        like_emoji = await get_user_like_emoji(owner_id)
        dislike_emoji = await get_user_dislike_emoji(owner_id)
        
        like_btn = await create_button_raw("id", "like_btn", f"{like_emoji}{new_like_count}", callback_data=f"id_like_{owner_id}")
        dislike_btn = await create_button_raw("id", "dislike_btn", f"{dislike_emoji}{new_dislike_count}", callback_data=f"id_dislike_{owner_id}")
        
        updated_keyboard = {"inline_keyboard": [[like_btn, dislike_btn]]}
        bot_token = client.bot_token if hasattr(client, "bot_token") else settings.TOKEN

        try:
            await telegram_api_post(bot_token, "editMessageReplyMarkup", {
                    "chat_id": chat_id,
                    "message_id": message_id,
                    "reply_markup": updated_keyboard
                })
        except Exception as e:
            print(f"خطأ: {e}")

        if not await r.get(f'{owner_id}:disableIDNotifications:{Dev_FINAL}'):
            try:
                reactor_name = callback_query.from_user.first_name
                reactor_mention = f'<a href="tg://user?id={reactor_id}">{html.escape(str(reactor_name))}</a>'
                now = time.localtime()
                date_str = time.strftime("%Y/%m/%d", now)
                time_str = time.strftime("%I:%M%p", now)
                
                user_btn = await create_button_raw("id", "user_btn", f" {reactor_name[:15]}", user_id=reactor_id)
                notification_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(**user_btn)]])
                
                notification_text = f"""• وصلك دس لايك {dislike_emoji}
• أسمه ↤ {reactor_mention}
• عدد دس لايكاتك ↤ {new_dislike_count}
• بتاريخ ↤ {date_str}
• بالساعة ↤ {time_str}

• تقدر تعطل اشعارات الايدي بإمر ↤ ( تعطيل اشعارات الايدي )"""
                
                await client.send_message(
                    owner_id, 
                    notification_text, 
                    disable_web_page_preview=True,
                    reply_markup=notification_keyboard
                )
            except Exception:
                pass

    await callback_query.answer()


@Client.on_message(filters.group, group=-723)
async def addmsgCount(c,m):
   r = get_global_r()
   Dev_FINAL = get_global_dev()
   k = get_global_k()
   
   if m.from_user and m.from_user.is_bot:
       return
   
   if m.from_user and await r.get(f'{m.from_user.id}:mute:{m.chat.id}{Dev_FINAL}'):
       return
   
   if await r.get(f"{m.from_user.id}:ban_admin:{m.chat.id}{Dev_FINAL}"):
       return
   
   if not m.text and not m.caption:
       return
   
   if not await claim_event_once(f"msgcount:{Dev_FINAL}:{m.chat.id}:{m.id}"):
      return

   await r.incrby(f'{Dev_FINAL}{m.chat.id}:TotalMsgs:{m.from_user.id}', 1)
   await r.zincrby(f'TotalMsgsSorted:{m.chat.id}:{Dev_FINAL}', 1, str(m.from_user.id))
   await r.zincrby(f'GlobalGroupMsg:{Dev_FINAL}', 1, str(m.chat.id))
   await r.set(f"{m.from_user.id}:bankName", m.from_user.first_name[:25])