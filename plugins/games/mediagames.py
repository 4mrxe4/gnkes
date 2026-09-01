from helpers.context import get_global_r, get_global_dev, get_global_k
import html
r = get_global_r()
Dev_FINAL = get_global_dev()
k = get_global_k()
k = get_global_k()
Dev_FINAL = get_global_dev()
r = get_global_r()
from helpers.context import get_global_r, get_global_dev, get_global_k
from compat import Client
import random, asyncio, json, uuid, requests, time
from compat import *
from compat import *
import settings
from helpers.ranks import *
from helpers.games import *
from ..buttons import register_buttons, get_button_custom, get_button_color, create_button_raw
from .utils import add_game_earnings, enforce_balance_cap, safe_int
from helpers.redis import r as shared_r
from helpers.replies_store import (
    plugins_games_mediagames_103,
    plugins_games_mediagames_121,
    plugins_games_mediagames_133,
    plugins_games_mediagames_138,
    plugins_games_mediagames_143,
    plugins_games_mediagames_146,
    plugins_games_mediagames_151,
    plugins_games_mediagames_158,
    plugins_games_mediagames_217,
    plugins_games_mediagames_265,
    plugins_games_mediagames_279,
    plugins_games_mediagames_298,
    plugins_games_mediagames_358,
    plugins_games_mediagames_360,
    plugins_games_mediagames_79,
    plugins_games_mediagames_90,
    plugins_games_mediagames_93,
    plugins_games_mediagames_96,
    plugins_games_mediagames_99,
)
CUSTOM_GAMES_KEY = f"{Dev_FINAL}:custom_games"

BUTTONS_DEFINITIONS = {
    "guess": {
        "name": "أزرار التخمين",
        "buttons": [
            {"id": "add_guess", "default": "اضغط للاضافة"},
        ]
    }
}

register_buttons(BUTTONS_DEFINITIONS)

async def get_custom_game_data(game_name):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    game = await r.hget(CUSTOM_GAMES_KEY, game_name)
    if game:
        return json.loads(game.decode() if isinstance(game, bytes) else game)
    return None

def _extract_photo_and_answer(item):
    photo_raw = item.get('photo', '')
    caption = item.get('caption', 'None')
    answers = item.get('answer', [])

    if photo_raw.startswith('type=photo&photo='):
        parts = photo_raw.split('&caption=')
        photo_file_id = parts[0].replace('type=photo&photo=', '')
        if len(parts) > 1 and parts[1] not in ('None', ''):
            caption = parts[1]
    else:
        photo_file_id = photo_raw

    if caption in ('None', ''):
        caption = None

    return photo_file_id, answers, caption

