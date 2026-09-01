"""
ميزة الاشتراك الاجباري (لكل قروب على حدة) — إعادة بناء كاملة.

نُسف المنطق القديم بالكامل (كان عالمياً لكل بوتات Dev_FINAL عبر مفتاح
forceChannel:{Dev_FINAL} في plugins/handlers.py) واستُبدل بهذا الملف الذي
يجعل الاشتراك الاجباري خاصية مستقلة لكل قروب (chat_id) على حدة.

الأوامر:
    اضف اشتراك @channel   -> المالك الاساسي فقط (gowner_pls) للقروب
    حذف الاشتراك الاجباري  -> المالك الاساسي فقط (gowner_pls) للقروب

الشروط:
    - يجب أن يكون البوت مشرفاً (admin) في القناة المستهدفة قبل قبول الأمر.
    - إن فقد البوت صلاحية الإشراف في القناة لاحقاً، يُلغى الاشتراك الاجباري
      تلقائياً لكل القروبات المرتبطة بها (نتحقق من ذلك عند كل رسالة عبر
      get_chat_member على البوت نفسه، لأن Bot API لا يبعث تحديث my_chat_member
      لكل الأحداث بشكل يغطيه compat.py حالياً — الفحص هنا "كسول" lazy لكنه
      يحقق نفس النتيجة عملياً بأول رسالة تصل بعد فقد الإشراف).
    - الأعضاء الذين رتبتهم admin_pls فأعلى (مشرف/مالك/مطور..) معفيّون من
      الاشتراك الاجباري تماماً.
    - أي عضو آخر غير مشترك بالقناة: تُحذف رسالته، ويصله تحذير واحد فقط طالما
      استمر غير مشترك (لا يتكرر التحذير مع كل رسالة)، فإذا اشترك توقف الحذف،
      وإذا غادر القناة بعد ذلك يصله تحذير جديد مرة واحدة أيضاً.
"""

