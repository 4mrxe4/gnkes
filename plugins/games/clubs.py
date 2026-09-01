from helpers.redis import r
from .utils import enforce_balance_cap, safe_int
from .top import get_farmers_data_fast
import random
import time
import html
from compat import Client, filters
from ..buttons import register_buttons, create_button_raw

BUTTONS_DEFINITIONS = {
    "clubs": {
        "name": "أزرار الأندية",
        "buttons": [
            {"id": "club_prev", "default": "السابق"},
            {"id": "club_next", "default": "التالي"},
            {"id": "club_cancel", "default": "إلغاء"},
            {"id": "club_arab", "default": "🇸🇦 اندية عربية"},
            {"id": "club_foreign", "default": "🌎 اندية اجنبية"},
            {"id": "club_players_btn", "default": "لاعبينك"},
            {"id": "club_buy_btn", "default": "شراء"},
            {"id": "club_next_player_btn", "default": "التالي"},
            {"id": "club_accept_race_btn", "default": "موافق"},
            {"id": "club_accept_match_btn", "default": "موافق"},
            {"id": "club_reject_match_btn", "default": "رفض"},
        ]
    }
}

register_buttons(BUTTONS_DEFINITIONS)


COUNTRY_FLAGS = {
    "البرتغال": "🇵🇹", "الأرجنتين": "🇦🇷", "البرازيل": "🇧🇷", "مصر": "🇪🇬",
    "فرنسا": "🇫🇷", "النرويج": "🇳🇴", "بلجيكا": "🇧🇪", "كرواتيا": "🇭🇷",
    "بولندا": "🇵🇱", "هولندا": "🇳🇱", "إسبانيا": "🇪🇸", "سلوفينيا": "🇸🇮",
    "ألمانيا": "🇩🇪", "إيطاليا": "🇮🇹", "إنجلترا": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "النمسا": "🇦🇹",
    "المغرب": "🇲🇦", "السعودية": "🇸🇦", "الجزائر": "🇩🇿", "اليمن": "🇾🇪",
    "تونس": "🇹🇳", "العراق": "🇮🇶", "الأردن": "🇯🇴", "الإمارات": "🇦🇪",
    "قطر": "🇶🇦", "الكويت": "🇰🇼", "عمان": "🇴🇲", "فلسطين": "🇵🇸",
    "أوروغواي": "🇺🇾", "أوروجواي": "🇺🇾", "ويلز": "🏴󠁧󠁢󠁷󠁬󠁳󠁿", "السنغال": "🇸🇳",
    "الدنمارك": "🇩🇰", "سلوفاكيا": "🇸🇰", "البحرين": "🇧🇭", "لبنان": "🇱🇧",
    "سوريا": "🇸🇾",
}

PLAYERS_POOL = [
    {"name": "ميسي", "position": "هجوم", "country": "الأرجنتين", "energy": 96},
    {"name": "رونالدو", "position": "هجوم", "country": "البرتغال", "energy": 95},
    {"name": "مبابي", "position": "هجوم", "country": "فرنسا", "energy": 93},
    {"name": "هالاند", "position": "هجوم", "country": "النرويج", "energy": 92},
    {"name": "نيمار", "position": "هجوم", "country": "البرازيل", "energy": 90},
    {"name": "محمد صلاح", "position": "هجوم", "country": "مصر", "energy": 91},
    {"name": "بنزيما", "position": "هجوم", "country": "فرنسا", "energy": 88},
    {"name": "ليفاندوفسكي", "position": "هجوم", "country": "بولندا", "energy": 88},
    {"name": "فينيسيوس", "position": "هجوم", "country": "البرازيل", "energy": 89},
    {"name": "كين", "position": "هجوم", "country": "إنجلترا", "energy": 87},
    {"name": "جريزمان", "position": "هجوم", "country": "فرنسا", "energy": 85},
    {"name": "دي بروين", "position": "وسط", "country": "بلجيكا", "energy": 91},
    {"name": "مودريتش", "position": "وسط", "country": "كرواتيا", "energy": 87},
    {"name": "كانتي", "position": "وسط", "country": "فرنسا", "energy": 85},
    {"name": "كاسيميرو", "position": "وسط", "country": "البرازيل", "energy": 84},
    {"name": "بيدري", "position": "وسط", "country": "إسبانيا", "energy": 84},
    {"name": "بيلينجهام", "position": "وسط", "country": "إنجلترا", "energy": 89},
    {"name": "فان دايك", "position": "دفاع", "country": "هولندا", "energy": 89},
    {"name": "راموس", "position": "دفاع", "country": "إسبانيا", "energy": 86},
    {"name": "ألابا", "position": "دفاع", "country": "النمسا", "energy": 85},
    {"name": "نيكو شولز", "position": "دفاع", "country": "ألمانيا", "energy": 78},
    {"name": "أرنولد", "position": "دفاع", "country": "إنجلترا", "energy": 84},
    {"name": "كورتوا", "position": "حارس", "country": "بلجيكا", "energy": 90},
    {"name": "أوبلاك", "position": "حارس", "country": "سلوفينيا", "energy": 90},
    {"name": "اليسون", "position": "حارس", "country": "البرازيل", "energy": 89},
    {"name": "نوير", "position": "حارس", "country": "ألمانيا", "energy": 88},
    {"name": "دوناروما", "position": "حارس", "country": "إيطاليا", "energy": 85},
    {"name": "زيدان", "position": "وسط", "country": "فرنسا", "energy": 90},
    {"name": "مارادونا", "position": "هجوم", "country": "الأرجنتين", "energy": 96},
    {"name": "بيليه", "position": "هجوم", "country": "البرازيل", "energy": 96},
    {"name": "مالديني", "position": "دفاع", "country": "إيطاليا", "energy": 88},
    {"name": "سواريز", "position": "هجوم", "country": "أوروغواي", "energy": 86},
    {"name": "بيل", "position": "هجوم", "country": "ويلز", "energy": 82},
    {"name": "ماني", "position": "هجوم", "country": "السنغال", "energy": 85},
    {"name": "إريكسن", "position": "وسط", "country": "الدنمارك", "energy": 83},
    {"name": "فهد منصف", "position": "حارس", "country": "المغرب", "energy": 53},
    {"name": "سالم القحطاني", "position": "حارس", "country": "السعودية", "energy": 58},
    {"name": "ياسين بلعيد", "position": "دفاع", "country": "الجزائر", "energy": 61},
    {"name": "خالد العمري", "position": "دفاع", "country": "اليمن", "energy": 55},
    {"name": "عمر الشريف", "position": "دفاع", "country": "مصر", "energy": 64},
    {"name": "منير الهاشمي", "position": "وسط", "country": "تونس", "energy": 62},
    {"name": "علي كريم", "position": "وسط", "country": "العراق", "energy": 59},
    {"name": "زيد النعيمي", "position": "وسط", "country": "الأردن", "energy": 57},
    {"name": "راشد المهيري", "position": "هجوم", "country": "الإمارات", "energy": 66},
    {"name": "حمد الكواري", "position": "هجوم", "country": "قطر", "energy": 68},
    {"name": "فيصل العتيبي", "position": "هجوم", "country": "الكويت", "energy": 60},
    {"name": "سعيد البلوشي", "position": "هجوم", "country": "عمان", "energy": 56},
    {"name": "محمود فارس", "position": "دفاع", "country": "فلسطين", "energy": 54},
    {"name": "عبدالرحمن غانم", "position": "وسط", "country": "السعودية", "energy": 70},
    {"name": "يوسف الزهراني", "position": "هجوم", "country": "السعودية", "energy": 72},
]

