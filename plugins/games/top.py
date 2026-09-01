from helpers.context import get_global_r, get_global_dev, get_global_k
r = get_global_r()
Dev_FINAL = get_global_dev()
k = get_global_k()
from helpers.redis import r as _shared_r
import requests
import json
import re
import aiohttp
import asyncio
import time

br = get_global_r()
Dev_FINAL = get_global_dev()
k = get_global_k()

from compat import Client
from compat import InlineKeyboardMarkup, InlineKeyboardButton
from compat import ParseMode
from compat import filters
from helpers.ranks import *
from helpers.top_snapshot import get_top_snapshot, LOCAL_TYPES as SNAPSHOT_LOCAL_TYPES
from ..buttons import register_buttons, get_button_custom, get_button_color, create_button_raw
from ..protect import get_top, get_emoji_bank, _decode_if_bytes, get_chat_score, get_chat_name_from_api, GLOBAL_TOP_NS
from .utils import add_game_earnings, show_game_earnings_top
from helpers.replies_store import (
    REPLIES,
    plugins_games_top_1193,
    plugins_games_top_1216,
    plugins_games_top_1218,
    plugins_games_top_1220,
    plugins_games_top_1223,
    plugins_games_top_1225,
    plugins_games_top_1227,
)

BUTTONS_DEFINITIONS = {
    "top": {
        "name": "أزرار التوب",
        "buttons": [
            {"id": "top_invaders", "default": "توب الغزاة 🏅"},
            {"id": "top_genius", "default": "توب العباقرة"},
            {"id": "top_interactive", "default": "توب المتفاعلين"},
            {"id": "top_farmers", "default": "توب المزارع"},
            {"id": "top_donations", "default": "توب المتبرعين"},
            {"id": "top_money", "default": "توب الفلوس"},
            {"id": "top_thieves", "default": "توب الحراميه"},
            {"id": "top_marriage_local", "default": "الزواج بالقروب"},
            {"id": "top_marriage_global", "default": "الزواج العام"},
            {"id": "top_likes", "default": "توب اللايكات"},
            {"id": "top_groups", "default": "توب القروبات"},
            {"id": "top_close", "default": "اخفاء التوب"},
        ]
    },
    "invaders": {
        "name": "أزرار الغزاة",
        "buttons": [
            {"id": "invaders_back", "default": "رجوع"},
            {"id": "invaders_close", "default": "اخفاء التوب"},
        ]
    },
    "groups": {
        "name": "أزرار المجموعات",
        "buttons": [
            {"id": "groups_players", "default": "قروبات الالعاب"},
            {"id": "groups_interactive", "default": "قروبات التفاعل"},
            {"id": "groups_back", "default": "رجوع"},
            {"id": "groups_close", "default": "اخفاء التوب"},
        ]
    },
    "likes": {
        "name": "أزرار اللايكات",
        "buttons": [
            {"id": "likes_show", "default": "توب اللايكات"},
            {"id": "dislikes_show", "default": "توب الدسلايكات"},
            {"id": "likes_back", "default": "رجوع"},
            {"id": "likes_close", "default": "اخفاء التوب"},
        ]
    }
}

register_buttons(BUTTONS_DEFINITIONS)

CACHE = {}
CACHE_TTL = 60

def _get_cached(key):
    entry = CACHE.get(key)
    if entry and entry['expire'] > time.time():
        return entry['data']
    return None

def _set_cached(key, data):
    CACHE[key] = {'data': data, 'expire': time.time() + CACHE_TTL}

async def update_interactive_top(chat_id, user_id, increment=1):
    key = f"top:interactive:{chat_id}"
    await r.zincrby(key, increment, str(user_id))


async def update_thieves_top(user_id, new_stolen):
    await r.zadd("top:thieves", {str(user_id): new_stolen})

async def update_donations_top(user_id, new_donated):
    await r.zadd("top:donations", {str(user_id): new_donated})

async def update_farmers_top(user_id, new_plants):
    await r.zadd("top:farmers", {str(user_id): new_plants})

async def update_marriage_top(chat_id, marriage_id, new_money, is_global=False):
    key = "top:marriage:global" if is_global else f"top:marriage:{chat_id}"
    await r.zadd(key, {str(marriage_id): new_money})
    await r.hset(f"marriage:data:{marriage_id}", mapping={"money": str(new_money)})

async def update_genius_top(chat_id, user_id, new_score):
    key = f"top:genius:{chat_id}"
    await r.zadd(key, {str(user_id): new_score})

async def update_likes_top(user_id, new_likes):
    await r.zadd("top:likes", {str(user_id): new_likes})

async def update_dislikes_top(user_id, new_dislikes):
    await r.zadd("top:dislikes", {str(user_id): new_dislikes})

async def update_groups_interactive_top(chat_id, new_msgs):
    await r.zadd("top:groups:interactive", {str(chat_id): new_msgs})

async def update_groups_players_top(chat_id, new_earnings):
    await r.zadd("top:groups:players", {str(chat_id): new_earnings})

async def update_money_top(user_id, new_balance):
    await _shared_r.zadd("top:money", {str(user_id): new_balance})

async def get_money_data_old(client=None):
    all_users = await _shared_r.smembers('BankList')
    balance_list = []
    for uid in all_users:
        uid_str = uid.decode() if isinstance(uid, bytes) else uid
        bal_raw = await _shared_r.get(f'{uid_str}:Floos')
        if bal_raw:
            balance_list.append((int(bal_raw), uid_str))
    balance_list.sort(reverse=True)
    result = []
    uids = []
    for bal, uid in balance_list[:20]:
        uids.append(uid)
        result.append({"id": uid, "money": bal})
    if uids:
        names = await get_user_names_batch(uids, client)
        for item in result:
            item["name"] = names.get(item["id"], f"مستخدم {item['id']}")
    my_rank = None
    my_bal = 0
    if client is not None:
        me_obj = getattr(client, "me", None)
        user_id = me_obj.id if me_obj is not None else None
        if user_id:
            for idx, item in enumerate(result):
                if str(item["id"]) == str(user_id):
                    my_rank = idx + 1
                    my_bal = item["money"]
                    break
            if my_rank is None:
                my_bal_raw = await _shared_r.get(f'{user_id}:Floos')
                my_bal = int(my_bal_raw) if my_bal_raw else 0
                for idx, (bal, _) in enumerate(balance_list):
                    if bal == my_bal:
                        my_rank = idx + 1
                        break
    return result, my_rank, my_bal

