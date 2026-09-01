from helpers.context import get_global_r, get_global_dev, get_global_k
r = get_global_r()
Dev_FINAL = get_global_dev()
k = get_global_k()
k = get_global_k()
Dev_FINAL = get_global_dev()
r = get_global_r()
from helpers.context import get_global_r, get_global_dev, get_global_k
"""
[ = This plugin is a part from Rfinal Source code = ]
{"Developer":"https://t.me/i0i0ii"}
"""

import random, asyncio, json, time, re
from compat import *
from compat import *
from helpers.ranks import *
from helpers.games import *
from .utils import add_game_earnings, enforce_balance_cap
from compat import Client
async def handle_math_games(c, m, k, text):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if text == 'احسب':
        name = random.choice(Maths)
        name1 = name
        name = re.sub("200", "250 - 50 = ?", name)
        name = re.sub("605", "655 - 50 = ?", name)
        name = re.sub("210", "247 - 37 = ?", name)
        name = re.sub("128", "168 - 40 = ?", name)
        name = re.sub("126", "202 - 76 = ?", name)
        name = re.sub("263", "31297 ÷ 119 = ?", name)
        name = re.sub("150", "246 - 96 = ?", name)
        name = re.sub("2000", "200 × 10 = ?", name)
        name = re.sub("40", "95 - 55 = ?", name)
        name = re.sub("242", "276 - 34 = ?", name)
        name = re.sub("14", "29 - 15 = ?", name)
        name = re.sub("13", "16 - 3 = ?", name)
        name = re.sub("1000", "956 + 44 = ?", name)
        name = re.sub("810", "767 + 43 = ?", name)
        name = re.sub("110", "77 + 33 = ?", name)
        name = re.sub("830", "745 + 85 = ?", name)
        name = re.sub("111", "66 + 45 = ?", name)
        name = re.sub("92", "61 + 31 = ?", name)
        name = re.sub("1110", "988 + 122 = ?", name)
        name = re.sub("6800", "85 × 80 = ?", name)
        name = re.sub("1554", "777 × 2 = ?", name)
        name = re.sub("920", "92 × 10 = ?", name)
        name = re.sub("1740", "87 × 20 = ?", name)
        name = re.sub("1140", "76 × 15 = ?", name)
        name = re.sub("1056", "88 × 12 = ?", name)
        name = re.sub("331", "243 + 88 = ?", name)
        name = re.sub("162", "250 - 88 = ?", name)
        name = re.sub("245", "290 - 45 = ?", name)
        name = re.sub("900", "975 - 75 = ?", name)
        name = re.sub("791", "878 - 87= ?", name)
        name = re.sub("0", "99 - 99 = ?", name)
        name = re.sub("57", "77 - 20 = ?", name)
        name = re.sub("220", "250 - 30 = ?", name)
        await r.set(f'{m.chat.id}:game:{Dev_FINAL}', name1, ex=600)
        await m.reply(plugins_games_math_62(name))
        return True

    if text == 'خواتم':
        name = random.randint(1, 6)
        await r.set(f'{m.chat.id}:game5tm:{m.from_user.id}{Dev_FINAL}', name, ex=600)
        await r.delete(f'{m.chat.id}:game:{Dev_FINAL}')
        return await m.reply(REPLIES['plugins_games_math_69'])

    if await r.get(f'{m.chat.id}:game5tm:{m.from_user.id}{Dev_FINAL}'):
        try:
            if int(text) == await r.get(f'{m.chat.id}:game5tm:{m.from_user.id}{Dev_FINAL}'):
                ra = random.randint(1, 5)
                t = await r.ttl(f'{m.chat.id}:game5tm:{m.from_user.id}{Dev_FINAL}')
                timeo = f"{600 - int(t)}.{random.randint(1,9)}"
                await r.delete(f'{m.chat.id}:game5tm:{m.from_user.id}{Dev_FINAL}')
                if await r.get(f'{m.from_user.id}:Floos'):
                    get = int((await r.get(f'{m.from_user.id}:Floos')) or 0)
                    await r.set(f'{m.from_user.id}:Floos', get + ra)
                    await enforce_balance_cap(r, m, k, m.from_user.id)
                    floos = int((await r.get(f'{m.from_user.id}:Floos')) or 0)
                else:
                    floos = ra
                    await r.set(f'{m.from_user.id}:Floos', ra)
                    await enforce_balance_cap(r, m, k, m.from_user.id)
                await add_game_earnings(m.from_user.id, m.chat.id, ra, m.id)
                return await m.reply(plugins_games_math_95(k, k, timeo, k, floos))
            else:
                await r.delete(f'{m.chat.id}:game5tm:{m.from_user.id}{Dev_FINAL}')
                return await m.reply(plugins_games_math_103(k))
        except:
            pass

    if text == 'ارقام':
        num = ''
        for a in range(random.randint(5, 15)):
            num += str(random.randint(1, 9))
        await r.set(f'{m.chat.id}:game:{Dev_FINAL}', num, ex=600)
        await m.reply(plugins_games_math_112(num), protect_content=True)
        return True

    return None

