from helpers.context import get_global_r, get_global_dev, get_global_k
from compat import InlineKeyboardMarkup, InlineKeyboardButton
from helpers.redis import r
import random, re, time
from .utils import safe_int, enforce_balance_cap
from helpers.replies_store import (
    plugins_games_shop_104,
    plugins_games_shop_108,
    plugins_games_shop_112,
    plugins_games_shop_117,
    plugins_games_shop_126,
    plugins_games_shop_135,
    plugins_games_shop_137,
    plugins_games_shop_146,
    plugins_games_shop_157,
    plugins_games_shop_158,
    plugins_games_shop_170,
    plugins_games_shop_172,
    plugins_games_shop_176,
    plugins_games_shop_179,
    plugins_games_shop_182,
    plugins_games_shop_189,
    plugins_games_shop_197,
    plugins_games_shop_200,
    plugins_games_shop_205,
    plugins_games_shop_208,
    plugins_games_shop_215,
    plugins_games_shop_244,
    plugins_games_shop_255,
    plugins_games_shop_266,
    plugins_games_shop_271,
    plugins_games_shop_274,
    plugins_games_shop_276,
    plugins_games_shop_281,
    plugins_games_shop_288,
    plugins_games_shop_301,
    plugins_games_shop_306,
    plugins_games_shop_309,
    plugins_games_shop_312,
    plugins_games_shop_321,
    plugins_games_shop_386,
    plugins_games_shop_393,
    plugins_games_shop_397,
    plugins_games_shop_401,
    plugins_games_shop_405,
    plugins_games_shop_412,
    plugins_games_shop_414,
    plugins_games_shop_416,
    plugins_games_shop_420,
    plugins_games_shop_425,
    plugins_games_shop_434,
    plugins_games_shop_457,
    plugins_games_shop_460,
    plugins_games_shop_463,
    plugins_games_shop_466,
    plugins_games_shop_469,
    plugins_games_shop_471,
    plugins_games_shop_487,
    plugins_games_shop_495,
    plugins_games_shop_505,
    plugins_games_shop_510,
    plugins_games_shop_512,
    plugins_games_shop_517,
    plugins_games_shop_519,
    plugins_games_shop_521,
    plugins_games_shop_524,
    plugins_games_shop_529,
    plugins_games_shop_563,
    plugins_games_shop_565,
    plugins_games_shop_569,
    plugins_games_shop_576,
)

LOAN_MIN = 3000000
LOAN_MAX = 2000000000
LOAN_DURATION = 10800
LOAN_MAX_BALANCE = 600000

STOCK_BASE_PRICE = 100
STOCK_MIN_PCT = -30
STOCK_MAX_PCT = 30
STOCK_REFRESH = 3600
STOCK_PCT_KEY = 'stock:global_pct'

STOCK_TRADE_COOLDOWN = 120
PSHOP_RESERVE_COOLDOWN = 120

PSHOP_DEFAULT_PRICE = 150
PSHOP_SELL_FLAT = 10
PSHOP_ZRF_COOLDOWN = 900
PSHOP_MAX_NAME_LEN = 20

PSHOP_OWNER_KEY = 'pshop_item_owner'


def _clean_name(name):
    return name.replace("*", "").replace("`", "").replace("|", "").replace("#", "").replace("<", "").replace(">", "").replace("_", "")


async def _display_name(user_id, tg_user=None):
    name_raw = await r.get(f'{user_id}:bankName')
    if name_raw:
        name = name_raw
    elif tg_user is not None:
        name = tg_user.first_name
    else:
        name = str(user_id)
    return _clean_name(name)


def _fmt_wait(seconds):
    seconds = max(0, int(seconds))
    return time.strftime('%M:%S', time.gmtime(seconds))


def _now_date():
    return time.strftime('%Y/%m/%d', time.localtime())


def _now_time():
    return time.strftime('%I:%M%p', time.localtime())


def _parse_qty_name(text):
    text_clean = re.sub(r'[^\w\s]', '', text)
    parts = text_clean.split()
    if len(parts) < 3:
        return None, None
    qty_str = ''.join(filter(str.isdigit, parts[1]))
    if not qty_str:
        return None, None
    qty = int(qty_str)
    name = _clean_name(" ".join(parts[2:]).strip())
    if not name:
        return None, None
    return qty, name