async def get_money_data_fast(client=None, limit=20):
    results = await _shared_r.zrevrange("top:money", 0, limit-1, withscores=True)
    if results:
        uids = [int(member) for member, _ in results]
        names = await get_user_names_batch(uids, client)
        data = []
        for uid, score in results:
            uid_int = int(uid)
            data.append({
                "id": uid_int,
                "name": names.get(uid_int, f"مستخدم {uid_int}"),
                "money": int(score)
            })
        my_rank = None
        my_bal = 0
        if client and hasattr(client, 'me'):
            me_obj = getattr(client, 'me', None)
            user_id = me_obj.id if me_obj is not None else None
            if user_id:
                for idx, item in enumerate(data):
                    if item["id"] == user_id:
                        my_rank = idx + 1
                        my_bal = item["money"]
                        break
                if my_rank is None:
                    rank = await _shared_r.zrevrank("top:money", str(user_id))
                    if rank is not None:
                        my_rank = rank + 1
                        my_bal = int(await _shared_r.zscore("top:money", str(user_id)) or 0)
        return data, my_rank, my_bal
    old_data, my_rank, my_bal = await get_money_data_old(client)
    if old_data:
        mapping = {str(item["id"]): item["money"] for item in old_data}
        if mapping:
            await _shared_r.zadd("top:money", mapping)
    return old_data, my_rank, my_bal


async def get_thieves_data_old(client=None):
    all_users = await _shared_r.smembers('BankList')
    stolen_list = []
    for uid in all_users:
        uid_str = uid.decode() if isinstance(uid, bytes) else uid
        stolen_raw = await _shared_r.get(f'{uid_str}:Zrf')
        if stolen_raw:
            stolen_list.append((int(stolen_raw), uid_str))
    stolen_list.sort(reverse=True)
    result = []
    uids = []
    for stolen, uid in stolen_list[:20]:
        uids.append(uid)
        result.append({"id": uid, "money": stolen})
    if uids:
        names = await get_user_names_batch(uids, client)
        for item in result:
            item["name"] = names.get(item["id"], f"مستخدم {item['id']}")
    my_rank = None
    my_stolen = 0
    if client is not None:
        me_obj = getattr(client, "me", None)
        user_id = me_obj.id if me_obj is not None else None
        if user_id:
            for idx, item in enumerate(result):
                if str(item["id"]) == str(user_id):
                    my_rank = idx + 1
                    my_stolen = item["money"]
                    break
            if my_rank is None:
                my_stolen_raw = await _shared_r.get(f'{user_id}:Zrf')
                my_stolen = int(my_stolen_raw) if my_stolen_raw else 0
                for idx, (stolen, _) in enumerate(stolen_list):
                    if stolen == my_stolen:
                        my_rank = idx + 1
                        break
    return result, my_rank, my_stolen


async def get_donations_data_old(client=None):
    all_users = await r.smembers('BankList')
    donated_list = []
    for uid in all_users:
        uid_str = uid.decode() if isinstance(uid, bytes) else uid
        donated_raw = await r.get(f'{uid_str}:donated')
        if donated_raw:
            donated_list.append((int(donated_raw), uid_str))
    donated_list.sort(reverse=True)
    result = []
    uids = []
    for donated, uid in donated_list[:20]:
        uids.append(uid)
        result.append({"id": uid, "donated": donated})
    if uids:
        names = await get_user_names_batch(uids, client)
        for item in result:
            item["name"] = names.get(item["id"], f"مستخدم {item['id']}")
    my_rank = None
    my_donated = 0
    if client is not None:
        me_obj = getattr(client, "me", None)
        user_id = me_obj.id if me_obj is not None else None
        if user_id:
            for idx, item in enumerate(result):
                if str(item["id"]) == str(user_id):
                    my_rank = idx + 1
                    my_donated = item["donated"]
                    break
            if my_rank is None:
                my_donated_raw = await r.get(f'{user_id}:donated')
                my_donated = int(my_donated_raw) if my_donated_raw else 0
                for idx, (donated, _) in enumerate(donated_list):
                    if donated == my_donated:
                        my_rank = idx + 1
                        break
    return result, my_rank, my_donated

async def get_interactive_data_old(chat_id, client=None):
    dev = str(Dev_FINAL)
    pattern = f"{dev}{chat_id}:TotalMsgs:*"
    users_keys = await r.keys(pattern)
    result = []
    uids = []
    msgs_dict = {}
    for user_key in users_keys:
        try:
            key = _decode_if_bytes(user_key)
            uid = int(key.split("TotalMsgs:")[1])
            msgs = int(await r.get(user_key) or 0)
            if msgs > 0:
                uids.append(uid)
                msgs_dict[uid] = msgs
        except:
            pass
    if uids:
        names = await get_user_names_batch(uids, client)
        for uid in uids:
            name = names.get(uid, f"مستخدم {uid}")
            result.append({"name": name, "id": uid, "msgs": msgs_dict[uid]})
    result.sort(key=lambda x: x["msgs"], reverse=True)
    return result[:20]

async def get_farmers_data_old(client=None):
    bank_list = await _shared_r.smembers("BankList")
    crops = ["بطاطا", "بندوره", "خس", "خيار", "جزر", "فليفله", "فريز", "ذره", "ثوم", "فطر", "تفاح", "عنب", "زيتون", "موز", "مانجا"]
    result = []
    uids = []
    plants_dict = {}
    for user in bank_list:
        try:
            uid = int(_decode_if_bytes(user))
            farm_name = await _shared_r.get(f"{uid}:farm_name")
            if farm_name:
                uids.append(uid)
        except:
            pass
    if uids:
        for uid in uids:
            total_plants = 0
            crop_keys = [f"{uid}:crop_{crop}" for crop in crops]
            crop_values = await _shared_r.mget(crop_keys)
            for val in crop_values:
                total_plants += int(val) if val else 0
            if total_plants > 0:
                plants_dict[uid] = total_plants
        if plants_dict:
            names = await get_user_names_batch(list(plants_dict.keys()), client)
            for uid in plants_dict:
                name = names.get(uid, f"مستخدم {uid}")
                result.append({"name": name, "id": uid, "plants": plants_dict[uid]})
    result.sort(key=lambda x: x["plants"], reverse=True)
    return result[:20]

async def get_marriage_data_old(chat_id=None, client=None):
    dev = str(Dev_FINAL)
    result = []
    if chat_id:
        marriages = await r.smembers(f"{chat_id}:zwag:{dev}")
    else:
        all_keys = await r.keys(f"*:zwag:{dev}")
        marriages = []
        for key in all_keys:
            marriages.extend(await r.smembers(_decode_if_bytes(key)))
    for marriage in marriages:
        try:
            m_str = _decode_if_bytes(marriage)
            parts = m_str.split('&&')
            if len(parts) >= 1:
                ids = parts[0].split('--')
                if len(ids) >= 2:
                    uid1, uid2 = int(ids[0]), int(ids[1])
                    money = 0
                    for p in parts:
                        if p.startswith('floos='):
                            money = int(p.split('=')[1])
                            break
                    if money > 0:
                        names = await get_user_names_batch([uid1, uid2], client)
                        name_1 = names.get(uid1, f"مستخدم {uid1}")
                        name_2 = names.get(uid2, f"مستخدم {uid2}")
                        result.append({"name_1": name_1, "name_2": name_2, "money": money, "uid1": uid1, "uid2": uid2})
        except:
            pass
    result.sort(key=lambda x: x["money"], reverse=True)
    return result[:20]

