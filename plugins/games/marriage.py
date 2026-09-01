import re
import asyncio

from helpers.context import get_global_r, get_global_dev, get_global_k
from helpers.redis import r as _shared_r
from compat import Client, filters, InlineKeyboardMarkup, InlineKeyboardButton
from .utils import enforce_balance_cap
from ..protect import get_top, get_emoji_bank


BOT_MARRIAGE_REPLIES = [
    '• خذلك المسكين يبي يتزوج بوت ',
    '• الله لايصيبني بالحول الي صايبك ',
    '• 👓 ينصح بها الاطباء لمثل هذه الحالات',
    '• الله يعين ، تصحر عاطفي عند الاخ يبي يتزوج بوت',
    '• مااحب افسد اجوائك بس ذا بوت يالامير',
]

_bot_marriage_counter = 0


def get_next_bot_marriage_reply() -> str:
    global _bot_marriage_counter
    reply = BOT_MARRIAGE_REPLIES[_bot_marriage_counter % len(BOT_MARRIAGE_REPLIES)]
    _bot_marriage_counter += 1
    return reply


def get_arabic_wife_number(wife_number):
    arabic_numbers = {
        '1': 'الاولى',
        '2': 'الثانيه',
        '3': 'الثالثه',
        '4': 'الرابعه',
    }
    return arabic_numbers.get(str(wife_number), str(wife_number))


def arabic_to_number(arabic):
    mapping = {
        'الاولى': 1,
        'الثانيه': 2,
        'الثالثه': 3,
        'الرابعه': 4,
    }
    return mapping.get(arabic, 0)


def get_next_wife_number(wives_ids):
    for i in range(1, 5):
        if f'wife{i}' not in wives_ids:
            return i
    return None


