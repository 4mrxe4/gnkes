from helpers.context import get_global_r, get_global_dev, get_global_k
r = get_global_r()
Dev_FINAL = get_global_dev()
k = get_global_k()
k = get_global_k()
Dev_FINAL = get_global_dev()
r = get_global_r()
from helpers.context import get_global_r, get_global_dev, get_global_k

import random, asyncio, json, time
from compat import *
from compat import *
from helpers.ranks import *
from compat import Client
from helpers.replies_store import (
    REPLIES,
    plugins_games_roulette_238,
    plugins_games_roulette_239,
    plugins_games_roulette_252,
    plugins_games_roulette_254,
    plugins_games_roulette_260,
    plugins_games_roulette_265,
    plugins_games_roulette_272,
    plugins_games_roulette_279,
    plugins_games_roulette_281,
    plugins_games_roulette_283,
    plugins_games_roulette_285,
    plugins_games_roulette_297,
    plugins_games_roulette_305,
    plugins_games_roulette_309,
    plugins_games_roulette_330,
    plugins_games_roulette_352,
    plugins_games_roulette_357,
    plugins_games_roulette_397,
    plugins_games_roulette_402,
    plugins_games_roulette_420,
    plugins_games_roulette_431,
    plugins_games_roulette_434,
    plugins_games_roulette_443,
    plugins_games_roulette_448,
    plugins_games_roulette_449,
    plugins_games_roulette_462,
    plugins_games_roulette_464,
    plugins_games_roulette_471,
    plugins_games_roulette_477,
    plugins_games_roulette_484,
    plugins_games_roulette_485,
    plugins_games_roulette_498,
    plugins_games_roulette_500,
    plugins_games_roulette_507,
    plugins_games_roulette_512,
    plugins_games_roulette_600,
    plugins_games_roulette_672,
    plugins_games_roulette_683,
    plugins_games_roulette_716,
    plugins_games_roulette_755,
    plugins_games_roulette_757,
    plugins_games_roulette_774,
    plugins_games_roulette_776,
    plugins_games_roulette_797,
    plugins_games_roulette_799,
    plugins_games_roulette_820,
)

AQAB_PUNISHMENTS = [
    "ارقص دقيقتين",
    "اطلع برا المجموعة وارجع",
    "اكتب اسمك بالعكس",
    "قل نكتة بايخة",
    "غني اغنية طفولية",
    "اقرأ اخر ٣ رسايل من شاتك الخاص",
    "حط ستوري عن العقاب",
    "غير اسمك لاسم مضحك",
    "صيح فد وحدة بالمجموعة",
    "سوي حركة غبية"
]

_ROLET_GAME_TTL = 1800
_ROLET_UPDATE_INTERVAL = 5
_ROLET_LOCK_VAL = "1"

_ROLET_TASKS = {}

def _rolet_keys(chat_id, dev):
    return {
        "active": f'{chat_id}:ROLET_ACTIVE:{dev}',
        "lock": f'{chat_id}:ROLET_STARTLOCK:{dev}',
        "game": f'{chat_id}:ROLETGAME:{dev}',
        "list": f'{chat_id}:ListRolet:{dev}',
        "time": f'{chat_id}:ROLET_TIME:{dev}',
    }

def _rolet_cancel_task(chat_id):
    task = _ROLET_TASKS.pop(chat_id, None)
    if task and not task.done():
        task.cancel()

def format_time(seconds):
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"

