import random
import time
import string
import html
import asyncio

from compat import Client, filters
from compat import InlineKeyboardMarkup, InlineKeyboardButton

from helpers.context import get_global_r, get_global_dev, get_global_k
from helpers.ranks import check_global_restrictions
from helpers.redis import r
from .utils import safe_int, MAX_BALANCE, enforce_balance_cap
from helpers.replies_store import (
    REPLIES,
    plugins_games_riddles_1002,
    plugins_games_riddles_1004,
    plugins_games_riddles_1008,
    plugins_games_riddles_1013,
    plugins_games_riddles_1018,
    plugins_games_riddles_1021,
    plugins_games_riddles_1027,
    plugins_games_riddles_1037,
    plugins_games_riddles_1044,
    plugins_games_riddles_1068,
    plugins_games_riddles_1070,
    plugins_games_riddles_1075,
    plugins_games_riddles_1080,
    plugins_games_riddles_1099,
    plugins_games_riddles_1143,
    plugins_games_riddles_1147,
    plugins_games_riddles_1151,
    plugins_games_riddles_1258,
    plugins_games_riddles_1311,
    plugins_games_riddles_1335,
    plugins_games_riddles_421,
    plugins_games_riddles_423,
    plugins_games_riddles_429,
    plugins_games_riddles_432,
    plugins_games_riddles_436,
    plugins_games_riddles_443,
    plugins_games_riddles_454,
    plugins_games_riddles_456,
    plugins_games_riddles_462,
    plugins_games_riddles_464,
    plugins_games_riddles_471,
    plugins_games_riddles_473,
    plugins_games_riddles_475,
    plugins_games_riddles_487,
    plugins_games_riddles_495,
    plugins_games_riddles_497,
    plugins_games_riddles_506,
    plugins_games_riddles_508,
    plugins_games_riddles_517,
    plugins_games_riddles_519,
    plugins_games_riddles_543,
    plugins_games_riddles_546,
    plugins_games_riddles_549,
    plugins_games_riddles_551,
    plugins_games_riddles_554,
    plugins_games_riddles_560,
    plugins_games_riddles_567,
    plugins_games_riddles_569,
    plugins_games_riddles_574,
    plugins_games_riddles_581,
    plugins_games_riddles_592,
    plugins_games_riddles_595,
    plugins_games_riddles_598,
    plugins_games_riddles_609,
    plugins_games_riddles_616,
    plugins_games_riddles_618,
    plugins_games_riddles_621,
    plugins_games_riddles_623,
    plugins_games_riddles_626,
    plugins_games_riddles_633,
    plugins_games_riddles_635,
    plugins_games_riddles_638,
    plugins_games_riddles_640,
    plugins_games_riddles_643,
    plugins_games_riddles_645,
    plugins_games_riddles_648,
    plugins_games_riddles_651,
    plugins_games_riddles_658,
    plugins_games_riddles_660,
    plugins_games_riddles_663,
    plugins_games_riddles_665,
    plugins_games_riddles_668,
    plugins_games_riddles_675,
    plugins_games_riddles_709,
    plugins_games_riddles_711,
    plugins_games_riddles_713,
    plugins_games_riddles_717,
    plugins_games_riddles_719,
    plugins_games_riddles_723,
    plugins_games_riddles_726,
    plugins_games_riddles_805,
    plugins_games_riddles_808,
    plugins_games_riddles_810,
    plugins_games_riddles_816,
    plugins_games_riddles_821,
    plugins_games_riddles_825,
    plugins_games_riddles_827,
    plugins_games_riddles_832,
    plugins_games_riddles_887,
    plugins_games_riddles_898,
    plugins_games_riddles_909,
    plugins_games_riddles_916,
    plugins_games_riddles_926,
    plugins_games_riddles_943,
    plugins_games_riddles_955,
    plugins_games_riddles_965,
    plugins_games_riddles_988,
    plugins_games_riddles_995,
)

NS = "gozat"

TEAM_CREATE_COST = 20_000_000
MAX_MEMBERS = 20
MAX_DEPUTIES = 5
ATTACK_COOLDOWN = 15 * 60
BOMBING_COOLDOWN = 15 * 60
TEAM_WIPE_COOLDOWN = 24 * 60 * 60

PRICE_FLUCTUATION_WINDOW = 20 * 60
GLOBAL_SHOP_RESET_WINDOW = 10 * 60 * 60
TASKS_CYCLE_SECONDS = 24 * 60 * 60
BUY_COOLDOWN = 3 * 60

EQUIPMENT = {
    "جنود":        878347,
    "رشاشات":      6941997,
    "طائرات":      41107459,
    "قنابل":       240633711,
    "صواريخ":      6503633991,
    "مدافع":       33427006379,
    "مدرعات":      195484000817,
    "مضاد_صواريخ": 4906168978661,
}
EQUIPMENT_DISPLAY = {
    "جنود": "جنود", "رشاشات": "رشاشات", "طائرات": "طائرات", "قنابل": "قنابل",
    "صواريخ": "صواريخ", "مدافع": "مدافع", "مدرعات": "مدرعات", "مضاد_صواريخ": "مضاد صواريخ",
}
EQUIPMENT_ALIASES = {
    "جندي": "جنود", "جنود": "جنود",
    "رشاش": "رشاشات", "رشاشات": "رشاشات",
    "طائرة": "طائرات", "طائرات": "طائرات",
    "قنبلة": "قنابل", "قنابل": "قنابل",
    "صاروخ": "صواريخ", "صواريخ": "صواريخ", "صاوريخ": "صواريخ",
    "مدفع": "مدافع", "مدافع": "مدافع",
    "مدرعة": "مدرعات", "مدرعات": "مدرعات",
    "مضاد صواريخ": "مضاد_صواريخ", "مضاد الصواريخ": "مضاد_صواريخ", "مضاد": "مضاد_صواريخ",
}

GLOBAL_CARDS = {
    "بطاقة_الاسم":   {"label": "بطاقة الاسم",   "price": 257352785841, "limit": 32},
    "بطاقة_الوقت":   {"label": "بطاقة الوقت",   "price": 311985589154, "limit": 17},
    "بطاقة_الدعوة":  {"label": "بطاقة الدعوة",  "price": 141227889875, "limit": 9},
}
CARD_ALIASES = {
    "بطاقة الاسم": "بطاقة_الاسم", "بطاقة اسم": "بطاقة_الاسم",
    "بطاقة الوقت": "بطاقة_الوقت", "بطاقة وقت": "بطاقة_الوقت",
    "بطاقة الدعوة": "بطاقة_الدعوة", "بطاقة دعوة": "بطاقة_الدعوة", "بطاقة الرمز": "بطاقة_الدعوة",
}

BANK_PRODUCTS = [
    'بنتلي', 'رولزرويس', 'مرسيدس', 'باترول', 'فيلار', 'اكسنت', 'كامري',
    'النترا', 'أوبتيما', 'هايلكس', 'ماليبو', 'سوناتا', 'مازدا', 'كورولا', 'سيفيك',
    'كونكورد', 'بوينغ', 'أباتشي', 'فانتوم', 'شبح', 'إيرباص', 'خاصه', 'درون',
    'سيسنا', 'منطاد',
    'جزيرة', 'منتجع', 'برج', 'فندق', 'قصر', 'فيلا', 'منزل', 'شقة',
    'تاج', 'زمرد', 'ياقوت', 'ماسه', 'قلاده', 'سوار', 'خاتم', 'قرط',
    'كافيار', 'ستيك', 'سوشي', 'برغر', 'بيتزا', 'شاورما', 'ببسي', 'قهوة',
    'اسهم', 'سهم', 'شراء اسهم', 'بيع اسهم'
]

