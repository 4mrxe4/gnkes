from helpers.context import get_global_r, get_global_dev, get_global_k
r = get_global_r()
Dev_FINAL = get_global_dev()
k = get_global_k()
k = get_global_k()
Dev_FINAL = get_global_dev()
r = get_global_r()
from helpers.context import get_global_r, get_global_dev, get_global_k
from compat import Client
import random, asyncio, json, urllib.parse, time, re, traceback, builtins
from compat import *
from compat import *
from helpers.ranks import *
from helpers.games import *
from helpers.redis import r as shared_r
from helpers.redis import RedisFake
from .utils import add_game_earnings, enforce_balance_cap
import builtins
from helpers.replies_store import (
    REPLIES,
    plugins_games_devgames_1011,
    plugins_games_devgames_1030,
    plugins_games_devgames_1042,
    plugins_games_devgames_1060,
    plugins_games_devgames_1067,
    plugins_games_devgames_1075,
    plugins_games_devgames_1093,
    plugins_games_devgames_1099,
    plugins_games_devgames_1107,
    plugins_games_devgames_1113,
    plugins_games_devgames_1125,
    plugins_games_devgames_1137,
    plugins_games_devgames_1145,
    plugins_games_devgames_1150,
    plugins_games_devgames_1161,
    plugins_games_devgames_1164,
    plugins_games_devgames_1179,
    plugins_games_devgames_1194,
    plugins_games_devgames_1198,
    plugins_games_devgames_1208,
    plugins_games_devgames_1219,
    plugins_games_devgames_1230,
    plugins_games_devgames_1239,
    plugins_games_devgames_1246,
    plugins_games_devgames_1255,
    plugins_games_devgames_1261,
    plugins_games_devgames_1265,
    plugins_games_devgames_1270,
    plugins_games_devgames_1293,
    plugins_games_devgames_1311,
    plugins_games_devgames_1317,
    plugins_games_devgames_1321,
    plugins_games_devgames_1326,
    plugins_games_devgames_1338,
    plugins_games_devgames_1356,
    plugins_games_devgames_1364,
    plugins_games_devgames_1381,
    plugins_games_devgames_1386,
    plugins_games_devgames_1402,
    plugins_games_devgames_1434,
    plugins_games_devgames_1442,
    plugins_games_devgames_1449,
    plugins_games_devgames_1455,
    plugins_games_devgames_1462,
    plugins_games_devgames_1465,
    plugins_games_devgames_1479,
    plugins_games_devgames_1491,
    plugins_games_devgames_1499,
    plugins_games_devgames_1505,
    plugins_games_devgames_1533,
    plugins_games_devgames_1544,
    plugins_games_devgames_1555,
    plugins_games_devgames_1601,
    plugins_games_devgames_1612,
    plugins_games_devgames_1647,
    plugins_games_devgames_1657,
    plugins_games_devgames_1662,
    plugins_games_devgames_1668,
    plugins_games_devgames_1691,
    plugins_games_devgames_1693,
    plugins_games_devgames_1709,
    plugins_games_devgames_1716,
    plugins_games_devgames_1730,
    plugins_games_devgames_1735,
    plugins_games_devgames_1740,
    plugins_games_devgames_1749,
    plugins_games_devgames_1762,
    plugins_games_devgames_1773,
    plugins_games_devgames_1805,
    plugins_games_devgames_1870,
    plugins_games_devgames_1887,
    plugins_games_devgames_1915,
    plugins_games_devgames_1932,
    plugins_games_devgames_1948,
    plugins_games_devgames_1950,
    plugins_games_devgames_1998,
    plugins_games_devgames_2002,
    plugins_games_devgames_2007,
    plugins_games_devgames_334,
    plugins_games_devgames_338,
    plugins_games_devgames_340,
    plugins_games_devgames_365,
    plugins_games_devgames_367,
    plugins_games_devgames_390,
    plugins_games_devgames_410,
    plugins_games_devgames_414,
    plugins_games_devgames_418,
    plugins_games_devgames_422,
    plugins_games_devgames_426,
    plugins_games_devgames_429,
    plugins_games_devgames_437,
    plugins_games_devgames_445,
    plugins_games_devgames_449,
    plugins_games_devgames_452,
    plugins_games_devgames_477,
    plugins_games_devgames_518,
    plugins_games_devgames_547,
    plugins_games_devgames_586,
    plugins_games_devgames_599,
    plugins_games_devgames_809,
    plugins_games_devgames_828,
    plugins_games_devgames_834,
    plugins_games_devgames_839,
    plugins_games_devgames_855,
    plugins_games_devgames_863,
    plugins_games_devgames_872,
    plugins_games_devgames_879,
    plugins_games_devgames_892,
    plugins_games_devgames_897,
    plugins_games_devgames_903,
    plugins_games_devgames_919,
    plugins_games_devgames_948,
    plugins_games_devgames_958,
    plugins_games_devgames_962,
    plugins_games_devgames_967,
    plugins_games_devgames_972,
)

AEC_ID = 5434703779

GLOBAL_R = RedisFake()

GLOBAL_GAMES_KEY = "GLOBAL:public_games"
GLOBAL_GAMES_META_KEY = "GLOBAL:public_games_meta"
GLOBAL_BUTTON_GAMES_KEY = "GLOBAL:public_button_games"
GLOBAL_GAMES_CATEGORIES_KEY = "GLOBAL:public_games_categories"

ALLOWED_RANKS = [AEC_ID]


def _local_game_key(dev_final):
    return f"{dev_final}:public_games_local"

def _local_button_key(dev_final):
    return f"{dev_final}:public_button_games_local"


async def is_dev_or_dev2(user_id, chat_id):
    """رتبة Dev (مالك البوت) أو Dev² فقط - بدون Aec"""
    try:
        rank = await get_rank(user_id, chat_id)
    except Exception:
        return False
    return rank in ('Dev', 'Dev²')


async def can_manage_public_content(user_id, chat_id):
    """من يحق له الاضافة على لعبة عامة موجودة: Aec، أو Dev/Dev²"""
    if user_id in ALLOWED_RANKS:
        return True
    return await is_dev_or_dev2(user_id, chat_id)


def _split_by_owner(items):
    """يقسم قائمة عناصر (ميديا/اسئلة) إلى (عام لـ Aec، محلي لغيره)"""
    base_items, local_items = [], []
    for item in items:
        if 'added_by' not in item or item.get('added_by') == AEC_ID:
            base_items.append(item)
        else:
            local_items.append(item)
    return base_items, local_items





async def get_public_categories():
    """جلب جميع الفئات والألعاب"""
    categories = await GLOBAL_R.hgetall(GLOBAL_GAMES_CATEGORIES_KEY)
    if not categories:
        return {'الرئيسية': []}

    result = {}
    for cat, games in categories.items():
        cat = cat.decode() if isinstance(cat, bytes) else cat
        games = json.loads(games.decode() if isinstance(games, bytes) else games)
        result[cat] = games
    return result

async def save_public_categories(categories):
    """حفظ الفئات والألعاب"""
    for cat, games in categories.items():
        await GLOBAL_R.hset(GLOBAL_GAMES_CATEGORIES_KEY, cat, json.dumps(games))

async def move_game_to_category(game_name, category_name):
    """نقل لعبة إلى فئة معينة"""
    categories = await get_public_categories()

    for cat, games in categories.items():
        if game_name in games:
            games.remove(game_name)
            break

    if category_name not in categories:
        categories[category_name] = []
    if game_name not in categories[category_name]:
        categories[category_name].append(game_name)

    await save_public_categories(categories)
    return True

async def get_games_by_category(category_name='الرئيسية'):
    """جلب ألعاب فئة معينة"""
    categories = await get_public_categories()
    return categories.get(category_name, [])

async def get_all_game_names():
    """جلب أسماء جميع الألعاب"""
    games = await get_all_public_games()
    button_games = await get_public_button_games()
    all_games = [g['name'] for g in games] + [g['name'] for g in button_games]
    return all_games


async def is_public_game_admin(user_id):
    """التحقق من صلاحية إدارة الألعاب العامة (Aec🎖️ فقط)"""
    return user_id in ALLOWED_RANKS



async def get_public_game_meta(game_name):
    meta = await GLOBAL_R.hget(GLOBAL_GAMES_META_KEY, game_name)
    if meta:
        return json.loads(meta.decode() if isinstance(meta, bytes) else meta)
    return None

async def save_public_game_meta(game_name, data):
    await GLOBAL_R.hset(GLOBAL_GAMES_META_KEY, game_name, json.dumps(data))

async def delete_public_game_meta(game_name):
    await GLOBAL_R.hdel(GLOBAL_GAMES_META_KEY, game_name)

async def get_all_public_games():
    games = await GLOBAL_R.hgetall(GLOBAL_GAMES_META_KEY)
    result = []
    for name, data in games.items():
        name = name.decode() if isinstance(name, bytes) else name
        data = json.loads(data.decode() if isinstance(data, bytes) else data)
        result.append(data)
    return result



async def _get_base_game_media(game_name):
    game = await GLOBAL_R.hget(GLOBAL_GAMES_KEY, game_name)
    if game:
        data = json.loads(game.decode() if isinstance(game, bytes) else game)
        return data.get('media', [])
    return []

async def _get_local_game_media(game_name):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    raw = await r.hget(_local_game_key(Dev_FINAL), game_name)
    if raw:
        data = json.loads(raw.decode() if isinstance(raw, bytes) else raw)
        return data.get('media', [])
    return []

async def get_public_game_data(game_name):
    """يرجع دائماً الدمج: محتوى Aec العام + محتوى Dev/Dev² المحلي لهذا البوت"""
    base_media = await _get_base_game_media(game_name)
    local_media = await _get_local_game_media(game_name)
    if not base_media and not local_media:
        if not await get_public_game_meta(game_name):
            return None
    return {"media": base_media + local_media}

async def save_public_game_data(game_name, data):
    """
    يستقبل القائمة الكاملة (كما تُقرأ من get_public_game_data ثم تُعدَّل)
    ويعيد توزيعها تلقائياً حسب added_by: عناصر Aec → الطبقة العامة (تصل
    فوراً لكل البوتات)، وعناصر Dev/Dev² → الطبقة المحلية لهذا البوت فقط.
    هذا يضمن استحالة أن يمس حفظ محلي محتوى Aec العام.
    """
    full_media = data.get('media', []) if data else []
    base_items, local_items = _split_by_owner(full_media)

    current_base = await _get_base_game_media(game_name)
    if json.dumps(current_base, sort_keys=True, ensure_ascii=False) != json.dumps(base_items, sort_keys=True, ensure_ascii=False):
        await GLOBAL_R.hset(GLOBAL_GAMES_KEY, game_name, json.dumps({"media": base_items}))

    r = get_global_r()
    Dev_FINAL = get_global_dev()
    await r.hset(_local_game_key(Dev_FINAL), game_name, json.dumps({"media": local_items}))