async def get_genius_data_old(chat_id, client=None):
    try:
        with open("high_scores.json", "r") as f:
            high_scores = json.load(f)
    except:
        high_scores = {}
    chat_scores = high_scores.get(str(chat_id), {})
    sorted_scores = sorted(chat_scores.items(), key=lambda item: item[1], reverse=True)[:20]
    uids = [int(uid) for uid, _ in sorted_scores]
    result = []
    if uids:
        names = await get_user_names_batch(uids, client)
        for uid, score in sorted_scores:
            uid_int = int(uid)
            name = names.get(uid_int, f"مستخدم {uid}")
            result.append({"name": name[:15], "id": uid_int, "score": score})
    return result

async def get_likes_data_old(data_type, client=None):
    dev = str(Dev_FINAL)
    result = []
    bot_id = None
    try:
        from helpers.context import get_current_bot_id
        bot_id = get_current_bot_id()
        if bot_id:
            bot_id = int(bot_id)
    except:
        pass
    pattern = "global_reactions:*"
    uids = []
    counts_dict = {}
    for key_raw in await r.keys(pattern):
        key = _decode_if_bytes(key_raw)
        try:
            uid = int(key.split("global_reactions:")[1])
            if bot_id and uid == bot_id:
                continue
            data = await r.get(key)
            if data:
                loaded = json.loads(data)
                if data_type == "likes":
                    count = len(loaded.get('likes', []))
                else:
                    count = len(loaded.get('dislikes', []))
                if count > 0:
                    uids.append(uid)
                    counts_dict[uid] = count
        except Exception as e:
            pass
    if uids:
        names = await get_user_names_batch(uids, client)
        for uid in uids:
            name = names.get(uid, f"مستخدم {uid}")
            result.append({"name": name, "id": uid, "count": counts_dict[uid]})
    result.sort(key=lambda x: x["count"], reverse=True)
    return result[:20]

async def get_groups_interactive_data_old(client=None):
    result = []
    for key_raw in await _shared_r.keys(f"{GLOBAL_TOP_NS}:TotalGroupMsgs:*"):
        key = _decode_if_bytes(key_raw)
        try:
            parts = key.split(":TotalGroupMsgs:")
            if len(parts) >= 2:
                gid = int(parts[1])
                msgs = int(await _shared_r.get(key_raw) or 0)
                if msgs > 0:
                    title = await _resolve_group_title(gid, client)
                    if not title:
                        # يُمنع تماماً عرض الـID كاسم بديل — تُستبعد.
                        continue
                    result.append({"name": title, "msgs": msgs})
        except:
            pass
    result.sort(key=lambda x: x["msgs"], reverse=True)
    return result[:20]

async def get_games_earnings_data_old(client=None):
    result = []
    for key_raw in await _shared_r.keys(f"*:game_earnings:{GLOBAL_TOP_NS}"):
        key = _decode_if_bytes(key_raw)
        try:
            parts = key.split(":game_earnings:")
            if len(parts) >= 2:
                chat_id = int(parts[0].rsplit(':', 1)[-1])
                if chat_id >= 0:
                    continue
                earnings = int(await _shared_r.get(key_raw) or 0)
                if earnings > 0:
                    title = await _resolve_group_title(chat_id, client)
                    if not title:
                        continue
                    result.append({"name": title, "earnings": earnings})
        except:
            pass
    result.sort(key=lambda x: x["earnings"], reverse=True)
    return result[:20]

async def get_interactive_data_fast(chat_id, client=None, limit=20):
    key = f"top:interactive:{chat_id}"
    results = await r.zrevrange(key, 0, limit-1, withscores=True)
    if results:
        uids = [int(member) for member, _ in results]
        names = await get_user_names_batch(uids, client)
        data = []
        for uid, score in results:
            uid_int = int(uid)
            data.append({
                "id": uid_int,
                "name": names.get(uid_int, f"مستخدم {uid_int}"),
                "msgs": int(score)
            })
        return data
    old_data = await get_interactive_data_old(chat_id, client)
    if old_data:
        mapping = {str(item["id"]): item["msgs"] for item in old_data}
        if mapping:
            await r.zadd(key, mapping)
    return old_data


async def get_thieves_data_fast(client=None, limit=20):
    all_users = await _shared_r.smembers('BankList')
    stolen_list = []
    for uid in all_users:
        uid_str = uid.decode() if isinstance(uid, bytes) else uid
        stolen_raw = await _shared_r.get(f'{uid_str}:Zrf')
        if stolen_raw:
            stolen_list.append((int(stolen_raw), uid_str))
    stolen_list.sort(reverse=True)
    result = []
    uids = []
    for stolen, uid in stolen_list[:limit]:
        uids.append(uid)
        result.append({"id": uid, "money": stolen})
    if uids:
        names = await get_user_names_batch(uids, client)
        for item in result:
            item["name"] = names.get(item["id"], f"مستخدم {item['id']}")
    
    my_rank = None
    my_stolen = 0
    if client is not None:
        me_obj = getattr(client, "me", None)
        user_id = me_obj.id if me_obj is not None else None
        if user_id:
            for idx, item in enumerate(result):
                if str(item["id"]) == str(user_id):
                    my_rank = idx + 1
                    my_stolen = item["money"]
                    break
            if my_rank is None:
                my_stolen_raw = await _shared_r.get(f'{user_id}:Zrf')
                my_stolen = int(my_stolen_raw) if my_stolen_raw else 0
                for idx, (stolen, _) in enumerate(stolen_list):
                    if stolen == my_stolen:
                        my_rank = idx + 1
                        break
    return result, my_rank, my_stolen