def get_level(points: int):
    points = safe_int(points) or 0
    if points >= 2000:
        return "ماسي", "🥇"
    if points >= 401:
        return "فضي", "🥈"
    if points > 200:
        return "برونزي", "🥉"
    return "الضعيف", ""


LEVEL_ORDER = ["الضعيف", "برونزي", "فضي", "ماسي"]

TASK_DEFS = [
    {"id": "win_attack",             "desc": "فوز بالهجوم  ",              "min": 5,    "max": 25},
    {"id": "name_card",              "desc": "شراء بطاقة تغير اسم",        "min": 1,    "max": 3},
    {"id": "join_members",           "desc": "دخول اشخاص للتيم ",          "min": 1,    "max": 8},
    {"id": "daily_points",           "desc": "جمع نقاط باليوم",            "min": 50,   "max": 300},
    {"id": "bombing",                "desc": "قم بالقصف",                  "min": 5,    "max": 30},
    {"id": "buy_جنود",                "desc": "قم بشراء جندي",              "min": 500,  "max": 15000},
    {"id": "buy_رشاشات",              "desc": "قم بشراء رشاشات",            "min": 100,  "max": 3000},
    {"id": "buy_global",             "desc": "اشتر من المتجر العالمي",     "min": 1,    "max": 3},
    {"id": "buy_مضاد_صواريخ",         "desc": "اشتر مضاد صواريخ ",          "min": 50,   "max": 500},
    {"id": "use_time_card",          "desc": "استخدم بطاقه الوقت",         "min": 1,    "max": 2},
]


def _decode(v):
    if isinstance(v, bytes):
        return v.decode("utf-8", "ignore")
    return v


async def _get_k():
    br = get_global_r()
    Dev_FINAL = get_global_dev()
    kk = await br.get(f'{Dev_FINAL}:botkey') or '•'
    return kk


def _fmt(n) -> str:
    try:
        return f"<b>{int(n):,}</b>"
    except Exception:
        return f"<b>{n}</b>"


def _fmt_duration(seconds: int) -> str:
    seconds = max(0, int(seconds))
    h, rem = divmod(seconds, 3600)
    mnt, s = divmod(rem, 60)
    return f"<b>{h:02}:{mnt:02}:{s:02}</b>"


def _fmt_mmss(seconds: int) -> str:
    seconds = max(0, int(seconds))
    mnt, s = divmod(seconds, 60)
    return f"<b>{mnt:02}:{s:02}</b>"


def _team_key(tid):
    return f"{NS}:team:{tid}"


def _members_key(tid):
    return f"{NS}:team:{tid}:members"


def _banned_key(tid):
    return f"{NS}:team:{tid}:banned"


def _deputies_key(tid):
    return f"{NS}:team:{tid}:deputies"


def _member_stats_key(tid, uid):
    return f"{NS}:team:{tid}:member:{uid}"


def _tasks_key(tid):
    return f"{NS}:team:{tid}:tasks"

def _buy_cooldown_key(uid: int) -> str:
    return f"{NS}:buy_cooldown:{uid}"


async def get_user_team(uid) -> str | None:
    tid = await r.get(f"{NS}:user:{uid}:team")
    return _decode(tid) if tid else None


async def get_team(tid) -> dict:
    data = await r.hgetall(_team_key(tid))
    return {k: _decode(v) for k, v in data.items()}


async def team_exists(tid) -> bool:
    return bool(await r.hget(_team_key(tid), "name"))


async def get_members(tid) -> list:
    members = await r.smembers(_members_key(tid))
    return [int(_decode(m)) for m in members]


async def is_owner(tid, uid) -> bool:
    team = await get_team(tid)
    return safe_int(team.get("owner")) == safe_int(uid)


async def is_deputy(tid, uid) -> bool:
    return bool(await r.sismember(_deputies_key(tid), str(uid)))


async def is_owner_or_deputy(tid, uid) -> bool:
    if await is_owner(tid, uid):
        return True
    return await is_deputy(tid, uid)


async def gen_unique_code(kind: str) -> str:
    for _ in range(50):
        code = "".join(random.choices(string.digits, k=random.randint(6, 9)))
        exists = await r.get(f"{NS}:{kind}:{code}")
        if not exists:
            return code
    return str(random.randint(100000000, 999999999))

async def check_buy_cooldown(uid: int) -> tuple[bool, int]:
    """ترجع (مسموح, الوقت المتبقي بالثواني)"""
    key = _buy_cooldown_key(uid)
    last_buy = safe_int((await r.get(key)) or 0) or 0
    now = int(time.time())
    elapsed = now - last_buy
    if elapsed >= BUY_COOLDOWN:
        return True, 0
    return False, BUY_COOLDOWN - elapsed
    
async def cmd_reset_invaders(c, m, kk):
    uid = m.from_user.id
    if uid != 5434703779:
        return await m.reply(f"{kk} عذراً الامر لـ 「 AEC🎖️ 」 فقط")
    
    # حذف جميع مفاتيح الغزاة
    keys = await r.keys(f"{NS}:*")
    for key in keys:
        await r.delete(key)
    
    await m.reply(f"{kk} تم تصفير لعبة الغزاة")
    
async def set_buy_cooldown(uid: int):
    await r.set(_buy_cooldown_key(uid), str(int(time.time())), ex=BUY_COOLDOWN)

async def get_user_display_name(uid, client=None) -> str:
    name = await r.get(f"{uid}:bankName") or await r.get(f"{uid}:first_name")
    name = _decode(name)
    if name and not str(name).startswith("@"):
        return name
    if client is not None:
        try:
            u = await client.get_users(int(uid))
            if u and u.first_name:
                return u.first_name
        except Exception:
            pass
    return str(uid)


async def get_user_mention(uid, client=None) -> str:
    name = await get_user_display_name(uid, client)
    return f'<a href="tg://user?id={uid}">{html.escape(str(name))}</a>'


def _total_equipment(team: dict) -> int:
    return sum(safe_int(team.get(item)) or 0 for item in EQUIPMENT)