try:
    with open("high_scores.json", "r") as f:
        high_scores = json.load(f)
except FileNotFoundError:
    high_scores = {}

users_math_genius = {}
TIME_LIMIT = 10
DEV_IDS = {5434703779, int(Dev_FINAL) if str(Dev_FINAL).lstrip('-').isdigit() else 5434703779}

def save_scores():
    with open("high_scores.json", "w") as f:
        json.dump(high_scores, f, indent=4)

def get_user_level(score):
    if score < 20:
        return "\u0628\u0631\u0648\u0646\u0632\u064a", "\ud83e\udd49"
    elif score < 40:
        return "\u0641\u0636\u064a", "\ud83e\udd48"
    elif score < 60:
        return "\u0630\u0647\u0628\u064a", "\ud83e\udd47"
    elif score < 80:
        return "\u0628\u0644\u0627\u062a\u064a\u0646\u064a", "\ud83c\udfc5"
    else:
        return "\u0645\u0627\u0633\u062a\u0631", "\ud83d\udc51"

def is_developer(user_id):
    """live check (bot_id الحالي من contextvar) — لا قيمة مجمدة من الاستيراد."""
    dev = get_global_dev()
    dev_id = int(dev) if str(dev).lstrip('-').isdigit() else 0
    return user_id == 5434703779 or user_id == dev_id

def is_dev_user(user_id: int) -> bool:
    """تحقق من المطور بشكل live (bot_id الحالي من contextvar) — لا قيمة مجمدة من الاستيراد."""
    dev = get_global_dev()
    dev_id = int(dev) if str(dev).lstrip('-').isdigit() else 0
    return user_id == 5434703779 or user_id == dev_id

async def get_top_genius(client, chat_id, top_n=5):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    chat_scores = high_scores.get(str(chat_id), {})
    sorted_scores = sorted(chat_scores.items(), key=lambda item: item[1], reverse=True)

    gold = []
    silver = []
    bronze = []

    for user_id, score in sorted_scores:
        level, _ = get_user_level(score)
        try:
            user = await client.get_users(int(user_id))
            name = user.first_name
        except Exception:
            name = f"المستخدم {user_id}"

        if level == "ذهبي":
            gold.append((name, score))
        elif level == "فضي":
            silver.append((name, score))
        elif level == "برونزي":
            bronze.append((name, score))

    top_genius_text = "🏆 **توب العباقرة** 🏆\n\n"

    if gold:
        top_genius_text += "🥇**المستوى الذهبي**🥇\n"
        for i, (name, score) in enumerate(gold[:top_n]):
            top_genius_text += f"{i+1}. {name} ↤︎ {score}\n"
        top_genius_text += "\n"

    if silver:
        top_genius_text += "🥈**المستوى الفضي**🥈\n"
        for i, (name, score) in enumerate(silver[:top_n]):
            top_genius_text += f"{i+1}. {name} ↤︎ {score}\n"
        top_genius_text += "\n"

    if bronze:
        top_genius_text += "🥉**المستوى البرونزي**🥉\n"
        for i, (name, score) in enumerate(bronze[:top_n]):
            top_genius_text += f"{i+1}. {name} ↤︎ {score}\n"
        top_genius_text += "\n"

    if not gold and not silver and not bronze:
        top_genius_text += "• لا يوجد لاعبين مسجلين حتى الآن.\n"

    return top_genius_text

def generate_question(user_score):
    level, _ = get_user_level(user_score)
    if level == "برونزي":
        num1 = random.randint(1, 20)
        num2 = random.randint(1, 20)
        operation = random.choice(["+", "-"])
        if operation == "+":
            question = f"{num1} + {num2} = ?"
            correct_answer = num1 + num2
        else:
            num1, num2 = max(num1, num2), min(num1, num2)
            question = f"{num1} - {num2} = ?"
            correct_answer = num1 - num2
    elif level == "فضي":
        num1 = random.randint(10, 99)
        num2 = random.randint(10, 99)
        operation = random.choice(["+", "-"])
        if operation == "+":
            question = f"{num1} + {num2} = ?"
            correct_answer = num1 + num2
        else:
            num1, num2 = max(num1, num2), min(num1, num2)
            question = f"{num1} - {num2} = ?"
            correct_answer = num1 - num2
    else:
        num1 = random.randint(100, 999)
        num2 = random.randint(100, 999)
        operation = random.choice(["+", "-"])
        if operation == "+":
            question = f"{num1} + {num2} = ?"
            correct_answer = num1 + num2
        else:
            num1, num2 = max(num1, num2), min(num1, num2)
            question = f"{num1} - {num2} = ?"
            correct_answer = num1 - num2
    return question, correct_answer

