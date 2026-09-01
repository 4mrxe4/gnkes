

from helpers.redis import r
from .utils import enforce_balance_cap, safe_int
from .top import get_farmers_data_fast, update_farmers_top, update_thieves_top
import random
import time
import hashlib
from compat import Client, filters
from ..buttons import register_buttons, create_button_raw

BUTTONS_DEFINITIONS = {
    "farm": {
        "name": "أزرار المزرعة",
        "buttons": [
            {"id": "farm_shop_seeds", "default": "• شراء البذور"},
            {"id": "farm_shop_animals", "default": "• شراء الحيوانات"},
            {"id": "farm_shop_tools", "default": "• شراء الأدوات"},
            {"id": "farm_shop_back", "default": "رجوع"},
            {"id": "farm_shop_close", "default": "اخفاء"},
        ]
    }
}

register_buttons(BUTTONS_DEFINITIONS)


SEEDS = {
    "قمح":     {"emoji": "🌾", "price": 10000,      "level": 0,   "grow": 1800},
    "ذره":     {"emoji": "🌽", "price": 25000,      "level": 3,   "grow": 2400},
    "جزر":     {"emoji": "🥕", "price": 57000,      "level": 5,   "grow": 3000},
    "خيار":    {"emoji": "🥒", "price": 123000,     "level": 7,   "grow": 3600},
    "طماطم":   {"emoji": "🍅", "price": 257000,     "level": 10,  "grow": 4500},
    "بطاطس":   {"emoji": "🥔", "price": 527000,     "level": 14,  "grow": 5400},
    "ليمون":   {"emoji": "🍋", "price": 1300000,    "level": 18,  "grow": 6600},
    "تفاح":    {"emoji": "🍎", "price": 2680000,    "level": 25,  "grow": 8400},
    "برتقال":  {"emoji": "🍊", "price": 5560000,    "level": 30,  "grow": 10200},
    "عنب":     {"emoji": "🍇", "price": 11320000,   "level": 37,  "grow": 12600},
    "فراوله":  {"emoji": "🍓", "price": 22950000,   "level": 45,  "grow": 15000},
    "توت":     {"emoji": "🫐", "price": 46200000,   "level": 60,  "grow": 18000},
    "كرز":     {"emoji": "🍒", "price": 135000000,  "level": 75,  "grow": 22500},
    "اناناس":  {"emoji": "🍍", "price": 340000000,  "level": 100, "grow": 27000},
    "جوزهند":  {"emoji": "🥥", "price": 1000000000, "level": 120, "grow": 33000, "label": "جوز الهند"},
}

ANIMALS_PROD = {
    "دجاج":  {"emoji": "🐓", "price": 100000,   "product": "بيض",  "product_emoji": "🥚"},
    "بقر":   {"emoji": "🐄", "price": 250000,   "product": "حليب", "product_emoji": "🥛"},
    "غنم":   {"emoji": "🐑", "price": 750000,   "product": "صوف",  "product_emoji": "🧶"},
    "سمك":   {"emoji": "🐟", "price": 1500000,  "product": "سوشي", "product_emoji": "🍣"},
    "طيور":  {"emoji": "🦅", "price": 2000000,  "product": "ريش",  "product_emoji": "🪶"},
    "نحل":   {"emoji": "🐝", "price": 1000000,  "product": "عسل",  "product_emoji": "🍯"},
}

ANIMALS_PET = {
    "قطط":  {"emoji": "🐈", "price": 120000},
    "كلاب": {"emoji": "🦮", "price": 360000},
    "خيول": {"emoji": "🐎", "price": 950000},
}

PRODUCT_PRICE = {
    "بيض": 10000, "صوف": 50000, "حليب": 100000,
    "عسل": 300000, "ريش": 600000, "سوشي": 1000000,
}

FEED_COST_PER_ANIMAL = 125000

TOOLS = {
    "الفأس": {"price": 15, "desc": "يزيد سرعة الحصاد بنسبة 25%"},
    "الدلو": {"price": 20, "desc": "يقلل وقت المحاصيل لنصف المدة"},
    "المعول": {"price": 30, "desc": "يعطي مضاعفة للحصاد x2"},
}

DELIVERY_POOL = [
    ("الكرز", "🍒"), ("الجزر", "🥕"), ("الجبن", "🧀"), ("المانجو", "🥭"),
    ("البطيخ", "🍉"), ("الاكاسيا", "🌼"), ("الموز", "🍌"), ("العسل", "🍯"),
]

CONTINENTS = {
    "آسيا": {
        "plants": [("الزنجبيل", "🫚"), ("الأرز", "🌾"), ("الشاي", "🍃"), ("الخيزران", "🎍"),
                   ("قصب السكر", "🎋"), ("الكركم", "🌼"), ("فول الصويا", "🫘"), ("الموز الآسيوي", "🍌"),
                   ("جوز الهند الآسيوي", "🥥"), ("المانجو الآسيوي", "🥭")],
        "flowers": [("اللوتس", "🪷"), ("الأوركيد", "🌺"), ("الياسمين", "🌸"), ("زهرة الكرز", "🌸"),
                    ("الأقحوان", "🌼"), ("زنبق النمر", "🌷"), ("الفاوانيا", "🌸"), ("لوتس أزرق", "💠"),
                    ("زهرة الخشخاش", "🌺"), ("الجاردينيا", "⚪")],
        "animals": [("الفيل", "🐘"), ("النمر", "🐅"), ("الباندا", "🐼"), ("القرد", "🐒"),
                    ("الجاموس", "🐃"), ("الطاووس", "🦚"), ("الكوبرا", "🐍"), ("وحيد القرن الآسيوي", "🦏"),
                    ("الغزال", "🦌"), ("الببغاء", "🦜")],
    },
    "أفريقيا": {
        "plants": [("الباوباب", "🌳"), ("الذرة الرفيعة", "🌾"), ("الكسافا", "🍠"), ("القطن", "☁️"),
                   ("النخيل", "🌴"), ("الموز الأفريقي", "🍌"), ("الفول السوداني", "🥜"), ("البن", "☕"),
                   ("الدخن", "🌾"), ("الكاكاو", "🍫")],
        "flowers": [("البروتيا", "🌺"), ("الكركديه", "🌺"), ("زهرة الصحراء", "🌵"), ("الجاكاراندا", "💜"),
                    ("الليلي الأفريقي", "🪻"), ("زهرة النار", "🔥"), ("السوسن الأفريقي", "💠"),
                    ("الأقحوان البري", "🌼"), ("زهرة الرمال", "🏜️"), ("الأوركيد الأفريقية", "🌸")],
        "animals": [("الأسد", "🦁"), ("الزرافة", "🦒"), ("الفيل الأفريقي", "🐘"), ("وحيد القرن", "🦏"),
                    ("الحمار الوحشي", "🦓"), ("الفهد", "🐆"), ("الجمل", "🐫"), ("القرد الأفريقي", "🐒"),
                    ("التمساح", "🐊"), ("الغوريلا", "🦍")],
    },
    "أوروبا": {
        "plants": [("العنب الأوروبي", "🍇"), ("الزيتون", "🫒"), ("القمح الأوروبي", "🌾"),
                   ("عباد الشمس", "🌻"), ("البطاطس الأوروبية", "🥔"), ("الشعير", "🌾"),
                   ("التفاح الأوروبي", "🍎"), ("الكستناء", "🌰"), ("الكرز الأوروبي", "🍒"), ("الخوخ", "🍑")],
        "flowers": [("التوليب", "🌷"), ("الخزامى", "💜"), ("الورد", "🌹"), ("النرجس", "🌼"),
                    ("البنفسج", "💐"), ("زنبق الوادي", "🤍"), ("الداليا", "🌺"), ("الأقحوان الأوروبي", "🌼"),
                    ("عباد الشمس البري", "🌻"), ("الكاميليا", "🌸")],
        "animals": [("الدب البني", "🐻"), ("الذئب", "🐺"), ("الثعلب", "🦊"), ("الغزال الأوروبي", "🦌"),
                    ("القندس", "🦫"), ("البومة", "🦉"), ("الأرنب البري", "🐇"), ("الخنزير البري", "🐗"),
                    ("الصقر", "🦅"), ("القنفذ", "🦔")],
    },
    "أمريكا الشمالية": {
        "plants": [("الذرة الأمريكية", "🌽"), ("القطن الأمريكي", "☁️"), ("التبغ", "🍂"), ("القرع", "🎃"),
                   ("التوت البري", "🫐"), ("البقان", "🌰"), ("الصنوبر", "🌲"), ("عباد الشمس الأمريكي", "🌻"),
                   ("فول الصويا الأمريكي", "🫘"), ("البطاطا الحلوة", "🍠")],
        "flowers": [("الخشخاش الكاليفورني", "🧡"), ("عباد الشمس البري", "🌻"), ("الأوركيد البري", "🌸"),
                    ("الياسمين الأمريكي", "🤍"), ("زنبق النار", "🧡"), ("الجلاديولس", "🌺"),
                    ("زهرة الرمان البري", "🌺"), ("الداليا الأمريكية", "🌺"), ("نبتة الربيع", "🌼"),
                    ("زهرة القطن", "🤍")],
        "animals": [("الدب الرمادي", "🐻"), ("النسر الأصلع", "🦅"), ("البيسون", "🦬"), ("الذئب الرمادي", "🐺"),
                    ("الوعل", "🦌"), ("الراكون", "🦝"), ("القندس الأمريكي", "🦫"), ("الأرنب البري", "🐇"),
                    ("الثعلب الأحمر", "🦊"), ("البوما", "🐆")],
    },
    "أمريكا الجنوبية": {
        "plants": [("الكاكاو الأمازوني", "🍫"), ("الأناناس", "🍍"), ("الموز الأمازوني", "🍌"),
                   ("البابايا", "🍈"), ("المطاط", "🌳"), ("الكينوا", "🌾"), ("الكسافا الأمازونية", "🍠"),
                   ("جوز البرازيل", "🌰"), ("قصب السكر الأمازوني", "🎋"), ("الأفوكادو", "🥑")],
        "flowers": [("الأوركيد الأمازونية", "🌺"), ("زهرة الآلام", "💜"), ("البروميليا", "🌸"),
                    ("زنبق الأمازون", "🤍"), ("الهيليكونيا", "🌺"), ("طيور الجنة", "🧡"),
                    ("اللوتس الأمازوني", "🪷"), ("الأوركيد الأرجوانية", "💜"), ("زهرة الفانيليا", "🤍"),
                    ("الكاتليا", "💗")],
        "animals": [("الجاغوار", "🐆"), ("التوكان", "🦜"), ("الأناكوندا", "🐍"), ("الكسلان", "🦥"),
                    ("القرد العنكبوتي", "🐒"), ("الب ببغاء الأحمر", "🦜"), ("التمساح الأمريكي", "🐊"),
                    ("اللاما", "🦙"), ("الكابيبارا", "🐹"), ("النسر الحرشفي", "🦅")],
    },
    "أستراليا": {
        "plants": [("الأوكالبتوس", "🌿"), ("الأكاسيا", "🌼"), ("شجرة الشاي الأسترالية", "🍃"),
                   ("البانكسيا", "🌾"), ("قصب السكر الأسترالي", "🎋"), ("الكيوي الأسترالي", "🥝"),
                   ("المكاديميا", "🌰"), ("الصبار الأسترالي", "🌵"), ("عشب الكنغر", "🌾"),
                   ("شجرة الكينا", "🌳")],
        "flowers": [("الوراتا", "❤️"), ("البروتيا الأسترالية", "🌺"), ("كنغر باو", "🧡"),
                    ("الأوركيد البرية", "🌸"), ("زهرة الشمعة", "🕯️"), ("زهرة الوطل", "💛"),
                    ("الفلانرز الأزرق", "💙"), ("الأكاسيا الذهبية", "💛"), ("السوسن الأسترالي", "💜"),
                    ("زهرة الصحراء الحمراء", "❤️")],
        "animals": [("الكنغر", "🦘"), ("الكوالا", "🐨"), ("خلد الماء", "🦫"), ("الوالابي", "🦘"),
                    ("الإيمو", "🦤"), ("التمساح الأسترالي", "🐊"), ("الوومبت", "🐨"),
                    ("الببغاء الكوكاتو", "🦜"), ("العنكبوت الأسترالي", "🕷️"), ("الشيطان التسماني", "😈")],
    },
}

