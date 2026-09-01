from helpers.context import get_global_r, get_global_dev, get_global_k
from helpers.context import get_current_bot_id
import html
r = get_global_r()
Dev_FINAL = get_global_dev()
k = get_global_k()
from .utils import add_game_earnings, enforce_balance_cap
from compat import Client
import random, asyncio, json, urllib.parse, time
from helpers.games import is_game_disabled_in_chat, set_game_disabled_in_chat
from helpers.redis import r as shared_r
from compat import *
from compat import *
from helpers.ranks import *
from helpers.games import *
from compat import Client
from .devgames import (
    get_public_game_meta,
    get_public_game_data,
    get_public_button_game_data,
    get_all_public_games,
    get_public_button_games,
    delete_public_game_data,
    delete_public_game_meta,
    delete_public_button_game_data,
    is_public_game_admin,
    save_public_game_data,
    save_public_button_game_data
)
from helpers.replies_store import (
    REPLIES,
    plugins_games_addgame_1020,
    plugins_games_addgame_1039,
    plugins_games_addgame_1045,
    plugins_games_addgame_1053,
    plugins_games_addgame_1069,
    plugins_games_addgame_1077,
    plugins_games_addgame_1086,
    plugins_games_addgame_1093,
    plugins_games_addgame_1106,
    plugins_games_addgame_1111,
    plugins_games_addgame_1117,
    plugins_games_addgame_1133,
    plugins_games_addgame_1162,
    plugins_games_addgame_1172,
    plugins_games_addgame_1176,
    plugins_games_addgame_1181,
    plugins_games_addgame_1186,
    plugins_games_addgame_1222,
    plugins_games_addgame_1313,
    plugins_games_addgame_1325,
    plugins_games_addgame_1357,
    plugins_games_addgame_1380,
    plugins_games_addgame_1414,
    plugins_games_addgame_1440,
    plugins_games_addgame_1445,
    plugins_games_addgame_1456,
    plugins_games_addgame_1462,
    plugins_games_addgame_1468,
    plugins_games_addgame_1470,
    plugins_games_addgame_1478,
    plugins_games_addgame_1482,
    plugins_games_addgame_1487,
    plugins_games_addgame_1498,
    plugins_games_addgame_1509,
    plugins_games_addgame_1555,
    plugins_games_addgame_1566,
    plugins_games_addgame_1601,
    plugins_games_addgame_1606,
    plugins_games_addgame_1617,
    plugins_games_addgame_1622,
    plugins_games_addgame_1631,
    plugins_games_addgame_1654,
    plugins_games_addgame_1656,
    plugins_games_addgame_1672,
    plugins_games_addgame_1679,
    plugins_games_addgame_1732,
    plugins_games_addgame_1749,
    plugins_games_addgame_1777,
    plugins_games_addgame_1794,
    plugins_games_addgame_181,
    plugins_games_addgame_1810,
    plugins_games_addgame_1812,
    plugins_games_addgame_200,
    plugins_games_addgame_202,
    plugins_games_addgame_226,
    plugins_games_addgame_228,
    plugins_games_addgame_254,
    plugins_games_addgame_301,
    plugins_games_addgame_353,
    plugins_games_addgame_357,
    plugins_games_addgame_362,
    plugins_games_addgame_366,
    plugins_games_addgame_369,
    plugins_games_addgame_377,
    plugins_games_addgame_381,
    plugins_games_addgame_386,
    plugins_games_addgame_394,
    plugins_games_addgame_398,
    plugins_games_addgame_401,
    plugins_games_addgame_406,
    plugins_games_addgame_414,
    plugins_games_addgame_418,
    plugins_games_addgame_421,
    plugins_games_addgame_450,
    plugins_games_addgame_494,
    plugins_games_addgame_523,
    plugins_games_addgame_565,
    plugins_games_addgame_578,
    plugins_games_addgame_597,
    plugins_games_addgame_609,
    plugins_games_addgame_629,
    plugins_games_addgame_636,
    plugins_games_addgame_650,
    plugins_games_addgame_655,
    plugins_games_addgame_661,
    plugins_games_addgame_665,
    plugins_games_addgame_669,
    plugins_games_addgame_673,
    plugins_games_addgame_677,
    plugins_games_addgame_682,
    plugins_games_addgame_696,
    plugins_games_addgame_714,
    plugins_games_addgame_722,
    plugins_games_addgame_739,
    plugins_games_addgame_744,
    plugins_games_addgame_762,
    plugins_games_addgame_794,
    plugins_games_addgame_803,
    plugins_games_addgame_811,
    plugins_games_addgame_818,
    plugins_games_addgame_824,
    plugins_games_addgame_831,
    plugins_games_addgame_834,
    plugins_games_addgame_848,
    plugins_games_addgame_862,
    plugins_games_addgame_870,
    plugins_games_addgame_876,
    plugins_games_addgame_905,
    plugins_games_addgame_916,
    plugins_games_addgame_922,
    plugins_games_addgame_941,
    plugins_games_addgame_949,
    plugins_games_addgame_955,
    plugins_games_addgame_963,
    plugins_games_addgame_969,
    plugins_games_addgame_977,
    plugins_games_addgame_982,
)

CUSTOM_GAMES_KEY = f"{Dev_FINAL}:custom_games"
CUSTOM_GAMES_META_KEY = f"{Dev_FINAL}:custom_games_meta"
CUSTOM_BUTTON_GAMES_KEY = f"{Dev_FINAL}:custom_button_games"

async def get_custom_game_data(game_name):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if not game_name:
        return None
    game = await r.hget(CUSTOM_GAMES_KEY, game_name)
    if game:
        if isinstance(game, bytes):
            game = game.decode('utf-8')
        return json.loads(game)
    return None

async def save_game_data(game_name, data):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if not game_name:
        return
    await r.hset(CUSTOM_GAMES_KEY, game_name, json.dumps(data))

async def delete_game_data(game_name):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if not game_name:
        return
    await r.hdel(CUSTOM_GAMES_KEY, game_name)

async def get_custom_game_meta(game_name):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if not game_name:
        return None
    meta = await r.hget(CUSTOM_GAMES_META_KEY, game_name)
    if meta:
        if isinstance(meta, bytes):
            meta = meta.decode('utf-8')
        return json.loads(meta)
    return None

async def save_custom_game_meta(game_name, data):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if not game_name:
        return
    await r.hset(CUSTOM_GAMES_META_KEY, game_name, json.dumps(data))

async def delete_custom_game_meta(game_name):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if not game_name:
        return
    await r.hdel(CUSTOM_GAMES_META_KEY, game_name)

async def get_all_custom_games():
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    games = await r.hgetall(CUSTOM_GAMES_META_KEY)
    result = []
    for name, data in games.items():
        if isinstance(name, bytes):
            name = name.decode('utf-8')
        if isinstance(data, bytes):
            data = data.decode('utf-8')
        result.append(json.loads(data))
    return result

async def get_button_game_data(game_name):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if not game_name:
        return None
    game = await r.hget(CUSTOM_BUTTON_GAMES_KEY, game_name)
    if game:
        if isinstance(game, bytes):
            game = game.decode('utf-8')
        return json.loads(game)
    return None

async def save_button_game_data(game_name, data):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if not game_name:
        return
    await r.hset(CUSTOM_BUTTON_GAMES_KEY, game_name, json.dumps(data))

async def delete_button_game_data(game_name):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if not game_name:
        return
    await r.hdel(CUSTOM_BUTTON_GAMES_KEY, game_name)

_GAME_CONTENT_PREFIXES = ('اضف ', 'حذف ', 'قائمة ', 'قائمه ')

def _is_game_content_prefix(text: str) -> bool:
    """أوامر إدارة محتوى اللعبة (اضافة/حذف/عرض)، بكلا شكلي كلمة "قائمة" (بالتاء
    المربوطة أو بدونها) حتى لا يفلت أي شكل من فحوصات تجاوز تفعيل/تعطيل اللعب."""
    return bool(text) and text.startswith(_GAME_CONTENT_PREFIXES)