async def is_user_jailed(rc, user_id):
    debt = safe_int((await rc.get(f'{user_id}:LoanDebt')) or 0)
    if debt <= 0:
        return False
    deadline = safe_int((await rc.get(f'{user_id}:LoanDeadline')) or 0)
    return time.time() >= deadline


JAIL_BLOCKED_EXACT = {
    'استثمار فلوسي', 'حظ فلوسي', 'كنز', 'بخشيش', 'راتب', 'زرف',
    'مضاربه', 'بدء المراهنه', 'بدا المراهنه', 'تبرعاتي',
    'سعر الاسهم', 'اسهمي', 'متجري', 'اخفاء متجري',
    'فتح بيع', 'قفل بيع', 'زرف اغراضه', 'متجره',
    'اطعام الحيوانات', 'حذف الحيوانات', 'حذف مزرعتي', 'مسح مزرعتي',
    'مهام المزرعه', 'مهام المزرعة', 'نهب',
}

JAIL_BLOCKED_PREFIXES = (
    'استثمار ', 'حظ ', 'مضاربه ', 'مراهنه', 'انا ',
    'شراء ', 'بيع ', 'اهداء ', 'حجز ', 'ضع سعر ', 'تبرع ',
    'زراعة ', 'زراعه ', 'حصاد ', 'استكشاف ', 'جمع منتجات ',
    'انشاء مزرعه ', 'انشاء مزرعة ',
)


def jail_should_block(text):
    if text in JAIL_BLOCKED_EXACT:
        return True
    return text.startswith(JAIL_BLOCKED_PREFIXES)


async def handle_loan_commands(c, m, k, text):
    user_id = m.from_user.id

    if text == 'قرض':
        if not await r.sismember('BankList', user_id):
            return await m.reply(plugins_games_shop_104(k))
        debt = safe_int((await r.get(f'{user_id}:LoanDebt')) or 0)
        if debt > 0:
            if await is_user_jailed(r, user_id):
                return await m.reply(plugins_games_shop_108(k, k))
            return await m.reply(plugins_games_shop_112(k, k, debt))
        balance = safe_int((await r.get(f'{user_id}:Floos')) or 0)
        if balance > LOAN_MAX_BALANCE:
            return await m.reply(plugins_games_shop_117(k, LOAN_MAX_BALANCE, k, balance))
        amount = random.randint(LOAN_MIN, LOAN_MAX)
        deadline = int(time.time()) + LOAN_DURATION
        await r.set(f'{user_id}:LoanDebt', amount)
        await r.set(f'{user_id}:LoanDeadline', deadline)
        current_floos = safe_int((await r.get(f'{user_id}:Floos')) or 0)
        await r.set(f'{user_id}:Floos', current_floos + amount)
        await enforce_balance_cap(r, m, k, user_id)
        name = await _display_name(user_id, m.from_user)
        return await m.reply(plugins_games_shop_126(k, name, amount))

    if text == 'سجني':
        debt = safe_int((await r.get(f'{user_id}:LoanDebt')) or 0)
        if debt <= 0:
            return await m.reply(plugins_games_shop_135(k))
        if await is_user_jailed(r, user_id):
            return await m.reply(plugins_games_shop_137(k, k, debt, k))
        deadline = safe_int((await r.get(f'{user_id}:LoanDeadline')) or 0)
        remaining = deadline - int(time.time())
        h, rem = divmod(max(0, remaining), 3600)
        mnt, sec = divmod(rem, 60)
        return await m.reply(plugins_games_shop_146(k, h, mnt, sec))

    if text == 'ديوني':
        debt = safe_int((await r.get(f'{user_id}:LoanDebt')) or 0)
        if debt <= 0:
            return await m.reply(plugins_games_shop_157(k))
        return await m.reply(plugins_games_shop_158(k, debt, k, k))

    if text == 'ديونه':
        if not m.reply_to_message or not m.reply_to_message.from_user:
            return None
        target = m.reply_to_message.from_user
        debt = safe_int((await r.get(f'{target.id}:LoanDebt')) or 0)
        if debt <= 0:
            return await m.reply(plugins_games_shop_170(k))
        name = await _display_name(target.id, target)
        return await m.reply(plugins_games_shop_172(k, name, debt))

    if text == 'سداد ديوني':
        if not await r.sismember('BankList', user_id):
            return await m.reply(plugins_games_shop_176(k))
        debt = safe_int((await r.get(f'{user_id}:LoanDebt')) or 0)
        if debt <= 0:
            return await m.reply(plugins_games_shop_179(k))
        balance = safe_int((await r.get(f'{user_id}:Floos')) or 0)
        if balance < debt:
            return await m.reply(plugins_games_shop_182(k, k, debt, k, balance))
        await r.set(f'{user_id}:Floos', balance - debt)
        await r.delete(f'{user_id}:LoanDebt')
        await r.delete(f'{user_id}:LoanDeadline')
        return await m.reply(plugins_games_shop_189(k, k, debt))

    if text == 'سداد ديونه':
        if not m.reply_to_message or not m.reply_to_message.from_user:
            return None
        if not await r.sismember('BankList', user_id):
            return await m.reply(plugins_games_shop_197(k))
        target = m.reply_to_message.from_user
        if target.id == user_id:
            return await m.reply(plugins_games_shop_200(k, k))
        debt = safe_int((await r.get(f'{target.id}:LoanDebt')) or 0)
        if debt <= 0:
            return await m.reply(plugins_games_shop_205(k))
        balance = safe_int((await r.get(f'{user_id}:Floos')) or 0)
        if balance < debt:
            return await m.reply(plugins_games_shop_208(k, k, debt, k, balance))
        await r.set(f'{user_id}:Floos', balance - debt)
        await r.delete(f'{target.id}:LoanDebt')
        await r.delete(f'{target.id}:LoanDeadline')
        return await m.reply(plugins_games_shop_215(k, k, debt))

    return None


