from helpers.context import get_global_r, get_global_dev, get_global_k
r = get_global_r()
Dev_FINAL = get_global_dev()
k = get_global_k()

import random
import os
import json
from helpers.http import telegram_api_post
from helpers.emoji import render_custom_emoji_entities
from compat import ChatAction, MessageEntityType
from compat import filters
from pydub import AudioSegment
import speech_recognition as sr
import settings
from gtts import gTTS
from threading import Thread
from compat import *
from compat import *
from helpers.ranks import *
from helpers.games import *
from .protect import *
from .buttons import create_button, get_button_info, register_buttons, get_button_custom, get_button_color, create_button_raw
from helpers.replies_store import (
    REPLIES,
    plugins_media_167,
    plugins_media_196,
    plugins_media_220,
)

BUTTONS_DEFINITIONS = {
    "media": {
        "name": "أزرار الميديا والألعاب",
        "buttons": [
            {"id": "back_to_main", "default": "رجوع"},
            {"id": "close_menu", "default": "اغلاق"},
            {"id": "advanced_games", "default": "العاب اونلاين"},
            {"id": "fun_list", "default": "لعبة الغزاة 🥇"},
            {"id": "bank_list", "default": "لعبة البنك"},
            {"id": "clubs_list", "default": "لعبة الاندية"},
            {"id": "farm_list", "default": "لعبة المزارع"},
        ]
    }
}

register_buttons(BUTTONS_DEFINITIONS)

async def process_text_with_emoji(message):
    if not message or not message.text:
        return None
    processed_text = message.text
    if message.entities:
        processed_text = render_custom_emoji_entities(processed_text, message.entities)
    return processed_text

async def build_media_keyboard_raw(user_id):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    buttons = []
    
    row1 = []
    fun_btn = await create_button_raw("media", "fun_list", "لعبة الغزاة 🥇", callback_data=f"fun_list:{user_id}")
    row1.append(fun_btn)
    buttons.append(row1)
    
    row2 = []
    bank_btn = await create_button_raw("media", "bank_list", "لعبة البنك", callback_data=f"bank_list:{user_id}")
    clubs_btn = await create_button_raw("media", "clubs_list", "لعبة الاندية", callback_data=f"clubs_list:{user_id}")
    row2.append(bank_btn)
    row2.append(clubs_btn)
    buttons.append(row2)
    
    row3 = []
    farm_btn = await create_button_raw("media", "farm_list", "لعبة المزارع", callback_data=f"farm_list:{user_id}")
    advanced_btn = await create_button_raw("media", "advanced_games", "العاب اونلاين", callback_data=f"advanced_games:{user_id}")
    row3.append(farm_btn)
    row3.append(advanced_btn)
    buttons.append(row3)
    
    row4 = []
    close_btn = await create_button_raw("media", "close_menu", "اغلاق", callback_data=f"close_menu:{user_id}")
    row4.append(close_btn)
    buttons.append(row4)
    
    return {"inline_keyboard": buttons}

async def build_back_close_keyboard_raw(user_id, back_callback):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    buttons = []
    
    row = []
    back_btn = await create_button_raw("media", "back_to_main", "رجوع", callback_data=back_callback)
    close_btn = await create_button_raw("media", "close_menu", "اغلاق", callback_data=f"close_menu:{user_id}")
    row.append(back_btn)
    row.append(close_btn)
    buttons.append(row)
    
    return {"inline_keyboard": buttons}

async def send_or_edit_message(c, m, text, reply_markup, is_edit=False):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    bot_token = c.bot_token if hasattr(c, "bot_token") else settings.TOKEN
    chat_id = m.message.chat.id if hasattr(m, "message") else m.chat.id
    
    if is_edit:
        await telegram_api_post(bot_token, "editMessageText", {
            "chat_id": chat_id,
            "message_id": m.message.id if hasattr(m, "message") else m.id,
            "text": text,
            "parse_mode": "HTML",
            "reply_markup": reply_markup
        })
    else:
        await telegram_api_post(bot_token, "sendMessage", {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
            "reply_markup": reply_markup
        })