def generate_options(correct_answer):
    options = [correct_answer]
    attempts = 0
    while len(options) < 3 and attempts < 10:
        wrong_answer = random.randint(correct_answer - 15, correct_answer + 15)
        if wrong_answer != correct_answer and wrong_answer not in options:
            options.append(wrong_answer)
        attempts += 1
    random.shuffle(options)
    return options

async def ask_question(client, chat_id, user_id, reply_to_message_id, previous_question_message_id=None):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if (chat_id, user_id) not in users_math_genius or not users_math_genius[(chat_id, user_id)].get("is_playing"):
        return

    score = users_math_genius[(chat_id, user_id)]["score"]
    level_text, level_medal = get_user_level(score)
    question_text, correct_answer = generate_question(score)
    options = generate_options(correct_answer)
    users_math_genius[(chat_id, user_id)]["correct_answer"] = correct_answer

    keyboard = [
        [InlineKeyboardButton(str(options[0]), callback_data=f"answer_{options[0]}"),
         InlineKeyboardButton(str(options[1]), callback_data=f"answer_{options[1]}"),
         InlineKeyboardButton(str(options[2]), callback_data=f"answer_{options[2]}")]
    ]
    keyboard.append([InlineKeyboardButton("إنهاء اللعبة", callback_data="end_game")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    user = await client.get_users(user_id)
    mention = user.mention()

    question_message = await client.send_message(
        chat_id,
        f"• اهلا {mention}\n• لديك {TIME_LIMIT} ثوان للإجابة\n• المستوى {level_text} {level_medal}\n• نقاطك ↤︎ {score}\n• سؤالك ↤︎ {question_text}",
        reply_to_message_id=reply_to_message_id,
        reply_markup=reply_markup
    )
    users_math_genius[(chat_id, user_id)]["question_message_id"] = question_message.id
    users_math_genius[(chat_id, user_id)]["start_time"] = asyncio.get_event_loop().time()

    if previous_question_message_id:
        try:
            await client.delete_messages(chat_id, previous_question_message_id)
        except Exception as e:
            print(f"Error deleting previous question message: {e}")

async def check_timeout(client, chat_id, user_id, message_id):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    await asyncio.sleep(TIME_LIMIT)
    if (chat_id, user_id) in users_math_genius and users_math_genius[(chat_id, user_id)].get("is_playing") and users_math_genius[(chat_id, user_id)].get("question_message_id") == message_id:
        score = users_math_genius[(chat_id, user_id)]["score"]
        users_math_genius[(chat_id, user_id)]["is_playing"] = False
        await client.edit_message_text(
            chat_id,
            message_id,
            f"• انتهى الوقت \n• انتهت اللعبة لـ ↤︎{users_math_genius[(chat_id, user_id)]['mention']}\n• سكورك هو ↤︎ {score}"
        )
        if str(chat_id) not in high_scores:
            high_scores[str(chat_id)] = {}
        high_scores[str(chat_id)][str(user_id)] = max(score, high_scores[str(chat_id)].get(str(user_id), 0))
        save_scores()
        del users_math_genius[(chat_id, user_id)]

import json
import random
import time
from compat import Client, filters
from compat import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from helpers.ranks import *
from helpers.replies_store import (
    REPLIES,
    plugins_games_math_103,
    plugins_games_math_112,
    plugins_games_math_512,
    plugins_games_math_552,
    plugins_games_math_62,
    plugins_games_math_95,
)

HIGH_SCORES_FILE = "high_scores.json"

def load_scores():
    try:
        with open(HIGH_SCORES_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_scores(scores):
    with open(HIGH_SCORES_FILE, "w") as f:
        json.dump(scores, f, indent=4)

def get_level(score):
    if score < 10:
        return "برونزي", "🥉"
    elif score < 25:
        return "فضي", "🥈"
    else:
        return "ذهبي", "🥇"

def generate_question(score):
    level, _ = get_level(score)
    if level == "برونزي":
        num1 = random.randint(1, 20)
        num2 = random.randint(1, 20)
        op = random.choice(["+", "-"])
        if op == "+":
            question = f"{num1} + {num2}"
            answer = num1 + num2
        else:
            if num1 < num2:
                num1, num2 = num2, num1
            question = f"{num1} - {num2}"
            answer = num1 - num2
    elif level == "فضي":
        num1 = random.randint(10, 99)
        num2 = random.randint(10, 99)
        op = random.choice(["+", "-"])
        if op == "+":
            question = f"{num1} + {num2}"
            answer = num1 + num2
        else:
            if num1 < num2:
                num1, num2 = num2, num1
            question = f"{num1} - {num2}"
            answer = num1 - num2
    else:
        num1 = random.randint(100, 999)
        num2 = random.randint(100, 999)
        op = random.choice(["+", "-"])
        if op == "+":
            question = f"{num1} + {num2}"
            answer = num1 + num2
        else:
            if num1 < num2:
                num1, num2 = num2, num1
            question = f"{num1} - {num2}"
            answer = num1 - num2
    return question, answer

def generate_options(correct):
    options = [correct]
    while len(options) < 4:
        wrong = correct + random.randint(-10, 10)
        if wrong != correct and wrong not in options and wrong > 0:
            options.append(wrong)
    random.shuffle(options)
    return options

async def send_question(client, chat_id, user_id, reply_to_id):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    score = int(await r.get(f"genius_score:{chat_id}:{user_id}") or 0)
    name = await r.get(f"genius_name:{chat_id}:{user_id}") or "لاعب"

    question, answer = generate_question(score)
    options = generate_options(answer)

    await r.set(f"genius_answer:{chat_id}:{user_id}", answer, ex=20)
    await r.set(f"genius_question:{chat_id}:{user_id}", question, ex=20)

    level, medal = get_level(score)

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(str(options[0]), callback_data=f"genius_ans_{options[0]}_{chat_id}_{user_id}"),
            InlineKeyboardButton(str(options[1]), callback_data=f"genius_ans_{options[1]}_{chat_id}_{user_id}")
        ],
        [
            InlineKeyboardButton(str(options[2]), callback_data=f"genius_ans_{options[2]}_{chat_id}_{user_id}"),
            InlineKeyboardButton(str(options[3]), callback_data=f"genius_ans_{options[3]}_{chat_id}_{user_id}")
        ],
        [InlineKeyboardButton(" إنهاء اللعبة", callback_data=f"genius_end_{chat_id}_{user_id}")]
    ])

    await client.send_message(
        chat_id,
        f" **لعبة عبقري الرياضيات** \n\n"
        f"اللاعب: {name}\n"
        f"المستوى: {level} {medal}\n"
        f"نقاطك: {score}\n\n"
        f"**السؤال:** {question} = ?\n\n"
        f" لديك 20 ثانية للإجابة!",
        reply_markup=keyboard,
        reply_to_message_id=reply_to_id if reply_to_id != 0 else None
    )

