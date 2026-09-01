from helpers.context import get_global_r, get_global_dev, get_global_k
r = get_global_r()
Dev_FINAL = get_global_dev()
k = get_global_k()
import re
from compat import *
from compat import *
from compat import *
from helpers.ranks import *
from .protect import claim_event_once
from helpers.replies_store import (
    REPLIES,
    plugins_upfake_161,
    plugins_upfake_166,
    plugins_upfake_167,
    plugins_upfake_185,
    plugins_upfake_188,
    plugins_upfake_191,
    plugins_upfake_202,
    plugins_upfake_205,
    plugins_upfake_209,
    plugins_upfake_211,
    plugins_upfake_214,
    plugins_upfake_221,
    plugins_upfake_224,
    plugins_upfake_226,
    plugins_upfake_228,
    plugins_upfake_230,
    plugins_upfake_237,
    plugins_upfake_240,
    plugins_upfake_242,
    plugins_upfake_255,
    plugins_upfake_264,
    plugins_upfake_267,
    plugins_upfake_269,
    plugins_upfake_292,
    plugins_upfake_295,
    plugins_upfake_297,
    plugins_upfake_300,
    plugins_upfake_304,
    plugins_upfake_324,
    plugins_upfake_331,
    plugins_upfake_350,
    plugins_upfake_354,
    plugins_upfake_363,
    plugins_upfake_366,
    plugins_upfake_370,
    plugins_upfake_507,
)

"""
[ = هذا الملف يضيف نظامين مرتبطين برتب التفاعل = ]

1) رتب التفاعل التلقائية:
   - تفعيل/تعطيل الرفع التلقائي.
   - تحديد عدد رسائل (من توب المتفاعلين) يرفع بعده العضو تلقائياً لرتبة حقيقية
     (مميز / ادمن / مدير / مالك) — بدون تجاوز المالك الاساسي.

2) رتب التفاعل الوهمية (المضافة بالاسم):
   - اضافة/حذف اسماء رتب مخصصة داخل المجموعة.
   - رفع عضو برتبة مخصصة بالرد عليه، مع محرر صلاحيات بالأزرار
     (نفس المفاتيح الموجودة أصلاً بقاعدة الاشراف، بدون انشاء مفاتيح جديدة).
   - العضو المرفوع بهذي الطريقة يُستثنى من الاقفال المطابقة للصلاحية المفعّلة
     فقط (عبر fake_rank_pls في helpers/ranks.py)، وليس استثناء كامل كالادمن الحر.

3) رفع عام (Dev² فقط): تغيير اسم ظهور العضو في كل الكشوفات (رتبته/رتبتي/كشف..)
   بدون التأثير على صلاحياته الفعلية.
"""

# --------------------------------------------------------------------------
# الاعدادات / المفاتيح
# --------------------------------------------------------------------------

# رتب حقيقية يسمح الرفع التلقائي لها (اقل من المالك الاساسي)
AUTO_TIERS = {
    'مميز': {'list': 'listPRE', 'rank': 'rankPRE'},
    'ادمن': {'list': 'listADMIN', 'rank': 'rankADMIN'},
    'مدير': {'list': 'listMOD', 'rank': 'rankMOD'},
    'مالك': {'list': 'listOWNER', 'rank': 'rankOWNER'},
}
# ترتيب الاولوية من الاقل للاعلى (يستخدم بالترقية التصاعدية)
AUTO_TIERS_ORDER = ['مميز', 'ادمن', 'مدير', 'مالك']

# دالة فحص "هل العضو عنده هذي الرتبة او اعلى فعلياً؟" لكل رتبة تلقائية
# تستخدم لاستثناء اي عضو رتبته الحالية اعلى او تساوي الرتبة المستهدفة
# من الرفع (مثلاً: مدير لا يُرفع ادمن، لكن يُرفع مالك لأنها اعلى منه)
TIER_RANK_CHECK = {
    'مميز': pre_pls,
    'ادمن': admin_pls,
    'مدير': mod_pls,
    'مالك': owner_pls,
}