async def handle_social_games(c, m, k, text):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    
    admin_setup_commands = ['اضف لعبه', 'اضف لعبة', 'اضف لعبه ازرار', 'اضف لعبة ازرار', 'مسح لعبه', 'مسح لعبة', 'قائمة الالعاب', 'قائمه الالعاب']
    has_active_setup_wizard = bool(
        await r.get(f'{m.from_user.id}:addGameStep:{m.chat.id}{Dev_FINAL}') or
        await r.get(f'{m.from_user.id}:addMediaStep:{m.chat.id}{Dev_FINAL}') or
        await r.get(f'{m.from_user.id}:addButtonStep:{m.chat.id}{Dev_FINAL}') or
        await r.get(f'{m.from_user.id}:deleteMediaStep:{m.chat.id}{Dev_FINAL}') or
        await r.get(f'{m.from_user.id}:deleteGameStep:{m.chat.id}{Dev_FINAL}')
    )
    # أوامر إدارة محتوى الألعاب (اضف/حذف/قائمة محتوى، وأي خطوة معالج نشطة تابعة
    # لها) هي عمليات إدارية بحتة (المطوّر يضيف/يحذف محتوى) ولا علاقة لها بتفعيل
    # أو تعطيل اللعب داخل الشات، لذلك يجب ألا تُشترط بوجود مفتاح
    # {chat_id}:enable إطلاقاً - هذا المفتاح خاص فقط بتفعيل/تعطيل قدرة الأعضاء
    # على اللعب الفعلي، وهو غير موجود أصلاً في الخاص. إدارة المحتوى تعمل بأي
    # وقت بغض النظر عن حالة التفعيل، تماماً مثل أي أمر إداري آخر.
    is_content_management_cmd = (
        text in admin_setup_commands or
        _is_game_content_prefix(text) or
        has_active_setup_wizard
    )
    
    if not is_content_management_cmd:
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
    
    admin_commands = ['اضف لعبه', 'اضف لعبة', 'اضف لعبه ازرار', 'اضف لعبة ازرار', 'مسح لعبه', 'مسح لعبة', 'قائمة الالعاب', 'قائمه الالعاب']
    
    is_custom_game_cmd = False
    if _is_game_content_prefix(text):
        parts = text.split(' ', 1)
        if len(parts) == 2:
            game_name = parts[1].strip()
            if game_name.endswith(' الكل'):
                game_name = game_name.replace(' الكل', '').strip()
            
            if (await get_custom_game_meta(game_name) or 
                await get_button_game_data(game_name) or 
                await get_public_game_meta(game_name) or 
                await get_public_button_game_data(game_name)):
                is_custom_game_cmd = True
    
    is_admin_cmd = is_custom_game_cmd or text in admin_commands
    
    if is_admin_cmd and not await dev2_pls(m.from_user.id, m.chat.id):
        return await m.reply(plugins_games_addgame_181(k))
    
    if text.startswith('تعطيل ') or text.startswith('تفعيل '):
        is_enable_cmd = text.startswith('تفعيل ')
        candidate_name = text[len('تفعيل '):].strip() if is_enable_cmd else text[len('تعطيل '):].strip()
        if candidate_name and (
            await get_custom_game_meta(candidate_name) or
            await get_button_game_data(candidate_name) or
            await get_public_game_meta(candidate_name) or
            await get_public_button_game_data(candidate_name)
        ):
            if not await gowner_pls(m.from_user.id, m.chat.id):
                return None
            await set_game_disabled_in_chat(m.chat.id, candidate_name, disabled=not is_enable_cmd)
            action_word = 'فعلت' if is_enable_cmd else 'عطلت'
            admin_name = m.from_user.first_name or m.from_user.username or "عضو"
            admin_mention = f"<a href='tg://user?id={m.from_user.id}'>{html.escape(str(admin_name))}</a>"
            await m.reply(f"• من「 {admin_mention} 」\n• ابشر {action_word} {candidate_name}\n-")
            return True
    
    if await r.get(f'{m.from_user.id}:addGameStep:{m.chat.id}{Dev_FINAL}'):
        return await handle_add_game_step(c, m, k, text)
    
    if await r.get(f'{m.from_user.id}:addMediaStep:{m.chat.id}{Dev_FINAL}'):
        return await handle_add_media_step(c, m, k, text)
    
    if await r.get(f'{m.from_user.id}:addButtonStep:{m.chat.id}{Dev_FINAL}'):
        return await handle_add_button_step(c, m, k, text)
    
    if await r.get(f'{m.from_user.id}:deleteMediaStep:{m.chat.id}{Dev_FINAL}'):
        return await handle_delete_media_step(c, m, k, text)
    
    if await r.get(f'{m.from_user.id}:deleteGameStep:{m.chat.id}{Dev_FINAL}'):
        return await handle_delete_game_step(c, m, k, text)
    
    if text == 'اضف لعبه' or text == 'اضف لعبة':
        if await r.get(f'{m.from_user.id}:addGameStep:{m.chat.id}{Dev_FINAL}'):
            return await m.reply(plugins_games_addgame_200(k))
        await r.set(f'{m.from_user.id}:addGameStep:{m.chat.id}{Dev_FINAL}', 'wait_type')
        await m.reply(plugins_games_addgame_202(k))
        return True
    
    if text == 'اضف لعبه ازرار' or text == 'اضف لعبة ازرار':
        if await r.get(f'{m.from_user.id}:addGameStep:{m.chat.id}{Dev_FINAL}'):
            return await m.reply(plugins_games_addgame_226(k))
        await r.set(f'{m.from_user.id}:addGameStep:{m.chat.id}{Dev_FINAL}', 'wait_type_button')
        await m.reply(plugins_games_addgame_228(k))
        return True
    
    if text == 'مسح لعبه' or text == 'مسح لعبة':
        games = await get_all_custom_games()
        button_games = await r.hgetall(CUSTOM_BUTTON_GAMES_KEY)
        public_games = await get_all_public_games()
        public_button_games = await get_public_button_games()
        
        if not games and not button_games and not public_games and not public_button_games:
            return await m.reply(plugins_games_addgame_254(k))
        
        txt = f'{k} قائمة الالعاب المخصصة:\n\n'
        i = 1
        
        for game in games:
            txt += f'{i} - {game["name"]} ({game["type"]})\n'
            i += 1
        
        for name, data in button_games.items():
            if isinstance(name, bytes):
                name = name.decode('utf-8')
            if isinstance(data, dict):
                txt += f'{i} - {name} (ازرار | {data.get("type", "غير معروف")})\n'
            else:
                try:
                    if isinstance(data, bytes):
                        data = data.decode('utf-8')
                    data_dict = json.loads(data) if isinstance(data, str) else data
                    txt += f'{i} - {name} (ازرار | {data_dict.get("type", "غير معروف")})\n'
                except:
                    txt += f'{i} - {name} (ازرار)\n'
            i += 1
        
        for game in public_games:
            txt += f'{i} - {game["name"]} ({game["type"]}) [عام]\n'
            i += 1
        
        for game in public_button_games:
            if isinstance(game, dict):
                txt += f'{i} - {game.get("name", "غير معروف")} (ازرار | {game.get("data", {}).get("type", "غير معروف")}) [عام]\n'
            else:
                txt += f'{i} - {game} (ازرار) [عام]\n'
            i += 1
        
        txt += f'\n{k} ارسل رقم اللعبة التي تريد مسحها\nللالغاء اكتب الغاء'
        await r.set(f'{m.from_user.id}:deleteGameStep:{m.chat.id}{Dev_FINAL}', 'wait_number')
        await m.reply(txt)
        return True
    
    if text == 'قائمة الالعاب' or text == 'قائمه الالعاب':
        games = await get_all_custom_games()
        button_games = await r.hgetall(CUSTOM_BUTTON_GAMES_KEY)
        public_games = await get_all_public_games()
        public_button_games = await get_public_button_games()
        
        if not games and not button_games and not public_games and not public_button_games:
            return await m.reply(plugins_games_addgame_301(k))
        
        txt = f'{k} قائمة الالعاب المخصصة:\n\n'
        
        for game in games:
            has_q = 'اسئلة' if game.get('has_questions', False) else 'بدون اسئلة'
            has_m = 'فلوس' if game.get('has_money', False) else 'بدون فلوس'
            txt += f'• {game["name"]} ({game["type"]} | {has_q} | {has_m})\n'
        
        for name, data in button_games.items():
            if isinstance(name, bytes):
                name = name.decode('utf-8')
            if isinstance(data, dict):
                has_m = 'فلوس' if data.get('has_money', False) else 'بدون فلوس'
                txt += f'• {name} (ازرار | {data.get("type", "غير معروف")} | {has_m})\n'
            else:
                try:
                    if isinstance(data, bytes):
                        data = data.decode('utf-8')
                    data_dict = json.loads(data) if isinstance(data, str) else data
                    has_m = 'فلوس' if data_dict.get('has_money', False) else 'بدون فلوس'
                    txt += f'• {name} (ازرار | {data_dict.get("type", "غير معروف")} | {has_m})\n'
                except:
                    txt += f'• {name} (ازرار)\n'
        
        for game in public_games:
            has_q = 'اسئلة' if game.get('has_questions', False) else 'بدون اسئلة'
            has_m = 'فلوس' if game.get('has_money', False) else 'بدون فلوس'
            txt += f'• {game["name"]} ({game["type"]} | {has_q} | {has_m}) [عام]\n'
        
        for game in public_button_games:
            if isinstance(game, dict):
                has_m = 'فلوس' if game.get("data", {}).get('has_money', False) else 'بدون فلوس'
                txt += f'• {game.get("name", "غير معروف")} (ازرار | {game.get("data", {}).get("type", "غير معروف")} | {has_m}) [عام]\n'
            else:
                txt += f'• {game} (ازرار) [عام]\n'
        
        await m.reply(txt)
        return True
    
    if text.startswith('قائمة '):
        game_name = text.replace('قائمة ', '').strip()
        if await get_custom_game_meta(game_name):
            return await handle_list_media(c, m, k, game_name)
        if await get_button_game_data(game_name):
            return await handle_list_button_media(c, m, k, game_name)
    
    if text.startswith('اضف '):
        game_name = text.replace('اضف ', '').strip()
        meta = await get_custom_game_meta(game_name)
        if meta:
            if await r.get(f'{m.from_user.id}:addMediaStep:{m.chat.id}{Dev_FINAL}'):
                return await m.reply(plugins_games_addgame_353(k))
            await r.set(f'{m.from_user.id}:addMediaStep:{m.chat.id}{Dev_FINAL}', 'wait_photo')
            await r.set(f'{m.from_user.id}:addMediaType:{m.chat.id}{Dev_FINAL}', game_name)
            await r.set(f'{m.from_user.id}:addMediaMeta:{m.chat.id}{Dev_FINAL}', json.dumps(meta))
            await m.reply(plugins_games_addgame_357(k, meta["type"]))
            return True
        btn_game_data = await get_button_game_data(game_name)
        if btn_game_data:
            if await r.get(f'{m.from_user.id}:addButtonStep:{m.chat.id}{Dev_FINAL}'):
                return await m.reply(plugins_games_addgame_362(k))
            await r.set(f'{m.from_user.id}:addButtonType:{m.chat.id}{Dev_FINAL}', game_name)
            if btn_game_data.get('type') == 'نصوص':
                await r.set(f'{m.from_user.id}:addButtonStep:{m.chat.id}{Dev_FINAL}', 'wait_media')
                await m.reply(plugins_games_addgame_366(k))
            else:
                await r.set(f'{m.from_user.id}:addButtonStep:{m.chat.id}{Dev_FINAL}', 'wait_media_file')
                await m.reply(plugins_games_addgame_369(k, btn_game_data["type"]))
            return True
    
    if text.startswith('حذف '):
        if text.endswith(' الكل'):
            game_name = text.replace(' الكل', '').replace('حذف ', '').strip()
            if await get_custom_game_meta(game_name):
                await save_game_data(game_name, {"media": []})
                await m.reply(plugins_games_addgame_377(k, game_name))
                return True
            if await get_button_game_data(game_name):
                await save_button_game_data(game_name, {"questions": []})
                await m.reply(plugins_games_addgame_381(k, game_name))
                return True
            if await get_public_game_meta(game_name):
                game_data = await get_public_game_data(game_name)
                if not game_data or not game_data.get("media"):
                    return await m.reply(plugins_games_addgame_386(k, game_name))
                
                is_admin = await is_public_game_admin(m.from_user.id)
                media_list = game_data["media"]
                
                if not is_admin:
                    filtered_list = [item for item in media_list if item.get('added_by', 0) == m.from_user.id]
                    if not filtered_list:
                        return await m.reply(plugins_games_addgame_394(k))
                    for item in filtered_list:
                        media_list.remove(item)
                    await save_public_game_data(game_name, game_data)
                    await m.reply(plugins_games_addgame_398(k, len(filtered_list), game_name))
                else:
                    await save_public_game_data(game_name, {"media": []})
                    await m.reply(plugins_games_addgame_401(k, game_name))
                return True
            if await get_public_button_game_data(game_name):
                game_data = await get_public_button_game_data(game_name)
                if not game_data or not game_data.get("questions"):
                    return await m.reply(plugins_games_addgame_406(k, game_name))
                
                is_admin = await is_public_game_admin(m.from_user.id)
                questions_list = game_data["questions"]
                
                if not is_admin:
                    filtered_list = [item for item in questions_list if item.get('added_by', 0) == m.from_user.id]
                    if not filtered_list:
                        return await m.reply(plugins_games_addgame_414(k))
                    for item in filtered_list:
                        questions_list.remove(item)
                    await save_public_button_game_data(game_name, game_data)
                    await m.reply(plugins_games_addgame_418(k, len(filtered_list), game_name))
                else:
                    await save_public_button_game_data(game_name, {"questions": []})
                    await m.reply(plugins_games_addgame_421(k, game_name))
                return True
        else:
            game_name = text.replace('حذف ', '').strip()
            if await get_custom_game_meta(game_name):
                return await handle_delete_media(c, m, k, game_name)
            if await get_button_game_data(game_name):
                return await handle_delete_button_media(c, m, k, game_name)
            if await get_public_game_meta(game_name):
                return await handle_delete_public_media(c, m, k, game_name)
            if await get_public_button_game_data(game_name):
                return await handle_delete_public_button_media(c, m, k, game_name)
    
    if await get_custom_game_meta(text):
        if await is_game_disabled_in_chat(m.chat.id, text):
            return None
        return await handle_play_custom_game(c, m, k, text)
    
    if await get_button_game_data(text):
        if await is_game_disabled_in_chat(m.chat.id, text):
            return None
        return await handle_play_button_game(c, m, k, text)

    return None