ARAB_CLUBS = {
    "الهلال": {"price": 5000000}, "النصر": {"price": 5000000}, "الاتحاد": {"price": 4500000},
    "الأهلي": {"price": 4000000}, "الأهلي المصري": {"price": 4000000}, "الزمالك": {"price": 3500000},
    "الرجاء": {"price": 3500000}, "الوداد": {"price": 3500000}, "الترجي": {"price": 3500000},
    "الصفاقسي": {"price": 3000000}, "شباب بلوزداد": {"price": 3000000}, "وفاق سطيف": {"price": 3000000},
    "القوة الجوية": {"price": 3000000}, "الزوراء": {"price": 2500000}, "الفيصلي": {"price": 2500000},
    "الوحدات": {"price": 2500000}, "الكويت": {"price": 2500000}, "القادسية": {"price": 2500000},
    "السد": {"price": 3000000}, "الدحيل": {"price": 3000000}, "المحرق": {"price": 2500000},
    "الرفاع": {"price": 2500000}, "السيب": {"price": 2500000}, "العين": {"price": 3000000},
    "شباب الأهلي": {"price": 3000000}, "العهد": {"price": 2500000}, "الأنصار": {"price": 2500000},
    "شباب الخليل": {"price": 2000000}, "هلال القدس": {"price": 2000000}, "الجيش": {"price": 2500000},
    "الوحدة": {"price": 2500000}, "التلال": {"price": 2000000}, "شباب الجبل": {"price": 2000000},
}

FOREIGN_CLUBS = {
    "ريال مدريد": {"price": 10000000}, "برشلونة": {"price": 9000000}, "بايرن ميونخ": {"price": 8000000},
    "مانشستر يونايتد": {"price": 8000000}, "ليفربول": {"price": 7500000}, "مانشستر سيتي": {"price": 7500000},
    "باريس سان جيرمان": {"price": 7000000}, "تشيلسي": {"price": 6500000}, "انتر ميلان": {"price": 6000000},
    "ميلان": {"price": 5500000}, "يوفنتوس": {"price": 5500000}, "توتنهام": {"price": 5000000},
    "ارسنال": {"price": 5000000}, "اتلتيكو مدريد": {"price": 5000000},
}

CLUB_COUNTRY = {
    "الهلال": "السعودية", "النصر": "السعودية", "الاتحاد": "السعودية",
    "الأهلي": "السعودية", "الأهلي المصري": "مصر", "الزمالك": "مصر",
    "الرجاء": "المغرب", "الوداد": "المغرب", "الترجي": "تونس",
    "الصفاقسي": "تونس", "شباب بلوزداد": "الجزائر", "وفاق سطيف": "الجزائر",
    "القوة الجوية": "العراق", "الزوراء": "العراق", "الفيصلي": "الأردن",
    "الوحدات": "الأردن", "الكويت": "الكويت", "القادسية": "الكويت",
    "السد": "قطر", "الدحيل": "قطر", "المحرق": "البحرين",
    "الرفاع": "البحرين", "السيب": "عمان", "العين": "الإمارات",
    "شباب الأهلي": "الإمارات", "العهد": "لبنان", "الأنصار": "لبنان",
    "شباب الخليل": "فلسطين", "هلال القدس": "فلسطين", "الجيش": "سوريا",
    "الوحدة": "سوريا", "التلال": "اليمن", "شباب الجبل": "لبنان",
    "ريال مدريد": "إسبانيا", "برشلونة": "إسبانيا", "بايرن ميونخ": "ألمانيا",
    "مانشستر يونايتد": "إنجلترا", "ليفربول": "إنجلترا", "مانشستر سيتي": "إنجلترا",
    "باريس سان جيرمان": "فرنسا", "تشيلسي": "إنجلترا", "انتر ميلان": "إيطاليا",
    "ميلان": "إيطاليا", "يوفنتوس": "إيطاليا", "توتنهام": "إنجلترا",
    "ارسنال": "إنجلترا", "اتلتيكو مدريد": "إسبانيا",
}

CLUBS_PER_PAGE = 5
MAX_PLAYERS = 11
RACE_EMOJI_PAIRS = ["⛹🫥", "🏃💨", "⚡🔥", "🐆💫", "🚀🌟"]
COMPUTER_OPPONENTS = list(ARAB_CLUBS.keys()) + list(FOREIGN_CLUBS.keys())

TRAIN_COOLDOWN = 600
PENALTY_COOLDOWN = 240
FRIENDLY_COOLDOWN = 600
MATCH_COOLDOWN = 1200
RACE_ACCEPT_TTL = 90
RACE_WINDOW = 60
PENALTY_WINDOW = 60

LEAGUE_REG_WINDOW = 3600
LEAGUE_MATCH_WINDOW = 900
LEAGUE_COOLDOWN_WINDOW = 1800
LEAGUE_SIZE = 10
LEAGUE_STAKE = 30


def player_price(energy: int) -> int:
    return int(100000 * (1 + energy / 100))


def flag_of(country: str) -> str:
    return COUNTRY_FLAGS.get(country, "🏳️")


def club_flag(club_name: str) -> str:
    return flag_of(CLUB_COUNTRY.get(club_name, ""))


def mention(uid, name) -> str:
    safe_name = html.escape(str(name) if name else str(uid))
    return f'<a href="tg://user?id={uid}">{safe_name}</a>'


def fmt_time(seconds: int) -> str:
    seconds = max(0, int(seconds))
    h, rem = divmod(seconds, 3600)
    mnt, sec = divmod(rem, 60)
    if h > 0:
        return f"{h:02d}:{mnt:02d}:{sec:02d}"
    return f"{mnt:02d}:{sec:02d}"


async def get_club_name(uid):
    v = await r.get(f"{uid}:club_name")
    if isinstance(v, bytes):
        v = v.decode("utf-8")
    return v


async def get_skills(uid) -> int:
    return safe_int(await r.get(f"{uid}:club_skills"))


async def get_points(uid) -> int:
    return safe_int(await r.get(f"{uid}:club_points"))


async def require_club(m):
    uid = m.from_user.id
    if not await r.sismember("BankList", uid):
        await m.reply("• يجب أن يكون لديك حساب بنكي أولاً\n• اكتب ↤ <code>انشاء حساب بنكي</code>")
        return None
    cname = await get_club_name(uid)
    if not cname:
        await m.reply("• عذراً عزيزي لا يوجد لديك نادي\n• اكتب ↤ <code>انشاء نادي</code>")
        return None
    return cname


