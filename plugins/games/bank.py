from helpers.context import get_global_r, get_global_dev, get_global_k
import html
r = get_global_r()
Dev_FINAL = get_global_dev()
k = get_global_k()
from compat import Client, filters
from compat import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import random, re, time, string, asyncio
from threading import Thread
from compat import *
from compat import *
from compat import *
import settings
from helpers.ranks import *
from helpers.games import *
from ..protect import get_top, get_emoji_bank, _decode_if_bytes, get_chat_score, get_chat_name_from_api
from ..buttons import register_buttons, get_button_custom, get_button_color, create_button_raw
from helpers.redis import r
from .top import get_top_interactive, handle_top_settings
from .marriage import handle_marriage_commands
from .words import handle_word_games
from .questions import handle_quiz_games
from .math import handle_math_games
from .mediagames import handle_media_games
from .addgame import handle_social_games
from .quiz import handle_quiz_commands
from .farm import *
from .clubs import *
from .devgames import handle_public_games
from .hazr import handle_hazr_game
from helpers.http import telegram_api_post
from .roulette import handle_social_gamesx
from .utils import (
    add_game_earnings, show_game_earnings_top,
    MAX_BALANCE, is_owner_only, safe_int,
    grant_medal, get_medals, enforce_balance_cap,
)
from .shop import (
    handle_loan_commands, handle_stock_commands, handle_personal_shop_commands,
    is_user_jailed, jail_should_block,
)
from compat import InputMediaPhoto, InputMediaVideo
from compat import Client
from helpers.replies_store import (
    REPLIES,
    plugins_games_bank_1001,
    plugins_games_bank_1004,
    plugins_games_bank_1017,
    plugins_games_bank_1043,
    plugins_games_bank_1045,
    plugins_games_bank_1079,
    plugins_games_bank_1110,
    plugins_games_bank_1267,
    plugins_games_bank_1272,
    plugins_games_bank_1276,
    plugins_games_bank_1282,
    plugins_games_bank_1285,
    plugins_games_bank_1289,
    plugins_games_bank_1343,
    plugins_games_bank_1366,
    plugins_games_bank_1377,
    plugins_games_bank_1409,
    plugins_games_bank_1421,
    plugins_games_bank_1424,
    plugins_games_bank_1444,
    plugins_games_bank_1460,
    plugins_games_bank_1463,
    plugins_games_bank_1465,
    plugins_games_bank_1468,
    plugins_games_bank_1472,
    plugins_games_bank_1477,
    plugins_games_bank_1485,
    plugins_games_bank_1487,
    plugins_games_bank_1502,
    plugins_games_bank_1510,
    plugins_games_bank_1515,
    plugins_games_bank_1520,
    plugins_games_bank_1528,
    plugins_games_bank_1543,
    plugins_games_bank_1551,
    plugins_games_bank_1555,
    plugins_games_bank_1559,
    plugins_games_bank_1564,
    plugins_games_bank_1584,
    plugins_games_bank_1591,
    plugins_games_bank_1595,
    plugins_games_bank_1603,
    plugins_games_bank_1605,
    plugins_games_bank_1607,
    plugins_games_bank_1620,
    plugins_games_bank_1629,
    plugins_games_bank_1633,
    plugins_games_bank_1641,
    plugins_games_bank_1643,
    plugins_games_bank_1656,
    plugins_games_bank_1665,
    plugins_games_bank_1669,
    plugins_games_bank_1688,
    plugins_games_bank_1692,
    plugins_games_bank_1696,
    plugins_games_bank_1712,
    plugins_games_bank_1716,
    plugins_games_bank_1720,
    plugins_games_bank_1744,
    plugins_games_bank_1750,
    plugins_games_bank_1754,
    plugins_games_bank_1756,
    plugins_games_bank_1763,
    plugins_games_bank_1768,
    plugins_games_bank_1771,
    plugins_games_bank_1773,
    plugins_games_bank_1781,
    plugins_games_bank_1828,
    plugins_games_bank_1834,
    plugins_games_bank_1836,
    plugins_games_bank_1840,
    plugins_games_bank_1843,
    plugins_games_bank_1848,
    plugins_games_bank_1851,
    plugins_games_bank_1857,
    plugins_games_bank_1861,
    plugins_games_bank_1866,
    plugins_games_bank_1868,
    plugins_games_bank_1877,
    plugins_games_bank_1881,
    plugins_games_bank_1891,
    plugins_games_bank_1898,
    plugins_games_bank_1915,
    plugins_games_bank_1919,
    plugins_games_bank_1930,
    plugins_games_bank_1940,
    plugins_games_bank_1948,
    plugins_games_bank_1952,
    plugins_games_bank_1976,
    plugins_games_bank_1990,
    plugins_games_bank_1994,
    plugins_games_bank_2010,
    plugins_games_bank_2023,
    plugins_games_bank_2209,
    plugins_games_bank_232,
    plugins_games_bank_239,
    plugins_games_bank_552,
    plugins_games_bank_555,
    plugins_games_bank_559,
    plugins_games_bank_569,
    plugins_games_bank_571,
    plugins_games_bank_576,
    plugins_games_bank_582,
    plugins_games_bank_594,
    plugins_games_bank_607,
    plugins_games_bank_610,
    plugins_games_bank_614,
    plugins_games_bank_627,
    plugins_games_bank_638,
    plugins_games_bank_655,
    plugins_games_bank_666,
    plugins_games_bank_668,
    plugins_games_bank_671,
    plugins_games_bank_675,
    plugins_games_bank_685,
    plugins_games_bank_688,
    plugins_games_bank_690,
    plugins_games_bank_693,
    plugins_games_bank_713,
    plugins_games_bank_722,
    plugins_games_bank_730,
    plugins_games_bank_738,
    plugins_games_bank_751,
    plugins_games_bank_759,
    plugins_games_bank_770,
    plugins_games_bank_775,
    plugins_games_bank_777,
    plugins_games_bank_780,
    plugins_games_bank_784,
    plugins_games_bank_786,
    plugins_games_bank_789,
    plugins_games_bank_804,
    plugins_games_bank_818,
    plugins_games_bank_832,
    plugins_games_bank_835,
    plugins_games_bank_839,
    plugins_games_bank_841,
    plugins_games_bank_844,
    plugins_games_bank_847,
    plugins_games_bank_855,
    plugins_games_bank_868,
    plugins_games_bank_871,
    plugins_games_bank_873,
    plugins_games_bank_876,
    plugins_games_bank_883,
    plugins_games_bank_886,
    plugins_games_bank_888,
    plugins_games_bank_891,
    plugins_games_bank_898,
    plugins_games_bank_905,
    plugins_games_bank_908,
    plugins_games_bank_910,
    plugins_games_bank_926,
    plugins_games_bank_948,
    plugins_games_bank_965,
    plugins_games_bank_966,
    plugins_games_bank_977,
    plugins_games_bank_979,
    plugins_games_bank_981,
    plugins_games_bank_983,
    plugins_games_bank_985,
    plugins_games_bank_990,
    plugins_games_bank_993,
    plugins_games_bank_997,
    plugins_games_bank_999,
)
BUTTONS_DEFINITIONS = {
    "bank": {
        "name": "أزرار البنك",
        "buttons": [
            {"id": "shop_cars", "default": "السيارات"},
            {"id": "shop_planes", "default": "الطائرات"},
            {"id": "shop_realestate", "default": "العقارات"},
            {"id": "shop_jewelry", "default": "المجوهرات"},
            {"id": "shop_foods", "default": "المأكولات"},
            {"id": "shop_back", "default": "رجوع"},
            {"id": "shop_close", "default": "إغلاق"},
        ]
    }
}

register_buttons(BUTTONS_DEFINITIONS)


async def update_top_score(user_id: int, amount: int, score_type: str):
    key = f"top:{score_type}"
    await r.zincrby(key, amount, str(user_id))
    
async def send_api_message(c, chat_id, text, reply_markup=None, parse_mode="HTML", reply_to_message_id=None):
    br = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    bot_token = c.bot_token if hasattr(c, "bot_token") else settings.TOKEN
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    if reply_to_message_id:
        payload["reply_to_message_id"] = reply_to_message_id
    return await telegram_api_post(bot_token, "sendMessage", payload)

async def edit_api_message(c, chat_id, message_id, text, reply_markup=None, parse_mode="HTML"):
    br = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    bot_token = c.bot_token if hasattr(c, "bot_token") else settings.TOKEN
    payload = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text,
        "parse_mode": parse_mode
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    return await telegram_api_post(bot_token, "editMessageText", payload)

SHOP_PRODUCTS = {
    "بنتلي": {"price": 3100000, "category": "cars", "name": "بنتلي"},
    "رولزرويس": {"price": 3200000, "category": "cars", "name": "رولزرويس"},
    "مرسيدس": {"price": 3000000, "category": "cars", "name": "مرسيدس"},
    "باترول": {"price": 1100000, "category": "cars", "name": "باترول"},
    "فيلار": {"price": 1000000, "category": "cars", "name": "فيلار"},
    "اكسنت": {"price": 900000, "category": "cars", "name": "اكسنت"},
    "كامري": {"price": 800000, "category": "cars", "name": "كامري"},
    "النترا": {"price": 700000, "category": "cars", "name": "النترا"},
    "أوبتيما": {"price": 650000, "category": "cars", "name": "أوبتيما"},
    "هايلكس": {"price": 600000, "category": "cars", "name": "هايلكس"},
    "ماليبو": {"price": 550000, "category": "cars", "name": "ماليبو"},
    "سوناتا": {"price": 500000, "category": "cars", "name": "سوناتا"},
    "مازدا": {"price": 450000, "category": "cars", "name": "مازدا"},
    "كورولا": {"price": 400000, "category": "cars", "name": "كورولا"},
    "سيفيك": {"price": 350000, "category": "cars", "name": "سيفيك"},
    "كونكورد": {"price": 50000000, "category": "planes", "name": "كونكورد"},
    "بوينغ": {"price": 30000000, "category": "planes", "name": "بوينغ"},
    "أباتشي": {"price": 20000000, "category": "planes", "name": "أباتشي"},
    "فانتوم": {"price": 10000000, "category": "planes", "name": "فانتوم"},
    "شبح": {"price": 10000000, "category": "planes", "name": "شبح"},
    "إيرباص": {"price": 5000000, "category": "planes", "name": "إيرباص"},
    "خاصه": {"price": 2000000, "category": "planes", "name": "خاصه"},
    "درون": {"price": 2000000, "category": "planes", "name": "درون"},
    "سيسنا": {"price": 500000, "category": "planes", "name": "سيسنا"},
    "منطاد": {"price": 100000, "category": "planes", "name": "منطاد"},
    "جزيرة": {"price": 500000, "category": "realestate", "name": "جزيرة"},
    "منتجع": {"price": 250000, "category": "realestate", "name": "منتجع"},
    "برج": {"price": 1000000, "category": "realestate", "name": "برج"},
    "فندق": {"price": 500000, "category": "realestate", "name": "فندق"},
    "قصر": {"price": 100000, "category": "realestate", "name": "قصر"},
    "فيلا": {"price": 500000, "category": "realestate", "name": "فيلا"},
    "منزل": {"price": 100000, "category": "realestate", "name": "منزل"},
    "شقة": {"price": 50000, "category": "realestate", "name": "شقة"},
    "تاج": {"price": 500000, "category": "jewelry", "name": "تاج"},
    "زمرد": {"price": 300000, "category": "jewelry", "name": "زمرد"},
    "ياقوت": {"price": 200000, "category": "jewelry", "name": "ياقوت"},
    "ماسه": {"price": 100000, "category": "jewelry", "name": "ماسه"},
    "قلاده": {"price": 500000, "category": "jewelry", "name": "قلاده"},
    "سوار": {"price": 200000, "category": "jewelry", "name": "سوار"},
    "خاتم": {"price": 50000, "category": "jewelry", "name": "خاتم"},
    "قرط": {"price": 25000, "category": "jewelry", "name": "قرط"},
    "كافيار": {"price": 50000, "category": "foods", "name": "كافيار"},
    "ستيك": {"price": 25000, "category": "foods", "name": "ستيك"},
    "سوشي": {"price": 15000, "category": "foods", "name": "سوشي"},
    "برغر": {"price": 5000, "category": "foods", "name": "برغر"},
    "بيتزا": {"price": 4000, "category": "foods", "name": "بيتزا"},
    "شاورما": {"price": 2000, "category": "foods", "name": "شاورما"},
    "ببسي": {"price": 1000, "category": "foods", "name": "ببسي"},
    "قهوة": {"price": 500, "category": "foods", "name": "قهوة"},
}

RANK_UPGRADES = {
    1: {"name": "سواق", "salary": 500},
    2: {"name": "طيار", "salary": 2500},
    3: {"name": "خياط", "salary": 9000},
    4: {"name": "مهندس", "salary": 18000},
    5: {"name": "معلم", "salary": 25000},
    6: {"name": "طبيب", "salary": 40000},
    7: {"name": "محامي", "salary": 70000},
    8: {"name": "قاضي", "salary": 100000},
    9: {"name": "مضمد", "salary": 20000},
    10: {"name": "تاجر", "salary": 50000},
}