async def _rolet_time_checker(c, chat_id, dev, k, creator_id, winners_count):
    r_local = get_global_r()
    keys = _rolet_keys(chat_id, dev)
    
    start_time = int(time.time())
    
    try:
        while True:
            await asyncio.sleep(5)
            
            if not await r_local.sismember(keys["active"], _ROLET_LOCK_VAL):
                break
            if await r_local.sismember(keys["lock"], _ROLET_LOCK_VAL):
                break
            
            elapsed = int(time.time()) - start_time
            remaining = _ROLET_GAME_TTL - elapsed
            
            if remaining <= 0:
                game_data = await r_local.hgetall(keys["game"])
                players = await r_local.smembers(keys["list"])
                
                if len(players) > 0:
                    player_ids = [int(pid.decode() if isinstance(pid, bytes) else pid) for pid in players]
                    random.shuffle(player_ids)
                    
                    try:
                        winners_count = int(game_data.get('winners', '1') or '1')
                    except (TypeError, ValueError):
                        winners_count = 1
                    
                    if len(player_ids) < winners_count:
                        winners_count = len(player_ids)
                    
                    selected_winners = player_ids[:winners_count]
                    
                    result_text = f"{k} انتهى وقت الروليت\n\n{k} الفائزين :\n\n"
                    for i, winner_id in enumerate(selected_winners, 1):
                        try:
                            get_user = await c.get_users(winner_id)
                            result_text += f"{i}- {get_user.mention()}\n"
                        except:
                            result_text += f"{i}- {winner_id}\n"
                    
                    try:
                        msg_id = int(game_data.get('msg_id', '0') or '0')
                        if msg_id:
                            await c.delete_messages(chat_id, msg_id)
                        await c.send_message(chat_id, result_text)
                    except Exception as e:
                        print(f"Error in rolet time checker: {e}")
                    
                    await r.delete(keys["active"], keys["game"], keys["list"], keys["lock"], keys["time"])
                    _rolet_cancel_task(chat_id)
                    break
                
                await r.delete(keys["active"], keys["game"], keys["list"], keys["lock"], keys["time"])
                _rolet_cancel_task(chat_id)
                break
            
            try:
                msg_id = int((await r_local.hgetall(keys["game"])).get('msg_id', '0') or '0')
                if msg_id:
                    keyboard = InlineKeyboardMarkup([
                        [InlineKeyboardButton("مشاركة", callback_data=f"rolet_join_{creator_id}")],
                        [InlineKeyboardButton("بدء الروليت", callback_data=f"rolet_start_{creator_id}")]
                    ])
                    await c.edit_message_text(
                        chat_id,
                        msg_id,
                        f'''{k} مرحباً بكم في لعبة الروليت

- يمكنكم التسجيل فيها عن طريق ضغط زر مشاركة

• عدد اللاعبين : {len(await r_local.smembers(keys["list"]))}

-''',
                        reply_markup=keyboard
                    )
            except MessageIdInvalid:
                break
            except:
                pass
            
    except asyncio.CancelledError:
        pass

async def _rolet_updater_task(c, chat_id, dev, k, creator_id):
    r_local = get_global_r()
    keys = _rolet_keys(chat_id, dev)

    initial_data = await r_local.hgetall(keys["game"])
    try:
        last_shown = int(initial_data.get('count', '0') or '0') if initial_data else 0
    except (TypeError, ValueError):
        last_shown = 0

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("مشاركة", callback_data=f"rolet_join_{creator_id}")],
        [InlineKeyboardButton("بدء الروليت", callback_data=f"rolet_start_{creator_id}")]
    ])

    try:
        while True:
            await asyncio.sleep(_ROLET_UPDATE_INTERVAL)

            if not await r_local.sismember(keys["active"], _ROLET_LOCK_VAL):
                break
            if await r_local.sismember(keys["lock"], _ROLET_LOCK_VAL):
                break

            data = await r_local.hgetall(keys["game"])
            if not data:
                break

            try:
                count = int(data.get('count', '0') or '0')
            except (TypeError, ValueError):
                count = 0

            if count == last_shown:
                continue

            try:
                msg_id = int(data.get('msg_id', '0') or '0')
            except (TypeError, ValueError):
                msg_id = 0
            if not msg_id:
                continue

            try:
                await c.edit_message_text(
                    chat_id,
                    msg_id,
                    f'''{k} مرحباً بكم في لعبة الروليت

- يمكنكم التسجيل فيها عن طريق ضغط زر مشاركة

• عدد اللاعبين : {count}
-''',
                    reply_markup=keyboard
                )
                last_shown = count
            except MessageNotModified:
                pass
            except MessageIdInvalid:
                break
            except Exception as e:
                print(f"Error updating rolet message: {e}")
                break

    except asyncio.CancelledError:
        pass
    finally:
        _ROLET_TASKS.pop(chat_id, None)

