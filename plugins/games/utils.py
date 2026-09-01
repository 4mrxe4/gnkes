
from helpers.context import get_global_r, get_global_dev, get_global_k
from ..protect import _decode_if_bytes, claim_event_once, update_chat_title_cache, GLOBAL_TOP_NS
from helpers.redis import r as _shared_r
from helpers.replies_store import (
    plugins_games_utils_150,
    plugins_games_utils_80,
)



MAX_BALANCE = 9223369697402920999

OWNER_ONLY_ID = 5434703779


def is_owner_only(user_id) -> bool:
    """يتحقق أن المستخدم هو صاحب المعرف المخوّل الوحيد لأوامر الإدارة الحساسة."""
    try:
        return int(user_id) == OWNER_ONLY_ID
    except (TypeError, ValueError):
        return False


def safe_int(value, default: int = 0) -> int:
    """تحويل آمن لأي قيمة قادمة من Redis إلى int بدون رمي int(None)."""
    if value is None:
        return default
    try:
        if isinstance(value, bytes):
            value = value.decode('utf-8')
        return int(value)
    except (TypeError, ValueError):
        return default


async def grant_medal(r, user_id, reason: str = "تجاوز حد الفلوس"):
    """يمنح المستخدم ميدالية دائمة داخل قاعدة البيانات (نظام ميداليات جديد)."""
    import time as _time
    medal_entry = f"{reason}||{int(_time.time())}"
    try:
        await r.rpush(f'{user_id}:medals_list', medal_entry)
    except Exception:
        pass
    count = safe_int((await r.get(f'{user_id}:medals_count')) or 0) + 1
    await r.set(f'{user_id}:medals_count', count)
    return count


async def get_medals(r, user_id):
    """يرجع عدد الميداليات وقائمة تفاصيلها (إن وجدت) لمستخدم معيّن."""
    count = safe_int((await r.get(f'{user_id}:medals_count')) or 0)
    details = []
    try:
        raw_list = await r.lrange(f'{user_id}:medals_list', 0, -1)
        for item in raw_list or []:
            if isinstance(item, bytes):
                item = item.decode('utf-8')
            parts = item.split('||')
            reason = parts[0] if parts else 'تجاوز حد الفلوس'
            ts = parts[1] if len(parts) > 1 else None
            details.append({'reason': reason, 'ts': ts})
    except Exception:
        pass
    return count, details


async def enforce_balance_cap(r, m, k, user_id):
    """
    الدالة الموحّدة الوحيدة التي تُستدعى من كل مكان يزيد فيه رصيد أي مستخدم
    (بنك، ألعاب، راتب، تحويل، مكافأة، هدية، زواج ... الخ) للتحقق من عدم تجاوز
    MAX_BALANCE. إن تجاوزه الرصيد ولو بمقدار 1: يُصفَّر الرصيد فوراً، يُمنح
    المستخدم ميدالية واحدة، وتُرسل رسالة التنبيه الموحّدة.

    ترجع True إذا تم تصفير الرصيد (تجاوز الحد)، و False إذا كان الرصيد سليماً.
    """
    current = safe_int((await r.get(f'{user_id}:Floos')) or 0)
    if current <= MAX_BALANCE:
        return False
    await r.set(f'{user_id}:Floos', 0)
    await grant_medal(r, user_id)
    try:
        if m is not None:
            await m.reply(plugins_games_utils_80(k))
    except Exception:
        pass
    return True

async def add_game_earnings(user_id, chat_id, amount, event_id=None, chat_title=None):
    """
    تُسجَّل هنا أي مكافأة بنكية ناجحة ناتجة عن فوز بلعبة (عامة أو خاصة أو مستقبلية)،
    ضمن إحصائية 'المجموعات الأكثر لعباً' تلقائياً، دون أي حاجة لكود إضافي في كل لعبة.

    كل عملية تحصيل ناجحة (بغض النظر عن قيمة المبلغ المحصَّل) تُحتسب نقطة واحدة
    فقط في التوب - المبلغ يُستخدم فقط للتحقق من أن هناك ربحاً فعلياً (amount > 0)،
    ولا علاقة له بعدد النقاط المُحتسبة.

    event_id: مُعرّف فريد للحدث الفعلي (مثل m.id أو callback_query.id) - عند تمريره
    يتم منع تكرار الاحتساب لنفس الفوز إذا استُدعيت الدالة أكثر من مرة (تعدد بوتات/هاندلرات).
    chat_title: اسم المجموعة إن كان متوفراً لدى المستدعي، لتحديث الاسم المعروض في التوب.
    """
    if amount <= 0:
        return

    if event_id is not None:
        if not await claim_event_once(f"gameearn:{chat_id}:{event_id}"):
            return

    user_key = f'{user_id}:game_earnings:{GLOBAL_TOP_NS}'
    group_key = f'{chat_id}:game_earnings:{GLOBAL_TOP_NS}'
    await _shared_r.incrby(user_key, 1)
    new_group_total = await _shared_r.incrby(group_key, 1)

    if chat_title:
        await update_chat_title_cache(chat_id, chat_title)

    return new_group_total

async def get_game_earnings_top(limit=20):
    k = get_global_k()
    pattern = f"*:game_earnings:{GLOBAL_TOP_NS}"
    result = []
    async for key_raw in _shared_r.scan_iter(match=pattern, count=100):
        key = _decode_if_bytes(key_raw)
        try:
            parts = key.split(":game_earnings:")
            if len(parts) >= 2:
                chat_id = int(parts[0].rsplit(':', 1)[-1])
                if chat_id >= 0:
                    continue
                earnings = int(await _shared_r.get(key_raw) or 0)
                if earnings > 0:
                    title = await _shared_r.get(f'{chat_id}:chat_title:{GLOBAL_TOP_NS}')
                    if not title:
                        title = f"مجموعة {chat_id}"
                    elif isinstance(title, bytes):
                        title = title.decode('utf-8')
                    result.append({
                        "chat_id": chat_id,
                        "title": title,
                        "earnings": earnings
                    })
        except Exception as e:
            print(f"خطأ في جلب توب الألعاب: {e}")
    result.sort(key=lambda x: x["earnings"], reverse=True)
    return result[:limit]

async def show_game_earnings_top(c, m, k):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    data = await get_game_earnings_top(20)
    if not data:
        return await m.reply(plugins_games_utils_150(k))
    
    # تعريف text هنا بقيمة فارغة
    text = ""
    emojis = ["🥇", "🥈", "🥉"]
    for i, group in enumerate(data[:20]):
        emoji = emojis[i] if i < 3 else f"{i+1:>4})"
        title = group["title"][:35]
        earnings = group["earnings"]
        text += f"{emoji} {earnings:,} l {title}\n"
    
    my_rank = None
    my_earnings = 0
    for i, group in enumerate(data):
        if group["chat_id"] == m.chat.id:
            my_rank = i + 1
            my_earnings = group["earnings"]
            break
    
    if my_rank:
        text += f"\n• مركز مجموعتك ↤︎ {my_rank} \n• نقاط مجموعتك ↤︎ {my_earnings:,}"
    
    # إرسال النص النهائي
    await m.reply(text)