TREASURES = [
    {"name": "قطعة اثرية", "credit": 40000},
    {"name": "حجر الماسي", "credit": 35000},
    {"name": "لباس قديم", "credit": 10000},
    {"name": "عصى سحرية", "credit": 23000},
    {"name": "جوال نوكيا", "credit": 8000},
    {"name": "صدف", "credit": 27000},
    {"name": "ابريق صدئ", "credit": 18000},
    {"name": "قناع فرعوني", "credit": 100000},
    {"name": "جرة ذهب", "credit": 50000},
    {"name": "مصباح فضي", "credit": 36000},
    {"name": "لوحة نحاسية", "credit": 29000},
    {"name": "جوارب قديمة", "credit": 1000},
    {"name": "اناء فخاري", "credit": 16000},
    {"name": "خوذة محارب", "credit": 12000},
    {"name": "سيف جدي مرزوق", "credit": 19000},
    {"name": "مكنسة جدتي", "credit": 14000},
    {"name": "فأس ارطغرل", "credit": 26000},
    {"name": "بندقية", "credit": 22000},
    {"name": "كبريت ناري", "credit": 11000},
    {"name": "فرو ثعلب", "credit": 33000},
    {"name": "جلد تمساح", "credit": 40000},
    {"name": "باقة ورود", "credit": 17000},
]

def get_random_sell_price(original_price):
    return int(original_price * random.uniform(0.8, 1.2))

def is_what_percent_of(num_a, num_b):
    return (num_a / num_b) * 100

@Client.on_message(filters.group, group=33)
async def gamesHandler(c,m):
    br = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    k = await br.get(f'{Dev_FINAL}:botkey')
    channel = await br.get(f'{Dev_FINAL}:BotChannel') if await br.get(f'{Dev_FINAL}:BotChannel') else ''
    await gamesFunc(c,m,k,channel)

@Client.on_message(filters.dice & filters.group, group=45)
async def diceFunc(c,m):
   br = get_global_r()
   Dev_FINAL = get_global_dev()
   k = get_global_k()
   if await br.get(f'{m.chat.id}:disableGames:{Dev_FINAL}'):  return False
   if m.dice and m.dice.emoji == "🎲":
     k = await br.get(f'{Dev_FINAL}:botkey')
     if m.dice.value == 6:
        await asyncio.sleep(3)
        ra = 100
        if await r.get(f'{m.from_user.id}:Floos'):
           get = int((await r.get(f'{m.from_user.id}:Floos')) or 0)
           await r.set(f'{m.from_user.id}:Floos',get+ra)
           await enforce_balance_cap(r, m, k, m.from_user.id)
           floos = int((await r.get(f'{m.from_user.id}:Floos')) or 0)
        else:
           floos = ra
           await r.set(f'{m.from_user.id}:Floos',ra)
           await enforce_balance_cap(r, m, k, m.from_user.id)
        await add_game_earnings(m.from_user.id, m.chat.id, ra, m.id)
        return await m.reply(plugins_games_bank_232(k, m.link, k, floos), disable_web_page_preview=True)
     else:
        await asyncio.sleep(3)
        return await m.reply(plugins_games_bank_239(k))

async def show_bank_menu(c, msg, k, user_id, chat_id):
    br = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    bank_text = f"""
{k} عشان تسوي حساب لازم تختار نوع البطاقة

{k}  <code>الاهلي</code>
{k}  <code>الراجحي</code>
{k}  <code>الانماء</code>

{k} - اضغط للنسخ
"""
    await send_api_message(c, chat_id, bank_text, reply_markup=None)

async def finalize_account_creation(c, msg, k, user_id, chat_id, bank_type):
    br = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if bank_type == 'ahli':
        bank_name = 'الاهلي'
    elif bank_type == 'rajehi':
        bank_name = 'الراجحي'
    elif bank_type == 'anmua':
        bank_name = 'الانماء'
    else:
        return
    id_num = '4'
    for a in range(15):
        id_num += str(random.randint(1, 9))
    card = random.choice(['الاهلي كارد', 'الراجحي كارد', 'الإنماء كارد', 'مدى كارد'])
    rank_index = 1
    floos = 2000
    await r.set(f'{user_id}:bankType', bank_name)
    await r.set(f'{user_id}:bankID', int(id_num))
    await r.set(f'{user_id}:bankCard', card)
    await r.set(f'{user_id}:rank_index', rank_index)
    await r.set(f'{user_id}:rank', 0)
    user_info = await c.get_users(user_id)
    await r.set(f'{user_id}:bankName', user_info.first_name)
    await r.sadd('BankList', user_id)
    await r.set(f'{id_num}:getAccBank', user_id)
    await r.set(f'{user_id}:Floos', floos)
    await enforce_balance_cap(r, msg, k, user_id)
    await r.delete(f'{user_id}:createBank:{chat_id}')
    success_text = f"""
{k} تم إنشاء حسابك البنكي بنجاح! 🎉

{k} البنك : {bank_name}
{k} رقم الحساب : <code>{id_num}</code>
{k} نوع البطاقة : {card}
{k} الرصيد : {floos:,} ﷼ 💸
{k} الوظيفة : {RANK_UPGRADES[rank_index]['name']}

{k} اكتب <code>حسابي</code> لمشاهدة تفاصيل حسابك
"""
    try:
        await msg.edit_text(success_text, reply_markup=None)
    except Exception:
        await msg.reply(success_text)
    if await br.get(f'DevGroup:{Dev_FINAL}'):
        try:
            await c.send_message(
                int((await br.get(f'DevGroup:{Dev_FINAL}')) or 0),
                f' ⟨ {user_info.mention()} ⟩\n{k} سوى حساب بالبنك\n{k} رقم حسابه ( <code>{id_num}</code> )'
            )
        except:
            pass

async def show_shop_menu(c, m, k):
    br = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    user_id = m.from_user.id
    shop_text = """
 <b>المتجر</b>
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
• أهلاً بك في المتجر 
• اختر القسم المناسب :
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
"""
    cars_btn = await create_button_raw("bank", f"shop_cars:{user_id}", "السيارات", callback_data=f"shop_cars:{user_id}")
    planes_btn = await create_button_raw("bank", f"shop_planes:{user_id}", "الطائرات", callback_data=f"shop_planes:{user_id}")
    realestate_btn = await create_button_raw("bank", f"shop_realestate:{user_id}", "العقارات", callback_data=f"shop_realestate:{user_id}")
    jewelry_btn = await create_button_raw("bank", f"shop_jewelry:{user_id}", "المجوهرات", callback_data=f"shop_jewelry:{user_id}")
    foods_btn = await create_button_raw("bank", f"shop_foods:{user_id}", "المأكولات", callback_data=f"shop_foods:{user_id}")
    close_btn = await create_button_raw("bank", f"shop_close:{user_id}", "إغلاق", callback_data=f"shop_close:{user_id}")
    reply_markup = {
        "inline_keyboard": [
            [jewelry_btn, realestate_btn],
            [planes_btn, cars_btn],
            [foods_btn],
            [close_btn]
        ]
    }
    await send_api_message(c, m.chat.id, shop_text, reply_markup=reply_markup)

async def show_cars_menu(c, m, k, callback_query=None):
    br = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    user_id = callback_query.from_user.id if callback_query else m.from_user.id
    cars_text = """
 <b>السيارات المتوفرة</b>
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
• رولزرويس | السعر : 3200000 ﷼
• بنتلي | السعر : 3100000 ﷼
• مرسيدس | السعر : 3000000 ﷼
• باترول | السعر : 1100000 ﷼
• أوبتيما | السعر : 6,500000 ﷼
• ماليبو | السعر : 5,500000 ﷼
• كامري | السعر : 4,500000 ﷼
• سيفيك | السعر : 3,500000 ﷼
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
• للشراء : شراء 2 بنتلي
• للبيع : بيع 2 بنتلي
• للإهداء : اهداء 2 بنتلي (بالرد)

"""
    back_btn = await create_button_raw("bank", f"shop_back:{user_id}", "رجوع", callback_data=f"shop_back:{user_id}")
    close_btn = await create_button_raw("bank", f"shop_close:{user_id}", "إغلاق", callback_data=f"shop_close:{user_id}")
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(**back_btn)],
        [InlineKeyboardButton(**close_btn)]
    ])
    if callback_query:
        try:
            await callback_query.edit_message_text(cars_text, reply_markup=reply_markup)
        except Exception as e:
            print(f"Error: {e}")
    else:
        return await m.reply(cars_text, reply_markup=reply_markup)

async def show_planes_menu(c, m, k, callback_query=None):
    br = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    user_id = callback_query.from_user.id if callback_query else m.from_user.id
    planes_text = """
 <b>الطيارات المتوفرة</b>
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
• كونكورد | السعر : 5000000000 ﷼
• بوينغ | السعر : 3000000000 ﷼
• أباتشي | السعر : 2000000000 ﷼
• فانتوم | السعر : 1000000000 ﷼
• إيرباص | السعر : 500000000 ﷼
• درون | السعر : 200000000 ﷼
• سيسنا | السعر : 50000000 ﷼
• منطاد | السعر : 10000000 ﷼
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
• للشراء : شراء 1 بوينغ
• للبيع : بيع 2 أباتشي
• للإهداء : اهداء 1 درون (بالرد)

"""
    back_btn = await create_button_raw("bank", f"shop_back:{user_id}", "رجوع", callback_data=f"shop_back:{user_id}")
    close_btn = await create_button_raw("bank", f"shop_close:{user_id}", "إغلاق", callback_data=f"shop_close:{user_id}")
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(**back_btn)],
        [InlineKeyboardButton(**close_btn)]
    ])
    if callback_query:
        try:
            await callback_query.edit_message_text(planes_text, reply_markup=reply_markup)
        except Exception as e:
            print(f"Error: {e}")
    else:
        return await m.reply(planes_text, reply_markup=reply_markup)

async def show_realestate_menu(c, m, k, callback_query=None):
    br = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    user_id = callback_query.from_user.id if callback_query else m.from_user.id
    realestate_text = """
 <b>العقارات المتوفرة</b>
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
• جزيرة | السعر : 50000000 ﷼
• منتجع | السعر : 25000000 ﷼
• برج | السعر : 10000000 ﷼
• فندق | السعر : 5000000 ﷼
• قصر | السعر : 1000000 ﷼
• فيلا | السعر : 500000 ﷼
• منزل | السعر : 100000 ﷼
• شقة | السعر : 50000 ﷼
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
• للشراء : شراء 1 جزيرة
• للبيع : بيع 2 فيلا
• للإهداء : اهداء 1 منزل (بالرد)

"""
    back_btn = await create_button_raw("bank", f"shop_back:{user_id}", "رجوع", callback_data=f"shop_back:{user_id}")
    close_btn = await create_button_raw("bank", f"shop_close:{user_id}", "إغلاق", callback_data=f"shop_close:{user_id}")
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(**back_btn)],
        [InlineKeyboardButton(**close_btn)]
    ])
    if callback_query:
        try:
            await callback_query.edit_message_text(realestate_text, reply_markup=reply_markup)
        except Exception as e:
            print(f"Error: {e}")
    else:
        return await m.reply(realestate_text, reply_markup=reply_markup)

async def show_jewelry_menu(c, m, k, callback_query=None):
    br = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    user_id = callback_query.from_user.id if callback_query else m.from_user.id
    jewelry_text = """
 <b>المجوهرات المتوفرة</b>
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
• تاج | السعر : 5000000 ﷼
• زمرد | السعر : 3000000 ﷼
• ياقوت | السعر : 2000000 ﷼
• ماسه | السعر : 1000000 ﷼
• قلاده | السعر : 500000 ﷼
• سوار | السعر : 200000 ﷼
• خاتم | السعر : 50000 ﷼
• قرط | السعر : 25000 ﷼
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
• للشراء : شراء 2 تاج
• للبيع : بيع 3 زمرد
• للإهداء : اهداء 1 خاتم (بالرد)

"""
    back_btn = await create_button_raw("bank", f"shop_back:{user_id}", "رجوع", callback_data=f"shop_back:{user_id}")
    close_btn = await create_button_raw("bank", f"shop_close:{user_id}", "إغلاق", callback_data=f"shop_close:{user_id}")
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(**back_btn)],
        [InlineKeyboardButton(**close_btn)]
    ])
    if callback_query:
        try:
            await callback_query.edit_message_text(jewelry_text, reply_markup=reply_markup)
        except Exception as e:
            print(f"Error: {e}")
    else:
        return await m.reply(jewelry_text, reply_markup=reply_markup)

async def show_foods_menu(c, m, k, callback_query=None):
    br = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    user_id = callback_query.from_user.id if callback_query else m.from_user.id
    foods_text = """
 <b>المأكولات المتوفرة</b>
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
• كافيار | السعر : 50000 ﷼
• ستيك | السعر : 25000 ﷼
• سوشي | السعر : 15000 ﷼
• برغر | السعر : 5000 ﷼
• بيتزا | السعر : 4000 ﷼
• شاورما | السعر : 2000 ﷼
• ببسي | السعر : 1000 ﷼
• قهوة | السعر : 500 ﷼
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
• للشراء : شراء 2 كافيار
• للبيع : بيع 3 ستيك
• للإهداء : اهداء 1 برغر (بالرد)

"""
    back_btn = await create_button_raw("bank", f"shop_back:{user_id}", "رجوع", callback_data=f"shop_back:{user_id}")
    close_btn = await create_button_raw("bank", f"shop_close:{user_id}", "إغلاق", callback_data=f"shop_close:{user_id}")
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(**back_btn)],
        [InlineKeyboardButton(**close_btn)]
    ])
    if callback_query:
        try:
            await callback_query.edit_message_text(foods_text, reply_markup=reply_markup)
        except Exception as e:
            print(f"Error: {e}")
    else:
        return await m.reply(foods_text, reply_markup=reply_markup)