async def handle_social_gamesx(c, m, k, text):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if not text:
        return None
    
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

    if text == 'احكام':
        if await r.get(f'{m.chat.id}:AHKAMGAME:{Dev_FINAL}'):
            return await m.reply(plugins_games_roulette_238(k))
        await m.reply(plugins_games_roulette_239(k, k, k))
        await r.delete(f'{m.chat.id}:ListAhkam:{Dev_FINAL}')
        await r.set(f'{m.chat.id}:AHKAMGAME:{Dev_FINAL}', m.from_user.id, ex=120)
        await r.sadd(f'{m.chat.id}:ListAhkam:{Dev_FINAL}', m.from_user.id)
        return True

    if text == 'انا' and await r.get(f'{m.chat.id}:AHKAMGAME:{Dev_FINAL}'):
        if await r.sismember(f'{m.chat.id}:ListAhkam:{Dev_FINAL}', m.from_user.id):
            return await m.reply(plugins_games_roulette_252(k))
        else:
            await m.reply(plugins_games_roulette_254(k))
            await r.sadd(f'{m.chat.id}:ListAhkam:{Dev_FINAL}', m.from_user.id)
            return True

    if text == 'تم' and await r.get(f'{m.chat.id}:AHKAMGAME:{Dev_FINAL}') and m.from_user.id == int((await r.get(f'{m.chat.id}:AHKAMGAME:{Dev_FINAL}')) or 0):
        players = [elem for elem in await r.smembers(f'{m.chat.id}:ListAhkam:{Dev_FINAL}')]
        
        # التحقق من عدد اللاعبين
        if len(players) < 2:
            await m.reply(f'{k} عدد اللاعبين اقل من 2')
            await r.delete(f'{m.chat.id}:ListAhkam:{Dev_FINAL}')
            await r.delete(f'{m.chat.id}:AHKAMGAME:{Dev_FINAL}')
            return True
        
        # خلط اللاعبين عشوائياً
        random.shuffle(players)
        
        # اختيار المحكوم (أول لاعب)
        judged_id = players[0]
        
        # اختيار الحاكم (ثاني لاعب)
        judge_id = players[1]
        
        getUser_judged = await c.get_users(int(judged_id))
        getUser_judge = await c.get_users(int(judge_id))
        
        await m.reply(plugins_games_roulette_265(k, getUser_judged.mention(), getUser_judge.mention()))
        
        await r.delete(f'{m.chat.id}:ListAhkam:{Dev_FINAL}')
        await r.delete(f'{m.chat.id}:AHKAMGAME:{Dev_FINAL}')
        return True

    if text.startswith('روليت'):
        if not await admin_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_games_roulette_272(k))

        parts = text.split()
        if len(parts) > 1:
            try:
                winners_count = int(parts[1])
                if winners_count > 50:
                    return await m.reply(plugins_games_roulette_279(k))
                if winners_count < 1:
                    return await m.reply(plugins_games_roulette_281(k))
            except ValueError:
                return await m.reply(plugins_games_roulette_283(k))
        else:
            return await m.reply(plugins_games_roulette_285(k))

        keys = _rolet_keys(m.chat.id, Dev_FINAL)

        active_exists = await r.sismember(keys["active"], _ROLET_LOCK_VAL)
        if active_exists:
            time_key = keys["time"]
            start_time = await r.get(time_key)
            if start_time:
                elapsed = int(time.time()) - int(start_time)
                remaining = _ROLET_GAME_TTL - elapsed
                if remaining > 0:
                    return await m.reply(
                        plugins_games_roulette_297(k, format_time(remaining), k)
                    )
                else:
                    await r.delete(keys["active"], keys["game"], keys["list"], keys["lock"], keys["time"])
                    _rolet_cancel_task(m.chat.id)
            else:
                return await m.reply(plugins_games_roulette_305(k))

        acquired = await r.sadd(keys["active"], _ROLET_LOCK_VAL)
        if not acquired:
            return await m.reply(plugins_games_roulette_309(k))

        await r.delete(keys["game"], keys["list"], keys["lock"])
        await r.hset(keys["game"], mapping={
            'creator': str(m.from_user.id),
            'winners': str(winners_count),
            'count': '0',
            'msg_id': '0',
        })
        await r.expire(keys["active"], _ROLET_GAME_TTL)
        await r.expire(keys["game"], _ROLET_GAME_TTL)
        await r.expire(keys["list"], _ROLET_GAME_TTL)
        
        start_time = int(time.time())
        await r.set(keys["time"], start_time, ex=_ROLET_GAME_TTL)

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("مشاركة", callback_data=f"rolet_join_{m.from_user.id}")],
            [InlineKeyboardButton("بدء الروليت", callback_data=f"rolet_start_{m.from_user.id}")]
        ])

        sent = await m.reply(plugins_games_roulette_330(k, format_time(_ROLET_GAME_TTL)), reply_markup=keyboard)

        msg_id = getattr(sent, "id", None) or getattr(sent, "message_id", None)
        if msg_id:
            await r.hset(keys["game"], 'msg_id', msg_id)

        _rolet_cancel_task(m.chat.id)
        _ROLET_TASKS[m.chat.id] = asyncio.create_task(
            _rolet_time_checker(c, m.chat.id, Dev_FINAL, k, m.from_user.id, winners_count)
        )
        return True

    if text == 'انهاء الروليت':
        if not await owner_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_games_roulette_352(k))

        keys = _rolet_keys(m.chat.id, Dev_FINAL)

        if not await r.sismember(keys["active"], _ROLET_LOCK_VAL):
            return await m.reply(plugins_games_roulette_357(k))

        game_data = await r.hgetall(keys["game"])
        try:
            msg_id = int(game_data.get('msg_id', '0') or '0')
            if msg_id:
                await c.delete_messages(m.chat.id, msg_id)
        except Exception as e:
            print(f"Error deleting rolet message: {e}")

        await r.delete(keys["active"], keys["game"], keys["list"], keys["lock"], keys["time"])
        _rolet_cancel_task(m.chat.id)

        await m.reply(plugins_games_roulette_397(k))
        return True

    if text == 'الروليت':
        if await r.get(f'{m.chat.id}:NEWROLETGAME:{Dev_FINAL}'):
            return await m.reply(plugins_games_roulette_402(k))
        
        list_key = f'{m.chat.id}:ListNewRolet:{Dev_FINAL}'
        game_key = f'{m.chat.id}:NEWROLETGAME:{Dev_FINAL}'
        
        members = await r.smembers(list_key)
        for member in members:
            await r.srem(list_key, member)
        
        await r.delete(game_key)
        await asyncio.sleep(0.1)
        
        await r.set(game_key, m.from_user.id)
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("انضمام للروليت", callback_data=f"new_rolet_join_{m.from_user.id}")]
        ])
        
        await m.reply(plugins_games_roulette_420(k), reply_markup=keyboard)
        return True

    if text == 'الغاء الروليت':
        if not await admin_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_games_roulette_431(k))
        
        if not await r.get(f'{m.chat.id}:NEWROLETGAME:{Dev_FINAL}'):
            return await m.reply(plugins_games_roulette_434(k))
        
        list_key = f'{m.chat.id}:ListNewRolet:{Dev_FINAL}'
        members = await r.smembers(list_key)
        for member in members:
            await r.srem(list_key, member)
        
        await r.delete(f'{m.chat.id}:NEWROLETGAME:{Dev_FINAL}')
        
        await m.reply(plugins_games_roulette_443(k))
        return True

    if text == 'عقاب':
        if await r.get(f'{m.chat.id}:AQABGAME:{Dev_FINAL}'):
            return await m.reply(plugins_games_roulette_448(k))
        await m.reply(plugins_games_roulette_449(k, k, k))
        await r.delete(f'{m.chat.id}:ListAqab:{Dev_FINAL}')
        await r.set(f'{m.chat.id}:AQABGAME:{Dev_FINAL}', m.from_user.id, ex=120)
        await r.sadd(f'{m.chat.id}:ListAqab:{Dev_FINAL}', m.from_user.id)
        return True

    if text == 'انا' and await r.get(f'{m.chat.id}:AQABGAME:{Dev_FINAL}'):
        if await r.sismember(f'{m.chat.id}:ListAqab:{Dev_FINAL}', m.from_user.id):
            return await m.reply(plugins_games_roulette_462(k))
        else:
            await m.reply(plugins_games_roulette_464(k))
            await r.sadd(f'{m.chat.id}:ListAqab:{Dev_FINAL}', m.from_user.id)
            return True

    if text == 'تم' and await r.get(f'{m.chat.id}:AQABGAME:{Dev_FINAL}') and m.from_user.id == int((await r.get(f'{m.chat.id}:AQABGAME:{Dev_FINAL}')) or 0):
        players = await r.smembers(f'{m.chat.id}:ListAqab:{Dev_FINAL}')
        if len(players) == 1:
            return await m.reply(plugins_games_roulette_471(k))
        else:
            ids = [elem for elem in players]
            loser_id = random.choice(ids)
            getUser = await c.get_users(int(loser_id))
            punishment = random.choice(AQAB_PUNISHMENTS)
            await m.reply(plugins_games_roulette_477(k, getUser.mention(), k, punishment))
            await r.delete(f'{m.chat.id}:ListAqab:{Dev_FINAL}')
            await r.delete(f'{m.chat.id}:AQABGAME:{Dev_FINAL}')
            return True

    if text == 'كرسي' or text == 'كرسي الاعتراف':
        if await r.get(f'{m.chat.id}:KOORSIGAME:{Dev_FINAL}'):
            return await m.reply(plugins_games_roulette_484(k))
        await m.reply(plugins_games_roulette_485(k, k, k))
        await r.delete(f'{m.chat.id}:ListKoorsi:{Dev_FINAL}')
        await r.set(f'{m.chat.id}:KOORSIGAME:{Dev_FINAL}', m.from_user.id, ex=120)
        await r.sadd(f'{m.chat.id}:ListKoorsi:{Dev_FINAL}', m.from_user.id)
        return True

    if text == 'انا' and await r.get(f'{m.chat.id}:KOORSIGAME:{Dev_FINAL}'):
        if await r.sismember(f'{m.chat.id}:ListKoorsi:{Dev_FINAL}', m.from_user.id):
            return await m.reply(plugins_games_roulette_498(k))
        else:
            await m.reply(plugins_games_roulette_500(k))
            await r.sadd(f'{m.chat.id}:ListKoorsi:{Dev_FINAL}', m.from_user.id)
            return True

    if text == 'تم' and await r.get(f'{m.chat.id}:KOORSIGAME:{Dev_FINAL}') and m.from_user.id == int((await r.get(f'{m.chat.id}:KOORSIGAME:{Dev_FINAL}')) or 0):
        players = await r.smembers(f'{m.chat.id}:ListKoorsi:{Dev_FINAL}')
        if len(players) == 1:
            return await m.reply(plugins_games_roulette_507(k))
        else:
            ids = [elem for elem in players]
            confessor_id = random.choice(ids)
            getUser = await c.get_users(int(confessor_id))
            await m.reply(plugins_games_roulette_512(k, getUser.mention(), k))
            await r.delete(f'{m.chat.id}:ListKoorsi:{Dev_FINAL}')
            await r.delete(f'{m.chat.id}:KOORSIGAME:{Dev_FINAL}')
            return True

    return None

