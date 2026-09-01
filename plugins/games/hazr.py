"""
[ = This plugin is a part from Rfinal Source code = ]
لعبة "حزر" - لعبة تخمين جماعية:
- من يكتب "حزر" يبدأ اللعبة ويُسجَّل تلقائياً.
- من يكتب "انا" يُسجَّل باللعبة (اثناء مرحلة التسجيل فقط).
- صاحب اللعبة فقط من يكتب "نعم" لإغلاق التسجيل وبدء الجولة.
- يتم اختيار عضو عشوائي من المسجلين ويُكتم (تُحذف رسائله) لمدة 3 دقائق.
- تُرسل كلمة عشوائية عبر زر كولباك يراها الجميع إلا المكتوم.
- إذا كتب المكتوم الكلمة الصحيحة يُفك كتمه فوراً.
- رتبة admin_pls يمكنها استخدام أمر "سماح" (بالرد) لفك القيود عن العضو فوراً.
"""
from helpers.context import get_global_r, get_global_dev, get_global_k
from compat import Client
from compat import *
from helpers.ranks import *
import random, asyncio, uuid, html

MUTE_SECONDS = 180

HAZR_WORDS = [
    ('مقص', 'شيء يستخدم لقطع الاشياء، يتوفر بكثرة عند الحلاقين'),
    ('مفتاح', 'شيء صغير معدني يفتح ويقفل به الباب'),
    ('مظلة', 'تحميك من المطر او الشمس وتحملها فوق راسك'),
    ('ساعة', 'تخبرك كم الوقت، توضع باليد او تعلق بالحائط'),
    ('كرسي', 'تجلس عليه، يوجد غالبا بجانب الطاولة'),
    ('ثلاجة', 'جهاز كهربائي يبرد الطعام ويحفظه'),
    ('مكنسة', 'تستخدم لتنظيف الارض من الغبار'),
    ('نظارة', 'توضع على العين لتحسين الرؤيه'),
    ('مروحه', 'تدور وتعطي هواء لتخفيف الحر'),
    ('حقيبه', 'تحمل فيها اغراضك عند السفر او الدوام'),
    ('مصباح', 'يضيء الغرفه عندما يكون الظلام'),
    ('سلم', 'تصعد عليه للوصول لمكان عالي'),
    ('قلم', 'تكتب فيه على الورق'),
    ('جسر', 'تنظر فيها لترى انعكاس وجهك'),
    ('مفك', 'اداه تستخدم لفك وربط البراغي'),
    ('بطانيه', 'تتغطى فيها وانت نايم بالشتاء'),
    ('مطرقه', 'اداه يستخدمها النجار لدق المسامير'),
    ('صحن', 'يوضع فيه الطعام على السفره'),
    ('طاوله', 'يوضع فيه الطعام على السفره'),    
    ('ميسي', 'يوضع فيه الطعام على السفره'),
    ('صحن', 'يوضع فيه الطعام على السفره'),        
]


def _hazr_key(base, chat_id, dev):
    return f'{chat_id}:hazr_{base}:{dev}'


async def _clear_hazr_state(r, chat_id, Dev_FINAL):
    await r.delete(
        _hazr_key('state', chat_id, Dev_FINAL),
        _hazr_key('starter', chat_id, Dev_FINAL),
        _hazr_key('players', chat_id, Dev_FINAL),
        _hazr_key('muted', chat_id, Dev_FINAL),
        _hazr_key('answer', chat_id, Dev_FINAL),
        _hazr_key('round', chat_id, Dev_FINAL),
    )