def apply_dowry_discount(amount: int) -> int:
    return int(int(amount) * 85 // 100)


async def _do_local_marriage(c, m, k, text, wife_number):
    r = get_global_r()
    Dev_FINAL = get_global_dev()

    dowry_parts = re.findall('[0-9]+', text)
    if not dowry_parts:
        return None
    dowry = int(dowry_parts[0])

    target = m.reply_to_message.from_user
    proposer = m.from_user

    if await r.get(f'{target.id}:isMarried:{m.chat.id}{Dev_FINAL}') == "True":
        husband_id = await r.get(f'{target.id}:marriedTo:{m.chat.id}{Dev_FINAL}')
        husband_user = await c.get_users(int(husband_id))
        return await m.reply(f'• الحق {husband_user.mention()} يبون يتزوجون زوجتك')

    wives_ids = await r.hgetall(f'{proposer.id}:wives:{m.chat.id}{Dev_FINAL}')

    if wives_ids and str(target.id) in wives_ids.values():
        return await m.reply('• ي دلخ ذي زوجتك من قبل')

    if await r.get(f'{proposer.id}:isMarried:{m.chat.id}{Dev_FINAL}') == "True":
        return await m.reply('• لا تقرب للمتزوجين')

    if target.id == proposer.id:
        return await m.reply('• غبي تبي تتزوج نفسك!')
    if target.id == c.id or target.is_bot:
        return await m.reply(get_next_bot_marriage_reply())

    if wives_ids and len(wives_ids) >= 4:
        return await m.reply('خلاص يالحبيب 4 زوجات يكفي تراها مو مسابقة.')

    wife_key = f'wife{wife_number}'

    if wives_ids and wife_key in wives_ids:
        occupied_id = wives_ids[wife_key]
        if wife_number == 1:
            return await m.reply('• انت متزوج الزوجه الاولى')
        occupied_user = await c.get_users(int(occupied_id))
        return await m.reply(f'• انت متزوج {get_arabic_wife_number(wife_number)} بالفعل من {occupied_user.mention()}')

    expected_next = get_next_wife_number(wives_ids)
    if expected_next is None:
        return await m.reply('خلاص يالحبيب 4 زوجات يكفي تراها مو مسابقة.')
    if wife_number != expected_next:
        return await m.reply(f'• رح تزوج {get_arabic_wife_number(expected_next)} قبل')

    if dowry < 1000:
        return await m.reply('• المهر لازم اكثر من 1000 ريال 💸')

    floos_from_user = int((await _shared_r.get(f'{proposer.id}:Floos')) or 0)
    if dowry > floos_from_user:
        return await m.reply('مطفر فلوسك ماتكفي')

    if floos_from_user == dowry:
        await _shared_r.delete(f'{proposer.id}:Floos')
    else:
        await _shared_r.set(f'{proposer.id}:Floos', floos_from_user - dowry)
        await enforce_balance_cap(_shared_r, m, k, proposer.id)

    registered_dowry = apply_dowry_discount(dowry)

    await r.hset(f'{proposer.id}:wives:{m.chat.id}{Dev_FINAL}', wife_key, target.id)
    await r.set(f'{target.id}:isMarried:{m.chat.id}{Dev_FINAL}', "True")
    await r.set(f'{target.id}:marriedTo:{m.chat.id}{Dev_FINAL}', proposer.id)
    await r.set(f'{proposer.id}:MARRYMONEY:{m.chat.id}{Dev_FINAL}:{target.id}', registered_dowry)
    await r.sadd(f'{m.chat.id}:zwag:{Dev_FINAL}', f'{target.id}--{proposer.id}&&wife={wife_number}&&floos={registered_dowry}')

    return await m.reply(
        f'• مبرووك تم زواجكم\n'
        f'• الزوج :{proposer.mention()}\n'
        f'• الزوجه {get_arabic_wife_number(wife_number)} :{target.mention()}\n'
        f'• المهر : {registered_dowry:,} بعد خصم 15%\n'
        f'• لعرض عقدكم اكتبو زواجي'
    )


async def _do_local_divorce(c, m, k, wife_number):
    r = get_global_r()
    Dev_FINAL = get_global_dev()

    wives_data = await r.hgetall(f'{m.from_user.id}:wives:{m.chat.id}{Dev_FINAL}')
    wife_key = f'wife{wife_number}'
    if not wives_data or wife_key not in wives_data:
        return await m.reply(f'• رح تزوج {get_arabic_wife_number(wife_number)} قبل')

    wife_id = wives_data[wife_key]
    wife_user = await c.get_users(int(wife_id))
    dowry = int(await r.get(f'{m.from_user.id}:MARRYMONEY:{m.chat.id}{Dev_FINAL}:{wife_id}') or 0)

    await r.hdel(f'{m.from_user.id}:wives:{m.chat.id}{Dev_FINAL}', wife_key)
    await r.delete(f'{m.from_user.id}:MARRYMONEY:{m.chat.id}{Dev_FINAL}:{wife_id}')
    await r.set(f'{wife_id}:isMarried:{m.chat.id}{Dev_FINAL}', "False")
    await r.delete(f'{wife_id}:marriedTo:{m.chat.id}{Dev_FINAL}')

    current_floos = int(await _shared_r.get(f'{wife_id}:Floos') or 0)
    await _shared_r.set(f'{wife_id}:Floos', current_floos + dowry)
    await enforce_balance_cap(_shared_r, m, k, wife_id)

    for member in await r.smembers(f'{m.chat.id}:zwag:{Dev_FINAL}'):
        parts = member.split('&&')
        user_pair = f'{m.from_user.id}--{wife_id}'
        reversed_user_pair = f'{wife_id}--{m.from_user.id}'
        if parts[0] == user_pair or parts[0] == reversed_user_pair:
            await r.srem(f'{m.chat.id}:zwag:{Dev_FINAL}', member)

    return await m.reply(f'• تم طلقتك من {wife_user.mention()}')


async def handle_marriage_commands(c, m, k, text):
    r = get_global_r()
    Dev_FINAL = get_global_dev()

    global_result = await handle_global_marriage_commands(c, m, k, text)
    if global_result is not None:
        return global_result

    if m.reply_to_message and m.reply_to_message.from_user:
        if text.startswith('زواج ') and len(text.split()) == 2 and re.findall('[0-9]+', text):
            return await _do_local_marriage(c, m, k, text, 1)

        if text.startswith('زواج الثانيه ') and len(text.split()) == 3 and re.findall('[0-9]+', text):
            return await _do_local_marriage(c, m, k, text, 2)

        if text.startswith('زواج الثالثه ') and len(text.split()) == 3 and re.findall('[0-9]+', text):
            return await _do_local_marriage(c, m, k, text, 3)

        if text.startswith('زواج الرابعه ') and len(text.split()) == 3 and re.findall('[0-9]+', text):
            return await _do_local_marriage(c, m, k, text, 4)

    if text == 'طلاق':
        return await _do_local_divorce(c, m, k, 1)

    if text.startswith('طلاق '):
        wife_number_word = text.split()[1]
        wife_number = arabic_to_number(wife_number_word)
        if wife_number:
            return await _do_local_divorce(c, m, k, wife_number)
        return None

    if text == 'خلع' and await r.get(f'{m.from_user.id}:isMarried:{m.chat.id}{Dev_FINAL}') == "True":
        husband_id = await r.get(f'{m.from_user.id}:marriedTo:{m.chat.id}{Dev_FINAL}')
        dowry = int(await r.get(f'{husband_id}:MARRYMONEY:{m.chat.id}{Dev_FINAL}:{m.from_user.id}') or 0)
        wives_data_husband = await r.hgetall(f'{husband_id}:wives:{m.chat.id}{Dev_FINAL}')
        wife_key_to_remove = None
        if wives_data_husband and str(m.from_user.id) in wives_data_husband.values():
            wife_key_to_remove = [wk for wk, wv in wives_data_husband.items() if wv == str(m.from_user.id)][0]

        if not wife_key_to_remove:
            return await m.reply('• انتي مو متزوجه اصلاً')

        wife_floos = int(await _shared_r.get(f'{m.from_user.id}:Floos') or 0)
        if wife_floos < dowry:
            return await m.reply(f'• عشان تخلعينه لازم تجمعين {dowry:,} ريال\n-')

        if wife_floos == dowry:
            await _shared_r.delete(f'{m.from_user.id}:Floos')
        else:
            await _shared_r.set(f'{m.from_user.id}:Floos', wife_floos - dowry)

        husband_user = await c.get_users(int(husband_id))
        await r.hdel(f'{husband_id}:wives:{m.chat.id}{Dev_FINAL}', wife_key_to_remove)
        await r.delete(f'{husband_id}:MARRYMONEY:{m.chat.id}{Dev_FINAL}:{m.from_user.id}')
        await r.set(f'{m.from_user.id}:isMarried:{m.chat.id}{Dev_FINAL}', "False")
        await r.delete(f'{m.from_user.id}:marriedTo:{m.chat.id}{Dev_FINAL}')

        current_floos_husband = int(await _shared_r.get(f'{husband_id}:Floos') or 0)
        await _shared_r.set(f'{husband_id}:Floos', current_floos_husband + dowry)
        await enforce_balance_cap(_shared_r, m, k, husband_id)

        for member in await r.smembers(f'{m.chat.id}:zwag:{Dev_FINAL}'):
            parts = member.split('&&')
            user_pair = f'{m.from_user.id}--{husband_id}'
            reversed_user_pair = f'{husband_id}--{m.from_user.id}'
            if parts[0] == user_pair or parts[0] == reversed_user_pair:
                await r.srem(f'{m.chat.id}:zwag:{Dev_FINAL}', member)

        return await m.reply(f'• تم خلعتك من {husband_user.mention()}')

    if text == 'زواجي':
        if await r.get(f'{m.from_user.id}:isMarried:{m.chat.id}{Dev_FINAL}') == "True":
            husband_id = await r.get(f'{m.from_user.id}:marriedTo:{m.chat.id}{Dev_FINAL}')
            husband_user = await c.get_users(int(husband_id))
            wives_data_husband = await r.hgetall(f'{husband_id}:wives:{m.chat.id}{Dev_FINAL}')
            wife_number = None
            if wives_data_husband and str(m.from_user.id) in wives_data_husband.values():
                wife_key = [wk for wk, wv in wives_data_husband.items() if wv == str(m.from_user.id)][0]
                wife_number = wife_key.replace('wife', '')
            dowry = int(await r.get(f'{husband_id}:MARRYMONEY:{m.chat.id}{Dev_FINAL}:{m.from_user.id}') or 0)
            return await m.reply(
                f'• أهلاً بك في زواجك\n'
                f'• الزوج : {husband_user.mention()}\n'
                f'• الزوجه : {m.from_user.mention()}\n'
                f'• المهر : {dowry:,} ريال 💸\n'
                f'• رقم الزوجه : {get_arabic_wife_number(wife_number)}\n'
                f'-'
            )
        wives_data = await r.hgetall(f'{m.from_user.id}:wives:{m.chat.id}{Dev_FINAL}')
        if wives_data:
            wives_list = f'أهلاً بك في قائمة زوجاتك\n• الزوج :  {m.from_user.mention()} 🤵🏻\u200d♂\n━━━━━━━━━━━━\n'
            for wife_key in sorted(wives_data.keys()):
                wife_id = wives_data[wife_key]
                wife_user = await c.get_users(int(wife_id))
                dowry = int(await r.get(f'{m.from_user.id}:MARRYMONEY:{m.chat.id}{Dev_FINAL}:{wife_id}') or 0)
                wife_number = wife_key.replace('wife', '')
                wives_list += f'\n- الزوجه {get_arabic_wife_number(wife_number)} : {wife_user.mention()} 👰🏻\u200d♀\n- المهر : {dowry:,} ريال\n'
            return await m.reply(wives_list)
        return await m.reply('• عذرا عزيزي انت اعزب"')

    if text == 'زوجتي':
        wives_data = await r.hgetall(f'{m.from_user.id}:wives:{m.chat.id}{Dev_FINAL}')
        if wives_data and 'wife1' in wives_data:
            wife1_user = await c.get_users(int(wives_data['wife1']))
            return await m.reply(f'• ي {wife1_user.mention()} زوجك يبيك')
        return await m.reply('• اطلب الله ودورلك ع زوجه')

    if text == 'زوجتي الثانيه':
        wives_data = await r.hgetall(f'{m.from_user.id}:wives:{m.chat.id}{Dev_FINAL}')
        if wives_data and 'wife2' in wives_data:
            wife2_user = await c.get_users(int(wives_data['wife2']))
            return await m.reply(f'• ي {wife2_user.mention()} زوجك يبيك')
        return await m.reply('• اطلب الله ودورلك ع زوجه')

    if text == 'زوجتي الثالثه':
        wives_data = await r.hgetall(f'{m.from_user.id}:wives:{m.chat.id}{Dev_FINAL}')
        if wives_data and 'wife3' in wives_data:
            wife3_user = await c.get_users(int(wives_data['wife3']))
            return await m.reply(f'• ي {wife3_user.mention()} زوجك يبيك')
        return await m.reply('• اطلب الله ودورلك ع زوجه')

    if text == 'زوجتي الرابعه':
        wives_data = await r.hgetall(f'{m.from_user.id}:wives:{m.chat.id}{Dev_FINAL}')
        if wives_data and 'wife4' in wives_data:
            wife4_user = await c.get_users(int(wives_data['wife4']))
            return await m.reply(f'• ي {wife4_user.mention()} زوجك يبيك')
        return await m.reply('• اطلب الله ودورلك ع زوجه')

    if text == 'زوجي':
        if await r.get(f'{m.from_user.id}:isMarried:{m.chat.id}{Dev_FINAL}') == "True":
            husband_id = await r.get(f'{m.from_user.id}:marriedTo:{m.chat.id}{Dev_FINAL}')
            husband_user = await c.get_users(int(husband_id))
            wives_data_husband = await r.hgetall(f'{husband_id}:wives:{m.chat.id}{Dev_FINAL}')
            wife_number = 'غير محدد'
            if wives_data_husband and str(m.from_user.id) in wives_data_husband.values():
                wife_key = [wk for wk, wv in wives_data_husband.items() if wv == str(m.from_user.id)][0]
                wife_number = get_arabic_wife_number(wife_key.replace('wife', ''))
            return await m.reply(f'• ي {husband_user.mention()} زوجتك {wife_number} تبيك')
        return await m.reply('• اطلب الله ودورلك ع زوج')

    if text in ('زواجات', 'توب زواجات', 'توب الزواجات', 'توب المتزوجين'):
        if not await r.smembers(f'{m.chat.id}:zwag:{Dev_FINAL}'):
            return await m.reply('• ماكو زواجات بالقروب لين الحين')
        users = []
        for marriage in await r.smembers(f'{m.chat.id}:zwag:{Dev_FINAL}'):
            parts = marriage.split('&&')
            if len(parts) > 1 and 'wife=1' in parts[1]:
                user_id_1 = int(parts[0].split('--')[0])
                user_id_2 = int(parts[0].split('--')[1])
                money_part = [p for p in parts if 'floos=' in p]
                if money_part:
                    money = int(money_part[0].split('=')[1])
                    name_1 = await r.get(f'{user_id_1}:bankName')
                    if not name_1:
                        try:
                            name_1 = (await c.get_chat(user_id_1)).first_name[:10]
                            await r.set(f'{user_id_1}:bankName', name_1)
                        except Exception:
                            name_1 = 'INVALID_NAME'
                            await r.set(f'{user_id_1}:bankName', name_1)
                    else:
                        name_1 = name_1[:10]
                    name_2 = await r.get(f'{user_id_2}:bankName')
                    if not name_2:
                        try:
                            name_2 = (await c.get_chat(user_id_2)).first_name[:10]
                            await r.set(f'{user_id_2}:bankName', name_2)
                        except Exception:
                            name_2 = 'INVALID_NAME'
                            await r.set(f'{user_id_2}:bankName', name_2)
                    else:
                        name_2 = name_2[:10]
                    users.append({'name_1': name_1, 'name_2': name_2, 'money': money})
        top = get_top(users)[:20]
        out_text = f'توب اغنى {len(top)} زوجات بالقروب :\n\n'
        count = 0
        for user in top:
            count += 1
            emoji = get_emoji_bank(count)
            prefix = emoji if emoji else f'{count} '
            out_text += f'{prefix}) {user["money"]:,} 💵 l {user["name_1"]}  👫 {user["name_2"]}\n\n'
        _bot_username = await r.get(f'{Dev_FINAL}:bot_username') or (await r.get('bot_username')) or 'test_bot'
        out_text += f'\n<a href="https://t.me/{_bot_username}?start=rules">قوانين التُوب</a>'
        return await m.reply(out_text, disable_web_page_preview=True)

    if text == 'مسح الزواج':
        from helpers.ranks import devp_pls
        if await devp_pls(m.from_user.id, m.chat.id):
            async for key in r.scan_iter(match=f'*zwag:{m.chat.id}{Dev_FINAL}', count=100):
                await r.delete(key)
            async for key in r.scan_iter(match=f'*:wives:{m.chat.id}{Dev_FINAL}', count=100):
                await r.delete(key)
            async for key in r.scan_iter(match=f'*:isMarried:{m.chat.id}{Dev_FINAL}', count=100):
                await r.delete(key)
            async for key in r.scan_iter(match=f'*:marriedTo:{m.chat.id}{Dev_FINAL}', count=100):
                await r.delete(key)
            async for key in r.scan_iter(match=f'*:MARRYMONEY:{m.chat.id}{Dev_FINAL}:*', count=100):
                await r.delete(key)
            await r.delete(f'{m.chat.id}:zwag:{Dev_FINAL}')
            return await m.reply('• تم مسح جميع الزواجات بهذي المجموعة')
        return await m.reply('• هذا الأمر للمطورين فقط')

    return None


GLOBAL_PROPOSAL_TIMEOUT = 120


async def _get_global_spouse_label(c, r, Dev_FINAL, user_id):
    wife_id = await r.get(f'{user_id}:wifeGlobal:{Dev_FINAL}')
    if wife_id:
        wife_user = await c.get_users(int(wife_id))
        return False, wife_user.first_name[:15]
    husband_id = await r.get(f'{user_id}:marriedToGlobal:{Dev_FINAL}')
    if husband_id:
        husband_user = await c.get_users(int(husband_id))
        return True, husband_user.first_name[:15]
    return None


async def handle_global_proposal(c, m, k, text):
    r = get_global_r()
    Dev_FINAL = get_global_dev()

    parts = text.split()
    if len(parts) != 3 or not re.findall('[0-9]+', parts[2]):
        return None

    dowry = int(parts[2])
    proposer = m.from_user
    target = m.reply_to_message.from_user

    if target.id == proposer.id:
        return await m.reply('• غبي تبي تتزوج نفسك!')
    if target.id == c.id or target.is_bot:
        return await m.reply(get_next_bot_marriage_reply())

    if dowry < 1000:
        return await m.reply('• المهر لازم اكثر من 1000 ريال 💸')

    if await r.get(f'{proposer.id}:isMarriedGlobal:{Dev_FINAL}') == "True" or await r.get(f'{proposer.id}:wifeGlobal:{Dev_FINAL}'):
        return await m.reply('• انت متزوج عام بالفعل')

    target_status = await _get_global_spouse_label(c, r, Dev_FINAL, target.id)
    if target_status is not None:
        is_female, spouse_name = target_status
        if is_female:
            return await m.reply(f'• وخر ذا محجوز لـ ↤ {spouse_name}')
        return await m.reply(f'• وخر ذي محجوزه لـ ↤ {spouse_name}')

    floos_from_user = int(await _shared_r.get(f'{proposer.id}:Floos') or 0)
    if dowry > floos_from_user:
        return await m.reply('مطفر فلوسك ماتكفي')

    pending_key = f'{proposer.id}:{target.id}:pendingGlobal:{Dev_FINAL}'
    await r.set(pending_key, "1")

    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("موافقة", callback_data=f"gm_acc_{proposer.id}_{target.id}_{dowry}")],
            [InlineKeyboardButton("رفض", callback_data=f"gm_rej_{proposer.id}_{target.id}")],
        ]
    )

    proposal_text = (
        f'• لديك طلب زواج بالعام \n\n'
        f'• الزوج ↤ {proposer.mention()}\n'
        f'• انتي الزوجة ↤ {target.mention()}\n'
        f'• المهر ↤ {dowry:,} ريال 💸\n'
        f'- من حقوقك الشخصية الموافقة او الرفض حددي مستقبلك الالكتروني'
    )

    sent = await m.reply_to_message.reply(proposal_text, reply_markup=keyboard)

    asyncio.create_task(
        _expire_global_proposal(c, m.chat.id, sent.id, pending_key)
    )

    return True