async def delete_public_game_data(game_name):
    """حذف كامل محتوى اللعبة: الطبقة العامة + الطبقة المحلية لهذا البوت"""
    await GLOBAL_R.hdel(GLOBAL_GAMES_KEY, game_name)
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    await r.hdel(_local_game_key(Dev_FINAL), game_name)



async def _get_base_button_game(game_name):
    game = await GLOBAL_R.hget(GLOBAL_BUTTON_GAMES_KEY, game_name)
    if game:
        return json.loads(game.decode() if isinstance(game, bytes) else game)
    return None

async def _get_local_button_questions(game_name):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    raw = await r.hget(_local_button_key(Dev_FINAL), game_name)
    if raw:
        data = json.loads(raw.decode() if isinstance(raw, bytes) else raw)
        return data.get('questions', [])
    return []

async def get_public_button_game_data(game_name):
    """يرجع دائماً الدمج: اسئلة Aec العامة + اسئلة Dev/Dev² المحلية لهذا البوت"""
    base = await _get_base_button_game(game_name)
    if not base:
        return None
    local_questions = await _get_local_button_questions(game_name)
    merged = dict(base)
    merged['questions'] = list(base.get('questions', [])) + local_questions
    return merged

async def save_public_button_game_data(game_name, data):
    """يعيد توزيع الاسئلة حسب added_by تماماً مثل محتوى الألعاب العادية"""
    questions = data.get('questions', []) if data else []
    base_questions, local_questions = _split_by_owner(questions)

    base = await _get_base_button_game(game_name) or {}
    new_base = {
        'type': data.get('type', base.get('type')),
        'has_money': data.get('has_money', base.get('has_money', False)),
        'questions': base_questions,
    }
    if json.dumps(base, sort_keys=True, ensure_ascii=False) != json.dumps(new_base, sort_keys=True, ensure_ascii=False):
        await GLOBAL_R.hset(GLOBAL_BUTTON_GAMES_KEY, game_name, json.dumps(new_base))

    r = get_global_r()
    Dev_FINAL = get_global_dev()
    await r.hset(_local_button_key(Dev_FINAL), game_name, json.dumps({'questions': local_questions}))

async def delete_public_button_game_data(game_name):
    await GLOBAL_R.hdel(GLOBAL_BUTTON_GAMES_KEY, game_name)
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    await r.hdel(_local_button_key(Dev_FINAL), game_name)

async def get_public_button_games():
    """جلب جميع ألعاب الأزرار (مدموجة: عام + محلي لهذا البوت)"""
    base_all = await GLOBAL_R.hgetall(GLOBAL_BUTTON_GAMES_KEY)
    result = []
    for name in base_all.keys():
        name = name.decode() if isinstance(name, bytes) else name
        merged = await get_public_button_game_data(name)
        if merged:
            result.append({'name': name, 'data': merged})
    return result


async def handle_public_games(c, m, k, text):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    
    admin_setup_commands = [
        'اضف لعبه عام', 'اضف لعبة عام', 
        'اضف لعبه ازرار عام', 'اضف لعبة ازرار عام',
        'مسح لعبه عام', 'مسح لعبة عام',
    ]
    has_active_setup_wizard = bool(
        await r.get(f'{m.from_user.id}:addPublicGameStep:{m.chat.id}{Dev_FINAL}') or
        await r.get(f'{m.from_user.id}:addPublicMediaStep:{m.chat.id}{Dev_FINAL}') or
        await r.get(f'{m.from_user.id}:addPublicButtonStep:{m.chat.id}{Dev_FINAL}') or
        await r.get(f'{m.from_user.id}:deletePublicMediaStep:{m.chat.id}{Dev_FINAL}') or
        await r.get(f'{m.from_user.id}:deletePublicGameStep:{m.chat.id}{Dev_FINAL}')
    )
    is_admin_setup_cmd = (
        text in admin_setup_commands or
        (text.startswith('اضف ') and text.endswith(' عام')) or
        (text.startswith('حذف ') and text.endswith(' عام')) or
        (text.startswith('قائمة ') and text.endswith(' عام')) or
        has_active_setup_wizard
    )
    
    if not is_admin_setup_cmd:
        if not await r.get(f'{m.chat.id}:enable:{Dev_FINAL}'):
            return None
    if await r.get(f'{m.chat.id}:mute:{Dev_FINAL}') and not await admin_pls(m.from_user.id, m.chat.id):
        return None
    if await r.get(f'{m.from_user.id}:mute:{m.chat.id}{Dev_FINAL}'):
        return None
    if await r.get(f'{m.from_user.id}:mute:{Dev_FINAL}'):
        return None
    if await r.get(f'{m.chat.id}:addCustom:{m.from_user.id}{Dev_FINAL}'):
        return None
    if await r.get(f'{m.chat.id}addCustomG:{m.from_user.id}{Dev_FINAL}'):
        return None
    if await r.get(f'{m.chat.id}:delCustom:{m.from_user.id}{Dev_FINAL}') or await r.get(f'{m.chat.id}:delCustomG:{m.from_user.id}{Dev_FINAL}'):
        return None
    
    name = await r.get(f'{Dev_FINAL}:BotName') if await r.get(f'{Dev_FINAL}:BotName') else 'فاينل'
    if text.startswith(f'{name} '):
        text = text.replace(f'{name} ', '')
    
    if await r.get(f'{m.chat.id}:Custom:{m.chat.id}{Dev_FINAL}&text={text}'):
        text = await r.get(f'{m.chat.id}:Custom:{m.chat.id}{Dev_FINAL}&text={text}')
    if await r.get(f'Custom:{Dev_FINAL}&text={text}'):
        text = await r.get(f'Custom:{Dev_FINAL}&text={text}')
    
    if await r.get(f'{m.from_user.id}:addPublicGameStep:{m.chat.id}{Dev_FINAL}'):
        return await handle_add_public_game_step(c, m, k, text)
    
    if await r.get(f'{m.from_user.id}:addPublicMediaStep:{m.chat.id}{Dev_FINAL}'):
        return await handle_add_public_media_step(c, m, k, text)
    
    if await r.get(f'{m.from_user.id}:addPublicButtonStep:{m.chat.id}{Dev_FINAL}'):
        return await handle_add_public_button_step(c, m, k, text)
    
    if await r.get(f'{m.from_user.id}:deletePublicMediaStep:{m.chat.id}{Dev_FINAL}'):
        return await handle_delete_public_media_step(c, m, k, text)
    
    if await r.get(f'{m.from_user.id}:deletePublicGameStep:{m.chat.id}{Dev_FINAL}'):
        return await handle_delete_public_game_step(c, m, k, text)
    
    admin_commands = [
        'اضف لعبه عام', 'اضف لعبة عام', 
        'اضف لعبه ازرار عام', 'اضف لعبة ازرار عام',
        'مسح لعبه عام', 'مسح لعبة عام',
    ]
    
    is_admin_cmd = False
    
    if text in admin_commands:
        is_admin_cmd = True
    
    elif text.startswith('اضف ') and text.endswith(' عام'):
        game_name = text.replace('اضف ', '').replace(' عام', '').strip()
        if await get_public_game_meta(game_name) or await get_public_button_game_data(game_name):
            is_admin_cmd = True
        else:
            return None
    
    elif text.startswith('حذف ') and text.endswith(' عام'):
        game_name = text.replace('حذف ', '').replace(' عام', '').strip()
        if await get_public_game_meta(game_name) or await get_public_button_game_data(game_name):
            is_admin_cmd = True
        else:
            return None
    
    elif text.startswith('قائمة ') and text.endswith(' عام'):
        game_name = text.replace('قائمة ', '').replace(' عام', '').strip()
        if await get_public_game_meta(game_name) or await get_public_button_game_data(game_name):
            is_admin_cmd = True
        else:
            return None
    
    if is_admin_cmd and not await is_public_game_admin(m.from_user.id):
        return await m.reply(plugins_games_devgames_334(k))
    
    if text == 'اضف لعبه عام' or text == 'اضف لعبة عام':
        if await r.get(f'{m.from_user.id}:addPublicGameStep:{m.chat.id}{Dev_FINAL}'):
            return await m.reply(plugins_games_devgames_338(k))
        await r.set(f'{m.from_user.id}:addPublicGameStep:{m.chat.id}{Dev_FINAL}', 'wait_type')
        await m.reply(plugins_games_devgames_340(k))
        return True
    
    
    if text == 'اضف لعبه ازرار عام' or text == 'اضف لعبة ازرار عام':
        if await r.get(f'{m.from_user.id}:addPublicGameStep:{m.chat.id}{Dev_FINAL}'):
            return await m.reply(plugins_games_devgames_365(k))
        await r.set(f'{m.from_user.id}:addPublicGameStep:{m.chat.id}{Dev_FINAL}', 'wait_type_button')
        await m.reply(plugins_games_devgames_367(k))
        return True
    
    if text == 'مسح لعبه عام' or text == 'مسح لعبة عام':
        games = await get_all_public_games()
        button_games = await get_public_button_games()
        if not games and not button_games:
            return await m.reply(plugins_games_devgames_390(k))
        txt = f'{k} قائمة الالعاب العامه:\n\n'
        i = 1
        for game in games:
            txt += f'{i} - {game["name"]} ({game["type"]})\n'
            i += 1
        for game in button_games:
            txt += f'{i} - {game["name"]} (ازرار | {game["data"]["type"]})\n'
            i += 1
        txt += f'\n{k} ارسل رقم اللعبة التي تريد مسحها\nللالغاء اكتب الغاء'
        await r.set(f'{m.from_user.id}:deletePublicGameStep:{m.chat.id}{Dev_FINAL}', 'wait_number')
        await m.reply(txt)
        return True
    
    if text.startswith('اضف '):
        game_name = text.replace('اضف ', '').strip()
        meta = await get_public_game_meta(game_name)
        btn_game_data = None if meta else await get_public_button_game_data(game_name)

        if (meta or btn_game_data) and not await can_manage_public_content(m.from_user.id, m.chat.id):
            return await m.reply(plugins_games_devgames_410(k))

        if meta:
            if await r.get(f'{m.from_user.id}:addPublicMediaStep:{m.chat.id}{Dev_FINAL}'):
                return await m.reply(plugins_games_devgames_414(k))
            await r.set(f'{m.from_user.id}:addPublicMediaStep:{m.chat.id}{Dev_FINAL}', 'wait_photo')
            await r.set(f'{m.from_user.id}:addPublicMediaType:{m.chat.id}{Dev_FINAL}', game_name)
            await r.set(f'{m.from_user.id}:addPublicMediaMeta:{m.chat.id}{Dev_FINAL}', json.dumps(meta))
            await m.reply(plugins_games_devgames_418(k, meta["type"]))
            return True
        if btn_game_data:
            if await r.get(f'{m.from_user.id}:addPublicButtonStep:{m.chat.id}{Dev_FINAL}'):
                return await m.reply(plugins_games_devgames_422(k))
            await r.set(f'{m.from_user.id}:addPublicButtonType:{m.chat.id}{Dev_FINAL}', game_name)
            if btn_game_data.get('type') == 'نصوص':
                await r.set(f'{m.from_user.id}:addPublicButtonStep:{m.chat.id}{Dev_FINAL}', 'wait_media')
                await m.reply(plugins_games_devgames_426(k))
            else:
                await r.set(f'{m.from_user.id}:addPublicButtonStep:{m.chat.id}{Dev_FINAL}', 'wait_media_file')
                await m.reply(plugins_games_devgames_429(k, btn_game_data["type"]))
            return True
    
    if text.endswith(' الكل'):
        game_name = text.replace(' الكل', '').replace('حذف ', '').strip()
        if await get_public_game_meta(game_name):
            game_data = await get_public_game_data(game_name)
            if not game_data or not game_data.get("media"):
                return await m.reply(plugins_games_devgames_437(k, game_name))
            
            is_admin = await is_public_game_admin(m.from_user.id)
            media_list = game_data["media"]
            
            if not is_admin:
                filtered_list = [item for item in media_list if item.get('added_by', 0) == m.from_user.id]
                if not filtered_list:
                    return await m.reply(plugins_games_devgames_445(k))
                for item in filtered_list:
                    media_list.remove(item)
                await save_public_game_data(game_name, game_data)
                await m.reply(plugins_games_devgames_449(k, len(filtered_list), game_name))
            else:
                await save_public_game_data(game_name, {"media": []})
                await m.reply(plugins_games_devgames_452(k, game_name))
            return True
        else:
            game_name = text.replace('حذف ', '').strip()
            if await get_public_game_meta(game_name):
                return await handle_delete_public_media(c, m, k, game_name)
            if await get_public_button_game_data(game_name):
                return await handle_delete_public_button_media(c, m, k, game_name)
    
    if await get_public_game_meta(text):
        if await is_game_disabled_in_chat(m.chat.id, text):
            return None
        return await handle_play_public_game(c, m, k, text)
    
    if await get_public_button_game_data(text):
        if await is_game_disabled_in_chat(m.chat.id, text):
            return None
        return await handle_play_public_button_game(c, m, k, text)

    return None