async def handle_shop_commands(c, m, k, text):
    br = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if text in ['متجر البنك', 'المتجر', 'المعرض', 'معرض']:
        return await show_shop_menu(c, m, k)
    if text.startswith('شراء ') and is_farm_style_command(text):
        return None
    if text.startswith('شراء '):
        return await handle_buy(c, m, k, text)
    if text.startswith('بيع ') and is_farm_style_command(text):
        return None
    if text.startswith('بيع '):
        return await handle_sell(c, m, k, text)
    if text.startswith('اهداء ') and m.reply_to_message:
        return await handle_gift(c, m, k, text)
    if text == 'ممتلكاتي':
        return await show_my_items(c, m, k)
    if text == 'ممتلكاته' and m.reply_to_message:
        return await show_his_items(c, m, k)
    return None

async def handle_buy(c, m, k, text):
    br = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    
    if text.startswith('شراء ') and any(x in text for x in ['جنود', 'جندي', 'رشاش', 'رشاشات', 'طائرة', 'طائرات', 'قنبلة', 'قنابل', 'صاروخ', 'صواريخ', 'مدفع', 'مدافع', 'مدرعة', 'مدرعات', 'مضاد', 'بطاقة', 'اسهم', 'سهم', 'شراء اسهم', 'بيع اسهم']):
        return None
    
    if text.startswith('شراء لاعب') or text.startswith('شراء ') and 'لاعب' in text:
        return None
    
    try:
        import re
        text_clean = re.sub(r'[^\w\s]', '', text)
        parts = text_clean.split()
        if len(parts) < 3:
            return await m.reply(plugins_games_bank_552(k))
        quantity_str = ''.join(filter(str.isdigit, parts[1]))
        if not quantity_str:
            return await m.reply(plugins_games_bank_555(k))
        quantity = int(quantity_str)
        item_parts = parts[2:]
        if not item_parts:
            return await m.reply(plugins_games_bank_559(k))
        item_name = " ".join(item_parts).strip()
        found_item = None
        for product_key, product_info in SHOP_PRODUCTS.items():
            if item_name.lower() == product_info['name'].lower():
                found_item = product_key
                break
            if item_name.lower() in product_info['name'].lower():
                found_item = product_key
        if not found_item:
            return await m.reply(plugins_games_bank_569(k))
        if not await r.sismember('BankList', m.from_user.id):
            return await m.reply(plugins_games_bank_571(k))
        price = SHOP_PRODUCTS[found_item]['price']
        total_price = price * quantity
        user_balance = int(await r.get(f'{m.from_user.id}:Floos') or 0)
        if user_balance < total_price:
            return await m.reply(plugins_games_bank_576(k, total_price, user_balance))
        new_balance = user_balance - total_price
        await r.set(f'{m.from_user.id}:Floos', new_balance)
        await enforce_balance_cap(r, m, k, m.from_user.id)
        await r.hincrby(f'{m.from_user.id}:items', found_item, quantity)
        new_balance_str = await r.get(f'{m.from_user.id}:Floos')
        await m.reply(plugins_games_bank_582(k, k, found_item, k, quantity, k, total_price, k, new_balance_str, k))
    except Exception as e:
        print(f"Error in handle_buy: {e}")
        return await m.reply(plugins_games_bank_594(k))

async def handle_sell(c, m, k, text):
    br = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if text.startswith('بيع لاعب'):
        return None
    try:
        import re
        text_clean = re.sub(r'[^\w\s]', '', text)
        parts = text_clean.split()
        if len(parts) < 3:
            return await m.reply(plugins_games_bank_607(k))
        quantity_str = ''.join(filter(str.isdigit, parts[1]))
        if not quantity_str:
            return await m.reply(plugins_games_bank_610(k))
        quantity = int(quantity_str)
        item_parts = parts[2:]
        if not item_parts:
            return await m.reply(plugins_games_bank_614(k))
        item_name = " ".join(item_parts).strip()
        found_item = None
        for product_key, product_info in SHOP_PRODUCTS.items():
            if item_name.lower() == product_info['name'].lower():
                found_item = product_key
                break
            if item_name.lower() in product_info['name'].lower():
                found_item = product_key
        if not found_item:
            return None
        user_items = await r.hget(f'{m.from_user.id}:items', found_item)
        if not user_items or int(user_items) < quantity:
            return await m.reply(plugins_games_bank_627(k, quantity, found_item))
        original_price = SHOP_PRODUCTS[found_item]['price']
        sell_price_per_item = get_random_sell_price(original_price)
        total_sell_price = sell_price_per_item * quantity
        await r.hincrby(f'{m.from_user.id}:items', found_item, -quantity)
        await r.incrby(f'{m.from_user.id}:Floos', total_sell_price)
        new_balance = await r.get(f'{m.from_user.id}:Floos')
        remaining_items = await r.hget(f'{m.from_user.id}:items', found_item) or 0
        original_total = original_price * quantity
        profit_percent = ((total_sell_price - original_total) / original_total) * 100
        profit_emoji = "📈" if profit_percent > 0 else "📉"
        await m.reply(plugins_games_bank_638(k, profit_emoji, k, found_item, k, quantity, k, sell_price_per_item, k, total_sell_price, k, profit_percent, k, new_balance, k, remaining_items, found_item))
        if int(remaining_items) == 0:
            await r.hdel(f'{m.from_user.id}:items', found_item)
    except Exception as e:
        print(f"Error in handle_sell: {e}")
        return await m.reply(plugins_games_bank_655(k))

async def handle_gift(c, m, k, text):
    br = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    try:
        import re
        text_clean = re.sub(r'[^\w\s]', '', text)
        parts = text_clean.split()
        if len(parts) < 3:
            return await m.reply(plugins_games_bank_666(k))
        if not m.reply_to_message:
            return await m.reply(plugins_games_bank_668(k))
        quantity_str = ''.join(filter(str.isdigit, parts[1]))
        if not quantity_str:
            return await m.reply(plugins_games_bank_671(k))
        quantity = int(quantity_str)
        item_parts = parts[2:]
        if not item_parts:
            return await m.reply(plugins_games_bank_675(k))
        item_name = " ".join(item_parts).strip()
        found_item = None
        for product_key, product_info in SHOP_PRODUCTS.items():
            if item_name.lower() == product_info['name'].lower():
                found_item = product_key
                break
            if item_name.lower() in product_info['name'].lower():
                found_item = product_key
        if not found_item:
            farm_gift_result = await try_farm_gift(c, m, k, quantity, item_name)
            if farm_gift_result is not None:
                return farm_gift_result
            return await m.reply(plugins_games_bank_685(k))
        target_user = m.reply_to_message.from_user
        if target_user.id == m.from_user.id:
            return await m.reply(plugins_games_bank_688(k))
        if target_user.is_bot:
            return await m.reply(plugins_games_bank_690(k))
        user_items = await r.hget(f'{m.from_user.id}:items', found_item)
        if not user_items or int(user_items) < quantity:
            return await m.reply(plugins_games_bank_693(k, quantity, found_item))
        await r.hincrby(f'{m.from_user.id}:items', found_item, -quantity)
        await r.hincrby(f'{target_user.id}:items', found_item, quantity)
        remaining_items = await r.hget(f'{m.from_user.id}:items', found_item) or 0
        if int(remaining_items) == 0:
            await r.hdel(f'{m.from_user.id}:items', found_item)
        try:
            await c.send_message(
                target_user.id,
                f"""
{k} وصلتك هدية جديدة! 🎉

{k} من : {m.from_user.first_name}
{k} المنتج : {found_item}
{k} العدد : {quantity}
{k} اكتب <code>ممتلكاتي</code> لمشاهدة ممتلكاتك
"""
            )
        except Exception:
            pass
        await m.reply(plugins_games_bank_713(k, k, target_user.id, html.escape(str(target_user.first_name)), k, found_item, k, quantity))
    except Exception as e:
        print(f"Error in handle_gift: {e}")
        return await m.reply(plugins_games_bank_722(k))

async def show_my_items(c, m, k):
    br = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    user_items = await r.hgetall(f'{m.from_user.id}:items')
    if not user_items:
        return await m.reply(plugins_games_bank_730(k))
    lines = []
    for item, qty in user_items.items():
        qty_num = int(qty)
        if qty_num > 0:
            clean_name = item.replace("🚗", "").replace("✈️", "").replace("🏘️", "").strip()
            lines.append(f"• {clean_name} ↤︎ {qty_num}")
    if not lines:
        return await m.reply(plugins_games_bank_738(k))
    items_text = f"<b>ممتلكات {m.from_user.first_name}</b> :\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
    items_text += "\n".join(lines)
    items_text += f"\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n• للبيع : <code>بيع 2 سوشي</code>\n• للإهداء : <code>اهداء 1 سوشي</code> (بالرد)"
    await m.reply(items_text)

async def show_his_items(c, m, k):
    br = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    target_user = m.reply_to_message.from_user
    user_items = await r.hgetall(f'{target_user.id}:items')
    if not user_items:
        return await m.reply(plugins_games_bank_751(k, target_user.first_name))
    lines = []
    for item, qty in user_items.items():
        qty_num = int(qty)
        if qty_num > 0:
            clean_name = item.replace("🚗", "").replace("✈️", "").replace("🏘️", "").strip()
            lines.append(f"• {clean_name} ↤︎ {qty_num}")
    if not lines:
        return await m.reply(plugins_games_bank_759(k, target_user.first_name))
    items_text = f"<b>ممتلكات {target_user.first_name}</b> :\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
    items_text += "\n".join(lines)
    items_text += f"\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯"
    await m.reply(items_text)

async def handle_mudaraba(c, m, k, text):
    br = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if not await r.sismember('BankList', m.from_user.id):
        return await m.reply(plugins_games_bank_770(k))
    cooldown = await r.get(f'{m.from_user.id}:BankWaitMDRB')
    if cooldown:
        ttl = await r.ttl(f'{m.from_user.id}:BankWaitMDRB')
        wait = time.strftime('%M:%S', time.gmtime(ttl))
        return await m.reply(plugins_games_bank_775(k, k, wait))
    if text == 'مضاربه':
        return await m.reply(plugins_games_bank_777(k))
    parts = text.split()
    if len(parts) != 2:
        return await m.reply(plugins_games_bank_780(k))
    try:
        amount = int(parts[1])
    except:
        return await m.reply(plugins_games_bank_784(k))
    if amount < 100:
        return await m.reply(plugins_games_bank_786(k))
    user_balance = int(await r.get(f'{m.from_user.id}:Floos') or 0)
    if user_balance < amount:
        return await m.reply(plugins_games_bank_789(k))
    win_chance = random.randint(1, 100)
    profit_percent = random.randint(1, 90)
    if win_chance > 50:
        profit_amount = int(amount * profit_percent / 100)
        multiplier = 1
        double_key = f'{m.from_user.id}:wheel_double'
        if await r.get(double_key):
            multiplier = 2
        profit_amount *= multiplier
        new_balance = user_balance + profit_amount
        await r.set(f'{m.from_user.id}:Floos', new_balance)
        await enforce_balance_cap(r, m, k, m.from_user.id)
        await add_game_earnings(m.from_user.id, m.chat.id, profit_amount, m.id)
        await r.setex(f'{m.from_user.id}:BankWaitMDRB', 900, 1)
        await m.reply(plugins_games_bank_804(k, amount, k, profit_percent, k, profit_amount, k, new_balance))
    else:
        loss_amount = int(amount * profit_percent / 100)
        new_balance = user_balance - loss_amount
        await r.set(f'{m.from_user.id}:Floos', new_balance)
        await enforce_balance_cap(r, m, k, m.from_user.id)
        await r.setex(f'{m.from_user.id}:BankWaitMDRB', 900, 1)
        await m.reply(plugins_games_bank_818(k, amount, k, profit_percent, k, loss_amount, k, new_balance))

async def handle_bet(c, m, k, text):
    br = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if not await r.sismember('BankList', m.from_user.id):
        return await m.reply(plugins_games_bank_832(k))
    parts = text.split()
    if len(parts) != 2:
        return await m.reply(plugins_games_bank_835(k))
    try:
        amount = int(parts[1])
    except:
        return await m.reply(plugins_games_bank_839(k))
    if amount < 1000:
        return await m.reply(plugins_games_bank_841(k))
    user_balance = int(await r.get(f'{m.from_user.id}:Floos') or 0)
    if user_balance < amount:
        return await m.reply(plugins_games_bank_844(k, user_balance))
    betting_host = await br.get(f'betting_host_{m.chat.id}')
    if betting_host:
        return await m.reply(plugins_games_bank_847(k, amount))
    await br.set(f'betting_host_{m.chat.id}', m.from_user.id)
    await br.set(f'betting_amount_{m.chat.id}', amount)
    await br.sadd(f'betting_players_{m.chat.id}', m.from_user.id)
    await br.set(f'betting_player_amount_{m.chat.id}_{m.from_user.id}', amount)
    new_balance = user_balance - amount
    await r.set(f'{m.from_user.id}:Floos', new_balance)
    await enforce_balance_cap(r, m, k, m.from_user.id)
    await m.reply(plugins_games_bank_855(k, k, amount, k, amount, k))