async def _expire_global_proposal(c, chat_id, message_id, pending_key):
    r = get_global_r()
    await asyncio.sleep(GLOBAL_PROPOSAL_TIMEOUT)
    try:
        still_pending = await r.get(pending_key)
        if still_pending == "1":
            await r.delete(pending_key)
            await c.edit_message_text(chat_id, message_id, '• تم الغاء زواجكم السبب تاخرتي بقرارك')
    except Exception:
        pass


@Client.on_callback_query(filters.regex(r"^(gm_acc_|gm_rej_)"), group=-4335)
async def handle_global_proposal_callback(c, callback_query, k):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    data = callback_query.data
    user_id = callback_query.from_user.id

    if data.startswith("gm_acc_"):
        parts = data.split("_")
        proposer_id = int(parts[2])
        target_id = int(parts[3])
        dowry = int(parts[4])

        if user_id != target_id:
            return await callback_query.answer('تبي تتزوج؟ الطلب مو لك', show_alert=True)

        pending_key = f'{proposer_id}:{target_id}:pendingGlobal:{Dev_FINAL}'
        if await r.get(pending_key) != "1":
            return await callback_query.answer('انتهت صلاحية الطلب', show_alert=True)

        proposer = await c.get_users(proposer_id)
        wife = await c.get_users(user_id)

        if await r.get(f'{proposer_id}:isMarriedGlobal:{Dev_FINAL}') == "True" or await r.get(f'{proposer_id}:wifeGlobal:{Dev_FINAL}'):
            await r.delete(pending_key)
            await callback_query.message.edit_text('• الزوج ارتبط بزواج عام آخر', reply_markup=None)
            return await callback_query.answer('انتهى الطلب', show_alert=True)

        if await _get_global_spouse_label(c, r, Dev_FINAL, user_id) is not None:
            await r.delete(pending_key)
            await callback_query.message.edit_text('• انتي مرتبطه بزواج عام آخر', reply_markup=None)
            return await callback_query.answer('انتهى الطلب', show_alert=True)

        floos_from_user = int(await _shared_r.get(f'{proposer_id}:Floos') or 0)
        if dowry > floos_from_user:
            await r.delete(pending_key)
            await callback_query.message.edit_text('مطفر فلوسك ماتكفي', reply_markup=None)
            return await callback_query.answer('الرصيد لا يكفي', show_alert=True)

        if floos_from_user == dowry:
            await _shared_r.delete(f'{proposer_id}:Floos')
        else:
            await _shared_r.set(f'{proposer_id}:Floos', floos_from_user - dowry)
            await enforce_balance_cap(_shared_r, None, k, proposer_id)

        registered_dowry = apply_dowry_discount(dowry)

        await r.set(f'{proposer_id}:wifeGlobal:{Dev_FINAL}', user_id)
        await r.set(f'{proposer_id}:isMarriedGlobal:{Dev_FINAL}', "True")
        await r.set(f'{user_id}:marriedToGlobal:{Dev_FINAL}', proposer_id)
        await r.set(f'{proposer_id}:MARRYMONEYGLOBAL:{Dev_FINAL}', registered_dowry)
        await r.sadd(f'zwagGlobal:{Dev_FINAL}', f'{user_id}--{proposer_id}&&floos={registered_dowry}')
        await r.delete(pending_key)

        success_text = (
            f'مبروك الزواج! 💕\n\n'
            f'🤵 العريس: {proposer.mention()}\n'
            f'👰 العروسة: {wife.mention()}\n'
            f'💸 المهر: {registered_dowry:,} ريال بعد خصم 15%'
        )
        await callback_query.message.edit_text(success_text, reply_markup=None)
        return await callback_query.answer('تم الزواج 🎉', show_alert=True)

    elif data.startswith("gm_rej_"):
        parts = data.split("_")
        proposer_id = int(parts[2])
        target_id = int(parts[3])

        if user_id != target_id:
            return await callback_query.answer('شوضعك يحلو؟ الرفض مو لك', show_alert=True)

        pending_key = f'{proposer_id}:{target_id}:pendingGlobal:{Dev_FINAL}'
        await r.delete(pending_key)

        proposer = await c.get_users(proposer_id)
        reject_text = f'تم رفض طلب الزواج من {proposer.mention()}'
        await callback_query.message.edit_text(reject_text, reply_markup=None)
        return await callback_query.answer('تم الرفض')