async def _get_stock_state():
    pct_raw = await r.get(STOCK_PCT_KEY)
    if pct_raw is None:
        pct = random.randint(STOCK_MIN_PCT, STOCK_MAX_PCT)
        await r.set(STOCK_PCT_KEY, pct, ex=STOCK_REFRESH)
        ttl = STOCK_REFRESH
    else:
        pct = safe_int(pct_raw)
        ttl = await r.ttl(STOCK_PCT_KEY)
        if not ttl or ttl < 0:
            ttl = STOCK_REFRESH
    price = int(round(STOCK_BASE_PRICE * (1 + pct / 100)))
    return pct, price, ttl


async def handle_stock_commands(c, m, k, text):
    user_id = m.from_user.id

    if text == 'سعر الاسهم':
        pct, price, ttl = await _get_stock_state()
        emoji = '📈' if pct >= 0 else '📉'
        wait = _fmt_wait(ttl)
        return await m.reply(plugins_games_shop_244(k, k, pct, k, emoji, k, price, wait))

    if text == 'اسهمي':
        stocks = safe_int((await r.get(f'{user_id}:stocks')) or 0)
        return await m.reply(plugins_games_shop_255(k, k, stocks, k, k))

    if text.startswith('شراء اسهم'):
        if await r.get(f'{user_id}:stock_buy_cd'):
            ttl = await r.ttl(f'{user_id}:stock_buy_cd')
            wait = _fmt_wait(ttl)
            return await m.reply(plugins_games_shop_266(k, k, wait))
        nums = re.findall(r'[0-9]+', text[len('شراء اسهم'):])
        if not nums:
            return await m.reply(plugins_games_shop_271(k))
        quantity = int(nums[0])
        if quantity <= 0:
            return await m.reply(plugins_games_shop_274(k))
        if not await r.sismember('BankList', user_id):
            return await m.reply(plugins_games_shop_276(k))
        pct, price, ttl = await _get_stock_state()
        total = price * quantity
        balance = safe_int((await r.get(f'{user_id}:Floos')) or 0)
        if balance < total:
            return await m.reply(plugins_games_shop_281(k, total, balance))
        new_balance = balance - total
        await r.set(f'{user_id}:Floos', new_balance)
        await enforce_balance_cap(r, m, k, user_id)
        new_stocks = safe_int((await r.get(f'{user_id}:stocks')) or 0) + quantity
        await r.set(f'{user_id}:stocks', new_stocks)
        await r.set(f'{user_id}:stock_buy_cd', 1, ex=STOCK_TRADE_COOLDOWN)
        return await m.reply(plugins_games_shop_288(k, k, quantity, k, price, k, total, new_balance))

    if text.startswith('بيع اسهم'):
        if await r.get(f'{user_id}:stock_sell_cd'):
            ttl = await r.ttl(f'{user_id}:stock_sell_cd')
            wait = _fmt_wait(ttl)
            return await m.reply(plugins_games_shop_301(k, k, wait))
        nums = re.findall(r'[0-9]+', text[len('بيع اسهم'):])
        if not nums:
            return await m.reply(plugins_games_shop_306(k))
        quantity = int(nums[0])
        if quantity <= 0:
            return await m.reply(plugins_games_shop_309(k))
        stocks = safe_int((await r.get(f'{user_id}:stocks')) or 0)
        if stocks < quantity:
            return await m.reply(plugins_games_shop_312(k, quantity, stocks))
        pct, price, ttl = await _get_stock_state()
        total = price * quantity
        new_stocks = stocks - quantity
        await r.set(f'{user_id}:stocks', new_stocks)
        balance = safe_int((await r.get(f'{user_id}:Floos')) or 0) + total
        await r.set(f'{user_id}:Floos', balance)
        await enforce_balance_cap(r, m, k, user_id)
        await r.set(f'{user_id}:stock_sell_cd', 1, ex=STOCK_TRADE_COOLDOWN)
        return await m.reply(plugins_games_shop_321(k, k, quantity, k, price, k, total, balance))

    return None