EXPLORE_COOLDOWN = 1800
ROB_COOLDOWN = 1200
DISCOVERY_MIN_PRICE = 1_000_000_000
DISCOVERY_MAX_PRICE = 1_000_000_000_000

DISCOVERY_ITEMS = {}
for _cont, _cats in CONTINENTS.items():
    for _cat, _items in _cats.items():
        for _name, _emoji in _items:
            DISCOVERY_ITEMS[_name] = {"emoji": _emoji, "category": _cat, "continent": _cont}


def _norm(s: str) -> str:
    s = (s or "").strip()
    s = s.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")
    s = s.replace("ة", "ه")
    return s


def resolve_key(name: str, table: dict):
    if not name:
        return None
    n = _norm(name)
    if n in table:
        return n
    if n.startswith("ال") and n[2:] in table:
        return n[2:]
    alt = "ال" + n
    if alt in table:
        return alt
    for key in table:
        nk = _norm(key)
        if nk == n or nk == n.replace("ال", "", 1) or ("ال" + nk) == n:
            return key
    return None


def fmt_time(seconds: int) -> str:
    seconds = max(0, int(seconds))
    h, rem = divmod(seconds, 3600)
    mnt, sec = divmod(rem, 60)
    if h > 0:
        return f"{h:02d}:{mnt:02d}:{sec:02d}"
    return f"{mnt:02d}:{sec:02d}"


def label(key: str, table: dict) -> str:
    return table[key].get("label", key)


def discovery_unit_price(name: str) -> int:
    h = int(hashlib.md5(name.encode("utf-8")).hexdigest(), 16)
    span = DISCOVERY_MAX_PRICE - DISCOVERY_MIN_PRICE
    return DISCOVERY_MIN_PRICE + (h % span)


async def get_farm_name(uid):
    v = await r.get(f"{uid}:farm_name")
    if isinstance(v, bytes):
        v = v.decode("utf-8")
    return v


async def get_level(uid) -> int:
    return safe_int(await r.get(f"{uid}:farm_level"))


async def get_score(uid) -> int:
    return safe_int(await r.get(f"{uid}:farm_score"))


async def add_score(uid, amount):
    new_score = safe_int(await r.incrby(f"{uid}:farm_score", amount))
    await update_farmers_top(uid, new_score)
    return new_score


async def bump_theft_count(uid):
    new_count = safe_int(await r.incr(f"{uid}:farm_theft_count"))
    await update_thieves_top(uid, new_count)
    return new_count


async def _progress_task(uid, ttype, target=None):
    raw = await r.hgetall(f"{uid}:farm_tasks")
    if not raw:
        return None
    changed = False
    for k_raw, v_raw in raw.items():
        k_field = k_raw.decode() if isinstance(k_raw, bytes) else k_raw
        v_field = v_raw.decode() if isinstance(v_raw, bytes) else v_raw
        t_target, t_need, t_done = v_field.split(",")
        t_need, t_done = int(t_need), int(t_done)
        if k_field != ttype:
            continue
        if target is not None and t_target != "-" and t_target != target:
            continue
        if t_done >= t_need:
            continue
        t_done += 1
        changed = True
        await r.hset(f"{uid}:farm_tasks", k_field, f"{t_target},{t_need},{t_done}")

    if not changed:
        return None

    all_done = True
    raw2 = await r.hgetall(f"{uid}:farm_tasks")
    for v_raw in raw2.values():
        v_field = v_raw.decode() if isinstance(v_raw, bytes) else v_raw
        _, t_need, t_done = v_field.split(",")
        if int(t_done) < int(t_need):
            all_done = False
            break
    if all_done and raw2:
        await r.delete(f"{uid}:farm_tasks")
        new_level = safe_int(await r.incrby(f"{uid}:farm_level", 10))
        return new_level
    return None


async def create_farm(c, m, k, farm_name):
    uid = m.from_user.id
    if not await r.sismember("BankList", uid):
        return await m.reply("• يجب أن يكون لديك حساب بنكي أولاً\n• اكتب ↤ <code>انشاء حساب بنكي</code>")

    if await get_farm_name(uid):
        return await m.reply("• لديك مزرعة بالفعل\n• لعرضها اكتب ↤ <code>معلومات مزرعتي</code>")

    farm_name = farm_name.strip()
    if not farm_name or len(farm_name) > 30:
        return await m.reply("• اسم غير صالح للمزرعة\n• مثال ↤ <code>انشاء مزرعه مزرعتي الجميلة</code>")

    name_key = f"farm_name_global_{farm_name}"
    if await r.get(name_key):
        return await m.reply("• عذراً هذا الاسم مستخدم بالفعل\n• اختر اسماً آخر لمزرعتك")

    await r.set(f"{uid}:farm_name", farm_name)
    await r.set(name_key, uid)
    await r.set(f"{uid}:farm_level", 0)
    await r.set(f"{uid}:farm_score", 0)
    await update_farmers_top(uid, 0)

    await m.reply(
        f"<b>🌾 مبروك! تم إنشاء مزرعتك بنجاح</b>\n"
        f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
        f"• اسم المزرعة ↤ {farm_name}\n"
        f"• المستوى ↤ 0\n\n"
        f"• لعرض متجر المزارع اكتب ↤ <code>متجر المزارع</code>\n"
        f"• لعرض معلومات مزرعتك اكتب ↤ <code>معلومات مزرعتي</code>"
    )