async def get_donations_data_fast(client=None, limit=20):
    results = await r.zrevrange("top:donations", 0, limit-1, withscores=True)
    if results:
        uids = [int(member) for member, _ in results]
        names = await get_user_names_batch(uids, client)
        data = []
        for uid, score in results:
            uid_int = int(uid)
            data.append({
                "id": uid_int,
                "name": names.get(uid_int, f"مستخدم {uid_int}"),
                "donated": int(score)
            })
        my_rank = None
        my_donated = 0
        if client and hasattr(client, 'me'):
            me_obj = getattr(client, 'me', None)
            user_id = me_obj.id if me_obj is not None else None
            if user_id:
                for idx, item in enumerate(data):
                    if item["id"] == user_id:
                        my_rank = idx + 1
                        my_donated = item["donated"]
                        break
                if my_rank is None:
                    rank = await r.zrevrank("top:donations", str(user_id))
                    if rank is not None:
                        my_rank = rank + 1
                        my_donated = int(await r.zscore("top:donations", str(user_id)) or 0)
        return data, my_rank, my_donated
    old_data, my_rank, my_donated = await get_donations_data_old(client)
    if old_data:
        mapping = {str(item["id"]): item["donated"] for item in old_data}
        if mapping:
            await r.zadd("top:donations", mapping)
    return old_data, my_rank, my_donated

async def get_farmers_data_fast(client=None, limit=20):
    key = "top:farmers"
    results = await r.zrevrange(key, 0, limit-1, withscores=True)
    if results:
        uids = [int(member) for member, _ in results]
        names = await get_user_names_batch(uids, client)
        data = []
        for uid, score in results:
            uid_int = int(uid)
            data.append({
                "id": uid_int,
                "name": names.get(uid_int, f"مستخدم {uid_int}"),
                "plants": int(score)
            })
        return data
    old_data = await get_farmers_data_old(client)
    if old_data:
        mapping = {str(item["id"]): item["plants"] for item in old_data}
        if mapping:
            await r.zadd(key, mapping)
    return old_data

async def get_marriage_data_fast(chat_id=None, client=None, limit=20, is_global=False):
    key = "top:marriage:global" if is_global else f"top:marriage:{chat_id}"
    results = await r.zrevrange(key, 0, limit-1, withscores=True)
    if results:
        marriage_ids = [int(member) for member, _ in results]
        data = []
        for mid, score in results:
            mid_int = int(mid)
            marriage_info = await r.hgetall(f"marriage:data:{mid_int}")
            if marriage_info:
                parts = marriage_info.get("parts", "").split('--')
                if len(parts) >= 2:
                    try:
                        uid1, uid2 = int(parts[0]), int(parts[1])
                    except ValueError:
                        # قيد بيانات تالف (تم كتابته قبل هذا الإصلاح بأسماء
                        # بدل آيديات) — يُتجاهل هذا السجل بدل تعطيل التوب
                        # كاملاً لبقية المجموعة.
                        continue
                    names = await get_user_names_batch([uid1, uid2], client)
                    name_1 = names.get(uid1, f"مستخدم {uid1}")
                    name_2 = names.get(uid2, f"مستخدم {uid2}")
                    data.append({
                        "name_1": name_1,
                        "name_2": name_2,
                        "money": int(score)
                    })
        return data
    old_data = await get_marriage_data_old(chat_id, client)
    if old_data:
        import random
        for item in old_data:
            mid = random.randint(100000, 999999)
            await r.zadd(key, {str(mid): item["money"]})
            uid1 = item.get("uid1")
            uid2 = item.get("uid2")
            if uid1 is not None and uid2 is not None:
                # يُخزَّن آيدي المستخدمين هنا (وليس الاسم) لأن القراءة السريعة
                # أعلاه تتوقع "uid1--uid2" وتحوّلها بـ int() — هذا هو إصلاح
                # الخطأ الذي كان يحفظ الأسماء هنا بدل الآيديات فيفشل لاحقاً.
                await r.hset(f"marriage:data:{mid}", mapping={"parts": f"{uid1}--{uid2}"})
    return old_data

async def get_genius_data_fast(chat_id, client=None, limit=20):
    key = f"top:genius:{chat_id}"
    results = await r.zrevrange(key, 0, limit-1, withscores=True)
    if results:
        uids = [int(member) for member, _ in results]
        names = await get_user_names_batch(uids, client)
        data = []
        for uid, score in results:
            uid_int = int(uid)
            data.append({
                "id": uid_int,
                "name": names.get(uid_int, f"مستخدم {uid_int}"),
                "score": int(score)
            })
        return data
    old_data = await get_genius_data_old(chat_id, client)
    if old_data:
        mapping = {str(item["id"]): item["score"] for item in old_data}
        if mapping:
            await r.zadd(key, mapping)
    return old_data

async def get_likes_data_fast(data_type, client=None, limit=20):
    # نستخدم نفس مصدر الحقيقة ونفس منطق أمر الكتابة في identity.py
    # (get_likes_top_global) بدل الاعتماد على top:likes / top:dislikes
    # في Redis، لأن هذه المجموعة لا تُحدَّث عند حدوث لايك/دسلايك فعلي
    # وبالتالي تصبح قديمة ومختلفة عن نتيجة الأمر بالنص.
    from ..identity import get_likes_top_global
    data = await get_likes_top_global(data_type, client)
    return data[:limit]

async def _resolve_group_title(gid_int, client):
    """يعيد اسم المجموعة الحقيقي إن أمكن الحصول عليه (من الكاش المشترك، أو
    حياً عبر client.get_chat عند توفره)، أو None إن تعذّر ذلك تماماً —
    ولا يُعيد أبداً شكلاً بديلاً يحتوي على رقم المجموعة (Chat ID)، حتى لا
    يظهر أي ID في توب المجموعات مهما كانت الحالة. على المستدعي استبعاد أي
    مجموعة يُعاد لها None بدل عرضها.

    غالب حالات الفشل التام سببها أن البوت لم يعد عضواً في تلك المجموعة —
    وهذا قيد من تيليجرام نفسه (لا يسمح بجلب اسم مجموعة البوت ليس عضواً
    فيها) لا يوجد له حل برمجي سوى استبعاد تلك المجموعة من العرض، وهو ما
    تفعله هذه الدالة الآن."""
    title = await _shared_r.get(f'{gid_int}:chat_title:{GLOBAL_TOP_NS}')
    if isinstance(title, bytes):
        title = title.decode('utf-8')
    if title:
        return title
    if client is not None:
        live_title = await get_chat_name_from_api(gid_int, client)
        if live_title and not live_title.startswith("Chat "):
            return live_title
    return None