async def _pshop_price(owner_id, name):
    price_raw = await r.hget(f'{owner_id}:pshop_prices', name)
    if not price_raw:
        return PSHOP_DEFAULT_PRICE
    return safe_int(price_raw, PSHOP_DEFAULT_PRICE)


async def _format_pshop(owner_id, header, empty_text):
    items = await r.hgetall(f'{owner_id}:pshop_items')
    lines = []
    idx = 1
    for name, qty in items.items():
        qty_num = safe_int(qty)
        if qty_num <= 0:
            continue
        price = await _pshop_price(owner_id, name)
        lines.append(f"{idx} - {name} ↤︎ ( {price} ﷼) ↤︎ {qty_num}")
        idx += 1
    if not lines:
        return empty_text
    return f"{header}\n\n" + "\n".join(lines)


async def _resolve_item_owner(name):
    """
    يرجع معرف صاحب الحجز الحالي لغرض بالاسم المعطى، أو None إذا كان الغرض متاحاً
    للحجز من جديد (لا يوجد صاحب سابق، أو نفذت كميته بالكامل عند صاحبه سواء
    بالبيع أو بالزرف الكامل - عندها تُفقد الحصرية تلقائياً وتُحذف من السجل).
    """
    owner_raw = await r.hget(PSHOP_OWNER_KEY, name)
    owner_id = safe_int(owner_raw)
    if owner_id <= 0:
        return None
    owned_qty = safe_int(await r.hget(f'{owner_id}:pshop_items', name))
    if owned_qty <= 0:
        await r.hdel(PSHOP_OWNER_KEY, name)
        return None
    return owner_id