async def handle_play_public_game(c, m, k, game_name):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    meta = await get_public_game_meta(game_name)
    game_data = await get_public_game_data(game_name)
    
    if not game_data or not game_data.get("media"):
        return await m.reply(plugins_games_devgames_477(k, game_name))
    
    media_list = game_data["media"]
    total = len(media_list)
    
    current_index_key = f'{m.chat.id}:public_game_index:{game_name}:{m.from_user.id}'
    current_index = await r.get(current_index_key)
    if current_index:
        current_index = int(current_index.decode() if isinstance(current_index, bytes) else current_index)
    else:
        current_index = 0
    
    if current_index >= total:
        current_index = 0
    
    item = media_list[current_index]
    
    next_index = (current_index + 1) % total
    await r.set(current_index_key, next_index, ex=3600)
    
    if meta.get('has_questions', False):
        await r.set(f'{m.chat.id}:game:{Dev_FINAL}', json.dumps(item.get('answer', [])), ex=600)
        await r.set(f'{m.chat.id}:public_game_current:{game_name}:{m.from_user.id}', str(current_index), ex=600)
        has_money = 1 if meta.get('has_money', False) else 0
        await r.set(f'{m.chat.id}:public_game_has_money:{game_name}:{m.from_user.id}', has_money, ex=600)
        await r.set(f'{m.chat.id}:public_game_name:{m.from_user.id}', game_name, ex=600)
        await r.set(f'{m.chat.id}:game_answer_start:{Dev_FINAL}', str(time.time()), ex=600)
    
    show_change_button = not meta.get('has_questions', False) and meta.get('type') != 'نصوص'
    reply_markup = None
    
    if show_change_button:
        caption_text = f'ㅤㅤㅤㅤㅤ 『 {current_index + 1} 』ㅤㅤㅤㅤㅤㅤㅤ'
        change_btn = InlineKeyboardButton("تغيير", callback_data=f"public_change_{game_name}_{next_index}_{m.from_user.id}")
        reply_markup = InlineKeyboardMarkup([[change_btn]])
    else:
        caption_text = (item.get('caption', '') or meta.get('caption', '')) if meta.get('has_questions', False) else ''
    
    if meta['type'] == 'صور':
        if 'media' in item:
            await m.reply_photo(item['media'], caption=caption_text, reply_markup=reply_markup)
        elif 'text' in item:
            await m.reply(plugins_games_devgames_518(caption_text, item['text']), reply_markup=reply_markup)
    
    elif meta['type'] == 'فيديو':
        if 'media' in item:
            await m.reply_video(item['media'], caption=caption_text, reply_markup=reply_markup)
    
    elif meta['type'] == 'صوت':
        if 'media' in item:
            await m.reply_audio(item['media'], caption=caption_text, reply_markup=reply_markup)
        elif 'voice' in item:
            await m.reply_voice(item['voice'], caption=caption_text)
    
    elif meta['type'] == 'قيفات':
        if 'media' in item:
            await m.reply_animation(item['media'], caption=caption_text, reply_markup=reply_markup)
    
    elif meta['type'] == 'نصوص':
        if 'text' in item:
            caption_text = meta.get('caption', '') if meta.get('has_questions', False) else ''
            await m.reply(f"{caption_text}\n\n{item['text']}" if caption_text else item['text'])
    
    return True

async def handle_play_public_button_game(c, m, k, game_name):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    game_data = await get_public_button_game_data(game_name)
    if not game_data or not game_data.get("questions"):
        return await m.reply(plugins_games_devgames_547(k, game_name))
    
    questions_list = game_data["questions"]
    total = len(questions_list)
    
    current_index_key = f'{m.chat.id}:public_button_index:{game_name}:{m.from_user.id}'
    current_index = await r.get(current_index_key)
    if current_index:
        current_index = int(current_index.decode() if isinstance(current_index, bytes) else current_index)
    else:
        current_index = 0
    
    if current_index >= total:
        current_index = 0
    
    item = questions_list[current_index]
    question = item.get('question', '')
    correct_answer = item.get('correct_answer', '')
    wrong_answers = item.get('wrong_answers', [])
    
    all_answers = wrong_answers + [correct_answer]
    random.shuffle(all_answers)
    
    buttons = []
    for i, ans in enumerate(all_answers):
        is_correct = (ans == correct_answer)
        callback_data = f"public_button_ans_{game_name}_{current_index}_{i}_{str(is_correct)}_{m.from_user.id}"
        buttons.append(InlineKeyboardButton(ans, callback_data=callback_data))
    
    reply_markup = InlineKeyboardMarkup([
        [buttons[0], buttons[1]],
        [buttons[2], buttons[3]]
    ])
    
    has_money = game_data.get('has_money', False)
    await r.set(f'{m.chat.id}:public_button_has_money:{game_name}:{m.from_user.id}', 1 if has_money else 0, ex=600)
    await r.set(f'{m.chat.id}:public_button_name:{m.from_user.id}', game_name, ex=600)
    
    if game_data['type'] == 'نصوص':
        await m.reply(plugins_games_devgames_586(question), reply_markup=reply_markup)
    else:
        media_id = item.get('media')
        if media_id:
            if game_data['type'] == 'صور':
                await m.reply_photo(media_id, caption=f"؟ {question}", reply_markup=reply_markup)
            elif game_data['type'] == 'فيديو':
                await m.reply_video(media_id, caption=f"؟ {question}", reply_markup=reply_markup)
            elif game_data['type'] == 'صوت':
                await m.reply_audio(media_id, caption=f"؟ {question}", reply_markup=reply_markup)
            elif game_data['type'] == 'قيفات':
                await m.reply_animation(media_id, caption=f"؟ {question}", reply_markup=reply_markup)
        else:
            await m.reply(plugins_games_devgames_599(question), reply_markup=reply_markup)
    
    return True

def parse_telegram_message_link(link):
    """
    يستخرج مرجع القناة (يوزر او chat_id) ورقم الرسالة من رابط رسالة تيليجرام.
    يدعم:
      https://t.me/username/12345
      t.me/username/12345
      https://t.me/username/12345?single   (روابط الالبومات)
      https://t.me/c/1234567890/12345      (قنوات عبر المعرف الرقمي الداخلي)
    يرجع (chat_ref, message_id) او (None, None) لو الرابط غير صالح.
    """
    if not link:
        return None, None

    link = link.strip()
    link = link.split('?')[0].split('#')[0].rstrip('/')

    if not link.startswith('http'):
        link = 'https://' + link

    m = re.match(r'https?://t\.me/c/(\d+)/(\d+)$', link)
    if m:
        internal_id = int(m.group(1))
        message_id = int(m.group(2))
        chat_ref = int(f"-100{internal_id}")
        return chat_ref, message_id

    m = re.match(r'https?://t\.me/([A-Za-z0-9_]{4,})/(\d+)$', link)
    if m:
        username = m.group(1)
        message_id = int(m.group(2))
        return '@' + username, message_id

    return None, None