async def get_groups_interactive_data_fast(limit=20, client=None):
    key = "top:groups:interactive"
    # نجلب نافذة مرشّحين أوسع من limit (بحد أقصى معقول) لأن بعض المجموعات
    # قد يتعذّر حل اسمها كلياً (البوت غادرها) فتُستبعد — هذا يعوّض النقص
    # ويحافظ على عرض limit مجموعة حقيقية الاسم متى توفّر عدد كافٍ منها،
    # بدل الاكتفاء بأول limit وعرض بعضها كـID.
    candidate_count = min(limit * 4, 200)
    results = await r.zrevrange(key, 0, candidate_count - 1, withscores=True)
    if results:
        data = []
        for gid, score in results:
            if len(data) >= limit:
                break
            gid_int = int(gid)
            title = await _resolve_group_title(gid_int, client)
            if not title:
                # يُمنع تماماً عرض الـID كاسم بديل — تُستبعد هذه المجموعة.
                continue
            data.append({
                "name": title,
                "msgs": int(score)
            })
        return data
    old_data = await get_groups_interactive_data_old(client)
    if old_data:
        for key_raw in await _shared_r.keys(f"{GLOBAL_TOP_NS}:TotalGroupMsgs:*"):
            key = _decode_if_bytes(key_raw)
            try:
                gid = int(key.split(":TotalGroupMsgs:")[1])
                title = await _shared_r.get(f'{gid}:chat_title:{GLOBAL_TOP_NS}')
                if isinstance(title, bytes):
                    title = title.decode('utf-8')
                if not title:
                    continue
                for item in old_data:
                    if item["name"] == title:
                        await r.zadd("top:groups:interactive", {str(gid): item["msgs"]})
                        break
            except:
                pass
    return old_data

async def get_groups_players_data_fast(limit=20, client=None):
    key = "top:groups:players"
    candidate_count = min(limit * 4, 200)
    results = await r.zrevrange(key, 0, candidate_count - 1, withscores=True)
    if results:
        data = []
        for gid, score in results:
            if len(data) >= limit:
                break
            gid_int = int(gid)
            title = await _resolve_group_title(gid_int, client)
            if not title:
                continue
            data.append({
                "name": title,
                "earnings": int(score)
            })
        return data
    old_data = await get_games_earnings_data_old(client)
    if old_data:
        for key_raw in await _shared_r.keys(f"*:game_earnings:{GLOBAL_TOP_NS}"):
            key = _decode_if_bytes(key_raw)
            try:
                parts = key.split(":game_earnings:")
                if len(parts) >= 2:
                    chat_id = int(parts[0].rsplit(':', 1)[-1])
                    if chat_id >= 0:
                        continue
                    earnings = int(await _shared_r.get(key_raw) or 0)
                    if earnings > 0:
                        await r.zadd("top:groups:players", {str(chat_id): earnings})
            except:
                pass
    return old_data

def format_top_text(data, title, key_name, suffix="", is_global=False, user_id=None):
    if not data:
        return f"{k} لا توجد بيانات لعرضها حالياً.\n_"
    text = f" • توب اعلى 20 {title} {'في البوت' if is_global else 'بالقروب'}\n\n"
    emojis = ["🥇", "🥈", "🥉"]
    for i, item in enumerate(data[:20]):
        emoji = emojis[i] if i < 3 else f"{i+1:>4})"
        name = item.get("name", "غير معروف")
        value = item.get(key_name, 0)
        text += f"{emoji} {value:,} {suffix} l {name}\n"
    if user_id is not None:
        my_rank = None
        my_value = 0
        for i, item in enumerate(data):
            if item.get("id") == user_id:
                my_rank = i + 1
                my_value = item.get(key_name, 0)
                break
        if my_rank is not None:
            label_map = {
                "money": "فلوسك",
                "msgs": "رسايلك",
                "donated": "تبرعت",
                "count": "عددك",
                "score": "نقاطك",
                "plants": "نباتاتك"
            }
            label = label_map.get(key_name, "قيمتك")
            text += f"\n• مركزك ↤︎ {my_rank} \n• {label} ↤︎ {my_value:,} {suffix}"
    return text