# الصلاحيات المتاحة بمحرر رتبة التفاعل الوهمية: (المفتاح الداخلي، النص الظاهر بالزر)
UPFAKE_PERMS = [
    ('restrict', 'تقييد'),
    ('mute', 'كتم'),
    ('ban', 'حظر'),
    ('mention', 'ارسال منشن'),
    ('block_msg', 'منع الرسائل'),
    ('replies', 'اضافه ردود'),
    ('id', 'تفعيل الايدي'),
    ('links', 'ارسال روابط'),
    ('forward', 'توجيه رسائل'),
    ('delete', 'مسح الرسائل'),
    ('media', 'ارسال وسائط'),
]
UPFAKE_PERM_MAP = dict(UPFAKE_PERMS)

OWNER_DENY = 'عذراً الامر لـ「 المالك الاساسي 」 فقط'
DEV2_DENY = 'عذراً الامر لـ「 Dev² 」 فقط'


def _perms_keyboard(target_id: int, perms: dict):
    rows = []
    pairs = UPFAKE_PERMS
    i = 0
    # نعرضها صف لصف كما بالطلب (تقييد لحاله، وبعدها كل صلاحيتين بصف)
    single = pairs[0]
    rest = pairs[1:]
    state = 'نعم' if str(perms.get(single[0], '0')) == '1' else 'لا'
    rows.append([InlineKeyboardButton(f"{single[1]} {state}", callback_data=f"ufperm_{single[0]}:{target_id}")])
    while i < len(rest):
        chunk = rest[i:i + 2]
        row = []
        for key, label in chunk:
            state = 'نعم' if str(perms.get(key, '0')) == '1' else 'لا'
            row.append(InlineKeyboardButton(f"{label} {state}", callback_data=f"ufperm_{key}:{target_id}"))
        rows.append(row)
        i += 2
    rows.append([InlineKeyboardButton('رفع بالمحدد', callback_data=f"ufperm_done:{target_id}")])
    return InlineKeyboardMarkup(rows)


async def _get_target_from_reply(m):
    if m.reply_to_message and m.reply_to_message.from_user:
        return m.reply_to_message.from_user
    return None


async def _build_gowner_mentions(c: Client, r, chat_id: int, bot_id: str) -> str:
    """يبني قائمة منشن (سطر لكل واحد) لكل المالكين الاساسيين بالمجموعة."""
    ids = await r.smembers(f'{chat_id}:listGOWNER:{bot_id}')
    if not ids:
        return ''
    lines = []
    count = 0
    for gid in ids:
        if count >= 30:
            break
        try:
            user = await c.get_users(int(gid))
            mention = user.mention()
        except Exception:
            try:
                mention = f'<a href="tg://user?id={int(gid)}">مالك اساسي</a>'
            except Exception:
                continue
        lines.append(f'- {mention}')
        count += 1
    return '\n'.join(lines)


@Client.on_message(filters.text & filters.group, group=910)
async def upfakeHandler(c: Client, m: Message):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    k = await r.get(f'{Dev_FINAL}:botkey') or '•'
    await upfake_func(c, m, k)