async def save_media_from_channel_by_message_link(c, m, game_name, chat_ref, start_message_id, count, meta):
    """
    يجلب الميديا بدءاً من رقم رسالة محدد (مستخرج من رابط اخر ميديا في القناة)
    ونزولاً للاقدم: start_message_id, start_message_id-1, start_message_id-2 ...
    """
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()

    BATCH_SIZE = 200

    try:
        try:
            chat = await c.get_chat(chat_ref)
            chat_id = chat.id
        except Exception as e:
            return False, f"لا يمكن الوصول للقناة عبر الرابط.\nسبب الخطأ: {e}\n\nتأكد ان الرابط صحيح وان الرسالة لم تُحذف."

        matched_messages = []
        seen_groups = {}
        current_id = start_message_id
        reached_start_of_chat = False

        while len(matched_messages) < count and current_id >= 1:
            lowest_id = max(current_id - BATCH_SIZE, 0)
            
            batch_ids = builtins.list(range(current_id, lowest_id, -1))
            
            if not batch_ids:
                break

            try:
                batch = await c.get_messages(chat_id, message_ids=batch_ids)
            except Exception as e:
                return False, f"خطأ اثناء جلب الرسائل: {e}"

            if not batch:
                break
            
            if not isinstance(batch, builtins.list):
                batch = [batch]

            for msg in batch:
                if msg is None or getattr(msg, 'empty', False):
                    continue

                try:
                    has_media = False
                    if meta['type'] == 'صور' and msg.photo:
                        has_media = True
                    elif meta['type'] == 'فيديو' and msg.video:
                        has_media = True
                    elif meta['type'] == 'صوت' and (msg.audio or msg.voice):
                        has_media = True
                    elif meta['type'] == 'قيفات' and msg.animation:
                        has_media = True
                    elif meta['type'] == 'نصوص' and msg.text:
                        has_media = True

                    if not has_media:
                        continue

                    gid = getattr(msg, 'media_group_id', None)
                    if gid:
                        taken = seen_groups.get(gid, 0)
                        if taken >= 2:
                            continue
                        seen_groups[gid] = taken + 1

                    matched_messages.append(msg)
                    if len(matched_messages) >= count:
                        break
                except Exception:
                    continue

            if lowest_id <= 0:
                reached_start_of_chat = True

            current_id = lowest_id

        if not matched_messages:
            return False, f"لا يوجد {meta['type']} حول الرسالة المرسلة.\nجرّب رابط رسالة اخرى تحتوي {meta['type']} فعلياً."

        game_data = await get_public_game_data(game_name)
        if not game_data:
            game_data = {"media": []}

        existing_ids = {item.get('_src_msg_id') for item in game_data["media"] if item.get('_src_msg_id')}

        added_count = 0
        for msg in matched_messages:
            if msg.id in existing_ids:
                continue

            media_item = {"added_by": m.from_user.id, "_src_msg_id": msg.id}

            try:
                if meta['type'] == 'صور' and msg.photo:
                    media_item["media"] = msg.photo.file_id
                elif meta['type'] == 'فيديو' and msg.video:
                    media_item["media"] = msg.video.file_id
                elif meta['type'] == 'صوت':
                    if msg.audio:
                        media_item["media"] = msg.audio.file_id
                    elif msg.voice:
                        media_item["voice"] = msg.voice.file_id
                elif meta['type'] == 'قيفات' and msg.animation:
                    media_item["media"] = msg.animation.file_id
                elif meta['type'] == 'نصوص' and msg.text:
                    media_item["text"] = msg.text
                else:
                    continue

                if msg.caption:
                    media_item["caption"] = msg.html

                if meta.get('has_questions', False):
                    media_item["answer"] = []

                game_data["media"].append(media_item)
                added_count += 1
            except Exception:
                continue

        if added_count == 0:
            return False, f"لا يوجد {meta['type']} جديد (كل ما تم العثور عليه محفوظ مسبقاً)."

        await save_public_game_data(game_name, game_data)

        note = ""
        if added_count < count and reached_start_of_chat:
            note = f"\n{k} ملاحظة: انتهت رسائل القناة قبل استيفاء العدد المطلوب"

        return True, f"تم حفظ {added_count} {meta['type']} (المطلوب: {count}){note}"

    except Exception as e:
        tb = traceback.format_exc()
        print(f"[save_media_from_channel_by_message_link] {tb}")
        last_line = tb.strip().splitlines()[-2] if len(tb.strip().splitlines()) >= 2 else ""
        return False, f"خطأ: {str(e)}\nموقع الخطأ: {last_line}"


async def handle_add_public_media_step(c, m, k, text):
    """معالج إضافة ميديا للألعاب العامة"""
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    
    step_raw = await r.get(f'{m.from_user.id}:addPublicMediaStep:{m.chat.id}{Dev_FINAL}')
    if step_raw is None:
        return True
    
    step = step_raw.decode() if isinstance(step_raw, bytes) else str(step_raw)
    
    game_name_raw = await r.get(f'{m.from_user.id}:addPublicMediaType:{m.chat.id}{Dev_FINAL}')
    if game_name_raw is None:
        return True
    
    game_name = game_name_raw.decode() if isinstance(game_name_raw, bytes) else str(game_name_raw)
    
    meta_raw = await r.get(f'{m.from_user.id}:addPublicMediaMeta:{m.chat.id}{Dev_FINAL}')
    meta = None
    if meta_raw:
        meta = json.loads(meta_raw.decode() if isinstance(meta_raw, bytes) else meta_raw)
    
    if text == 'الغاء':
        await r.delete(f'{m.from_user.id}:addPublicMediaStep:{m.chat.id}{Dev_FINAL}')
        await r.delete(f'{m.from_user.id}:addPublicMediaType:{m.chat.id}{Dev_FINAL}')
        await r.delete(f'{m.from_user.id}:addPublicMediaMeta:{m.chat.id}{Dev_FINAL}')
        await r.delete(f'{m.from_user.id}:addPublicMediaData:{m.chat.id}{Dev_FINAL}')
        await r.delete(f'{m.from_user.id}:addPublicMediaBatch:{m.chat.id}{Dev_FINAL}')
        await m.reply(plugins_games_devgames_809(k))
        return True
    
    if step == 'wait_photo':
        if text == 'تم':
            batch_key = f'{m.from_user.id}:addPublicMediaBatch:{m.chat.id}{Dev_FINAL}'
            batch_data = await r.get(batch_key)
            if batch_data:
                if isinstance(batch_data, bytes):
                    batch_data = batch_data.decode('utf-8')
                batch = json.loads(batch_data)
                if batch:
                    game_data = await get_public_game_data(game_name)
                    if not game_data:
                        game_data = {"media": []}
                    for item in batch:
                        game_data["media"].append(item)
                    await save_public_game_data(game_name, game_data)
                    await r.delete(batch_key)
                    await m.reply(plugins_games_devgames_828(k, len(batch), meta["type"]))
            
            await r.delete(f'{m.from_user.id}:addPublicMediaStep:{m.chat.id}{Dev_FINAL}')
            await r.delete(f'{m.from_user.id}:addPublicMediaType:{m.chat.id}{Dev_FINAL}')
            await r.delete(f'{m.from_user.id}:addPublicMediaMeta:{m.chat.id}{Dev_FINAL}')
            await r.delete(f'{m.from_user.id}:addPublicMediaData:{m.chat.id}{Dev_FINAL}')
            await m.reply(plugins_games_devgames_834(k))
            return True
        
        if meta and meta.get('type') == 'نصوص':
            if not text or text.strip() == '':
                await m.reply(plugins_games_devgames_839(k))
                return True
            
            lines = text.strip().split('\n')
            added = 0
            game_data = await get_public_game_data(game_name)
            if not game_data:
                game_data = {"media": []}
            
            for line in lines:
                line = line.strip()
                if line:
                    if meta.get('has_questions', False):
                        await r.set(f'{m.from_user.id}:addPublicMediaData:{m.chat.id}{Dev_FINAL}', 
                                    json.dumps({'text': line, 'caption': ''}))
                        await r.set(f'{m.from_user.id}:addPublicMediaStep:{m.chat.id}{Dev_FINAL}', 'wait_answers')
                        await m.reply(plugins_games_devgames_855(k, k))
                        return True
                    else:
                        game_data["media"].append({"text": line, "answer": [], "added_by": m.from_user.id})
                        added += 1
            
            if added > 0 and not meta.get('has_questions', False):
                await save_public_game_data(game_name, game_data)
                await m.reply(plugins_games_devgames_863(k, added, k, len(game_data["media"]), k, k))
                await r.set(f'{m.from_user.id}:addPublicMediaStep:{m.chat.id}{Dev_FINAL}', 'wait_photo')
            return True
        
        media_id = None
        media_type = None
        
        if meta and meta.get('type') == 'صور':
            if not m.photo:
                await m.reply(plugins_games_devgames_872(k))
                return True
            media_id = m.photo.file_id
            media_type = 'photo'
        
        elif meta and meta.get('type') == 'فيديو':
            if not m.video:
                await m.reply(plugins_games_devgames_879(k))
                return True
            media_id = m.video.file_id
            media_type = 'video'
        
        elif meta and meta.get('type') == 'صوت':
            if m.audio:
                media_id = m.audio.file_id
                media_type = 'audio'
            elif m.voice:
                media_id = m.voice.file_id
                media_type = 'voice'
            else:
                await m.reply(plugins_games_devgames_892(k))
                return True
        
        elif meta and meta.get('type') == 'قيفات':
            if not m.animation:
                await m.reply(plugins_games_devgames_897(k))
                return True
            media_id = m.animation.file_id
            media_type = 'animation'
        
        else:
            await m.reply(plugins_games_devgames_903(k))
            return True
        
        has_questions_flow = bool(meta and meta.get('has_questions', False))
        caption = (m.html if m.caption else '') if has_questions_flow else ''
        
        if has_questions_flow and meta.get('type') == 'صور' and not caption.strip():
            await m.reply(plugins_games_devgames_1491(k, meta["type"]))
            return True
        
        save_data = {}
        if media_type == 'voice':
            save_data = {'voice': media_id, 'caption': caption}
        else:
            save_data = {'media': media_id, 'caption': caption}
        
        if meta and meta.get('has_questions', False):
            await r.set(f'{m.from_user.id}:addPublicMediaData:{m.chat.id}{Dev_FINAL}', 
                        json.dumps(save_data))
            await r.set(f'{m.from_user.id}:addPublicMediaStep:{m.chat.id}{Dev_FINAL}', 'wait_answers')
            await m.reply(plugins_games_devgames_919(k, meta["type"], k))
            return True
        
        batch_key = f'{m.from_user.id}:addPublicMediaBatch:{m.chat.id}{Dev_FINAL}'
        batch_data = await r.get(batch_key)
        if batch_data:
            if isinstance(batch_data, bytes):
                batch_data = batch_data.decode('utf-8')
            batch = json.loads(batch_data)
        else:
            batch = []
        
        if 'voice' in save_data:
            batch.append({"voice": save_data['voice'], "answer": [], "caption": caption, "added_by": m.from_user.id})
        else:
            batch.append({"media": save_data['media'], "answer": [], "caption": caption, "added_by": m.from_user.id})
        
        await r.set(batch_key, json.dumps(batch), ex=300)
        
        game_data = await get_public_game_data(game_name)
        if not game_data:
            game_data = {"media": []}
        
        for item in batch:
            game_data["media"].append(item)
        
        await save_public_game_data(game_name, game_data)
        await r.delete(batch_key)
        
        await m.reply(plugins_games_devgames_948(k, len(batch), meta["type"], k, len(game_data["media"]), k, k))
        await r.set(f'{m.from_user.id}:addPublicMediaStep:{m.chat.id}{Dev_FINAL}', 'wait_photo')
        return True
    
    elif step == 'wait_answers':
        if text == 'تم':
            await r.delete(f'{m.from_user.id}:addPublicMediaStep:{m.chat.id}{Dev_FINAL}')
            await r.delete(f'{m.from_user.id}:addPublicMediaType:{m.chat.id}{Dev_FINAL}')
            await r.delete(f'{m.from_user.id}:addPublicMediaMeta:{m.chat.id}{Dev_FINAL}')
            await r.delete(f'{m.from_user.id}:addPublicMediaData:{m.chat.id}{Dev_FINAL}')
            await m.reply(plugins_games_devgames_958(k))
            return True
        
        if not text or text.strip() == '':
            await m.reply(plugins_games_devgames_962(k))
            return True
        
        answers = [a.strip() for a in text.strip().split('\n') if a.strip()]
        if not answers:
            await m.reply(plugins_games_devgames_967(k))
            return True
        
        data_raw = await r.get(f'{m.from_user.id}:addPublicMediaData:{m.chat.id}{Dev_FINAL}')
        if not data_raw:
            await m.reply(plugins_games_devgames_972(k))
            await r.delete(f'{m.from_user.id}:addPublicMediaStep:{m.chat.id}{Dev_FINAL}')
            await r.delete(f'{m.from_user.id}:addPublicMediaType:{m.chat.id}{Dev_FINAL}')
            return True
        
        if isinstance(data_raw, bytes):
            data_raw = data_raw.decode('utf-8')
        data = json.loads(data_raw)
        
        game_data = await get_public_game_data(game_name)
        if not game_data:
            game_data = {"media": []}
        
        if 'text' in data:
            game_data["media"].append({
                "text": data['text'],
                "answer": answers,
                "added_by": m.from_user.id
            })
        elif 'voice' in data:
            game_data["media"].append({
                "voice": data['voice'],
                "answer": answers,
                "caption": data.get('caption', ''),
                "added_by": m.from_user.id
            })
        else:
            game_data["media"].append({
                "media": data['media'],
                "answer": answers,
                "caption": data.get('caption', ''),
                "added_by": m.from_user.id
            })
        
        await save_public_game_data(game_name, game_data)
        
        await r.delete(f'{m.from_user.id}:addPublicMediaData:{m.chat.id}{Dev_FINAL}')
        await r.set(f'{m.from_user.id}:addPublicMediaStep:{m.chat.id}{Dev_FINAL}', 'wait_photo')
        
        await m.reply(plugins_games_devgames_1011(k, k, ", ".join(answers), k, len(game_data["media"]), k, k))
        return True
    
    return True