async def require_farm(m):
    uid = m.from_user.id
    if not await r.sismember("BankList", uid):
        await m.reply("• يجب أن يكون لديك حساب بنكي أولاً\n• اكتب ↤ <code>انشاء حساب بنكي</code>")
        return None
    fname = await get_farm_name(uid)
    if not fname:
        await m.reply("• ليس لديك مزرعة بعد\n• أنشئ واحدة بكتابة ↤ <code>انشاء مزرعه (الاسم)</code>")
        return None
    return fname


async def show_farm_info(c, m, k):
    uid = m.from_user.id
    fname = await require_farm(m)
    if not fname:
        return
    level = await get_level(uid)
    score = await get_score(uid)
    balance = safe_int(await r.get(f"{uid}:Floos"))

    seeds_hash = await r.hgetall(f"{uid}:farm_seeds") or {}
    harvest_hash = await r.hgetall(f"{uid}:farm_harvest") or {}
    planted = 0
    for ck in SEEDS:
        planted += safe_int(await r.get(f"{uid}:farm_planted_{ck}"))

    prod_count = 0
    for ak in ANIMALS_PROD:
        prod_count += safe_int(await r.hget(f"{uid}:farm_animals", ak))
    pet_count = 0
    for pk in ANIMALS_PET:
        pet_count += safe_int(await r.hget(f"{uid}:farm_pets", pk))

    text = (
        f"<b>🌾 معلومات مزرعتك</b>\n"
        f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
        f"• الاسم ↤ {fname}\n"
        f"• المستوى ↤ {level}\n"
        f"• نقاط التوب ↤ {score:,}\n"
        f"• رصيدك البنكي ↤ {balance:,} ﷼\n"
        f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
        f"• بذور مملوكة ↤ {sum(safe_int(v) for v in seeds_hash.values())}\n"
        f"• مزروع حالياً ↤ {planted}\n"
        f"• محاصيل جاهزة للبيع ↤ {sum(safe_int(v) for v in harvest_hash.values())}\n"
        f"• حيوانات إنتاجية ↤ {prod_count}\n"
        f"• حيوانات أليفة ↤ {pet_count}\n"
    )
    await m.reply(text)


async def show_farm_level(c, m, k):
    uid = m.from_user.id
    if not await require_farm(m):
        return
    level = await get_level(uid)
    actions = safe_int(await r.get(f"{uid}:farm_harvest_actions"))
    remaining = 3 - (actions % 3) if actions % 3 != 0 else 3
    await m.reply(
        f"<b>⭐ مستوى مزرعتك الحالي ↤ {level}</b>\n"
        f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
        f"• كل 3 عمليات حصاد ناجحة ترفع مستواك درجة\n"
        f"• متبقي {remaining} عملية حصاد ناجحة للمستوى القادم\n"
        f"• إكمال مهام المزرعة اليومية يرفع مستواك 10 درجات دفعة واحدة"
    )


async def delete_farm(c, m, k):
    uid = m.from_user.id
    fname = await require_farm(m)
    if not fname:
        return
    for ck in SEEDS:
        await r.delete(f"{uid}:farm_planted_{ck}")
        await r.delete(f"{uid}:farm_planted_time_{ck}")
    await r.delete(f"{uid}:farm_seeds")
    await r.delete(f"{uid}:farm_harvest")
    await r.delete(f"{uid}:farm_discoveries")
    await r.delete(f"{uid}:farm_animals")
    await r.delete(f"{uid}:farm_pets")
    await r.delete(f"{uid}:farm_products")
    await r.delete(f"{uid}:farm_tasks")
    await r.delete(f"{uid}:farm_delivery_list")
    for ak in ANIMALS_PROD:
        await r.delete(f"{uid}:farm_ready_{ak}")
    await r.delete(f"{uid}:farm_name")
    await r.delete(f"{uid}:farm_level")
    await r.delete(f"{uid}:farm_score")
    await r.delete(f"{uid}:farm_harvest_actions")
    await r.delete(f"farm_name_global_{fname}")
    await r.zrem("top:farmers", str(uid))
    await m.reply("• تم حذف مزرعتك بالكامل بنجاح ")


def _seeds_menu_text():
    text = "<b>🌱 أهلاً بك عزيزي في متجر شراء البذور للمزرعة وتفاصيله:</b>\n\n"
    for key, info in SEEDS.items():
        name = info.get("label", key)
        text += f"- {name} {info['emoji']} ↤ {info['price']:,}﷼ للمستوى {info['level']} فما فوق\n"
    text += "\n• للشراء ↤ <code>شراء بذور القمح 2</code>"
    return text


def _animals_menu_text():
    text = "<b>🐄 أهلاً بك عزيزي في متجر شراء الحيوانات وتفاصيله:</b>\n\n"
    text += "<b>• قائمة الحيوانات الإنتاجية:</b>\n"
    for i, (key, info) in enumerate(ANIMALS_PROD.items(), 1):
        text += f"{i}- {key} {info['emoji']} ↤ {info['price']:,}﷼\n"
    text += "\n━━━━━━━━━━━━\n\n<b>• قائمة الحيوانات الأليفة:</b>\n"
    for i, (key, info) in enumerate(ANIMALS_PET.items(), 1):
        text += f"{i}- {key} {info['emoji']} ↤ {info['price']:,}﷼\n"
    text += "\n• للشراء ↤ <code>شراء دجاج 10</code>"
    return text


def _tools_menu_text():
    text = "<b>🪓 أهلاً بك عزيزي في متجر الأدوات وتفاصيله:</b>\n\n"
    for name, info in TOOLS.items():
        text += f"- {name} ↤ {info['price']} عملة 🪙\n  ↳ {info['desc']}\n\n"
    text += "• للشراء ↤ <code>شراء اداة الفأس 1</code>\n• للاستخدام ↤ <code>استخدام اداة الفأس</code>"
    return text


async def _shop_keyboard(back=False):
    if not back:
        b1 = await create_button_raw("farm", "farm_shop_seeds", "• شراء البذور", callback_data="farmshop:seeds")
        b2 = await create_button_raw("farm", "farm_shop_animals", "• شراء الحيوانات", callback_data="farmshop:animals")
        b3 = await create_button_raw("farm", "farm_shop_tools", "• شراء الأدوات", callback_data="farmshop:tools")
        buttons = [[b1], [b2], [b3]]
    else:
        b_back = await create_button_raw("farm", "farm_shop_back", "رجوع", callback_data="farmshop:main")
        buttons = [[b_back]]
    b_close = await create_button_raw("farm", "farm_shop_close", "اخفاء", callback_data="farmshop:close")
    buttons.append([b_close])
    return {"inline_keyboard": buttons}


async def show_farm_shop(c, m, k):
    if not await require_farm(m):
        return
    text = "• أهلاً بك عزيزي في متجر المزارع، اختر ما تريد من الأزرار:\n"
    await m.reply(text, reply_markup=await _shop_keyboard())


@Client.on_callback_query(filters.regex(r"^farmshop:"), group=-4333)
async def farm_shop_callback(client, callback_query):
    action = callback_query.data.split(":", 1)[1]
    msg = callback_query.message
    uid = callback_query.from_user.id

    if action == "close":
        await callback_query.answer()
        try:
            await client.delete_messages(msg.chat.id, msg.id)
        except Exception:
            pass
        return

    if not msg.reply_to_message or msg.reply_to_message.from_user.id != uid:
        return await callback_query.answer("الامر لايخصك", show_alert=True)

    await callback_query.answer()
    try:
        if action == "seeds":
            await msg.edit_text(_seeds_menu_text(), reply_markup=await _shop_keyboard(back=True))
        elif action == "animals":
            await msg.edit_text(_animals_menu_text(), reply_markup=await _shop_keyboard(back=True))
        elif action == "tools":
            await msg.edit_text(_tools_menu_text(), reply_markup=await _shop_keyboard(back=True))
        elif action == "main":
            await msg.edit_text(
                "• أهلاً بك عزيزي في متجر المزارع، اختر ما تريد من الأزرار:\n",
                reply_markup=await _shop_keyboard()
            )
    except Exception:
        pass