async def handle_global_marriage_commands(c, m, k, text):
    r = get_global_r()
    Dev_FINAL = get_global_dev()

    if text.startswith('زواج عام ') and len(text.split()) == 3:
        if not (m.reply_to_message and m.reply_to_message.from_user):
            return None
        return await handle_global_proposal(c, m, k, text)

    if text == 'زواجي عام':
        wife_id = await r.get(f'{m.from_user.id}:wifeGlobal:{Dev_FINAL}')
        husband_id = await r.get(f'{m.from_user.id}:marriedToGlobal:{Dev_FINAL}')
        if wife_id:
            wife_user = await c.get_users(int(wife_id))
            dowry = int(await r.get(f'{m.from_user.id}:MARRYMONEYGLOBAL:{Dev_FINAL}') or 0)
            return await m.reply(
                f'• أهلاً بك في زواجك العام\n'
                f'• الزوج : {m.from_user.first_name[:15]}\n'
                f'• الزوجه : {wife_user.first_name[:15]}\n'
                f'• المهر : {dowry:,} ريال 💸\n'
                f'-'
            )
        if husband_id:
            husband_user = await c.get_users(int(husband_id))
            dowry = int(await r.get(f'{husband_id}:MARRYMONEYGLOBAL:{Dev_FINAL}') or 0)
            return await m.reply(
                f'• أهلاً بك في زواجك العام\n'
                f'• الزوج : {husband_user.first_name[:15]}\n'
                f'• الزوجه : {m.from_user.first_name[:15]}\n'
                f'• المهر : {dowry:,} ريال 💸\n'
                f'-'
            )
        return await m.reply('• ماعندك زواج عام')

    if text == 'طلاق عام':
        wife_id = await r.get(f'{m.from_user.id}:wifeGlobal:{Dev_FINAL}')
        if not wife_id:
            return await m.reply('• ماعندك زواج عام')
        dowry = int(await r.get(f'{m.from_user.id}:MARRYMONEYGLOBAL:{Dev_FINAL}') or 0)

        await r.delete(f'{m.from_user.id}:wifeGlobal:{Dev_FINAL}')
        await r.delete(f'{m.from_user.id}:isMarriedGlobal:{Dev_FINAL}')
        await r.delete(f'{m.from_user.id}:MARRYMONEYGLOBAL:{Dev_FINAL}')
        await r.delete(f'{wife_id}:marriedToGlobal:{Dev_FINAL}')

        current_floos = int(await _shared_r.get(f'{wife_id}:Floos') or 0)
        await _shared_r.set(f'{wife_id}:Floos', current_floos + dowry)
        await enforce_balance_cap(_shared_r, m, k, wife_id)

        for member in await r.smembers(f'zwagGlobal:{Dev_FINAL}'):
            parts = member.split('&&')
            user_pair = f'{m.from_user.id}--{wife_id}'
            reversed_user_pair = f'{wife_id}--{m.from_user.id}'
            if parts[0] == user_pair or parts[0] == reversed_user_pair:
                await r.srem(f'zwagGlobal:{Dev_FINAL}', member)

        return await m.reply('• تم طلقتك عام')

    if text == 'خلع عام':
        husband_id = await r.get(f'{m.from_user.id}:marriedToGlobal:{Dev_FINAL}')
        if not husband_id:
            return await m.reply('• ماعندك زواج عام')
        dowry = int(await r.get(f'{husband_id}:MARRYMONEYGLOBAL:{Dev_FINAL}') or 0)

        wife_floos = int(await _shared_r.get(f'{m.from_user.id}:Floos') or 0)
        if wife_floos < dowry:
            return await m.reply(f'• عشان تخلعينه لازم تجمعين {dowry:,} ريال\n-')

        if wife_floos == dowry:
            await _shared_r.delete(f'{m.from_user.id}:Floos')
        else:
            await _shared_r.set(f'{m.from_user.id}:Floos', wife_floos - dowry)

        await r.delete(f'{husband_id}:wifeGlobal:{Dev_FINAL}')
        await r.delete(f'{husband_id}:isMarriedGlobal:{Dev_FINAL}')
        await r.delete(f'{husband_id}:MARRYMONEYGLOBAL:{Dev_FINAL}')
        await r.delete(f'{m.from_user.id}:marriedToGlobal:{Dev_FINAL}')

        current_floos_husband = int(await _shared_r.get(f'{husband_id}:Floos') or 0)
        await _shared_r.set(f'{husband_id}:Floos', current_floos_husband + dowry)
        await enforce_balance_cap(_shared_r, m, k, husband_id)

        for member in await r.smembers(f'zwagGlobal:{Dev_FINAL}'):
            parts = member.split('&&')
            user_pair = f'{m.from_user.id}--{husband_id}'
            reversed_user_pair = f'{husband_id}--{m.from_user.id}'
            if parts[0] == user_pair or parts[0] == reversed_user_pair:
                await r.srem(f'zwagGlobal:{Dev_FINAL}', member)

        return await m.reply('• تم خلعتك عام')

    if text in ('توب المتزوجين عام', 'توب الزواجات عام', 'زواجات عام'):
        members = await r.smembers(f'zwagGlobal:{Dev_FINAL}')
        if not members:
            return await m.reply('• ماكو زواجات عام لين الحين')
        users = []
        for marriage in members:
            parts = marriage.split('&&')
            user_id_1 = int(parts[0].split('--')[0])
            user_id_2 = int(parts[0].split('--')[1])
            money_part = [p for p in parts if 'floos=' in p]
            if not money_part:
                continue
            money = int(money_part[0].split('=')[1])
            try:
                name_1 = (await c.get_chat(user_id_1)).first_name[:10]
            except Exception:
                name_1 = 'INVALID_NAME'
            try:
                name_2 = (await c.get_chat(user_id_2)).first_name[:10]
            except Exception:
                name_2 = 'INVALID_NAME'
            users.append({'name_1': name_1, 'name_2': name_2, 'money': money})
        top = get_top(users)[:20]
        out_text = f'توب اغنى {len(top)} زوجات عام :\n\n'
        count = 0
        for user in top:
            count += 1
            emoji = get_emoji_bank(count)
            prefix = emoji if emoji else f'{count} '
            out_text += f'{prefix}) {user["money"]:,} 💵 l {user["name_1"]}  👫 {user["name_2"]}\n\n'
        return await m.reply(out_text, disable_web_page_preview=True)

    return None