async def handle_add_public_game_step(c, m, k, text):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    step = await r.get(f'{m.from_user.id}:addPublicGameStep:{m.chat.id}{Dev_FINAL}')
    if isinstance(step, bytes):
        step = step.decode()
    
    if text == 'الغاء':
        await r.delete(f'{m.from_user.id}:addPublicGameStep:{m.chat.id}{Dev_FINAL}')
        await r.delete(f'{m.from_user.id}:addPublicGameMeta:{m.chat.id}{Dev_FINAL}')
        await r.delete(f'{m.from_user.id}:addPublicGameChannel:{m.chat.id}{Dev_FINAL}')
        await m.reply(plugins_games_devgames_1030(k))
        return True
    
    if step == 'wait_type' or step == 'wait_type_button':
        is_button = (step == 'wait_type_button')
        game_type = None
        for t in ['صور', 'نصوص', 'صوت', 'قيفات', 'فيديو']:
            if t in text:
                game_type = t
                break
        
        if not game_type:
            await m.reply(plugins_games_devgames_1042(k))
            return True
        
        if is_button:
            has_money = 'فلوس' in text
            await r.set(f'{m.from_user.id}:addPublicGameStep:{m.chat.id}{Dev_FINAL}', 'wait_name_button')
            await r.set(f'{m.from_user.id}:addPublicGameMeta:{m.chat.id}{Dev_FINAL}', 
                        json.dumps({'type': game_type, 'has_money': has_money, 'is_button': True}))
            has_m_text = 'مع فلوس' if has_money else 'بدون فلوس'
            await m.reply(plugins_games_devgames_1060(k, game_type, has_m_text, k))
            return True
        
        has_questions = 'اسئله' in text or 'اسئلة' in text
        has_money = 'فلوس' in text
        
        if has_money and not has_questions:
            await m.reply(plugins_games_devgames_1067(k, k))
            return True
        
        meta_data = {'type': game_type, 'has_questions': has_questions, 'has_money': has_money, 'is_button': False}
        await r.set(f'{m.from_user.id}:addPublicGameMeta:{m.chat.id}{Dev_FINAL}', json.dumps(meta_data))
        
        if not has_questions and not has_money and not is_button:
            await r.set(f'{m.from_user.id}:addPublicGameStep:{m.chat.id}{Dev_FINAL}', 'wait_add_method')
            await m.reply(plugins_games_devgames_1075(k, game_type, k))
            return True
        
        await r.set(f'{m.from_user.id}:addPublicGameStep:{m.chat.id}{Dev_FINAL}', 'wait_name')
        
        opts = []
        if has_questions:
            opts.append('اسئلة')
        if has_money:
            opts.append('فلوس')
        opts_text = ' + '.join(opts) if opts else 'بدون اسئلة وبدون فلوس'
        
        await m.reply(plugins_games_devgames_1093(k, game_type, opts_text, k))
        return True
    
    elif step == 'wait_add_method':
        meta_raw = await r.get(f'{m.from_user.id}:addPublicGameMeta:{m.chat.id}{Dev_FINAL}')
        if not meta_raw:
            await m.reply(plugins_games_devgames_1099(k))
            await r.delete(f'{m.from_user.id}:addPublicGameStep:{m.chat.id}{Dev_FINAL}')
            return True
        
        meta = json.loads(meta_raw.decode() if isinstance(meta_raw, bytes) else meta_raw)
        
        if text.strip() == '1' or text.strip() == '1' or 'فردي' in text:
            await r.set(f'{m.from_user.id}:addPublicGameStep:{m.chat.id}{Dev_FINAL}', 'wait_name')
            await m.reply(plugins_games_devgames_1107(k, k))
            return True
        
        elif text.strip() == '2' or text.strip() == '2' or 'قناة' in text:
            await r.set(f'{m.from_user.id}:addPublicGameStep:{m.chat.id}{Dev_FINAL}', 'wait_channel_username')
            await r.set(f'{m.from_user.id}:addPublicGameMeta:{m.chat.id}{Dev_FINAL}', json.dumps(meta))
            await m.reply(plugins_games_devgames_1113(k, k, k, k))
            return True
        
        else:
            await m.reply(plugins_games_devgames_1125(k, k))
            return True
    
    elif step == 'wait_channel_username':
        meta_raw = await r.get(f'{m.from_user.id}:addPublicGameMeta:{m.chat.id}{Dev_FINAL}')
        if not meta_raw:
            await m.reply(plugins_games_devgames_1137(k))
            await r.delete(f'{m.from_user.id}:addPublicGameStep:{m.chat.id}{Dev_FINAL}')
            return True
        
        meta = json.loads(meta_raw.decode() if isinstance(meta_raw, bytes) else meta_raw)
        
        link = text.strip()
        if not link:
            await m.reply(plugins_games_devgames_1145(k))
            return True
        
        chat_ref, start_message_id = parse_telegram_message_link(link)
        if chat_ref is None:
            await m.reply(plugins_games_devgames_1150(k, k))
            return True
        
        try:
            chat = await c.get_chat(chat_ref)
            if not chat:
                await m.reply(plugins_games_devgames_1161(k))
                return True
        except Exception as e:
            await m.reply(plugins_games_devgames_1164(k, k, e))
            return True
        
        await r.set(f'{m.from_user.id}:addPublicGameChannel:{m.chat.id}{Dev_FINAL}', json.dumps({"chat_ref": chat_ref, "start_id": start_message_id}))
        await r.set(f'{m.from_user.id}:addPublicGameStep:{m.chat.id}{Dev_FINAL}', 'wait_message_range')
        await r.set(f'{m.from_user.id}:addPublicGameMeta:{m.chat.id}{Dev_FINAL}', json.dumps(meta))
        
        await m.reply(plugins_games_devgames_1179(k, start_message_id, k, meta["type"]))
        return True
    
    elif step == 'wait_message_range':
        try:
            count = int(text.strip())
            if count < 1:
                raise ValueError("عدد غير صحيح")
            if count > 500:
                await m.reply(plugins_games_devgames_1194(k))
                return True
            
        except Exception as e:
            await m.reply(plugins_games_devgames_1198(k, k))
            return True
        
        meta_raw = await r.get(f'{m.from_user.id}:addPublicGameMeta:{m.chat.id}{Dev_FINAL}')
        if not meta_raw:
            await m.reply(plugins_games_devgames_1208(k))
            await r.delete(f'{m.from_user.id}:addPublicGameStep:{m.chat.id}{Dev_FINAL}')
            return True
        
        meta = json.loads(meta_raw.decode() if isinstance(meta_raw, bytes) else meta_raw)
        
        channel_ref_raw = await r.get(f'{m.from_user.id}:addPublicGameChannel:{m.chat.id}{Dev_FINAL}')
        if isinstance(channel_ref_raw, bytes):
            channel_ref_raw = channel_ref_raw.decode()
        
        if not channel_ref_raw:
            await m.reply(plugins_games_devgames_1219(k))
            await r.delete(f'{m.from_user.id}:addPublicGameStep:{m.chat.id}{Dev_FINAL}')
            return True
        
        channel_ref_data = json.loads(channel_ref_raw)
        chat_ref = channel_ref_data["chat_ref"]
        start_message_id = channel_ref_data["start_id"]
        
        temp_name = f"temp_game_{m.from_user.id}_{int(time.time())}"
        meta['temp_name'] = temp_name
        
        await m.reply(plugins_games_devgames_1230(k, count, meta["type"], start_message_id))
        
        success, message = await save_media_from_channel_by_message_link(
            c, m, temp_name, chat_ref, start_message_id, count, meta
        )
        
        if success:
            await r.set(f'{m.from_user.id}:addPublicGameStep:{m.chat.id}{Dev_FINAL}', 'wait_name_from_channel')
            await r.set(f'{m.from_user.id}:addPublicGameMeta:{m.chat.id}{Dev_FINAL}', json.dumps(meta))
            await m.reply(plugins_games_devgames_1239(message, k))
        else:
            await m.reply(plugins_games_devgames_1246(message))
            await r.delete(f'{m.from_user.id}:addPublicGameStep:{m.chat.id}{Dev_FINAL}')
            await r.delete(f'{m.from_user.id}:addPublicGameMeta:{m.chat.id}{Dev_FINAL}')
            await r.delete(f'{m.from_user.id}:addPublicGameChannel:{m.chat.id}{Dev_FINAL}')
        
        return True
    
    elif step == 'wait_name_from_channel':
        if not text or text.strip() == '':
            await m.reply(plugins_games_devgames_1255(k))
            return True
        
        game_name = text.strip()
        
        if await get_public_game_meta(game_name):
            await m.reply(plugins_games_devgames_1261(k, k))
            return True
        
        if await get_public_button_game_data(game_name):
            await m.reply(plugins_games_devgames_1265(k, k))
            return True
        
        meta_raw = await r.get(f'{m.from_user.id}:addPublicGameMeta:{m.chat.id}{Dev_FINAL}')
        if not meta_raw:
            await m.reply(plugins_games_devgames_1270(k))
            await r.delete(f'{m.from_user.id}:addPublicGameStep:{m.chat.id}{Dev_FINAL}')
            return True
        
        meta = json.loads(meta_raw.decode() if isinstance(meta_raw, bytes) else meta_raw)
        temp_name = meta.get('temp_name')
        
        if temp_name:
            temp_data = await get_public_game_data(temp_name)
            if temp_data:
                await save_public_game_data(game_name, temp_data)
                await delete_public_game_data(temp_name)
        
        meta['name'] = game_name
        await save_public_game_meta(game_name, meta)
        
        await r.delete(f'{m.from_user.id}:addPublicGameStep:{m.chat.id}{Dev_FINAL}')
        await r.delete(f'{m.from_user.id}:addPublicGameMeta:{m.chat.id}{Dev_FINAL}')
        await r.delete(f'{m.from_user.id}:addPublicGameChannel:{m.chat.id}{Dev_FINAL}')
        
        has_q = 'مع اسئلة' if meta.get('has_questions', False) else 'بدون اسئلة'
        has_m = 'مع فلوس' if meta.get('has_money', False) else 'بدون فلوس'
        
        await m.reply(plugins_games_devgames_1293(k, k, game_name, k, meta['type'], k, has_q, k, has_m, k, k, k, game_name, k, game_name, k, game_name, k, game_name, k, game_name))
        return True
    
    elif step == 'wait_name' or step == 'wait_name_button':
        if not text or text.strip() == '':
            await m.reply(plugins_games_devgames_1311(k))
            return True
        
        game_name = text.strip()
        
        if await get_public_game_meta(game_name):
            await m.reply(plugins_games_devgames_1317(k, k))
            return True
        
        if await get_public_button_game_data(game_name):
            await m.reply(plugins_games_devgames_1321(k, k))
            return True
        
        meta_raw = await r.get(f'{m.from_user.id}:addPublicGameMeta:{m.chat.id}{Dev_FINAL}')
        if not meta_raw:
            await m.reply(plugins_games_devgames_1326(k))
            await r.delete(f'{m.from_user.id}:addPublicGameStep:{m.chat.id}{Dev_FINAL}')
            return True
        
        meta = json.loads(meta_raw.decode() if isinstance(meta_raw, bytes) else meta_raw)
        meta['name'] = game_name
        
        if meta.get('is_button', False):
            await save_public_button_game_data(game_name, {"type": meta['type'], "has_money": meta['has_money'], "questions": []})
            await r.delete(f'{m.from_user.id}:addPublicGameStep:{m.chat.id}{Dev_FINAL}')
            await r.delete(f'{m.from_user.id}:addPublicGameMeta:{m.chat.id}{Dev_FINAL}')
            has_m = 'مع فلوس' if meta['has_money'] else 'بدون فلوس'
            await m.reply(plugins_games_devgames_1338(k, k, game_name, k, meta['type'], k, has_m, k, k, game_name, k, game_name, k, game_name, k, game_name, k, game_name))
            return True
        
        await r.set(f'{m.from_user.id}:addPublicGameMeta:{m.chat.id}{Dev_FINAL}', json.dumps(meta))
        
        if meta['has_questions'] and meta['type'] not in ('نصوص', 'صور'):
            await r.set(f'{m.from_user.id}:addPublicGameStep:{m.chat.id}{Dev_FINAL}', 'wait_caption')
            await m.reply(plugins_games_devgames_1356(k))
        else:
            await save_public_game_meta(game_name, meta)
            await save_public_game_data(game_name, {"media": []})
            await r.delete(f'{m.from_user.id}:addPublicGameStep:{m.chat.id}{Dev_FINAL}')
            await r.delete(f'{m.from_user.id}:addPublicGameMeta:{m.chat.id}{Dev_FINAL}')
            has_q = 'مع اسئلة' if meta['has_questions'] else 'بدون اسئلة'
            has_m = 'مع فلوس' if meta['has_money'] else 'بدون فلوس'
            await m.reply(plugins_games_devgames_1364(k, k, game_name, k, meta['type'], k, has_q, k, has_m, k, k, game_name, k, game_name, k, game_name, k, game_name, k, game_name))
        return True
    
    elif step == 'wait_caption':
        if not text or text.strip() == '':
            await m.reply(plugins_games_devgames_1381(k))
            return True
        
        meta_raw = await r.get(f'{m.from_user.id}:addPublicGameMeta:{m.chat.id}{Dev_FINAL}')
        if not meta_raw:
            await m.reply(plugins_games_devgames_1386(k))
            await r.delete(f'{m.from_user.id}:addPublicGameStep:{m.chat.id}{Dev_FINAL}')
            return True
        
        meta = json.loads(meta_raw.decode() if isinstance(meta_raw, bytes) else meta_raw)
        meta['caption'] = text.strip()
        game_name = meta['name']
        
        await save_public_game_meta(game_name, meta)
        await save_public_game_data(game_name, {"media": []})
        await r.delete(f'{m.from_user.id}:addPublicGameStep:{m.chat.id}{Dev_FINAL}')
        await r.delete(f'{m.from_user.id}:addPublicGameMeta:{m.chat.id}{Dev_FINAL}')
        
        has_q = 'مع اسئلة' if meta['has_questions'] else 'بدون اسئلة'
        has_m = 'مع فلوس' if meta['has_money'] else 'بدون فلوس'
        
        await m.reply(plugins_games_devgames_1402(k, k, game_name, k, meta['type'], k, has_q, k, has_m, k, meta['caption'], k, k, game_name, k, game_name, k, game_name, k, game_name, k, game_name))
        return True
    
    return True