async def get_players(uid):
    """يعيد قائمة [(slot, name, position, energy, country)] للاعبين المملوكين."""
    out = []
    for i in range(1, MAX_PLAYERS + 1):
        data = await r.get(f"{uid}:player_{i}")
        if not data:
            continue
        if isinstance(data, bytes):
            data = data.decode("utf-8")
        parts = data.split("|")
        if len(parts) < 4:
            continue
        name, position, energy, country = parts[0], parts[1], safe_int(parts[2]), parts[3]
        out.append((i, name, position, energy, country))
    return out


async def total_club_power(uid):
    """قوة النادي = مهارات النادي + مجموع طاقة اللاعبين."""
    skills = await get_skills(uid)
    players = await get_players(uid)
    return skills + sum(e for _, _, _, e, _ in players)


async def create_club(c, m, k):
    uid = m.from_user.id
    if not await r.sismember("BankList", uid):
        return await m.reply("• يجب أن يكون لديك حساب بنكي أولاً\n• اكتب ↤ <code>انشاء حساب بنكي</code>")

    if await get_club_name(uid):
        return await m.reply("• عذراً عزيزي يوجد لديك نادي\n• اكتب ↤ <code>نادي</code>")

    arab_btn = await create_button_raw("clubs", "club_arab", "🇸🇦 اندية عربية", callback_data=f"clubtype:arab:{uid}")
    foreign_btn = await create_button_raw("clubs", "club_foreign", "🌎 اندية اجنبية", callback_data=f"clubtype:foreign:{uid}")
    cancel_btn = await create_button_raw("clubs", "club_cancel", "إلغاء", callback_data=f"clubtype:cancel:{uid}")

    await m.reply(
        "⚽ <b>اختر نوع النادي:</b>\n_",
        reply_markup={"inline_keyboard": [[arab_btn], [foreign_btn], [cancel_btn]]}
    )


async def _owner_ok(callback_query, owner_id):
    if callback_query.from_user.id != owner_id:
        await callback_query.answer("الامر لايخصك", show_alert=True)
        return False
    return True