def parse_name_qty(text: str, drop_tokens: int = 1):
    tokens = text.split()
    if len(tokens) <= drop_tokens + 1:
        return None, None
    body = tokens[drop_tokens:]
    qty_tok = body[-1]
    name = " ".join(body[:-1]).strip()
    if not qty_tok.isdigit():
        return name, None
    qty = int(qty_tok)
    if qty <= 0:
        return name, None
    return name, qty


async def buy_seeds(c, m, k, text):
    uid = m.from_user.id
    fname = await require_farm(m)
    if not fname:
        return
    name, qty = parse_name_qty(text, drop_tokens=2)
    if qty is None:
        return await m.reply("• الصيغة غير صحيحة\n• مثال ↤ <code>شراء بذور القمح 2</code>")

    ckey = resolve_key(name, SEEDS)
    if not ckey:
        return await m.reply("• عذراً لا يوجد بذور بهذا الاسم\n• لعرض البذور المتوفرة اكتب ↤ <code>متجر المزارع</code>")

    info = SEEDS[ckey]
    level = await get_level(uid)
    if level < info["level"]:
        return await m.reply(
            f"• للتمكن من شراء بذور {label(ckey, SEEDS)} {info['emoji']}\n"
            f"• يجب ان يكون مستوى مزرعتك {info['level']}"
        )

    total_price = info["price"] * qty
    balance = safe_int(await r.get(f"{uid}:Floos"))
    if balance < total_price:
        return await m.reply(
            f"• رصيدك لا يكفي لهذه العملية\n"
            f"• المطلوب ↤ {total_price:,}﷼\n"
            f"• رصيدك ↤ {balance:,}﷼"
        )

    new_balance = balance - total_price
    await r.set(f"{uid}:Floos", new_balance)
    await enforce_balance_cap(r, m, k, uid)
    await r.hincrby(f"{uid}:farm_seeds", ckey, qty)
    await _progress_task(uid, "buy_seed", ckey)

    await m.reply(
        f"• عملية شراء بذور ناجحة \n"
        f"• البذور ↤ {label(ckey, SEEDS)} {info['emoji']}\n"
        f"• العدد ↤ {qty}\n"
        f"• بقيمة ↤ {total_price:,}﷼\n"
        f"• رصيدك الآن ↤ {new_balance:,}﷼\n\n"
        f"• لزراعتها اكتب ↤ <code>زراعة {ckey} {qty}</code>"
    )


async def show_my_seeds(c, m, k):
    uid = m.from_user.id
    if not await require_farm(m):
        return
    seeds_hash = await r.hgetall(f"{uid}:farm_seeds") or {}
    seeds_hash = {(kk.decode() if isinstance(kk, bytes) else kk): vv for kk, vv in seeds_hash.items()}
    seeds_hash = {kk: vv for kk, vv in seeds_hash.items() if safe_int(vv) > 0}

    if not seeds_hash:
        return await m.reply("• قائمة بذورك فارغة\n• يمكنك شراء بذور بتلك الطريقة ↤ <code>متجر المزارع</code>")

    text = "<b>🌱 قائمة بذورك المتوفرة ↓↓</b>\n\n"
    for ckey, qty in seeds_hash.items():
        info = SEEDS.get(ckey, {"emoji": "🌱"})
        text += f"• {label(ckey, SEEDS)} {info['emoji']} ↤ {int(safe_int(qty))}\n"
    text += "\n• للزراعة ↤ <code>زراعة (البذور) (العدد)</code>"
    await m.reply(text)


async def plant_crop(c, m, k, text):
    uid = m.from_user.id
    if not await require_farm(m):
        return
    name, qty = parse_name_qty(text, drop_tokens=1)
    if qty is None:
        return await m.reply("• الصيغة غير صحيحة\n• مثال ↤ <code>زراعة قمح 10</code>")

    ckey = resolve_key(name, SEEDS)
    if not ckey:
        return await m.reply(
            f"• عذراً عزيزي لا يوجد لديك {name}\n• لمعرفة بذورك اكتب ↤ <code>بذوري</code>"
        )

    owned = safe_int(await r.hget(f"{uid}:farm_seeds", ckey))
    if owned < qty:
        return await m.reply(
            f"• عذراً عزيزي لا يوجد لديك {qty} من بذور {label(ckey, SEEDS)}\n"
            f"• المتوفر لديك ↤ {owned}\n• لمعرفة بذورك اكتب ↤ <code>بذوري</code>"
        )

    if await r.get(f"{uid}:farm_planted_{ckey}"):
        return await m.reply(
            f"• لديك زراعة قائمة بالفعل من {label(ckey, SEEDS)}\n"
            f"• أكمل حصادها أولاً ثم أعد الزراعة"
        )

    info = SEEDS[ckey]
    level = await get_level(uid)
    grow_time = info["grow"] + level * 60

    await r.hincrby(f"{uid}:farm_seeds", ckey, -qty)
    await r.set(f"{uid}:farm_planted_{ckey}", qty)
    await r.set(f"{uid}:farm_planted_time_{ckey}", int(time.time()) + grow_time)

    await m.reply(
        f"• عملية زراعة ناجحة 🌱\n"
        f"• البذور ↤ {label(ckey, SEEDS)} {info['emoji']}\n"
        f"• العدد ↤ {qty}\n"
        f"• وقت النضج ↤ {fmt_time(grow_time)}\n\n"
        f"• لمعرفة مزروعاتك اكتب ↤ <code>مزروعاتي</code>"
    )


async def show_my_plants(c, m, k):
    uid = m.from_user.id
    if not await require_farm(m):
        return
    lines = []
    now = int(time.time())
    for ckey, info in SEEDS.items():
        planted = safe_int(await r.get(f"{uid}:farm_planted_{ckey}"))
        if planted <= 0:
            continue
        ready_at = safe_int(await r.get(f"{uid}:farm_planted_time_{ckey}"))
        remaining = ready_at - now
        if remaining > 0:
            status = f"متبقي للحصاد ⛏️ ↤ {fmt_time(remaining)}"
        else:
            status = "جاهز للحصاد "
        lines.append(f"• {label(ckey, SEEDS)} {info['emoji']} ↤ {planted}\n  ↳ {status}")

    if not lines:
        return await m.reply("• لا توجد لديك مزروعات حالياً\n• لزراعة بذورك اكتب ↤ <code>زراعة (البذور) (العدد)</code>")

    text = "<b>🌿 قائمة المزروعات لديك هي ↓↓</b>\n\n" + "\n\n".join(lines)
    text += "\n\n• يمكنك الحصاد بتلك الطريقة ↤ <code>حصاد (الاسم) (العدد)</code>"
    await m.reply(text)


async def harvest_crop(c, m, k, text):
    uid = m.from_user.id
    if not await require_farm(m):
        return
    name, qty = parse_name_qty(text, drop_tokens=1)
    if qty is None:
        return await m.reply("• الصيغة غير صحيحة\n• مثال ↤ <code>حصاد قمح 10</code>")

    ckey = resolve_key(name, SEEDS)
    if not ckey:
        return await m.reply(f"• عذراً لا توجد لديك زراعة باسم {name}")

    planted = safe_int(await r.get(f"{uid}:farm_planted_{ckey}"))
    if planted <= 0:
        return await m.reply(f"• عذراً لا توجد لديك زراعة من {label(ckey, SEEDS)} حالياً")

    ready_at = safe_int(await r.get(f"{uid}:farm_planted_time_{ckey}"))
    remaining = ready_at - int(time.time())
    if remaining > 0:
        return await m.reply(
            f"• عذراً لا يمكنك حصاد {label(ckey, SEEDS)} {SEEDS[ckey]['emoji']}\n"
            f"• تعال بعد ↤ {fmt_time(remaining)}"
        )

    if qty > planted:
        return await m.reply(f"• لا يوجد لديك {qty} من {label(ckey, SEEDS)} المزروع\n• المتاح للحصاد ↤ {planted}")

    remaining_planted = planted - qty
    if remaining_planted <= 0:
        await r.delete(f"{uid}:farm_planted_{ckey}")
        await r.delete(f"{uid}:farm_planted_time_{ckey}")
    else:
        await r.set(f"{uid}:farm_planted_{ckey}", remaining_planted)

    await r.hincrby(f"{uid}:farm_harvest", ckey, qty)

    points = qty * 2
    actions = safe_int(await r.incr(f"{uid}:farm_harvest_actions"))
    leveled_up = False
    if actions % 3 == 0:
        await r.incr(f"{uid}:farm_level")
        leveled_up = True
    await add_score(uid, points)

    text_out = (
        f"• عملية حصاد ناجحة لـ {label(ckey, SEEDS)} {SEEDS[ckey]['emoji']}\n"
        f"• عددها ↤ {qty}\n"
        f"• تم إعطاءك ↤ {points} \n\n"
        f"• لمعرفة محاصيلك اكتب ↤ <code>محاصيلي</code>"
    )
    if leveled_up:
        lvl = await get_level(uid)
        text_out += f"\n\n<b>⭐ ترقية! ارتفع مستوى مزرعتك إلى {lvl}</b>"
    await m.reply(text_out)