async def handle_play_custom_game(c, m, k, game_name):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    meta = await get_custom_game_meta(game_name)
    game_data = await get_custom_game_data(game_name)
    
    if not game_data or not game_data.get("media"):
        return await m.reply(plugins_games_addgame_450(k, game_name))
    
    media_list = game_data["media"]
    total = len(media_list)
    
    current_index_key = f'{m.chat.id}:custom_game_index:{game_name}:{m.from_user.id}'
    current_index = await r.get(current_index_key)
    if current_index:
        if isinstance(current_index, bytes):
            current_index = int(current_index.decode('utf-8'))
        else:
            current_index = int(current_index)
    else:
        current_index = 0
    
    if current_index >= total:
        current_index = 0
    
    item = media_list[current_index]
    
    next_index = (current_index + 1) % total
    await r.set(current_index_key, next_index, ex=3600)
    
    if meta.get('has_questions', False):
        await r.set(f'{m.chat.id}:game:{Dev_FINAL}', json.dumps(item.get('answer', [])), ex=600)
        await r.set(f'{m.chat.id}:custom_game_current:{game_name}:{m.from_user.id}', str(current_index), ex=600)
        has_money = 1 if meta.get('has_money', False) else 0
        await r.set(f'{m.chat.id}:custom_game_has_money:{game_name}:{m.from_user.id}', has_money, ex=600)
        await r.set(f'{m.chat.id}:custom_game_name:{m.from_user.id}', game_name, ex=600)
        await r.set(f'{m.chat.id}:game_answer_start:{Dev_FINAL}', str(time.time()), ex=600)
    
    show_change_button = not meta.get('has_questions', False) and meta.get('type') != 'نصوص'
    reply_markup = None
    
    if show_change_button:
        caption_text = f'ㅤㅤㅤㅤㅤ 『 {current_index + 1} 』ㅤㅤㅤㅤㅤㅤㅤ'
        change_btn = InlineKeyboardButton("تغيير", callback_data=f"change_{game_name}_{next_index}_{m.from_user.id}")
        reply_markup = InlineKeyboardMarkup([[change_btn]])
    else:
        caption_text = (item.get('caption', '') or meta.get('caption', '')) if meta.get('has_questions', False) else ''
    
    if meta['type'] == 'صور':
        if 'media' in item:
            await m.reply_photo(item['media'], caption=caption_text, reply_markup=reply_markup)
        elif 'text' in item:
            await m.reply(plugins_games_addgame_494(caption_text, item['text']), reply_markup=reply_markup)
    
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