async def show_clubs_page(client, callback_query, club_type, page, owner_id):
    clubs_list = list(ARAB_CLUBS.items()) if club_type == "arab" else list(FOREIGN_CLUBS.items())
    total_pages = max(1, (len(clubs_list) + CLUBS_PER_PAGE - 1) // CLUBS_PER_PAGE)
    start = page * CLUBS_PER_PAGE
    current = clubs_list[start:start + CLUBS_PER_PAGE]
    type_name = "العربية" if club_type == "arab" else "الأجنبية"

    text = f"⚽ <b>اختر ناديك من الأندية {type_name}</b> 「 {page + 1}/{total_pages} 」\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯"

    rows = []
    for name, info in current:
        # عكس الترتيب: السعر أولاً، ثم السهم، ثم الاسم
        price_btn = {"text": f"{info['price']:,}", "callback_data": f"clubnoop:{owner_id}"}
        arrow_btn = {"text": "↤", "callback_data": f"clubnoop:{owner_id}"}
        name_btn = {"text": f"{name} {club_flag(name)}", "callback_data": f"clubpick:{club_type}:{name}:{owner_id}"}
        
        # الآن الترتيب: [السعر, السهم, الاسم]
        rows.append([price_btn, arrow_btn, name_btn])

    nav = []
    if page > 0:
        nav.append(await create_button_raw("clubs", "club_prev", "السابق", callback_data=f"clubpage:{club_type}:{page-1}:{owner_id}"))
    if page < total_pages - 1:
        nav.append(await create_button_raw("clubs", "club_next", "التالي", callback_data=f"clubpage:{club_type}:{page+1}:{owner_id}"))
    if nav:
        rows.append(nav)
    rows.append([await create_button_raw("clubs", "club_cancel", "إلغاء", callback_data=f"clubtype:cancel:{owner_id}")])

    await callback_query.message.edit_text(text, reply_markup={"inline_keyboard": rows})


@Client.on_callback_query(filters.regex(r"^clubnoop:"), group=-4332)
async def club_noop_callback(client, callback_query):
    await callback_query.answer()


async def confirm_create_club(client, callback_query, uid, club_type, club_name):
    table = ARAB_CLUBS if club_type == "arab" else FOREIGN_CLUBS
    info = table.get(club_name)
    if not info:
        return await callback_query.answer("اضغط اسم النادي", show_alert=True)

    price = info["price"]
    balance = safe_int(await r.get(f"{uid}:Floos"))
    if balance < price:
        cancel_btn = await create_button_raw("clubs", "club_cancel", "إلغاء", callback_data=f"clubtype:cancel:{uid}")
        return await callback_query.message.edit_text(
            f"• فلوسك لا تكفي لشراء هذا النادي\n• السعر ↤ {price:,}﷼\n• رصيدك ↤ {balance:,}﷼",
            reply_markup={"inline_keyboard": [[cancel_btn]]}
        )

    new_balance = balance - price
    await r.set(f"{uid}:Floos", new_balance)
    await enforce_balance_cap(r, callback_query.message, None, uid)

    carried_points = safe_int(await r.get(f"{uid}:club_points_carry"))
    await r.delete(f"{uid}:club_points_carry")

    await r.set(f"{uid}:club_name", club_name)
    await r.set(f"{uid}:club_type", club_type)
    await r.set(f"{uid}:club_points", carried_points)
    await r.set(f"{uid}:club_skills", 0)

    name_mention = mention(uid, callback_query.from_user.first_name or "عزيزي")
    await callback_query.message.edit_text(
        f"• تم انشاء نادي {'عربي 🇸🇦' if club_type == 'arab' else 'اجنبي 🌍'} ⚽\n"
        f"• اسمك ↤ {name_mention}\n"
        f"• اسم النادي ↤ {club_name} {club_flag(club_name)}\n"
        f"• بقيمة ↤ {price:,}\n"
        f"• فلوسك الان ↤ {new_balance:,}\n\n"
        f"- لمعرفة المزيد حول ناديك اكتب ↤ <code>نادي</code>\n_"
    )


@Client.on_callback_query(filters.regex(r"^clubtype:"), group=-4332)
async def club_type_callback(client, callback_query):
    _, action, owner_str = callback_query.data.split(":")
    owner_id = int(owner_str)
    if not await _owner_ok(callback_query, owner_id):
        return
    await callback_query.answer()
    if action == "cancel":
        await callback_query.message.edit_text("تم إلغاء العملية")
        return
    await show_clubs_page(client, callback_query, action, 0, owner_id)


@Client.on_callback_query(filters.regex(r"^clubpage:"), group=-4332)
async def club_page_callback(client, callback_query):
    _, club_type, page_str, owner_str = callback_query.data.split(":")
    owner_id = int(owner_str)
    if not await _owner_ok(callback_query, owner_id):
        return
    await callback_query.answer()
    await show_clubs_page(client, callback_query, club_type, int(page_str), owner_id)


@Client.on_callback_query(filters.regex(r"^clubpick:"), group=-4332)
async def club_pick_callback(client, callback_query):
    _, club_type, club_name, owner_str = callback_query.data.split(":")
    owner_id = int(owner_str)
    if not await _owner_ok(callback_query, owner_id):
        return
    await callback_query.answer()
    await confirm_create_club(client, callback_query, owner_id, club_type, club_name)


async def show_club(c, m, k):
    uid = m.from_user.id
    cname = await require_club(m)
    if not cname:
        return
    skills = await get_skills(uid)
    points = await get_points(uid)
    players = await get_players(uid)
    name_mention = mention(uid, m.from_user.first_name or "عزيزي")

    text = (
        f"⚽ <b>أهلاً بك عزيزي</b> ↤ {name_mention}\n"
        f"• اسم ناديك ↤ {cname} {club_flag(cname)}\n"
        f"• عدد لاعبينك ↤ {len(players)}\n"
        f"• مهارات النادي ↤ {skills}\n\n"
        f"• نقاط النادي ↤ {points}\n_"
    )
    players_btn = await create_button_raw("clubs", "club_players_btn", "لاعبينك", callback_data=f"clubplayers:0:{uid}")
    await m.reply(text, reply_markup={"inline_keyboard": [[players_btn]]})


async def _players_page_text(uid, idx):
    players = await get_players(uid)
    cname = await get_club_name(uid) or ""
    cflag = club_flag(cname)
    if not players:
        return f"• لاعبين تم شرائهم بنادي {cname} {cflag} :\n\n• لا يوجد لديك لاعبين بعد\n\n- يمكنك شراء لاعبين بكتابة ↤ <code>شراء لاعبين</code>", 0
    idx = idx % len(players)
    _, name, position, energy, country = players[idx]
    text = (
        f"• لاعبين تم شرائهم بنادي {cname} {cflag} :\n\n"
        f"• اسم اللاعب ↤ {name}\n"
        f"• جنسيته ↤ {flag_of(country)}\n"
        f"• مركزه ↤ {position}\n"
        f"• طاقته ↤ {energy}%\n\n"
        f" - يمكنك شراء لاعبين بكتابة ↤ <code>شراء لاعبين</code>\n_"
    )
    return text, idx


@Client.on_callback_query(filters.regex(r"^clubplayers:"), group=-4332)
async def club_players_callback(client, callback_query):
    _, idx_str, owner_str = callback_query.data.split(":")
    owner_id = int(owner_str)
    if not await _owner_ok(callback_query, owner_id):
        return
    await callback_query.answer()
    idx = int(idx_str)
    text, real_idx = await _players_page_text(owner_id, idx)
    next_btn = await create_button_raw("clubs", "club_next_player_btn", "التالي", callback_data=f"clubplayers:{real_idx+1}:{owner_id}")
    await callback_query.message.edit_text(text, reply_markup={"inline_keyboard": [[next_btn]]})


async def _pick_candidate(uid):
    players = await get_players(uid)
    owned_names = {p[1] for p in players}
    pool = [p for p in PLAYERS_POOL if p["name"] not in owned_names]
    if not pool:
        return None
    candidate = random.choice(pool)
    await r.setex(f"{uid}:club_buy_candidate", 600, f"{candidate['name']}|{candidate['position']}|{candidate['energy']}|{candidate['country']}")
    return candidate


def _candidate_text(cname, candidate):
    price = player_price(candidate["energy"])
    return (
        f"• جميع الاعبين لشرائهم لنادي ↤ {cname} {club_flag(cname)} :\n\n"
        f"• الاسم ↤ {candidate['name']}\n"
        f"• سعره ↤ {price:,} 💸\n"
        f"• جنسيته ↤ {flag_of(candidate['country'])}\n"
        f"• مركزه ↤ {candidate['position']}\n"
        f"• طاقته ↤ {candidate['energy']}%\n_"
    )


async def buy_players(c, m, k):
    uid = m.from_user.id
    cname = await require_club(m)
    if not cname:
        return
    players = await get_players(uid)
    if len(players) >= MAX_PLAYERS:
        return await m.reply(f"• نادي {cname} مكتمل بالفعل\n• الحد الأقصى ↤ {MAX_PLAYERS} لاعب")

    candidate = await _pick_candidate(uid)
    if not candidate:
        return await m.reply("• لا يوجد لاعبين جدد متاحين حالياً لشراءهم")

    buy_btn = await create_button_raw("clubs", "club_buy_btn", "شراء", callback_data=f"clubbuy:buy:{uid}")
    next_btn = await create_button_raw("clubs", "club_next_player_btn", "التالي", callback_data=f"clubbuy:next:{uid}")

    await m.reply(_candidate_text(cname, candidate), reply_markup={"inline_keyboard": [[buy_btn], [next_btn]]})


@Client.on_callback_query(filters.regex(r"^clubbuy:"), group=-4332)
async def club_buy_callback(client, callback_query):
    _, action, owner_str = callback_query.data.split(":")
    owner_id = int(owner_str)
    if not await _owner_ok(callback_query, owner_id):
        return
    await callback_query.answer()

    cname = await get_club_name(owner_id)
    if not cname:
        return await callback_query.message.edit_text("• عذراً عزيزي لا يوجد لديك نادي")

    if action == "next":
        candidate = await _pick_candidate(owner_id)
        if not candidate:
            return await callback_query.message.edit_text("• لا يوجد لاعبين جدد متاحين حالياً لشراءهم")
        buy_btn = await create_button_raw("clubs", "club_buy_btn", "شراء", callback_data=f"clubbuy:buy:{owner_id}")
        next_btn = await create_button_raw("clubs", "club_next_player_btn", "التالي", callback_data=f"clubbuy:next:{owner_id}")
        return await callback_query.message.edit_text(_candidate_text(cname, candidate), reply_markup={"inline_keyboard": [[buy_btn], [next_btn]]})

    raw = await r.get(f"{owner_id}:club_buy_candidate")
    if not raw:
        return await callback_query.message.edit_text("• انتهت صلاحية هذا العرض\n• اكتب ↤ شراء لاعبين من جديد")
    if isinstance(raw, bytes):
        raw = raw.decode("utf-8")
    name, position, energy_str, country = raw.split("|")
    energy = safe_int(energy_str)

    players = await get_players(owner_id)
    if len(players) >= MAX_PLAYERS:
        return await callback_query.message.edit_text(f"• نادي {cname} مكتمل بالفعل\n• الحد الأقصى ↤ {MAX_PLAYERS} لاعب")
    if any(p[1] == name for p in players):
        return await callback_query.message.edit_text("• هذا اللاعب موجود لديك بالفعل")

    price = player_price(energy)
    balance = safe_int(await r.get(f"{owner_id}:Floos"))
    if balance < price:
        return await callback_query.message.edit_text(f"• فلوسك لا تكفي لشراء {name}\n• السعر ↤ {price:,}﷼\n• رصيدك ↤ {balance:,}﷼")

    slot = None
    taken = {p[0] for p in players}
    for i in range(1, MAX_PLAYERS + 1):
        if i not in taken:
            slot = i
            break

    new_balance = balance - price
    await r.set(f"{owner_id}:Floos", new_balance)
    await enforce_balance_cap(r, callback_query.message, None, owner_id)
    await r.set(f"{owner_id}:player_{slot}", f"{name}|{position}|{energy}|{country}")
    await r.delete(f"{owner_id}:club_buy_candidate")

    await callback_query.message.edit_text(
        f"• تم شراء لاعب جديد\n"
        f"• اسم الاعب ↤ {name}\n"
        f"• سعره ↤ {price:,} ريال\n"
        f"• جنسيته ↤ {flag_of(country)}\n"
        f"• مركزه ↤ {position}\n"
        f"• طاقته ↤ {energy}\n_"
    )


async def train_club(c, m, k):
    uid = m.from_user.id
    cname = await require_club(m)
    if not cname:
        return

    ttl = await r.ttl(f"{uid}:train_cooldown")
    if ttl and ttl > 0:
        return await m.reply(f"• يمكنك التمرين بعد {fmt_time(ttl)} دقيقة")

    gain = random.randint(2, 10)
    new_skills = safe_int(await r.incrby(f"{uid}:club_skills", gain))
    await r.setex(f"{uid}:train_cooldown", TRAIN_COOLDOWN, "1")

    await m.reply(
        f"• اسم النادي ↤ {cname} {club_flag(cname)}\n"
        f"• تم زيادة مهارات ↤ {gain}\n"
        f"• اصبحت مهارات النادي ↤ {new_skills}\n_"
    )


async def penalty_kick(c, m, k):
    uid = m.from_user.id
    cname = await require_club(m)
    if not cname:
        return

    ttl = await r.ttl(f"{uid}:penalty_cooldown")
    if ttl and ttl > 0:
        return await m.reply(f"• يمكنك لعب ضربات جزاء بعد {fmt_time(ttl)} دقيقة")

    await r.setex(f"{uid}:penalty_cooldown", PENALTY_COOLDOWN, "1")
    await r.setex(f"{uid}:penalty_pending", PENALTY_WINDOW, "1")

    await m.reply("• حسناً عزيزي لديك دقيقة فقط\n• ارسل ذلك ↤ <code>⚽</code>")


@Client.on_message(filters.group, group=-4331)
async def penalty_and_race_listener(client, message):
    """يستمع لمحاولات ضربات الجزاء ومنافسات السرعة النشطة."""
    if not message.from_user:
        return
    uid = message.from_user.id
    text = (message.text or "").strip()

    if message.dice and message.dice.emoji == "⚽":
        pending = await r.get(f"{uid}:penalty_pending")
        if pending:
            await r.delete(f"{uid}:penalty_pending")
            
            gain = message.dice.value

            if gain in (4, 5):
                await r.incrby(f"{uid}:club_skills", gain)
                msg_text = (
                    "• عالميه عالميه عالميه عالميه قوووول\n"
                    f"• تم زيادة مهاراتك ↤︎ {gain}"
                )
            elif gain in (1, 2):
                msg_text = (
                    "• يا الاحول الباب قدامك ضيعتها"
                )
            else:
                msg_text = (
                    "• يا الاحول الباب قدامك ضيعتها"
                )

            return await message.reply(msg_text)

    race_raw = await r.get(f"race:{message.chat.id}")
    if not race_raw:
        return
    if isinstance(race_raw, bytes):
        race_raw = race_raw.decode("utf-8")
    try:
        challenger_id, target_id, emoji_pair = race_raw.split("|", 2)
        challenger_id, target_id = int(challenger_id), int(target_id)
    except Exception:
        return

    if uid not in (challenger_id, target_id):
        return
    if text != emoji_pair:
        return

    deleted = await r.delete(f"race:{message.chat.id}")
    if not deleted:
        return

    loser_id = target_id if uid == challenger_id else challenger_id
    delta = random.randint(1, 10)

    winner_skills = safe_int(await r.incrby(f"{uid}:club_skills", delta))
    winner_points = safe_int(await r.incrby(f"{uid}:club_points", delta))

    loser_skills = safe_int(await r.get(f"{loser_id}:club_skills"))
    loser_points = safe_int(await r.get(f"{loser_id}:club_points"))
    new_loser_skills = max(0, loser_skills - delta)
    new_loser_points = max(0, loser_points - delta)
    await r.set(f"{loser_id}:club_skills", new_loser_skills)
    await r.set(f"{loser_id}:club_points", new_loser_points)

    winner_name = await _mention_via_client(client, uid)
    loser_name = await _mention_via_client(client, loser_id)

    await message.reply(
        f"• مبروك للفائز ↤ {winner_name}\n"
        f"• تم اضافة نقاط لمهارتك وناديك : {delta}\n\n"
        f"• تم الخصم من ↤ {loser_name}\n"
        f"• {delta} من نقاط مهاراته وناديه\n_"
    )


async def compete_challenge(c, m, k):
    uid = m.from_user.id
    cname = await require_club(m)
    if not cname:
        return
    if not m.reply_to_message:
        return await m.reply("• يجب أن يكون هذا الأمر رداً على شخص آخر")

    target = m.reply_to_message.from_user
    if target.id == uid:
        return await m.reply("• لا يمكنك التنافس مع نفسك")
    if target.is_bot:
        return await m.reply("• لا يمكنك التنافس مع البوت")

    target_club = await get_club_name(target.id)
    if not target_club:
        return await m.reply("• عذراً عزيزي هذا الشخص ليس لديه نادي")

    target_skills = await get_skills(target.id)
    if target_skills <= 0:
        return await m.reply("• عذراً عزيزي لا تستطيع التنافس لأن مهاراته لاتكفي")

    name_mention = mention(uid, m.from_user.first_name or "عزيزي")
    accept_btn = await create_button_raw("clubs", "club_accept_race_btn", "موافق", callback_data=f"racechal:{uid}:{target.id}")

    await m.reply(
        f"• الحلو ↤ {name_mention}\n"
        f"• يبي يتنافس معاك\n\n"
        f"- اسرع شخص يرسل المطلوب يفوز بنقاط مهارات",
        reply_markup={"inline_keyboard": [[accept_btn]]}
    )


@Client.on_callback_query(filters.regex(r"^racechal:"), group=-4332)
async def race_challenge_callback(client, callback_query):
    _, challenger_str, target_str = callback_query.data.split(":")
    challenger_id, target_id = int(challenger_str), int(target_str)

    if callback_query.from_user.id != target_id:
        return await callback_query.answer("الامر لايخصك", show_alert=True)

    await callback_query.answer()

    challenger_name = await _mention_via_client(client, challenger_id)
    target_name = await _mention_via_client(client, target_id)

    emoji_pair = random.choice(RACE_EMOJI_PAIRS)
    msg = callback_query.message
    await r.setex(f"race:{msg.chat.id}", RACE_WINDOW, f"{challenger_id}|{target_id}|{emoji_pair}")

    await msg.edit_text(
        f"• تم الموافقه\n"
        f"• المنافس ↤ {challenger_name}\n"
        f"• ضد ↤ {target_name}\n"
        f"• لديكم دقيقة اسرع شخص يرسل ↤ <code>{emoji_pair}</code>\n_"
    )


async def friendly_match(c, m, k):
    uid = m.from_user.id
    cname = await require_club(m)
    if not cname:
        return

    skills = await get_skills(uid)
    if skills <= 10:
        return await m.reply("• عذراً عزيزي يجب ان تكون مهارات ناديك فوق 10")

    ttl = await r.ttl(f"{uid}:friendly_cooldown")
    if ttl and ttl > 0:
        return await m.reply(f"• يمكنك لعب مباراة ودية بعد {fmt_time(ttl)} دقيقة")

    await r.setex(f"{uid}:friendly_cooldown", FRIENDLY_COOLDOWN, "1")

    opponent_club = random.choice(COMPUTER_OPPONENTS)
    delta = random.randint(1, 10)
    outcome = random.choice(["win", "win", "lose", "lose", "draw"])
    name_mention = mention(uid, m.from_user.first_name or "عزيزي")
    club_line = f"• اسم النادي ↤︎ {cname} {club_flag(cname)}"
    opp_line = f"• نادي الخصم ↤︎ {opponent_club} {club_flag(opponent_club)}"

    if outcome == "win":
        my_score = random.randint(2, 5)
        opp_score = random.randint(1, my_score - 1)
        await r.incrby(f"{uid}:club_skills", delta)
        result_line = (
            f"• مبرووك فزت بالمباراه ⚽️\n"
            f"• اسمك ↤︎ {name_mention}\n"
            f"{club_line}\n"
            f"{opp_line}\n"
            f"• النتيجة ↤︎ {my_score}-{opp_score}\n\n"
            f"- ربحت {delta} نقطة من مهارات ناديك\n_"
        )
    elif outcome == "lose":
        opp_score = random.randint(2, 5)
        my_score = random.randint(1, opp_score - 1)
        await r.set(f"{uid}:club_skills", max(0, skills - delta))
        result_line = (
            f"• حظ اوفر خسرت بالمباراة ⚽️\n"
            f"• اسمك ↤︎ {name_mention}\n"
            f"{club_line}\n"
            f"{opp_line}\n"
            f"• النتيجة ↤︎ {my_score}-{opp_score}\n\n"
            f"- خسرت {delta} نقطة من مهارات ناديك\n_"
        )
    else:
        draw_score = random.randint(1, 5)
        result_line = (
            f"• تعادل ⚽️\n"
            f"• اسمك ↤︎ {name_mention}\n"
            f"{club_line}\n"
            f"{opp_line}\n"
            f"• النتيجة ↤︎ {draw_score}-{draw_score}\n\n"
            f"- لا فوز ولا خسارة\n_"
        )

    await m.reply(result_line)


async def match_with_player(c, m, k):
    uid = m.from_user.id
    cname = await require_club(m)
    if not cname:
        return
    if not m.reply_to_message:
        return await m.reply("• يجب أن يكون هذا الأمر رداً على شخص آخر")

    opponent = m.reply_to_message.from_user
    if opponent.id == uid:
        return await m.reply("• لا يمكنك اللعب ضد نفسك")
    if opponent.is_bot:
        return await m.reply("• لا يمكنك اللعب ضد البوت")

    opp_club = await get_club_name(opponent.id)
    if not opp_club:
        return await m.reply("• عذراً عزيزي هذا الشخص ليس لديه نادي")

    my_skills = await get_skills(uid)
    if my_skills <= 30:
        return await m.reply("• عذراً عزيزي يجب ان تكون مهاراتك اكثر من 30")

    ttl = await r.ttl(f"{uid}:match_cooldown")
    if ttl and ttl > 0:
        return await m.reply(f"• يمكنك لعب مباراة أخرى بعد {fmt_time(ttl)} دقيقة")

    challenger_mention = mention(uid, m.from_user.first_name or "عزيزي")
    target_mention = mention(opponent.id, opponent.first_name or "عزيزي")
    accept_btn = await create_button_raw("clubs", "club_accept_match_btn", "موافق", callback_data=f"matchreq:accept:{uid}:{opponent.id}")
    reject_btn = await create_button_raw("clubs", "club_reject_match_btn", "رفض", callback_data=f"matchreq:reject:{uid}:{opponent.id}")

    await m.reply(
        f"• {challenger_mention}\n"
        f"• يتحداك ↤ {target_mention}\n"
        f"• ناديه ↤ {cname} {club_flag(cname)}\n\n"
        f"- هل توافق على خوض المباراة؟\n_",
        reply_markup={"inline_keyboard": [[accept_btn, reject_btn]]}
    )


@Client.on_callback_query(filters.regex(r"^matchreq:"), group=-4332)
async def match_request_callback(client, callback_query):
    _, action, challenger_str, target_str = callback_query.data.split(":")
    challenger_id, target_id = int(challenger_str), int(target_str)

    if callback_query.from_user.id != target_id:
        return await callback_query.answer("الامر لايخصك", show_alert=True)

    await callback_query.answer()

    challenger_mention = await _mention_via_client(client, challenger_id)
    target_mention = await _mention_via_client(client, target_id)

    if action == "reject":
        return await callback_query.message.edit_text(
            f"• رفض ↤ {target_mention}\n"
            f"• تحدي ↤ {challenger_mention}\n\n"
            f"- تم إلغاء المباراة\n_"
        )

    cname = await get_club_name(challenger_id)
    opp_club = await get_club_name(target_id)
    if not cname or not opp_club:
        return await callback_query.message.edit_text("• عذراً أحد الطرفين لم يعد لديه نادي")

    my_skills = await get_skills(challenger_id)
    opp_skills = await get_skills(target_id)

    ttl = await r.ttl(f"{challenger_id}:match_cooldown")
    if ttl and ttl > 0:
        return await callback_query.message.edit_text(f"• انتهت صلاحية هذا التحدي\n• يمكن للمتحدي لعب مباراة أخرى بعد {fmt_time(ttl)} دقيقة")

    await r.setex(f"{challenger_id}:match_cooldown", MATCH_COOLDOWN, "1")

    delta = random.randint(10, 25)
    club_line = f"• ناديك ↤ {cname} {club_flag(cname)}\n• نادي الخصم ↤ {opp_club} {club_flag(opp_club)}"

    if my_skills > opp_skills:
        await r.incrby(f"{challenger_id}:club_skills", delta)
        await r.incrby(f"{challenger_id}:club_points", delta)
        result = f"🎉 فاز ↤ {challenger_mention}\n{club_line}\n\n- ربح {delta} نقطة ومهارة"
    elif my_skills < opp_skills:
        await r.incrby(f"{target_id}:club_skills", delta)
        await r.incrby(f"{target_id}:club_points", delta)
        result = f"🎉 فاز ↤ {target_mention}\n{club_line}\n\n- ربح {delta} نقطة ومهارة"
    else:
        result = f"تعادل!\n{club_line}\n\n- لا فوز ولا خسارة"

    await callback_query.message.edit_text(result)


async def change_club(c, m, k):
    uid = m.from_user.id
    cname = await require_club(m)
    if not cname:
        return

    points = await get_points(uid)
    for i in range(1, MAX_PLAYERS + 1):
        await r.delete(f"{uid}:player_{i}")
    await r.delete(f"{uid}:club_name")
    await r.delete(f"{uid}:club_type")
    await r.delete(f"{uid}:club_skills")
    await r.delete(f"{uid}:club_points")
    await r.set(f"{uid}:club_points_carry", points)

    await m.reply("• يمكنك الان انشاء نادي جديد بنقاطك السابقة\n• اكتب ↤ <code>انشاء نادي</code>")


async def delete_club(c, m, k):
    uid = m.from_user.id
    cname = await require_club(m)
    if not cname:
        return

    for i in range(1, MAX_PLAYERS + 1):
        await r.delete(f"{uid}:player_{i}")
    await r.delete(f"{uid}:club_name")
    await r.delete(f"{uid}:club_type")
    await r.delete(f"{uid}:club_skills")
    await r.delete(f"{uid}:club_points")
    await r.delete(f"{uid}:club_points_carry")
    await r.delete(f"{uid}:train_cooldown")
    await r.delete(f"{uid}:penalty_cooldown")
    await r.delete(f"{uid}:friendly_cooldown")
    await r.delete(f"{uid}:match_cooldown")

    await m.reply("• تم حذف ناديك بالكامل بنجاح 🗑️")


async def _league_advance():
    """يتحقق من انتهاء المرحلة الحالية وينقل الدوري تلقائياً للمرحلة التالية عند الحاجة."""
    state = await r.get("league:state")
    if isinstance(state, bytes):
        state = state.decode("utf-8")
    if not state:
        await r.set("league:state", "open")
        await r.setex("league:timer", LEAGUE_REG_WINDOW, "1")
        return "open"

    ttl = await r.ttl("league:timer")
    if ttl and ttl > 0:
        return state

    if state == "open":
        await _league_start_matches()
        return "running"
    elif state == "running":
        await _league_finish_matches()
        return "cooldown"
    else:
        await r.delete("league:registrants")
        await r.delete("league:participants")
        await r.delete("league:results")
        await r.set("league:state", "open")
        await r.setex("league:timer", LEAGUE_REG_WINDOW, "1")
        return "open"


async def _league_start_matches():
    members = await r.smembers("league:registrants") or set()
    participants = [int(x.decode() if isinstance(x, bytes) else x) for x in members]
    random.shuffle(participants)

    pairs = []
    while len(participants) >= 2:
        a = participants.pop()
        b = participants.pop()
        pairs.append((a, b))

    serialized = "|".join(f"{a},{b}" for a, b in pairs)
    await r.set("league:pairings", serialized)
    await r.set("league:participants", ",".join(str(x) for x in ([p for pair in pairs for p in pair])))
    await r.set("league:state", "running")
    await r.setex("league:timer", LEAGUE_MATCH_WINDOW, "1")


async def _league_finish_matches():
    raw = await r.get("league:pairings")
    if isinstance(raw, bytes):
        raw = raw.decode("utf-8")
    results_lines = []
    if raw:
        for pair_str in raw.split("|"):
            if not pair_str:
                continue
            a_str, b_str = pair_str.split(",")
            a, b = int(a_str), int(b_str)
            a_skills = await get_skills(a)
            b_skills = await get_skills(b)
            a_club = await get_club_name(a) or "؟"
            b_club = await get_club_name(b) or "؟"

            if a_skills > b_skills:
                winner, loser = a, b
            elif b_skills > a_skills:
                winner, loser = b, a
            else:
                winner, loser = None, None

            if winner is not None:
                await r.incrby(f"{winner}:club_points", LEAGUE_STAKE * 2)
                await r.incrby(f"{winner}:club_skills", LEAGUE_STAKE * 2)
            else:
                await r.incrby(f"{a}:club_points", LEAGUE_STAKE)
                await r.incrby(f"{a}:club_skills", LEAGUE_STAKE)
                await r.incrby(f"{b}:club_points", LEAGUE_STAKE)
                await r.incrby(f"{b}:club_skills", LEAGUE_STAKE)

            try:
                a_user_name = (await _safe_name(a))
                b_user_name = (await _safe_name(b))
            except Exception:
                a_user_name, b_user_name = str(a), str(b)

            if winner == a:
                win_name = a_user_name
            elif winner == b:
                win_name = b_user_name
            else:
                win_name = None

            block = f"- مباراة : {a_user_name} ↤ {b_user_name}\n- الفريقين : {a_club} {club_flag(a_club)} ↤ {b_club} {club_flag(b_club)}\n"
            block += f"- مبروك للفائز : {win_name} 🏆" if win_name else "- تعادل، تم استرجاع نقاط الطرفين\n_"
            results_lines.append(block)

    results_text = "\n\n".join(results_lines) if results_lines else "• لم يشارك عدد كافٍ من الأندية هذه الجولة"
    await r.set("league:results", results_text)
    await r.set("league:state", "cooldown")
    await r.setex("league:timer", LEAGUE_COOLDOWN_WINDOW, "1")


_name_cache_client = {}


async def _safe_name(uid):
    try:
        client = _name_cache_client.get("c")
        if client:
            user = await client.get_users(uid)
            return mention(uid, user.first_name)
    except Exception:
        pass
    return mention(uid, str(uid))


async def _mention_via_client(client, uid):
    try:
        user = await client.get_users(uid)
        return mention(uid, user.first_name)
    except Exception:
        return mention(uid, str(uid))


async def show_league(c, m, k):
    _name_cache_client["c"] = c
    state = await _league_advance()
    uid = m.from_user.id

    if state == "open":
        members = await r.smembers("league:registrants") or set()
        count = len(members)
        text = "• الأنديه المشاركة في الدوري :\n\n"
        if count:
            i = 1
            for member in members:
                member_id = int(member.decode() if isinstance(member, bytes) else member)
                name = await _safe_name(member_id)
                club = await get_club_name(member_id) or "؟"
                text += f"{i} - الاسم ↤ {name}\n{i} - النادي ↤ {club} {club_flag(club)}\n\n"
                i += 1
        remaining = max(0, LEAGUE_SIZE - count)
        text += f"• متبقى ↤ {remaining}\n"
        if remaining > 0:
            text += "• التسجيل بالدوري متاح\n- للانضمام اكتب ↤ <code>انضمام للدوري</code>\n_"
        else:
            text += "• التسجيل مكتمل، ستبدأ المباريات قريباً\n_"
        return await m.reply(text)

    if state == "running":
        raw = await r.get("league:pairings")
        if isinstance(raw, bytes):
            raw = raw.decode("utf-8")
        text = "• تم توزيع الأندية المشاركة للدوري :\n\n"
        if raw:
            for pair_str in raw.split("|"):
                if not pair_str:
                    continue
                a_str, b_str = pair_str.split(",")
                a, b = int(a_str), int(b_str)
                a_name, b_name = await _safe_name(a), await _safe_name(b)
                a_club, b_club = await get_club_name(a) or "؟", await get_club_name(b) or "؟"
                text += f"• مباراة : {a_name} ↤ {b_name}\n• النوادي : {a_club} {club_flag(a_club)} ↤ {b_club} {club_flag(b_club)}\n\n"
        ttl = await r.ttl("league:timer")
        text += f"• التسجيل مقفل ستبداء المباريات بعد {fmt_time(ttl)} دقائق"
        return await m.reply(text)

    results = await r.get("league:results")
    if isinstance(results, bytes):
        results = results.decode("utf-8")
    ttl = await r.ttl("league:timer")
    text = (
        "• نتائج دوري الأنديه :\n"
        f"• تم اضافة {LEAGUE_STAKE * 2} نقطة و مهارات للفائزين\n"
        "• وتم خصمها من الخسرانين\n"
        "• مبروك للفائزين 🏆 :\n\n"
        f"{results or '• لا توجد نتائج'}\n\n"
        f"• التسجيل مقفل حالياً سيبداء بعد {fmt_time(ttl)} دقائق\n_"
    )
    return await m.reply(text)


async def join_league(c, m, k):
    _name_cache_client["c"] = c
    uid = m.from_user.id
    cname = await require_club(m)
    if not cname:
        return

    state = await _league_advance()
    if state != "open":
        return await m.reply("• التسجيل بالدوري غير متاح حالياً\n• اكتب ↤ <code>الدوري</code> لمعرفة الحالة")

    skills = await get_skills(uid)
    if skills <= 30:
        return await m.reply("• عذراً عزيزي يجب ان تكون مهاراتك اكثر من 30")

    points = await get_points(uid)
    if points < LEAGUE_STAKE:
        return await m.reply(f"• يجب أن تملك {LEAGUE_STAKE} نقطة على الأقل نادٍ للانضمام")

    already = await r.sismember("league:registrants", uid)
    if already:
        return await m.reply("• أنت مسجل بالفعل في الدوري")

    members = await r.smembers("league:registrants") or set()
    if len(members) >= LEAGUE_SIZE:
        return await m.reply("• التسجيل مكتمل بالفعل، انتظر الجولة القادمة")

    await r.decrby(f"{uid}:club_skills", LEAGUE_STAKE)
    await r.decrby(f"{uid}:club_points", LEAGUE_STAKE)
    await r.sadd("league:registrants", uid)

    new_count = len(await r.smembers("league:registrants") or set())
    if new_count >= LEAGUE_SIZE:
        await r.delete("league:timer")
        await r.setex("league:timer", 1, "1")

    await m.reply(
        f"• تم تسجيلك في الدوري بنجاح\n"
        f"• تم خصم {LEAGUE_STAKE} نقطة و{LEAGUE_STAKE} مهارة\n"
        f"• اكتب ↤ <code>الدوري</code> لمتابعة التسجيل\n_"
    )


async def show_clubs_top(c, m, k):
    all_users = await r.smembers("BankList") or set()
    clubs_list = []
    for uid in all_users:
        uid_str = uid.decode() if isinstance(uid, bytes) else uid
        club_name = await get_club_name(uid_str)
        if not club_name:
            continue
        points = await get_points(uid_str)
        if points > 0:
            clubs_list.append((points, int(uid_str), club_name))

    clubs_list.sort(reverse=True)

    text = "• توب الاندية العالمي 🏆 :\n\n"
    emojis = ["🥇", "🥈", "🥉"]
    if clubs_list:
        for i, (points, uid, club_name) in enumerate(clubs_list[:30]):
            name = await _mention_via_client(c, uid)
            marker = emojis[i] if i < 3 else f"{i + 1} )"
            text += f"{marker} {points:,}  l {name} \nl {club_name} {club_flag(club_name)}\n\n"
    else:
        text += "• لا يوجد نوادي حتى الآن\n"

    await m.reply(text)


async def handle_clubs_commands(c, m, k, text):
    text = (text or "").strip()
    if not text:
        return None

    if text in ("النوادي", "الاندية", "مساعدة النوادي", "مساعدة الاندية"):
        return await m.reply("""
⚽ <b>لعبة الأندية</b>\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n

• <b>انشاء نادي</b> :
- تسوي لك نادي وتطوره وتلعب فيه بقيمة محددة .

• <b>شراء لاعبين</b> :
- تشتري لاعبين لك بالنادي 

• <b>نادي</b> :
- تستطيع رؤية ناديك ومعرفة عدد لاعبينك ونقاطه ومهاراته 

• <b>تدريب</b> :
- تدرب ناديك كل 20 دقيقه وتزود من مهارات ناديك 

• <b>تنافس (بالرد على الشخص)</b> :
- تتنافس بسرعة الكتابة انت وشخص الاسرع يفوز بمهارات ونقاط 

• <b>ضربة جزاء</b> :
- تختبر مهاراتك بالكورة تجيب هدف اسطوري تستلم نقاط 

• <b>مباراة ودية</b> :
- انت وحظك تفوز بالمباراة تزيد مهاراتك تخسر تنقص مهاراة ناديك 

• <b>مباراة (بالرد ع الشخص)</b> :
- تلعب مباراة ضد شخص تعتمد على مهارات النادي الاكثر يفوز بنقاط + مهارات

• <b>تغير النادي</b> :
- تغير ناديك وقت ماتغير النادي ينحذفون لاعبينك .

• <b>الدوري</b> :
- دوري كل ساعة 10 نوادي يقابلون بعض بشكل عشوائي

• <b>انضمام للدوري</b> :
- اذا كان التسجيل متاح بالنادي تنضم وتنتظر توزيع الادوار
ملاحظة : تنخصم منك 30 مهارات ونقاط 

- الفايز بالدوري : ترجع له النقاط دبل
- الخسران بالدوري : ما يرجع له شيء
- المتعادلين بالدوري : ترجع نقاطكم

• <b>توب النوادي</b> :
- توب خاص باكثر نوادي عندهم نقاط

• <b>حذف النادي</b> :
- تحذف ناديك بالكامل .
_
        """)


    if text == "انشاء نادي":
        return await create_club(c, m, k)

    if text == "نادي":
        return await show_club(c, m, k)

    if text == "شراء لاعبين" or text == "شراء لاعب":
        return await buy_players(c, m, k)

    if text == "تدريب":
        return await train_club(c, m, k)

    if text in ("تنافس",):
        return await compete_challenge(c, m, k)

    if text in ("ضربة جزاء", "ضربه جزاء"):
        return await penalty_kick(c, m, k)

    if text in ("مباراة ودية", "مباراه وديه", "مباراة وديه", "مباراه ودية"):
        return await friendly_match(c, m, k)

    if text in ("مباراة", "مباراه") and m.reply_to_message:
        return await match_with_player(c, m, k)

    if text in ("تغير النادي", "تغيير النادي"):
        return await change_club(c, m, k)

    if text in ("حذف النادي", "مسح النادي", "مسح ناديي"):
        return await delete_club(c, m, k)

    if text == "الدوري":
        return await show_league(c, m, k)

    if text == "انضمام للدوري":
        return await join_league(c, m, k)

    if text == "توب النوادي":
        return await show_clubs_top(c, m, k)

    return None