async def show_my_harvest(c, m, k):
    uid = m.from_user.id
    if not await require_farm(m):
        return
    h = await r.hgetall(f"{uid}:farm_harvest") or {}
    h = {(kk.decode() if isinstance(kk, bytes) else kk): vv for kk, vv in h.items()}
    h = {kk: vv for kk, vv in h.items() if safe_int(vv) > 0}
    if not h:
        return await m.reply("• لا توجد لديك محاصيل محصودة بعد\n• احصد مزروعاتك بكتابة ↤ <code>حصاد (البذور) (العدد)</code>")

    text = "<b>🌾 قائمة محاصيلك المحصودة ↓↓</b>\n\n"
    for ckey, qty in h.items():
        info = SEEDS.get(ckey, {"emoji": "🌾", "price": 0})
        sell_price = info["price"] * 2
        text += f"• {label(ckey, SEEDS)} {info['emoji']} ↤ {int(safe_int(qty))} (سعر البيع {sell_price:,}﷼/وحدة)\n"
    text += "\n• للبيع ↤ <code>بيع (البذور) (العدد)</code>"
    await m.reply(text)


async def sell_harvest(c, m, k, name, qty):
    uid = m.from_user.id
    ckey = resolve_key(name, SEEDS)
    if not ckey:
        return None
    owned = safe_int(await r.hget(f"{uid}:farm_harvest", ckey))
    if owned <= 0:
        await m.reply(f"• لا توجد لديك محاصيل محصودة من {label(ckey, SEEDS)}\n• لمعرفة محاصيلك اكتب ↤ <code>محاصيلي</code>")
        return True
    if qty > owned:
        await m.reply(f"• لا يوجد لديك {qty} من {label(ckey, SEEDS)} المحصود\n• المتوفر لديك ↤ {owned}")
        return True

    unit_price = SEEDS[ckey]["price"] * 2
    total = unit_price * qty
    await r.hincrby(f"{uid}:farm_harvest", ckey, -qty)
    new_balance = safe_int(await r.incrby(f"{uid}:Floos", total))
    await enforce_balance_cap(r, m, k, uid)
    await _progress_task(uid, "sell_any")

    await m.reply(
        f"• عملية بيع لـ {label(ckey, SEEDS)} {SEEDS[ckey]['emoji']}\n"
        f"• العدد ↤ {qty}\n"
        f"• بقيمة ↤ {total:,}﷼\n"
        f"• رصيدك الآن ↤ {new_balance:,}﷼"
    )
    return True


async def explore_continent(c, m, k, text):
    uid = m.from_user.id
    if not await require_farm(m):
        return
    cont_raw = text.replace("استكشاف", "", 1).strip()
    ckey = resolve_key(cont_raw, CONTINENTS)
    if not ckey:
        names = "، ".join(CONTINENTS.keys())
        return await m.reply(f"• قارة غير معروفة\n• القارات المتاحة ↤ {names}")

    cooldown_key = f"{uid}:farm_explore_cd"
    ttl = await r.ttl(cooldown_key)
    if ttl and ttl > 0:
        return await m.reply(f"• لا يمكنك استكشاف القارات\n• يجب المحاولة بعد ↤ {fmt_time(ttl)}")

    await r.setex(cooldown_key, EXPLORE_COOLDOWN, "1")

    cont = CONTINENTS[ckey]
    p_name, p_emoji = random.choice(cont["plants"])
    f_name, f_emoji = random.choice(cont["flowers"])
    a_name, a_emoji = random.choice(cont["animals"])
    p_qty = random.randint(1, 10)
    f_qty = random.randint(1, 10)
    a_qty = random.randint(1, 10)

    await r.hincrby(f"{uid}:farm_discoveries", p_name, p_qty)
    await r.hincrby(f"{uid}:farm_discoveries", f_name, f_qty)
    await r.hincrby(f"{uid}:farm_discoveries", a_name, a_qty)

    await m.reply(
        f"• استكشفت قارة {ckey} المليئة بالمفاجآت…\n"
        f"- وقد عادت بعثتك بالاكتشافات التالية:\n\n"
        f"• {p_name} {p_emoji} ↤ {p_qty}\n"
        f"• {f_name} {f_emoji} ↤ {f_qty}\n"
        f"• {a_name} {a_emoji} ↤ {a_qty}\n\n"
        f"- لمعرفة اكتشافاتك اكتب ↤ <code>مكتشفاتي</code>"
    )


async def show_my_discoveries(c, m, k):
    uid = m.from_user.id
    if not await require_farm(m):
        return
    d = await r.hgetall(f"{uid}:farm_discoveries") or {}
    d = {(kk.decode() if isinstance(kk, bytes) else kk): vv for kk, vv in d.items()}
    d = {kk: vv for kk, vv in d.items() if safe_int(vv) > 0}
    if not d:
        return await m.reply("• لا توجد لديك مكتشفات بعد\n• استكشف القارات لتحصل عليها ↤ <code>استكشاف (القارة)</code>")

    text = "<b>• قائمة المكتشفات المتوفرة لديك ↓↓</b>\n\n"
    for name, qty in d.items():
        qty = int(safe_int(qty))
        item = DISCOVERY_ITEMS.get(name, {"emoji": "🎁"})
        total_value = discovery_unit_price(name) * qty
        text += f"• {name} {item['emoji']} ↤ {qty} ({total_value:,} 💸)\n"
    text += "\n- يمكنك بيع مكتشفاتك مثل ↤ <code>بيع (اسم المكتشف) (العدد)</code>"
    await m.reply(text)


async def sell_discovery(c, m, k, name, qty):
    uid = m.from_user.id
    match = None
    for item_name in DISCOVERY_ITEMS:
        if _norm(item_name) == _norm(name):
            match = item_name
            break
    if not match:
        return None
    owned = safe_int(await r.hget(f"{uid}:farm_discoveries", match))
    if owned <= 0:
        await m.reply(f"• لا توجد لديك مكتشفات من {match}\n• لمعرفة مكتشفاتك اكتب ↤ <code>مكتشفاتي</code>")
        return True
    if qty > owned:
        await m.reply(f"• لا يوجد لديك {qty} من {match}\n• المتوفر لديك ↤ {owned}")
        return True

    unit_price = discovery_unit_price(match)
    total = unit_price * qty
    await r.hincrby(f"{uid}:farm_discoveries", match, -qty)
    new_balance = safe_int(await r.incrby(f"{uid}:Floos", total))
    await enforce_balance_cap(r, m, k, uid)
    await _progress_task(uid, "sell_any")

    await m.reply(
        f"• عملية بيع لـ {match} {DISCOVERY_ITEMS[match]['emoji']}\n"
        f"• العدد ↤ {qty}\n"
        f"• بقيمة ↤ {total:,} 💸\n"
        f"• رصيدك الآن ↤ {new_balance:,} ﷼"
    )
    return True


async def buy_animal(c, m, k, text):
    uid = m.from_user.id
    if not await require_farm(m):
        return
    name, qty = parse_name_qty(text, drop_tokens=1)
    if qty is None:
        return None

    akey = resolve_key(name, ANIMALS_PROD)
    is_pet = False
    if not akey:
        akey = resolve_key(name, ANIMALS_PET)
        is_pet = True
    if not akey:
        return None

    table = ANIMALS_PET if is_pet else ANIMALS_PROD
    info = table[akey]
    total_price = info["price"] * qty
    balance = safe_int(await r.get(f"{uid}:Floos"))
    if balance < total_price:
        return await m.reply(
            f"• رصيدك لا يكفي لهذه العملية\n• المطلوب ↤ {total_price:,}﷼\n• رصيدك ↤ {balance:,}﷼"
        )

    new_balance = balance - total_price
    await r.set(f"{uid}:Floos", new_balance)
    await enforce_balance_cap(r, m, k, uid)
    hash_key = f"{uid}:farm_pets" if is_pet else f"{uid}:farm_animals"
    await r.hincrby(hash_key, akey, qty)

    await m.reply(
        f"• عملية شراء حيوان ناجحة \n"
        f"• الحيوان ↤ {akey} {info['emoji']}\n"
        f"• العدد ↤ {qty}\n"
        f"• بقيمة ↤ {total_price:,} ريال 💸\n\n"
        f"- لعرض حيواناتك اكتب ↤ <code>حيواناتي</code>"
    )
    return True