from helpers.context import get_global_r, get_global_dev, get_global_k
from compat import (
    Client,
    filters,
    ChatMemberStatus,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from compat import errors
from helpers.ranks import gowner_pls, admin_pls, dev2_pls, check_global_restrictions

# ---------------------------------------------------------------------------
# مفاتيح Redis
# ---------------------------------------------------------------------------
# بيانات القناة المفروضة على قروب معيّن (خاصة بكل بوت Dev_FINAL على حدة):
#   force_sub:chat:{chat_id}:{Dev_FINAL}          -> "channel_id|@username|title"
# فهرس عكسي (قناة -> القروبات المرتبطة بها) لإلغاء الاشتراك تلقائياً لو
# القروب الفعلي (نادراً نحتاجه لأن الفحص كسول عبر chat_id مباشرة، لكنه مفيد
# لأي تنظيف مستقبلي):
#   force_sub:channel_groups:{channel_id}:{Dev_FINAL} -> set(chat_id)
# تحذير واحد فقط لكل عضو طالما هو غير مشترك:
#   force_sub:warned:{chat_id}:{user_id}:{Dev_FINAL}  -> "1"


def _chat_key(chat_id, dev):
    return f"force_sub:chat:{chat_id}:{dev}"


def _channel_groups_key(channel_id, dev):
    return f"force_sub:channel_groups:{channel_id}:{dev}"


def _warned_key(chat_id, user_id, dev):
    return f"force_sub:warned:{chat_id}:{user_id}:{dev}"


async def _get_force_channel(r, chat_id, dev):
    """يعيد (channel_id, username, title) أو None إن لم يوجد اشتراك اجباري."""
    raw = await r.get(_chat_key(chat_id, dev))
    if not raw:
        return None
    try:
        channel_id_s, username, title = raw.split("|", 2)
        return int(channel_id_s), username, title
    except Exception:
        return None


async def _clear_force_channel(r, chat_id, dev, channel_id=None):
    await r.delete(_chat_key(chat_id, dev))
    if channel_id is not None:
        try:
            await r.srem(_channel_groups_key(channel_id, dev), str(chat_id))
        except Exception:
            pass


# ---------------------------------------------------------------------------
# الاشتراك الاجباري "العام" — يعيّنه Dev/Dev2 من لوحة التحكم في الخاص، ويُطبَّق
# على كل قروبات هذا البوت دفعة واحدة. لا يلغي/يستبدل اشتراك القروب الخاص (لو
# كان مالك القروب قد عيّن قناة مختلفة لقروبه) — كلاهما يُطلبان معاً في نفس
# القروب إذا اجتمعا، بنفس آلية _get_force_channel لكن على مستوى البوت كله
# بدل chat_id واحد.
# ---------------------------------------------------------------------------
def _global_key(dev):
    return f"force_sub:global:{dev}"


def _global_wizard_key(user_id, dev):
    return f"force_sub:global_wizard:{user_id}:{dev}"


async def _get_global_force_channel(r, dev):
    """يعيد (channel_id, username, title) أو None إن لم يوجد اشتراك اجباري عام."""
    raw = await r.get(_global_key(dev))
    if not raw:
        return None
    try:
        channel_id_s, username, title = raw.split("|", 2)
        return int(channel_id_s), username, title
    except Exception:
        return None


async def _clear_global_force_channel(r, dev):
    await r.delete(_global_key(dev))


async def _validate_and_store_channel(c, username: str):
    """يتحقق أن البوت مشرف بالقناة المعطاة (نفس شرط اشتراك القروب) ويعيد
    (channel_id, title) عند النجاح، أو (None, رسالة خطأ) عند الفشل."""
    try:
        target_chat = await c.get_chat("@" + username)
    except Exception:
        return None, "تعذر العثور على قناة بهذا اليوزر، تأكد منه وحاول مجدداً"

    channel_id = target_chat.id
    channel_title = target_chat.title or username

    try:
        me = await c.get_me()
        bot_member = await c.get_chat_member(channel_id, me.id)
    except Exception:
        return None, "تعذر التحقق من صلاحيات البوت داخل القناة\nتأكد أن البوت مضاف كمشرف بالقناة أولاً"

    if bot_member.status != ChatMemberStatus.ADMINISTRATOR and bot_member.status != ChatMemberStatus.OWNER:
        return None, "يجب اضافة البوت كـ 「 مشرف 」 بالقناة أولاً قبل تعيينها كاشتراك اجباري"

    return (channel_id, channel_title), None


# ---------------------------------------------------------------------------
# أوامر لوحة Dev/Dev2 (تعمل من الخاص): تعيين/مسح الاشتراك الاجباري العام
# ---------------------------------------------------------------------------
@Client.on_message(filters.private & filters.text, group=-89)
async def dev_global_force_subscribe_cmd(c, m):
    if not m.from_user:
        return m.continue_propagation()

    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    text = (m.text or "").strip()
    wizard_key = _global_wizard_key(m.from_user.id, Dev_FINAL)

    if text == 'تعيين الاشتراك الاجباري':
        if not await dev2_pls(m.from_user.id, m.chat.id, c):
            return m.continue_propagation()
        await r.set(wizard_key, 1, ex=600)
        await m.reply(
            f"{k} ارسل يوزر القناة التي تريد تعيينها كاشتراك اجباري عام (لكل قروبات بوتك)\n"
            f"{k} مثال: @channel_username\n"
            f"{k} او اكتب الغاء"
        )
        return m.stop_propagation()

    if text == 'مسح الاشتراك الاجباري':
        if not await dev2_pls(m.from_user.id, m.chat.id, c):
            return m.continue_propagation()
        if not await _get_global_force_channel(r, Dev_FINAL):
            await m.reply(f"{k} لا يوجد اشتراك اجباري عام مفعّل بهذا البوت")
            return m.stop_propagation()
        await _clear_global_force_channel(r, Dev_FINAL)
        await m.reply(f"{k} تم حذف الاشتراك الاجباري العام بنجاح")
        return m.stop_propagation()

    if await r.get(wizard_key):
        if not await dev2_pls(m.from_user.id, m.chat.id, c):
            return m.continue_propagation()
        if text == 'الغاء':
            await r.delete(wizard_key)
            await m.reply(f"{k} تم الالغاء")
            return m.stop_propagation()

        username = text.lstrip('@').strip()
        if not username:
            await m.reply(f"{k} صيغة غير صحيحة، ارسل يوزر القناة او اكتب الغاء")
            return m.stop_propagation()

        result, error = await _validate_and_store_channel(c, username)
        if error:
            await m.reply(f"{k} {error}")
            return m.stop_propagation()

        channel_id, channel_title = result
        await r.delete(wizard_key)
        await r.set(_global_key(Dev_FINAL), f"{channel_id}|@{username}|{channel_title}")
        await m.reply(
            "• تم تعيين الاشتراك الاجباري العام لكل قروبات بوتك\n"
            f"• القناة ↤︎ {channel_title}\n"
            "• لحذفه اكتب ( مسح الاشتراك الاجباري )"
        )
        return m.stop_propagation()

    return m.continue_propagation()


# ---------------------------------------------------------------------------
# أمر: اضف اشتراك @username
# ---------------------------------------------------------------------------
@Client.on_message(filters.text & filters.group, group=-90)
async def add_force_subscribe_cmd(c, m):
    text = (m.text or "").strip()
    if not text.startswith("اضف اشتراك"):
        return m.continue_propagation()

    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()

    if not await check_global_restrictions(c, m, k):
        return m.stop_propagation()

    if not m.from_user:
        return m.stop_propagation()

    if not await gowner_pls(m.from_user.id, m.chat.id):
        await m.reply(f"{k} عذراً هذا الأمر لـ 「 المالك الاساسي 」 فقط")
        return m.stop_propagation()

    parts = text.split()
    username = None
    for p in parts[2:]:
        if p.startswith("@"):
            username = p[1:].strip()
            break

    if not username:
        await m.reply(
            f"{k} صيغة الأمر غير صحيحة\n"
            f"{k} اكتب ↤ اضف اشتراك @يوزر_القناة"
        )
        return m.stop_propagation()

    try:
        target_chat = await c.get_chat("@" + username)
    except Exception:
        await m.reply(f"{k} تعذر العثور على قناة بهذا اليوزر، تأكد منه وحاول مجدداً")
        return m.stop_propagation()

    channel_id = target_chat.id
    channel_title = target_chat.title or username

    try:
        me = await c.get_me()
        bot_member = await c.get_chat_member(channel_id, me.id)
    except Exception:
        await m.reply(
            f"{k} تعذر التحقق من صلاحيات البوت داخل القناة\n"
            f"{k} تأكد أن البوت مضاف كمشرف بالقناة أولاً"
        )
        return m.stop_propagation()

    if bot_member.status != ChatMemberStatus.ADMINISTRATOR and bot_member.status != ChatMemberStatus.OWNER:
        await m.reply(
            f"{k} يجب اضافة البوت كـ 「 مشرف 」 بالقناة أولاً قبل تعيينها كاشتراك اجباري"
        )
        return m.stop_propagation()

    await r.set(_chat_key(m.chat.id, Dev_FINAL), f"{channel_id}|@{username}|{channel_title}")
    try:
        await r.sadd(_channel_groups_key(channel_id, Dev_FINAL), str(m.chat.id))
    except Exception:
        pass
    # قروب جديد باشتراك جديد = تحذيرات القديمة (لو وُجدت من اشتراك سابق) لا معنى لها
    try:
        await r.delete(_chat_key(m.chat.id, Dev_FINAL) + ":_reserved")
    except Exception:
        pass

    await m.reply(
        "• تم تعيين الاشتراك الاجباري \n"
        f"• القناة ↤︎ {channel_title} \n"
        "• لحذفه اكتب ( حذف الاشتراك الاجباري )"
    )
    return m.stop_propagation()


# ---------------------------------------------------------------------------
# أمر: حذف الاشتراك الاجباري
# ---------------------------------------------------------------------------
@Client.on_message(filters.text & filters.group, group=-90)
async def del_force_subscribe_cmd(c, m):
    text = (m.text or "").strip()
    if text != "حذف الاشتراك الاجباري":
        return m.continue_propagation()

    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()

    if not await check_global_restrictions(c, m, k):
        return m.stop_propagation()

    if not m.from_user:
        return m.stop_propagation()

    if not await gowner_pls(m.from_user.id, m.chat.id):
        await m.reply(f"{k} عذراً هذا الأمر لـ 「 المالك الاساسي 」 فقط")
        return m.stop_propagation()

    info = await _get_force_channel(r, m.chat.id, Dev_FINAL)
    if not info:
        await m.reply(f"{k} لا يوجد اشتراك اجباري مفعّل بهذا القروب")
        return m.stop_propagation()

    channel_id, _username, _title = info
    await _clear_force_channel(r, m.chat.id, Dev_FINAL, channel_id)
    await m.reply(f"{k} تم حذف الاشتراك الاجباري بنجاح")
    return m.stop_propagation()


# ---------------------------------------------------------------------------
# الفحص الفعلي: هل يحق لهذا العضو الكتابة بالقروب؟
# يعمل بأولوية مبكرة جداً (قبل أي معالج آخر) على كل الرسائل.
# ---------------------------------------------------------------------------
@Client.on_message(filters.group, group=-2000000000000)
async def enforce_force_subscribe(c, m):
    if not m.from_user or m.from_user.is_bot:
        return m.continue_propagation()

    r = get_global_r()
    Dev_FINAL = get_global_dev()

    chat_info = await _get_force_channel(r, m.chat.id, Dev_FINAL)
    global_info = await _get_global_force_channel(r, Dev_FINAL)

    if not chat_info and not global_info:
        return m.continue_propagation()

    # نبني قائمة القنوات المطلوبة (قد تكون قناة القروب الخاصة + القناة العامة
    # للبوت معاً، بلا تعارض بينهما — كل واحدة مستقلة وتُطلب بجانب الاخرى).
    required = []
    if chat_info:
        required.append(('chat', chat_info))
    if global_info:
        required.append(('global', global_info))

    user_id = m.from_user.id

    # المشرفون فأعلى معفيّون تماماً من الاشتراك الاجباري
    if await admin_pls(user_id, m.chat.id):
        return m.continue_propagation()

    me = await c.get_me()

    missing = []
    for source, (channel_id, username, title) in required:
        # تحقق كسول من أن البوت مازال مشرفاً بالقناة، وإلا يُلغى الاشتراك تلقائياً
        try:
            bot_member = await c.get_chat_member(channel_id, me.id)
            if bot_member.status not in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER):
                if source == 'chat':
                    await _clear_force_channel(r, m.chat.id, Dev_FINAL, channel_id)
                else:
                    await _clear_global_force_channel(r, Dev_FINAL)
                continue
        except Exception:
            if source == 'chat':
                await _clear_force_channel(r, m.chat.id, Dev_FINAL, channel_id)
            else:
                await _clear_global_force_channel(r, Dev_FINAL)
            continue

        try:
            member = await c.get_chat_member(channel_id, user_id)
            is_subscribed = member.status in (
                ChatMemberStatus.MEMBER,
                ChatMemberStatus.ADMINISTRATOR,
                ChatMemberStatus.OWNER,
            )
        except errors.UserNotParticipant:
            is_subscribed = False
        except Exception:
            # أي خطأ غير متوقع بالتحقق (فلود مثلاً) لا نعاقب العضو عليه لهذه القناة
            continue

        if not is_subscribed:
            missing.append((username, title))

    warn_key = _warned_key(m.chat.id, user_id, Dev_FINAL)

    if not missing:
        # مشترك بكل ما هو مطلوب (او تعذر التحقق ولم نُعاقبه) -> نسمح ونصفّر التحذير
        await r.delete(warn_key)
        return m.continue_propagation()

    # ناقص اشتراك واحد او اكثر: تُحذف رسالته دائماً
    try:
        await m.delete()
    except Exception:
        pass

    already_warned = await r.get(warn_key)
    if already_warned:
        return m.stop_propagation()

    await r.set(warn_key, "1")

    buttons = [
        [InlineKeyboardButton(title, url=f"https://t.me/{username.lstrip('@')}")]
        for username, title in missing
    ]
    kb = InlineKeyboardMarkup(buttons)

    if len(missing) == 1:
        body = f"• يجب الاشتراك في ↤︎  {missing[0][1]}\n"
    else:
        titles = "، ".join(t for _u, t in missing)
        body = f"• يجب الاشتراك في القنوات التالية ↤︎  {titles}\n"

    try:
        await c.send_message(
            m.chat.id,
            "• عذرا عزيزي ↤︎" + m.from_user.mention + "\n"
            + body
            + "• اضغط الازرار واشترك لكي تستطيع إرسال رسائل هنا",
            reply_markup=kb,
            parse_mode="HTML",
        )
    except Exception:
        pass

    return m.stop_propagation()