async def handle_play_button_game(c, m, k, game_name):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    game_data = await get_button_game_data(game_name)
    if not game_data or not game_data.get("questions"):
        return await m.reply(plugins_games_addgame_523(k, game_name))
    
    questions_list = game_data["questions"]
    total = len(questions_list)
    
    current_index_key = f'{m.chat.id}:button_game_index:{game_name}:{m.from_user.id}'
    current_index = await r.get(current_index_key)
    if current_index:
        if isinstance(current_index, bytes):
            current_index = int(current_index.decode('utf-8'))
        else:
            current_index = int(current_index)
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
        callback_data = f"button_ans_{game_name}_{current_index}_{i}_{str(is_correct)}_{m.from_user.id}"
        buttons.append(InlineKeyboardButton(ans, callback_data=callback_data))
    
    reply_markup = InlineKeyboardMarkup([
        [buttons[0], buttons[1]],
        [buttons[2], buttons[3]]
    ])
    
    has_money = game_data.get('has_money', False)
    await r.set(f'{m.chat.id}:button_game_has_money:{game_name}:{m.from_user.id}', 1 if has_money else 0, ex=600)
    await r.set(f'{m.chat.id}:button_game_name:{m.from_user.id}', game_name, ex=600)
    
    if game_data['type'] == 'نصوص':
        await m.reply(plugins_games_addgame_565(question), reply_markup=reply_markup)
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
            await m.reply(plugins_games_addgame_578(question), reply_markup=reply_markup)
    
    return True

async def handle_add_game_step(c, m, k, text):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    step_raw = await r.get(f'{m.from_user.id}:addGameStep:{m.chat.id}{Dev_FINAL}')
    if step_raw is None:
        return True
    if isinstance(step_raw, bytes):
        step = step_raw.decode('utf-8')
    else:
        step = str(step_raw)
    
    if text == 'الغاء':
        await r.delete(f'{m.from_user.id}:addGameStep:{m.chat.id}{Dev_FINAL}')
        await r.delete(f'{m.from_user.id}:addGameMeta:{m.chat.id}{Dev_FINAL}')
        await m.reply(plugins_games_addgame_597(k))
        return True
    
    if step == 'wait_type' or step == 'wait_type_button':
        is_button = (step == 'wait_type_button')
        game_type = None
        for t in ['صور', 'نصوص', 'صوت', 'قيفات', 'فيديو']:
            if t in text:
                game_type = t
                break
        
        if not game_type:
            await m.reply(plugins_games_addgame_609(k))
            return True
        
        if is_button:
            has_money = 'فلوس' in text
            await r.set(f'{m.from_user.id}:addGameStep:{m.chat.id}{Dev_FINAL}', 'wait_name_button')
            await r.set(f'{m.from_user.id}:addGameMeta:{m.chat.id}{Dev_FINAL}', 
                        json.dumps({'type': game_type, 'has_money': has_money, 'is_button': True}))
            has_m_text = 'مع فلوس' if has_money else 'بدون فلوس'
            await m.reply(plugins_games_addgame_629(k, game_type, has_m_text, k))
            return True
        
        has_questions = 'اسئله' in text or 'اسئلة' in text
        has_money = 'فلوس' in text
        
        if has_money and not has_questions:
            await m.reply(plugins_games_addgame_636(k, k))
            return True
        
        await r.set(f'{m.from_user.id}:addGameStep:{m.chat.id}{Dev_FINAL}', 'wait_name')
        await r.set(f'{m.from_user.id}:addGameMeta:{m.chat.id}{Dev_FINAL}', 
                    json.dumps({'type': game_type, 'has_questions': has_questions, 'has_money': has_money, 'is_button': False}))
        
        opts = []
        if has_questions:
            opts.append('اسئلة')
        if has_money:
            opts.append('فلوس')
        opts_text = ' + '.join(opts) if opts else 'بدون اسئلة وبدون فلوس'
        
        await m.reply(plugins_games_addgame_650(k, game_type, opts_text, k))
        return True
    
    elif step == 'wait_name' or step == 'wait_name_button':
        if not text or text.strip() == '':
            await m.reply(plugins_games_addgame_655(k))
            return True
        
        game_name = text.strip()
        
        if await get_custom_game_meta(game_name):
            await m.reply(plugins_games_addgame_661(k, k))
            return True
        
        if await get_button_game_data(game_name):
            await m.reply(plugins_games_addgame_665(k, k))
            return True
        
        if await get_public_game_meta(game_name):
            await m.reply(plugins_games_addgame_669(k, k))
            return True
        
        if await get_public_button_game_data(game_name):
            await m.reply(plugins_games_addgame_673(k, k))
            return True
        
        if game_name in ['احكام', 'روليت', 'عقاب', 'كرسي']:
            await m.reply(plugins_games_addgame_677(k, k))
            return True
        
        meta_raw = await r.get(f'{m.from_user.id}:addGameMeta:{m.chat.id}{Dev_FINAL}')
        if not meta_raw:
            await m.reply(plugins_games_addgame_682(k))
            await r.delete(f'{m.from_user.id}:addGameStep:{m.chat.id}{Dev_FINAL}')
            return True
        
        if isinstance(meta_raw, bytes):
            meta_raw = meta_raw.decode('utf-8')
        meta = json.loads(meta_raw)
        meta['name'] = game_name
        
        if meta.get('is_button', False):
            await save_button_game_data(game_name, {"type": meta['type'], "has_money": meta['has_money'], "questions": []})
            await r.delete(f'{m.from_user.id}:addGameStep:{m.chat.id}{Dev_FINAL}')
            await r.delete(f'{m.from_user.id}:addGameMeta:{m.chat.id}{Dev_FINAL}')
            has_m = 'مع فلوس' if meta['has_money'] else 'بدون فلوس'
            await m.reply(plugins_games_addgame_696(k, k, game_name, k, meta['type'], k, has_m, k, k, game_name, k, game_name, k, game_name, k, game_name, k, game_name))
            return True
        
        await r.set(f'{m.from_user.id}:addGameMeta:{m.chat.id}{Dev_FINAL}', json.dumps(meta))
        
        if meta['has_questions'] and meta['type'] not in ('نصوص', 'صور'):
            await r.set(f'{m.from_user.id}:addGameStep:{m.chat.id}{Dev_FINAL}', 'wait_caption')
            await m.reply(plugins_games_addgame_714(k))
        else:
            await save_custom_game_meta(game_name, meta)
            await save_game_data(game_name, {"media": []})
            await r.delete(f'{m.from_user.id}:addGameStep:{m.chat.id}{Dev_FINAL}')
            await r.delete(f'{m.from_user.id}:addGameMeta:{m.chat.id}{Dev_FINAL}')
            has_q = 'مع اسئلة' if meta['has_questions'] else 'بدون اسئلة'
            has_m = 'مع فلوس' if meta['has_money'] else 'بدون فلوس'
            await m.reply(plugins_games_addgame_722(k, k, game_name, k, meta['type'], k, has_q, k, has_m, k, k, game_name, k, game_name, k, game_name, k, game_name, k, game_name))
        return True
    
    elif step == 'wait_caption':
        if not text or text.strip() == '':
            await m.reply(plugins_games_addgame_739(k))
            return True
        
        meta_raw = await r.get(f'{m.from_user.id}:addGameMeta:{m.chat.id}{Dev_FINAL}')
        if not meta_raw:
            await m.reply(plugins_games_addgame_744(k))
            await r.delete(f'{m.from_user.id}:addGameStep:{m.chat.id}{Dev_FINAL}')
            return True
        
        if isinstance(meta_raw, bytes):
            meta_raw = meta_raw.decode('utf-8')
        meta = json.loads(meta_raw)
        meta['caption'] = text.strip()
        game_name = meta['name']
        
        await save_custom_game_meta(game_name, meta)
        await save_game_data(game_name, {"media": []})
        await r.delete(f'{m.from_user.id}:addGameStep:{m.chat.id}{Dev_FINAL}')
        await r.delete(f'{m.from_user.id}:addGameMeta:{m.chat.id}{Dev_FINAL}')
        
        has_q = 'مع اسئلة' if meta['has_questions'] else 'بدون اسئلة'
        has_m = 'مع فلوس' if meta['has_money'] else 'بدون فلوس'
        
        await m.reply(plugins_games_addgame_762(k, k, game_name, k, meta['type'], k, has_q, k, has_m, k, meta['caption'], k, k, game_name, k, game_name, k, game_name, k, game_name, k, game_name))
        return True
    
    return True