async def show_my_animals(c, m, k):
    uid = m.from_user.id
    if not await require_farm(m):
        return
    pets = await r.hgetall(f"{uid}:farm_pets") or {}
    prod = await r.hgetall(f"{uid}:farm_animals") or {}
    pets = {(kk.decode() if isinstance(kk, bytes) else kk): vv for kk, vv in pets.items()}
    prod = {(kk.decode() if isinstance(kk, bytes) else kk): vv for kk, vv in prod.items()}

    text = "<b>🐾 قائمة الحيوانات الأليفة المتوفرة لديك ↓↓</b>\n\n"
    any_pet = False
    for pk, qty in pets.items():
        qty = int(safe_int(qty))
        if qty <= 0:
            continue
        any_pet = True
        info = ANIMALS_PET.get(pk, {"emoji": "🐾"})
        text += f"• {pk} {info['emoji']} ↤ {qty}\n"
    if not any_pet:
        text += "• لا يوجد لديك حيوانات أليفة\n"

    text += "\n\n<b>🐄 قائمة الحيوانات الإنتاجية المتوفرة لديك ↓↓</b>\n\n"
    any_prod = False
    for pk, qty in prod.items():
        qty = int(safe_int(qty))
        if qty <= 0:
            continue
        any_prod = True
        info = ANIMALS_PROD.get(pk, {"emoji": "🐾"})
        text += f"• {pk} {info['emoji']} ↤ {qty}\n"
    if not any_prod:
        text += "• لا يوجد لديك حيوانات إنتاجية\n• للشراء اكتب ↤ <code>متجر المزارع</code>"
    else:
        text += "\n- يجب إطعامها بكتابة ( <code>اطعام الحيوانات</code> )"

    await m.reply(text)


async def feed_animals(c, m, k):
    uid = m.from_user.id
    if not await require_farm(m):
        return
    prod = await r.hgetall(f"{uid}:farm_animals") or {}
    prod = {(kk.decode() if isinstance(kk, bytes) else kk): int(safe_int(vv)) for kk, vv in prod.items()}
    owned_types = [ak for ak, qty in prod.items() if qty > 0 and ak in ANIMALS_PROD]

    if not owned_types:
        return await m.reply("• قائمة حيواناتك فارغه للشراء اكتب ↤ ( <code>متجر المزارع</code> )")

    pending = [ak for ak in owned_types if await r.get(f"{uid}:farm_ready_{ak}")]
    if pending:
        lines = "\n".join(f"- <code>جمع منتجات {ak}</code>" for ak in owned_types)
        return await m.reply(
            "• لأطعام الحيوانات يجب عليك أولاً جمع منتجات الحيوانات بتلك الاوامر:\n" + lines
        )

    total_animals = sum(prod[ak] for ak in owned_types)
    cost = total_animals * FEED_COST_PER_ANIMAL
    balance = safe_int(await r.get(f"{uid}:Floos"))
    if balance < cost:
        return await m.reply(f"• رصيدك لا يكفي لإطعام حيواناتك\n• المطلوب ↤ {cost:,} ريال 💸\n• رصيدك ↤ {balance:,} ريال 💸")

    new_balance = balance - cost
    await r.set(f"{uid}:Floos", new_balance)
    await enforce_balance_cap(r, m, k, uid)

    for ak in owned_types:
        await r.set(f"{uid}:farm_ready_{ak}", "1")

    await _progress_task(uid, "feed")

    lines = "\n".join(f"- <code>جمع منتجات {ak}</code>" for ak in owned_types)
    await m.reply(
        f"• تم خصم {cost:,} ريال 💸 وتم إطعام جميع الحيوانات بنجاح\n\n"
        f"• لجمع منتجات الحيوانات:\n{lines}"
    )


async def collect_products(c, m, k, animal_word):
    uid = m.from_user.id
    if not await require_farm(m):
        return
    akey = resolve_key(animal_word, ANIMALS_PROD)
    if not akey:
        return None

    owned = safe_int(await r.hget(f"{uid}:farm_animals", akey))
    if owned <= 0:
        return await m.reply(f"• لا تملك حيوانات {akey} لتجمع منتجاتها")

    if not await r.get(f"{uid}:farm_ready_{akey}"):
        return await m.reply(
            f"• منتجات {akey} غير جاهزة بعد\n• أطعم حيواناتك أولاً بكتابة ↤ <code>اطعام الحيوانات</code>"
        )

    info = ANIMALS_PROD[akey]
    product = info["product"]
    await r.delete(f"{uid}:farm_ready_{akey}")
    await r.hincrby(f"{uid}:farm_products", product, owned)

    await m.reply(
        f"• تم جمع منتجات {akey} {info['emoji']} وتم إعطاءك:\n"
        f"• {product} {info['product_emoji']} ↤ {owned}\n\n"
        f"• لعرض منتجاتك اكتب ↤ ( <code>منتجاتي</code> )"
    )
    return True


async def show_my_products(c, m, k):
    uid = m.from_user.id
    if not await require_farm(m):
        return
    prods = await r.hgetall(f"{uid}:farm_products") or {}
    prods = {(kk.decode() if isinstance(kk, bytes) else kk): int(safe_int(vv)) for kk, vv in prods.items()}
    prods = {kk: vv for kk, vv in prods.items() if vv > 0}
    if not prods:
        return await m.reply("• لا توجد لديك منتجات بعد\n• اجمعها بكتابة ↤ <code>جمع منتجات (الحيوان)</code>")

    emoji_map = {info["product"]: info["product_emoji"] for info in ANIMALS_PROD.values()}
    text = "<b>🧺 قائمة المنتجات المتوفرة لديك ↓↓</b>\n\n"
    for pname, qty in prods.items():
        text += f"• {pname} {emoji_map.get(pname, '🧺')} ↤ {qty}\n"
    text += "\n- تستطيع بيعها بتلك الطريقة ↤ <code>بيع (المنتج) (العدد)</code>"
    await m.reply(text)


async def sell_product(c, m, k, name, qty):
    uid = m.from_user.id
    pkey = resolve_key(name, PRODUCT_PRICE)
    if not pkey:
        return None
    owned = safe_int(await r.hget(f"{uid}:farm_products", pkey))
    if owned <= 0:
        await m.reply(f"• لا توجد لديك منتجات من {pkey}\n• لمعرفة منتجاتك اكتب ↤ <code>منتجاتي</code>")
        return True
    if qty > owned:
        await m.reply(f"• لا يوجد لديك {qty} من {pkey}\n• المتوفر لديك ↤ {owned}")
        return True

    unit_price = PRODUCT_PRICE[pkey]
    total = unit_price * qty
    remaining = owned - qty
    await r.hincrby(f"{uid}:farm_products", pkey, -qty)
    new_balance = safe_int(await r.incrby(f"{uid}:Floos", total))
    await enforce_balance_cap(r, m, k, uid)
    await _progress_task(uid, "sell_any")

    await m.reply(
        f"• عملية بيع لـ {pkey}\n"
        f"• العدد ↤ {qty}\n"
        f"• بقيمة ↤ {total:,} ريال 💸\n"
        f"• المتبقي ↤ {remaining}"
    )
    return True


async def delete_animals(c, m, k):
    uid = m.from_user.id
    if not await require_farm(m):
        return
    await r.delete(f"{uid}:farm_animals")
    await r.delete(f"{uid}:farm_pets")
    await r.delete(f"{uid}:farm_products")
    for ak in ANIMALS_PROD:
        await r.delete(f"{uid}:farm_ready_{ak}")
    await m.reply("• تم حذف جميع حيواناتك بنجاح ")


async def show_my_coins(c, m, k):
    uid = m.from_user.id
    coins = safe_int(await r.get(f"{uid}:farm_coins"))
    await m.reply(f"• عملاتك هي ↤ {coins} عملة 🪙")


async def buy_tool(c, m, k, text):
    uid = m.from_user.id
    if not await require_farm(m):
        return
    name, qty = parse_name_qty(text, drop_tokens=2)
    if qty is None:
        return await m.reply("• الصيغة غير صحيحة\n• مثال ↤ <code>شراء اداة الفأس 1</code>")

    tkey = resolve_key(name, TOOLS)
    if not tkey:
        return await m.reply("• اسم الأداة غير معروف\n• لعرض الأدوات المتاحة اكتب ↤ <code>متجر المزارع</code>")

    info = TOOLS[tkey]
    total_cost = info["price"] * qty
    coins = safe_int(await r.get(f"{uid}:farm_coins"))
    if coins < total_cost:
        return await m.reply(f"• لشراء اداة {tkey}\n• يجب عليك جمع {total_cost} عملات 🪙")

    await r.decrby(f"{uid}:farm_coins", total_cost)
    await r.hincrby(f"{uid}:farm_tools", tkey, qty)
    await m.reply(f"• تم شراء اداة {tkey} بنجاح \n• العدد ↤ {qty}")