async def handle_bet_join(c, m, k, text):
    br = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if not await r.sismember('BankList', m.from_user.id):
        return await m.reply(plugins_games_bank_868(k))
    betting_host = await br.get(f'betting_host_{m.chat.id}')
    if not betting_host:
        return await m.reply(plugins_games_bank_871(k))
    if str(betting_host) == str(m.from_user.id):
        return await m.reply(plugins_games_bank_873(k))
    already_joined = await br.sismember(f'betting_players_{m.chat.id}', m.from_user.id)
    if already_joined:
        return await m.reply(plugins_games_bank_876(k))
    parts = text.split()
    if len(parts) != 2:
        return
    try:
        amount = int(parts[1])
    except:
        return await m.reply(plugins_games_bank_883(k))
    bet_amount = await br.get(f'betting_amount_{m.chat.id}')
    if not bet_amount:
        return await m.reply(plugins_games_bank_886(k))
    if amount != int(bet_amount):
        return await m.reply(plugins_games_bank_888(k, bet_amount))
    user_balance = int(await r.get(f'{m.from_user.id}:Floos') or 0)
    if user_balance < amount:
        return await m.reply(plugins_games_bank_891(k, user_balance))
    new_balance = user_balance - amount
    await r.set(f'{m.from_user.id}:Floos', new_balance)
    await enforce_balance_cap(r, m, k, m.from_user.id)
    await br.sadd(f'betting_players_{m.chat.id}', m.from_user.id)
    await br.set(f'betting_player_amount_{m.chat.id}_{m.from_user.id}', amount)
    players_count = await br.scard(f'betting_players_{m.chat.id}')
    await m.reply(plugins_games_bank_898(k, m.from_user.first_name, amount, k, players_count))

async def handle_bet_end(c, m, k, text):
    br = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if not await r.sismember('BankList', m.from_user.id):
        return await m.reply(plugins_games_bank_905(k))
    betting_host = await br.get(f'betting_host_{m.chat.id}')
    if not betting_host:
        return await m.reply(plugins_games_bank_908(k))
    if str(betting_host) != str(m.from_user.id):
        return await m.reply(plugins_games_bank_910(k))
    players_raw = await br.smembers(f'betting_players_{m.chat.id}')
    players_list = []
    for player in players_raw:
        players_list.append(player.decode() if isinstance(player, bytes) else player)
    if len(players_list) < 2:
        for player in players_list:
            player_amount = await br.get(f'betting_player_amount_{m.chat.id}_{player}')
            if player_amount:
                current = int(await r.get(f'{player}:Floos') or 0)
                await r.set(f'{player}:Floos', current + int(player_amount))
                await enforce_balance_cap(r, m, k, player)
                await br.delete(f'betting_player_amount_{m.chat.id}_{player}')
        await br.delete(f'betting_host_{m.chat.id}')
        await br.delete(f'betting_amount_{m.chat.id}')
        await br.delete(f'betting_players_{m.chat.id}')
        return await m.reply(plugins_games_bank_926(k))
    total_amount = 0
    for player in players_list:
        player_amount = await br.get(f'betting_player_amount_{m.chat.id}_{player}')
        if player_amount:
            total_amount += int(player_amount)
    winner = random.choice(players_list)
    tax = int(total_amount * 0.25)
    win_amount = total_amount - tax
    winner_balance = int(await r.get(f'{winner}:Floos') or 0)
    await r.set(f'{winner}:Floos', winner_balance + win_amount)
    await enforce_balance_cap(r, m, k, winner)
    for player in players_list:
        await br.delete(f'betting_player_amount_{m.chat.id}_{player}')
    await br.delete(f'betting_host_{m.chat.id}')
    await br.delete(f'betting_amount_{m.chat.id}')
    await br.delete(f'betting_players_{m.chat.id}')
    try:
        winner_user = await c.get_users(int(winner))
        winner_name = winner_user.first_name
    except:
        winner_name = f"مستخدم {winner}"
    await m.reply(plugins_games_bank_948(k, k, winner_name, k, total_amount, k, tax, k, win_amount))

async def handle_medals(c, m, k, text):
    br = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    target = m.reply_to_message.from_user if m.reply_to_message else m.from_user
    count, details = await get_medals(r, target.id)
    if count <= 0:
        if target.id == m.from_user.id:
            return await m.reply(plugins_games_bank_965(k))
        return await m.reply(plugins_games_bank_966(k))
    txt = f"{k} ميداليات {target.first_name} : {count} 🎖\n"
    for i, item in enumerate(details[-10:], 1):
        txt += f"{i}) {item['reason']}\n"
    await m.reply(txt)

async def handle_donate(c, m, k, text):
    br = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if not await r.sismember('BankList', m.from_user.id):
        return await m.reply(plugins_games_bank_977(k))
    if not m.reply_to_message:
        return await m.reply(plugins_games_bank_979(k))
    if m.reply_to_message.from_user.id == m.from_user.id:
        return await m.reply(plugins_games_bank_981(k))
    if m.reply_to_message.from_user.is_bot:
        return await m.reply(plugins_games_bank_983(k))
    if not await r.sismember('BankList', m.reply_to_message.from_user.id):
        return await m.reply(plugins_games_bank_985(k))
    cooldown = await r.get(f'{m.from_user.id}:BankWaitDONATE')
    if cooldown:
        ttl = await r.ttl(f'{m.from_user.id}:BankWaitDONATE')
        wait = time.strftime('%M:%S', time.gmtime(ttl))
        return await m.reply(plugins_games_bank_990(k, k, wait))
    parts = text.split()
    if len(parts) != 2:
        return await m.reply(plugins_games_bank_993(k))
    try:
        amount = int(parts[1])
    except:
        return await m.reply(plugins_games_bank_997(k))
    if amount < 1000:
        return await m.reply(plugins_games_bank_999(k))
    if amount > 10000:
        return await m.reply(plugins_games_bank_1001(k))
    user_balance = int(await r.get(f'{m.from_user.id}:Floos') or 0)
    if user_balance < amount:
        return await m.reply(plugins_games_bank_1004(k, user_balance))
    target_user = m.reply_to_message.from_user
    target_balance = int(await r.get(f'{target_user.id}:Floos') or 0)
    new_balance = user_balance - amount
    new_target = target_balance + amount
    await r.set(f'{m.from_user.id}:Floos', new_balance)
    await enforce_balance_cap(r, m, k, m.from_user.id)
    await r.set(f'{target_user.id}:Floos', new_target)
    await enforce_balance_cap(r, m, k, target_user.id)
    donated_before = int(await r.get(f'{m.from_user.id}:donated') or 0)
    donated_new = donated_before + amount
    await r.set(f'{m.from_user.id}:donated', donated_new)
    await r.setex(f'{m.from_user.id}:BankWaitDONATE', 600, 1)
    await m.reply(plugins_games_bank_1017(k, k, amount, k, target_user.id, html.escape(str(target_user.first_name)), k, new_balance, k, donated_new))
    try:
        await c.send_message(
            target_user.id,
            f"""
{k} وصلك تبرع جديد! 🎉

{k} من : {m.from_user.first_name}
{k} المبلغ : {amount} ﷼
"""
        )
    except:
        pass

async def handle_my_donations(c, m, k, text):
    br = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if not await r.sismember('BankList', m.from_user.id):
        return await m.reply(plugins_games_bank_1043(k))
    donated = int(await r.get(f'{m.from_user.id}:donated') or 0)
    await m.reply(plugins_games_bank_1045(k, donated))

def get_current_rank(user_rank_index):
    return RANK_UPGRADES.get(user_rank_index)