async def handle_add_button_step(c, m, k, text):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    step_raw = await r.get(f'{m.from_user.id}:addButtonStep:{m.chat.id}{Dev_FINAL}')
    if step_raw is None:
        return True
    if isinstance(step_raw, bytes):
        step = step_raw.decode('utf-8')
    else:
        step = str(step_raw)
    
    game_name_raw = await r.get(f'{m.from_user.id}:addButtonType:{m.chat.id}{Dev_FINAL}')
    if game_name_raw is None:
        await m.reply(plugins_games_addgame_794(k))
        return True
    if isinstance(game_name_raw, bytes):
        game_name = game_name_raw.decode('utf-8')
    else:
        game_name = str(game_name_raw)
    
    game_data = await get_button_game_data(game_name)
    if not game_data:
        await m.reply(plugins_games_addgame_803(k))
        await r.delete(f'{m.from_user.id}:addButtonStep:{m.chat.id}{Dev_FINAL}')
        return True
    
    if text == 'الغاء':
        await r.delete(f'{m.from_user.id}:addButtonStep:{m.chat.id}{Dev_FINAL}')
        await r.delete(f'{m.from_user.id}:addButtonType:{m.chat.id}{Dev_FINAL}')
        await r.delete(f'{m.from_user.id}:addButtonData:{m.chat.id}{Dev_FINAL}')
        await m.reply(plugins_games_addgame_811(k))
        return True
    
    if text == 'تم':
        await r.delete(f'{m.from_user.id}:addButtonStep:{m.chat.id}{Dev_FINAL}')
        await r.delete(f'{m.from_user.id}:addButtonType:{m.chat.id}{Dev_FINAL}')
        await r.delete(f'{m.from_user.id}:addButtonData:{m.chat.id}{Dev_FINAL}')
        await m.reply(plugins_games_addgame_818(k))
        return True
    
    if step == 'wait_media':
        question = text.strip()
        if not question:
            await m.reply(plugins_games_addgame_824(k))
            return True
        
        await r.set(f'{m.from_user.id}:addButtonData:{m.chat.id}{Dev_FINAL}', json.dumps({'question': question}))
        
        if game_data['type'] != 'نصوص':
            await r.set(f'{m.from_user.id}:addButtonStep:{m.chat.id}{Dev_FINAL}', 'wait_media_file')
            await m.reply(plugins_games_addgame_831(k, game_data["type"]))
        else:
            await r.set(f'{m.from_user.id}:addButtonStep:{m.chat.id}{Dev_FINAL}', 'wait_answers')
            await m.reply(plugins_games_addgame_834(k, k, k))
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
            await m.reply(plugins_games_addgame_848(k, game_data["type"]))
            return True
        
        data_raw = await r.get(f'{m.from_user.id}:addButtonData:{m.chat.id}{Dev_FINAL}')
        if data_raw:
            if isinstance(data_raw, bytes):
                data_raw = data_raw.decode('utf-8')
            data = json.loads(data_raw)
        else:
            data = {}
        
        if 'question' not in data:
            caption = m.html if m.caption else ''
            if not caption or not caption.strip():
                await m.reply(plugins_games_addgame_862(k, game_data["type"]))
                return True
            data['question'] = caption.strip()
        
        data['media'] = media_id
        await r.set(f'{m.from_user.id}:addButtonData:{m.chat.id}{Dev_FINAL}', json.dumps(data))
        
        await r.set(f'{m.from_user.id}:addButtonStep:{m.chat.id}{Dev_FINAL}', 'wait_answers')
        await m.reply(plugins_games_addgame_870(k, game_data["type"], k))
        return True
    
    elif step == 'wait_answers':
        lines = [line.strip() for line in text.strip().split('\n') if line.strip()]
        if len(lines) < 4:
            await m.reply(plugins_games_addgame_876(k))
            return True
        
        wrong_answers = lines[:3]
        correct_answer = lines[3]
        
        data_raw = await r.get(f'{m.from_user.id}:addButtonData:{m.chat.id}{Dev_FINAL}')
        if data_raw:
            if isinstance(data_raw, bytes):
                data_raw = data_raw.decode('utf-8')
            data = json.loads(data_raw)
        else:
            data = {'question': ''}
        
        question_item = {
            'question': data.get('question', ''),
            'wrong_answers': wrong_answers,
            'correct_answer': correct_answer
        }
        
        if 'media' in data:
            question_item['media'] = data['media']
        
        game_data['questions'].append(question_item)
        await save_button_game_data(game_name, game_data)
        
        await r.delete(f'{m.from_user.id}:addButtonData:{m.chat.id}{Dev_FINAL}')
        await r.set(f'{m.from_user.id}:addButtonStep:{m.chat.id}{Dev_FINAL}', 'wait_media')
        
        await m.reply(plugins_games_addgame_905(k, k, data.get("question", ""), k, correct_answer, k, len(game_data["questions"]), k, k))
        return True
    
    return True

async def handle_delete_game_step(c, m, k, text):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if text == 'الغاء':
        await r.delete(f'{m.from_user.id}:deleteGameStep:{m.chat.id}{Dev_FINAL}')
        await m.reply(plugins_games_addgame_916(k))
        return True
    
    try:
        index = int(text.strip()) - 1
    except:
        await m.reply(plugins_games_addgame_922(k))
        return True
    
    games = await get_all_custom_games()
    button_games_dict = await r.hgetall(CUSTOM_BUTTON_GAMES_KEY)
    button_games = []
    for name, data in button_games_dict.items():
        if isinstance(name, bytes):
            name = name.decode('utf-8')
        if isinstance(data, bytes):
            data = data.decode('utf-8')
        button_games.append({'name': name, 'data': json.loads(data)})
    
    public_games = await get_all_public_games()
    public_button_games = await get_public_button_games()
    
    total = len(games) + len(button_games) + len(public_games) + len(public_button_games)
    
    if index < 0 or index >= total:
        await m.reply(plugins_games_addgame_941(k))
        return True
    
    if index < len(games):
        game = games[index]
        game_name = game['name']
        await delete_game_data(game_name)
        await delete_custom_game_meta(game_name)
        await m.reply(plugins_games_addgame_949(k, game_name))
    
    elif index < len(games) + len(button_games):
        btn_index = index - len(games)
        game_name = button_games[btn_index]['name']
        await delete_button_game_data(game_name)
        await m.reply(plugins_games_addgame_955(k, game_name))
    
    elif index < len(games) + len(button_games) + len(public_games):
        pub_index = index - len(games) - len(button_games)
        game = public_games[pub_index]
        game_name = game['name']
        
        if not await is_public_game_admin(m.from_user.id):
            await m.reply(plugins_games_addgame_963(k))
            await r.delete(f'{m.from_user.id}:deleteGameStep:{m.chat.id}{Dev_FINAL}')
            return True
        
        await delete_public_game_data(game_name)
        await delete_public_game_meta(game_name)
        await m.reply(plugins_games_addgame_969(k, game_name))
    
    else:
        pub_btn_index = index - len(games) - len(button_games) - len(public_games)
        if pub_btn_index < len(public_button_games):
            game_name = public_button_games[pub_btn_index]['name']
            
            if not await is_public_game_admin(m.from_user.id):
                await m.reply(plugins_games_addgame_977(k))
                await r.delete(f'{m.from_user.id}:deleteGameStep:{m.chat.id}{Dev_FINAL}')
                return True
            
            await delete_public_button_game_data(game_name)
            await m.reply(plugins_games_addgame_982(k, game_name))
    
    await r.delete(f'{m.from_user.id}:deleteGameStep:{m.chat.id}{Dev_FINAL}')
    return True