async def get_top_text(chat_id, user_id, data_type, client=None, force_refresh=False):
    k = get_global_k()
    cache_key = f"top:{data_type}:{chat_id}:{user_id}"
    if not force_refresh:
        cached = _get_cached(cache_key)
        if cached:
            return cached

    # مصدر البيانات الوحيد لكل الأنواع (عدا الغزاة، الذي يبقى حياً كما كان)
    # هو الـSnapshot المشترك — نفسه الذي تقرأ منه أزرار التوب أيضاً، فلا
    # يوجد حساب مختلف بين النص والأزرار، ولا حساب ثقيل عند طلب المستخدم.
    snap_chat_id = chat_id if data_type in SNAPSHOT_LOCAL_TYPES else None

    if data_type == "invaders":
        text = await get_invaders_top()
    elif data_type == "interactive":
        data = await get_top_snapshot("interactive", client, chat_id=snap_chat_id)
        text = format_top_text(data, "متفاعلين", "msgs", user_id=user_id)
    elif data_type == "money":
        data, my_rank, my_bal = await get_top_snapshot("money", client)
        text = "<b>توب الفلوس</b>\n\n"
        emojis = ["🥇", "🥈", "🥉"]
        for i, item in enumerate(data[:10]):
            emo = emojis[i] if i < 3 else f"{i+1})"
            text += f"{emo} {item['money']:,}💰 l {item['name'][:15]}\n"
        if my_rank is not None:
            text += f"\n━━━━━━━━━\n• مركزك ↤︎ {my_rank} \n• فلوسك ↤︎ {my_bal:,} ﷼"
    elif data_type == "thieves":
        data, my_rank, my_stolen = await get_top_snapshot("thieves", client)
        text = "<b>توب الحرامية</b>\n\n"
        emojis = ["🥇", "🥈", "🥉"]
        for i, item in enumerate(data[:10]):
            emo = emojis[i] if i < 3 else f"{i+1})"
            text += f"{emo} {item['money']:,}💰 l {item['name'][:15]}\n"
        if my_rank is not None:
            text += f"\n━━━━━━━━━\n• مركزك ↤︎ {my_rank} \n• سرقت ↤︎ {my_stolen:,} ﷼"
    elif data_type == "donations":
        data, my_rank, my_donated = await get_top_snapshot("donations", client)
        text = "<b>توب المتبرعين</b>\n\n"
        emojis = ["🥇", "🥈", "🥉"]
        for i, item in enumerate(data[:10]):
            emo = emojis[i] if i < 3 else f"{i+1})"
            text += f"{emo} {item['donated']:,}💰 l {item['name'][:15]}\n"
        if my_rank is not None:
            text += f"\n━━━━━━━━━\n• مركزك ↤︎ {my_rank} \n• تبرعت ↤︎ {my_donated:,} ﷼"
    elif data_type == "farmers":
        data = await get_top_snapshot("farmers", client)
        if not data:
            text = f"{k} لا يوجد مزارع بعد\n_"
        else:
            text = " • توب اعلى 20 مزرعه في البوت\n\n"
            emojis = ["🥇", "🥈", "🥉"]
            for i, farmer in enumerate(data[:20]):
                emoji = emojis[i] if i < 3 else f"{i+1:>4})"
                name = farmer["name"][:15]
                text += f"{emoji} {farmer['plants']:,} l {name}\n"
    elif data_type == "marriage_global":
        data = await get_top_snapshot("marriage_global", client)
        if not data:
            text = f"{k} لا توجد زواجات مسجلة\n_"
        else:
            text = " • توب اعلى 20 زواج في البوت\n\n"
            emojis = ["🥇", "🥈", "🥉"]
            for i, marriage in enumerate(data[:20]):
                emoji = emojis[i] if i < 3 else f"{i+1:>4})"
                text += f"{emoji} {marriage['money']:,} l {marriage['name_1'][:15]} 🤝 {marriage['name_2'][:15]}\n"
    elif data_type == "marriage_local":
        data = await get_top_snapshot("marriage_local", client, chat_id=chat_id)
        if not data:
            text = f"{k} لا توجد زواجات في هذا القروب\n_"
        else:
            text = " • توب اعلى 20 زواج بالقروب\n\n"
            emojis = ["🥇", "🥈", "🥉"]
            for i, marriage in enumerate(data[:20]):
                emoji = emojis[i] if i < 3 else f"{i+1:>4})"
                text += f"{emoji} {marriage['money']:,} l {marriage['name_1'][:15]} 🤝 {marriage['name_2'][:15]}\n"
    elif data_type == "genius":
        data = await get_top_snapshot("genius", client, chat_id=chat_id)
        if not data:
            text = f"{k} لا يوجد لاعبين مسجلين حتى الآن.\n\nللعب: اكتب <code>عبقري</code>"
        else:
            text = " • توب اعلى 20 عبقري بالقروب\n\n"
            emojis = ["🥇", "🥈", "🥉"]
            for i, item in enumerate(data[:20]):
                emoji = emojis[i] if i < 3 else f"{i+1:>4})"
                text += f"{emoji} {item['score']:,} l {item['name']}\n"
    elif data_type == "likes":
        from ..identity import get_user_like_emoji
        data = await get_top_snapshot("likes", client)
        if not data:
            text = f"{k} لا توجد بيانات لعرضها حالياً.\n_"
        else:
            text = " • توب اعلى 20 لايك في البوت\n\n"
            emojis = ["🥇", "🥈", "🥉"]
            for i, item in enumerate(data[:20]):
                emoji = emojis[i] if i < 3 else f"{i+1:>4})"
                name = item.get("name", "مستخدم")
                item_user_id = item.get("id")
                like_emoji = await get_user_like_emoji(item_user_id)
                text += f"{emoji} {item['count']:,} {like_emoji} l {name}\n"
    elif data_type == "dislikes":
        from ..identity import get_user_dislike_emoji
        data = await get_top_snapshot("dislikes", client)
        if not data:
            text = f"{k} لا توجد بيانات لعرضها حالياً.\n_"
        else:
            text = " • توب اعلى 20 دسلايك في البوت\n\n"
            emojis = ["🥇", "🥈", "🥉"]
            for i, item in enumerate(data[:20]):
                emoji = emojis[i] if i < 3 else f"{i+1:>4})"
                name = item.get("name", "مستخدم")
                item_user_id = item.get("id")
                dislike_emoji = await get_user_dislike_emoji(item_user_id)
                text += f"{emoji} {item['count']:,} {dislike_emoji} l {name}\n"
    elif data_type == "groups_interactive":
        data = await get_top_snapshot("groups_interactive", client)
        if not data:
            text = f"{k} لا توجد مجموعات مسجلة بعد\n_"
        else:
            text = " • توب اكثر 20 قروب متفاعلين في البوت\n\n"
            emojis = ["🥇", "🥈", "🥉"]
            for i, group in enumerate(data[:20]):
                emoji = emojis[i] if i < 3 else f"{i+1:>4})"
                text += f"{emoji} {group['msgs']:,} l {group['name'][:35]}\n"
    elif data_type == "groups_players":
        data = await get_top_snapshot("groups_players", client)
        if not data:
            text = f"{k} لا توجد مجموعات مسجلة في توب الألعاب بعد\n_"
        else:
            text = " • توب اكثر 20 قروب يلعبون في البوت\n\n"
            emojis = ["🥇", "🥈", "🥉"]
            for i, group in enumerate(data[:20]):
                emoji = emojis[i] if i < 3 else f"{i+1:>4})"
                text += f"{emoji} {group['earnings']:,} l {group['name'][:35]}\n"
    else:
        text = f"{k} حدث خطأ: نوع البيانات غير معروف"

    if data_type != "invaders" and not text.startswith(f"{k} حدث خطأ"):
        text += "\n\n- يتم تحديث التوبات كل 10 دقائق ."

    _set_cached(cache_key, text)
    return text

async def get_invaders_top():
    try:
        NS = "gozat"
        LEVEL_ORDER = ["الضعيف", "برونزي", "فضي", "ماسي"]
        level_emoji = {"ماسي": "🥇", "فضي": "🥈", "برونزي": "🥉", "الضعيف": ""}
        medals = ["🥇", "🥈", "🥉"]
        all_tids = await _shared_r.smembers(f"{NS}:teams")
        teams = []
        for tid_raw in all_tids:
            tid = _decode_if_bytes(tid_raw)
            team_data = await _shared_r.hgetall(f"{NS}:team:{tid}")
            if not team_data:
                continue
            team = {k: _decode_if_bytes(v) for k, v in team_data.items()}
            points = int(team.get("points") or 0)
            if points <= 0:
                continue
            if points >= 2000:
                level = "ماسي"
            elif points >= 401:
                level = "فضي"
            elif points > 200:
                level = "برونزي"
            else:
                level = "الضعيف"
            teams.append((level, points, team.get("name"), team.get("owner"), team.get("hidden"), team.get("attack")))
        grouped = {lv: [] for lv in LEVEL_ORDER}
        for level, points, name, owner, hidden, attack in teams:
            grouped[level].append((points, name, owner, hidden, attack))
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
                    block.append(f"{badge} ) {points:,} 🏅  l  {name}    l   {display_code}")
            blocks.append("\n".join(block))
        return f"{k}\n\n" + "\n\n\n".join(blocks)
    except Exception as e:
        return f"{k} لا توجد بيانات للغزاة حالياً.\n_"