async def gamesFunc(c,m,k,channel):
   br = get_global_r()
   Dev_FINAL = get_global_dev()
   k = get_global_k()
   if not await check_global_restrictions(c, m, k):
       return
   if not await br.get(f'{m.chat.id}:enable:{Dev_FINAL}'):
       return
   if await br.get(f'{m.from_user.id}:gbangames:{Dev_FINAL}'):  return
   if await br.get(f'{m.from_user.id}:mute:{m.chat.id}{Dev_FINAL}'):  return
   if await br.get(f'{m.chat.id}:addCustom:{m.from_user.id}{Dev_FINAL}'):  return
   if await br.get(f'{m.chat.id}addCustomG:{m.from_user.id}{Dev_FINAL}'):  return
   if await br.get(f'{m.chat.id}:delCustom:{m.from_user.id}{Dev_FINAL}') or await br.get(f'{m.chat.id}:delCustomG:{m.from_user.id}{Dev_FINAL}'):  return
   if await br.get(f'{m.chat.id}:mute:{Dev_FINAL}') and not await admin_pls(m.from_user.id,m.chat.id):  return
   if await br.get(f'{m.from_user.id}:mute:{Dev_FINAL}'):  return
   text = m.text or '' 
   name = await br.get(f'{Dev_FINAL}:BotName') if await br.get(f'{Dev_FINAL}:BotName') else 'فوق'
   if text.startswith(f'{name} '):
      text = text.replace(f'{name} ','')
   if await br.get(f'{m.chat.id}:Custom:{m.chat.id}{Dev_FINAL}&text={text}'):
     text = await br.get(f'{m.chat.id}:Custom:{m.chat.id}{Dev_FINAL}&text={text}')
   if await br.get(f'Custom:{Dev_FINAL}&text={text}'):
     text = await br.get(f'Custom:{Dev_FINAL}&text={text}')

   if await check_and_guard_locked_command(c, m, k, text):
       return

   if await br.get(f'{m.chat.id}:disableGames:{Dev_FINAL}'):  return

   if jail_should_block(text) and await is_user_jailed(r, m.from_user.id):
       debt = safe_int((await r.get(f'{m.from_user.id}:LoanDebt')) or 0)
       return await m.reply(plugins_games_bank_1079(k, k, k, debt))

   if text == 'توب القروبات' or text == 'توب القروبات اللاعبة' or text == 'القروبات اللاعبة':
       return await show_game_earnings_top(c, m, k)

   if text == 'انشاء حساب بنكي':
     if await r.sismember('BankList', m.from_user.id):
       bank = await r.get(f'{m.from_user.id}:bankType')
       acc_id_raw = await r.get(f'{m.from_user.id}:bankID')
       if acc_id_raw is None:
         bank = bank or 'الاهلي'
         new_id = '4'
         for _a in range(15):
           new_id += str(random.randint(1, 9))
         card = random.choice(['الاهلي كارد', 'الراجحي كارد', 'الإنماء كارد', 'مدى كارد'])
         await r.set(f'{m.from_user.id}:bankType', bank)
         await r.set(f'{m.from_user.id}:bankID', int(new_id))
         if not await r.get(f'{m.from_user.id}:bankCard'):
           await r.set(f'{m.from_user.id}:bankCard', card)
         await r.set(f'{new_id}:getAccBank', m.from_user.id)
         if not await r.get(f'{m.from_user.id}:bankName'):
           await r.set(f'{m.from_user.id}:bankName', m.from_user.first_name)
         acc_id = int(new_id)
       else:
         acc_id = safe_int(acc_id_raw)
       return await m.reply(plugins_games_bank_1110(k, bank, k, k, acc_id))
     else:
       await r.set(f'{m.from_user.id}:createBank:{m.chat.id}',1,ex=300)
       return await show_bank_menu(c, m, k, m.from_user.id, m.chat.id)

   stock_result = await handle_stock_commands(c, m, k, text)
   if stock_result is not None:
       return stock_result

   shop_result = await handle_shop_commands(c, m, k, text)
   if shop_result is not None:
       return shop_result

   pshop_result = await handle_personal_shop_commands(c, m, k, text)
   if pshop_result is not None:
       return pshop_result

   loan_result = await handle_loan_commands(c, m, k, text)
   if loan_result is not None:
       return loan_result

   if text.startswith('مضاربه'):
     if text == 'مضاربه':
       return await handle_mudaraba(c, m, k, text)
     if text.startswith('مضاربه '):
       return await handle_mudaraba(c, m, k, text)

   if text.startswith('مراهنه'):
       print(f"[DEBUG] Detected 'مراهنه' command with text: {text}")
       result = await handle_bet(c, m, k, text)
       if result is not None:
           return result

   if text.startswith('انا ') and len(text.split()) == 2:
      try:
         int(text.split()[1])
         return await handle_bet_join(c, m, k, text)
      except:
         pass

   if text in ['بدء المراهنه', 'بدا المراهنه']:
      result = await handle_bet_end(c, m, k, text)
      if result is not None:
         return result

   if text == 'ميدالياتي' or text == 'ميداليات':
     return await handle_medals(c, m, k, text)

   if text.startswith('تبرع '):
     return await handle_donate(c, m, k, text)

   if text == 'تبرعاتي':
     return await handle_my_donations(c, m, k, text)

   if text == 'توب المتبرعين' or text == 'توب التبرعات':
       all_users = await r.smembers('BankList')
       donated_list = []
       
       for uid in all_users:
           uid_str = uid.decode() if isinstance(uid, bytes) else uid
           donated_raw = await r.get(f'{uid_str}:donated')
           if donated_raw:
               donated_list.append((int(donated_raw), uid_str))
             
       donated_list.sort(reverse=True)
       
       top_text = "<b>توب المتبرعين</b>\n\n"
       emojis = ["🥇", "🥈", "🥉"]
       
       for i, (donated, uid) in enumerate(donated_list[:10]):
           name_raw = await r.get(f'{uid}:bankName')
           if name_raw:
               name = name_raw.decode() if isinstance(name_raw, bytes) else name_raw
           else:
               name = f"مستخدم {uid}"
             
           emo = emojis[i] if i < 3 else f"{i+1})"
           top_text += f"{emo} {donated:,}💰 l {name[:15]}\n"

       my_donated_raw = await r.get(f'{m.from_user.id}:donated')
       my_donated = int(my_donated_raw) if my_donated_raw else 0
       my_rank = next((i + 1 for i, (_, uid) in enumerate(donated_list) if uid == str(m.from_user.id)), 1)
       
       top_text += f"\n\n━━━━━━━━━\n• مركزك ↤︎ {my_rank} \n• تبرعت ↤︎ {my_donated:,} ﷼"
       await m.reply(top_text)


   if text == 'توب الحراميه' or text == 'توب الحرامية' or text == 'توب الزرف':
       all_users = await r.smembers('BankList')
       stolen_list = []
       
       for uid in all_users:
           uid_str = uid.decode() if isinstance(uid, bytes) else uid
           stolen_raw = await r.get(f'{uid_str}:Zrf')
           if stolen_raw:
               stolen_list.append((int(stolen_raw), uid_str))
             
       stolen_list.sort(reverse=True)
       
       top_text = "<b>توب الحرامية</b>\n\n"
       emojis = ["🥇", "🥈", "🥉"]
       
       for i, (stolen, uid) in enumerate(stolen_list[:10]):
           name_raw = await r.get(f'{uid}:bankName')
           if name_raw:
               name = name_raw.decode() if isinstance(name_raw, bytes) else name_raw
           else:
               name = f"مستخدم {uid}"
             
           emo = emojis[i] if i < 3 else f"{i+1})"
           top_text += f"{emo} {stolen:,}💰 l {name[:15]}\n"

       my_stolen_raw = await r.get(f'{m.from_user.id}:Zrf')
       my_stolen = int(my_stolen_raw) if my_stolen_raw else 0
       my_rank = next((i + 1 for i, (_, uid) in enumerate(stolen_list) if uid == str(m.from_user.id)), 1)
       
       top_text += f"\n\n━━━━━━━━━\n• مركزك ↤︎ {my_rank} \n• سرقت ↤︎ {my_stolen:,} ﷼"
       await m.reply(top_text)


   if text == 'توب الفلوس':
       all_users = await r.smembers('BankList')
       balance_list = []
       
       for uid in all_users:
           uid_str = uid.decode() if isinstance(uid, bytes) else uid
           bal_raw = await r.get(f'{uid_str}:Floos')
           if bal_raw:
               balance_list.append((int(bal_raw), uid_str))
             
       balance_list.sort(reverse=True)
       
       top_text = "<b>توب الفلوس</b>\n\n"
       emojis = ["🥇", "🥈", "🥉"]
       
       for i, (bal, uid) in enumerate(balance_list[:10]):
           name_raw = await r.get(f'{uid}:bankName')
           if name_raw:
               name = name_raw.decode() if isinstance(name_raw, bytes) else name_raw
           else:
               name = f"مستخدم {uid}"
             
           emo = emojis[i] if i < 3 else f"{i+1})"
           top_text += f"{emo} {bal:,}💰 l {name[:15]}\n"

       my_bal_raw = await r.get(f'{m.from_user.id}:Floos')
       my_bal = int(my_bal_raw) if my_bal_raw else 0
       my_rank = next((i + 1 for i, (_, uid) in enumerate(balance_list) if uid == str(m.from_user.id)), 1)
       
       top_text += f"\n\n━━━━━━━━━\n• مركزك ↤︎ {my_rank} \n• فلوسك ↤︎ {my_bal:,} ﷼"
       await m.reply(top_text)



   if await br.get(f'{m.from_user.id}:toTrans:{m.chat.id}{Dev_FINAL}'):
      if not re.findall('[0-9]+', text):
        await br.delete(f'{m.from_user.id}:toTrans:{m.chat.id}{Dev_FINAL}')
        return await m.reply(plugins_games_bank_1267(k))
      acc_id = int(re.findall('[0-9]+', text)[0])
      acc_id_from = safe_int((await r.get(f'{m.from_user.id}:bankID')) or 0)
      if acc_id == acc_id_from:
        await br.delete(f'{m.from_user.id}:toTrans:{m.chat.id}{Dev_FINAL}')
        return await m.reply(plugins_games_bank_1272(k))
      floos_to_trans = int((await br.get(f'{m.from_user.id}:toTrans:{m.chat.id}{Dev_FINAL}')) or 0)
      await br.delete(f'{m.from_user.id}:toTrans:{m.chat.id}{Dev_FINAL}')
      if not await r.sismember('BankList', m.from_user.id):
        return await m.reply(plugins_games_bank_1276(k))
      if not await r.get(f'{m.from_user.id}:Floos'):
        floos = 0
      else:
        floos = int((await r.get(f'{m.from_user.id}:Floos')) or 0)
      if floos_to_trans > floos:
        return await m.reply(plugins_games_bank_1282(k))
      else:
        if not await r.get(f'{acc_id}:getAccBank'):
          return await m.reply(plugins_games_bank_1285(k))
        else:
          id_to = int((await r.get(f'{acc_id}:getAccBank')) or 0)
          if not await r.sismember('BankList', id_to):
            return await m.reply(plugins_games_bank_1289(k))
          bank_name_raw = await r.get(f'{id_to}:bankName')
          if bank_name_raw:
            name_to = bank_name_raw[:10] if len(bank_name_raw) > 10 else bank_name_raw
          else:
            gett = await c.get_users(int((await r.get(f'{acc_id}:getAccBank')) or 0))
            name_to = gett.first_name[:10] if len(gett.first_name) > 10 else gett.first_name
            await r.set(f'{id_to}:bankName', name_to)
          if floos_to_trans == floos:
            await r.delete(f'{m.from_user.id}:Floos')
          else:
            await r.set(f'{m.from_user.id}:Floos', floos - floos_to_trans)
            await enforce_balance_cap(r, m, k, m.from_user.id)
          bank_to = await r.get(f'{id_to}:bankType')
          bank_from = await r.get(f'{m.from_user.id}:bankType')
          name_from_raw = await r.get(f'{m.from_user.id}:bankName')
          if name_from_raw:
            name_from = name_from_raw[:10] if len(name_from_raw) > 10 else name_from_raw
          else:
            name_from = m.from_user.first_name[:10] if len(m.from_user.first_name) > 10 else m.from_user.first_name
          mention_from = f'<a href="tg://user?id={m.from_user.id}">{html.escape(str(name_from))}</a>'
          mention_to = f'<a href="tg://user?id={id_to}">{html.escape(str(name_to))}</a>'
          if not await r.get(f'{id_to}:Floos'):
            floos_to = 0
          else:
            floos_to = int((await r.get(f'{id_to}:Floos')) or 0)
          txt = 'حوالة صادرة\n\nمن: {}\nحساب رقم: {}\nبنك: {}\nالى: {}\nحساب رقم: {}\nبنك: {}'.format(mention_from, acc_id_from, bank_from, mention_to, acc_id, bank_to)
          if bank_from != bank_to:
             floos_to_tran = int(floos_to_trans - floos_to_trans / 10)
             txt += '\nخصمت 10% ضريبة بنك الى بنك'
             txt += f'\nالمبلغ: {floos_to_tran} ﷼ 💸'
          else:
             floos_to_tran = floos_to_trans
             txt += f'\nالمبلغ: {floos_to_tran} ﷼ 💸'
          await r.set(f'{id_to}:Floos', floos_to + floos_to_tran)
          await enforce_balance_cap(r, m, k, id_to)
          return await m.reply(txt, disable_web_page_preview=True)

   if await r.get(f'{m.from_user.id}:createBank:{m.chat.id}'):
     await r.delete(f'{m.from_user.id}:createBank:{m.chat.id}')
     if await r.get(f'{m.from_user.id}:bankID'):
       id = int((await r.get(f'{m.from_user.id}:bankID')) or 0)
       floos_to_add = 0
     else:
       id = '4'
       floos_to_add = 2000
       for a in range(15):
         id += str(random.randint(1,9))
     if not await r.get(f'{m.from_user.id}:Floos'):
       floos = 0
     else:
       floos = int((await r.get(f'{m.from_user.id}:Floos')) or 0)

     if not text in ['الاهلي','الراجحي', 'الانماء']:
       return await m.reply(plugins_games_bank_1343(k))
     card = random.choice(['الاهلي كارد','الراجحي كارد','الإنماء كارد','مدى كارد'])
     if text == 'الاهلي':
        await r.set(f'{m.from_user.id}:bankType', 'الاهلي')
        await r.set(f'{m.from_user.id}:bankID', int(id))
        await r.set(f'{m.from_user.id}:bankCard',card)
     if text == 'الراجحي':
        await r.set(f'{m.from_user.id}:bankType', 'الراجحي')
        await r.set(f'{m.from_user.id}:bankID', int(id))
        await r.set(f'{m.from_user.id}:bankCard',card)
     if text == 'الانماء':
        await r.set(f'{m.from_user.id}:bankType', 'الانماء')
        await r.set(f'{m.from_user.id}:bankID', int(id))
        await r.set(f'{m.from_user.id}:bankCard',card)

     await r.sadd('BankList', m.from_user.id)
     await r.set(f'{id}:getAccBank', m.from_user.id)
     fff = floos + floos_to_add
     await r.set(f'{m.from_user.id}:Floos',fff)
     await enforce_balance_cap(r, m, k, m.from_user.id)
     await r.set(f'{m.from_user.id}:bankName', m.from_user.first_name)
     await r.set(f'{m.from_user.id}:rank_index', 1)
     await r.set(f'{m.from_user.id}:rank', 0)
     await m.reply(plugins_games_bank_1366(k, text, k, id, k, card, k, fff))
     if await br.get(f'DevGroup:{Dev_FINAL}'):
         await c.send_message(int((await br.get(f'DevGroup:{Dev_FINAL}')) or 0),
           f' ⟨ {m.from_user.mention()} ⟩\n{k} سوى حساب بالبنك\n{k} رقم حسابه ( <code>{id}</code> )')
     return

   if text == 'توب' or text == 'التوب':
     return await get_top_interactive(c, m, k, channel)

   if text == 'حسابي':
     if not await r.sismember('BankList', m.from_user.id):
       return await m.reply(plugins_games_bank_1377(k))
     else:
       card = await r.get(f'{m.from_user.id}:bankCard')
       bank = await r.get(f'{m.from_user.id}:bankType')
       id_raw = await r.get(f'{m.from_user.id}:bankID')
       if id_raw is None or not bank or not card:
         bank = bank or 'الاهلي'
         new_id = '4'
         for _a in range(15):
           new_id += str(random.randint(1, 9))
         card = card or random.choice(['الاهلي كارد', 'الراجحي كارد', 'الإنماء كارد', 'مدى كارد'])
         await r.set(f'{m.from_user.id}:bankType', bank)
         await r.set(f'{m.from_user.id}:bankID', int(new_id))
         await r.set(f'{m.from_user.id}:bankCard', card)
         await r.set(f'{new_id}:getAccBank', m.from_user.id)
         id = int(new_id)
       else:
         id = safe_int(id_raw)
       rank_index = int(await r.get(f'{m.from_user.id}:rank_index') or 1)
       current_rank = get_current_rank(rank_index)
       rank_name = current_rank['name'] if current_rank else "سواق"
       if not await r.get(f'{m.from_user.id}:Floos'):
         floos = 0
       else:
         floos = int((await r.get(f'{m.from_user.id}:Floos')) or 0)
       name_raw = await r.get(f'{m.from_user.id}:bankName')
       if name_raw:
         name = name_raw.replace("*","").replace("`","").replace("|","").replace("#","").replace("<","").replace(">","").replace("_","")
       else:
         name = m.from_user.first_name.replace("*","").replace("`","").replace("|","").replace("#","").replace("<","").replace(">","").replace("_","")
       stolen = int(await r.get(f'{m.from_user.id}:Zrf') or 0)
       donated = int(await r.get(f'{m.from_user.id}:donated') or 0)
       await m.reply(plugins_games_bank_1409(k, name, k, id, k, bank, k, card, k, floos, k, rank_name, k, stolen, k, donated))

   if text == 'مسح حسابي' or text == 'حذف حسابي':
       if not await r.sismember('BankList', m.from_user.id):
           return await m.reply(plugins_games_bank_1421(k))
       else:
           await r.srem('BankList', m.from_user.id)
           await m.reply(plugins_games_bank_1424(k))

   if text.startswith('حساب ') and len(text.split()) == 2 and re.findall('[0-9]+', text):
      acc_id = int(re.findall('[0-9]+', text)[0])
      if await r.get(f'{acc_id}:getAccBank'):
         id = int((await r.get(f'{acc_id}:getAccBank')) or 0)
         name_raw = await r.get(f'{id}:bankName')
         if name_raw:
           name = name_raw[:10] if len(name_raw) > 10 else name_raw
         else:
           gett = await c.get_users(int((await r.get(f'{acc_id}:getAccBank')) or 0))
           name = gett.first_name[:10] if len(gett.first_name) > 10 else gett.first_name
           await r.set(f'{id}:bankName', name)
         bank = await r.get(f'{id}:bankType')
         card = await r.get(f'{id}:bankCard')
         if not await r.get(f'{id}:Floos'):
           floos = 0
         else:
           floos = int((await r.get(f'{id}:Floos')) or 0)
         stolen = int(await r.get(f'{id}:Zrf') or 0)
         await m.reply(plugins_games_bank_1444(k, name.replace("*","").replace("`","").replace("|","").replace("#","").replace("<","").replace(">","").replace("_",""), k, acc_id, k, bank, k, card, k, floos, k, stolen))

   if text.startswith('تحويل ') and len(text.split()) == 2 and re.findall('[0-9]+', text):
      floos_to_trans = int(re.findall('[0-9]+', text)[0])
      if not await r.get(f'{m.from_user.id}:Floos'):
        floos = 0
      else:
        floos = int((await r.get(f'{m.from_user.id}:Floos')) or 0)
      if floos_to_trans < 200:
        return await m.reply(plugins_games_bank_1460(k))
      else:
        if floos_to_trans > floos:
          return await m.reply(plugins_games_bank_1463(k))
        if not await r.sismember('BankList', m.from_user.id):
          return await m.reply(plugins_games_bank_1465(k))
        else:
          await br.set(f'{m.from_user.id}:toTrans:{m.chat.id}{Dev_FINAL}', floos_to_trans, ex=600)
          return await m.reply(plugins_games_bank_1468(k))

   if text.startswith('حظ ') and len(text.split()) == 2 and re.findall('[0-9]+', text):
       if not await r.sismember('BankList', m.from_user.id):
           return await m.reply(plugins_games_bank_1472(k))
       
       if await r.get(f'{m.from_user.id}:BankWaitHZ'):
           get = await r.ttl(f'{m.from_user.id}:BankWaitHZ')
           wait = time.strftime('%M:%S', time.gmtime(get))
           return await m.reply(plugins_games_bank_1477(k, k, wait))
       else:
           if not await r.get(f'{m.from_user.id}:Floos'):
               floos = 0
           else:
               floos = int((await r.get(f'{m.from_user.id}:Floos')) or 0)
           floos_to_hz = int(re.findall('[0-9]+', text)[0])
           if floos_to_hz == 0:
               return await m.reply(plugins_games_bank_1485(k))
           if floos_to_hz > floos:
               return await m.reply(plugins_games_bank_1487(k))
           else:
               await r.setex(f'{m.from_user.id}:BankWaitHZ', 1200, 1)
               hzz = random.choice(['yes','no'])
               if hzz == 'yes':
                   fls = floos_to_hz
                   multiplier = 1
                   double_key = f'{m.from_user.id}:wheel_double'
                   if await r.get(double_key):
                       multiplier = 2
                   fls *= multiplier
                   floos_com = floos+fls
                   await r.set(f'{m.from_user.id}:Floos', floos+fls)
                   await enforce_balance_cap(r, m, k, m.from_user.id)
                   await add_game_earnings(m.from_user.id, m.chat.id, fls, m.id)
                   return await m.reply(plugins_games_bank_1502(k, k, floos, k, floos_com))
               else:
                   fls = floos-floos_to_hz
                   if fls == 0:
                       await r.delete(f'{m.from_user.id}:Floos')
                   else:
                       await r.set(f'{m.from_user.id}:Floos', fls)
                       await enforce_balance_cap(r, m, k, m.from_user.id)
                   return await m.reply(plugins_games_bank_1510(k, k, floos, k, fls))


   if text == "حظ فلوسي":
       if not await r.sismember('BankList', m.from_user.id):
           return await m.reply(plugins_games_bank_1515(k))
       
       if await r.get(f'{m.from_user.id}:BankWaitHZ'):
           get = await r.ttl(f'{m.from_user.id}:BankWaitHZ')
           wait = time.strftime('%M:%S', time.gmtime(get))
           return await m.reply(plugins_games_bank_1520(k, k, wait))
       else:
           if not await r.get(f'{m.from_user.id}:Floos'):
               floos = 0
           else:
               floos = int((await r.get(f'{m.from_user.id}:Floos')) or 0)
           floos_to_hz = floos
           if floos_to_hz == 0:
               return await m.reply(plugins_games_bank_1528(k))
           else:
               await r.setex(f'{m.from_user.id}:BankWaitHZ', 1200, 1)
               hzz = random.choice(['yes','no'])
               if hzz == 'yes':
                   fls = floos_to_hz
                   multiplier = 1
                   double_key = f'{m.from_user.id}:wheel_double'
                   if await r.get(double_key):
                       multiplier = 2
                   fls *= multiplier
                   floos_com = floos+fls
                   await r.set(f'{m.from_user.id}:Floos', floos+fls)
                   await enforce_balance_cap(r, m, k, m.from_user.id)
                   await add_game_earnings(m.from_user.id, m.chat.id, fls, m.id)
                   return await m.reply(plugins_games_bank_1543(k, k, floos, k, floos_com))
               else:
                   fls = floos-floos_to_hz
                   if fls == 0:
                       await r.delete(f'{m.from_user.id}:Floos')
                   else:
                       await r.set(f'{m.from_user.id}:Floos', fls)
                       await enforce_balance_cap(r, m, k, m.from_user.id)
                   return await m.reply(plugins_games_bank_1551(k, k, floos, k, fls))

   if text == 'عجله' or text == 'عجلة':
       if not await r.sismember('BankList', m.from_user.id):
           return await m.reply(plugins_games_bank_1555(k))
       
       user_balance = int(await r.get(f'{m.from_user.id}:Floos') or 0)
       if user_balance < 5000000:
           return await m.reply(plugins_games_bank_1559(k))
       
       if await r.get(f'{m.from_user.id}:BankWaitWheel'):
           get = await r.ttl(f'{m.from_user.id}:BankWaitWheel')
           wait = time.strftime('%M:%S', time.gmtime(get))
           return await m.reply(plugins_games_bank_1564(k, k, wait))
       
       await r.setex(f'{m.from_user.id}:BankWaitWheel', 300, 1)
       
       await r.setex(f'{m.from_user.id}:wheel_state', 120, 'waiting_confirm')
       
       photo_url = "https://graph.org/file/f35a758520fcd6afdb4a0-15f933974732ee2c94.jpg"
       caption = f"{k} عجلة الحظ\n{k} سيتم خصم 5 ملايين ﷼ من رصيدك"
       keyboard = InlineKeyboardMarkup([
           [
               InlineKeyboardButton("الغاء", callback_data=f"wheel_cancel:{m.from_user.id}"),
               InlineKeyboardButton("تاكيد", callback_data=f"wheel_confirm:{m.from_user.id}")
           ]
       ])
       try:
           await m.reply_photo(photo=photo_url, caption=caption, reply_markup=keyboard)
       except Exception as e:
           print(f"Error sending wheel photo: {e}")
           await r.delete(f'{m.from_user.id}:BankWaitWheel')
           await r.delete(f'{m.from_user.id}:wheel_state')
           return await m.reply(plugins_games_bank_1584(k))
       return



   if text == 'استثمار ' and len(text.split()) == 2 and re.findall('[0-9]+', text):
     if not await r.sismember('BankList', m.from_user.id):
       return await m.reply(plugins_games_bank_1591(k))
     if await r.get(f'{m.from_user.id}:BankWaitEST'):
       get = await r.ttl(f'{m.from_user.id}:BankWaitEST')
       wait = time.strftime('%M:%S', time.gmtime(get))
       return await m.reply(plugins_games_bank_1595(k, k, wait))
     else:
       if not await r.get(f'{m.from_user.id}:Floos'):
         floos = 0
       else:
         floos = int((await r.get(f'{m.from_user.id}:Floos')) or 0)
       floos_to_est = int(re.findall('[0-9]+', text)[0])
       if floos_to_est == 0:
         return await m.reply(plugins_games_bank_1603(k))
       if floos_to_est > floos:
         return await m.reply(plugins_games_bank_1605(k))
       if floos_to_est < 2000:
         return await m.reply(plugins_games_bank_1607(k))
       else:
         await r.setex(f'{m.from_user.id}:BankWaitEST', 1200, 1)
         one = int(floos_to_est/random.randint(1,9))
         multiplier = 1
         double_key = f'{m.from_user.id}:wheel_double'
         if await r.get(double_key):
             multiplier = 2
         one *= multiplier
         rb7 = int(is_what_percent_of(one,floos_to_est))
         await r.set(f'{m.from_user.id}:Floos',floos+one)
         await enforce_balance_cap(r, m, k, m.from_user.id)
         await add_game_earnings(m.from_user.id, m.chat.id, one, m.id)
         await m.reply(plugins_games_bank_1620(k, k, rb7, k, one, k, floos+one))

   if text == "استثمار فلوسي":
     if not await r.sismember('BankList', m.from_user.id):
       return await m.reply(plugins_games_bank_1629(k))
     if await r.get(f'{m.from_user.id}:BankWaitEST'):
       get = await r.ttl(f'{m.from_user.id}:BankWaitEST')
       wait = time.strftime('%M:%S', time.gmtime(get))
       return await m.reply(plugins_games_bank_1633(k, k, wait))
     else:
       if not await r.get(f'{m.from_user.id}:Floos'):
         floos = 0
       else:
         floos = int((await r.get(f'{m.from_user.id}:Floos')) or 0)
       floos_to_est = floos
       if floos_to_est == 0:
         return await m.reply(plugins_games_bank_1641(k))
       if floos_to_est < 2000:
         return await m.reply(plugins_games_bank_1643(k))
       else:
         await r.setex(f'{m.from_user.id}:BankWaitEST', 1200, 1)
         one = int(floos_to_est/random.randint(1,9))
         multiplier = 1
         double_key = f'{m.from_user.id}:wheel_double'
         if await r.get(double_key):
             multiplier = 2
         one *= multiplier
         rb7 = int(is_what_percent_of(one,floos_to_est))
         await r.set(f'{m.from_user.id}:Floos',floos+one)
         await enforce_balance_cap(r, m, k, m.from_user.id)
         await add_game_earnings(m.from_user.id, m.chat.id, one, m.id)
         await m.reply(plugins_games_bank_1656(k, k, rb7, k, one, k, floos+one))

   if text == 'كنز':
     if not await r.sismember('BankList', m.from_user.id):
       return await m.reply(plugins_games_bank_1665(k))
     if await r.get(f'{m.from_user.id}:BankWaitKNZ'):
       get = await r.ttl(f'{m.from_user.id}:BankWaitKNZ')
       wait = time.strftime('%M:%S', time.gmtime(get))
       return await m.reply(plugins_games_bank_1669(k, wait))
     else:
       if not await r.get(f'{m.from_user.id}:Floos'):
          floos = 0
       else:
          floos = int((await r.get(f'{m.from_user.id}:Floos')) or 0)
       knz = random.choice(TREASURES)
       money = knz['credit']
       name = knz['name']
       await r.setex(f'{m.from_user.id}:BankWaitKNZ', 600, 1)
       multiplier = 1
       double_key = f'{m.from_user.id}:wheel_double'
       if await r.get(double_key):
           multiplier = 2
       money *= multiplier
       await r.set(f'{m.from_user.id}:Floos', floos+money)
       await enforce_balance_cap(r, m, k, m.from_user.id)
       await add_game_earnings(m.from_user.id, m.chat.id, money, m.id)
       fls = floos+money
       return await m.reply(plugins_games_bank_1688(k, m.from_user.mention(m.from_user.first_name[:10]), k, money, k, name, k, k, fls))

   if text == 'بخشيش':
     if not await r.sismember('BankList', m.from_user.id):
       return await m.reply(plugins_games_bank_1692(k))
     if await r.get(f'{m.from_user.id}:BankWaitB5'):
       get = await r.ttl(f'{m.from_user.id}:BankWaitB5')
       wait = time.strftime('%M:%S', time.gmtime(get))
       return await m.reply(plugins_games_bank_1696(k, k, wait))
     else:
       b5 = random.randint(200, 4000)
       await r.setex(f'{m.from_user.id}:BankWaitB5', 300, 1)
       if not await r.get(f'{m.from_user.id}:Floos'):
          floos = 0
       else:
          floos = int((await r.get(f'{m.from_user.id}:Floos')) or 0)
       multiplier = 1
       double_key = f'{m.from_user.id}:wheel_double'
       if await r.get(double_key):
           multiplier = 2
       b5 *= multiplier
       await r.set(f'{m.from_user.id}:Floos', floos+b5)
       await enforce_balance_cap(r, m, k, m.from_user.id)
       await add_game_earnings(m.from_user.id, m.chat.id, b5, m.id)
       await m.reply(plugins_games_bank_1712(k, b5))

   if text == 'راتب':
     if not await r.sismember('BankList', m.from_user.id):
       return await m.reply(plugins_games_bank_1716(k))
     if await r.get(f'{m.from_user.id}:BankWaitSalary'):
       get = await r.ttl(f'{m.from_user.id}:BankWaitSalary')
       wait = time.strftime('%M:%S', time.gmtime(get))
       return await m.reply(plugins_games_bank_1720(k, wait))
     else:
       rank_index = int(await r.get(f'{m.from_user.id}:rank_index') or 1)
       current_rank = get_current_rank(rank_index)
       if not current_rank:
         money = random.randint(2000, 16000)
         name = "سواق"
       else:
         money = random.randint(2000, 16000)
         name = current_rank['name']
       await r.setex(f'{m.from_user.id}:BankWaitSalary', 300, 1)
       if not await r.get(f'{m.from_user.id}:Floos'):
          floos = 0
       else:
          floos = int((await r.get(f'{m.from_user.id}:Floos')) or 0)
       multiplier = 1
       double_key = f'{m.from_user.id}:wheel_double'
       if await r.get(double_key):
           multiplier = 2
       money *= multiplier
       await r.set(f'{m.from_user.id}:Floos', floos+money)
       await enforce_balance_cap(r, m, k, m.from_user.id)
       await add_game_earnings(m.from_user.id, m.chat.id, money, m.id)
       fls = floos+money
       await m.reply(plugins_games_bank_1744(k, m.from_user.mention(m.from_user.first_name[:10]), k, money, k, name, k, k, fls))

   if text == 'زرف' and m.reply_to_message and m.reply_to_message.from_user:
       if m.reply_to_message.from_user.id == int(Dev_FINAL):
           return await m.reply(REPLIES['plugins_games_bank_1748'])
       if not await r.sismember('BankList', m.from_user.id):
           return await m.reply(plugins_games_bank_1750(k))
       if await br.get(f'jail_{m.from_user.id}'):
           ttl = await br.ttl(f'jail_{m.from_user.id}')
           wait = time.strftime('%M:%S', time.gmtime(ttl))
           return await m.reply(plugins_games_bank_1754(k, k, wait))
       if not await r.sismember('BankList', m.reply_to_message.from_user.id):
           return await m.reply(plugins_games_bank_1756(k))
       if m.reply_to_message.from_user.id == m.from_user.id:
           return await m.reply(REPLIES['plugins_games_bank_1758'])
       
       if await r.get(f'{m.from_user.id}:BankWaitZRF'):
           get = await r.ttl(f'{m.from_user.id}:BankWaitZRF')
           wait = time.strftime('%M:%S', time.gmtime(get))
           return await m.reply(plugins_games_bank_1763(k, k, wait))
       
       if await r.get(f'{m.reply_to_message.from_user.id}:BankWaitMZROF'):
           get = await r.ttl(f'{m.reply_to_message.from_user.id}:BankWaitMZROF')
           wait = time.strftime('%M:%S', time.gmtime(get))
           return await m.reply(plugins_games_bank_1768(k, k, wait))
       
       if not await r.get(f'{m.reply_to_message.from_user.id}:Floos'):
           return await m.reply(plugins_games_bank_1771(k))
       if int((await r.get(f'{m.reply_to_message.from_user.id}:Floos')) or 0) < 2000:
           return await m.reply(plugins_games_bank_1773(k))
       else:
           await r.setex(f'{m.from_user.id}:BankWaitZRF', 600, 1)
           await r.setex(f'{m.reply_to_message.from_user.id}:BankWaitMZROF', 600, 1)
           zrf = random.randint(50, 1000)
           floos = int((await r.get(f'{m.reply_to_message.from_user.id}:Floos')) or 0)
           await r.set(f'{m.reply_to_message.from_user.id}:Floos', floos - zrf)
           await enforce_balance_cap(r, m, k, m.reply_to_message.from_user.id)
           await m.reply(plugins_games_bank_1781(k, zrf))
           if not await r.get(f'{m.from_user.id}:Floos'):
               floos_from_user = 0
           else:
               floos_from_user = int((await r.get(f'{m.from_user.id}:Floos')) or 0)
           multiplier = 1
           double_key = f'{m.from_user.id}:wheel_double'
           if await r.get(double_key):
               multiplier = 2
           zrf_add = zrf * multiplier
           await r.set(f'{m.from_user.id}:Floos', floos_from_user + zrf_add)
           await enforce_balance_cap(r, m, k, m.from_user.id)
           await r.sadd('BankZrf', m.from_user.id)
           zrff_before = int(await r.get(f'{m.from_user.id}:Zrf') or 0)
           await r.set(f'{m.from_user.id}:Zrf', zrff_before + zrf_add)
           try:
               await c.send_message(
                   m.reply_to_message.from_user.id,
                   f'{k} الحق الحق حلالك!!\n{k} ذا الحرامي {m.from_user.mention()}\n{k} سرق منك ( {zrf} ﷼ 💸 )',
                   reply_markup=InlineKeyboardMarkup(
                       [[
                           InlineKeyboardButton(m.chat.title, url=m.link)
                       ]]
                   )
               )
           except:
               pass


   if text == 'ddddxxxx' or text == 'ddddvvvvv':
       if await devp_pls(m.from_user.id, m.chat.id):
           keys_to_delete = [
               f'{m.from_user.id}:BankWaitB5',
               f'{m.from_user.id}:BankWaitEST',
               f'{m.from_user.id}:BankWaitHZ',
               f'{m.from_user.id}:BankWaitKNZ',
               f'{m.from_user.id}:BankWaitZRF',
               f'{m.from_user.id}:BankWaitMDRB',
               f'{m.from_user.id}:BankWaitDONATE',
               f'{m.from_user.id}:BankWaitSalary',
               f'{m.from_user.id}:BankWaitWheel',
           ]
           deleted = 0
           for key in keys_to_delete:
               if await r.get(key):
                   await r.delete(key)
                   deleted += 1
           await m.reply(plugins_games_bank_1828(k, deleted))

   if text == 'تصفير البنك':
     if is_owner_only(m.from_user.id):
        yes_btn = await create_button_raw("bank", "confirm_reset", "اي", callback_data='yes:del:bank')
        no_btn = await create_button_raw("bank", "cancel_reset", "لا", callback_data='no:del:bank')
        return await m.reply(plugins_games_bank_1834(k),reply_markup=InlineKeyboardMarkup ([[InlineKeyboardButton(**yes_btn)],[InlineKeyboardButton(**no_btn)]]))
     else:
        return await m.reply(plugins_games_bank_1836(k))

   if text == 'فلوسي':
     if not await r.get(f'{m.from_user.id}:Floos'):
        await m.reply(plugins_games_bank_1840(k))
     else:
        floos = int((await r.get(f'{m.from_user.id}:Floos')) or 0)
        return await m.reply(plugins_games_bank_1843(k, floos))

   if text == 'فلوس':
     if not m.reply_to_message:
       if not await r.get(f'{m.from_user.id}:Floos'):
         return await m.reply(plugins_games_bank_1848(k))
       else:
         floos = int((await r.get(f'{m.from_user.id}:Floos')) or 0)
       return await m.reply(plugins_games_bank_1851(k, floos))
     else:
       if not await r.get(f'{m.reply_to_message.from_user.id}:Floos'):
         floos = 0
       else:
         floos = int((await r.get(f'{m.reply_to_message.from_user.id}:Floos')) or 0)
       return await m.reply(plugins_games_bank_1857(k, floos))

   if text.startswith('بيع فلوسي ') and len(text.split()) == 3 and re.findall('[0-9]+', text):
     if not await r.get(f'{m.from_user.id}:Floos'):
        await m.reply(plugins_games_bank_1861(k))
     else:
        floos_to_sale = int(re.findall('[0-9]+', text)[0])
        floos = int((await r.get(f'{m.from_user.id}:Floos')) or 0)
        if floos_to_sale == 0:
         return await m.reply(plugins_games_bank_1866(k))
        if floos_to_sale > floos:
          return await m.reply(plugins_games_bank_1868(k, floos))
        if floos_to_sale == floos:
           await r.delete(f'{m.from_user.id}:Floos')
        else:
           await r.set(f'{m.from_user.id}:Floos',floos-floos_to_sale)
           await enforce_balance_cap(r, m, k, m.from_user.id)
        get = int((await br.get(f'{m.chat.id}:TotalMsgs:{m.from_user.id}{Dev_FINAL}')) or 0)
        rsayl = floos_to_sale * 20
        await br.set(f'{m.chat.id}:TotalMsgs:{m.from_user.id}{Dev_FINAL}', get+rsayl)
        await m.reply(plugins_games_bank_1877(k, floos_to_sale, k, get + rsayl))

   if text.startswith('اضف فلوس ') and len(text.split()) == 3 and re.findall('[0-9]+', text):
     if not is_owner_only(m.from_user.id):
        return await m.reply(plugins_games_bank_1881(k))
     if m.reply_to_message and m.reply_to_message.from_user:
          floos_to_add = int(re.findall('[0-9]+', text)[0])
          if not await r.get(f'{m.reply_to_message.from_user.id}:Floos'):
             await r.set(f'{m.reply_to_message.from_user.id}:Floos',floos_to_add)
             await enforce_balance_cap(r, m, k, m.reply_to_message.from_user.id)
          else:
             floos = int((await r.get(f'{m.reply_to_message.from_user.id}:Floos')) or 0)
             await r.set(f'{m.reply_to_message.from_user.id}:Floos',floos_to_add+floos)
             await enforce_balance_cap(r, m, k, m.reply_to_message.from_user.id)
          await m.reply(plugins_games_bank_1891(m.reply_to_message.from_user.mention(), k, floos_to_add))

   if text == 'استخراج الاكواد':
      if await devp_pls(m.from_user.id,m.chat.id):
         if await br.get(f'{Dev_FINAL}:codeWait'):
           t = await br.ttl(f'{Dev_FINAL}:codeWait')
           wait = time.strftime('%H:%M:%S', time.gmtime(t))
           return await m.reply(plugins_games_bank_1898(k, wait))
         else:
           txt = 'اكواد الكشط:\n'
           ccc = 1
           for none in range(10):
             code = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(10)])
             await br.set(f'{code}:CodeBank:{Dev_FINAL}',1,ex=7200)
             txt += f'{ccc} ) <code>{code}</code>\n'
             ccc += 1
           await br.set(f'{Dev_FINAL}:codeWait',1,ex=7200)
           txt += '\n~ الأكواد صالحة لساعتين فقط .'
           txt += '\n༄'
           return await m.reply(txt)

   if text.startswith('كشط ') and len(text.split()) == 2:
     code = text.split()[1]
     if not await br.get(f'{code}:CodeBank:{Dev_FINAL}'):
       return await m.reply(plugins_games_bank_1915(k))
     if await br.get(f'{m.from_user.id}:BankWaitKSHT:{Dev_FINAL}'):
       t = await br.ttl(f'{m.from_user.id}:BankWaitKSHT:{Dev_FINAL}')
       wait = time.strftime('%H:%M:%S', time.gmtime(t))
       return await m.reply(plugins_games_bank_1919(k, wait))
     else:
       await br.delete(f'{code}:CodeBank:{Dev_FINAL}')
     if not await r.get(f'{m.from_user.id}:Floos'):
       floos_from_user = 0
     else:
       floos_from_user = int((await r.get(f'{m.from_user.id}:Floos')) or 0)
     chance = random.choice([1000000000, 2000000000, 3000000000])
     await r.set(f'{m.from_user.id}:Floos',floos_from_user+chance)
     await enforce_balance_cap(r, m, k, m.from_user.id)
     await add_game_earnings(m.from_user.id, m.chat.id, chance, m.id)
     await m.reply(plugins_games_bank_1930(k, k, chance, k, floos_from_user, k, floos_from_user+chance))
     await br.set(f'{m.from_user.id}:BankWaitKSHT:{Dev_FINAL}',1,ex=7200)
     if await br.get(f'DevGroup:{Dev_FINAL}'):
       alert = f'𖡋 𝐍𝐀𝐌𝐄 ⌯ {m.from_user.mention()}\n𖡋 𝐈𝐃 ⌯ <code>{m.from_user.id}</code>\n\nكشط الكود <code>{code}</code> وأخذ {chance} ﷼ 💸'
       await c.send_message(int((await br.get(f'DevGroup:{Dev_FINAL}')) or 0),alert)

   if text == 'تصفير الممتلكات':
        if is_owner_only(m.from_user.id):
            yes_btn = await create_button_raw("bank", "confirm_reset_items", "اي", callback_data='confirm_reset_items')
            no_btn = await create_button_raw("bank", "cancel_reset_items", "لا", callback_data='cancel_reset_items')
            return await m.reply(plugins_games_bank_1940(k),
                                 reply_markup=InlineKeyboardMarkup (
                                     [[
                                         InlineKeyboardButton(**yes_btn),
                                         InlineKeyboardButton(**no_btn)
                                     ]]
                                 ))
        else:
            return await m.reply(plugins_games_bank_1948(k))

   if text.startswith('تصفير فلوس ') and len(text.split()) >= 3:
       if not is_owner_only(m.from_user.id):
           return await m.reply(plugins_games_bank_1952(k))
       query = text.split(' ', 2)[2].strip()
       target_id = None
       if query.lstrip('-').isdigit():
           target_id = int(query)
       else:
           all_users = await r.smembers('BankList')
           for uid_raw in all_users:
               uid_str = uid_raw.decode() if isinstance(uid_raw, bytes) else uid_raw
               cached_name = await r.get(f'{uid_str}:bankName')
               if cached_name and query in cached_name:
                   target_id = safe_int(uid_str)
                   break
           if target_id is None:
               for uid_raw in all_users:
                   uid_str = uid_raw.decode() if isinstance(uid_raw, bytes) else uid_raw
                   try:
                       user_obj = await c.get_users(int(uid_str))
                   except Exception:
                       continue
                   if user_obj and user_obj.first_name and query in user_obj.first_name:
                       target_id = safe_int(uid_str)
                       break
       if target_id is None:
           return await m.reply(plugins_games_bank_1976(k))
       deleted = 0
       for key in await r.keys(f'{target_id}:*'):
           key_str = key if isinstance(key, str) else key.decode()
           await r.delete(key_str)
           deleted += 1
       await r.srem('BankList', target_id)
       await r.delete(f'global_reactions:{target_id}')
       for bk in await r.keys('*:getAccBank'):
           bk_str = bk if isinstance(bk, str) else bk.decode()
           val = await r.get(bk_str)
           if val is not None and str(val) == str(target_id):
               await r.delete(bk_str)
               deleted += 1
       return await m.reply(plugins_games_bank_1990(k, target_id))

   if text.startswith('تصفير مجموعة ') and len(text.split()) >= 3:
       if not is_owner_only(m.from_user.id):
           return await m.reply(plugins_games_bank_1994(k))
       query = text.split(' ', 2)[2].strip()
       target_gid = None
       if query.lstrip('-').isdigit():
           target_gid = int(query)
       else:
           for tk in await r.keys('*:chat_title:*'):
               tk_str = tk if isinstance(tk, str) else tk.decode()
               title_val = await r.get(tk_str)
               if title_val and query in title_val:
                   try:
                       target_gid = int(tk_str.split(':chat_title:')[0])
                       break
                   except (ValueError, IndexError):
                       continue
       if target_gid is None:
           return await m.reply(plugins_games_bank_2010(k))
       seen = set()
       deleted = 0
       matched_keys = list(await r.keys(f'{target_gid}:*'))
       matched_keys += list(await r.keys(f'*:{target_gid}'))
       matched_keys += list(await r.keys(f'*:{target_gid}:*'))
       for key in matched_keys:
           key_str = key if isinstance(key, str) else key.decode()
           if key_str in seen:
               continue
           seen.add(key_str)
           await r.delete(key_str)
           deleted += 1
       return await m.reply(plugins_games_bank_2023(k, target_gid, deleted))

   top_settings_result = await handle_top_settings(c, m, k, text)
   if top_settings_result is not None:
       return top_settings_result

   marriage_result = await handle_marriage_commands(c, m, k, text)
   if marriage_result is not None:
       return marriage_result

   word_result = await handle_word_games(c, m, k, text)
   if word_result is not None:
       return word_result

   quiz_result = await handle_quiz_games(c, m, k, text)
   if quiz_result is not None:
       return quiz_result

   math_result = await handle_math_games(c, m, k, text)
   if math_result is not None:
       return math_result

   media_result = await handle_media_games(c, m, k, m.text or '')
   if media_result is not None:
       return media_result

   hazr_result = await handle_hazr_game(c, m, k, m.text or '')
   if hazr_result is not None:
       return hazr_result

   social_result = await handle_social_games(c, m, k, m.text or '')
   if social_result is not None:
       return social_result

   quiz_cmd_result = await handle_quiz_commands(c, m, k, text, c)
   if quiz_cmd_result is not None:
       return quiz_cmd_result

   farm_result = await handle_farm_commands(c, m, k, text)
   if farm_result is not None:
      return farm_result

   clubs_result = await handle_clubs_commands(c, m, k, text)
   if clubs_result is not None:
      return clubs_result

   public_result = await handle_public_games(c, m, k, m.text or '')
   if public_result is not None:
       return public_result

   social_result = await handle_social_gamesx(c, m, k, m.text)
   if social_result is not None:
       return social_result

   return None