async def use_tool(c, m, k, tool_word):
    uid = m.from_user.id
    if not await require_farm(m):
        return
    tkey = resolve_key(tool_word, TOOLS)
    if not tkey:
        return await m.reply("• اسم الأداة غير معروف")
    owned = safe_int(await r.hget(f"{uid}:farm_tools", tkey))
    if owned <= 0:
        return await m.reply(f"• لا تملك اداة {tkey}\n• اشترها اولاً من ↤ <code>متجر المزارع</code>")
    await m.reply(f"• تم استخدام اداة {tkey} \n• {TOOLS[tkey]['desc']}")


async def _get_delivery_list(uid):
    raw = await r.get(f"{uid}:farm_delivery_list")
    if raw:
        if isinstance(raw, bytes):
            raw = raw.decode("utf-8")
        items = []
        for part in raw.split("|"):
            if not part:
                continue
            name, emoji, remaining = part.split(",")
            items.append((name, emoji, int(remaining)))
        if items:
            return items

    picks = random.sample(DELIVERY_POOL, k=min(6, len(DELIVERY_POOL)))
    items = [(name, emoji, random.randint(1, 11)) for name, emoji in picks]
    serialized = "|".join(f"{name},{emoji},{remaining}" for name, emoji, remaining in items)
    await r.set(f"{uid}:farm_delivery_list", serialized)
    return items


async def show_delivery_tasks(c, m, k):
    if not await require_farm(m):
        return
    uid = m.from_user.id
    items = await _get_delivery_list(uid)
    text = "<b>• طلبات التوصيل الجديدة 🚚 :</b>\n\n"
    for name, emoji, remaining in items:
        text += f"• {name} {emoji} ↤ المتبقي {remaining}\n"
    text += "\n- عند إكتمال الطلبات اكتب ↤ <code>تنفيذ مهام التوصيل</code>"
    await m.reply(text)


async def execute_delivery_tasks(c, m, k):
    if not await require_farm(m):
        return
    uid = m.from_user.id
    items = await _get_delivery_list(uid)
    text = "• لا تزال لديك مهام لم تكتمل:\n\n"
    for name, emoji, remaining in items:
        text += f"• {name} {emoji} ↤ المتبقي {remaining}\n"
    text += "\n- أكمل المهام ثم اكتب ↤ <code>تنفيذ مهام التوصيل</code>"
    await m.reply(text)


async def _get_daily_tasks(uid):
    raw = await r.hgetall(f"{uid}:farm_tasks")
    if raw:
        tasks = []
        for ttype, val in raw.items():
            ttype = ttype.decode() if isinstance(ttype, bytes) else ttype
            val = val.decode() if isinstance(val, bytes) else val
            target, need, done = val.split(",")
            tasks.append({"type": ttype, "target": target, "need": int(need), "done": int(done)})
        if tasks:
            return tasks

    tasks = []
    seed_key = random.choice(list(SEEDS.keys()))
    tasks.append({"type": "buy_seed", "target": seed_key, "need": random.randint(3, 10), "done": 0})
    tasks.append({"type": "sell_any", "target": "-", "need": random.randint(3, 10), "done": 0})
    tasks.append({"type": "feed", "target": "-", "need": random.randint(3, 10), "done": 0})

    mapping = {t["type"]: f"{t['target']},{t['need']},{t['done']}" for t in tasks}
    await r.hset(f"{uid}:farm_tasks", mapping=mapping)
    return tasks


TASK_LABELS = {
    "buy_seed": lambda t: f"شراء بذور {label(t['target'], SEEDS)} {SEEDS.get(t['target'], {}).get('emoji', '')}",
    "sell_any": lambda t: "بيع المنتجات",
    "feed": lambda t: "أطعام الحيوانات",
}


async def show_farm_tasks(c, m, k):
    if not await require_farm(m):
        return
    uid = m.from_user.id
    tasks = await _get_daily_tasks(uid)
    text = "<b>• المهام اليومية لمزرعتك ↓↓↓</b>\n\n"
    for i, t in enumerate(tasks, 1):
        remaining = max(0, t["need"] - t["done"])
        text += f"{i}- {TASK_LABELS[t['type']](t)} المتبقي ↤ {remaining}\n"
    text += "\n• عند اكتمال المهام يتم رفع مستوى مزرعتك 10 نقاط"
    await m.reply(text)


async def show_farm_top(c, m, k):
    data = await get_farmers_data_fast(c, limit=30)
    if not data:
        return await m.reply("• لا يوجد مزارعون في التوب حتى الآن")

    emojis = ["🥇", "🥈", "🥉"]
    text = "<b>• توب المزارع المزدهرة 🌴 :</b>\n\n"
    for i, entry in enumerate(data[:30]):
        rank_marker = emojis[i] if i < 3 else f"{i + 1})"
        name = str(entry["name"])[:20]
        text += f"{rank_marker} {entry['plants']:,}  l {name}   \n"
    text += " ━━━━━━━━━━━━\n\n"
    text += "<b>• ملاحظة :</b> هذا التوب خاص بـ أصحاب المزارع المزدهرة، اي شخص مخالف للعبة و حاط يوزر بينحظر من اللعبة وتنحذف مزرعته"
    await m.reply(text)


async def rob_farm(c, m, k):
    uid = m.from_user.id
    if not await require_farm(m):
        return
    if not m.reply_to_message:
        return await m.reply("• يجب أن يكون هذا الأمر رداً على شخص آخر")

    target = m.reply_to_message.from_user
    if target.id == uid:
        return await m.reply("• في شخص ينهب نفسة ؟")
    if target.is_bot:
        return await m.reply("• ركز شوي انا بوت")

    target_fname = await get_farm_name(target.id)
    if not target_fname:
        return await m.reply("• ماعنده مزرعه\n• اجعله يكتب اكتب ( <code>انشاء مزرعه</code> )")

    protect_key = f"farm_robbed_protect_{target.id}"
    protect_ttl = await r.ttl(protect_key)
    if protect_ttl and protect_ttl > 0:
        return await m.reply(f"• عذراً ذلك تم نهبة مسبقاً\n• يجب المحاولة بعد ↤ {fmt_time(protect_ttl)}")

    cooldown_key = f"{uid}:farm_rob_cooldown"
    cd_ttl = await r.ttl(cooldown_key)
    if cd_ttl and cd_ttl > 0:
        return await m.reply(f"• توك نهبت مزرعة شخص\n• يجب المحاولة بعد ↤ {fmt_time(cd_ttl)}")

    await r.setex(protect_key, ROB_COOLDOWN, "1")
    await r.setex(cooldown_key, ROB_COOLDOWN, "1")

    dog_count = safe_int(await r.hget(f"{target.id}:farm_pets", "كلاب"))
    fail_chance = min(0.15 + dog_count * 0.12, 0.75)
    if random.random() < fail_chance:
        if dog_count > 0:
            return await m.reply("• فشلت عملية النهب\n• كلب الحراسة نبح عليك 🐶 وطردك من المزرعه")
        return 

    pools = []
    harvest = await r.hgetall(f"{target.id}:farm_harvest") or {}
    for name, qty in harvest.items():
        name = name.decode() if isinstance(name, bytes) else name
        if safe_int(qty) > 0:
            pools.append(("harvest", name, safe_int(qty)))
    disc = await r.hgetall(f"{target.id}:farm_discoveries") or {}
    for name, qty in disc.items():
        name = name.decode() if isinstance(name, bytes) else name
        if safe_int(qty) > 0:
            pools.append(("discovery", name, safe_int(qty)))
    animals = await r.hgetall(f"{target.id}:farm_animals") or {}
    for name, qty in animals.items():
        name = name.decode() if isinstance(name, bytes) else name
        if safe_int(qty) > 0:
            pools.append(("animal", name, safe_int(qty)))

    if not pools:
        return await m.reply("• فشلت عملية النهب\n• مزرعة هذا الشخص فارغة ولا يوجد بها شيء لنهبه")

    kind, item_name, item_owned = random.choice(pools)
    steal_qty = min(random.randint(1, 10), item_owned)

    if kind == "harvest":
        hash_field = "farm_harvest"
        emoji = SEEDS.get(item_name, {}).get("emoji", "🌾")
    elif kind == "discovery":
        hash_field = "farm_discoveries"
        emoji = DISCOVERY_ITEMS.get(item_name, {}).get("emoji", "🎁")
    else:
        hash_field = "farm_animals"
        emoji = ANIMALS_PROD.get(item_name, {}).get("emoji", "🐾")

    await r.hincrby(f"{target.id}:{hash_field}", item_name, -steal_qty)
    await r.hincrby(f"{uid}:{hash_field}", item_name, steal_qty)
    await bump_theft_count(uid)

    await m.reply(
        f"• نجحت عملية النهب 🥷\n"
        f"• قمت بنهب ↤ {item_name} {emoji}\n"
        f"• العدد ↤ {steal_qty}\n\n"
        f"• مزرعة {target.first_name} محمية الآن لمدة 20 دقيقة"
    )