@Client.on_message(filters.text & filters.group, group=55)
async def genius_game_start(client, message):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if not await check_global_restrictions(client, message, k):
        return
    if await r.get(f'{message.chat.id}:disableGames:{Dev_FINAL}'):
        return

    text = message.text.lower()
    if text == "عبقري":
        chat_id = message.chat.id
        user_id = message.from_user.id

        if await r.get(f"genius_active:{chat_id}:{user_id}"):
            return await message.reply(REPLIES['plugins_games_math_442'])

        scores = load_scores()
        chat_scores = scores.get(str(chat_id), {})
        user_score = chat_scores.get(str(user_id), 0)

        await r.set(f"genius_active:{chat_id}:{user_id}", 1, ex=300)
        await r.set(f"genius_score:{chat_id}:{user_id}", user_score)
        await r.set(f"genius_name:{chat_id}:{user_id}", message.from_user.first_name[:20])

        await send_question(client, chat_id, user_id, message.id)

@Client.on_callback_query(filters.regex(r"^(genius_|math_|answer_|end_game)"), group=3)
async def genius_callback(client, callback_query):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    data = callback_query.data

    if data.startswith("genius_ans_"):
        parts = data.split("_")
        if len(parts) >= 5:
            try:
                user_answer = int(parts[2])
                chat_id = int(parts[3])
                user_id = int(parts[4])
            except Exception as e:
                print(f"Error parsing: {e}")
                return await callback_query.answer(REPLIES['plugins_games_math_470'], show_alert=True)

            if callback_query.from_user.id != user_id:
                return await callback_query.answer(REPLIES['plugins_games_math_473'], show_alert=True)

            if not await r.get(f"genius_active:{chat_id}:{user_id}"):
                return await callback_query.answer(REPLIES['plugins_games_math_476'], show_alert=True)

            correct_answer = await r.get(f"genius_answer:{chat_id}:{user_id}")
            if not correct_answer:
                return await callback_query.answer(REPLIES['plugins_games_math_480'], show_alert=True)

            correct_answer = int(correct_answer)
            current_score = int(await r.get(f"genius_score:{chat_id}:{user_id}") or 0)
            name = await r.get(f"genius_name:{chat_id}:{user_id}") or "لاعب"

            if user_answer == correct_answer:
                new_score = current_score + 1
                await r.set(f"genius_score:{chat_id}:{user_id}", new_score)

                scores = load_scores()
                chat_scores = scores.get(str(chat_id), {})
                old_score = chat_scores.get(str(user_id), 0)
                chat_scores[str(user_id)] = max(old_score, new_score)
                scores[str(chat_id)] = chat_scores
                save_scores(scores)

                await callback_query.answer(REPLIES['plugins_games_math_497'], show_alert=False)

                try:
                    await callback_query.message.delete()
                except:
                    pass

                await send_question(client, chat_id, user_id, 0)
            else:
                await r.delete(f"genius_active:{chat_id}:{user_id}")
                await r.delete(f"genius_score:{chat_id}:{user_id}")
                await r.delete(f"genius_name:{chat_id}:{user_id}")
                await r.delete(f"genius_answer:{chat_id}:{user_id}")
                await r.delete(f"genius_question:{chat_id}:{user_id}")

                await callback_query.message.edit_text(
                    plugins_games_math_512(name, correct_answer, current_score)
                )
                await callback_query.answer(REPLIES['plugins_games_math_519'], show_alert=True)

    elif data.startswith("genius_end_"):
        parts = data.split("_")
        if len(parts) >= 4:
            try:
                chat_id = int(parts[2])
                user_id = int(parts[3])
            except:
                return await callback_query.answer(REPLIES['plugins_games_math_528'], show_alert=True)

            if callback_query.from_user.id != user_id:
                return await callback_query.answer(REPLIES['plugins_games_math_531'], show_alert=True)

            if not await r.get(f"genius_active:{chat_id}:{user_id}"):
                return await callback_query.answer(REPLIES['plugins_games_math_534'], show_alert=True)

            current_score = int(await r.get(f"genius_score:{chat_id}:{user_id}") or 0)
            name = await r.get(f"genius_name:{chat_id}:{user_id}") or "لاعب"

            scores = load_scores()
            chat_scores = scores.get(str(chat_id), {})
            old_score = chat_scores.get(str(user_id), 0)
            chat_scores[str(user_id)] = max(old_score, current_score)
            scores[str(chat_id)] = chat_scores
            save_scores(scores)

            await r.delete(f"genius_active:{chat_id}:{user_id}")
            await r.delete(f"genius_score:{chat_id}:{user_id}")
            await r.delete(f"genius_name:{chat_id}:{user_id}")
            await r.delete(f"genius_answer:{chat_id}:{user_id}")
            await r.delete(f"genius_question:{chat_id}:{user_id}")

            await callback_query.message.edit_text(
                plugins_games_math_552(name, current_score)
            )
            await callback_query.answer(REPLIES['plugins_games_math_558'], show_alert=False)