async def _perform_full_bank_reset():
    """
    يمسح من القاعدة كل شيء يخص البنك حرفياً لكل المستخدمين بلا استثناء: الفلوس،
    الحسابات البنكية، الهدايا/الممتلكات، الميداليات، الفلوس الحرامية (Zrf)،
    القروض، الاسهم الشخصية، المتاجر الشخصية (ممتلكات + اسعار + حالة القفل/الاخفاء)،
    وأي مفاتيح انتظار (BankWait*) خاصة بأي مستخدم مسجل في BankList. لا يبقى أي أثر
    مرتبط بأي مستخدم بعد التنفيذ.
    """
    deleted = 0
    all_users = await r.smembers('BankList')
    for uid_raw in all_users:
        uid_str = uid_raw.decode() if isinstance(uid_raw, bytes) else uid_raw
        for key in await r.keys(f'{uid_str}:*'):
            key_str = key if isinstance(key, str) else key.decode()
            await r.delete(key_str)
            deleted += 1
        await r.delete(f'global_reactions:{uid_str}')

    for bk in await r.keys('*:getAccBank'):
        bk_str = bk if isinstance(bk, str) else bk.decode()
        await r.delete(bk_str)
        deleted += 1

    await r.delete('BankList')
    await r.delete('pshop_item_owner')
    return deleted