@Client.on_message(filters.private & filters.command("start") & ~filters.bot, group=-901)
async def guess_start_handler(c, m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    
    if not m.command:
        return
    
    if len(m.command) < 2:
        return
    
    data = m.command[1]
    if not data.startswith("guess_"):
        return

    game_id = data[len("guess_"):]
    game_key = f"{Dev_FINAL}:guess_game:{game_id}"

    if not await r.exists(game_key):
        return await m.reply(plugins_games_mediagames_79(k))


    game_data = await r.hgetall(game_key)
    chat_id = game_data.get(b"chat_id") or game_data.get("chat_id")
    chat_id = chat_id.decode() if isinstance(chat_id, bytes) else chat_id

    starter_id = game_data.get(b"starter_id") or game_data.get("starter_id")
    if starter_id:
        starter_id = starter_id.decode() if isinstance(starter_id, bytes) else starter_id
        if str(m.from_user.id) != str(starter_id):
            return await m.reply(plugins_games_mediagames_90(k))
    else:
        if not await owner_pls(m.from_user.id, int(chat_id)):
            return await m.reply(plugins_games_mediagames_93(k))

    if await r.get(f"{Dev_FINAL}:guess_ended:{game_id}"):
        return await m.reply(plugins_games_mediagames_96(k))

    if await r.get(f"{Dev_FINAL}:guess_pending:{game_id}"):
        return await m.reply(plugins_games_mediagames_99(k))

    await r.set(f"{Dev_FINAL}:guess_pending:{game_id}", str(m.from_user.id), ex=300)
    await r.set(f"{Dev_FINAL}:guess_pending:{m.from_user.id}", game_id, ex=300)
    await m.reply(plugins_games_mediagames_103(k))

@Client.on_message(filters.private & ~filters.command("start"), group=-902)
async def guess_receive_handler(c, m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()

    pending = await r.get(f"{Dev_FINAL}:guess_pending:{m.from_user.id}")
    if not pending:
        return

    game_id = pending.decode() if isinstance(pending, bytes) else pending
    game_key = f"{Dev_FINAL}:guess_game:{game_id}"

    if not await r.exists(game_key):
        await r.delete(f"{Dev_FINAL}:guess_pending:{m.from_user.id}")
        await r.delete(f"{Dev_FINAL}:guess_pending:{game_id}")
        return await m.reply(plugins_games_mediagames_121(k))

    game_data = await r.hgetall(game_key)
    chat_id = game_data.get(b"chat_id") or game_data.get("chat_id")
    chat_id = chat_id.decode() if isinstance(chat_id, bytes) else chat_id

    starter_id = game_data.get(b"starter_id") or game_data.get("starter_id")
    if starter_id:
        starter_id = starter_id.decode() if isinstance(starter_id, bytes) else starter_id
        if str(m.from_user.id) != str(starter_id):
            await r.delete(f"{Dev_FINAL}:guess_pending:{m.from_user.id}")
            await r.delete(f"{Dev_FINAL}:guess_pending:{game_id}")
            return await m.reply(plugins_games_mediagames_133(k))
    else:
        if not await owner_pls(m.from_user.id, int(chat_id)):
            await r.delete(f"{Dev_FINAL}:guess_pending:{m.from_user.id}")
            await r.delete(f"{Dev_FINAL}:guess_pending:{game_id}")
            return await m.reply(plugins_games_mediagames_138(k))

    if await r.get(f"{Dev_FINAL}:guess_ended:{game_id}"):
        await r.delete(f"{Dev_FINAL}:guess_pending:{m.from_user.id}")
        await r.delete(f"{Dev_FINAL}:guess_pending:{game_id}")
        return await m.reply(plugins_games_mediagames_143(k))

    if not m.text:
        return await m.reply(plugins_games_mediagames_146(k))

    word = m.text.strip()

    if len(word) >= 50:
        return await m.reply(plugins_games_mediagames_151(k))

    await r.hset(f"{Dev_FINAL}:guess_words:{game_id}", word.lower(), word)
    await r.expire(f"{Dev_FINAL}:guess_words:{game_id}", 21600)
    await r.delete(f"{Dev_FINAL}:guess_pending:{m.from_user.id}")
    await r.delete(f"{Dev_FINAL}:guess_pending:{game_id}")

    await m.reply(plugins_games_mediagames_158(k, k, word))

    try:
        await c.send_message(
            int(chat_id),
            f"{k} تمت إضافة تخمين\n{k} في حال تم تخمين الكلمة سيتم مسحها تلقائياً\n_"
        )
    except:
        pass

async def handle_media_games(c, m, k, text):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if await r.get(f'{m.chat.id}:addGameStep:{m.from_user.id}{Dev_FINAL}'):
        return None

    active_games_key = f"{Dev_FINAL}:guess_active_games:{m.chat.id}"
    active_games = await r.smembers(active_games_key)
    if active_games:
        guess_text = text.strip().lower()
        for gid in active_games:
            gid = gid.decode() if isinstance(gid, bytes) else gid
            
            if await r.get(f"{Dev_FINAL}:guess_ended:{gid}"):
                await r.srem(active_games_key, gid)
                continue
                
            words_key = f"{Dev_FINAL}:guess_words:{gid}"
            found = await r.hget(words_key, guess_text)
            if found:
                original_word = found.decode() if isinstance(found, bytes) else found
                
                await r.hdel(words_key, guess_text)
                
                await r.set(f"{Dev_FINAL}:guess_ended:{gid}", 1, ex=3600)
                await r.srem(active_games_key, gid)
                
                game_key = f"{Dev_FINAL}:guess_game:{gid}"
                await r.delete(game_key)
                await r.delete(words_key)
                
                guesser_name = m.from_user.first_name or m.from_user.username or "عضو"
                guesser_mention = f'<a href="tg://user?id={m.from_user.id}">{html.escape(str(guesser_name))}</a>'
                
                try:
                    await m.delete()
                except:
                    pass
                
                await c.send_message(
                    m.chat.id,
                    f"{k} جابها صح 🥳\n{k} {guesser_mention}\n{k} {original_word}\n_"
                )
                
                return True

    if text == 'اضف تخمين':
        if not await owner_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_games_mediagames_217(k))

        game_id = uuid.uuid4().hex[:8]
        starter_name = m.from_user.first_name or m.from_user.username or "عضو"

        await r.hset(f"{Dev_FINAL}:guess_game:{game_id}", mapping={
            "chat_id": str(m.chat.id),
            "starter_id": str(m.from_user.id),
            "starter_name": starter_name
        })
        await r.expire(f"{Dev_FINAL}:guess_game:{game_id}", 21600)
        await r.sadd(active_games_key, game_id)
        await r.expire(active_games_key, 21600)

        mention = f'<a href="tg://user?id={m.from_user.id}">{html.escape(str(starter_name))}</a>'
        message_text = f"{k} بدء لعبة التخمين ↤︎ {mention}\n{k} اضغط الزر لاضافة تخمين للاعضاء\n_"

        # التعرف الصحيح على يوزر البوت في aiogram
        bot_info = await c.me() if callable(getattr(c, "me", None)) else await c.get_me()
        bot_username = bot_info.username or ""

        # إنشاء رابط الزر
        url_link = f"https://t.me/{bot_username}?start=guess_{game_id}"
        
        # إنشاء الكيبورد المباشر بأسلوب aiogram (مع الحفاظ على دالة التلوين إذا كانت تُرجع استجابة مناسبة أو إنشائه مباشرة)
        add_btn = await create_button_raw("guess", "add_guess", "اضغط للاضافة", url=url_link)

        # دعم أنماط الأزرار الملونة المدمجة في aiogram 3.x أينما وجدت InlineKeyboardButton
        if isinstance(add_btn, dict):
            kb_button = InlineKeyboardButton(
                text=add_btn.get("text", "اضغط للاضافة"),
                url=add_btn.get("url", url_link),
                style=add_btn.get("style", "success")  # الخاصية المدمجة بالتلوين
            )
        else:
            kb_button = InlineKeyboardButton(text="اضغط للاضافة", url=url_link)

        keyboard = InlineKeyboardMarkup(inline_keyboard=[[kb_button]])

        # إرسال الرسالة مباشرة عبر aiogram وحفظ message_id
        sent_msg = await m.reply(message_text, reply_markup=keyboard, parse_mode="HTML")
        
        if sent_msg and hasattr(sent_msg, "message_id"):
            await r.hset(f"{Dev_FINAL}:guess_game:{game_id}", "start_msg_id", str(sent_msg.message_id))
        
        return True


    if text == 'ايموجي':
        if await r.get(f'{m.chat.id}:gameEmoji:{Dev_FINAL}'):
            return await m.reply(plugins_games_mediagames_265(k, k))
        ran = random.choice(emojis_pics)
        emoji = ran['emoji']
        photo = ran['photo']
        a = await m.reply_photo(photo, caption='اسرع واحد يرسل الايموجي')
        await r.delete(f'{m.chat.id}:game:{Dev_FINAL}')
        await asyncio.sleep(3)
        await r.set(f'{m.chat.id}:gameEmoji:{Dev_FINAL}', emoji, ex=20)
        await a.edit_media(media=InputMediaPhoto(media='https://telegra.ph/file/b53b14951a50d7f75c39e.jpg', caption='ارسل الايموجي الحين'))
        return True

    if text == 'سكب':
        if await r.get(f'{m.chat.id}:gameEmoji:{Dev_FINAL}'):
            await r.delete(f'{m.chat.id}:gameEmoji:{Dev_FINAL}')
            await m.reply(plugins_games_mediagames_279(k))
            return True

    if await r.get(f'{m.chat.id}:gameEmoji:{Dev_FINAL}'):
        if text == await r.get(f'{m.chat.id}:gameEmoji:{Dev_FINAL}'):
            ra = random.randint(1, 5)
            t = await r.ttl(f'{m.chat.id}:gameEmoji:{Dev_FINAL}')
            timeo = f"{20 - int(t)}.{random.randint(1,9)}"
            await r.delete(f'{m.chat.id}:gameEmoji:{Dev_FINAL}')
            if await shared_r.get(f'{m.from_user.id}:Floos'):
                get = int((await shared_r.get(f'{m.from_user.id}:Floos')) or 0)
                await shared_r.set(f'{m.from_user.id}:Floos', get + ra)
                await enforce_balance_cap(shared_r, m, k, m.from_user.id)
                floos = int((await shared_r.get(f'{m.from_user.id}:Floos')) or 0)
            else:
                floos = ra
                await shared_r.set(f'{m.from_user.id}:Floos', ra)
                await enforce_balance_cap(shared_r, m, k, m.from_user.id)
            await add_game_earnings(m.from_user.id, m.chat.id, ra, m.id)
            return await m.reply(plugins_games_mediagames_298(k, k, timeo, k, floos))

    if text == 'كرة قدم' or text == 'كره قدم':
        ph = random.choice(football)
        await r.set(f'{m.chat.id}:game:{Dev_FINAL}', ph['answer'], ex=600)
        caption = ph['caption'] if ph['caption'] else 'وش اسم الاعب ؟'
        await m.reply_photo(ph['photo'], caption=caption)
        return True
        
    if await r.get(f'{m.chat.id}:game:{Dev_FINAL}'):
        answer = await r.get(f'{m.chat.id}:game:{Dev_FINAL}')
        if isinstance(answer, bytes):
            answer = answer.decode()
    
        is_correct = False
    
        if answer.startswith('[') and answer.endswith(']'):
            try:
                parsed = json.loads(answer)
                if hasattr(parsed, '__iter__') and not isinstance(parsed, (str, dict)):
                    user_answer = text.strip().lower()
                    for correct_answer in parsed:
                        if user_answer == correct_answer.strip().lower():
                            is_correct = True
                            break
            except Exception:
                if text.strip().lower() == answer.strip().lower():
                    is_correct = True
        else:
            if text.strip().lower() == answer.strip().lower():
                is_correct = True
    
        if is_correct:
            await r.delete(f'{m.chat.id}:game:{Dev_FINAL}')
    
            game_name = await r.get(f'{m.chat.id}:custom_game_name:{m.from_user.id}')
            if game_name:
                game_name = game_name.decode() if isinstance(game_name, bytes) else game_name
                has_money_key = f'{m.chat.id}:custom_game_has_money:{game_name}:{m.from_user.id}'
            else:
                public_game_name = await r.get(f'{m.chat.id}:public_game_name:{m.from_user.id}')
                if public_game_name:
                    public_game_name = public_game_name.decode() if isinstance(public_game_name, bytes) else public_game_name
                    has_money_key = f'{m.chat.id}:public_game_has_money:{public_game_name}:{m.from_user.id}'
                else:
                    has_money_key = f'{m.chat.id}:custom_game_has_money:{m.chat.id}:{m.from_user.id}'
    
            has_money = await r.get(has_money_key)
            has_money = safe_int(has_money, 0)
    
            start_raw = await r.get(f'{m.chat.id}:game_answer_start:{Dev_FINAL}')
            if start_raw:
                try:
                    start_ts = float(start_raw.decode() if isinstance(start_raw, bytes) else start_raw)
                    elapsed = max(0.0, time.time() - start_ts)
                except Exception:
                    elapsed = round(random.uniform(1, 10), 2)
            else:
                elapsed = round(random.uniform(1, 10), 2)
            await r.delete(f'{m.chat.id}:game_answer_start:{Dev_FINAL}')
    
            user_name = m.from_user.first_name or m.from_user.username or "عضو"
            mention = f"<a href='tg://user?id={m.from_user.id}'>{html.escape(str(user_name))}</a>"
    
            lines = [
                f"• اجابة صحيحة ↤︎ {mention}",
                f"• عدد الثواني ↤︎ {elapsed:.2f}",
            ]
    
            if has_money == 1:
                ra = random.randint(1, 5)
                current_floos = safe_int(await shared_r.get(f'{m.from_user.id}:Floos'), 0)
                floos = current_floos + ra
                await shared_r.set(f'{m.from_user.id}:Floos', floos)
                await enforce_balance_cap(shared_r, m, k, m.from_user.id)
                floos = safe_int(await shared_r.get(f'{m.from_user.id}:Floos'), 0)
                await add_game_earnings(m.from_user.id, m.chat.id, ra, m.id)
                lines.append(f"• فلوسك ↤︎ {floos} ﷼ 💸")
    
            lines.append("-")
            return await m.reply("\n".join(lines))

    return None