async def handle_add_media_step(c, m, k, text):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    step_raw = await r.get(f'{m.from_user.id}:addMediaStep:{m.chat.id}{Dev_FINAL}')
    if step_raw is None:
        return True
    if isinstance(step_raw, bytes):
        step = step_raw.decode('utf-8')
    else:
        step = str(step_raw)
    
    game_name_raw = await r.get(f'{m.from_user.id}:addMediaType:{m.chat.id}{Dev_FINAL}')
    if game_name_raw is None:
        return True
    if isinstance(game_name_raw, bytes):
        game_name = game_name_raw.decode('utf-8')
    else:
        game_name = str(game_name_raw)
    
    meta_raw = await r.get(f'{m.from_user.id}:addMediaMeta:{m.chat.id}{Dev_FINAL}')
    meta = None
    if meta_raw:
        if isinstance(meta_raw, bytes):
            meta_raw = meta_raw.decode('utf-8')
        meta = json.loads(meta_raw)
    
    if text == 'الغاء':
        await r.delete(f'{m.from_user.id}:addMediaStep:{m.chat.id}{Dev_FINAL}')
        await r.delete(f'{m.from_user.id}:addMediaType:{m.chat.id}{Dev_FINAL}')
        await r.delete(f'{m.from_user.id}:addMediaMeta:{m.chat.id}{Dev_FINAL}')
        await r.delete(f'{m.from_user.id}:addMediaData:{m.chat.id}{Dev_FINAL}')
        await r.delete(f'{m.from_user.id}:addMediaBatch:{m.chat.id}{Dev_FINAL}')
        await m.reply(plugins_games_addgame_1020(k))
        return True
    
    if step == 'wait_photo':
        if text == 'تم':
            batch_key = f'{m.from_user.id}:addMediaBatch:{m.chat.id}{Dev_FINAL}'
            batch_data = await r.get(batch_key)
            if batch_data:
                if isinstance(batch_data, bytes):
                    batch_data = batch_data.decode('utf-8')
                batch = json.loads(batch_data)
                if batch:
                    game_data = await get_custom_game_data(game_name)
                    if not game_data:
                        game_data = {"media": []}
                    for item in batch:
                        game_data["media"].append(item)
                    await save_game_data(game_name, game_data)
                    await r.delete(batch_key)
                    await m.reply(plugins_games_addgame_1039(k, len(batch), meta["type"]))
            
            await r.delete(f'{m.from_user.id}:addMediaStep:{m.chat.id}{Dev_FINAL}')
            await r.delete(f'{m.from_user.id}:addMediaType:{m.chat.id}{Dev_FINAL}')
            await r.delete(f'{m.from_user.id}:addMediaMeta:{m.chat.id}{Dev_FINAL}')
            await r.delete(f'{m.from_user.id}:addMediaData:{m.chat.id}{Dev_FINAL}')
            await m.reply(plugins_games_addgame_1045(k))
            return True
        
        if m.media_group_id and meta and meta.get('type') == 'صور':
            return True
        
        if meta and meta.get('type') == 'نصوص':
            if not text or text.strip() == '':
                await m.reply(plugins_games_addgame_1053(k))
                return True
            
            lines = text.strip().split('\n')
            added = 0
            game_data = await get_custom_game_data(game_name)
            if not game_data:
                game_data = {"media": []}
            
            for line in lines:
                line = line.strip()
                if line:
                    if meta.get('has_questions', False):
                        await r.set(f'{m.from_user.id}:addMediaData:{m.chat.id}{Dev_FINAL}', 
                                    json.dumps({'text': line, 'caption': ''}))
                        await r.set(f'{m.from_user.id}:addMediaStep:{m.chat.id}{Dev_FINAL}', 'wait_answers')
                        await m.reply(plugins_games_addgame_1069(k, k))
                        return True
                    else:
                        game_data["media"].append({"text": line, "answer": []})
                        added += 1
            
            if added > 0 and not meta.get('has_questions', False):
                await save_game_data(game_name, game_data)
                await m.reply(plugins_games_addgame_1077(k, added, k, len(game_data["media"]), k, k))
                await r.set(f'{m.from_user.id}:addMediaStep:{m.chat.id}{Dev_FINAL}', 'wait_photo')
            return True
        
        media_id = None
        media_type = None
        
        if meta and meta.get('type') == 'صور':
            if not m.photo:
                await m.reply(plugins_games_addgame_1086(k))
                return True
            media_id = m.photo.file_id
            media_type = 'photo'
        
        elif meta and meta.get('type') == 'فيديو':
            if not m.video:
                await m.reply(plugins_games_addgame_1093(k))
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
                await m.reply(plugins_games_addgame_1106(k))
                return True
        
        elif meta and meta.get('type') == 'قيفات':
            if not m.animation:
                await m.reply(plugins_games_addgame_1111(k))
                return True
            media_id = m.animation.file_id
            media_type = 'animation'
        
        else:
            await m.reply(plugins_games_addgame_1117(k))
            return True
        
        has_questions_flow = bool(meta and meta.get('has_questions', False))
        caption = (m.html if m.caption else '') if has_questions_flow else ''
        
        if has_questions_flow and meta.get('type') == 'صور' and not caption.strip():
            await m.reply(plugins_games_addgame_862(k, meta["type"]))
            return True
        
        save_data = {}
        if media_type == 'voice':
            save_data = {'voice': media_id, 'caption': caption}
        else:
            save_data = {'media': media_id, 'caption': caption}
        
        if meta and meta.get('has_questions', False):
            await r.set(f'{m.from_user.id}:addMediaData:{m.chat.id}{Dev_FINAL}', 
                        json.dumps(save_data))
            await r.set(f'{m.from_user.id}:addMediaStep:{m.chat.id}{Dev_FINAL}', 'wait_answers')
            await m.reply(plugins_games_addgame_1133(k, meta["type"], k))
            return True
        
        batch_key = f'{m.from_user.id}:addMediaBatch:{m.chat.id}{Dev_FINAL}'
        batch_data = await r.get(batch_key)
        if batch_data:
            if isinstance(batch_data, bytes):
                batch_data = batch_data.decode('utf-8')
            batch = json.loads(batch_data)
        else:
            batch = []
        
        if 'voice' in save_data:
            batch.append({"voice": save_data['voice'], "answer": [], "caption": caption})
        else:
            batch.append({"media": save_data['media'], "answer": [], "caption": caption})
        
        await r.set(batch_key, json.dumps(batch), ex=300)
        
        game_data = await get_custom_game_data(game_name)
        if not game_data:
            game_data = {"media": []}
        
        for item in batch:
            game_data["media"].append(item)
        
        await save_game_data(game_name, game_data)
        await r.delete(batch_key)
        
        await m.reply(plugins_games_addgame_1162(k, len(batch), meta["type"], k, len(game_data["media"]), k, k))
        await r.set(f'{m.from_user.id}:addMediaStep:{m.chat.id}{Dev_FINAL}', 'wait_photo')
        return True
    
    elif step == 'wait_answers':
        if text == 'تم':
            await r.delete(f'{m.from_user.id}:addMediaStep:{m.chat.id}{Dev_FINAL}')
            await r.delete(f'{m.from_user.id}:addMediaType:{m.chat.id}{Dev_FINAL}')
            await r.delete(f'{m.from_user.id}:addMediaMeta:{m.chat.id}{Dev_FINAL}')
            await r.delete(f'{m.from_user.id}:addMediaData:{m.chat.id}{Dev_FINAL}')
            await m.reply(plugins_games_addgame_1172(k))
            return True
        
        if not text or text.strip() == '':
            await m.reply(plugins_games_addgame_1176(k))
            return True
        
        answers = [a.strip() for a in text.strip().split('\n') if a.strip()]
        if not answers:
            await m.reply(plugins_games_addgame_1181(k))
            return True
        
        data_raw = await r.get(f'{m.from_user.id}:addMediaData:{m.chat.id}{Dev_FINAL}')
        if not data_raw:
            await m.reply(plugins_games_addgame_1186(k))
            await r.delete(f'{m.from_user.id}:addMediaStep:{m.chat.id}{Dev_FINAL}')
            await r.delete(f'{m.from_user.id}:addMediaType:{m.chat.id}{Dev_FINAL}')
            return True
        
        if isinstance(data_raw, bytes):
            data_raw = data_raw.decode('utf-8')
        data = json.loads(data_raw)
        
        game_data = await get_custom_game_data(game_name)
        if not game_data:
            game_data = {"media": []}
        
        if 'text' in data:
            game_data["media"].append({
                "text": data['text'],
                "answer": answers
            })
        elif 'voice' in data:
            game_data["media"].append({
                "voice": data['voice'],
                "answer": answers,
                "caption": data.get('caption', '')
            })
        else:
            game_data["media"].append({
                "media": data['media'],
                "answer": answers,
                "caption": data.get('caption', '')
            })
        
        await save_game_data(game_name, game_data)
        
        await r.delete(f'{m.from_user.id}:addMediaData:{m.chat.id}{Dev_FINAL}')
        await r.set(f'{m.from_user.id}:addMediaStep:{m.chat.id}{Dev_FINAL}', 'wait_photo')
        
        await m.reply(plugins_games_addgame_1222(k, k, ", ".join(answers), k, len(game_data["media"]), k, k))
        return True
    
    return True