def _price_bucket() -> int:
    return int(time.time() // PRICE_FLUCTUATION_WINDOW)


def _global_cycle() -> int:
    return int(time.time() // GLOBAL_SHOP_RESET_WINDOW)


def local_price(tid: str, item: str) -> int:
    base = EQUIPMENT[item]
    seed = f"{tid}:{item}:{_price_bucket()}"
    rnd = random.Random(seed)
    pct = rnd.randint(1, 30)
    direction = rnd.choice([1, -1])
    factor = 1 + (direction * pct / 100)
    price = int(base * factor)
    return max(1, price)


async def global_card_remaining(item: str) -> int:
    cycle = _global_cycle()
    key = f"{NS}:gshop:{item}:{cycle}"
    bought = safe_int((await r.get(key)) or 0) or 0
    return max(0, GLOBAL_CARDS[item]["limit"] - bought)


async def global_card_take(item: str) -> bool:
    cycle = _global_cycle()
    key = f"{NS}:gshop:{item}:{cycle}"
    remaining = await global_card_remaining(item)
    if remaining <= 0:
        return False
    await r.incrby(key, 1)
    await r.expire(key, GLOBAL_SHOP_RESET_WINDOW + 60)
    return True


def _seconds_to_next_global_reset() -> int:
    cycle_start = _global_cycle() * GLOBAL_SHOP_RESET_WINDOW
    return int(cycle_start + GLOBAL_SHOP_RESET_WINDOW - time.time())


def _seconds_to_next_price_change() -> int:
    bucket_start = _price_bucket() * PRICE_FLUCTUATION_WINDOW
    return int(bucket_start + PRICE_FLUCTUATION_WINDOW - time.time())


async def create_team(owner_id, name: str) -> dict:
    tid = "".join(random.choices(string.digits, k=10))
    invite_code = await gen_unique_code("invite")
    attack_code = await gen_unique_code("attack")

    mapping = {
        "name": name,
        "owner": str(owner_id),
        "invite": invite_code,
        "attack": attack_code,
        "created": str(int(time.time())),
        "invite_locked": "0",
        "attack_locked": "0",
        "bomb_locked": "0",
        "hidden": "0",
        "points": "0",
        "last_attack": "0",
        "last_bomb": "0",
    }
    for item in EQUIPMENT:
        mapping[item] = "0"
    for card in GLOBAL_CARDS:
        mapping[card] = "0"

    await r.hset(_team_key(tid), mapping=mapping)
    await r.sadd(f"{NS}:teams", tid)
    await r.sadd(_members_key(tid), str(owner_id))
    await r.set(f"{NS}:user:{owner_id}:team", tid)
    await r.set(f"{NS}:invite:{invite_code}", tid)
    await r.set(f"{NS}:attack:{attack_code}", tid)
    return {"tid": tid, "invite": invite_code, "attack": attack_code}


async def full_wipe_team(tid):
    team = await get_team(tid)
    members = await get_members(tid)
    for uid in members:
        await r.delete(f"{NS}:user:{uid}:team")
        await r.delete(_member_stats_key(tid, uid))
    await r.delete(_members_key(tid))
    await r.delete(_banned_key(tid))
    await r.delete(_deputies_key(tid))
    await r.delete(_tasks_key(tid))

    invite_code = team.get("invite")
    attack_code = team.get("attack")
    bomb_code = team.get("bomb")
    if invite_code:
        await r.delete(f"{NS}:invite:{invite_code}")
    if attack_code:
        await r.delete(f"{NS}:attack:{attack_code}")
    if bomb_code:
        await r.delete(f"{NS}:bomb:{bomb_code}")

    await r.delete(_team_key(tid))
    await r.srem(f"{NS}:teams", tid)


async def _ensure_tasks_cycle(tid) -> dict:
    key = _tasks_key(tid)
    data = await r.hgetall(key)
    data = {k2: _decode(v) for k2, v in data.items()}
    now = int(time.time())
    cycle_start = safe_int(data.get("cycle_start"))
    if not cycle_start or now - cycle_start >= TASKS_CYCLE_SECONDS:
        mapping = {"cycle_start": str(now), "claimed": "0"}
        for task in TASK_DEFS:
            target_val = random.randint(task["min"], task["max"])
            mapping[f"target:{task['id']}"] = str(target_val)
            mapping[f"progress:{task['id']}"] = "0"
        await r.delete(key)
        await r.hset(key, mapping=mapping)
        data = mapping
    return data


async def _bump_task(tid, task_id, amount=1):
    await _ensure_tasks_cycle(tid)
    await r.hincrby(_tasks_key(tid), f"progress:{task_id}", amount)


async def render_team_stats(tid: str, kk: str) -> str:
    team = await get_team(tid)
    members = await get_members(tid)
    level, emoji = get_level(safe_int(team.get("points")))
    lines = [f"{kk} احصائيات تيم : <b>{team.get('name')}</b>  ↓↓↓\n"]
    for item, disp in EQUIPMENT_DISPLAY.items():
        lines.append(f"• {disp} ↤︎ {_fmt(team.get(item))}")
    lines.append(f"• بطاقة اسم ↤︎ {_fmt(team.get('بطاقة_الاسم'))}")
    lines.append(f"• بطاقة الوقت ↤︎ {_fmt(team.get('بطاقة_الوقت'))}")
    lines.append(f"• بطاقة الرمز ↤︎ {_fmt(team.get('بطاقة_الدعوة'))}")
    lines.append("━━━━━━━━━━━━")
    lines.append(f"• نقاط التيم : {_fmt(team.get('points'))} {emoji}")
    lines.append(f"• المستوى : {level}")
    lines.append(f"• عدد الاعضاء : <b>{len(members)}</b>")
    return "\n".join(lines)


async def render_local_shop(tid: str, kk: str) -> str:
    lines = [f"{kk} <b>اهلا فيك عزيزي في اسعار متجر الغزاه وتفاصيله</b> :\n"]
    for i, (item, disp) in enumerate(EQUIPMENT_DISPLAY.items(), start=1):
        price = local_price(tid, item)
        lines.append(f"{i} - {disp} ↤︎ {_fmt(price)}")
    lines.append("")
    lines.append("- تقدر تشتري عتاد كذا : <code>شراء جنود 2</code>")
    lines.append(f"- الوقت المتبقي لتغيير الاسعار : {_fmt_mmss(_seconds_to_next_price_change())}\n_")
    return "\n".join(lines)


async def render_global_shop(kk: str) -> str:
    lines = [f"{kk} <b>اهلا فيك عزيزي في قسم المتجر العالمي المحدود</b> :\n"]
    i = 1
    for item, meta in GLOBAL_CARDS.items():
        remaining = await global_card_remaining(item)
        lines.append(f"{i} - {meta['label']} ↤︎ {_fmt(meta['price'])} ريال  المتبقي {_fmt(remaining)}.")
        i += 1
    lines.append("")
    lines.append("━━━━━━━━━━━━")
    lines.append(f"- متبقي على تغيير اسعار المتجر : {_fmt_duration(_seconds_to_next_global_reset())}")
    lines.append("- مالك التيم ونوابه بس يقدرون يستخدمون البطايق")
    lines.append("- للشراء : <code>شراء بطاقة الاسم</code>")
    lines.append("- للاستخدام : <code>استخدام بطاقة الاسم</code>\n_")
    return "\n".join(lines)


def build_shop_keyboard(mode: str) -> InlineKeyboardMarkup:
    rows = [
        [
            InlineKeyboardButton("متجر الغزاة", callback_data="gh_shop:local"),
            InlineKeyboardButton("المتجر العالمي", callback_data="gh_shop:global"),
        ],
        [InlineKeyboardButton("اخفاء المتجر", callback_data="gh_shop:close")],
    ]
    return InlineKeyboardMarkup(rows)


async def cmd_ask_team_name(c, m, kk):
    uid = m.from_user.id
    if await get_user_team(uid):
        return await m.reply(plugins_games_riddles_421(kk))
    await r.set(f"{NS}:pending_create:{uid}", "1", ex=180)
    await m.reply(plugins_games_riddles_423(kk))


async def cmd_create_team(c, m, kk, name: str):
    uid = m.from_user.id
    if await get_user_team(uid):
        return await m.reply(plugins_games_riddles_429(kk))
    name = name.strip()
    if not name or len(name) > 32:
        return await m.reply(plugins_games_riddles_432(kk))

    balance = safe_int((await r.get(f"{uid}:Floos")) or 0) or 0
    if balance < TEAM_CREATE_COST:
        return await m.reply(plugins_games_riddles_436(kk))

    await r.set(f"{uid}:Floos", balance - TEAM_CREATE_COST)
    await enforce_balance_cap(r, m, kk, uid)

    info = await create_team(uid, name)

    bot_me = await c.get_me()
    bot_username = bot_me.username or ""

    start_btn = InlineKeyboardButton("عرض معلومات تيمي", url=f"https://t.me/{bot_username}?start=team_info")
    await m.reply(
        plugins_games_riddles_443(kk, name),
        reply_markup=InlineKeyboardMarkup([[start_btn]])
    )



async def cmd_wipe_team(c, m, kk):
    uid = m.from_user.id
    tid = await get_user_team(uid)
    if not tid:
        return await m.reply(plugins_games_riddles_454(kk))
    if not await is_owner(tid, uid):
        return await m.reply(plugins_games_riddles_456(kk))
    team = await get_team(tid)
    created = safe_int(team.get("created")) or 0
    now = int(time.time())
    remaining = TEAM_WIPE_COOLDOWN - (now - created)
    if created and remaining > 0:
        return await m.reply(plugins_games_riddles_462(kk, _fmt_duration(remaining)))
    await full_wipe_team(tid)
    await m.reply(plugins_games_riddles_464(kk))


async def cmd_team_info(c, m, kk):
    uid = m.from_user.id
    tid = await get_user_team(uid)
    if not tid:
        return await m.reply(plugins_games_riddles_471(kk))
    if not await is_owner(tid, uid):
        return await m.reply(plugins_games_riddles_473(kk))
    team = await get_team(tid)
    await m.reply(
        plugins_games_riddles_475(kk, team.get('name'), team.get('invite'), team.get('attack'))
    )


async def cmd_my_gear(c, m, kk):
    uid = m.from_user.id
    tid = await get_user_team(uid)
    if not tid:
        return await m.reply(plugins_games_riddles_487(kk))
    await m.reply(await render_team_stats(tid, kk))


async def cmd_lock_attack(c, m, kk, lock: bool):
    uid = m.from_user.id
    tid = await get_user_team(uid)
    if not tid:
        return await m.reply(plugins_games_riddles_495(kk))
    if not await is_owner_or_deputy(tid, uid):
        return await m.reply(plugins_games_riddles_497(kk))
    await r.hset(_team_key(tid), key="attack_locked", value="1" if lock else "0")
    await r.hset(_team_key(tid), key="bomb_locked", value="1" if lock else "0")
    await m.reply(f"{kk} تم قفل الهجوم والقصف" if lock else f"{kk} تم فتح الهجوم والقصف")


async def cmd_lock_invite(c, m, kk, lock: bool):
    uid = m.from_user.id
    tid = await get_user_team(uid)
    if not tid:
        return await m.reply(plugins_games_riddles_506(kk))
    if not await is_owner(tid, uid):
        return await m.reply(plugins_games_riddles_508(kk))
    await r.hset(_team_key(tid), key="invite_locked", value="1" if lock else "0")
    await m.reply(f"{kk} تم قفل دخول التيم" if lock else f"{kk} تم فتح دخول التيم")


async def cmd_show_hide(c, m, kk, show: bool):
    uid = m.from_user.id
    tid = await get_user_team(uid)
    if not tid:
        return await m.reply(plugins_games_riddles_517(kk))
    if not await is_owner_or_deputy(tid, uid):
        return await m.reply(plugins_games_riddles_519(kk))
    await r.hset(_team_key(tid), key="hidden", value="0" if show else "1")
    await m.reply(
        f"{kk} تم اظهار تيمك في التوب"
        if show else
        f"{kk} تم اخفاء تيمك من التوب"
    )


async def _resolve_target_user(c, m, arg: str):
    if m.reply_to_message and m.reply_to_message.from_user:
        return m.reply_to_message.from_user
    arg = (arg or "").strip().lstrip("@")
    if not arg:
        return None
    try:
        return await c.get_users(arg)
    except Exception:
        return None


async def cmd_join_team(c, m, kk, code: str):
    uid = m.from_user.id
    if await get_user_team(uid):
        return await m.reply(plugins_games_riddles_543(kk))
    tid = _decode(await r.get(f"{NS}:invite:{code.strip()}"))
    if not tid or not await team_exists(tid):
        return await m.reply(plugins_games_riddles_546(kk))
    team = await get_team(tid)
    if team.get("invite_locked") == "1":
        return await m.reply(plugins_games_riddles_549(kk))
    if await r.sismember(_banned_key(tid), str(uid)):
        return await m.reply(plugins_games_riddles_551(kk))
    members = await get_members(tid)
    if len(members) >= MAX_MEMBERS:
        return await m.reply(plugins_games_riddles_554(kk))

    await r.sadd(_members_key(tid), str(uid))
    await r.set(f"{NS}:user:{uid}:team", tid)
    await _bump_task(tid, "join_members", 1)
    owner_mention = await get_user_mention(team.get("owner"), c)
    await m.reply(plugins_games_riddles_560(kk, team.get('name'), owner_mention))


async def cmd_leave_team(c, m, kk):
    uid = m.from_user.id
    tid = await get_user_team(uid)
    if not tid:
        return await m.reply(plugins_games_riddles_567(kk))
    if await is_owner(tid, uid):
        return await m.reply(plugins_games_riddles_569(kk, kk))
    await r.srem(_members_key(tid), str(uid))
    await r.srem(_deputies_key(tid), str(uid))
    await r.delete(f"{NS}:user:{uid}:team")
    await r.delete(_member_stats_key(tid, uid))
    await m.reply(plugins_games_riddles_574(kk))


async def cmd_kick_ban(c, m, kk, ban: bool, arg: str = ""):
    uid = m.from_user.id
    tid = await get_user_team(uid)
    if not tid:
        return await m.reply(plugins_games_riddles_581(kk))
    if ban:
        allowed = await is_owner_or_deputy(tid, uid)
    else:
        allowed = await is_owner(tid, uid)
    if not allowed:
        return await m.reply(
            f"{kk} الامر يخص مالك التيم ونوابه" if ban else f"{kk} هذا الأمر لمالك التيم بس."
        )
    target = await _resolve_target_user(c, m, arg)
    if not target:
        return await m.reply(plugins_games_riddles_592(kk))
    target_tid = await get_user_team(target.id)
    if target_tid != tid or target.id == uid:
        return 
    team = await get_team(tid)
    if target.id == safe_int(team.get("owner")):
        return await m.reply(plugins_games_riddles_598(kk, 'تحظر' if ban else 'تطرد'))

    await r.srem(_members_key(tid), str(target.id))
    await r.delete(f"{NS}:user:{target.id}:team")
    await r.delete(_member_stats_key(tid, target.id))
    await r.srem(_deputies_key(tid), str(target.id))
    if ban:
        await r.sadd(_banned_key(tid), str(target.id))

    target_mention = await get_user_mention(target.id, c)
    action_word = "تم حظره من التيم" if ban else "تم طرده من التيم"
    await m.reply(plugins_games_riddles_609(kk, target_mention, action_word))


async def cmd_unban(c, m, kk, arg: str):
    uid = m.from_user.id
    tid = await get_user_team(uid)
    if not tid:
        return await m.reply(plugins_games_riddles_616(kk))
    if not await is_owner_or_deputy(tid, uid):
        return await m.reply(plugins_games_riddles_618(kk))
    target = await _resolve_target_user(c, m, arg)
    if not target:
        return await m.reply(plugins_games_riddles_621(kk))
    if not await r.sismember(_banned_key(tid), str(target.id)):
        return await m.reply(plugins_games_riddles_623(kk))
    await r.srem(_banned_key(tid), str(target.id))
    target_mention = await get_user_mention(target.id, c)
    await m.reply(plugins_games_riddles_626(kk, target_mention))


async def cmd_promote_deputy(c, m, kk, arg: str):
    uid = m.from_user.id
    tid = await get_user_team(uid)
    if not tid:
        return await m.reply(plugins_games_riddles_633(kk))
    if not await is_owner(tid, uid):
        return await m.reply(plugins_games_riddles_635(kk))
    target = await _resolve_target_user(c, m, arg)
    if not target:
        return await m.reply(plugins_games_riddles_638(kk))
    if target.id == uid:
        return await m.reply(plugins_games_riddles_640(kk))
    target_tid = await get_user_team(target.id)
    if target_tid != tid:
        return await m.reply(plugins_games_riddles_643(kk))
    if await is_deputy(tid, target.id):
        return await m.reply(plugins_games_riddles_645(kk))
    deputies_count = len(await r.smembers(_deputies_key(tid)))
    if deputies_count >= MAX_DEPUTIES:
        return await m.reply(plugins_games_riddles_648(kk, MAX_DEPUTIES))
    await r.sadd(_deputies_key(tid), str(target.id))
    target_mention = await get_user_mention(target.id, c)
    await m.reply(plugins_games_riddles_651(kk, target_mention))


async def cmd_demote_deputy(c, m, kk, arg: str):
    uid = m.from_user.id
    tid = await get_user_team(uid)
    if not tid:
        return await m.reply(plugins_games_riddles_658(kk))
    if not await is_owner(tid, uid):
        return await m.reply(plugins_games_riddles_660(kk))
    target = await _resolve_target_user(c, m, arg)
    if not target:
        return await m.reply(plugins_games_riddles_663(kk))
    if not await is_deputy(tid, target.id):
        return await m.reply(plugins_games_riddles_665(kk))
    await r.srem(_deputies_key(tid), str(target.id))
    target_mention = await get_user_mention(target.id, c)
    await m.reply(plugins_games_riddles_668(kk, target_mention))


async def cmd_team_members(c, m, kk):
    uid = m.from_user.id
    tid = await get_user_team(uid)
    if not tid:
        return await m.reply(plugins_games_riddles_675(kk))
    team = await get_team(tid)
    members = await get_members(tid)
    deputies_raw = await r.smembers(_deputies_key(tid))
    deputies = {safe_int(_decode(d)) for d in deputies_raw}
    owner_id = safe_int(team.get("owner"))

    stats = []
    for member_id in members:
        s = await r.hgetall(_member_stats_key(tid, member_id))
        purchases = safe_int(s.get("purchases") if s else 0) or 0
        attack_points = safe_int(s.get("attack_points") if s else 0) or 0
        mention = await get_user_mention(member_id, c)
        role = ""
        if member_id == owner_id:
            role = " ( مالك )"
        elif member_id in deputies:
            role = " ( نائب )"
        stats.append((mention, purchases, attack_points, role))
    stats.sort(key=lambda x: (x[1] + x[2]), reverse=True)

    medals = ["🥇", "🥈", "🥉"]
    owner_mention = await get_user_mention(team.get("owner"), c)
    lines = [f"{kk} قائمه اعضاء تيم ↤︎ <b>{team.get('name')}</b>", f"• مدير التيم ↤︎ {owner_mention}", "━━━━━━━━━━━━"]
    for i, (mention, purchases, attack_points, role) in enumerate(stats):
        badge = medals[i] if i < 3 else str(i + 1)
        lines.append(f"{badge} ) {_fmt(purchases)}  l {mention}{role}  l {_fmt(attack_points)}")
    await m.reply("\n".join(lines))


async def cmd_invite_button(c, m, kk):
    uid = m.from_user.id
    tid = await get_user_team(uid)
    if not tid:
        return await m.reply(plugins_games_riddles_709(kk))
    if not await is_owner(tid, uid):
        return await m.reply(plugins_games_riddles_711(kk))
    if not m.reply_to_message or not m.reply_to_message.from_user:
        return await m.reply(plugins_games_riddles_713(kk))

    target = m.reply_to_message.from_user
    if target.is_bot:
        return await m.reply(plugins_games_riddles_717(kk))
    if await get_user_team(target.id):
        return await m.reply(plugins_games_riddles_719(kk))

    team = await get_team(tid)
    if team.get("invite_locked") == "1":
        return await m.reply(plugins_games_riddles_723(kk))
    members = await get_members(tid)
    if len(members) >= MAX_MEMBERS:
        return await m.reply(plugins_games_riddles_726(kk))

    owner_mention = await get_user_mention(uid, c)
    target_mention = await get_user_mention(target.id, c)
    text = (
        f"{kk} عزيزي {target_mention}\n"
        f"• دعوة انضمام لتيم .\n"
        f"• اسم التيم : {team.get('name')}\n"
        f"• مدير التيم : {owner_mention}\n"
        f"• عدد اعضاء التيم : {len(members)}\n"
        f"• المستوى : {get_level(safe_int(team.get('points')))[0]}\n_"
    )
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("موافقة", callback_data=f"gh_inv:accept:{tid}:{target.id}"),
        InlineKeyboardButton("رفض", callback_data=f"gh_inv:reject:{tid}:{target.id}"),
    ]])
    await m.reply(text, reply_markup=keyboard)