async def handle_add_public_button_step(c, m, k, text):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    step = await r.get(f'{m.from_user.id}:addPublicButtonStep:{m.chat.id}{Dev_FINAL}')
    if isinstance(step, bytes):
        step = step.decode()
    
    game_name = await r.get(f'{m.from_user.id}:addPublicButtonType:{m.chat.id}{Dev_FINAL}')
    if isinstance(game_name, bytes):
        game_name = game_name.decode()
    
    game_data = await get_public_button_game_data(game_name)
    if not game_data:
        await m.reply(plugins_games_devgames_1434(k))
        await r.delete(f'{m.from_user.id}:addPublicButtonStep:{m.chat.id}{Dev_FINAL}')
        return True
    
    if text == 'الغاء':
        await r.delete(f'{m.from_user.id}:addPublicButtonStep:{m.chat.id}{Dev_FINAL}')
        await r.delete(f'{m.from_user.id}:addPublicButtonType:{m.chat.id}{Dev_FINAL}')
        await r.delete(f'{m.from_user.id}:addPublicButtonData:{m.chat.id}{Dev_FINAL}')
        await m.reply(plugins_games_devgames_1442(k))
        return True
    
    if text == 'تم':
        await r.delete(f'{m.from_user.id}:addPublicButtonStep:{m.chat.id}{Dev_FINAL}')
        await r.delete(f'{m.from_user.id}:addPublicButtonType:{m.chat.id}{Dev_FINAL}')
        await r.delete(f'{m.from_user.id}:addPublicButtonData:{m.chat.id}{Dev_FINAL}')
        await m.reply(plugins_games_devgames_1449(k))
        return True
    
    if step == 'wait_media':
        question = text.strip()
        if not question:
            await m.reply(plugins_games_devgames_1455(k))
            return True
        
        await r.set(f'{m.from_user.id}:addPublicButtonData:{m.chat.id}{Dev_FINAL}', json.dumps({'question': question}))
        
        if game_data['type'] != 'نصوص':
            await r.set(f'{m.from_user.id}:addPublicButtonStep:{m.chat.id}{Dev_FINAL}', 'wait_media_file')
            await m.reply(plugins_games_devgames_1462(k, game_data["type"]))
        else:
            await r.set(f'{m.from_user.id}:addPublicButtonStep:{m.chat.id}{Dev_FINAL}', 'wait_answers')
            await m.reply(plugins_games_devgames_1465(k, k, k))
        return True
    
    elif step == 'wait_media_file':
        media_id = None
        if game_data['type'] == 'صور' and m.photo:
            media_id = m.photo.file_id
        elif game_data['type'] == 'فيديو' and m.video:
            media_id = m.video.file_id
        elif game_data['type'] == 'صوت' and m.audio:
            media_id = m.audio.file_id
        elif game_data['type'] == 'قيفات' and m.animation:
            media_id = m.animation.file_id
        else:
            await m.reply(plugins_games_devgames_1479(k, game_data["type"]))
            return True
        
        data_raw = await r.get(f'{m.from_user.id}:addPublicButtonData:{m.chat.id}{Dev_FINAL}')
        if data_raw:
            data = json.loads(data_raw.decode() if isinstance(data_raw, bytes) else data_raw)
        else:
            data = {}
        
        if 'question' not in data:
            caption = m.html if m.caption else ''
            if not caption or not caption.strip():
                await m.reply(plugins_games_devgames_1491(k, game_data["type"]))
                return True
            data['question'] = caption.strip()
        
        data['media'] = media_id
        await r.set(f'{m.from_user.id}:addPublicButtonData:{m.chat.id}{Dev_FINAL}', json.dumps(data))
        
        await r.set(f'{m.from_user.id}:addPublicButtonStep:{m.chat.id}{Dev_FINAL}', 'wait_answers')
        await m.reply(plugins_games_devgames_1499(k, game_data["type"], k))
        return True
    
    elif step == 'wait_answers':
        lines = [line.strip() for line in text.strip().split('\n') if line.strip()]
        if len(lines) < 4:
            await m.reply(plugins_games_devgames_1505(k))
            return True
        
        wrong_answers = lines[:3]
        correct_answer = lines[3]
        
        data_raw = await r.get(f'{m.from_user.id}:addPublicButtonData:{m.chat.id}{Dev_FINAL}')
        if data_raw:
            data = json.loads(data_raw.decode() if isinstance(data_raw, bytes) else data_raw)
        else:
            data = {'question': ''}
        
        question_item = {
            'question': data.get('question', ''),
            'wrong_answers': wrong_answers,
            'correct_answer': correct_answer,
            'added_by': m.from_user.id
        }
        
        if 'media' in data:
            question_item['media'] = data['media']
        
        game_data['questions'].append(question_item)
        await save_public_button_game_data(game_name, game_data)
        
        await r.delete(f'{m.from_user.id}:addPublicButtonData:{m.chat.id}{Dev_FINAL}')
        await r.set(f'{m.from_user.id}:addPublicButtonStep:{m.chat.id}{Dev_FINAL}', 'wait_media')
        
        await m.reply(plugins_games_devgames_1533(k, k, data.get("question", ""), k, correct_answer, k, len(game_data["questions"]), k, k))
        return True
    
    return True