async def _auto_unmute_after_delay(c, chat_id, muted_id, round_token, delay=MUTE_SECONDS):
    await asyncio.sleep(delay)
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    k = await r.get(f'{Dev_FINAL}:botkey') or '•'
    
    current_round = await r.get(_hazr_key('round', chat_id, Dev_FINAL))
    if current_round is None:
        return
    current_round = current_round.decode() if isinstance(current_round, bytes) else current_round
    if current_round != round_token:
        return
    
    current_muted = await r.get(_hazr_key('muted', chat_id, Dev_FINAL))
    if current_muted is None:
        return
    current_muted = current_muted.decode() if isinstance(current_muted, bytes) else current_muted
    if str(current_muted) != str(muted_id):
        return
    
    await _clear_hazr_state(r, chat_id, Dev_FINAL)
    
    try:
        member = await c.get_chat_member(chat_id, muted_id)
        name = member.user.first_name or member.user.username or "العضو"
        mention = f"<a href='tg://user?id={muted_id}'>{html.escape(str(name))}</a>"
    except Exception:
        mention = f"<a href='tg://user?id={muted_id}'>العضو</a>"
    
    try:
        return
    except Exception:
        pass


async def handle_hazr_game(c, m, k, text):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    
    if not m.from_user:
        return None
    
    chat_id = m.chat.id
    
    # ==== سماح (بالرد) — لرتبه admin_pls: تفك جميع القيود عن العضو فوراً ====
    if text == 'سماح' and m.reply_to_message and m.reply_to_message.from_user:
        if not await admin_pls(m.from_user.id, chat_id):
            return None
        target = m.reply_to_message.from_user
        
        current_muted = await r.get(_hazr_key('muted', chat_id, Dev_FINAL))
        if current_muted:
            current_muted = current_muted.decode() if isinstance(current_muted, bytes) else current_muted
        
        if current_muted and str(current_muted) == str(target.id):
            await _clear_hazr_state(r, chat_id, Dev_FINAL)
        
        name = target.first_name or target.username or "العضو"
        mention = f"<a href='tg://user?id={target.id}'>{html.escape(str(name))}</a>"
        await m.reply(f"• تم مسامحة {mention} \n وازالة عواقبه بالكامل\n-")
        return True
    
    # ==== فحص إن كان المرسل هو الشخص المكتوم حالياً باللعبه (حذف رسائله + فحص الإجابه) ====
    state = await r.get(_hazr_key('state', chat_id, Dev_FINAL))
    state = state.decode() if isinstance(state, bytes) else state
    
    if state == 'started':
        muted_id = await r.get(_hazr_key('muted', chat_id, Dev_FINAL))
        muted_id = muted_id.decode() if isinstance(muted_id, bytes) else muted_id
        
        if muted_id and str(m.from_user.id) == str(muted_id):
            answer = await r.get(_hazr_key('answer', chat_id, Dev_FINAL))
            answer = answer.decode() if isinstance(answer, bytes) else answer
            
            is_correct = bool(answer) and text.strip() == answer.strip()
            
            try:
                await m.delete()
            except Exception:
                pass
            
            if is_correct:
                await _clear_hazr_state(r, chat_id, Dev_FINAL)
                await c.send_message(chat_id, "• كفو عليك تم فك الكتم عنك\n-")
            
            return True
    
    # ==== حزر: بدء لعبه جديده + تسجيل تلقائي لمن بدأها ====
    if text == 'حزر':
        if state in ('registering', 'started'):
            return await m.reply("• هناك لعبه حزر شغاله بالفعل بهذي المجموعه\n-")
        
        await r.set(_hazr_key('state', chat_id, Dev_FINAL), 'registering')
        await r.set(_hazr_key('starter', chat_id, Dev_FINAL), str(m.from_user.id))
        await r.delete(_hazr_key('players', chat_id, Dev_FINAL))
        await r.sadd(_hazr_key('players', chat_id, Dev_FINAL), m.from_user.id)
        
        await m.reply("• تم بدا لعبه حزر وتم تسجيلك \n• اللي بيلعب يرسل ( انا ) .")
        return True
    
    # ==== انا: تسجيل باللعبه (اثناء مرحله التسجيل فقط) ====
    if text == 'انا':
        if state != 'registering':
            return None
        
        already = await r.sismember(_hazr_key('players', chat_id, Dev_FINAL), m.from_user.id)
        if already:
            return await m.reply("• اسمك موجود بالقائمه")
        
        await r.sadd(_hazr_key('players', chat_id, Dev_FINAL), m.from_user.id)
        await m.reply("• تم ضفتك للعبه حزر \n• للانتهاء يرسل نعم اللي بداء اللعبه .")
        return True
    
    # ==== نعم: اغلاق التسجيل وبدء الجوله (فقط من قام ببدء اللعبه) ====
    if text == 'نعم':
        if state != 'registering':
            return None
        
        starter = await r.get(_hazr_key('starter', chat_id, Dev_FINAL))
        starter = starter.decode() if isinstance(starter, bytes) else starter
        
        if not starter or str(m.from_user.id) != str(starter):
            return None
        
        player_ids_raw = await r.smembers(_hazr_key('players', chat_id, Dev_FINAL))
        player_ids = []
        for pid in player_ids_raw:
            pid = pid.decode() if isinstance(pid, bytes) else pid
            player_ids.append(int(pid))
        
        if len(player_ids) < 2:
            return await m.reply("• لازم يكون فيه لاعبين اثنين على الأقل عشان تبدأ اللعبه")
        
        chosen_id = random.choice(player_ids)
        word, hint = random.choice(HAZR_WORDS)
        round_token = uuid.uuid4().hex
        
        await r.set(_hazr_key('state', chat_id, Dev_FINAL), 'started')
        await r.set(_hazr_key('muted', chat_id, Dev_FINAL), str(chosen_id))
        await r.set(_hazr_key('answer', chat_id, Dev_FINAL), word)
        await r.set(_hazr_key('round', chat_id, Dev_FINAL), round_token)
        
        try:
            member = await c.get_chat_member(chat_id, chosen_id)
            name = member.user.first_name or member.user.username or "العضو"
            mention = f"<a href='tg://user?id={chosen_id}'>{html.escape(str(name))}</a>"
        except Exception:
            mention = f"<a href='tg://user?id={chosen_id}'>العضو</a>"
        
        btn = InlineKeyboardButton("الاجابه", callback_data=f"hazr_reveal_{chat_id}_{round_token}")
        markup = InlineKeyboardMarkup([[btn]])
        
        await m.reply(
            f"• الهمسه للجميع م عدا ( {mention} ) \n• تم كتمك لمدة 3 دقائق حتى تحزر الاجابه",
            reply_markup=markup,
        )
        
        asyncio.create_task(_auto_unmute_after_delay(c, chat_id, chosen_id, round_token))
        return True
    
    return None


@Client.on_callback_query(filters.regex(r"^hazr_reveal_"), group=-43732)
async def hazr_reveal_callback(c, callback_query):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    
    try:
        _, _, chat_id_str, round_token = callback_query.data.split('_', 3)
        chat_id = int(chat_id_str)
    except Exception:
        return await callback_query.answer()
    
    current_round = await r.get(_hazr_key('round', chat_id, Dev_FINAL))
    current_round = current_round.decode() if isinstance(current_round, bytes) else current_round
    
    if not current_round or current_round != round_token:
        return 
    
    muted_id = await r.get(_hazr_key('muted', chat_id, Dev_FINAL))
    muted_id = muted_id.decode() if isinstance(muted_id, bytes) else muted_id
    
    if muted_id and str(callback_query.from_user.id) == str(muted_id):
        return await callback_query.answer("• الهمسة مو الك", show_alert=True)
    
    answer = await r.get(_hazr_key('answer', chat_id, Dev_FINAL))
    answer = answer.decode() if isinstance(answer, bytes) else answer
    
    if not answer:
        return 
    
    return await callback_query.answer(f"• قربوله كلمة ( {answer} ) .", show_alert=True)