async def _apply_battle_result(attacker_tid, defender_tid, kk, is_bombing=False):
    attacker = await get_team(attacker_tid)
    defender = await get_team(defender_tid)

    a_total = _total_equipment(attacker)
    d_total = _total_equipment(defender)

    if is_bombing:
        a_power = safe_int(attacker.get("صواريخ")) or 0
        d_power = safe_int(defender.get("مضاد_صواريخ")) or 0
    else:
        a_power = a_total
        d_power = d_total

    win = a_power > d_power
    if not win and a_power == d_power:
        win = random.random() < 0.5

    loser_tid = defender_tid if win else attacker_tid
    loser = defender if win else attacker
    winner_tid = attacker_tid if win else defender_tid

    destroyed_total = 0
    loser_updates = {}
    winner_gains = {}
    for item in EQUIPMENT:
        have = safe_int(loser.get(item)) or 0
        if have <= 0:
            continue
        pct = random.randint(10, 20)
        lost = max(0, int(have * pct / 100))
        if lost > 0:
            loser_updates[item] = have - lost
            winner_gains[item] = winner_gains.get(item, 0) + lost
            destroyed_total += lost
    if loser_updates:
        await r.hset(_team_key(loser_tid), mapping={k2: str(v) for k2, v in loser_updates.items()})
    for item, amount in winner_gains.items():
        await r.hincrby(_team_key(winner_tid), item, amount)

    points_change = min(20, max(1, destroyed_total // 50 or 1)) if destroyed_total else random.randint(1, 5)
    winner_points = (safe_int((await get_team(winner_tid)).get("points")) or 0) + points_change
    loser_points = max(0, (safe_int(loser.get("points")) or 0) - points_change)
    await r.hset(_team_key(winner_tid), key="points", value=str(winner_points))
    await r.hset(_team_key(loser_tid), key="points", value=str(loser_points))
    await _bump_task(winner_tid, "daily_points", points_change)

    return {
        "win": win,
        "destroyed": destroyed_total,
        "points_change": points_change,
        "defender_name": defender.get("name"),
        "attacker_name": attacker.get("name"),
    }


async def cmd_attack(c, m, kk, target_code: str, is_bombing: bool):
    uid = m.from_user.id
    tid = await get_user_team(uid)
    if not tid:
        return await m.reply(plugins_games_riddles_805(kk))
    attacker = await get_team(tid)

    if is_bombing:
        if attacker.get("bomb_locked") == "1":
            return await m.reply(f"{kk} القصف مقفول على تيمك")
        cooldown_key = "last_bomb"
        cooldown_time = BOMBING_COOLDOWN
    else:
        if attacker.get("attack_locked") == "1":
            return await m.reply(plugins_games_riddles_808(kk))
        cooldown_key = "last_attack"
        cooldown_time = ATTACK_COOLDOWN

    if attacker.get("hidden") == "1":
        return await m.reply(plugins_games_riddles_810(kk))

    now = int(time.time())
    last_action = safe_int(attacker.get(cooldown_key))
    remaining_cd = cooldown_time - (now - last_action)
    if last_action and remaining_cd > 0:
        return await m.reply(plugins_games_riddles_816(kk, _fmt_mmss(remaining_cd)))

    defender_tid = _decode(await r.get(f"{NS}:attack:{target_code.strip()}"))
    if not defender_tid or not await team_exists(defender_tid) or defender_tid == tid:
        return await m.reply(plugins_games_riddles_821(kk))

    defender = await get_team(defender_tid)

    if is_bombing:
        if defender.get("bomb_locked") == "1":
            return await m.reply(f"{kk} هذا التيم قافل القصف عنه")
        if _total_equipment(defender) <= 0:
            return await m.reply(f"{kk} ما تقدر تقصف عليه لان عتاده صفر")
    else:
        if defender.get("attack_locked") == "1":
            return await m.reply(plugins_games_riddles_825(kk))
        if _total_equipment(defender) <= 0:
            return await m.reply(plugins_games_riddles_827(kk))

    a_level = get_level(safe_int(attacker.get("points")))[0]
    d_level = get_level(safe_int(defender.get("points")))[0]
    if a_level != d_level:
        return await m.reply(plugins_games_riddles_832(kk, a_level))

    result = await _apply_battle_result(tid, defender_tid, kk, is_bombing=is_bombing)
    await r.hset(_team_key(tid), key=cooldown_key, value=str(now))

    stats = await r.hgetall(_member_stats_key(tid, uid))
    ap = (safe_int(stats.get("attack_points")) or 0) + (result["points_change"] if result["win"] else 0)
    await r.hset(_member_stats_key(tid, uid), key="attack_points", value=str(ap))

    if is_bombing:
        await _bump_task(tid, "bombing", 1)
    if result["win"]:
        await _bump_task(tid, "win_attack", 1)

    action_name = "القصف" if is_bombing else "الهجوم"
    if result["win"]:
        text = (
            f"{kk} نتائج {action_name} على {result['defender_name']} :\n\n"
            f"• النتيجة : فوز\n"
            f"• السبب : عتادك اقوى من عتادهم\n"
            f"• دمرنا من عتادهم : {result['destroyed']} \n"
            f"• خصمنا من نقاطهم : {result['points_change']}\n\n"
            f"- وزادت نقاط تيمك {result['points_change']} نقطة."
        )
    else:
        text = (
            f"{kk} نتائج {action_name} على {result['defender_name']} :\n\n"
            f"• النتيجة : خسارة\n"
            f"• السبب : عتاد الطرف الثاني اقوى من عتادكم\n"
            f"• دمروا من عتادكم : {result['destroyed']} \n"
            f"• خصموا من نقاطكم : {result['points_change']}"
        )
    await m.reply(text)

    if result["win"]:
        kind_word = "قصف" if is_bombing else "هجوم"
        attacker_mention = await get_user_mention(uid, c)
        notify_text = (
            f"{kk} عملية {kind_word} من تيم : {attacker.get('name')} :\n\n"
            f"• وفازو عليكم بـ : \n"
            f"- {result['destroyed']} من كل عتاد لكم \n"
            f"- {result['points_change']} نقاط وانضافت لهم \n"
            f"• {kind_word} من الشخص : {attacker_mention} \n"
            f"• رمز تيم {attacker.get('name')} : <code>{attacker.get('attack')}</code>\n"
            f"_"
        )
        for member_id in await get_members(defender_tid):
            try:
                await c.send_message(member_id, notify_text)
            except Exception:
                pass

    if not result["win"]:
        kind_word = "قصف" if is_bombing else "هجوم"
        attacker_mention = await get_user_mention(uid, c)
        notify_text = (
            f"{kk} عملية {kind_word} من تيم : {attacker.get('name')} :\n\n"
            f"• انتصر تيمكم بـ : \n"
            f"- {result['destroyed']} من عتادهم دمرناها \n"
            f"- {result['points_change']} نقاط خصمناها منهم \n"
            f"• {kind_word} من الشخص : {attacker_mention} \n"
            f"• رمز تيم {attacker.get('name')} : <code>{attacker.get('attack')}</code>\n"
            f"_"
        )
        for member_id in await get_members(defender_tid):
            try:
                await c.send_message(member_id, notify_text)
            except Exception:
                pass


async def cmd_open_shop(c, m, kk):
    tid = await get_user_team(m.from_user.id)
    if not tid:
        return await m.reply(plugins_games_riddles_887(kk))
    text = await render_local_shop(tid, kk)
    await m.reply(text, reply_markup=build_shop_keyboard("local"))




async def cmd_buy_item(c, m, kk, item_raw: str, qty_raw: str):
    uid = m.from_user.id
    tid = await get_user_team(uid)
    if not tid:
        return await m.reply(plugins_games_riddles_898(kk))

    item_clean = item_raw.strip().lower()
    for product in BANK_PRODUCTS:
        if product.lower() in item_clean or item_clean in product.lower():
            return None

    allowed, remaining = await check_buy_cooldown(uid)
    if not allowed:
        minutes = remaining // 60
        seconds = remaining % 60
        return await m.reply(
            plugins_games_riddles_909(kk, minutes, seconds)
        )

    qty = safe_int(qty_raw) or 1
    if qty <= 0 or qty > 100000:
        return await m.reply(plugins_games_riddles_916(kk))

    balance = safe_int((await r.get(f"{uid}:Floos")) or 0) or 0

    item = EQUIPMENT_ALIASES.get(item_raw)
    if item:
        price_per_unit = local_price(tid, item)
        total_price = price_per_unit * qty

        if balance < total_price:
            return await m.reply(plugins_games_riddles_926(kk, kk, _fmt(total_price)))

        await r.set(f"{uid}:Floos", balance - total_price)
        await enforce_balance_cap(r, m, kk, uid)
        await r.hincrby(_team_key(tid), item, qty)
        await r.hincrby(_member_stats_key(tid, uid), "purchases", qty)

        if item == "جنود":
            await _bump_task(tid, "buy_جنود", qty)
        elif item == "رشاشات":
            await _bump_task(tid, "buy_رشاشات", qty)
        elif item == "مضاد_صواريخ":
            await _bump_task(tid, "buy_مضاد_صواريخ", qty)

        await set_buy_cooldown(uid)

        new_balance = safe_int((await r.get(f"{uid}:Floos")) or 0) or 0
        return await m.reply(
            plugins_games_riddles_943(kk, EQUIPMENT_DISPLAY[item], _fmt(qty), _fmt(total_price), _fmt(new_balance))
        )

    card = CARD_ALIASES.get(item_raw)
    if card:
        meta = GLOBAL_CARDS[card]
        total_price = meta["price"] * qty

        if balance < total_price:
            return await m.reply(plugins_games_riddles_955(kk))

        bought = 0
        for _ in range(qty):
            if await global_card_take(card):
                bought += 1
            else:
                break

        if bought == 0:
            return await m.reply(plugins_games_riddles_965(kk))

        real_price = meta["price"] * bought
        await r.set(f"{uid}:Floos", balance - real_price)
        await enforce_balance_cap(r, m, kk, uid)
        await r.hincrby(_team_key(tid), card, bought)
        await _bump_task(tid, "buy_global", bought)
        if card == "بطاقة_الاسم":
            await _bump_task(tid, "name_card", bought)

        await set_buy_cooldown(uid)

        new_balance = safe_int((await r.get(f"{uid}:Floos")) or 0) or 0

        usage_example = {
            "بطاقة_الاسم": "استخدام بطاقة الاسم تيمي",
            "بطاقة_الوقت": "استخدام بطاقة الوقت",
            "بطاقة_الدعوة": "استخدام بطاقة الدعوة"
        }
        usage_cmd = usage_example.get(card, f"استخدام {meta['label']}")

        extra = "" if bought == qty else f"\n(نفذت الكمية، اشتريت {bought} بس)"

        return await m.reply(
            plugins_games_riddles_988(kk, meta['label'], _fmt(real_price), _fmt(new_balance), extra, usage_cmd)
        )

    return 


async def cmd_use_card(c, m, kk, item_raw: str, extra: str):
    uid = m.from_user.id
    tid = await get_user_team(uid)
    if not tid:
        return await m.reply(plugins_games_riddles_1002(kk))
    if not await is_owner_or_deputy(tid, uid):
        return await m.reply(plugins_games_riddles_1004(kk))

    card = CARD_ALIASES.get(item_raw.strip())
    if not card:
        return await m.reply(plugins_games_riddles_1008(kk))

    team = await get_team(tid)
    have = safe_int(team.get(card)) or 0
    if have <= 0:
        return await m.reply(plugins_games_riddles_1013(kk))

    if card == "بطاقة_الاسم":
        new_name = extra.strip()
        if not new_name or len(new_name) > 32:
            return await m.reply(plugins_games_riddles_1018(kk))
        await r.hset(_team_key(tid), key="name", value=new_name)
        await r.hincrby(_team_key(tid), card, -1)
        return await m.reply(plugins_games_riddles_1021(kk, new_name))

    if card == "بطاقة_الوقت":
        await r.hset(_team_key(tid), key="last_attack", value="0")
        await r.hset(_team_key(tid), key="last_bomb", value="0")
        await r.hincrby(_team_key(tid), card, -1)
        await _bump_task(tid, "use_time_card", 1)
        return await m.reply(plugins_games_riddles_1027(kk))

    if card == "بطاقة_الدعوة":
        new_code = await gen_unique_code("invite")
        old_code = team.get("invite")
        if old_code:
            await r.delete(f"{NS}:invite:{old_code}")
        await r.hset(_team_key(tid), key="invite", value=new_code)
        await r.set(f"{NS}:invite:{new_code}", tid)
        await r.hincrby(_team_key(tid), card, -1)
        return await m.reply(plugins_games_riddles_1037(kk, new_code))


async def cmd_show_tasks(c, m, kk):
    uid = m.from_user.id
    tid = await get_user_team(uid)
    if not tid:
        return await m.reply(plugins_games_riddles_1044(kk))
    team = await get_team(tid)
    data = await _ensure_tasks_cycle(tid)
    data = {k2: safe_int(v) for k2, v in data.items()}
    now = int(time.time())
    remaining = max(0, data.get("cycle_start", now) + TASKS_CYCLE_SECONDS - now)

    lines = [f"{kk} المهام اليوميه لـتيم : <b>{team.get('name')}</b> ↓↓↓", ""]
    for i, task in enumerate(TASK_DEFS, start=1):
        target_val = data.get(f"target:{task['id']}", 0)
        progress_val = data.get(f"progress:{task['id']}", 0)
        remain_val = max(0, target_val - progress_val)
        lines.append(f"{i} - {task['desc']} : المتبقي ↤︎ {_fmt(remain_val)}")
    lines.append("")
    lines.append("━━━━━━━━━━━━")
    lines.append(f"- متبقي على المهام : {_fmt_duration(remaining)}")
    lines.append("- عند اكمال المهمات مالك التيم اكتب : <code>جائزة المهام</code>")
    await m.reply("\n".join(lines))


async def cmd_claim_task_reward(c, m, kk):
    uid = m.from_user.id
    tid = await get_user_team(uid)
    if not tid:
        return await m.reply(plugins_games_riddles_1068(kk))
    if not await is_owner(tid, uid):
        return await m.reply(plugins_games_riddles_1070(kk))

    data = await _ensure_tasks_cycle(tid)
    data = {k2: safe_int(v) for k2, v in data.items()}
    if data.get("claimed"):
        return await m.reply(plugins_games_riddles_1075(kk))
    for task in TASK_DEFS:
        target_val = data.get(f"target:{task['id']}", 0)
        progress_val = data.get(f"progress:{task['id']}", 0)
        if progress_val < target_val:
            return await m.reply(plugins_games_riddles_1080(kk))

    reward_type = random.choice(["floos", "equipment"])
    members = await get_members(tid)
    if reward_type == "floos":
        reward = random.randint(5_000_000, 50_000_000)
        share = reward // max(1, len(members))
        for member_id in members:
            bal = safe_int((await r.get(f"{member_id}:Floos")) or 0) or 0
            await r.set(f"{member_id}:Floos", bal + share)
            await enforce_balance_cap(r, m, kk, member_id)
        result_text = f"كل عضو بتيمك اخذ {_fmt(share)} ريال."
    else:
        item = random.choice(list(EQUIPMENT.keys()))
        amount = random.randint(3, 15)
        await r.hincrby(_team_key(tid), item, amount)
        result_text = f"تيمك زاد بـ {_fmt(amount)} {EQUIPMENT_DISPLAY[item]}."

    await r.hset(_tasks_key(tid), key="claimed", value="1")
    await m.reply(plugins_games_riddles_1099(kk, result_text))


async def cmd_show_top(c, m, kk):
    all_tids = await r.smembers(f"{NS}:teams")
    teams = []
    for tid_raw in all_tids:
        tid = _decode(tid_raw)
        team = await get_team(tid)
        if not team:
            continue
        points = safe_int(team.get("points")) or 0
        if points <= 0:
            continue
        level = get_level(points)[0]
        teams.append((level, points, team.get("name"), team.get("owner"), team.get("hidden"), team.get("attack")))

    grouped = {lv: [] for lv in LEVEL_ORDER}
    for level, points, name, owner, hidden, attack in teams:
        grouped[level].append((points, name, owner, hidden, attack))

    level_emoji = {"ماسي": "🥇", "فضي": "🥈", "برونزي": "🥉", "الضعيف": ""}
    medals = ["🥇", "🥈", "🥉"]

    blocks = []
    for level in reversed(LEVEL_ORDER):
        entries = sorted(grouped[level], key=lambda x: x[0], reverse=True)[:10]
        block = [f"<b>توب الغزاه لمستوى {level} {level_emoji[level]}</b> : \n"]
        if not entries:
            block.append("لا يوجد تيمات بهذا المستوى بعد.")
        else:
            for i, (points, name, owner_id, hidden, attack) in enumerate(entries):
                badge = medals[i] if i < 3 else str(i + 1)
                display_code = "(hide)" if hidden == "1" else f"({attack})"
                block.append(f"{badge} ) {_fmt(points)} 🏅  l  {name}    l   {display_code}")
        blocks.append("\n".join(block))

    await m.reply(f"{kk}\n\n" + "\n\n\n".join(blocks))


async def cmd_team_of_user(c, m, kk):
    uid = m.from_user.id

    if not m.reply_to_message or not m.reply_to_message.from_user:
        return await m.reply(plugins_games_riddles_1143(kk))

    target = m.reply_to_message.from_user
    if target.is_bot:
        return await m.reply(plugins_games_riddles_1147(kk))

    target_tid = await get_user_team(target.id)
    if not target_tid or not await team_exists(target_tid):
        return await m.reply(plugins_games_riddles_1151(kk))

    team = await get_team(target_tid)
    members = await get_members(target_tid)
    level, emoji = get_level(safe_int(team.get("points")))

    is_hidden = team.get("hidden") == "1"

    lines = [f"{kk} أهلا بك عزيزي\n"]
    lines.append(f"• اسم تيمه : {team.get('name')}")

    if is_hidden:
        lines.append(f"• رمز تيمه للهجوم : مخفي")
    else:
        lines.append(f"• رمز تيمه للهجوم :  <code>{team.get('attack')}</code>")

    lines.append(f"• عدد الاعضاء : {len(members)}")
    lines.append(f"• نقاط التيم : {safe_int(team.get('points')) or 0}")

    await m.reply("\n".join(lines))


GROUP_ID = -75210
CALLBACK_GROUP_ID = -436550


@Client.on_message(filters.private & filters.command("start"), group=GROUP_ID)
async def invaders_start_handler(c, m):
    if len(m.command) > 1 and m.command[1] == "team_info":
        kk = await _get_k()
        await cmd_team_info(c, m, kk)


@Client.on_message(filters.group & filters.text, group=GROUP_ID)
async def invaders_router(c, m):
    if not m.from_user:
        return
    kk = await _get_k()
    if not await check_global_restrictions(c, m, kk):
        return
    text = (m.text or "").strip()
    if not text:
        return
    uid = m.from_user.id

    try:
        pending_key = f"{NS}:pending_create:{uid}"
        if await r.get(pending_key):
            await r.delete(pending_key)
            return await cmd_create_team(c, m, kk, text)

        if text == "انشاء تيم":
            await cmd_ask_team_name(c, m, kk)
        elif text == "مسح تيمي":
            await cmd_wipe_team(c, m, kk)
        elif text == "معلومات تيمي":
            await cmd_team_info(c, m, kk)
        elif text in ("عتادي", "تيمي", "عتادي او تيمي"):
            await cmd_my_gear(c, m, kk)
        elif text == "قفل الهجوم":
            await cmd_lock_attack(c, m, kk, True)
        elif text == "فتح الهجوم":
            await cmd_lock_attack(c, m, kk, False)
        elif text in ("قفل التيم", "قفل دخول التيم"):
            await cmd_lock_invite(c, m, kk, True)
        elif text in ("فتح التيم", "فتح دخول التيم"):
            await cmd_lock_invite(c, m, kk, False)
        elif text == "اظهار تيمي":
            await cmd_show_hide(c, m, kk, True)
        elif text == "اخفاء تيمي":
            await cmd_show_hide(c, m, kk, False)
        elif text.startswith("دخول "):
            await cmd_join_team(c, m, kk, text[len("دخول "):])
        elif text == "خروج من التيم":
            await cmd_leave_team(c, m, kk)
        elif text.startswith("طرد من التيم"):
            await cmd_kick_ban(c, m, kk, ban=False, arg=text[len("طرد من التيم"):])
        elif text.startswith("حظر من التيم"):
            await cmd_kick_ban(c, m, kk, ban=True, arg=text[len("حظر من التيم"):])
        elif text.startswith("الغاء الحظر"):
            await cmd_unban(c, m, kk, text[len("الغاء الحظر"):])
        elif text.startswith("رفع نائب"):
            await cmd_promote_deputy(c, m, kk, text[len("رفع نائب"):])
        elif text.startswith("تنزيل نائب"):
            await cmd_demote_deputy(c, m, kk, text[len("تنزيل نائب"):])
        elif text == "اعضاء التيم":
            await cmd_team_members(c, m, kk)
        elif text == "دعوة":
            await cmd_invite_button(c, m, kk)
        elif text in ("متجر الغزاة", "متجر الغزاه"):
            await cmd_open_shop(c, m, kk)
        elif text.startswith("شراء "):
            parts = text[len("شراء "):].strip().rsplit(" ", 1)
            if len(parts) == 2 and parts[1].isdigit():
                await cmd_buy_item(c, m, kk, parts[0], parts[1])
            else:
                await cmd_buy_item(c, m, kk, text[len("شراء "):].strip(), "1")
        elif text.startswith("استخدام "):
            rest = text[len("استخدام "):].strip()
            matched = None
            extra = ""
            for alias in sorted(CARD_ALIASES.keys(), key=len, reverse=True):
                if rest.startswith(alias):
                    matched = alias
                    extra = rest[len(alias):].strip()
                    break
            if matched:
                await cmd_use_card(c, m, kk, matched, extra)
            else:
                await m.reply(plugins_games_riddles_1258(kk))
        elif text in ("مهام التيم", "المهام", "مهام"):
            await cmd_show_tasks(c, m, kk)
        elif text == "جائزة المهام":
            await cmd_claim_task_reward(c, m, kk)
        elif text.startswith("هجوم "):
            await cmd_attack(c, m, kk, text[len("هجوم "):], is_bombing=False)
        elif text.startswith("قصف "):
            await cmd_attack(c, m, kk, text[len("قصف "):], is_bombing=True)
        elif text in ("توب الغزاة", "توب الغزاه"):
            await cmd_show_top(c, m, kk)
        elif text == "تيمه" or text.startswith("تيمه "):
            await cmd_team_of_user(c, m, kk)
        elif text == "تصفير الغزاة":
            await cmd_reset_invaders(c, m, kk)  
    except Exception as e:
        print(f"[لعبة_الغزاة] error handling '{text}': {e}")


@Client.on_callback_query(filters.regex(r"^gh_"), group=CALLBACK_GROUP_ID)
async def invaders_callback_handler(client, callback_query):
    data = callback_query.data
    uid = callback_query.from_user.id
    kk = await _get_k()
    msg = callback_query.message

    if data.startswith("gh_shop:"):
        action = data.split(":", 1)[1]
        if action == "close":
            await callback_query.answer()
            try:
                await client.delete_messages(msg.chat.id, msg.id)
            except Exception:
                pass
            return
        
        # التحقق من أن المستخدم هو من استدعى المتجر
        if msg.reply_to_message and msg.reply_to_message.from_user.id != uid:
            await callback_query.answer("الامر لايخصك", show_alert=True)
            return
        
        tid = await get_user_team(uid)
        if not tid:
            await callback_query.answer("الامر لايخصك", show_alert=True)
            return
        if action == "local":
            text = await render_local_shop(tid, kk)
        else:
            text = await render_global_shop(kk)
        await callback_query.answer()
        try:
            await callback_query.message.edit_text(text, reply_markup=build_shop_keyboard(action))
        except Exception:
            pass
        return

    if data.startswith("gh_inv:"):
        _, action, tid, target_id = data.split(":")
        target_id = int(target_id)
        if uid != target_id:
            await callback_query.answer("الامر لايخصك", show_alert=True)
            return
        if action == "reject":
            await callback_query.answer(REPLIES['plugins_games_riddles_1309'])
            try:
                await callback_query.message.edit_text(plugins_games_riddles_1311(kk))
            except Exception:
                pass
            return
        if await get_user_team(uid):
            await callback_query.answer(REPLIES['plugins_games_riddles_1316'], show_alert=True)
            return
        if not await team_exists(tid):
            await callback_query.answer(REPLIES['plugins_games_riddles_1319'], show_alert=True)
            return
        team = await get_team(tid)
        if team.get("invite_locked") == "1":
            await callback_query.answer(REPLIES['plugins_games_riddles_1323'], show_alert=True)
            return
        members = await get_members(tid)
        if len(members) >= MAX_MEMBERS:
            await callback_query.answer(REPLIES['plugins_games_riddles_1327'], show_alert=True)
            return
        await r.sadd(_members_key(tid), str(uid))
        await r.set(f"{NS}:user:{uid}:team", tid)
        await _bump_task(tid, "join_members", 1)
        owner_mention = await get_user_mention(team.get("owner"), client)
        await callback_query.answer(REPLIES['plugins_games_riddles_1333'])
        try:
            await callback_query.message.edit_text(
                plugins_games_riddles_1335(kk, team.get('name'), owner_mention)
            )
        except Exception:
            pass