@Client.on_message(filters.text & filters.group, group=56)
async def genius_top_command(client, message):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if not await check_global_restrictions(client, message, k):
        return
    text = message.text.lower()
    if text == "توب العباقرة" or text == "توب العبقري":
        scores = load_scores()
        chat_scores = scores.get(str(message.chat.id), {})
        sorted_scores = sorted(chat_scores.items(), key=lambda x: x[1], reverse=True)

        if not sorted_scores:
            return await message.reply(REPLIES['plugins_games_math_572'])

        text_msg = "🏆 **قائمة العباقرة** 🏆\n━━━━━━━━━━━━━━━━━━━\n"
        for i, (uid, score) in enumerate(sorted_scores[:10]):
            try:
                user = await client.get_users(int(uid))
                name = user.first_name[:15]
            except:
                name = f"مستخدم {uid[:5]}"

            if i == 0:
                text_msg += f"🥇 {i+1}. {name} → {score} نقطة\n"
            elif i == 1:
                text_msg += f"🥈 {i+1}. {name} → {score} نقطة\n"
            elif i == 2:
                text_msg += f"🥉 {i+1}. {name} → {score} نقطة\n"
            else:
                text_msg += f"   {i+1}. {name} → {score} نقطة\n"

        await message.reply(text_msg)