async def upfake_func(c: Client, m: Message, k: str):
    r = get_global_r()
    Dev_FINAL = get_global_dev()

    if not await check_global_restrictions(c, m, k):
        return

    text = (m.text or '').strip()
    name = await r.get(f'{Dev_FINAL}:BotName') or 'فاينل'
    if text.startswith(f'{name} '):
        text = text.replace(f'{name} ', '')
    if await r.get(f'{m.chat.id}:Custom:{m.chat.id}{Dev_FINAL}&text={text}'):
        text = await r.get(f'{m.chat.id}:Custom:{m.chat.id}{Dev_FINAL}&text={text}')
    if await r.get(f'Custom:{Dev_FINAL}&text={text}'):
        text = await r.get(f'Custom:{Dev_FINAL}&text={text}')
    if await check_and_guard_locked_command(c, m, k, text):
        return

    uid = m.from_user.id
    cid = m.chat.id

    # ---------------------------------------------------------------
    # حذف تفاعل الرتب: يوقف الرفع التلقائي ويحذف تعيينات عدد الرسائل
    # (لا يسحب اي رتبة سبق ورفعها البوت، فقط يوقف الآلية ويمسح الاعدادات)
    # ---------------------------------------------------------------
    if text == 'حذف تفاعل الرتب':
        if not await gowner_pls(uid, cid, c):
            return await m.reply(plugins_upfake_161(k, OWNER_DENY))
        had_thresholds = await r.hgetall(f'{cid}:upfakeAutoThresholds:{Dev_FINAL}')
        await r.delete(f'{cid}:upfakeAutoEnabled:{Dev_FINAL}')
        await r.delete(f'{cid}:upfakeAutoThresholds:{Dev_FINAL}')
        if not had_thresholds:
            return await m.reply(plugins_upfake_166(k))
        return await m.reply(
            plugins_upfake_167(k, k)
        )

    # ---------------------------------------------------------------
    # ضع تفاعل <العدد> <الرتبة> — يعيّن العتبة ويشغّل الرفع التلقائي فوراً
    # مثال: ضع تفاعل 500 مالك
    # (تنبيه: لا نتدخل في اي نص آخر يبدأ بـ "ضع تفاعل " فهذا محجوز لتفاعلات
    #  riyaka.py النصية، نتعامل فقط مع الصيغة عدد+رتبة)
    # ---------------------------------------------------------------
    if text.startswith('ضع تفاعل '):
        remainder = text[len('ضع تفاعل '):].strip().split()
        if len(remainder) == 2 and remainder[0].isdigit() and remainder[1] in AUTO_TIERS:
            if not await gowner_pls(uid, cid, c):
                return await m.reply(plugins_upfake_185(k, OWNER_DENY))
            count_raw, tier = remainder
            if int(count_raw) <= 0:
                return await m.reply(plugins_upfake_188(k))
            await r.hset(f'{cid}:upfakeAutoThresholds:{Dev_FINAL}', tier, count_raw)
            await r.set(f'{cid}:upfakeAutoEnabled:{Dev_FINAL}', '1')
            return await m.reply(
                plugins_upfake_191(k, count_raw, tier, k)
            )
        # صيغة اخرى غير عدد+رتبة -> ليست امر رتب تفاعل، نتركها لمعالجات اخرى

    # ---------------------------------------------------------------
    # ضع رتبه <الرتبة> <العدد>
    # ---------------------------------------------------------------
    if text.startswith('ضع رتبه ') or text.startswith('ضع رتبة '):
        if not await gowner_pls(uid, cid, c):
            return await m.reply(plugins_upfake_202(k, OWNER_DENY))
        parts = text.split()
        if len(parts) != 4:
            return await m.reply(plugins_upfake_205(k))
        tier = parts[2]
        count_raw = parts[3]
        if tier not in AUTO_TIERS:
            return await m.reply(plugins_upfake_209(k))
        if not count_raw.isdigit() or int(count_raw) <= 0:
            return await m.reply(plugins_upfake_211(k))
        await r.hset(f'{cid}:upfakeAutoThresholds:{Dev_FINAL}', tier, count_raw)
        await r.set(f'{cid}:upfakeAutoEnabled:{Dev_FINAL}', '1')
        return await m.reply(plugins_upfake_214(k, count_raw, tier))

    # ---------------------------------------------------------------
    # اضف رتبه <الاسم>
    # ---------------------------------------------------------------
    if text.startswith('اضف رتبه ') or text.startswith('اضف رتبة '):
        if not await gowner_pls(uid, cid, c):
            return await m.reply(plugins_upfake_221(k, OWNER_DENY))
        rank_name = text.split(' ', 2)[2].strip() if len(text.split(' ', 2)) == 3 else ''
        if not rank_name:
            return await m.reply(plugins_upfake_224(k))
        if len(rank_name) > 20:
            return await m.reply(plugins_upfake_226(k))
        if await r.sismember(f'{cid}:upfakeDefs:{Dev_FINAL}', rank_name):
            return await m.reply(plugins_upfake_228(k, rank_name))
        await r.sadd(f'{cid}:upfakeDefs:{Dev_FINAL}', rank_name)
        return await m.reply(plugins_upfake_230(k, rank_name))

    # ---------------------------------------------------------------
    # حذف رتبه <الاسم>
    # ---------------------------------------------------------------
    if text.startswith('حذف رتبه ') or text.startswith('حذف رتبة '):
        if not await gowner_pls(uid, cid, c):
            return await m.reply(plugins_upfake_237(k, OWNER_DENY))
        rank_name = text.split(' ', 2)[2].strip() if len(text.split(' ', 2)) == 3 else ''
        if not rank_name:
            return await m.reply(plugins_upfake_240(k))
        if not await r.sismember(f'{cid}:upfakeDefs:{Dev_FINAL}', rank_name):
            return await m.reply(plugins_upfake_242(k))
        await r.srem(f'{cid}:upfakeDefs:{Dev_FINAL}', rank_name)
        holders = await r.smembers(f'{cid}:upfakeHolders:{Dev_FINAL}')
        for holder in list(holders or []):
            try:
                holder_id = int(holder)
            except Exception:
                continue
            current = await r.get(f'{cid}:upfakeHolder:{holder_id}:{Dev_FINAL}')
            if current == rank_name:
                await r.delete(f'{cid}:upfakeHolder:{holder_id}:{Dev_FINAL}')
                await r.delete(f'{cid}:upfakePerms:{holder_id}:{Dev_FINAL}')
                await r.srem(f'{cid}:upfakeHolders:{Dev_FINAL}', holder_id)
        return await m.reply(plugins_upfake_255(k, rank_name))

    # ---------------------------------------------------------------
    # رفع <اسم الرتبة الوهمية> بالرد
    # ---------------------------------------------------------------
    if text.startswith('رفع ') and not text.startswith('رفع عام '):
        rank_name = text[len('رفع '):].strip()
        if rank_name and await r.sismember(f'{cid}:upfakeDefs:{Dev_FINAL}', rank_name):
            if not await gowner_pls(uid, cid, c):
                return await m.reply(plugins_upfake_264(k, OWNER_DENY))
            target = await _get_target_from_reply(m)
            if not target:
                return await m.reply(plugins_upfake_267(k))
            if target.is_bot:
                return await m.reply(plugins_upfake_269(k))

            await r.set(f'{cid}:upfakeHolder:{target.id}:{Dev_FINAL}', rank_name)
            await r.sadd(f'{cid}:upfakeHolders:{Dev_FINAL}', target.id)
            # صلاحيات افتراضية: الكل (لا) اي معطلة
            default_perms = {key: '0' for key, _ in UPFAKE_PERMS}
            await r.hset(f'{cid}:upfakePerms:{target.id}:{Dev_FINAL}', mapping=default_perms)

            mention = target.mention() if hasattr(target, 'mention') else target.first_name
            text_out = (
                f"• المستخدم ↤︎「 {mention} 」\n"
                f"• تم رفعه ↢ {rank_name}\n\n"
                f"{k} تحرير صلاحيات العضو:"
            )
            return await m.reply(text_out, reply_markup=_perms_keyboard(target.id, default_perms))
        # اسم غير معرف كرتبة وهمية -> نتجاهل الامر (يترك لمعالجات اخرى مثل رفع مشرف / رفع للتسلية)
        return

    # ---------------------------------------------------------------
    # رفع عام <الاسم> — Dev² فقط
    # ---------------------------------------------------------------
    if text.startswith('رفع عام '):
        if not await dev2_pls(uid, cid, c):
            return await m.reply(plugins_upfake_292(k, DEV2_DENY))
        new_name = text[len('رفع عام '):].strip()
        if not new_name:
            return await m.reply(plugins_upfake_295(k))
        if len(new_name) > 25:
            return await m.reply(plugins_upfake_297(k))
        target = await _get_target_from_reply(m)
        if not target:
            return await m.reply(plugins_upfake_300(k))

        await r.set(f'{target.id}:upfakeGlobalName:{Dev_FINAL}', new_name)
        mention = target.mention() if hasattr(target, 'mention') else target.first_name
        return await m.reply(plugins_upfake_304(mention, new_name))

    # ---------------------------------------------------------------
    # تنزيل <اسم الرتبة> — يشيل الرتبة الوهمية عن العضو (بالرد)
    # مثال: تنزيل ملك / تنزيل اسطوره
    # لازم الاسم المذكور يطابق اسم الرتبة اللي هو حاملها فعلياً (تحقق أمان)
    # ---------------------------------------------------------------
    if text.startswith('تنزيل ') and not text.startswith('تنزيل عام '):
        rank_name = text[len('تنزيل '):].strip()
        if rank_name:
            target = await _get_target_from_reply(m)
            if not target:
                return
            holder = await r.get(f'{cid}:upfakeHolder:{target.id}:{Dev_FINAL}')
            if not holder:
                return
            if holder != rank_name:
                # الاسم المكتوب ما يطابق رتبة هذا العضو، نتجاهل (قد تكون رسالة عادية)
                return
            if not await gowner_pls(uid, cid, c):
                return await m.reply(plugins_upfake_324(k, OWNER_DENY))

            await r.delete(f'{cid}:upfakeHolder:{target.id}:{Dev_FINAL}')
            await r.delete(f'{cid}:upfakePerms:{target.id}:{Dev_FINAL}')
            await r.srem(f'{cid}:upfakeHolders:{Dev_FINAL}', target.id)

            mention = target.mention() if hasattr(target, 'mention') else target.first_name
            return await m.reply(plugins_upfake_331(mention, holder))
        return

    # ---------------------------------------------------------------
    # تنزيل عام <الاسم> — يشيل الاسم العام (Dev² فقط، بالرد)
    # مثال: تنزيل عام اسطوري
    # ---------------------------------------------------------------
    if text.startswith('تنزيل عام '):
        new_name = text[len('تنزيل عام '):].strip()
        if new_name:
            target = await _get_target_from_reply(m)
            if not target:
                return
            old_name = await r.get(f'{target.id}:upfakeGlobalName:{Dev_FINAL}')
            if not old_name:
                return
            if old_name != new_name:
                return
            if not await dev2_pls(uid, cid, c):
                return await m.reply(plugins_upfake_350(k, DEV2_DENY))

            await r.delete(f'{target.id}:upfakeGlobalName:{Dev_FINAL}')
            mention = target.mention() if hasattr(target, 'mention') else target.first_name
            return await m.reply(plugins_upfake_354(mention, old_name))
        return

    # ---------------------------------------------------------------
    # تعديل صلاحياته — يفتح محرر الصلاحيات بنفس الحالة الحالية (نعم تبقى نعم
    # ولا تبقى لا)، بدون تصفير الصلاحيات كما يصير بأمر الرفع من جديد
    # ---------------------------------------------------------------
    if text == 'تعديل صلاحياته':
        if not await gowner_pls(uid, cid, c):
            return await m.reply(plugins_upfake_363(k, OWNER_DENY))
        target = await _get_target_from_reply(m)
        if not target:
            return await m.reply(plugins_upfake_366(k))

        holder = await r.get(f'{cid}:upfakeHolder:{target.id}:{Dev_FINAL}')
        if not holder:
            return await m.reply(plugins_upfake_370(k))

        current = await r.hgetall(f'{cid}:upfakePerms:{target.id}:{Dev_FINAL}') or {}
        current = {**{key: '0' for key, _ in UPFAKE_PERMS}, **current}

        mention = target.mention() if hasattr(target, 'mention') else target.first_name
        text_out = (
            f"• المستخدم ↤︎「 {mention} 」\n"
            f"• رتبته ↢ {holder}\n\n"
            f"{k} تحرير صلاحيات العضو:"
        )
        return await m.reply(text_out, reply_markup=_perms_keyboard(target.id, current))

    return


