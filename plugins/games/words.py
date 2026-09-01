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
from compat import Client
import random, re
from compat import *
from compat import *
from helpers.ranks import *
from helpers.games import *
from .utils import enforce_balance_cap
from helpers.replies_store import (
    plugins_games_words_124,
    plugins_games_words_161,
    plugins_games_words_201,
    plugins_games_words_207,
    plugins_games_words_214,
    plugins_games_words_254,
    plugins_games_words_281,
    plugins_games_words_30,
    plugins_games_words_47,
    plugins_games_words_99,
)
async def handle_word_games(c, m, k, text):
   r = get_global_r()
   Dev_FINAL = get_global_dev()
   k = get_global_k()
   if await r.get(f'{m.chat.id}:addGameStep:{m.from_user.id}{Dev_FINAL}'):
      return None
   
   if text == 'جمل':
     gmla = random.choice(gomal)
     await r.set(f'{m.chat.id}:game:{Dev_FINAL}', gmla.replace(" '",""), ex=600)
     await m.reply(plugins_games_words_30(gmla, k))
   
   if await r.get(f'{m.chat.id}:game:{Dev_FINAL}'):
     if text == await r.get(f'{m.chat.id}:game:{Dev_FINAL}'):
        ra = random.randint(1,5)
        t = await r.ttl(f'{m.chat.id}:game:{Dev_FINAL}')
        timeo = f"{600 - int(t)}.{random.randint(1,9)}"
        await r.delete(f'{m.chat.id}:game:{Dev_FINAL}')
        if await r.get(f'{m.from_user.id}:Floos'):
           get = int((await r.get(f'{m.from_user.id}:Floos')) or 0)
           await r.set(f'{m.from_user.id}:Floos',get+ra)
           await enforce_balance_cap(r, m, k, m.from_user.id)
           floos = int((await r.get(f'{m.from_user.id}:Floos')) or 0)
        else:
           floos = ra
           await r.set(f'{m.from_user.id}:Floos',ra)
           await enforce_balance_cap(r, m, k, m.from_user.id)
        await m.reply(plugins_games_words_47(k, k, timeo, k, floos))
        return True
     
   if text == 'ترتيب':
     name = random.choice(trteep)
     name1 = name
     name = re.sub('سحور', 'س ر و ح', name)
     name = re.sub('سياره', 'ه ر س ي ا', name)
     name = re.sub('استقبال', 'ل ب ا ت ق س ا', name)
     name = re.sub('قنافه', 'ه ق ا ن ف', name)
     name = re.sub('ايفون', 'و ن ف ا', name)
     name = re.sub('بطاطس', 'ب ط ا ط س', name)
     name = re.sub('مطبخ', 'خ ب ط م', name)
     name = re.sub('كرستيانو', 'س ت ا ن و ك ر ي', name)
     name = re.sub('دجاجه', 'ج ج ا د ه', name)
     name = re.sub('مدرسه', 'ه م د ر س', name)
     name = re.sub('الوان', 'ن ا و ا ل', name)
     name = re.sub('غرفه', 'غ ه ر ف', name)
     name = re.sub('ثلاجه', 'ج ه ت ل ا', name)
     name = re.sub('قهوه', 'ه ق ه و', name)
     name = re.sub('سفينه', 'ه ن ف ي س', name)
     name = re.sub('مصر', 'ر م ص', name)
     name = re.sub('محطه', 'ه ط م ح', name)
     name = re.sub('طياره', 'ر ا ط ي ه', name)
     name = re.sub('رادار', 'ر ا ر ا د', name)
     name = re.sub('منزل', 'ن ز م ل', name)
     name = re.sub('مستشفى', 'ى ش س ف ت م', name)
     name = re.sub('كهرباء', 'ر ب ك ه ا ء', name)
     name = re.sub('تفاحه', 'ح ه ا ت ف', name)
     name = re.sub('اخطبوط', 'ط ب و ا خ ط', name)
     name = re.sub('سنترال', 'ن ر ت ل ا س', name)
     name = re.sub('فرنسا', 'ن ف ر س ا', name)
     name = re.sub('برتقاله', 'ر ت ق ب ا ه ل', name)
     name = re.sub('تفاح', 'ح ف ا ت', name)
     name = re.sub('مطرقه', 'ه ط م ر ق', name)
     name = re.sub('هريسه', 'س ه ر ي ه', name)
     name = re.sub('لبانه', 'ب ن ل ه ا', name)
     name = re.sub('شباك', 'ب ش ا ك', name)
     name = re.sub('باص', 'ص ا ب', name)
     name = re.sub('سمكه', 'ك س م ه', name)
     name = re.sub('ذباب', 'ب ا ب ذ', name)
     name = re.sub('تلفاز', 'ت ف ل ز ا', name)
     name = re.sub('حاسوب', 'س ا ح و ب', name)
     name = re.sub('انترنت', 'ا ت ن ر ن ت', name)
     name = re.sub('ساحه', 'ح ا ه س', name)
     name = re.sub('جسر', 'ر ج س', name)
     await r.set(f'{m.chat.id}:game:{Dev_FINAL}', name1,ex=600)
     await m.reply(plugins_games_words_99(name))
     return True
   
   if text == 'انقليزي':
     name = random.choice(english)
     name1 = name
     name = re.sub("ذئب", "wolf", name)
     name = re.sub("معلومات", "information", name)
     name = re.sub("قنوات", "channels", name)
     name = re.sub("مجموعات", "groups", name)
     name = re.sub("كتاب", "book", name)
     name = re.sub("تفاحه", "apple", name)
     name = re.sub("مصر", "egypt", name)
     name = re.sub("فلوس", "money", name)
     name = re.sub("اعلم", "i know", name)
     name = re.sub("تمساح", "crocodile", name)
     name = re.sub("مختلف", "different", name)
     name = re.sub("ذكي", "intelligent", name)
     name = re.sub("كلب", "dog", name)
     name = re.sub("صقر", "falcon", name)
     name = re.sub("مشكله", "error", name)
     name = re.sub("كمبيوتر", "computer", name)
     name = re.sub("اصدقاء", "friends", name)
     name = re.sub("منضده", "table", name)
     await r.set(f'{m.chat.id}:game:{Dev_FINAL}', name1,ex=600)
     await m.reply(plugins_games_words_124(name))
     return True
   
   if text == 'معاني':
     name = random.choice(m3any)
     name1 = name
     name = re.sub("قرد", "🐒", name)
     name = re.sub("دجاجه", "🐔", name)
     name = re.sub("بطريق", "🐧", name)
     name = re.sub("ضفدع", "🐸", name)
     name = re.sub("بومه", "🦉", name)
     name = re.sub("نحله", "🐝", name)
     name = re.sub("ديك", "🐓", name)
     name = re.sub("جمل", "🐫", name)
     name = re.sub("بقره", "🐄", name)
     name = re.sub("دولفين", "🐳", name)
     name = re.sub("تمساح", "🐊", name)
     name = re.sub("قرش", "🦈", name)
     name = re.sub("نمر", "🐅", name)
     name = re.sub("اخطبوط", "🐙", name)
     name = re.sub("سمكه", "🐟", name)
     name = re.sub("خفاش", "🦇", name)
     name = re.sub("اسد", "🦁", name)
     name = re.sub("فأر", "🐭", name)
     name = re.sub("ذئب", "🐺", name)
     name = re.sub("فراشه", "🦋", name)
     name = re.sub("عقرب", "🦂", name)
     name = re.sub("زرافه", "🦒", name)
     name = re.sub("قنفذ", "🦔", name)
     name = re.sub("تفاحه", "🍎", name)
     name = re.sub("باذنجان", "🍆", name)
     name = re.sub("قوس قزح", "🌈", name)
     name = re.sub("بزازه", "🍼", name)
     name = re.sub("بطيخ", "🍉", name)
     name = re.sub("وزه", "🦆", name)
     name = re.sub("كتكوت", "🐣", name)
     await r.set(f'{m.chat.id}:game:{Dev_FINAL}', name1,ex=600)
     await m.reply(plugins_games_words_161(name))
     return True
   
   if text == 'عربي':
     name = random.choice(Arab)
     name1 = name
     name = re.sub("اناث", "انثى", name)
     name = re.sub("ثيران", "ثور", name)
     name = re.sub("دروس", "درس", name)
     name = re.sub("فحص", "فحوص", name)
     name = re.sub("رجال", "رجل", name)
     name = re.sub("كتب", "كتاب", name)
     name = re.sub("ضغوط", "ضغط", name)
     name = re.sub("صف", "صفوف", name)
     name = re.sub("عصفور", "عصافير", name)
     name = re.sub("لصوص", "لص", name)
     name = re.sub("تماسيح", "تمساح", name)
     name = re.sub("ملك", "ملوك", name)
     name = re.sub("فصل", "فصول", name)
     name = re.sub("كلاب", "كلب", name)
     name = re.sub("صقور", "صقر", name)
     name = re.sub("عقد", "عقود", name)
     name = re.sub("بحور", "بحر", name)
     name = re.sub("هاتف", "هواتف", name)
     name = re.sub("حدائق", "حديقه", name)
     name = re.sub("مسرح", "مسارح", name)
     name = re.sub("جرائم", "جريمة", name)
     name = re.sub("مدارس", "مدرسة", name)
     name = re.sub("منزل", "منازل", name)
     name = re.sub("كرسي", "كراسي", name)
     name = re.sub("مناطق", "منطقة", name)
     name = re.sub("بيوت", "بيت", name)
     name = re.sub("بنك", "بنوك", name)
     name = re.sub("علم", "علوم", name)
     name = re.sub("وظائف", "وظيفة", name)
     name = re.sub("طلاب", "طالب", name)
     name = re.sub("مراحل", "مرحلة", name)
     name = re.sub("فنانين", "فنان", name)
     name = re.sub("صواريخ", "صاروخ", name)
     await r.set(f'{m.chat.id}:game:{Dev_FINAL}', name1,ex=600)
     await m.reply(plugins_games_words_201(name))
     return True
   
   if text == 'كلمات':
     name = random.choice(words)
     await r.set(f'{m.chat.id}:game:{Dev_FINAL}', name,ex=600)
     await m.reply(plugins_games_words_207(name))
     return True

   if text == 'تفكيك':
     tfkeek = random.choice(trteep)
     name = ' '.join(a for a in tfkeek)
     await r.set(f'{m.chat.id}:game:{Dev_FINAL}', name,ex=600)
     await m.reply(plugins_games_words_214(tfkeek))
     return True
   
   if text == 'تركيب':
     name = random.choice(tarkeeb)
     name1 = name
     name = re.sub("اناث", "ا ن ا ث", name)
     name = re.sub("ثيران", "ث ي ر ا ن", name)
     name = re.sub("دروس", "د ر و س", name)
     name = re.sub("فحص", "ف ح ص", name)
     name = re.sub("رجال", "ر ج ا ل", name)
     name = re.sub("انستا", "ا ن س ت ا", name)
     name = re.sub("ضغوط", "ض غ و ط", name)
     name = re.sub("صف", "ص ف", name)
     name = re.sub("رجب", "ر ج ب", name)
     name = re.sub("اسد", "ا س د", name)
     name = re.sub("وقع", "و ق ع", name)
     name = re.sub("ملك", "م ل ك", name)
     name = re.sub("فصل", "ف ص ل", name)
     name = re.sub("كلاب", "ك ل ا ب", name)
     name = re.sub("صقور", "ص ق و ر", name)
     name = re.sub("عقد", "ع ق د", name)
     name = re.sub("بحور", "ب ح و ر", name)
     name = re.sub("هاتف", "ه ا ت ف", name)
     name = re.sub("حدائق", "ح د ا ئ ق", name)
     name = re.sub("مسرح", "م س ر ح", name)
     name = re.sub("جرائم", "ج ر ا ئ م", name)
     name = re.sub("مدارس", "م د ا ر س", name)
     name = re.sub("منزل", "م ن ز ل", name)
     name = re.sub("كرسي", "ك ر س ي", name)
     name = re.sub("مناطق", "م ن ا ط ق", name)
     name = re.sub("بيوت", "ب ي و ت", name)
     name = re.sub("بنك", "ب ن ك", name)
     name = re.sub("علم", "ع ل م", name)
     name = re.sub("وظائف", "و ظ ا ئ ف", name)
     name = re.sub("طلاب", "ط ل ا ب", name)
     name = re.sub("مراحل", "م ر ا ح ل", name)
     name = re.sub("فنانين", "ف ن ا ن ي ن", name)
     name = re.sub("صواريخ", "ص و ا ر ي خ", name)
     await r.set(f'{m.chat.id}:game:{Dev_FINAL}', name1,ex=600)
     await m.reply(plugins_games_words_254(name))
   
   if text == 'اكمل':
     name = random.choice(mthal)
     name1 = name
     name = re.sub("اخوات", "لو قلبك مات متجيش على اتنين ... ", name)
     name = re.sub("زيهم", "اى ياعمهم اشتكيلك منهم تعمل ... ", name)
     name = re.sub("شمعتك", "دارى على ... تقيد", name)
     name = re.sub("داره", "من خرج من ... قل مقداره", name)
     name = re.sub("الوالدين", "رضا ... احسن من ابوك وامك", name)
     name = re.sub("الرءوس", "اذا تطاول الايدي تساوت ... ", name)
     name = re.sub("مرايه", "فى الوش ... وفى القفه سلايه", name)
     name = re.sub("حدو", "الشئ اللى يزيد عن ...  ينقلب لضدو", name)
     name = re.sub("رجالها", "مايجبها الا  ... ", name)
     name = re.sub("عدوك", "امشى عدل يحتار ... فيك", name)
     name = re.sub("الزبيب", "ضرب الحبيب زى اكل  ... ", name)
     name = re.sub("الغراب", "ياما جاب ...  لامه", name)
     name = re.sub("ماتو", "اللى اغتشو ... ", name)
     name = re.sub("اتمكن", "اتمسكن لحد ما ... ", name)
     name = re.sub("زجاج", "اللى بيتو من ... مايحدفش الناس بالطوب", name)
     name = re.sub("فار", "لو غاب القط العب يا ... ", name)
     name = re.sub("شهر", "امشي ... ولا تعدى نهر", name)
     name = re.sub("القتيل", "يقتل ... ويمشى فى جنازته", name)
     name = re.sub("الغطاس", "المايه تكدب ... ", name)
     name = re.sub("يكحلها", "جه ... عماها", name)
     name = re.sub("امه", "القرد فى عين ... غزال", name)
     await r.set(f'{m.chat.id}:game:{Dev_FINAL}', name1 ,ex=600)
     await m.reply(plugins_games_words_281(name))
     return True

   return None
