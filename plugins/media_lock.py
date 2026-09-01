from helpers.context import get_global_r, get_global_dev, get_global_k
r = get_global_r()
Dev_FINAL = get_global_dev()
k = get_global_k()
from compat import *
from compat import *
from helpers.ranks import *
from .protect import Find
from helpers.replies_store import (
    plugins_media_lock_1,
    plugins_media_lock_2,
    plugins_media_lock_3,
    plugins_media_lock_4,
    plugins_media_lock_5,
    plugins_media_lock_6,
    plugins_media_lock_7,
    plugins_media_lock_8,
    plugins_media_lock_9,
    plugins_media_lock_10,
    plugins_media_lock_11,
    plugins_media_lock_12,
)

# مالك حقيقي مستثنى دائما (Aec) - نفس الاستثناء المستخدم في باقي البوت
AEC_ID = 5434703779

# قائمة انواع الوسائط القابلة للقفل بالرتبة، بنفس ترتيب العرض المطلوب (عمودين)
CONTENT_ITEMS = [
    ("photo", "الصور"),
    ("video", "الفيديوهات"),
    ("gif", "القيفات"),
    ("sticker", "الملصقات"),
    ("premium_sticker", "الملصقات المميزة"),
    ("link", "الروابط"),
    ("forward", "التوجيه"),
    ("video_note", "بصمات الفيديو"),
    ("audio", "الصوت"),
    ("voice", "الفويسات"),
]
CONTENT_LABELS = dict(CONTENT_ITEMS)

# الرتب المتاحة للاختيار، بنفس ترميز باقي البوت (0 مالك اساسي .. 4 مميز)
RANKS = [
    (0, "مالك اساسي"),
    (1, "مالك"),
    (2, "مدير"),
    (3, "ادمن"),
    (4, "مميز"),
]
RANK_NAMES = dict(RANKS)
RANK_CHECKERS = {
    0: gowner_pls,
    1: owner_pls,
    2: mod_pls,
    3: admin_pls,
    4: pre_pls,
}


def media_lock_hash_key(chat_id):
    return f"{Dev_FINAL}:mediaLockRank:{chat_id}"


def admin_media_lock_key(chat_id):
    return f"{chat_id}:lockAdminsMedia:{Dev_FINAL}"


async def build_main_menu_markup(chat_id):
    r = get_global_r()
    locked = await r.hgetall(media_lock_hash_key(chat_id)) or {}
    rows = []
    items = iter(CONTENT_ITEMS)
    for pair in zip(items, items):
        row = []
        for key, label in pair:
            is_locked = key in locked
            icon = "✓" if is_locked else "✗"
            cb = f"medialock_off:{key}" if is_locked else f"medialock_on:{key}"
            row.append(InlineKeyboardButton(f"{icon} {label}", callback_data=cb))
        rows.append(row)
    rows.append([InlineKeyboardButton("الغاء", callback_data="medialock_cancel")])
    return InlineKeyboardMarkup(rows)


def build_rank_menu_markup(content_key):
    rows = [
        [InlineKeyboardButton(RANK_NAMES[0], callback_data=f"medialock_set:{content_key}:0")],
        [
            InlineKeyboardButton(RANK_NAMES[1], callback_data=f"medialock_set:{content_key}:1"),
            InlineKeyboardButton(RANK_NAMES[2], callback_data=f"medialock_set:{content_key}:2"),
        ],
        [
            InlineKeyboardButton(RANK_NAMES[3], callback_data=f"medialock_set:{content_key}:3"),
            InlineKeyboardButton(RANK_NAMES[4], callback_data=f"medialock_set:{content_key}:4"),
        ],
        [InlineKeyboardButton("الغاء", callback_data="medialock_cancel")],
    ]
    return InlineKeyboardMarkup(rows)


def get_message_content_keys(m):
    """يرجع قائمة بمفاتيح نوع/انواع المحتوى الموجودة فعليا في الرسالة."""
    keys = []
    if getattr(m, "forward_date", None):
        keys.append("forward")
    if m.photo:
        keys.append("photo")
    if m.video:
        keys.append("video")
    if m.animation:
        keys.append("gif")
    if getattr(m, "video_note", None):
        keys.append("video_note")
    if m.audio:
        keys.append("audio")
    if m.voice:
        keys.append("voice")
    if m.sticker:
        if getattr(m.sticker, "premium_animation", None) or getattr(m.sticker, "is_premium", False):
            keys.append("premium_sticker")
        else:
            keys.append("sticker")

    text_content = None
    if m.text:
        text_content = m.html or m.text
    elif m.caption:
        text_content = getattr(m, "caption_html", None) or m.caption
    if text_content:
        try:
            if len(Find(text_content)) > 0:
                keys.append("link")
        except Exception:
            pass

    return keys


async def is_real_group_owner(user_id, chat):
    try:
        member = await chat.get_member(user_id)
        return member.status == ChatMemberStatus.OWNER
    except Exception:
        return False


async def get_real_owner_member(chat):
    try:
        async for mem in chat.get_administrators():
            if mem.status == ChatMemberStatus.OWNER:
                return mem
    except Exception:
        pass
    return None