async def handle_games_and_media(c, m, k, text, channel):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if not await check_global_restrictions(c, m, k):
        return    
    if text.startswith("انطق ") or text.startswith("انطقي "):
        if not await r.get(f"{m.chat.id}:disableSay:{Dev_FINAL}"):
            txt = text.split(None, 1)[1]
            if len(txt) > 500:
                return await m.reply(REPLIES['plugins_media_145'])
    
            id = random.randint(999, 10000)
            output_mp3_path = f'final{id}.mp3'
            output_ogg_path = f'final{id}.ogg'
    
            try:
                o = gTTS(text=txt, lang="ar", slow=False)
                o.save(output_mp3_path)
    
                await c.send_chat_action(m.chat.id, ChatAction.RECORD_AUDIO)
    
                os.system(
                    f"ffmpeg -i {output_mp3_path} -ac 1 -strict -2 -codec:a libopus -b:a 128k -vbr off -ar 24000 {output_ogg_path} > /dev/null 2>&1"
                )
    
                await c.send_chat_action(m.chat.id, ChatAction.UPLOAD_AUDIO)
    
                await m.reply_voice(output_ogg_path, caption=f"الكلمة: {txt}")
    
            except Exception as e:
                print(f"حدث خطأ أثناء توليد أو إرسال الصوت: {e}")
                return await m.reply(plugins_media_167(e))
            finally:
                if os.path.exists(output_ogg_path):
                    os.remove(output_ogg_path)
                if os.path.exists(output_mp3_path):
                    os.remove(output_mp3_path)
            return True

    if (
        (text == "وش يقول" or text == "وش تقول")
        and m.reply_to_message
        and m.reply_to_message.voice
    ):
        if m.reply_to_message.voice.file_size > 20971520:
            return await m.reply(REPLIES['plugins_media_181'])
        id = random.randint(99, 1000)
        voice_file_path = f"./final{id}.ogg"
        await m.bot.download(m.reply_to_message.voice, destination=voice_file_path)
        
        s = sr.Recognizer()
        try:
            sound = AudioSegment.from_file(voice_file_path, format="ogg")
            wav_file_path = f"./final{id}.wav"
            sound.export(wav_file_path, format="wav")
            
            with sr.AudioFile(wav_file_path) as src:
                audio_source = s.record(src)
            text_result = s.recognize_google(audio_source, language="ar-SA")
            
            if os.path.exists(wav_file_path):
                os.remove(wav_file_path)
        except Exception as e:
            print(e)
            if os.path.exists(voice_file_path):
                os.remove(voice_file_path)
            return await m.reply(REPLIES['plugins_media_194'])
            
        if os.path.exists(voice_file_path):
            os.remove(voice_file_path)
        return await m.reply(plugins_media_196(text_result))

    if (
        (text == "اkaopsjhsjdidijd" or text == "ysusisgdvdgdfgdgdg")
        and m.reply_to_message
        and m.reply_to_message.voice
        and m.from_user.id == 5434703779
    ):
        if m.reply_to_message.voice.file_size > 20971520:
            return await m.reply(REPLIES['plugins_media_181'])
        id = random.randint(99, 1000)
        voice_file_path = f"./final{id}.ogg"
        await m.bot.download(m.reply_to_message.voice, destination=voice_file_path)
        
        s = sr.Recognizer()
        try:
            sound = AudioSegment.from_file(voice_file_path, format="ogg")
            wav_file_path = f"./final{id}.wav"
            sound.export(wav_file_path, format="wav")
            
            with sr.AudioFile(wav_file_path) as src:
                audio_source = s.record(src)
            text_result = s.recognize_google(audio_source, language="en-US")
            
            if os.path.exists(wav_file_path):
                os.remove(wav_file_path)
        except Exception as e:
            print(e)
            if os.path.exists(voice_file_path):
                os.remove(voice_file_path)
            return await m.reply(REPLIES['plugins_media_194'])
            
        if os.path.exists(voice_file_path):
            os.remove(voice_file_path)
        return await m.reply(plugins_media_220(text_result))


    if text.startswith("ضع كليشه الالعاب") and m.reply_to_message and m.reply_to_message.text:
        if not await dev2_pls(m.from_user.id, m.chat.id, c):
            return await m.reply(REPLIES['plugins_media_224'])
        processed_text = await process_text_with_emoji(m.reply_to_message)
        if processed_text:
            await r.set(f"{Dev_FINAL}:games_cliche:global", processed_text)
        else:
            await r.set(f"{Dev_FINAL}:games_cliche:global", m.reply_to_message.text)
        return await m.reply(REPLIES['plugins_media_230'])

    if text.startswith("ضع كليشه الغزاة") and m.reply_to_message and m.reply_to_message.text:
        if not await dev2_pls(m.from_user.id, m.chat.id, c):
            return await m.reply(REPLIES['plugins_media_224'])
        processed_text = await process_text_with_emoji(m.reply_to_message)
        if processed_text:
            await r.set(f"{Dev_FINAL}:fun_cliche:global", processed_text)
        else:
            await r.set(f"{Dev_FINAL}:fun_cliche:global", m.reply_to_message.text)
        return await m.reply(REPLIES['plugins_media_240'])

    if text.startswith("ضع كليشه الانديه") and m.reply_to_message and m.reply_to_message.text:
        if not await dev2_pls(m.from_user.id, m.chat.id, c):
            return await m.reply(REPLIES['plugins_media_224'])
        processed_text = await process_text_with_emoji(m.reply_to_message)
        if processed_text:
            await r.set(f"{Dev_FINAL}:clubs_cliche:global", processed_text)
        else:
            await r.set(f"{Dev_FINAL}:clubs_cliche:global", m.reply_to_message.text)
        return await m.reply(REPLIES['plugins_media_250'])

    if text.startswith("ضع كليشه المزارع") and m.reply_to_message and m.reply_to_message.text:
        if not await dev2_pls(m.from_user.id, m.chat.id, c):
            return await m.reply(REPLIES['plugins_media_224'])
        processed_text = await process_text_with_emoji(m.reply_to_message)
        if processed_text:
            await r.set(f"{Dev_FINAL}:farm_cliche:global", processed_text)
        else:
            await r.set(f"{Dev_FINAL}:farm_cliche:global", m.reply_to_message.text)
        return await m.reply(REPLIES['plugins_media_260'])

    if text.startswith("ضع كليشه البنك") and m.reply_to_message and m.reply_to_message.text:
        if not await dev2_pls(m.from_user.id, m.chat.id, c):
            return await m.reply(REPLIES['plugins_media_224'])
        processed_text = await process_text_with_emoji(m.reply_to_message)
        if processed_text:
            await r.set(f"{Dev_FINAL}:bank_cliche:global", processed_text)
        else:
            await r.set(f"{Dev_FINAL}:bank_cliche:global", m.reply_to_message.text)
        return await m.reply(REPLIES['plugins_media_270'])

    if text == "حذف كليشه الالعاب":
        if not await dev2_pls(m.from_user.id, m.chat.id, c):
            return await m.reply(REPLIES['plugins_media_224'])
        await r.delete(f"{Dev_FINAL}:games_cliche:global")
        return await m.reply(REPLIES['plugins_media_286'])

    if text == "حذف كليشه الغزاة":
        if not await dev2_pls(m.from_user.id, m.chat.id, c):
            return await m.reply(REPLIES['plugins_media_224'])
        await r.delete(f"{Dev_FINAL}:fun_cliche:global")
        return await m.reply(REPLIES['plugins_media_292'])

    if text == "حذف كليشه الانديه":
        if not await dev2_pls(m.from_user.id, m.chat.id, c):
            return await m.reply(REPLIES['plugins_media_224'])
        await r.delete(f"{Dev_FINAL}:clubs_cliche:global")
        return await m.reply(REPLIES['plugins_media_298'])

    if text == "حذف كليشه المزارع":
        if not await dev2_pls(m.from_user.id, m.chat.id, c):
            return await m.reply(REPLIES['plugins_media_224'])
        await r.delete(f"{Dev_FINAL}:farm_cliche:global")
        return await m.reply(REPLIES['plugins_media_304'])

    if text == "حذف كليشه البنك":
        if not await dev2_pls(m.from_user.id, m.chat.id, c):
            return await m.reply(REPLIES['plugins_media_224'])
        await r.delete(f"{Dev_FINAL}:bank_cliche:global")
        return await m.reply(REPLIES['plugins_media_310'])

    if (
        text == "الالعاب" or text == "العاب"
        or text.lower() == "/kems"
    ):
        if await r.get(f"{m.chat.id}:disableGames:{Dev_FINAL}"):
            return
        else:
            bot_token = c.bot_token if hasattr(c, "bot_token") else settings.TOKEN
            reply_markup = await build_media_keyboard_raw(m.from_user.id)
            
            games_text = await r.get(f"{Dev_FINAL}:games_cliche:global")
            if not games_text:
                games_text = """
• الالعاب للبوت 🎖.
↓ ↓ ↓ ↓ 
• كلمات
• عربي
• اكمل
• انقليزي
• تفكيك
• الاسرع
• العكس
• حزوره
• ترتيب
• علم دول
• دين
• عامه
• رياضيات
• مصطلح
• تركيب
• كت تويت .
• لو خيروك .
• صراحه .
• احكام
• الروليت
• موسيقى
• صور
• المختلف
• صور فنانين
• شخصيات بوب
• شخصيات كيبوب
• شخصيات انمي
• حروف
• حزر
• عقاب
• طبخات 
• مكياج
• اضف تخمين 
• كرة قدم 
"""
            
            await telegram_api_post(bot_token, "sendMessage", {
                    "chat_id": m.chat.id,
                    "text": games_text,
                    "parse_mode": "HTML",
                    "reply_markup": reply_markup
                })
            return

    return None