GIFTABLE_TABLES = [
    ("farm_harvest", SEEDS, "crop"),
    ("farm_discoveries", DISCOVERY_ITEMS, "discovery"),
    ("farm_animals", ANIMALS_PROD, "animal"),
]


async def try_farm_gift(c, m, k, quantity, item_name):
    uid = m.from_user.id
    target = m.reply_to_message.from_user if m.reply_to_message else None
    if target is None:
        return None

    resolved = None
    hash_field = None
    emoji = "🎁"
    for field, table, kind in GIFTABLE_TABLES:
        if kind == "discovery":
            for name in table:
                if _norm(name) == _norm(item_name):
                    resolved = name
                    emoji = table[name]["emoji"]
                    hash_field = field
                    break
        else:
            key = resolve_key(item_name, table)
            if key:
                resolved = key
                emoji = table[key]["emoji"]
                hash_field = field
        if resolved:
            break

    if not resolved:
        return None

    if target.id == uid:
        return await m.reply("• لا يمكنك إهداء نفسك")
    if target.is_bot:
        return await m.reply("• لا يمكنك إهداء البوت")

    owned = safe_int(await r.hget(f"{uid}:{hash_field}", resolved))
    if owned < quantity:
        return await m.reply(f"• لا يوجد لديك {quantity} من {resolved}\n• المتوفر لديك ↤ {owned}")

    await r.hincrby(f"{uid}:{hash_field}", resolved, -quantity)
    await r.hincrby(f"{target.id}:{hash_field}", resolved, quantity)

    await m.reply(
        f"• تم إهداء {resolved} {emoji} بنجاح 🎁\n"
        f"• العدد ↤ {quantity}\n"
        f"• إلى ↤ {target.first_name}"
    )
    return True


def is_farm_style_command(text: str) -> bool:
    tokens = text.split()
    if len(tokens) < 2:
        return False
    second = tokens[1]
    if second in ("بذور", "اداة"):
        return True
    if len(tokens) >= 3 and tokens[-1].isdigit() and not second.isdigit():
        return True
    return False


# ═══════════════════════════════════════════════════════════════
#  الموجّه الرئيسي لأوامر المزرعة
# ═══════════════════════════════════════════════════════════════

async def handle_farm_commands(c, m, k, text):
    text = (text or "").strip()
    if not text:
        return None

    if text in ("المزرعه", "المزرعة", "مساعدة المزرعه", "مساعدة المزرعة"):
        return await m.reply("""
            <b>🌾 لعبة المزرعة</b>\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n

• <b>انشاء مزرعه</b>
ـ تنشئ مزرعتك وتحط لها اسم

• <b>معلومات مزرعتي</b>
- يعرض معلومات مزرعتك بالكامل

• <b>مستوى مزرعتي</b>
- يعرض لك مستوى مزرعتك والتي تجمعها عبر حصاد المزروعات

• <b>متجر المزارع</b>
- يعرض البذور والحيوانات المتاحه فالمتجر للشراء

• <b>بذوري</b>
- يعرض لك البذور التي اشتريتها من المتجر

• <b>محاصيلي</b>
- يجيب المحاصيل التي قمت بحصادها

• <b>حيواناتي</b>
- يجيب لك الحيوانات التي اشتريتها من المتجر

• <b>شراء بذور (البذور) (العدد)</b>
- تشتري بذور لمزرعتك

• <b>زراعة (البذور) (العدد)</b>
- تزرع البذور عشان تقوم بحصادها

• <b>حصاد (البذور) (العدد)</b>
- تقوم بحصاد مزروعاتك وترقي مستوى مزرعتك لكل 3 محاصيل تترقى مزرعتك وتنافس التوب

• <b>مزروعاتي</b>
- تشوف البذور التي قمت بزراعتها ومتى وقت حصادها

• <b>بيع (البذور) (العدد)</b>
- تبيع المحاصيل التي قمت بحصادها وتاخذ دبل قيمة شراءها

• <b>شراء (الحيوان) (العدد)</b>
ـ تشتري حيوانات وتقوم باطعامها وجمع منتجاتها

• <b>اطعام الحيوانات</b>
- تقوم بإطعام حيواناتك عشان تجمع منتجاتها

• <b>جمع منتجات الحيوانات</b>
- جمع منتجات الغنم
- جمع منتجات البقر
- جمع منتجات الدجاج

• <b>منتجاتي</b>
- تشوف وشهي التي انتجتها حيواناتك وتبيعها

• <b>بيع (المنتج) (العدد)</b>
- تبيع منتجاتك بعد جمعها

• <b>حذف الحيوانات</b>
- تحذف جميع حيواناتك

• <b>حذف مزرعتي</b>
- تقوم بحذفها بشكل كامل

• <b>مهام المزرعه</b>
- مهام يومية لمزرعتك عند تنفيذها يزيد مستوى مزرعتك 10

• <b>توب المزارع</b>
- تشوف اكثر مستويات للمزارع بالتوب
-
        """)


    if text == "انشاء مزرعه" or text == "انشاء مزرعة":
        return await m.reply("• اكتب اسم مزرعتك بعد الأمر\n• مثال ↤ انشاء مزرعه مزرعتي الجميلة")
    if text.startswith("انشاء مزرعه ") or text.startswith("انشاء مزرعة "):
        farm_name = text.split(" ", 2)[2].strip()
        return await create_farm(c, m, k, farm_name)

    if text == "معلومات مزرعتي":
        return await show_farm_info(c, m, k)

    if text == "مستوى مزرعتي":
        return await show_farm_level(c, m, k)

    if text == "متجر المزارع":
        return await show_farm_shop(c, m, k)

    if text == "بذوري":
        return await show_my_seeds(c, m, k)

    if text == "محاصيلي":
        return await show_my_harvest(c, m, k)

    if text == "حيواناتي":
        return await show_my_animals(c, m, k)

    if text == "منتجاتي":
        return await show_my_products(c, m, k)

    if text == "مكتشفاتي":
        return await show_my_discoveries(c, m, k)

    if text == "مزروعاتي":
        return await show_my_plants(c, m, k)

    if text == "عملاتي":
        return await show_my_coins(c, m, k)

    if text.startswith("شراء بذور "):
        return await buy_seeds(c, m, k, text)

    if text.startswith("شراء اداة "):
        return await buy_tool(c, m, k, text)

    if text.startswith("استخدام اداة "):
        tool_word = text.replace("استخدام اداة ", "", 1).strip()
        return await use_tool(c, m, k, tool_word)

    if text.startswith("زراعة ") or text.startswith("زراعه "):
        return await plant_crop(c, m, k, text)

    if text.startswith("حصاد "):
        return await harvest_crop(c, m, k, text)

    if text.startswith("استكشاف "):
        return await explore_continent(c, m, k, text)

    if text == "اطعام الحيوانات":
        return await feed_animals(c, m, k)

    if text.startswith("جمع منتجات "):
        animal_word = text.replace("جمع منتجات ", "", 1).strip()
        return await collect_products(c, m, k, animal_word)

    if text == "حذف الحيوانات":
        return await delete_animals(c, m, k)

    if text == "حذف مزرعتي" or text == "مسح مزرعتي":
        return await delete_farm(c, m, k)

    if text == "مهام المزرعه" or text == "مهام المزرعة":
        return await show_farm_tasks(c, m, k)

    if text == "توب المزارع":
        return await show_farm_top(c, m, k)

    if text == "نهب":
        return await rob_farm(c, m, k)

    if text == "مهام التوصيل":
        return await show_delivery_tasks(c, m, k)

    if text == "تنفيذ مهام التوصيل":
        return await execute_delivery_tasks(c, m, k)

    if text.startswith("شراء ") and is_farm_style_command(text):
        result = await buy_animal(c, m, k, text)
        if result is not None:
            return result
        return None  # لم يُطابق أي حيوان/أليف معروف، تجاهل بصمت (لا تعارض رسائل)

    if text.startswith("بيع ") and is_farm_style_command(text):
        name, qty = parse_name_qty(text, drop_tokens=1)
        if qty is None:
            return None
        for sell_fn in (sell_harvest, sell_discovery, sell_product):
            result = await sell_fn(c, m, k, name, qty)
            if result is not None:
                return result
        return None  # لا يخص المزرعة، اترك السلسلة تكمل بصمت

    return None