async def _decrement_balance(user_id, amount):
    br = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    balance_str = await r.get(f'{user_id}:Floos')
    if balance_str is None:
        return False
    try:
        balance = int(balance_str)
        new_balance = balance - amount
        await r.set(f'{user_id}:Floos', str(new_balance))
        return True
    except ValueError:
        return False

@Client.on_callback_query(filters.regex(r"^(bank_|yes:del:bank|no:del:bank|bank_page_|bank_dep_|bank_with_|wheel_|shop_|confirm_reset_items|cancel_reset_items)"), group=-4331)
async def bank_callback_handler(client, callback_query):
    br = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    user_id = callback_query.from_user.id
    chat_id = callback_query.message.chat.id
    message_id = callback_query.message.id
    data = callback_query.data
    k = await br.get(f'{Dev_FINAL}:botkey') or '•'

    if data == 'yes:del:bank':
        if not is_owner_only(user_id):
            await callback_query.answer(REPLIES['plugins_games_bank_2131'], show_alert=True)
            return
        await callback_query.answer()
        deleted = await _perform_full_bank_reset()
        try:
            await callback_query.message.delete()
        except Exception:
            pass
        await client.send_message(chat_id, f'{k} تم تصفير البنك بالكامل ✅ ( {deleted} مفتاح محذوف )')
        return

    if data == 'no:del:bank':
        if not is_owner_only(user_id):
            await callback_query.answer(REPLIES['plugins_games_bank_2131'], show_alert=True)
            return
        await callback_query.answer()
        try:
            await callback_query.message.delete()
        except Exception:
            pass
        return

    if data.startswith("wheel_"):
        parts = data.split(":")
        if len(parts) >= 2:
            action = parts[0]
            target_user_id = parts[1] if len(parts) > 1 else None
            if target_user_id and str(user_id) != target_user_id:
                await callback_query.answer(REPLIES['plugins_games_bank_2159'], show_alert=True)
                return

            if action == "wheel_cancel":
                print(f"[wheel_cancel] user={user_id}")
                await callback_query.answer()
                try:
                    await client.delete_messages(chat_id=chat_id, message_ids=message_id)
                    print(f"[wheel_cancel] message deleted successfully")
                except Exception as e:
                    print(f"[wheel_cancel] delete error: {e}")
                await r.delete(f'{user_id}:wheel_state')
                return

            elif action == "wheel_confirm":
                print(f"[wheel_confirm] user={user_id}")
                await callback_query.answer()

                state_raw = await r.get(f'{user_id}:wheel_state')
                state = state_raw.decode('utf-8') if isinstance(state_raw, bytes) else state_raw
                if state != 'waiting_confirm':
                    await callback_query.answer(REPLIES['plugins_games_bank_2180'], show_alert=True)
                    return

                user_balance = int(await r.get(f'{user_id}:Floos') or 0)
                if user_balance < 5000000:
                    await callback_query.answer(REPLIES['plugins_games_bank_2185'], show_alert=True)
                    return

                new_balance = user_balance - 5000000
                await r.set(f'{user_id}:Floos', new_balance)
                await enforce_balance_cap(r, None, k, user_id)

                await r.setex(f'{user_id}:wheel_state', 120, 'waiting_stop')

                video_url = "https://graph.org/file/e44b9bddf4b4f8c1f1765-de0e504bff672af128.mp4"
                caption = f"{k} اضغط لأيقاف العجلة"
                stop_btn = InlineKeyboardButton("ايقاف", callback_data=f"wheel_stop:{user_id}")
                keyboard = InlineKeyboardMarkup([[stop_btn]])

                try:
                    await client.edit_message_media(
                        chat_id=chat_id,
                        message_id=message_id,
                        media=InputMediaVideo(media=video_url, caption=caption),
                        reply_markup=keyboard
                    )
                    print(f"[wheel_confirm] video edited successfully")
                except Exception as e:
                    print(f"[wheel_confirm] edit_message_media error: {e}")
                    await callback_query.message.reply(plugins_games_bank_2209(k))
                return

            elif action == "wheel_stop":
                print(f"[wheel_stop] user={user_id}")
                await callback_query.answer()

                state_raw = await r.get(f'{user_id}:wheel_state')
                state = state_raw.decode('utf-8') if isinstance(state_raw, bytes) else state_raw
                if state != 'waiting_stop':
                    await callback_query.answer(REPLIES['plugins_games_bank_2180'], show_alert=True)
                    return

                await r.delete(f'{user_id}:wheel_state')

                results = ["15m", "5m", "1m", "car", "double", "nothing"]
                result = random.choice(results)
                print(f"[wheel_stop] result={result}")

                if result == "15m":
                    photo = "https://graph.org/file/6d7d88757ea6cb97aac89-574683ac15368c6ec9.jpg"
                    text = "ربحت معانا ( 15 ) مليون ﷼"
                    amount = 15000000
                    current_balance = int(await r.get(f'{user_id}:Floos') or 0)
                    await r.set(f'{user_id}:Floos', current_balance + amount)
                    await enforce_balance_cap(r, None, k, user_id)
                    await add_game_earnings(user_id, chat_id, amount, callback_query.id)

                elif result == "5m":
                    photo = "https://graph.org/file/25d2f565ee02b585fce2d-77d27dd85b33242413.jpg"
                    text = "ربحت معانا ( 5 ) مليون ﷼"
                    amount = 5000000
                    current_balance = int(await r.get(f'{user_id}:Floos') or 0)
                    await r.set(f'{user_id}:Floos', current_balance + amount)
                    await enforce_balance_cap(r, None, k, user_id)
                    await add_game_earnings(user_id, chat_id, amount, callback_query.id)

                elif result == "1m":
                    photo = "https://graph.org/file/5a35c25bfd82b1a5f8a8a-8f82135c7558ee6119.jpg"
                    text = "ربحت معانا ( 1 ) مليون ﷼"
                    amount = 1000000
                    current_balance = int(await r.get(f'{user_id}:Floos') or 0)
                    await r.set(f'{user_id}:Floos', current_balance + amount)
                    await enforce_balance_cap(r, None, k, user_id)
                    await add_game_earnings(user_id, chat_id, amount, callback_query.id)

                elif result == "car":
                    photo = "https://graph.org/file/033f74f13b9194d50ccad-6e4a51615e29c9a023.jpg"
                    text = "مبروك ربحت معنا سيارة رولزرويس"
                    car_item = "رولزرويس"
                    await r.hincrby(f'{user_id}:items', car_item, 1)

                elif result == "double":
                    photo = "https://graph.org/file/043946514cdc1fb307b8a-62b7ecfe76c9a0cefe.jpg"
                    text = "ربحت معانا ( x2 ) مضاعفة ارباحك بالالعاب لمدة 5 دقائق"
                    await r.setex(f'{user_id}:wheel_double', 300, 1)

                else:
                    photo = "https://graph.org/file/104a304d03da2666b9e85-f0baf4029357632794.jpg"
                    text = "للاسف ماربحت ولاشي ، خذلك وردة"

                try:
                    await client.edit_message_media(
                        chat_id=chat_id,
                        message_id=message_id,
                        media=InputMediaPhoto(media=photo, caption=f"{k} {text}"),
                        reply_markup=None
                    )
                    print(f"[wheel_stop] result photo edited successfully")
                except Exception as e:
                    print(f"[wheel_stop] edit_message_media error: {e}")
                    await callback_query.message.reply_photo(photo=photo, caption=f"{k} {text}")
                return

        return
    if data.startswith("shop_"):
        parts = data.split(":")
        if len(parts) == 2:
            action, target_user_id = parts
            if str(user_id) != target_user_id:
                await callback_query.answer(REPLIES['plugins_games_bank_2289'], show_alert=True)
                return
            data = action
        else:
            if data in ["shop_back", "shop_close"]:
                pass
            else:
                await callback_query.answer(REPLIES['plugins_games_bank_2289'], show_alert=True)
                return

    if data == 'confirm_reset_items':
        await callback_query.answer()
        await callback_query.message.delete()
    elif data == 'cancel_reset_items':
        await callback_query.answer()
        await callback_query.message.delete()
    elif data == 'shop_cars':
        await callback_query.answer()
        await show_cars_menu(client, callback_query.message, k, callback_query=callback_query)
    elif data == 'shop_planes':
        await callback_query.answer()
        await show_planes_menu(client, callback_query.message, k, callback_query=callback_query)
    elif data == 'shop_realestate':
        await callback_query.answer()
        await show_realestate_menu(client, callback_query.message, k, callback_query=callback_query)
    elif data == 'shop_jewelry':
        await callback_query.answer()
        await show_jewelry_menu(client, callback_query.message, k, callback_query=callback_query)
    elif data == 'shop_foods':
        await callback_query.answer()
        await show_foods_menu(client, callback_query.message, k, callback_query=callback_query)
    elif data == 'shop_back':
        await callback_query.answer()
        shop_text = f"""
 <b>المتجر</b>
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
• أهلاً بك في المتجر 
• اختر القسم المناسب :
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
"""
        cars_btn = await create_button_raw("bank", f"shop_cars:{user_id}", "السيارات", callback_data=f"shop_cars:{user_id}")
        planes_btn = await create_button_raw("bank", f"shop_planes:{user_id}", "الطائرات", callback_data=f"shop_planes:{user_id}")
        realestate_btn = await create_button_raw("bank", f"shop_realestate:{user_id}", "العقارات", callback_data=f"shop_realestate:{user_id}")
        jewelry_btn = await create_button_raw("bank", f"shop_jewelry:{user_id}", "المجوهرات", callback_data=f"shop_jewelry:{user_id}")
        foods_btn = await create_button_raw("bank", f"shop_foods:{user_id}", "المأكولات", callback_data=f"shop_foods:{user_id}")
        close_btn = await create_button_raw("bank", f"shop_close:{user_id}", "إغلاق", callback_data=f"shop_close:{user_id}")
        reply_markup = {
            "inline_keyboard": [
                [jewelry_btn, realestate_btn],
                [planes_btn, cars_btn],
                [foods_btn],
                [close_btn]
            ]
        }
        await edit_api_message(client, callback_query.message.chat.id, callback_query.message.id, shop_text, reply_markup=reply_markup)
    elif data == 'shop_close':
        await callback_query.answer()
        await callback_query.message.delete()