async def handle_delete_public_media(c, m, k, game_name):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    game_data = await get_public_game_data(game_name)
    if not game_data or not game_data.get("media"):
        return await m.reply(plugins_games_devgames_1544(k, game_name))
    
    media_list = game_data["media"]
    is_admin = await is_public_game_admin(m.from_user.id)
    
    if not is_admin:
        filtered_list = [item for item in media_list if item.get('added_by', 0) == m.from_user.id]
    else:
        filtered_list = media_list
    
    if not filtered_list:
        return await m.reply(plugins_games_devgames_1555(k))
    
    txt = f'{k} قائمة محتوى {game_name}:\n'
    i = 1
    for item in filtered_list:
        if 'text' in item:
            text_preview = item["text"][:50] + ("..." if len(item["text"]) > 50 else "")
            line = f'{i} - {text_preview}\n'
            if len(txt) + len(line) > 4000:
                await m.reply(txt)
                txt = f'{k} قائمة محتوى {game_name} (مكمل):\n'
            txt += line
        elif 'media' in item or 'voice' in item:
            answers = item.get('answer', [])
            caption = item.get('caption', '')
            media_type = 'صورة' if 'media' in item else 'صوت' if 'voice' in item else 'ميديا'
            if answers:
                line = f'{i} - {media_type} | الاجابات: {", ".join(answers[:3])}{"..." if len(answers) > 3 else ""}\n'
            else:
                line = f'{i} - {media_type}\n'
            if len(txt) + len(line) > 4000:
                await m.reply(txt)
                txt = f'{k} قائمة محتوى {game_name} (مكمل):\n'
            txt += line
            if caption:
                line = f' {caption[:30]}{"..." if len(caption) > 30 else ""}\n'
                if len(txt) + len(line) > 4000:
                    await m.reply(txt)
                    txt = f'{k} قائمة محتوى {game_name} (مكمل):\n'
                txt += line
        i += 1
    
    txt += f'{k} ارسل رقم المحتوى الذي تريد حذفه\nللالغاء اكتب الغاء'
    await m.reply(txt)
    
    await r.set(f'{m.from_user.id}:deletePublicFilteredList:{m.chat.id}{Dev_FINAL}', json.dumps(filtered_list), ex=300)
    await r.set(f'{m.from_user.id}:deletePublicMediaStep:{m.chat.id}{Dev_FINAL}', 'wait_number')
    await r.set(f'{m.from_user.id}:deletePublicMediaType:{m.chat.id}{Dev_FINAL}', game_name)
    return True

async def handle_delete_public_button_media(c, m, k, game_name):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    game_data = await get_public_button_game_data(game_name)
    if not game_data or not game_data.get("questions"):
        return await m.reply(plugins_games_devgames_1601(k, game_name))
    
    questions_list = game_data["questions"]
    is_admin = await is_public_game_admin(m.from_user.id)
    
    if not is_admin:
        filtered_list = [item for item in questions_list if item.get('added_by', 0) == m.from_user.id]
    else:
        filtered_list = questions_list
    
    if not filtered_list:
        return await m.reply(plugins_games_devgames_1612(k))
    
    txt = f'{k} قائمة محتوى {game_name} (ازرار):\n'
    i = 1
    for item in filtered_list:
        q = item.get('question', '')
        correct = item.get('correct_answer', '')
        line = f'{i} - {q[:50]}{"..." if len(q) > 50 else ""}\n'
        if len(txt) + len(line) > 4000:
            await m.reply(txt)
            txt = f'{k} قائمة محتوى {game_name} (مكمل):\n'
        txt += line
        line = f'✓ {correct}\n'
        if len(txt) + len(line) > 4000:
            await m.reply(txt)
            txt = f'{k} قائمة محتوى {game_name} (مكمل):\n'
        txt += line
        i += 1
    
    txt += f'{k} ارسل رقم السؤال الذي تريد حذفه\nللالغاء اكتب الغاء'
    await m.reply(txt)
    
    await r.set(f'{m.from_user.id}:deletePublicFilteredList:{m.chat.id}{Dev_FINAL}', json.dumps(filtered_list), ex=300)
    await r.set(f'{m.from_user.id}:deletePublicMediaStep:{m.chat.id}{Dev_FINAL}', 'wait_number')
    await r.set(f'{m.from_user.id}:deletePublicMediaType:{m.chat.id}{Dev_FINAL}', game_name)
    return True

async def handle_delete_public_media_step(c, m, k, text):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if text == 'الغاء':
        await r.delete(f'{m.from_user.id}:deletePublicMediaStep:{m.chat.id}{Dev_FINAL}')
        await r.delete(f'{m.from_user.id}:deletePublicMediaType:{m.chat.id}{Dev_FINAL}')
        await r.delete(f'{m.from_user.id}:deletePublicFilteredList:{m.chat.id}{Dev_FINAL}')
        await m.reply(plugins_games_devgames_1647(k))
        return True
    
    game_name = await r.get(f'{m.from_user.id}:deletePublicMediaType:{m.chat.id}{Dev_FINAL}')
    if isinstance(game_name, bytes):
        game_name = game_name.decode()
    
    try:
        index = int(text.strip()) - 1
    except:
        await m.reply(plugins_games_devgames_1657(k))
        return True
    
    filtered_list_raw = await r.get(f'{m.from_user.id}:deletePublicFilteredList:{m.chat.id}{Dev_FINAL}')
    if not filtered_list_raw:
        await m.reply(plugins_games_devgames_1662(k))
        return True
    
    filtered_list = json.loads(filtered_list_raw.decode() if isinstance(filtered_list_raw, bytes) else filtered_list_raw)
    
    if index < 0 or index >= len(filtered_list):
        await m.reply(plugins_games_devgames_1668(k))
        return True
    
    deleted_item = filtered_list[index]
    
    game_data = await get_public_game_data(game_name)
    if game_data and game_data.get("media"):
        original_list = game_data["media"]
        for i, item in enumerate(original_list):
            if 'text' in item and 'text' in deleted_item and item['text'] == deleted_item['text']:
                original_list.pop(i)
                break
            elif 'media' in item and 'media' in deleted_item and item.get('media') == deleted_item.get('media'):
                original_list.pop(i)
                break
            elif 'voice' in item and 'voice' in deleted_item and item.get('voice') == deleted_item.get('voice'):
                original_list.pop(i)
                break
        
        await save_public_game_data(game_name, game_data)
        
        answers = deleted_item.get('answer', [])
        if answers:
            await m.reply(plugins_games_devgames_1691(k, k, ", ".join(answers), k, len(game_data["media"])))
        else:
            await m.reply(plugins_games_devgames_1693(k, k, len(game_data["media"])))
        
        await r.delete(f'{m.from_user.id}:deletePublicMediaStep:{m.chat.id}{Dev_FINAL}')
        await r.delete(f'{m.from_user.id}:deletePublicMediaType:{m.chat.id}{Dev_FINAL}')
        await r.delete(f'{m.from_user.id}:deletePublicFilteredList:{m.chat.id}{Dev_FINAL}')
        return True
    
    btn_data = await get_public_button_game_data(game_name)
    if btn_data and btn_data.get("questions"):
        original_list = btn_data["questions"]
        for i, item in enumerate(original_list):
            if item.get('question') == deleted_item.get('question'):
                original_list.pop(i)
                break
        
        await save_public_button_game_data(game_name, btn_data)
        await m.reply(plugins_games_devgames_1709(k, k, deleted_item.get("question", ""), k, len(btn_data["questions"])))
        
        await r.delete(f'{m.from_user.id}:deletePublicMediaStep:{m.chat.id}{Dev_FINAL}')
        await r.delete(f'{m.from_user.id}:deletePublicMediaType:{m.chat.id}{Dev_FINAL}')
        await r.delete(f'{m.from_user.id}:deletePublicFilteredList:{m.chat.id}{Dev_FINAL}')
        return True
    
    await m.reply(plugins_games_devgames_1716(k, game_name))
    await r.delete(f'{m.from_user.id}:deletePublicMediaStep:{m.chat.id}{Dev_FINAL}')
    await r.delete(f'{m.from_user.id}:deletePublicMediaType:{m.chat.id}{Dev_FINAL}')
    await r.delete(f'{m.from_user.id}:deletePublicFilteredList:{m.chat.id}{Dev_FINAL}')
    return True