# ------------------------------------------------------------------------
# محرر الصلاحيات بالازرار
# ------------------------------------------------------------------------

@Client.on_callback_query(filters.regex(r'^ufperm_'), group=-1420)
async def handle_upfake_perm_buttons(c: Client, cb: CallbackQuery):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    if not cb.message:
        return
    chat_id = cb.message.chat.id

    if not await gowner_pls(cb.from_user.id, chat_id, c):
        return await cb.answer(OWNER_DENY, show_alert=True)

    try:
        action, target_raw = cb.data.split(':')
        target_id = int(target_raw)
    except Exception:
        return await cb.answer(REPLIES['plugins_owners_399'], show_alert=True)

    holder = await r.get(f'{chat_id}:upfakeHolder:{target_id}:{Dev_FINAL}')
    if not holder:
        try:
            await cb.message.edit_reply_markup(None)
        except Exception:
            pass
        return await cb.answer(REPLIES['plugins_upfake_413'], show_alert=True)

    perm_key = action[len('ufperm_'):]

    if perm_key == 'done':
        try:
            await cb.message.edit_reply_markup(None)
        except Exception:
            pass
        return await cb.answer(REPLIES['plugins_upfake_422'], show_alert=True)

    if perm_key not in UPFAKE_PERM_MAP:
        return await cb.answer(REPLIES['plugins_upfake_425'], show_alert=True)

    current = await r.hgetall(f'{chat_id}:upfakePerms:{target_id}:{Dev_FINAL}') or {}
    new_val = '0' if str(current.get(perm_key, '0')) == '1' else '1'
    await r.hset(f'{chat_id}:upfakePerms:{target_id}:{Dev_FINAL}', perm_key, new_val)
    current[perm_key] = new_val

    try:
        await cb.message.edit_reply_markup(_perms_keyboard(target_id, current))
    except Exception as e:
        if 'MESSAGE_NOT_MODIFIED' not in str(e):
            raise e
    await cb.answer()