@Client.on_callback_query(filters.regex(r"^(rolet_|roulette_|rolet_join_|rolet_leave_|new_rolet_)"), group=-131)
async def rolet_callback(c, callback_query):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    data = callback_query.data
    k = await r.get(f'{Dev_FINAL}:botkey') or '•'
    
    if data.startswith('rolet_join_'):
        chat_id = callback_query.message.chat.id
        user_id = callback_query.from_user.id
        parts = data.split('_')
        if len(parts) >= 3:
            try:
                game_creator_id = int(parts[2])
            except ValueError:
                return await callback_query.answer(REPLIES['plugins_games_roulette_537'], show_alert=True)
        else:
            return await callback_query.answer(REPLIES['plugins_games_roulette_537'], show_alert=True)

        keys = _rolet_keys(chat_id, Dev_FINAL)

        if not await r.sismember(keys["active"], _ROLET_LOCK_VAL):
            return await callback_query.answer(REPLIES['plugins_games_roulette_542'], show_alert=True)
        if await r.sismember(keys["lock"], _ROLET_LOCK_VAL):
            return await callback_query.answer(REPLIES['plugins_games_roulette_542'], show_alert=True)

        added = await r.sadd(keys["list"], user_id)
        if not added:
            return await callback_query.answer(REPLIES['plugins_games_roulette_548'], show_alert=True)

        if await r.sismember(keys["lock"], _ROLET_LOCK_VAL):
            await r.srem(keys["list"], user_id)
            return await callback_query.answer(REPLIES['plugins_games_roulette_542'], show_alert=True)

        count = await r.scard(keys["list"])
        await r.hset(keys["game"], 'count', str(count))

        return await callback_query.answer(REPLIES['plugins_games_roulette_557'], show_alert=True)

    elif data.startswith('rolet_start_'):
        chat_id = callback_query.message.chat.id
        user_id = callback_query.from_user.id
        parts = data.split('_')
        if len(parts) >= 3:
            try:
                game_creator_id = int(parts[2])
            except ValueError:
                return await callback_query.answer(REPLIES['plugins_games_roulette_537'], show_alert=True)
        else:
            return await callback_query.answer(REPLIES['plugins_games_roulette_537'], show_alert=True)

        if user_id != game_creator_id:
            return await callback_query.answer(REPLIES['plugins_games_roulette_572'], show_alert=True)

        if not await admin_pls(user_id, chat_id):
            return await callback_query.answer(REPLIES['plugins_games_roulette_575'], show_alert=True)

        keys = _rolet_keys(chat_id, Dev_FINAL)

        if not await r.sismember(keys["active"], _ROLET_LOCK_VAL):
            return await callback_query.answer(REPLIES['plugins_games_roulette_542'], show_alert=True)

        locked = await r.sadd(keys["lock"], _ROLET_LOCK_VAL)
        if not locked:
            return await callback_query.answer(REPLIES['plugins_games_roulette_542'], show_alert=True)

        game_data = await r.hgetall(keys["game"])
        try:
            winners_count = int(game_data.get('winners', '1') or '1')
        except (TypeError, ValueError):
            winners_count = 1

        players = await r.smembers(keys["list"])

        if len(players) < 1:
            await r.srem(keys["lock"], _ROLET_LOCK_VAL)
            return await callback_query.answer(REPLIES['plugins_games_roulette_596'], show_alert=True)

        if len(players) < winners_count:
            await r.srem(keys["lock"], _ROLET_LOCK_VAL)
            return await callback_query.answer(plugins_games_roulette_600(winners_count), show_alert=True)

        player_ids = [int(pid.decode() if isinstance(pid, bytes) else pid) for pid in players]
        random.shuffle(player_ids)
        selected_winners = player_ids[:winners_count]

        result_text = f"{k} الفائزين في لعبة الروليت :\n\n"
        for i, winner_id in enumerate(selected_winners, 1):
            try:
                get_user = await c.get_users(winner_id)
                result_text += f"{i}- {get_user.mention()}\n"
            except:
                result_text += f"{i}- {winner_id}\n"

        final_message = f'''{k} انتهت لعبة الروليت

- عدد اللاعبين : {len(players)}
- عدد الفائزين : {winners_count}

{result_text}'''

        try:
            await callback_query.message.delete()
        except Exception as e:
            print(f"Error deleting old message: {e}")

        try:
            await callback_query.message.answer(final_message)
        except Exception as e:
            print(f"Error sending new message: {e}")
            try:
                await callback_query.message.reply(final_message)
            except Exception as e2:
                print(f"Error sending fallback message: {e2}")

        await r.delete(keys["active"], keys["game"], keys["list"], keys["lock"], keys["time"])
        _rolet_cancel_task(chat_id)

        await callback_query.answer(REPLIES['plugins_games_roulette_638'])
    
    elif data.startswith('new_rolet_join_'):
        chat_id = callback_query.message.chat.id
        user_id = callback_query.from_user.id
        parts = data.split('_')
        if len(parts) >= 4:
            try:
                game_creator_id = int(parts[3])
            except (ValueError, IndexError):
                return await callback_query.answer(REPLIES['plugins_games_roulette_537'], show_alert=True)
        else:
            return await callback_query.answer(REPLIES['plugins_games_roulette_537'], show_alert=True)
        
        game_exists = await r.get(f'{chat_id}:NEWROLETGAME:{Dev_FINAL}')
        if not game_exists:
            return await callback_query.answer(REPLIES['plugins_games_roulette_542'], show_alert=True)
        
        is_member = await r.sismember(f'{chat_id}:ListNewRolet:{Dev_FINAL}', user_id)
        if is_member:
            return await callback_query.answer(REPLIES['plugins_games_roulette_548'], show_alert=True)
        
        players = await r.smembers(f'{chat_id}:ListNewRolet:{Dev_FINAL}')
        if len(players) >= 5:
            return await callback_query.answer(REPLIES['plugins_games_roulette_662'], show_alert=True)
        
        await r.sadd(f'{chat_id}:ListNewRolet:{Dev_FINAL}', user_id)
        
        players = await r.smembers(f'{chat_id}:ListNewRolet:{Dev_FINAL}')
        players_count = len(players)
        
        try:
            get_user = await c.get_users(user_id)
            new_player_name = get_user.first_name
            await callback_query.answer(plugins_games_roulette_672(), show_alert=True)
        except:
            new_player_name = str(user_id)
            await callback_query.answer(REPLIES['plugins_games_roulette_675'], show_alert=True)
        
        if players_count < 5:
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("انضمام للروليت", callback_data=f"new_rolet_join_{game_creator_id}")]
            ])
            
            try:
                await callback_query.edit_message_text(
                    plugins_games_roulette_683(k, players_count, new_player_name),
                    reply_markup=keyboard
                )
            except Exception as e:
                print(f"Error updating message: {e}")
        
        else:
            players_list = []
            player_ids = []
            for pid in players:
                try:
                    pid_int = int(pid.decode() if isinstance(pid, bytes) else pid)
                    player_ids.append(pid_int)
                    get_user = await c.get_users(pid_int)
                    players_list.append(get_user.first_name)
                except:
                    players_list.append(str(pid))
                    player_ids.append(str(pid))
            
            buttons = []
            for i, player in enumerate(players_list[:5]):
                buttons.append([InlineKeyboardButton(player, callback_data=f"new_rolet_show_{i}")])
            
            buttons.append([InlineKeyboardButton("بدء الروليت", callback_data=f"new_rolet_start_{game_creator_id}")])
            
            keyboard = InlineKeyboardMarkup(buttons)
            
            try:
                await callback_query.edit_message_text(
                    plugins_games_roulette_716(k, chr(10).join([f"• {p}" for p in players_list[:5]])),
                    reply_markup=keyboard
                )
            except Exception as e:
                print(f"Error updating message: {e}")
            
            await r.set(f'{chat_id}:NewRoletPlayers:{Dev_FINAL}', json.dumps(player_ids))
    
    elif data.startswith('new_rolet_show_'):
        await callback_query.answer(REPLIES['plugins_games_roulette_730'], show_alert=True)
    
    elif data.startswith('new_rolet_start_'):
        chat_id = callback_query.message.chat.id
        user_id = callback_query.from_user.id
        parts = data.split('_')
        if len(parts) >= 4:
            try:
                game_creator_id = int(parts[3])
            except (ValueError, IndexError):
                return await callback_query.answer(REPLIES['plugins_games_roulette_537'], show_alert=True)
        else:
            return await callback_query.answer(REPLIES['plugins_games_roulette_537'], show_alert=True)
        
        game_exists = await r.get(f'{chat_id}:NEWROLETGAME:{Dev_FINAL}')
        if not game_exists:
            return await callback_query.answer(REPLIES['plugins_games_roulette_542'], show_alert=True)
        
        players = await r.smembers(f'{chat_id}:ListNewRolet:{Dev_FINAL}')
        
        player_ids = [int(pid.decode() if isinstance(pid, bytes) else pid) for pid in players]
        
        if len(player_ids) == 1:
            try:
                winner = await c.get_users(player_ids[0])
                await callback_query.message.edit_text(plugins_games_roulette_755(k, winner.mention()), reply_markup=None)
            except:
                await callback_query.message.edit_text(plugins_games_roulette_757(k, player_ids[0]), reply_markup=None)
            
            list_key = f'{chat_id}:ListNewRolet:{Dev_FINAL}'
            members = await r.smembers(list_key)
            for member in members:
                await r.srem(list_key, member)
            
            await r.delete(f'{chat_id}:NEWROLETGAME:{Dev_FINAL}')
            await r.delete(f'{chat_id}:NewRoletPlayers:{Dev_FINAL}')
            await callback_query.answer(REPLIES['plugins_games_roulette_542'])
            return
        
        loser_id = random.choice(player_ids)
        player_ids.remove(loser_id)
        
        try:
            loser = await c.get_users(loser_id)
            await callback_query.message.edit_text(plugins_games_roulette_774(k, loser.mention()), reply_markup=None)
        except:
            await callback_query.message.edit_text(plugins_games_roulette_776(k, loser_id), reply_markup=None)
        
        list_key = f'{chat_id}:ListNewRolet:{Dev_FINAL}'
        members = await r.smembers(list_key)
        for member in members:
            await r.srem(list_key, member)
        
        for pid in player_ids:
            await r.sadd(list_key, pid)
        
        remaining_players = []
        for pid in player_ids:
            try:
                get_user = await c.get_users(pid)
                remaining_players.append(get_user.first_name)
            except:
                remaining_players.append(str(pid))
        
        if len(remaining_players) == 1:
            try:
                winner = await c.get_users(player_ids[0])
                await callback_query.message.edit_text(plugins_games_roulette_797(k, winner.mention()), reply_markup=None)
            except:
                await callback_query.message.edit_text(plugins_games_roulette_799(k, player_ids[0]), reply_markup=None)
            
            list_key = f'{chat_id}:ListNewRolet:{Dev_FINAL}'
            members = await r.smembers(list_key)
            for member in members:
                await r.srem(list_key, member)
            
            await r.delete(f'{chat_id}:NEWROLETGAME:{Dev_FINAL}')
            await r.delete(f'{chat_id}:NewRoletPlayers:{Dev_FINAL}')
            await callback_query.answer(REPLIES['plugins_games_roulette_542'])
            return
        
        buttons = []
        for i, player in enumerate(remaining_players):
            buttons.append([InlineKeyboardButton(player, callback_data=f"new_rolet_show_{i}")])
        
        buttons.append([InlineKeyboardButton("بدء الروليت", callback_data=f"new_rolet_start_{game_creator_id}")])
        
        keyboard = InlineKeyboardMarkup(buttons)
        
        try:
            await callback_query.message.edit_text(
                plugins_games_roulette_820(k, len(remaining_players), chr(10).join([f"• {p}" for p in remaining_players])),
                reply_markup=keyboard
            )
        except Exception as e:
            print(f"Error editing message: {e}")
        
        await callback_query.answer()