async def build_main_top_keyboard(chat_id, user_id, active_type=None):
    if active_type is not None:
        keyboard = [
            [InlineKeyboardButton("رجوع", callback_data=f"top_main:back:{chat_id}:{user_id}")],
            [InlineKeyboardButton("اخفاء التوب", callback_data=f"top_main:close:{chat_id}:{user_id}")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    buttons_config = [
        [{"id": "top_invaders", "default": "توب الغزاة 🏅", "type": "invaders"}],
        [
            {"id": "top_genius", "default": "توب العباقرة", "type": "genius"},
            {"id": "top_interactive", "default": "توب المتفاعلين", "type": "interactive"}
        ],
        [
            {"id": "top_farmers", "default": "توب المزارع", "type": "farmers"},
            {"id": "top_donations", "default": "توب المتبرعين", "type": "donations"}
        ],
        [
            {"id": "top_money", "default": "توب الفلوس", "type": "money"},
            {"id": "top_thieves", "default": "توب الحراميه", "type": "thieves"}
        ],
        [
            {"id": "top_marriage_local", "default": "الزواج القروب", "type": "marriage_local"},
            {"id": "top_marriage_global", "default": "الزواج العام", "type": "marriage_global"}
        ],
        [
            {"id": "top_likes", "default": "توب اللايكات", "type": "likes"},
            {"id": "top_groups", "default": "توب القروبات", "type": "groups"}
        ],
        [{"id": "top_close", "default": "اخفاء التوب", "type": "close"}]
    ]

    keyboard = []
    for row in buttons_config:
        row_buttons = []
        for btn in row:
            btn_dict = await create_button_raw(
                "top",
                btn["id"],
                btn["default"],
                callback_data=f"top_main:{btn['type']}:{chat_id}:{user_id}"
            )
            row_buttons.append(InlineKeyboardButton(**btn_dict))
        keyboard.append(row_buttons)

    return InlineKeyboardMarkup(keyboard)

async def build_invaders_keyboard(chat_id, user_id):
    keyboard = [
        [InlineKeyboardButton("رجوع", callback_data=f"invaders:invaders_back:{chat_id}:{user_id}")],
        [InlineKeyboardButton("اخفاء التوب", callback_data=f"invaders:invaders_close:{chat_id}:{user_id}")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def build_groups_keyboard(chat_id, user_id):
    keyboard = []
    row_buttons = []
    for btn_def in BUTTONS_DEFINITIONS["groups"]["buttons"]:
        if btn_def["id"] in ["groups_back", "groups_close"]:
            continue
        btn = await create_button_raw(
            "groups",
            btn_def["id"],
            btn_def["default"],
            callback_data=f"groups:{btn_def['id']}:{chat_id}:{user_id}"
        )
        row_buttons.append(InlineKeyboardButton(**btn))
    keyboard.append(row_buttons)
    keyboard.append([InlineKeyboardButton("رجوع", callback_data=f"groups:groups_back:{chat_id}:{user_id}")])
    keyboard.append([InlineKeyboardButton("اخفاء التوب", callback_data=f"groups:groups_close:{chat_id}:{user_id}")])
    return InlineKeyboardMarkup(keyboard)

async def build_likes_keyboard(chat_id, user_id):
    keyboard = []
    row_buttons = []
    for btn_def in BUTTONS_DEFINITIONS["likes"]["buttons"]:
        if btn_def["id"] in ["likes_back", "likes_close"]:
            continue
        btn = await create_button_raw(
            "likes",
            btn_def["id"],
            btn_def["default"],
            callback_data=f"likes:{btn_def['id']}:{chat_id}:{user_id}"
        )
        row_buttons.append(InlineKeyboardButton(**btn))
    keyboard.append(row_buttons)
    keyboard.append([InlineKeyboardButton("رجوع", callback_data=f"likes:likes_back:{chat_id}:{user_id}")])
    keyboard.append([InlineKeyboardButton("اخفاء التوب", callback_data=f"likes:likes_close:{chat_id}:{user_id}")])
    return InlineKeyboardMarkup(keyboard)

async def get_user_name(uid, client=None):
    name = await _shared_r.get(f"{uid}:bankName")
    if not name:
        name = await _shared_r.get(f"{uid}:first_name")
    if isinstance(name, bytes):
        name = name.decode('utf-8')
    if name:
        name = name.strip()
    if name and not name.startswith('@') and name != str(uid):
        return name
    if client is not None:
        try:
            user_obj = await client.get_users(int(uid))
            live_name = (user_obj.first_name or '').strip()
            if live_name and not live_name.startswith('@'):
                await _shared_r.set(f"{uid}:bankName", live_name)
                return live_name
        except Exception:
            pass
    return None

async def get_user_names_batch(uids, client=None):
    names = {}
    keys = [f"{uid}:bankName" for uid in uids]
    values = await _shared_r.mget(keys)
    for uid, name in zip(uids, values):
        if name:
            if isinstance(name, bytes):
                name = name.decode('utf-8')
            if name and not name.startswith('@') and name != str(uid):
                names[uid] = name
    missing = [uid for uid in uids if uid not in names]
    if missing and client is not None:
        for uid in missing:
            try:
                user_obj = await client.get_users(int(uid))
                live_name = (user_obj.first_name or '').strip()
                if live_name and not live_name.startswith('@'):
                    await _shared_r.set(f"{uid}:bankName", live_name)
                    names[uid] = live_name
            except Exception:
                pass
    return names

async def edit_message_text(client, chat_id, message_id, text, parse_mode=ParseMode.HTML, reply_markup=None, disable_web_page_preview=False):
    await client.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        parse_mode=parse_mode,
        reply_markup=reply_markup,
        disable_web_page_preview=disable_web_page_preview
    )

@Client.on_callback_query(filters.regex(r"^(top_main:|invaders:|groups:|top:|likes:)"), group=-25)
async def top_callback_handler(client, callback_query):
    await callback_query.answer()
    data = callback_query.data
    chat_id = callback_query.message.chat.id
    message_id = callback_query.message.id
    user_id = callback_query.from_user.id

    if data.startswith("invaders:"):
        parts = data.split(":")
        if len(parts) >= 4:
            action = parts[1]
            target_chat_id = int(parts[2])
            target_user_id = int(parts[3])
            if user_id != target_user_id:
                await callback_query.answer(REPLIES['plugins_games_top_1064'], show_alert=True)
                return
            if action == "invaders_back":
                text = f"• اهلا بك في قائمة التوبات:\n_"
                markup = await build_main_top_keyboard(chat_id, user_id, active_type=None)
                await edit_message_text(client, chat_id, message_id, text, reply_markup=markup)
                return
            elif action == "invaders_close":
                await edit_message_text(client, chat_id, message_id, "• تم اخفاء التوب")
                return

    if data.startswith("groups:"):
        parts = data.split(":")
        if len(parts) >= 4:
            action = parts[1]
            target_chat_id = int(parts[2])
            target_user_id = int(parts[3])
            if user_id != target_user_id:
                await callback_query.answer(REPLIES['plugins_games_top_1064'], show_alert=True)
                return
            if action == "groups_back":
                text = f"• اهلا بك في قائمة التوبات:\n_"
                markup = await build_main_top_keyboard(chat_id, user_id, active_type=None)
                await edit_message_text(client, chat_id, message_id, text, reply_markup=markup)
                return
            elif action == "groups_close":
                await edit_message_text(client, chat_id, message_id, "• تم اخفاء التوب")
                return
            elif action == "groups_players":
                text = await get_top_text(chat_id, user_id, "groups_players", client)
                markup = await build_groups_keyboard(chat_id, user_id)
                await edit_message_text(client, chat_id, message_id, text, reply_markup=markup, disable_web_page_preview=True)
                return
            elif action == "groups_interactive":
                text = await get_top_text(chat_id, user_id, "groups_interactive", client)
                markup = await build_groups_keyboard(chat_id, user_id)
                await edit_message_text(client, chat_id, message_id, text, reply_markup=markup, disable_web_page_preview=True)
                return

    if data.startswith("likes:"):
        parts = data.split(":")
        if len(parts) >= 4:
            action = parts[1]
            target_chat_id = int(parts[2])
            target_user_id = int(parts[3])
            if user_id != target_user_id:
                await callback_query.answer(REPLIES['plugins_games_top_1064'], show_alert=True)
                return
            if action == "likes_back":
                text = f"• اهلا بك في قائمة التوبات\n_"
                markup = await build_main_top_keyboard(chat_id, user_id, active_type=None)
                await edit_message_text(client, chat_id, message_id, text, reply_markup=markup)
                return
            elif action == "likes_close":
                await edit_message_text(client, chat_id, message_id, "• تم اخفاء التوب")
                return
            elif action == "likes_show":
                text = await get_top_text(chat_id, user_id, "likes", client)
                markup = await build_likes_keyboard(chat_id, user_id)
                await edit_message_text(client, chat_id, message_id, text, reply_markup=markup, disable_web_page_preview=True)
                return
            elif action == "dislikes_show":
                text = await get_top_text(chat_id, user_id, "dislikes", client)
                markup = await build_likes_keyboard(chat_id, user_id)
                await edit_message_text(client, chat_id, message_id, text, reply_markup=markup, disable_web_page_preview=True)
                return

    if data.startswith("top_main:"):
        parts = data.split(":")
        if len(parts) >= 2 and parts[1] == "close":
            await edit_message_text(client, chat_id, message_id, "• تم اخفاء التوب")
            return
        elif len(parts) >= 4 and parts[1] == "back":
            target_chat_id = int(parts[2])
            target_user_id = int(parts[3])
            if user_id != target_user_id:
                await callback_query.answer(REPLIES['plugins_games_top_1064'], show_alert=True)
                return
            text = f"• اهلا بك في قائمة التوبات:\n_"
            markup = await build_main_top_keyboard(chat_id, user_id, active_type=None)
            await edit_message_text(client, chat_id, message_id, text, reply_markup=markup)
            return
        elif len(parts) >= 4 and parts[1] == "groups":
            target_chat_id = int(parts[2])
            target_user_id = int(parts[3])
            if user_id != target_user_id:
                await callback_query.answer(REPLIES['plugins_games_top_1064'], show_alert=True)
                return
            text = "• أهلاً بك عزيزي اختر نوع التوب للمجموعات الذي تريد عرضه:\n_"
            markup = await build_groups_keyboard(chat_id, user_id)
            await edit_message_text(client, chat_id, message_id, text, reply_markup=markup)
            return
        elif len(parts) >= 4 and parts[1] == "likes":
            target_chat_id = int(parts[2])
            target_user_id = int(parts[3])
            if user_id != target_user_id:
                await callback_query.answer(REPLIES['plugins_games_top_1064'], show_alert=True)
                return
            text = "• أهلاً بك عزيزي اختار نوع التوب للايدي الذي تريد عرضه:\n_"
            markup = await build_likes_keyboard(chat_id, user_id)
            await edit_message_text(client, chat_id, message_id, text, reply_markup=markup)
            return
        elif len(parts) >= 4 and parts[1] == "invaders":
            target_chat_id = int(parts[2])
            target_user_id = int(parts[3])
            if user_id != target_user_id:
                await callback_query.answer(REPLIES['plugins_games_top_1064'], show_alert=True)
                return
            text = await get_top_text(target_chat_id, target_user_id, "invaders", client)
            markup = await build_invaders_keyboard(chat_id, user_id)
            await edit_message_text(client, chat_id, message_id, text, reply_markup=markup, disable_web_page_preview=True)
            return
        elif len(parts) >= 4:
            data_type = parts[1]
            target_chat_id = int(parts[2])
            target_user_id = int(parts[3])
            if user_id != target_user_id:
                await callback_query.answer(REPLIES['plugins_games_top_1064'], show_alert=True)
                return
            text = await get_top_text(target_chat_id, target_user_id, data_type, client)
            markup = await build_main_top_keyboard(chat_id, user_id, active_type=data_type)
            await edit_message_text(client, chat_id, message_id, text, reply_markup=markup, disable_web_page_preview=True)
            return

async def get_top_interactive(c, m, k, channel):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if await r.get(f'{m.chat.id}:disableTop:{Dev_FINAL}'):
        return await m.reply(plugins_games_top_1193(k))

    # لا يوجد أي حساب/تجميع من Redis هنا: القائمة الرئيسية أزرار فقط، وكل
    # نوع توب يُقرأ من الـSnapshot المشترك (helpers/top_snapshot) فقط عند
    # فتح زره فعلياً — وليس عند مجرد كتابة "توب".
    text = f"• اهلا بك في قائمة التوبات:\n_"
    markup = await build_main_top_keyboard(m.chat.id, m.from_user.id, active_type=None)
    await m.reply(text, reply_markup=markup, parse_mode=ParseMode.HTML)

async def handle_top_settings(c, m, k, text):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if text == "تعطيل التوب":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_games_top_1216(k))
        if await r.get(f'{m.chat.id}:disableTop:{Dev_FINAL}'):
            return await m.reply(plugins_games_top_1218(k, m.from_user.mention(), k))
        await r.set(f'{m.chat.id}:disableTop:{Dev_FINAL}', 1)
        return await m.reply(plugins_games_top_1220(k, m.from_user.mention(), k))
    elif text == "تفعيل التوب":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_games_top_1223(k))
        if not await r.get(f'{m.chat.id}:disableTop:{Dev_FINAL}'):
            return await m.reply(plugins_games_top_1225(k, m.from_user.mention(), k))
        await r.delete(f'{m.chat.id}:disableTop:{Dev_FINAL}')
        return await m.reply(plugins_games_top_1227(k, m.from_user.mention(), k))
    return None