async def handle_delete_public_game_step(c, m, k, text):
    """حذف لعبة عامة كاملة من رقمها (بعد أمر 'مسح لعبه عام') - Aec فقط"""
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()

    if text == 'الغاء':
        await r.delete(f'{m.from_user.id}:deletePublicGameStep:{m.chat.id}{Dev_FINAL}')
        await m.reply(plugins_games_devgames_1730(k))
        return True

    if not await is_public_game_admin(m.from_user.id):
        await r.delete(f'{m.from_user.id}:deletePublicGameStep:{m.chat.id}{Dev_FINAL}')
        return await m.reply(plugins_games_devgames_1735(k))

    try:
        index = int(text.strip()) - 1
    except Exception:
        await m.reply(plugins_games_devgames_1740(k))
        return True

    games = await get_all_public_games()
    button_games = await get_public_button_games()
    combined = [{'name': g['name'], 'is_button': False} for g in games] + \
               [{'name': g['name'], 'is_button': True} for g in button_games]

    if index < 0 or index >= len(combined):
        await m.reply(plugins_games_devgames_1749(k))
        return True

    chosen = combined[index]
    game_name = chosen['name']

    if chosen['is_button']:
        await delete_public_button_game_data(game_name)
    else:
        await delete_public_game_meta(game_name)
        await delete_public_game_data(game_name)

    await r.delete(f'{m.from_user.id}:deletePublicGameStep:{m.chat.id}{Dev_FINAL}')
    await m.reply(plugins_games_devgames_1762(k, game_name))
    return True

async def handle_list_public_media(c, m, k, game_name):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    meta = await get_public_game_meta(game_name)
    game_data = await get_public_game_data(game_name)
    
    if not game_data or not game_data.get("media"):
        return await m.reply(plugins_games_devgames_1773(k, game_name))
    
    media_list = game_data["media"]
    txt = f'{k} قائمة محتوى {game_name}:\n'
    txt += f'{k} النوع: {meta["type"]}\n'
    txt += f'{k} عدد المحتوى: {len(media_list)}\n\n'
    
    for i, item in enumerate(media_list, 1):
        if 'text' in item:
            text_preview = item["text"][:50] + ("..." if len(item["text"]) > 50 else "")
            txt += f'{i} - {text_preview}\n'
        elif 'media' in item or 'voice' in item:
            answers = item.get('answer', [])
            caption = item.get('caption', '')
            media_type = 'صورة' if 'media' in item else 'صوت' if 'voice' in item else 'ميديا'
            if answers:
                txt += f'{i} - {media_type} | الاجابات: {", ".join(answers[:3])}{"..." if len(answers) > 3 else ""}\n'
            else:
                txt += f'{i} - {media_type}\n'
            if caption:
                txt += f'{k} {caption[:30]}{"..." if len(caption) > 30 else ""}\n'
        txt += '\n'
    
    await m.reply(txt)
    return True

async def handle_list_public_button_media(c, m, k, game_name):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    game_data = await get_public_button_game_data(game_name)
    if not game_data or not game_data.get("questions"):
        return await m.reply(plugins_games_devgames_1805(k, game_name))
    
    questions_list = game_data["questions"]
    txt = f'{k} قائمة محتوى {game_name} (ازرار):\n'
    txt += f'{k} النوع: {game_data["type"]}\n'
    txt += f'{k} عدد الاسئلة: {len(questions_list)}\n\n'
    
    for i, item in enumerate(questions_list, 1):
        q = item.get('question', '')
        correct = item.get('correct_answer', '')
        txt += f'{i} - {q[:50]}{"..." if len(q) > 50 else ""}\n'
        txt += f'    ✓ {correct}\n'
        txt += '\n'
    
    await m.reply(txt)
    return True


@Client.on_callback_query(filters.regex(r"^(public_change_|public_|public_button_ans_|dg_)"), group=-43732)
async def public_game_callback(c, callback_query):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    data = callback_query.data
    k = await r.get(f'{Dev_FINAL}:botkey') or '•'
    
    if data.startswith('public_change_'):
        parts = data.split('_')
        game_name = parts[2]
        next_index = int(parts[3])
        user_id = int(parts[4])
        
        if callback_query.from_user.id != user_id:
            return await callback_query.answer(REPLIES['plugins_games_addgame_1700'], show_alert=True)
        
        meta = await get_public_game_meta(game_name)
        game_data = await get_public_game_data(game_name)
        
        if not game_data or not game_data.get("media"):
            return await callback_query.answer(REPLIES['plugins_games_addgame_1706'], show_alert=True)
        
        media_list = game_data["media"]
        total = len(media_list)
        
        if next_index >= total:
            next_index = 0
        
        item = media_list[next_index]
        
        if 'media' not in item and 'voice' not in item and 'text' not in item:
            return await callback_query.answer(REPLIES['plugins_games_addgame_1717'], show_alert=True)
        
        current_index_key = f'{callback_query.message.chat.id}:public_game_index:{game_name}:{user_id}'
        await r.set(current_index_key, next_index, ex=3600)
        
        new_next = (next_index + 1) % total
        caption_text = f'ㅤㅤㅤㅤㅤ 『 {next_index + 1} 』ㅤㅤㅤㅤㅤ'
        
        if 'voice' in item:
            if meta['type'] == 'صوت':
                change_btn = InlineKeyboardButton("تغيير", callback_data=f"public_change_{game_name}_{new_next}_{user_id}")
                reply_markup = InlineKeyboardMarkup([[change_btn]])
                try:
                    await callback_query.message.reply_voice(item['voice'], caption=caption_text, reply_markup=reply_markup)
                except Exception as e:
                    await callback_query.answer(plugins_games_devgames_1870(str(e)[:50]), show_alert=True)
                    return
                await callback_query.message.delete()
                await callback_query.answer()
                return
        
        change_btn = InlineKeyboardButton("تغيير", callback_data=f"public_change_{game_name}_{new_next}_{user_id}")
        reply_markup = InlineKeyboardMarkup([[change_btn]])
        
        try:
            if meta['type'] == 'صور':
                if 'media' in item:
                    await callback_query.edit_message_media(
                        InputMediaPhoto(item['media'], caption=caption_text),
                        reply_markup=reply_markup
                    )
                elif 'text' in item:
                    await callback_query.edit_message_text(
                        plugins_games_devgames_1887(caption_text, item['text']),
                        reply_markup=reply_markup
                    )
            
            elif meta['type'] == 'فيديو':
                if 'media' in item:
                    await callback_query.edit_message_media(
                        InputMediaVideo(item['media'], caption=caption_text),
                        reply_markup=reply_markup
                    )
            
            elif meta['type'] == 'صوت':
                if 'media' in item:
                    await callback_query.edit_message_media(
                        InputMediaAudio(item['media'], caption=caption_text),
                        reply_markup=reply_markup
                    )
            
            elif meta['type'] == 'قيفات':
                if 'media' in item:
                    await callback_query.edit_message_media(
                        InputMediaAnimation(item['media'], caption=caption_text),
                        reply_markup=reply_markup
                    )
            
            elif meta['type'] == 'نصوص':
                if 'text' in item:
                    await callback_query.edit_message_text(
                        plugins_games_devgames_1915(caption_text, item['text']),
                        reply_markup=reply_markup
                    )
        
        except Exception as e:
            error_msg = str(e)
            if 'MEDIA_EMPTY' in error_msg or 'MEDIA_PREV_INVALID' in error_msg or 'Invalid media' in error_msg:
                try:
                    await callback_query.message.delete()
                except:
                    pass
                
                if meta['type'] == 'صور':
                    if 'media' in item:
                        await callback_query.message.reply_photo(item['media'], caption=caption_text, reply_markup=reply_markup)
                    elif 'text' in item:
                        await callback_query.message.reply(plugins_games_devgames_1932(caption_text, item['text']), reply_markup=reply_markup)
                
                elif meta['type'] == 'فيديو':
                    if 'media' in item:
                        await callback_query.message.reply_video(item['media'], caption=caption_text, reply_markup=reply_markup)
                
                elif meta['type'] == 'صوت':
                    if 'media' in item:
                        await callback_query.message.reply_audio(item['media'], caption=caption_text, reply_markup=reply_markup)
                
                elif meta['type'] == 'قيفات':
                    if 'media' in item:
                        await callback_query.message.reply_animation(item['media'], caption=caption_text, reply_markup=reply_markup)
                
                elif meta['type'] == 'نصوص':
                    if 'text' in item:
                        await callback_query.message.reply(plugins_games_devgames_1948(caption_text, item['text']), reply_markup=reply_markup)
            else:
                await callback_query.answer(plugins_games_devgames_1950(error_msg[:50]), show_alert=True)
                return
        
        await callback_query.answer()
    
    elif data.startswith('public_button_ans_'):
        parts = data.split('_')
        game_name = parts[3]
        question_index = int(parts[4])
        button_index = int(parts[5])
        is_correct = parts[6] == 'True'
        user_id = callback_query.from_user.id
        
        game_data = await get_public_button_game_data(game_name)
        if not game_data or not game_data.get("questions"):
            return await callback_query.answer(REPLIES['plugins_games_addgame_1706'], show_alert=True)
        
        questions_list = game_data["questions"]
        if question_index >= len(questions_list):
            return await callback_query.answer(REPLIES['plugins_games_addgame_1831'], show_alert=True)
        
        item = questions_list[question_index]
        question = item.get('question', '')
        chat_id = callback_query.message.chat.id
        
        if is_correct:
            has_money = bool(game_data.get('has_money', False))
            
            if has_money:
                ra = random.randint(1, 5)
                if await shared_r.get(f'{user_id}:Floos'):
                    get_raw = await shared_r.get(f'{user_id}:Floos')
                    if isinstance(get_raw, bytes):
                        get = int(get_raw.decode('utf-8'))
                    else:
                        get = int(get_raw)
                    await shared_r.set(f'{user_id}:Floos', get + ra)
                    await enforce_balance_cap(shared_r, callback_query.message, k, user_id)
                    floos_raw = await shared_r.get(f'{user_id}:Floos')
                    if isinstance(floos_raw, bytes):
                        floos = int(floos_raw.decode('utf-8'))
                    else:
                        floos = int(floos_raw)
                else:
                    floos = ra
                    await shared_r.set(f'{user_id}:Floos', ra)
                    await enforce_balance_cap(shared_r, callback_query.message, k, user_id)
                await add_game_earnings(user_id, chat_id, ra, callback_query.id)
                await callback_query.edit_message_text(
                    plugins_games_devgames_1998(question, k, ra, k, floos)
                )
            else:
                await callback_query.edit_message_text(
                    plugins_games_devgames_2002(question, k)
                )
        else:
            correct_answer = item.get('correct_answer', '')
            await callback_query.edit_message_text(
                plugins_games_devgames_2007(question, correct_answer)
            )
        
        await callback_query.answer()