async def handle_personal_shop_commands(c, m, k, text):
    user_id = m.from_user.id

    if text == 'متجري':
        name = await _display_name(user_id, m.from_user)
        header = f"{k} أهلا بك {name} في متجرك الخاص  :"
        return await m.reply(await _format_pshop(user_id, header, f'{k} متجرك فارغ'))

    if text == 'متجره':
        if not m.reply_to_message or not m.reply_to_message.from_user:
            return None
        target = m.reply_to_message.from_user
        if await r.get(f'{target.id}:pshop_hidden'):
            return await m.reply(plugins_games_shop_386(k))
        name = await _display_name(target.id, target)
        header = f"{k} متجر {name} :"
        return await m.reply(await _format_pshop(target.id, header, f'{k} متجره فارغ'))

    if text == 'اخفاء متجري':
        await r.set(f'{user_id}:pshop_hidden', 1)
        return await m.reply(plugins_games_shop_393(k))
    
    if text == 'اظهار متجري':
        await r.delete(f'{user_id}:pshop_hidden')
        return await m.reply(plugins_games_shop_397(k))

    if text == 'قفل بيع':
        await r.set(f'{user_id}:pshop_locked', 1)
        return await m.reply(plugins_games_shop_401(k))

    if text == 'فتح بيع':
        await r.delete(f'{user_id}:pshop_locked')
        return await m.reply(plugins_games_shop_405(k))

    if text == 'زرف اغراضه':
        if not m.reply_to_message or not m.reply_to_message.from_user:
            return None
        target = m.reply_to_message.from_user
        if target.id == user_id:
            return await m.reply(plugins_games_shop_412(k))
        if target.is_bot:
            return await m.reply(plugins_games_shop_414(k))
        if not await r.sismember('BankList', user_id):
            return await m.reply(plugins_games_shop_416(k))
        if await r.get(f'{user_id}:pshop_zrf_cd'):
            ttl = await r.ttl(f'{user_id}:pshop_zrf_cd')
            wait = _fmt_wait(ttl)
            return await m.reply(plugins_games_shop_420(k, k, wait))
        items = await r.hgetall(f'{target.id}:pshop_items')
        available = [(name, safe_int(qty)) for name, qty in items.items() if safe_int(qty) > 0]
        if not available:
            return await m.reply(plugins_games_shop_425(k))
        name, qty_owned = random.choice(available)
        stolen_qty = random.randint(1, qty_owned)
        await r.hincrby(f'{target.id}:pshop_items', name, -stolen_qty)
        remaining = safe_int(await r.hget(f'{target.id}:pshop_items', name))
        if remaining <= 0:
            await r.hdel(f'{target.id}:pshop_items', name)
        await r.hincrby(f'{user_id}:pshop_items', name, stolen_qty)
        await r.set(f'{user_id}:pshop_zrf_cd', 1, ex=PSHOP_ZRF_COOLDOWN)
        await m.reply(plugins_games_shop_434(k, k, name, k, stolen_qty))
        thief_name = await _display_name(user_id, m.from_user)
        dm_text = f"""{k} هالشخص زرفك ↤︎ {thief_name}
{k} الغرض ↤︎ {name}
{k} الكمية ↤︎ {stolen_qty}

{k} التاريخ ↤︎ {_now_date()}
{k} الساعة ↤︎ {_now_time()}
-"""
        try:
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(m.chat.title, url=m.link)]])
            await c.send_message(target.id, dm_text, reply_markup=reply_markup)
        except Exception:
            pass
        return

    if text.startswith('ضع سعر '):
        text_clean = re.sub(r'[^\w\s]', '', text)
        parts = text_clean.split()
        if len(parts) < 4:
            return await m.reply(plugins_games_shop_457(k))
        price_str = ''.join(filter(str.isdigit, parts[-1]))
        if not price_str:
            return await m.reply(plugins_games_shop_460(k))
        price = int(price_str)
        if price <= 0:
            return await m.reply(plugins_games_shop_463(k))
        name = _clean_name(" ".join(parts[2:-1]).strip())
        if not name:
            return await m.reply(plugins_games_shop_466(k))
        owned = safe_int(await r.hget(f'{user_id}:pshop_items', name))
        if owned <= 0:
            return await m.reply(plugins_games_shop_469(k))
        await r.hset(f'{user_id}:pshop_prices', name, price)
        return await m.reply(plugins_games_shop_471(k, name, price))

    if text.startswith('حذف '):
        if text.startswith('حذف لعبه') or text.startswith('حذف تفاعل الرتب' ) or text.startswith('حذف ردي') or text.startswith('حذف رده') or text.startswith('حذف رسائلي') or text.startswith('حذف تكليجاتي')  or text.startswith('حذف رتبه') or text.startswith('حذف امر') or text.startswith('حذف حسابي'):
            return None
        text_clean = re.sub(r'[^\w\s]', '', text)
        parts = text_clean.split()
        if len(parts) < 2:
            return None
        name = _clean_name(" ".join(parts[1:]).strip())
        if not name:
            return None
        if len(name) > PSHOP_MAX_NAME_LEN:
            return None
        owned = safe_int(await r.hget(f'{user_id}:pshop_items', name))
        if owned <= 0:
            return 
        total = PSHOP_SELL_FLAT
        await r.hdel(f'{user_id}:pshop_items', name)
        await r.hdel(f'{user_id}:pshop_prices', name)
        balance = safe_int((await r.get(f'{user_id}:Floos')) or 0) + total
        await r.set(f'{user_id}:Floos', balance)
        await enforce_balance_cap(r, m, k, user_id)
        return await m.reply(plugins_games_shop_495(k, name, k, total))

    if text.startswith('حجز '):
        if text.startswith('حجز لاعب'):
            return None
        if await r.get(f'{user_id}:pshop_reserve_cd'):
            ttl = await r.ttl(f'{user_id}:pshop_reserve_cd')
            wait = _fmt_wait(ttl)
            return await m.reply(plugins_games_shop_505(k, k, wait))
        qty, name = _parse_qty_name(text)
        if qty is None:
            return await m.reply(plugins_games_shop_510(k))
        if qty <= 0:
            return await m.reply(plugins_games_shop_512(k))

        if m.reply_to_message and m.reply_to_message.from_user and m.reply_to_message.from_user.id != user_id:
            seller = m.reply_to_message.from_user
            if seller.is_bot:
                return await m.reply(plugins_games_shop_517(k))
            if not await r.sismember('BankList', user_id):
                return await m.reply(plugins_games_shop_519(k))
            if await r.get(f'{seller.id}:pshop_locked'):
                return await m.reply(plugins_games_shop_521(k))
            owned = safe_int(await r.hget(f'{seller.id}:pshop_items', name))
            if owned < qty:
                return await m.reply(plugins_games_shop_524(k, qty, name))
            price = await _pshop_price(seller.id, name)
            total = price * qty
            balance = safe_int((await r.get(f'{user_id}:Floos')) or 0)
            if balance < total:
                return await m.reply(plugins_games_shop_529(k, total, balance))
            await r.hincrby(f'{seller.id}:pshop_items', name, -qty)
            remaining = safe_int(await r.hget(f'{seller.id}:pshop_items', name))
            if remaining <= 0:
                await r.hdel(f'{seller.id}:pshop_items', name)
            await r.hincrby(f'{user_id}:pshop_items', name, qty)
            await r.set(f'{user_id}:Floos', balance - total)
            await enforce_balance_cap(r, m, k, user_id)
            await r.set(f'{user_id}:pshop_reserve_cd', 1, ex=PSHOP_RESERVE_COOLDOWN)
            seller_balance = safe_int((await r.get(f'{seller.id}:Floos')) or 0) + total
            await r.set(f'{seller.id}:Floos', seller_balance)
            await enforce_balance_cap(r, m, k, seller.id)
            buyer_name = await _display_name(user_id, m.from_user)
            seller_name = await _display_name(seller.id, seller)
            deal_text = f"""
{k} عملية شراء اغراض
{k} البايع ↤︎ {seller_name}
{k} المشتري ↤︎ {buyer_name}

{k} الغرض ↤︎ {name}
{k} الكمية ↤︎ {qty}
{k} بسعر ↤︎ {price}

{k} التاريخ ↤︎ {_now_date()}
{k} الساعة ↤︎ {_now_time()}
-"""
            await m.reply(deal_text)
            try:
                await c.send_message(seller.id, deal_text)
            except Exception:
                pass
            return

        if not await r.sismember('BankList', user_id):
            return await m.reply(plugins_games_shop_563(k))
        if len(name) > PSHOP_MAX_NAME_LEN:
            return await m.reply(plugins_games_shop_565(k, PSHOP_MAX_NAME_LEN))

        current_owner = await _resolve_item_owner(name)
        if current_owner is not None and current_owner != user_id:
            return await m.reply(plugins_games_shop_569(k, name))
        if current_owner is None:
            await r.hset(PSHOP_OWNER_KEY, name, user_id)

        await r.hincrby(f'{user_id}:pshop_items', name, qty)
        price = await _pshop_price(user_id, name)
        await r.set(f'{user_id}:pshop_reserve_cd', 1, ex=PSHOP_RESERVE_COOLDOWN)
        return await m.reply(plugins_games_shop_576(k, qty, k, name, k, price))

    return None