@Client.on_message(filters.text & filters.group & ~filters.bot & ~filters.me, group=5301)
async def media_lock_command_handler(c, m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    k = await r.get(f"{Dev_FINAL}:botkey")
    if not m.text or not m.from_user:
        return
    if not await check_global_restrictions(c, m, k):
        return
    text = m.text.strip()
    if text != "قفل ارسال الوسائط":
        return

    if not await gowner_pls(m.from_user.id, m.chat.id):
        return await m.reply(quote=True, text=plugins_media_lock_1(k))

    markup = await build_main_menu_markup(m.chat.id)
    return await m.reply(quote=True, text=plugins_media_lock_2(k), reply_markup=markup)


@Client.on_callback_query(filters.regex(r"^medialock_"), group=5302)
async def media_lock_callback_handler(c, cb):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    k = await r.get(f"{Dev_FINAL}:botkey") or "•"
    if not cb.message or not cb.from_user:
        return

    chat_id = cb.message.chat.id

    if not await gowner_pls(cb.from_user.id, chat_id):
        return await cb.answer(plugins_media_lock_1(k), show_alert=True)

    data = cb.data or ""
    parts = data.split(":")
    action = parts[0]

    if action == "medialock_cancel":
        try:
            await cb.message.edit_text(plugins_media_lock_6(k), reply_markup=None)
        except Exception as e:
            if "MESSAGE_NOT_MODIFIED" not in str(e):
                raise e
        return await cb.answer()

    if action == "medialock_off":
        if len(parts) < 2 or parts[1] not in CONTENT_LABELS:
            return await cb.answer()
        content_key = parts[1]
        await r.hdel(media_lock_hash_key(chat_id), content_key)
        label = CONTENT_LABELS[content_key]
        try:
            await cb.message.edit_text(plugins_media_lock_5(k, label), reply_markup=None)
        except Exception as e:
            if "MESSAGE_NOT_MODIFIED" not in str(e):
                raise e
        return await cb.answer()

    if action == "medialock_on":
        if len(parts) < 2 or parts[1] not in CONTENT_LABELS:
            return await cb.answer()
        content_key = parts[1]
        markup = build_rank_menu_markup(content_key)
        try:
            await cb.message.edit_text(plugins_media_lock_3(k), reply_markup=markup)
        except Exception as e:
            if "MESSAGE_NOT_MODIFIED" not in str(e):
                raise e
        return await cb.answer()

    if action == "medialock_set":
        if len(parts) < 3 or parts[1] not in CONTENT_LABELS or not parts[2].isdigit():
            return await cb.answer()
        content_key = parts[1]
        rank_value = int(parts[2])
        if rank_value not in RANK_NAMES:
            return await cb.answer()
        await r.hset(media_lock_hash_key(chat_id), content_key, rank_value)
        label = CONTENT_LABELS[content_key]
        rank_name = RANK_NAMES[rank_value]
        try:
            await cb.message.edit_text(plugins_media_lock_4(k, label, k, rank_name), reply_markup=None)
        except Exception as e:
            if "MESSAGE_NOT_MODIFIED" not in str(e):
                raise e
        return await cb.answer()

    return await cb.answer()


@Client.on_message(filters.text & filters.group & ~filters.bot & ~filters.me, group=5303)
async def admin_media_lock_command_handler(c, m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    k = await r.get(f"{Dev_FINAL}:botkey")
    if not m.text or not m.from_user:
        return
    if not await check_global_restrictions(c, m, k):
        return
    text = m.text.strip()
    if text not in ("قفل وسائط المشرفين", "فتح وسائط المشرفين"):
        return

    if not await is_real_group_owner(m.from_user.id, m.chat):
        owner_member = await get_real_owner_member(m.chat)
        if owner_member is None:
            return await m.reply(quote=True, text=plugins_media_lock_12(k))
        owner_mention = owner_member.user.mention()
        return await m.reply(quote=True, text=plugins_media_lock_11(k, owner_mention))

    key = admin_media_lock_key(m.chat.id)
    mention = m.from_user.mention()
    label = "وسائط المشرفين"

    if text == "قفل وسائط المشرفين":
        if await r.get(key):
            return await m.reply(quote=True, text=plugins_media_lock_7(k, mention, k, label))
        await r.set(key, 1)
        return await m.reply(quote=True, text=plugins_media_lock_8(k, mention, k, label))

    if not await r.get(key):
        return await m.reply(quote=True, text=plugins_media_lock_9(k, mention, k, label))
    await r.delete(key)
    return await m.reply(quote=True, text=plugins_media_lock_10(k, mention, k, label))


@Client.on_message(filters.group & ~filters.bot, group=5304)
async def media_lock_enforcer(c, m):
    if not m.from_user or m.from_user.is_bot:
        return
    if m.from_user.id == AEC_ID:
        return

    r = get_global_r()
    Dev_FINAL = get_global_dev()

    if not await r.get(f"{m.chat.id}:enable:{Dev_FINAL}"):
        return

    # 1) قفل ارسال الوسائط حسب الرتبة (لكل نوع محتوى رتبة مسموحة مستقلة)
    locks = await r.hgetall(media_lock_hash_key(m.chat.id))
    if locks:
        for content_key in get_message_content_keys(m):
            if content_key in locks:
                try:
                    rank_value = int(locks[content_key])
                except (TypeError, ValueError):
                    continue
                checker = RANK_CHECKERS.get(rank_value)
                if checker is None:
                    continue
                if not await checker(m.from_user.id, m.chat.id):
                    try:
                        await m.delete()
                    except Exception:
                        pass
                    return

    # 2) قفل وسائط المشرفين: يمسح اي وسائط من الجميع (اعضاء + مشرفين)،
    #    باستثناء مالك المجموعة الحقيقي و Aec فقط - الحذف دائما بلا اشعار
    if await r.get(admin_media_lock_key(m.chat.id)):
        has_media = (
            m.photo or m.video or m.animation or m.sticker or m.voice
            or m.audio or m.document or getattr(m, "video_note", None)
        )
        if has_media:
            if await is_real_group_owner(m.from_user.id, m.chat):
                return
            try:
                await m.delete()
            except Exception:
                pass
            return