@Client.on_callback_query(filters.regex(r"^(fun_list:|bank_list:|clubs_list:|farm_list:|advanced_games:|back_to_main:|close_menu:)"), group=-73)
async def games_media_callback(client, callback_query):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    data = callback_query.data
    user_id = callback_query.from_user.id
    k = await r.get(f'{Dev_FINAL}:botkey') or '•'
    bot_token = client.bot_token if hasattr(client, "bot_token") else settings.TOKEN
    
    valid_prefixes = ["fun_list:", "bank_list:", "clubs_list:", "farm_list:", 
                      "advanced_games:", "back_to_main:", "close_menu:"]
    
    if not any(data.startswith(prefix) for prefix in valid_prefixes):
        return
    
    if data.startswith("fun_list:"):
        asked_user_id = int(data.split(":")[1])
        if user_id != asked_user_id:
            return await callback_query.answer(REPLIES['plugins_media_388'], show_alert=True)
        
        reply_markup = await build_back_close_keyboard_raw(user_id, f"back_to_main:{user_id}")
        
        fun_text = await r.get(f"{Dev_FINAL}:fun_cliche:global")
        if not fun_text:
            fun_text = """
• لعبة الغزاة ★
↓ ↓ ↓ ↓ 
- انشاء تيم :
تنشئ التيم وتعزم اخوياك له .

- مسح تيمي :
يمسح جميع عتاد تيمك مع الاعضاء ويتصفر كلشي بتيمك .

- معلومات تيمي :
لمالك التيم فقط يعطيك رمز دعوة تيمك ورمز هجوم تيمك .

- عتادي او تيمي :
يجيب لك عتاد التيم وعدد اعضاء التيم ومستوى تيمك ونقاطه .

- قفل الهجوم :
يقفل الهجوم والقصف ع تيمك .

- حظر او طرد بالرد واليوزر :
يطرد الشخص من تيمك ويحظره .

- قفل او فتح دخول التيم :
يقفل دخول التيم برمز الدعوه .

- دخول التيم :
تدخل تيمات برمز الدعوه الخاص بالتيم وكل تيم يتكون من 20 عضو فقط .

- خروج من التيم :
اذا تبي تطلع من التيم اللي دخلته .

- اعضاء التيم :
تعرف من اللي بتيمكم ومن اكثر واحد اشترى وفاز بالهجوم .

- متجر الغزاه :
يتكون من عتاد خاص للتيم تشتريه عشان تغزي ع تيمات ثانيه الاسعار تلقائيه .

- المتجر العالمي :
يتكون من بطايق تخص التيم كمية محدوده لكل التيمات يتصفر كل 10 ساعات ما تلحق عليها تروح .

- المهام او مهام التيم :
عبارة عن مهام يومية خاصة بالتيم تخلصها تكسبون جائزة التيم .

- جائزة المهام :
الامر لمالك التيم بعد م يخلص تيمك مهامهم تكسب الجائزه عشوائيه .

- اظهار او اخفاء تيمي :
الامر لمالك التيم تظهر رمز تيمك بالتوب عشان الناس تهجمك وانت مجبور ع ذلك عشان تهجم ع غيرك .

- الهجوم او الغزو :
هجوم + رمز التيم تهجم ع تيمات ثانيه 
يعتمد ع اعداد العتاد .

- القصف :
تقصف تيم اخر برمز الدعوه يعتمد ع عدد صواريخك و على مضاد الصواريخ للتيم الاخر .

- توب الغزاه :
توب مكون من 4 مستويات :
- ماسي 🥇
- فضي 🥈 
- برونزي 🥉 
- ضعيف 
ما تقدر تهجم او تقصف الا ع تيم بنفس مستواك .

- استخدام البطائق :
بطائق المتجر العالمي تتكون من :
بطائق تجاوز الوقت
بطائق تغير اسم التيم
بطائق تغير رمز الدعوه

( التيمات بتكون مرتبطة بجميع القروبات )
"""
        
        await telegram_api_post(bot_token, "editMessageText", {
                "chat_id": callback_query.message.chat.id,
                "message_id": callback_query.message.id,
                "text": fun_text,
                "parse_mode": "HTML",
                "reply_markup": reply_markup
            })
        await callback_query.answer()
    
    elif data.startswith("bank_list:"):
        asked_user_id = int(data.split(":")[1])
        if user_id != asked_user_id:
            return await callback_query.answer(REPLIES['plugins_media_388'], show_alert=True)
        
        reply_markup = await build_back_close_keyboard_raw(user_id, f"back_to_main:{user_id}")
        
        bank_text = await r.get(f"{Dev_FINAL}:bank_cliche:global")
        if not bank_text:
            bank_text = """
• لعبة البنك الموحد ★
↓ ↓ ↓ ↓ 
1 - انشاء حساب بنكي ، راتب ، بخشيش ، زرف ، استثمار ، مضاربه ، حظ .

2 - اضافة العجلة أكتب العجله ب 5 مليون ومن ضمن جوائزها :
- سيارة ، فلوس ، x2 = يتدبل كلشي تستخدمه لمدة 5 دقائق ، ..والخ

3 - ممتلكاتي تستطيع الشراء والبيع واهداء ممتلكاتك اوامرها 
كمثال : 
- شراء 2 سيارة
- اهداء 2 سيارة بالرد
- بيع 2 سيارة 

4 - الاسهم يمكنك شراء اسهم وبيعها بالطرق التاليه :
- شراء اسهم 2
- بيع اسهم 2 

كلشوي تتغير نسبة الاسهم اكتب ( سعر الاسهم )لمعرفة نسبتها

5 - اضافة قرض البوت يعطيك عشوائي قرض مع وقت للسداد القرض :
- مراهنة
- قرض
- سجني
- ديوني
- ديونه بالرد 
- سداد ديوني 
- سداد ديونه 

- اذا انسجنت مستحيل تلعب في اي شيء من البنك حتى تسدد او يسددون لك .

6 - اضافة توب القروبات اكثر 20 عشرين قروبات يلعبون العاب عاديه كثير بالقروب يتصدرون للتوب .


( التوب والفلوس مربوطة بجميع البوتات )"""
        
        await telegram_api_post(bot_token, "editMessageText", {
                "chat_id": callback_query.message.chat.id,
                "message_id": callback_query.message.id,
                "text": bank_text,
                "parse_mode": "HTML",
                "reply_markup": reply_markup
            })
        await callback_query.answer()
    
    elif data.startswith("clubs_list:"):
        asked_user_id = int(data.split(":")[1])
        if user_id != asked_user_id:
            return await callback_query.answer(REPLIES['plugins_media_388'], show_alert=True)
        
        reply_markup = await build_back_close_keyboard_raw(user_id, f"back_to_main:{user_id}")
        
        clubs_text = await r.get(f"{Dev_FINAL}:clubs_cliche:global")
        if not clubs_text:
            clubs_text = f"""
• لعبة الاندية ★.
↓ ↓ ↓ ↓ 
• انشاء نادي :
- تسوي لك نادي وتطوره وتلعب فيه بقيمة محددة .

• شراء لاعبين :
- تشتري لاعبين لك بالنادي 

• نادي :
- تستطيع رؤية ناديك ومعرفة عدد لاعبينك ونقاطه ومهاراته 

• تدريب :
- تدرب ناديك كل 20 دقيقه وتزود من مهارات ناديك 

• تنافس (بالرد على الشخص) :
- تتنافس بسرعة الكتابة انت وشخص الاسرع يفوز بمهارات ونقاط 

• ضربة جزاء :
- تختبر مهاراتك بالكورة تجيب هدف اسطوري تستلم نقاط 

• مباراة ودية :
- انت وحظك تفوز بالمباراة تزيد مهاراتك تخسر تنقص مهاراة ناديك 

• مباراة (بالرد ع الشخص) :
- تلعب مباراة ضد شخص تعتمد على مهارات النادي الاكثر يفوز بنقاط + مهارات

• تغير النادي :
- تغير ناديك وقت ماتغير النادي ينحذفون لاعبينك .

• الدوري :
- دوري كل ساعة 10 نوادي يقابلون بعض بشكل عشوائي

• انضمام للدوري :
- اذا كان التسجيل متاح بالنادي تنضم وتنتظر توزيع الادوار
ملاحظة : تنخصم منك 30 مهارات ونقاط 

- الفايز بالدوري : ترجع له النقاط دبل
- الخسران بالدوري : ما يرجع له شيء
- المتعادلين بالدوري : ترجع نقاطكم

• توب النوادي :
- توب خاص باكثر نوادي عندهم نقاط

• حذف النادي :
- تحذف ناديك بالكامل .
_
"""
        
        await telegram_api_post(bot_token, "editMessageText", {
                "chat_id": callback_query.message.chat.id,
                "message_id": callback_query.message.id,
                "text": clubs_text,
                "parse_mode": "HTML",
                "reply_markup": reply_markup
            })
        await callback_query.answer()
    
    elif data.startswith("farm_list:"):
        asked_user_id = int(data.split(":")[1])
        if user_id != asked_user_id:
            return await callback_query.answer(REPLIES['plugins_media_388'], show_alert=True)
        
        reply_markup = await build_back_close_keyboard_raw(user_id, f"back_to_main:{user_id}")
        
        farm_text = await r.get(f"{Dev_FINAL}:farm_cliche:global")
        if not farm_text:
            farm_text = f"""
• لعبة المزرعة  ★
↓ ↓ ↓ ↓ 
• انشاء مزرعه
ـ تنشئ مزرعتك وتحط لها اسم

• معلومات مزرعتي
- يعرض معلومات مزرعتك بالكامل

• مستوى مزرعتي
- يعرض لك مستوى مزرعتك والتي تجمعها عبر حصاد المزروعات

• متجر المزارع
- يعرض البذور والحيوانات المتاحه فالمتجر للشراء

• بذوري
- يعرض لك البذور التي اشتريتها من المتجر

• محاصيلي
- يجيب المحاصيل التي قمت بحصادها

• حيواناتي
- يجيب لك الحيوانات التي اشتريتها من المتجر

• شراء بذور (البذور) (العدد)
- تشتري بذور لمزرعتك

• زراعة (البذور) (العدد)
- تزرع البذور عشان تقوم بحصادها

• حصاد (البذور) (العدد)
- تقوم بحصاد مزروعاتك وترقي مستوى مزرعتك لكل 3 محاصيل تترقى مزرعتك وتنافس التوب


• مزروعاتي
- تشوف البذور التي قمت بزراعتها ومتى وقت حصادها

• بيع (البذور) (العدد)
- تبيع المحاصيل التي قمت بحصادها وتاخذ دبل قيمة شراءها

• شراء (الحيوان) (العدد)
ـ تشتري حيوانات وتقوم باطعامها وجمع منتجاتها

• اطعام الحيوانات
- تقوم بإطعام حيواناتك عشان تجمع منتجاتها

• جمع منتجات الحيوانات
- جمع منتجات الغنم
- جمع منتجات البقر
- جمع منتجات الدجاج

• منتجاتي
- تشوف وشهي التي انتجتها حيواناتك وتبيعها

• بيع (المنتج) (العدد)
- تبيع منتجاتك بعد جمعها

• حذف الحيوانات
- تحذف جميع حيواناتك

• حذف مزرعتي
- تقوم بحذفها بشكل كامل

• مهام المزرعه
- مهام يومية لمزرعتك عند تنفيذها يزيد مستوى مزرعتك 10

• توب المزارع
- تشوف اكثر مستويات للمزارع بالتوب
-
"""
        
        await telegram_api_post(bot_token, "editMessageText", {
                "chat_id": callback_query.message.chat.id,
                "message_id": callback_query.message.id,
                "text": farm_text,
                "parse_mode": "HTML",
                "reply_markup": reply_markup
            })
        await callback_query.answer()
    
    elif data.startswith("advanced_games:"):
        asked_user_id = int(data.split(":")[1])
        if user_id != asked_user_id:
            return await callback_query.answer(REPLIES['plugins_media_388'], show_alert=True)
        
        back_btn = await create_button_raw("media", "back_to_main", "رجوع", callback_data=f"back_to_main:{user_id}")
        close_btn = await create_button_raw("media", "close_menu", "اغلاق", callback_data=f"close_menu:{user_id}")
        
        reply_markup = {
            "inline_keyboard": [
                [
                    {"text": "حرب الفضاء 🛸", "url": "https://t.me/gamee?game=ATARIAsteroids"},
                    {"text": "لعبة الصواريخ 🚀", "url": "https://t.me/T4TTTTBOT?game=rocket"}
                ],
                [
                    {"text": "القط المشاكس 🐱", "url": "https://t.me/gamee?game=CrazyCat"},
                    {"text": "صيد الاسماك 🐟", "url": "https://t.me/gamee?game=SpikyFish3"}
                ],
                [
                    {"text": "سباق الدراجات 🏍", "url": "https://t.me/gamee?game=MotoFX2"},
                    {"text": "سباق سيارات 🏎", "url": "https://t.me/gamee?game=F1Racer"}
                ],
                [
                    {"text": "شطرنج ♟", "url": "https://t.me/T4TTTTBOT?game=chess"},
                    {"text": "ضرب الاسهم 🏹", "url": "https://t.me/T4TTTTBOT?game=arrow"}
                ],
                [
                    {"text": "كرة القدم ⚽", "url": "https://t.me/gamee?game=FootballStar"},
                    {"text": "كرة السلة 🏀", "url": "https://t.me/gamee?game=BasketBoyRush"}
                ],
                [
                    {"text": "لعبة الالوان 🔵🔴", "url": "https://t.me/T4TTTTBOT?game=color"},
                    {"text": "نينجا 🥷", "url": "https://t.me/gamee?game=GravityNinja21"}
                ],
                [
                    {"text": "كونج فو 🎽", "url": "https://t.me/gamee?game=KungFuInc"},
                    {"text": "فلابي بيرد 🐥", "url": "https://t.me/awesomebot?game=FlappyBird"}
                ],
                [
                    {"text": "جيت واي 🚨", "url": "https://t.me/gamee?game=Getaway"},
                    {"text": "لعبة 2048", "url": "https://t.me/awesomebot?game=g2048"}
                ],
                [
                    {"text": "الافعى 🐍", "url": "https://t.me/T4TTTTBOT?game=snake"},
                    back_btn
                ],
                [close_btn]
            ]
        }
        
        await telegram_api_post(bot_token, "editMessageText", {
                "chat_id": callback_query.message.chat.id,
                "message_id": callback_query.message.id,
                "text": f"""
• العاب اونلاين ★
↓ ↓ ↓ ↓ 
•  حرب الفضاء 
•  لعبة الصواريخ 
•  القط المشاكس 
•  صيد الاسماك 
•  سباق الدراجات 
•  سباق سيارات 
•  شطرنج 
•  ضرب الاسهم 
•  كرة القدم 
•  كرة السلة 
•  لعبة الالوان 
•  نينجا 
•  كونج فو 
•  فلافي بيرد 
•  جيت واي 
•  لعبة 2048
•  الافعى 
""",
                "parse_mode": "HTML",
                "reply_markup": reply_markup
            })
        await callback_query.answer()
    
    elif data.startswith("back_to_main:"):
        asked_user_id = int(data.split(":")[1])
        if user_id != asked_user_id:
            return await callback_query.answer(REPLIES['plugins_media_388'], show_alert=True)
        
        reply_markup = await build_media_keyboard_raw(user_id)
        
        games_text = await r.get(f"{Dev_FINAL}:games_cliche:global")
        if not games_text:
            games_text = """
• الالعاب للبوت 🎖.
↓ ↓ ↓ ↓ 
• كلمات
• عربي
• اكمل
• انقليزي
• تفكيك
• الاسرع
• العكس
• حزوره
• ترتيب
• علم دول
• دين
• عامه
• رياضيات
• مصطلح
• تركيب
• كت تويت .
• لو خيروك .
• صراحه .
• احكام
• الروليت
• موسيقى
• صور
• المختلف
• صور فنانين
• شخصيات بوب
• شخصيات كيبوب
• شخصيات انمي
• حروف
• حزر
• عقاب
• طبخات 
• مكياج
• اضف تخمين 
• كرة قدم """
        
        await telegram_api_post(bot_token, "editMessageText", {
                "chat_id": callback_query.message.chat.id,
                "message_id": callback_query.message.id,
                "text": games_text,
                "parse_mode": "HTML",
                "reply_markup": reply_markup
            })
        await callback_query.answer()
    
    elif data.startswith("close_menu:"):
        asked_user_id = int(data.split(":")[1])
        if user_id != asked_user_id:
            return await callback_query.answer(REPLIES['plugins_media_388'], show_alert=True)
        
        await callback_query.message.delete()
        await callback_query.answer()