@Client.on_message(filters.media_group & filters.group, group=38)
async def handle_album(c, m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    k = await r.get(f'{Dev_FINAL}:botkey') or '•'
    
    if not await r.get(f'{m.from_user.id}:addMediaStep:{m.chat.id}{Dev_FINAL}'):
        return
    
    step_raw = await r.get(f'{m.from_user.id}:addMediaStep:{m.chat.id}{Dev_FINAL}')
    if step_raw is None:
        return
    if isinstance(step_raw, bytes):
        step = step_raw.decode('utf-8')
    else:
        step = str(step_raw)
    
    if step != 'wait_photo':
        return
    
    game_name_raw = await r.get(f'{m.from_user.id}:addMediaType:{m.chat.id}{Dev_FINAL}')
    if game_name_raw is None:
        return
    if isinstance(game_name_raw, bytes):
        game_name = game_name_raw.decode('utf-8')
    else:
        game_name = str(game_name_raw)
    
    meta_raw = await r.get(f'{m.from_user.id}:addMediaMeta:{m.chat.id}{Dev_FINAL}')
    meta = None
    if meta_raw:
        if isinstance(meta_raw, bytes):
            meta_raw = meta_raw.decode('utf-8')
        meta = json.loads(meta_raw)
    
    if not meta:
        return
    
    media_group_id = m.media_group_id
    if not media_group_id:
        return
    
    group_key = f'{m.from_user.id}:album:{media_group_id}:{game_name}'
    
    album_data = await r.get(group_key)
    if album_data:
        if isinstance(album_data, bytes):
            album_data = album_data.decode('utf-8')
        album = json.loads(album_data)
    else:
        album = {"media": [], "count": 0}
    
    media_type = meta.get('type')
    if media_type == 'صور' and m.photo:
        album["media"].append({"media": m.photo.file_id, "answer": [], "caption": ''})
        album["count"] += 1
    elif media_type == 'فيديو' and m.video:
        album["media"].append({"media": m.video.file_id, "answer": [], "caption": ''})
        album["count"] += 1
    else:
        return
    
    await r.set(group_key, json.dumps(album), ex=3)
    await asyncio.sleep(2)
    
    final_album = await r.get(group_key)
    if final_album:
        if isinstance(final_album, bytes):
            final_album = final_album.decode('utf-8')
        final_album = json.loads(final_album)
    else:
        return
    
    game_data = await get_custom_game_data(game_name)
    if not game_data:
        game_data = {"media": []}
    
    for item in final_album["media"]:
        game_data["media"].append(item)
    
    await save_game_data(game_name, game_data)
    await r.delete(group_key)
    
    await m.reply(plugins_games_addgame_1313(k, final_album["count"], media_type, k, len(game_data["media"]), k, k))
    
    return True

async def handle_list_media(c, m, k, game_name):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    meta = await get_custom_game_meta(game_name)
    game_data = await get_custom_game_data(game_name)
    
    if not game_data or not game_data.get("media"):
        return await m.reply(plugins_games_addgame_1325(k, game_name))
    
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

async def handle_list_button_media(c, m, k, game_name):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    game_data = await get_button_game_data(game_name)
    if not game_data or not game_data.get("questions"):
        return await m.reply(plugins_games_addgame_1357(k, game_name))
    
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

async def handle_delete_media(c, m, k, game_name):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    game_data = await get_custom_game_data(game_name)
    if not game_data or not game_data.get("media"):
        return await m.reply(plugins_games_addgame_1380(k, game_name))
    
    media_list = game_data["media"]
    txt = f'{k} قائمة محتوى {game_name}:\n\n'
    
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
    
    txt += f'{k} ارسل رقم المحتوى الذي تريد حذفه\nللالغاء اكتب الغاء'
    
    await r.set(f'{m.from_user.id}:deleteMediaStep:{m.chat.id}{Dev_FINAL}', 'wait_number')
    await r.set(f'{m.from_user.id}:deleteMediaType:{m.chat.id}{Dev_FINAL}', game_name)
    await m.reply(txt)
    return True

async def handle_delete_button_media(c, m, k, game_name):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    game_data = await get_button_game_data(game_name)
    if not game_data or not game_data.get("questions"):
        return await m.reply(plugins_games_addgame_1414(k, game_name))
    
    questions_list = game_data["questions"]
    txt = f'{k} قائمة محتوى {game_name} (ازرار):\n\n'
    
    for i, item in enumerate(questions_list, 1):
        q = item.get('question', '')
        correct = item.get('correct_answer', '')
        txt += f'{i} - {q[:50]}{"..." if len(q) > 50 else ""}\n'
        txt += f'    ✓ {correct}\n'
        txt += '\n'
    
    txt += f'{k} ارسل رقم السؤال الذي تريد حذفه\nللالغاء اكتب الغاء'
    
    await r.set(f'{m.from_user.id}:deleteMediaStep:{m.chat.id}{Dev_FINAL}', 'wait_number')
    await r.set(f'{m.from_user.id}:deleteMediaType:{m.chat.id}{Dev_FINAL}', game_name)
    await m.reply(txt)
    return True

async def handle_delete_media_step(c, m, k, text):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if text == 'الغاء':
        await r.delete(f'{m.from_user.id}:deleteMediaStep:{m.chat.id}{Dev_FINAL}')
        await r.delete(f'{m.from_user.id}:deleteMediaType:{m.chat.id}{Dev_FINAL}')
        await m.reply(plugins_games_addgame_1440(k))
        return True
    
    game_name_raw = await r.get(f'{m.from_user.id}:deleteMediaType:{m.chat.id}{Dev_FINAL}')
    if game_name_raw is None:
        await m.reply(plugins_games_addgame_1445(k))
        return True
    
    if isinstance(game_name_raw, bytes):
        game_name = game_name_raw.decode('utf-8')
    else:
        game_name = str(game_name_raw)
    
    try:
        index = int(text.strip()) - 1
    except ValueError:
        await m.reply(plugins_games_addgame_1456(k))
        return True
    
    game_data = await get_custom_game_data(game_name)
    if game_data and game_data.get("media"):
        if index < 0 or index >= len(game_data["media"]):
            await m.reply(plugins_games_addgame_1462(k))
            return True
        deleted = game_data["media"].pop(index)
        await save_game_data(game_name, game_data)
        answers = deleted.get('answer', [])
        if answers:
            await m.reply(plugins_games_addgame_1468(k, k, ", ".join(answers), k, len(game_data["media"])))
        else:
            await m.reply(plugins_games_addgame_1470(k, k, len(game_data["media"])))
        await r.delete(f'{m.from_user.id}:deleteMediaStep:{m.chat.id}{Dev_FINAL}')
        await r.delete(f'{m.from_user.id}:deleteMediaType:{m.chat.id}{Dev_FINAL}')
        return True
    
    btn_data = await get_button_game_data(game_name)
    if btn_data and btn_data.get("questions"):
        if index < 0 or index >= len(btn_data["questions"]):
            await m.reply(plugins_games_addgame_1478(k))
            return True
        deleted = btn_data["questions"].pop(index)
        await save_button_game_data(game_name, btn_data)
        await m.reply(plugins_games_addgame_1482(k, k, deleted.get("question", ""), k, len(btn_data["questions"])))
        await r.delete(f'{m.from_user.id}:deleteMediaStep:{m.chat.id}{Dev_FINAL}')
        await r.delete(f'{m.from_user.id}:deleteMediaType:{m.chat.id}{Dev_FINAL}')
        return True
    
    await m.reply(plugins_games_addgame_1487(k, game_name))
    await r.delete(f'{m.from_user.id}:deleteMediaStep:{m.chat.id}{Dev_FINAL}')
    await r.delete(f'{m.from_user.id}:deleteMediaType:{m.chat.id}{Dev_FINAL}')
    return True

async def handle_delete_public_media(c, m, k, game_name):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    game_data = await get_public_game_data(game_name)
    if not game_data or not game_data.get("media"):
        return await m.reply(plugins_games_addgame_1498(k, game_name))
    
    media_list = game_data["media"]
    is_admin = await is_public_game_admin(m.from_user.id)
    
    if not is_admin:
        filtered_list = [item for item in media_list if item.get('added_by', 0) == m.from_user.id]
    else:
        filtered_list = media_list
    
    if not filtered_list:
        return await m.reply(plugins_games_addgame_1509(k))
    
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
        return await m.reply(plugins_games_addgame_1555(k, game_name))
    
    questions_list = game_data["questions"]
    is_admin = await is_public_game_admin(m.from_user.id)
    
    if not is_admin:
        filtered_list = [item for item in questions_list if item.get('added_by', 0) == m.from_user.id]
    else:
        filtered_list = questions_list
    
    if not filtered_list:
        return await m.reply(plugins_games_addgame_1566(k))
    
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
        await m.reply(plugins_games_addgame_1601(k))
        return True
    
    game_name_raw = await r.get(f'{m.from_user.id}:deletePublicMediaType:{m.chat.id}{Dev_FINAL}')
    if game_name_raw is None:
        await m.reply(plugins_games_addgame_1606(k))
        return True
    
    if isinstance(game_name_raw, bytes):
        game_name = game_name_raw.decode('utf-8')
    else:
        game_name = str(game_name_raw)
    
    try:
        index = int(text.strip()) - 1
    except ValueError:
        await m.reply(plugins_games_addgame_1617(k))
        return True
    
    filtered_list_raw = await r.get(f'{m.from_user.id}:deletePublicFilteredList:{m.chat.id}{Dev_FINAL}')
    if not filtered_list_raw:
        await m.reply(plugins_games_addgame_1622(k))
        return True
    
    if isinstance(filtered_list_raw, bytes):
        filtered_list_raw = filtered_list_raw.decode('utf-8')
    
    filtered_list = json.loads(filtered_list_raw)
    
    if index < 0 or index >= len(filtered_list):
        await m.reply(plugins_games_addgame_1631(k))
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
            await m.reply(plugins_games_addgame_1654(k, k, ", ".join(answers), k, len(game_data["media"])))
        else:
            await m.reply(plugins_games_addgame_1656(k, k, len(game_data["media"])))
        
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
        await m.reply(plugins_games_addgame_1672(k, k, deleted_item.get("question", ""), k, len(btn_data["questions"])))
        
        await r.delete(f'{m.from_user.id}:deletePublicMediaStep:{m.chat.id}{Dev_FINAL}')
        await r.delete(f'{m.from_user.id}:deletePublicMediaType:{m.chat.id}{Dev_FINAL}')
        await r.delete(f'{m.from_user.id}:deletePublicFilteredList:{m.chat.id}{Dev_FINAL}')
        return True
    
    await m.reply(plugins_games_addgame_1679(k, game_name))
    await r.delete(f'{m.from_user.id}:deletePublicMediaStep:{m.chat.id}{Dev_FINAL}')
    await r.delete(f'{m.from_user.id}:deletePublicMediaType:{m.chat.id}{Dev_FINAL}')
    await r.delete(f'{m.from_user.id}:deletePublicFilteredList:{m.chat.id}{Dev_FINAL}')
    return True

@Client.on_callback_query(filters.regex(r"^(change_|ag_|button_ans_)"), group=-43731)
async def custom_game_callback(c, callback_query):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    data = callback_query.data
    k = await r.get(f'{Dev_FINAL}:botkey') or '•'
    
    if data.startswith('change_'):
        parts = data.split('_')
        game_name = parts[1]
        next_index = int(parts[2])
        user_id = int(parts[3])
        
        if callback_query.from_user.id != user_id:
            return await callback_query.answer(REPLIES['plugins_games_addgame_1700'], show_alert=True)
        
        meta = await get_custom_game_meta(game_name)
        game_data = await get_custom_game_data(game_name)
        
        if not game_data or not game_data.get("media"):
            return await callback_query.answer(REPLIES['plugins_games_addgame_1706'], show_alert=True)
        
        media_list = game_data["media"]
        total = len(media_list)
        
        if next_index >= total:
            next_index = 0
        
        item = media_list[next_index]
        
        if 'media' not in item and 'voice' not in item and 'text' not in item:
            return await callback_query.answer(REPLIES['plugins_games_addgame_1717'], show_alert=True)
        
        current_index_key = f'{callback_query.message.chat.id}:custom_game_index:{game_name}:{user_id}'
        await r.set(current_index_key, next_index, ex=3600)
        
        new_next = (next_index + 1) % total
        caption_text = f'ㅤㅤㅤㅤㅤ 『 {next_index + 1} 』ㅤㅤㅤㅤㅤ'
        
        if 'voice' in item:
            if meta['type'] == 'صوت':
                change_btn = InlineKeyboardButton("تغيير", callback_data=f"change_{game_name}_{new_next}_{user_id}")
                reply_markup = InlineKeyboardMarkup([[change_btn]])
                try:
                    await callback_query.message.reply_voice(item['voice'], caption=caption_text, reply_markup=reply_markup)
                except Exception as e:
                    await callback_query.answer(plugins_games_addgame_1732(str(e)[:50]), show_alert=True)
                    return
                await callback_query.message.delete()
                await callback_query.answer()
                return
        
        change_btn = InlineKeyboardButton("تغيير", callback_data=f"change_{game_name}_{new_next}_{user_id}")
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
                        plugins_games_addgame_1749(caption_text, item['text']),
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
                        plugins_games_addgame_1777(caption_text, item['text']),
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
                        await callback_query.message.reply(plugins_games_addgame_1794(caption_text, item['text']), reply_markup=reply_markup)
                
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
                        await callback_query.message.reply(plugins_games_addgame_1810(caption_text, item['text']), reply_markup=reply_markup)
            else:
                await callback_query.answer(plugins_games_addgame_1812(error_msg[:50]), show_alert=True)
                return
        
        await callback_query.answer()
    
    elif data.startswith('button_ans_'):
        parts = data.split('_')
        game_name = parts[2]
        question_index = int(parts[3])
        button_index = int(parts[4])
        is_correct = parts[5] == 'True'
        user_id = callback_query.from_user.id
        
        game_data = await get_button_game_data(game_name)
        if not game_data or not game_data.get("questions"):
            return await callback_query.answer(REPLIES['plugins_games_addgame_1706'], show_alert=True)
        
        questions_list = game_data["questions"]
        if question_index >= len(questions_list):
            return await callback_query.answer(REPLIES['plugins_games_addgame_1831'], show_alert=True)
        
        item = questions_list[question_index]
        question = item.get('question', '')
        chat_id = callback_query.message.chat.id
        
        user = callback_query.from_user
        user_mention = f"<a href='tg://user?id={user.id}'>{html.escape(str(user.first_name))}</a>"
        
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
                text_result = f"{k} {user_mention}\n{k} احسنت اجابة صحيحه ربحت {ra} ريال"
            else:
                text_result = f"{k} {user_mention}\n{k} احسنت اجابة صحيحه"
        else:
            text_result = f"{k} {user_mention}\n{k} يا فاشل إجابتك خطا"
        
        msg = callback_query.message
        has_media = bool(msg.photo or msg.video or msg.animation or msg.audio or msg.document or msg.voice)
        
        reply_to_id = msg.reply_to_message.id if msg.reply_to_message else None
        
        if has_media:
            try:
                await msg.delete()
            except Exception:
                pass
            
            if reply_to_id:
                await c.send_message(
                    chat_id=chat_id,
                    text=text_result,
                    reply_to_message_id=reply_to_id,
                    disable_web_page_preview=True
                )
            else:
                await c.send_message(
                    chat_id=chat_id,
                    text=text_result,
                    disable_web_page_preview=True
                )
        else:
            try:
                await callback_query.edit_message_text(text_result, disable_web_page_preview=True)
            except Exception:
                try:
                    await msg.delete()
                except Exception:
                    pass
                if reply_to_id:
                    await c.send_message(
                        chat_id=chat_id,
                        text=text_result,
                        reply_to_message_id=reply_to_id,
                        disable_web_page_preview=True
                    )
                else:
                    await c.send_message(
                        chat_id=chat_id,
                        text=text_result,
                        disable_web_page_preview=True
                    )
        
        await callback_query.answer()