# ------------------------------------------------------------------------
# الرفع التلقائي عبر توب المتفاعلين (بعد عداد الرسائل مباشرة، group=-723)
# ------------------------------------------------------------------------

@Client.on_message(filters.group, group=-722)
async def upfakeAutoPromote(c: Client, m: Message):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    k = await r.get(f'{Dev_FINAL}:botkey') or '•'

    if not m.from_user or m.from_user.is_bot:
        return
    if not m.text and not m.caption:
        return

    chat_id = m.chat.id
    uid = m.from_user.id

    if not await r.get(f'{chat_id}:upfakeAutoEnabled:{Dev_FINAL}'):
        return

    thresholds = await r.hgetall(f'{chat_id}:upfakeAutoThresholds:{Dev_FINAL}')
    if not thresholds:
        return

    if not await claim_event_once(f'upfakeauto:{Dev_FINAL}:{chat_id}:{m.id}'):
        return

    msgs = int((await r.get(f'{Dev_FINAL}{chat_id}:TotalMsgs:{uid}')) or 0)
    if msgs <= 0:
        return

    for tier in AUTO_TIERS_ORDER:
        threshold = thresholds.get(tier)
        if not threshold:
            continue
        try:
            threshold = int(threshold)
        except Exception:
            continue
        if msgs < threshold:
            continue

        tier_info = AUTO_TIERS[tier]
        rank_key = f'{chat_id}:{tier_info["rank"]}:{uid}{Dev_FINAL}'
        if await r.get(rank_key):
            continue  # مرفوع لهذي الرتبة مسبقاً

        # استثناء: اذا العضو اصلاً عنده رتبة ادارية تساوي او اعلى من الرتبة
        # المستهدفة، ما نرفعه (رفعه لرتبة اقل من رتبته الحالية غلط)
        checker = TIER_RANK_CHECK.get(tier)
        if checker and await checker(uid, chat_id, c):
            continue

        await r.sadd(f'{chat_id}:{tier_info["list"]}:{Dev_FINAL}', uid)
        await r.set(rank_key, '1')

        try:
            mention = m.from_user.mention()
        except Exception:
            mention = m.from_user.first_name

        gowner_block = await _build_gowner_mentions(c, r, chat_id, Dev_FINAL)
        header = f"• للمالكين الاساسين\n━━━━━━━━━━━━\n{gowner_block}\n━━━━━━━━━━━━\n" if gowner_block else ""

        try:
            await m.reply(
                plugins_upfake_507(header, mention, msgs, tier)
            )
        except Exception:
            pass
