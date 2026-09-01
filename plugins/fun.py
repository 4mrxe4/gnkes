from helpers.context import get_global_r, get_global_dev, get_global_k
r = get_global_r()
Dev_FINAL = get_global_dev()
k = get_global_k()
import random, re, time
from threading import Thread
from compat import *
from compat import *
from compat import *
from helpers.ranks import *
from helpers.replies_store import (
    REPLIES,
    plugins_fun_104,
    plugins_fun_108,
    plugins_fun_112,
    plugins_fun_125,
    plugins_fun_128,
    plugins_fun_130,
    plugins_fun_140,
    plugins_fun_144,
    plugins_fun_151,
    plugins_fun_155,
    plugins_fun_159,
    plugins_fun_172,
    plugins_fun_175,
    plugins_fun_177,
    plugins_fun_187,
    plugins_fun_191,
    plugins_fun_198,
    plugins_fun_202,
    plugins_fun_206,
    plugins_fun_219,
    plugins_fun_222,
    plugins_fun_224,
    plugins_fun_234,
    plugins_fun_238,
    plugins_fun_245,
    plugins_fun_249,
    plugins_fun_253,
    plugins_fun_266,
    plugins_fun_269,
    plugins_fun_271,
    plugins_fun_281,
    plugins_fun_285,
    plugins_fun_292,
    plugins_fun_296,
    plugins_fun_300,
    plugins_fun_313,
    plugins_fun_316,
    plugins_fun_318,
    plugins_fun_328,
    plugins_fun_332,
    plugins_fun_339,
    plugins_fun_343,
    plugins_fun_347,
    plugins_fun_360,
    plugins_fun_363,
    plugins_fun_365,
    plugins_fun_375,
    plugins_fun_379,
    plugins_fun_386,
    plugins_fun_390,
    plugins_fun_394,
    plugins_fun_407,
    plugins_fun_410,
    plugins_fun_412,
    plugins_fun_422,
    plugins_fun_426,
    plugins_fun_433,
    plugins_fun_437,
    plugins_fun_441,
    plugins_fun_454,
    plugins_fun_457,
    plugins_fun_459,
    plugins_fun_46,
    plugins_fun_469,
    plugins_fun_473,
    plugins_fun_480,
    plugins_fun_484,
    plugins_fun_488,
    plugins_fun_50,
    plugins_fun_501,
    plugins_fun_504,
    plugins_fun_506,
    plugins_fun_516,
    plugins_fun_520,
    plugins_fun_527,
    plugins_fun_531,
    plugins_fun_535,
    plugins_fun_548,
    plugins_fun_551,
    plugins_fun_553,
    plugins_fun_563,
    plugins_fun_567,
    plugins_fun_57,
    plugins_fun_574,
    plugins_fun_578,
    plugins_fun_582,
    plugins_fun_595,
    plugins_fun_598,
    plugins_fun_600,
    plugins_fun_61,
    plugins_fun_610,
    plugins_fun_614,
    plugins_fun_621,
    plugins_fun_625,
    plugins_fun_629,
    plugins_fun_642,
    plugins_fun_645,
    plugins_fun_647,
    plugins_fun_65,
    plugins_fun_657,
    plugins_fun_661,
    plugins_fun_668,
    plugins_fun_672,
    plugins_fun_676,
    plugins_fun_689,
    plugins_fun_692,
    plugins_fun_694,
    plugins_fun_705,
    plugins_fun_708,
    plugins_fun_716,
    plugins_fun_718,
    plugins_fun_725,
    plugins_fun_728,
    plugins_fun_736,
    plugins_fun_738,
    plugins_fun_745,
    plugins_fun_748,
    plugins_fun_756,
    plugins_fun_758,
    plugins_fun_765,
    plugins_fun_767,
    plugins_fun_774,
    plugins_fun_776,
    plugins_fun_78,
    plugins_fun_783,
    plugins_fun_785,
    plugins_fun_790,
    plugins_fun_799,
    plugins_fun_807,
    plugins_fun_81,
    plugins_fun_818,
    plugins_fun_83,
    plugins_fun_93,
    plugins_fun_958,
    plugins_fun_97,
)



@Client.on_message(filters.text & filters.group, group=34)
async def funHandler(c,m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    k = await r.get(f'{Dev_FINAL}:botkey')
    channel = await r.get(f'{Dev_FINAL}:BotChannel') if await r.get(f'{Dev_FINAL}:BotChannel') else ''
    await funFunc(c,m,k,channel)
    
async def funFunc(c,m,k,channel):
   r = get_global_r()
   Dev_FINAL = get_global_dev()
   k = get_global_k()
   if await r.get(f'{m.chat.id}:disableFun:{Dev_FINAL}'):  return 
   if not await check_global_restrictions(c, m, k):
       return
   text = m.text
   name = await r.get(f'{Dev_FINAL}:BotName') if await r.get(f'{Dev_FINAL}:BotName') else 'فاينل'
   if text.startswith(f'{name} '):
      text = text.replace(f'{name} ','')
   if await r.get(f'{m.chat.id}:Custom:{m.chat.id}{Dev_FINAL}&text={text}'):
       text = await r.get(f'{m.chat.id}:Custom:{m.chat.id}{Dev_FINAL}&text={text}')
   if await r.get(f'Custom:{Dev_FINAL}&text={text}'):
       text = await r.get(f'Custom:{Dev_FINAL}&text={text}')
   if await check_and_guard_locked_command(c, m, k, text):
       return

   if text == 'رفع كيك' or text == 'رفع كيكه' or text == 'رفع كيكة':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention()
       id = m.reply_to_message.from_user.id
       if await r.sismember(f'{Dev_FINAL}:CakeList:{m.chat.id}',id):
         return await m.reply(plugins_fun_46(mention, k))
       else:
         await r.sadd(f'{Dev_FINAL}:CakeList:{m.chat.id}',id)
         await r.set(f'{Dev_FINAL}:CakeName:{id}', mention)
         return await m.reply(plugins_fun_50(mention, k))
   
   if text == 'تنزيل كيك' or text == 'تنزيل كيكه' or text == 'تنزيل كيكة':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention()
       id = m.reply_to_message.from_user.id
       if not await r.sismember(f'{Dev_FINAL}:CakeList:{m.chat.id}',id):
         return await m.reply(plugins_fun_57(mention, k))
       else:
         await r.srem(f'{Dev_FINAL}:CakeList:{m.chat.id}',id)
         await r.delete(f'{Dev_FINAL}:CakeName:{id}')
         return await m.reply(plugins_fun_61(mention, k))
   
   if text == 'قائمه الكيك' or text == 'قائمة الكيك':
     if not await r.smembers(f'{Dev_FINAL}:CakeList:{m.chat.id}'):
       return await m.reply(plugins_fun_65(k))
     else:
       txt = '• قائمة الكيك 🍰\n'
       count = 1
       for cake in await r.smembers(f'{Dev_FINAL}:CakeList:{m.chat.id}'):
          mention = await r.get(f'{Dev_FINAL}:CakeName:{cake}')
          txt += f'{count} - ⁪⁬⁪⁬{mention}\n'
          count += 1
       txt += '\n'
       return await m.reply(txt, disable_web_page_preview=True)
   
   if text == 'مسح قائمة الكيك' or text == 'مسح قائمه الكيك':
     if not await admin_pls(m.from_user.id,m.chat.id):
       return await m.reply(plugins_fun_78(k))
     else:
       if not await r.smembers(f'{Dev_FINAL}:CakeList:{m.chat.id}'):
         return await m.reply(plugins_fun_81(k))
       else:
         await m.reply(plugins_fun_83(k))
         for cake in await r.smembers(f'{Dev_FINAL}:CakeList:{m.chat.id}'):
           await r.srem(f'{Dev_FINAL}:CakeList:{m.chat.id}',int(cake))
           await r.delete(f'{Dev_FINAL}:CakeName:{cake}')
           
   if text == 'رفع عسل':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention()
       id = m.reply_to_message.from_user.id
       if await r.sismember(f'{Dev_FINAL}:3SLList:{m.chat.id}',id):
         return await m.reply(plugins_fun_93(mention, k))
       else:
         await r.sadd(f'{Dev_FINAL}:3SLList:{m.chat.id}',id)
         await r.set(f'{Dev_FINAL}:3SLName:{id}', mention)
         return await m.reply(plugins_fun_97(mention, k))
   
   if text == 'تنزيل عسل':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention()
       id = m.reply_to_message.from_user.id
       if not await r.sismember(f'{Dev_FINAL}:3SLList:{m.chat.id}',id):
         return await m.reply(plugins_fun_104(mention, k))
       else:
         await r.srem(f'{Dev_FINAL}:3SLList:{m.chat.id}',id)
         await r.delete(f'{Dev_FINAL}:3SLName:{id}')
         return await m.reply(plugins_fun_108(mention, k))
   
   if text == 'قائمه العسل' or text == 'قائمة العسل':
     if not await r.smembers(f'{Dev_FINAL}:3SLList:{m.chat.id}'):
       return await m.reply(plugins_fun_112(k))
     else:
       txt = '• قائمة العسل 🍯\n'
       count = 1
       for cake in await r.smembers(f'{Dev_FINAL}:3SLList:{m.chat.id}'):
          mention = await r.get(f'{Dev_FINAL}:3SLName:{cake}')
          txt += f'{count} - ⁪⁬⁪⁬{mention}\n'
          count += 1
       txt += '\n'
       return await m.reply(txt, disable_web_page_preview=True)
   
   if text == 'مسح قائمة العسل' or text == 'مسح قائمه العسل':
     if not await admin_pls(m.from_user.id,m.chat.id):
       return await m.reply(plugins_fun_125(k))
     else:
       if not await r.smembers(f'{Dev_FINAL}:3SLList:{m.chat.id}'):
         return await m.reply(plugins_fun_128(k))
       else:
         await m.reply(plugins_fun_130(k))
         for cake in await r.smembers(f'{Dev_FINAL}:3SLList:{m.chat.id}'):
           await r.srem(f'{Dev_FINAL}:3SLList:{m.chat.id}',int(cake))
           await r.delete(f'{Dev_FINAL}:3SLName:{cake}')

   if text == 'رفع نصاب':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention()
       id = m.reply_to_message.from_user.id
       if await r.sismember(f'{Dev_FINAL}:ZQList:{m.chat.id}',id):
         return await m.reply(plugins_fun_140(mention, k))
       else:
         await r.sadd(f'{Dev_FINAL}:ZQList:{m.chat.id}',id)
         await r.set(f'{Dev_FINAL}:ZQName:{id}', mention)
         return await m.reply(plugins_fun_144(mention, k))
   
   if text == 'تنزيل نصاب':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention()
       id = m.reply_to_message.from_user.id
       if not await r.sismember(f'{Dev_FINAL}:ZQList:{m.chat.id}',id):
         return await m.reply(plugins_fun_151(mention, k))
       else:
         await r.srem(f'{Dev_FINAL}:ZQList:{m.chat.id}',id)
         await r.delete(f'{Dev_FINAL}:ZQName:{id}')
         return await m.reply(plugins_fun_155(mention, k))
   
   if text == 'قائمه النصابين' or text == 'قائمة النصابين':
     if not await r.smembers(f'{Dev_FINAL}:ZQList:{m.chat.id}'):
       return await m.reply(plugins_fun_159(k))
     else:
       txt = '• قائمة النصابين 💩\n'
       count = 1
       for cake in await r.smembers(f'{Dev_FINAL}:ZQList:{m.chat.id}'):
          mention = await r.get(f'{Dev_FINAL}:ZQName:{cake}')
          txt += f'{count} - ⁪⁬⁪⁬{mention}\n'
          count += 1
       txt += '\n'
       return await m.reply(txt, disable_web_page_preview=True)
   
   if text == 'مسح قائمة النصابين' or text == 'مسح قائمه النصابين':
     if not await admin_pls(m.from_user.id,m.chat.id):
       return await m.reply(plugins_fun_172(k))
     else:
       if not await r.smembers(f'{Dev_FINAL}:ZQList:{m.chat.id}'):
         return await m.reply(plugins_fun_175(k))
       else:
         await m.reply(plugins_fun_177(k))
         for cake in await r.smembers(f'{Dev_FINAL}:ZQList:{m.chat.id}'):
           await r.srem(f'{Dev_FINAL}:ZQList:{m.chat.id}',int(cake))
           await r.delete(f'{Dev_FINAL}:ZQName:{cake}')

   if text == 'رفع حمار':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention()
       id = m.reply_to_message.from_user.id
       if await r.sismember(f'{Dev_FINAL}:7MRList:{m.chat.id}',id):
         return await m.reply(plugins_fun_187(mention, k))
       else:
         await r.sadd(f'{Dev_FINAL}:7MRList:{m.chat.id}',id)
         await r.set(f'{Dev_FINAL}:7MRName:{id}', mention)
         return await m.reply(plugins_fun_191(mention, k))
   
   if text == 'تنزيل حمار':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention()
       id = m.reply_to_message.from_user.id
       if not await r.sismember(f'{Dev_FINAL}:7MRList:{m.chat.id}',id):
         return await m.reply(plugins_fun_198(mention, k))
       else:
         await r.srem(f'{Dev_FINAL}:7MRList:{m.chat.id}',id)
         await r.delete(f'{Dev_FINAL}:7MRName:{id}')
         return await m.reply(plugins_fun_202(mention, k))
   
   if text == 'قائمه الحمير' or text == 'قائمة الحمير':
     if not await r.smembers(f'{Dev_FINAL}:7MRList:{m.chat.id}'):
       return await m.reply(plugins_fun_206(k))
     else:
       txt = '• قائمة الحمير 🦓\n'
       count = 1
       for cake in await r.smembers(f'{Dev_FINAL}:7MRList:{m.chat.id}'):
          mention = await r.get(f'{Dev_FINAL}:7MRName:{cake}')
          txt += f'{count} - ⁪⁬⁪⁬{mention}\n'
          count += 1
       txt += '\n'
       return await m.reply(txt, disable_web_page_preview=True)
   
   if text == 'مسح قائمة الحمير' or text == 'مسح قائمه الحمير':
     if not await admin_pls(m.from_user.id,m.chat.id):
       return await m.reply(plugins_fun_219(k))
     else:
       if not await r.smembers(f'{Dev_FINAL}:7MRList:{m.chat.id}'):
         return await m.reply(plugins_fun_222(k))
       else:
         await m.reply(plugins_fun_224(k))
         for cake in await r.smembers(f'{Dev_FINAL}:7MRList:{m.chat.id}'):
           await r.srem(f'{Dev_FINAL}:7MRList:{m.chat.id}',int(cake))
           await r.delete(f'{Dev_FINAL}:7MRName:{cake}')

   if text == 'رفع بقرة' or text == 'رفع بقره':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention()
       id = m.reply_to_message.from_user.id
       if await r.sismember(f'{Dev_FINAL}:COWList:{m.chat.id}',id):
         return await m.reply(plugins_fun_234(mention, k))
       else:
         await r.sadd(f'{Dev_FINAL}:COWList:{m.chat.id}',id)
         await r.set(f'{Dev_FINAL}:COWName:{id}', mention)
         return await m.reply(plugins_fun_238(mention, k))
   
   if text == 'تنزيل بقرة' or text == 'تنزيل بقره':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention()
       id = m.reply_to_message.from_user.id
       if not await r.sismember(f'{Dev_FINAL}:COWList:{m.chat.id}',id):
         return await m.reply(plugins_fun_245(mention, k))
       else:
         await r.srem(f'{Dev_FINAL}:COWList:{m.chat.id}',id)
         await r.delete(f'{Dev_FINAL}:COWName:{id}')
         return await m.reply(plugins_fun_249(mention, k))
   
   if text == 'قائمه البقر' or text == 'قائمة البقر':
     if not await r.smembers(f'{Dev_FINAL}:COWList:{m.chat.id}'):
       return await m.reply(plugins_fun_253(k))
     else:
       txt = '• قائمة البقر 🐄\n'
       count = 1
       for cake in await r.smembers(f'{Dev_FINAL}:COWList:{m.chat.id}'):
          mention = await r.get(f'{Dev_FINAL}:COWName:{cake}')
          txt += f'{count} - ⁪⁬⁪⁬{mention}\n'
          count += 1
       txt += '\n'
       return await m.reply(txt, disable_web_page_preview=True)
   
   if text == 'مسح قائمة البقر' or text == 'مسح قائمه البقر':
     if not await admin_pls(m.from_user.id,m.chat.id):
       return await m.reply(plugins_fun_266(k))
     else:
       if not await r.smembers(f'{Dev_FINAL}:COWList:{m.chat.id}'):
         return await m.reply(plugins_fun_269(k))
       else:
         await m.reply(plugins_fun_271(k))
         for cake in await r.smembers(f'{Dev_FINAL}:COWList:{m.chat.id}'):
           await r.srem(f'{Dev_FINAL}:COWList:{m.chat.id}',int(cake))
           await r.delete(f'{Dev_FINAL}:COWName:{cake}')

   if text == 'رفع كلب':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention()
       id = m.reply_to_message.from_user.id
       if await r.sismember(f'{Dev_FINAL}:DOGList:{m.chat.id}',id):
         return await m.reply(plugins_fun_281(mention, k))
       else:
         await r.sadd(f'{Dev_FINAL}:DOGList:{m.chat.id}',id)
         await r.set(f'{Dev_FINAL}:DOGName:{id}', mention)
         return await m.reply(plugins_fun_285(mention, k))
   
   if text == 'تنزيل كلب':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention()
       id = m.reply_to_message.from_user.id
       if not await r.sismember(f'{Dev_FINAL}:DOGList:{m.chat.id}',id):
         return await m.reply(plugins_fun_292(mention, k))
       else:
         await r.srem(f'{Dev_FINAL}:DOGList:{m.chat.id}',id)
         await r.delete(f'{Dev_FINAL}:DOGName:{id}')
         return await m.reply(plugins_fun_296(mention, k))
   
   if text == 'قائمه الكلاب' or text == 'قائمة الكلاب':
     if not await r.smembers(f'{Dev_FINAL}:DOGList:{m.chat.id}'):
       return await m.reply(plugins_fun_300(k))
     else:
       txt = '• قائمة الكلاب 🐩\n'
       count = 1
       for cake in await r.smembers(f'{Dev_FINAL}:DOGList:{m.chat.id}'):
          mention = await r.get(f'{Dev_FINAL}:DOGName:{cake}')
          txt += f'{count} - ⁪⁬⁪⁬{mention}\n'
          count += 1
       txt += '\n'
       return await m.reply(txt, disable_web_page_preview=True)
   
   if text == 'مسح قائمة الكلاب' or text == 'مسح قائمه الكلاب':
     if not await admin_pls(m.from_user.id,m.chat.id):
       return await m.reply(plugins_fun_313(k))
     else:
       if not await r.smembers(f'{Dev_FINAL}:DOGList:{m.chat.id}'):
         return await m.reply(plugins_fun_316(k))
       else:
         await m.reply(plugins_fun_318(k))
         for cake in await r.smembers(f'{Dev_FINAL}:DOGList:{m.chat.id}'):
           await r.srem(f'{Dev_FINAL}:DOGList:{m.chat.id}',int(cake))
           await r.delete(f'{Dev_FINAL}:DOGName:{cake}')

   if text == 'رفع قرد':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention()
       id = m.reply_to_message.from_user.id
       if await r.sismember(f'{Dev_FINAL}:MONList:{m.chat.id}',id):
         return await m.reply(plugins_fun_328(mention, k))
       else:
         await r.sadd(f'{Dev_FINAL}:MONList:{m.chat.id}',id)
         await r.set(f'{Dev_FINAL}:MONName:{id}', mention)
         return await m.reply(plugins_fun_332(mention, k))
   
   if text == 'تنزيل قرد':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention()
       id = m.reply_to_message.from_user.id
       if not await r.sismember(f'{Dev_FINAL}:MONList:{m.chat.id}',id):
         return await m.reply(plugins_fun_339(mention, k))
       else:
         await r.srem(f'{Dev_FINAL}:MONList:{m.chat.id}',id)
         await r.delete(f'{Dev_FINAL}:MONName:{id}')
         return await m.reply(plugins_fun_343(mention, k))
   
   if text == 'قائمه القرود' or text == 'قائمة القرود':
     if not await r.smembers(f'{Dev_FINAL}:MONList:{m.chat.id}'):
       return await m.reply(plugins_fun_347(k))
     else:
       txt = '• قائمة القرود 🐒\n'
       count = 1
       for cake in await r.smembers(f'{Dev_FINAL}:MONList:{m.chat.id}'):
          mention = await r.get(f'{Dev_FINAL}:MONName:{cake}')
          txt += f'{count} - ⁪⁬⁪⁬{mention}\n'
          count += 1
       txt += '\n'
       return await m.reply(txt, disable_web_page_preview=True)
   
   if text == 'مسح قائمة القرود' or text == 'مسح قائمه القرود':
     if not await admin_pls(m.from_user.id,m.chat.id):
       return await m.reply(plugins_fun_360(k))
     else:
       if not await r.smembers(f'{Dev_FINAL}:MONList:{m.chat.id}'):
         return await m.reply(plugins_fun_363(k))
       else:
         await m.reply(plugins_fun_365(k))
         for cake in await r.smembers(f'{Dev_FINAL}:MONList:{m.chat.id}'):
           await r.srem(f'{Dev_FINAL}:MONList:{m.chat.id}',int(cake))
           await r.delete(f'{Dev_FINAL}:MONName:{cake}')

   if text == 'رفع تيس':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention()
       id = m.reply_to_message.from_user.id
       if await r.sismember(f'{Dev_FINAL}:TESList:{m.chat.id}',id):
         return await m.reply(plugins_fun_375(mention, k))
       else:
         await r.sadd(f'{Dev_FINAL}:TESList:{m.chat.id}',id)
         await r.set(f'{Dev_FINAL}:TESName:{id}', mention)
         return await m.reply(plugins_fun_379(mention, k))
   
   if text == 'تنزيل تيس':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention()
       id = m.reply_to_message.from_user.id
       if not await r.sismember(f'{Dev_FINAL}:TESList:{m.chat.id}',id):
         return await m.reply(plugins_fun_386(mention, k))
       else:
         await r.srem(f'{Dev_FINAL}:TESList:{m.chat.id}',id)
         await r.delete(f'{Dev_FINAL}:TESName:{id}')
         return await m.reply(plugins_fun_390(mention, k))
   
   if text == 'قائمه التيس' or text == 'قائمة التيس':
     if not await r.smembers(f'{Dev_FINAL}:TESList:{m.chat.id}'):
       return await m.reply(plugins_fun_394(k))
     else:
       txt = '• قائمة التيوس 🐐\n'
       count = 1
       for cake in await r.smembers(f'{Dev_FINAL}:TESList:{m.chat.id}'):
          mention = await r.get(f'{Dev_FINAL}:TESName:{cake}')
          txt += f'{count} - ⁪⁬⁪⁬{mention}\n'
          count += 1
       txt += '\n'
       return await m.reply(txt, disable_web_page_preview=True)
   
   if text == 'مسح قائمة التيس' or text == 'مسح قائمه التيس':
     if not await admin_pls(m.from_user.id,m.chat.id):
       return await m.reply(plugins_fun_407(k))
     else:
       if not await r.smembers(f'{Dev_FINAL}:TESList:{m.chat.id}'):
         return await m.reply(plugins_fun_410(k))
       else:
         await m.reply(plugins_fun_412(k))
         for cake in await r.smembers(f'{Dev_FINAL}:TESList:{m.chat.id}'):
           await r.srem(f'{Dev_FINAL}:TESList:{m.chat.id}',int(cake))
           await r.delete(f'{Dev_FINAL}:TESName:{cake}')

   if text == 'رفع ثور':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention()
       id = m.reply_to_message.from_user.id
       if await r.sismember(f'{Dev_FINAL}:TORList:{m.chat.id}',id):
         return await m.reply(plugins_fun_422(mention, k))
       else:
         await r.sadd(f'{Dev_FINAL}:TORList:{m.chat.id}',id)
         await r.set(f'{Dev_FINAL}:TORName:{id}', mention)
         return await m.reply(plugins_fun_426(mention, k))
   
   if text == 'تنزيل ثور':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention()
       id = m.reply_to_message.from_user.id
       if not await r.sismember(f'{Dev_FINAL}:TORList:{m.chat.id}',id):
         return await m.reply(plugins_fun_433(mention, k))
       else:
         await r.srem(f'{Dev_FINAL}:TORList:{m.chat.id}',id)
         await r.delete(f'{Dev_FINAL}:TORName:{id}')
         return await m.reply(plugins_fun_437(mention, k))
   
   if text == 'قائمه الثور' or text == 'قائمة الثور':
     if not await r.smembers(f'{Dev_FINAL}:TORList:{m.chat.id}'):
       return await m.reply(plugins_fun_441(k))
     else:
       txt = '• قائمة الثور 🐂\n'
       count = 1
       for cake in await r.smembers(f'{Dev_FINAL}:TORList:{m.chat.id}'):
          mention = await r.get(f'{Dev_FINAL}:TORName:{cake}')
          txt += f'{count} - ⁪⁬⁪⁬{mention}\n'
          count += 1
       txt += '\n'
       return await m.reply(txt, disable_web_page_preview=True)
   
   if text == 'مسح قائمة الثور' or text == 'مسح قائمه الثور':
     if not await admin_pls(m.from_user.id,m.chat.id):
       return await m.reply(plugins_fun_454(k))
     else:
       if not await r.smembers(f'{Dev_FINAL}:TORList:{m.chat.id}'):
         return await m.reply(plugins_fun_457(k))
       else:
         await m.reply(plugins_fun_459(k))
         for cake in await r.smembers(f'{Dev_FINAL}:TORList:{m.chat.id}'):
           await r.srem(f'{Dev_FINAL}:TORList:{m.chat.id}',int(cake))
           await r.delete(f'{Dev_FINAL}:TORName:{cake}')

   if text == 'رفع هكر':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention()
       id = m.reply_to_message.from_user.id
       if await r.sismember(f'{Dev_FINAL}:B3SList:{m.chat.id}',id):
         return await m.reply(plugins_fun_469(mention, k))
       else:
         await r.sadd(f'{Dev_FINAL}:B3SList:{m.chat.id}',id)
         await r.set(f'{Dev_FINAL}:B3SName:{id}', mention)
         return await m.reply(plugins_fun_473(mention, k))
   
   if text == 'تنزيل هكر':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention()
       id = m.reply_to_message.from_user.id
       if not await r.sismember(f'{Dev_FINAL}:B3SList:{m.chat.id}',id):
         return await m.reply(plugins_fun_480(mention, k))
       else:
         await r.srem(f'{Dev_FINAL}:B3SList:{m.chat.id}',id)
         await r.delete(f'{Dev_FINAL}:B3SName:{id}')
         return await m.reply(plugins_fun_484(mention, k))
   
   if text == 'قائمه الهكر' or text == 'قائمة الهكر':
     if not await r.smembers(f'{Dev_FINAL}:B3SList:{m.chat.id}'):
       return await m.reply(plugins_fun_488(k))
     else:
       txt = '• قائمة الهكر 🏅\n'
       count = 1
       for cake in await r.smembers(f'{Dev_FINAL}:B3SList:{m.chat.id}'):
          mention = await r.get(f'{Dev_FINAL}:B3SName:{cake}')
          txt += f'{count} - ⁪⁬⁪⁬{mention}\n'
          count += 1
       txt += '\n'
       return await m.reply(txt, disable_web_page_preview=True)
   
   if text == 'مسح قائمة الهكر' or text == 'مسح قائمه الهكر':
     if not await admin_pls(m.from_user.id,m.chat.id):
       return await m.reply(plugins_fun_501(k))
     else:
       if not await r.smembers(f'{Dev_FINAL}:B3SList:{m.chat.id}'):
         return await m.reply(plugins_fun_504(k))
       else:
         await m.reply(plugins_fun_506(k))
         for cake in await r.smembers(f'{Dev_FINAL}:B3SList:{m.chat.id}'):
           await r.srem(f'{Dev_FINAL}:B3SList:{m.chat.id}',int(cake))
           await r.delete(f'{Dev_FINAL}:B3SName:{cake}')

   if text == 'رفع دجاجه' or text == 'رفع دجاجة':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention()
       id = m.reply_to_message.from_user.id
       if await r.sismember(f'{Dev_FINAL}:DJJList:{m.chat.id}',id):
         return await m.reply(plugins_fun_516(mention, k))
       else:
         await r.sadd(f'{Dev_FINAL}:DJJList:{m.chat.id}',id)
         await r.set(f'{Dev_FINAL}:DJJName:{id}', mention)
         return await m.reply(plugins_fun_520(mention, k))
   
   if text == 'تنزيل دجاجه' or text == 'تنزيل دجاجة':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention()
       id = m.reply_to_message.from_user.id
       if not await r.sismember(f'{Dev_FINAL}:DJJList:{m.chat.id}',id):
         return await m.reply(plugins_fun_527(mention, k))
       else:
         await r.srem(f'{Dev_FINAL}:DJJList:{m.chat.id}',id)
         await r.delete(f'{Dev_FINAL}:DJJName:{id}')
         return await m.reply(plugins_fun_531(mention, k))
   
   if text == 'قائمه الدجاج' or text == 'قائمة الدجاج':
     if not await r.smembers(f'{Dev_FINAL}:DJJList:{m.chat.id}'):
       return await m.reply(plugins_fun_535(k))
     else:
       txt = '• قائمة الدجاج 🐓\n'
       count = 1
       for cake in await r.smembers(f'{Dev_FINAL}:DJJList:{m.chat.id}'):
          mention = await r.get(f'{Dev_FINAL}:DJJName:{cake}')
          txt += f'{count} - ⁪⁬⁪⁬{mention}\n'
          count += 1
       txt += '\n'
       return await m.reply(txt, disable_web_page_preview=True)
   
   if text == 'مسح قائمة الدجاج' or text == 'مسح قائمه الدجاج':
     if not await admin_pls(m.from_user.id,m.chat.id):
       return await m.reply(plugins_fun_548(k))
     else:
       if not await r.smembers(f'{Dev_FINAL}:DJJList:{m.chat.id}'):
         return await m.reply(plugins_fun_551(k))
       else:
         await m.reply(plugins_fun_553(k))
         for cake in await r.smembers(f'{Dev_FINAL}:DJJList:{m.chat.id}'):
           await r.srem(f'{Dev_FINAL}:DJJList:{m.chat.id}',int(cake))
           await r.delete(f'{Dev_FINAL}:DJJName:{cake}')

   if text == 'رفع ملكه':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention()
       id = m.reply_to_message.from_user.id
       if await r.sismember(f'{Dev_FINAL}:HTFList:{m.chat.id}',id):
         return await m.reply(plugins_fun_563(mention, k))
       else:
         await r.sadd(f'{Dev_FINAL}:HTFList:{m.chat.id}',id)
         await r.set(f'{Dev_FINAL}:HTFName:{id}', mention)
         return await m.reply(plugins_fun_567(mention, k))
   
   if text == 'تنزيل ملكه':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention()
       id = m.reply_to_message.from_user.id
       if not await r.sismember(f'{Dev_FINAL}:HTFList:{m.chat.id}',id):
         return await m.reply(plugins_fun_574(mention, k))
       else:
         await r.srem(f'{Dev_FINAL}:HTFList:{m.chat.id}',id)
         await r.delete(f'{Dev_FINAL}:HTFName:{id}')
         return await m.reply(plugins_fun_578(mention, k))
   
   if text == 'قائمه الهطوف' or text == 'قائمة الهطوف':
     if not await r.smembers(f'{Dev_FINAL}:HTFList:{m.chat.id}'):
       return await m.reply(plugins_fun_582(k))
     else:
       txt = '• قائمة الهطوف 🧱\n'
       count = 1
       for cake in await r.smembers(f'{Dev_FINAL}:HTFList:{m.chat.id}'):
          mention = await r.get(f'{Dev_FINAL}:HTFName:{cake}')
          txt += f'{count} - ⁪⁬⁪⁬{mention}\n'
          count += 1
       txt += '\n'
       return await m.reply(txt, disable_web_page_preview=True)
   
   if text == 'مسح قائمة الهطوف' or text == 'مسح قائمه الهطوف':
     if not await admin_pls(m.from_user.id,m.chat.id):
       return await m.reply(plugins_fun_595(k))
     else:
       if not await r.smembers(f'{Dev_FINAL}:HTFList:{m.chat.id}'):
         return await m.reply(plugins_fun_598(k))
       else:
         await m.reply(plugins_fun_600(k))
         for cake in await r.smembers(f'{Dev_FINAL}:HTFList:{m.chat.id}'):
           await r.srem(f'{Dev_FINAL}:HTFList:{m.chat.id}',int(cake))
           await r.delete(f'{Dev_FINAL}:HTFName:{cake}')

   if text == 'رفع صياد':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention()
       id = m.reply_to_message.from_user.id
       if await r.sismember(f'{Dev_FINAL}:SYDList:{m.chat.id}',id):
         return await m.reply(plugins_fun_610(mention, k))
       else:
         await r.sadd(f'{Dev_FINAL}:SYDList:{m.chat.id}',id)
         await r.set(f'{Dev_FINAL}:SYDName:{id}', mention)
         return await m.reply(plugins_fun_614(mention, k))
   
   if text == 'تنزيل صياد':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention()
       id = m.reply_to_message.from_user.id
       if not await r.sismember(f'{Dev_FINAL}:SYDList:{m.chat.id}',id):
         return await m.reply(plugins_fun_621(mention, k))
       else:
         await r.srem(f'{Dev_FINAL}:SYDList:{m.chat.id}',id)
         await r.delete(f'{Dev_FINAL}:SYDName:{id}')
         return await m.reply(plugins_fun_625(mention, k))
   
   if text == 'قائمه الصيادين' or text == 'قائمة الصيادين':
     if not await r.smembers(f'{Dev_FINAL}:SYDList:{m.chat.id}'):
       return await m.reply(plugins_fun_629(k))
     else:
       txt = '• قائمة الصيادين 🔫\n'
       count = 1
       for cake in await r.smembers(f'{Dev_FINAL}:SYDList:{m.chat.id}'):
          mention = await r.get(f'{Dev_FINAL}:SYDName:{cake}')
          txt += f'{count} - ⁪⁬⁪⁬{mention}\n'
          count += 1
       txt += '\n'
       return await m.reply(txt, disable_web_page_preview=True)
   
   if text == 'مسح قائمة الصيادين' or text == 'مسح قائمه الصيادين':
     if not await admin_pls(m.from_user.id,m.chat.id):
       return await m.reply(plugins_fun_642(k))
     else:
       if not await r.smembers(f'{Dev_FINAL}:SYDList:{m.chat.id}'):
         return await m.reply(plugins_fun_645(k))
       else:
         await m.reply(plugins_fun_647(k))
         for cake in await r.smembers(f'{Dev_FINAL}:SYDList:{m.chat.id}'):
           await r.srem(f'{Dev_FINAL}:SYDList:{m.chat.id}',int(cake))
           await r.delete(f'{Dev_FINAL}:SYDName:{cake}')

   if text == 'رفع خروف':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention()
       id = m.reply_to_message.from_user.id
       if await r.sismember(f'{Dev_FINAL}:5RFList:{m.chat.id}',id):
         return await m.reply(plugins_fun_657(mention, k))
       else:
         await r.sadd(f'{Dev_FINAL}:5RFList:{m.chat.id}',id)
         await r.set(f'{Dev_FINAL}:5RFName:{id}', mention)
         return await m.reply(plugins_fun_661(mention, k))
   
   if text == 'تنزيل خروف':
     if m.reply_to_message and m.reply_to_message.from_user:
       mention = m.reply_to_message.from_user.mention()
       id = m.reply_to_message.from_user.id
       if not await r.sismember(f'{Dev_FINAL}:5RFList:{m.chat.id}',id):
         return await m.reply(plugins_fun_668(mention, k))
       else:
         await r.srem(f'{Dev_FINAL}:5RFList:{m.chat.id}',id)
         await r.delete(f'{Dev_FINAL}:5RFName:{id}')
         return await m.reply(plugins_fun_672(mention, k))
   
   if text == 'قائمه الخرفان' or text == 'قائمة الخرفان':
     if not await r.smembers(f'{Dev_FINAL}:5RFList:{m.chat.id}'):
       return await m.reply(plugins_fun_676(k))
     else:
       txt = '• قائمة الخرفان 🐏\n'
       count = 1
       for cake in await r.smembers(f'{Dev_FINAL}:5RFList:{m.chat.id}'):
          mention = await r.get(f'{Dev_FINAL}:5RFName:{cake}')
          txt += f'{count} - ⁪⁬⁪⁬{mention}\n'
          count += 1
       txt += '\n'
       return await m.reply(txt, disable_web_page_preview=True)
   
   if text == 'مسح قائمة الخرفان' or text == 'مسح قائمه الخرفان':
     if not await admin_pls(m.from_user.id,m.chat.id):
       return await m.reply(plugins_fun_689(k))
     else:
       if not await r.smembers(f'{Dev_FINAL}:5RFList:{m.chat.id}'):
         return await m.reply(plugins_fun_692(k))
       else:
         await m.reply(plugins_fun_694(k))
         for cake in await r.smembers(f'{Dev_FINAL}:5RFList:{m.chat.id}'):
           await r.srem(f'{Dev_FINAL}:5RFList:{m.chat.id}',int(cake))
           await r.delete(f'{Dev_FINAL}:5RFName:{cake}')


   if text == "نسبه الحب" or text == "نسبة الحب" or text == "نسبه حب" or text == "نسبة حب":
     percentages = ["😂 10", "🤤 20", "😢 30", "😔 35", "😒 75", "🤩 34", "😗 66", "🤐 82", "😪 23", "😫 19", "😛 55", "😜 80", "😲 63", "😓 32", "🙂 27", "😎 89", "😋 99", "😁 98", "😀 79", "🤣 100", "😣 8", "🙄 3", "😕 6", "🤯 0"]
     percentage = random.choice(percentages)
     if m.reply_to_message:
       target = m.reply_to_message.from_user.mention()
       return await m.reply(plugins_fun_705(m.from_user.mention(), target, percentage))
     else:
       await r.setex(f"love_wait:{m.from_user.id}:{m.chat.id}", 120, "true")
       return await m.reply(plugins_fun_708(k))

   if text and await r.get(f"love_wait:{m.from_user.id}:{m.chat.id}"):
     names = text.split()
     if len(names) >= 2:
       percentages = ["😂 10", "🤤 20", "😢 30", "😔 35", "😒 75", "🤩 34", "😗 66", "🤐 82", "😪 23", "😫 19", "😛 55", "😜 80", "😲 63", "😓 32", "🙂 27", "😎 89", "😋 99", "😁 98", "😀 79", "🤣 100", "😣 8", "🙄 3", "😕 6", "🤯 0"]
       percentage = random.choice(percentages)
       await r.delete(f"love_wait:{m.from_user.id}:{m.chat.id}")
       return await m.reply(plugins_fun_716(names[0], names[1], percentage))
     else:
       return await m.reply(plugins_fun_718(k))

   if text == "نسبه الكره" or text == "نسبة الكره" or text == "نسبه كره" or text == "نسبة كره":
     percentages = ["😂 10", "🤤 20", "😢 30", "😔 35", "😒 75", "🤩 34", "😗 66", "🤐 82", "😪 23", "😫 19", "😛 55", "😜 80", "😲 63", "😓 32", "🙂 27", "😎 89", "😋 99", "😁 98", "😀 79", "🤣 100", "😣 8", "🙄 3", "😕 6", "🤯 0"]
     percentage = random.choice(percentages)
     if m.reply_to_message:
       target = m.reply_to_message.from_user.mention()
       return await m.reply(plugins_fun_725(m.from_user.mention(), target, percentage))
     else:
       await r.setex(f"hate_wait:{m.from_user.id}:{m.chat.id}", 120, "true")
       return await m.reply(plugins_fun_728(k))

   if text and await r.get(f"hate_wait:{m.from_user.id}:{m.chat.id}"):
     names = text.split()
     if len(names) >= 2:
       percentages = ["😂 10", "🤤 20", "😢 30", "😔 35", "😒 75", "🤩 34", "😗 66", "🤐 82", "😪 23", "😫 19", "😛 55", "😜 80", "😲 63", "😓 32", "🙂 27", "😎 89", "😋 99", "😁 98", "😀 79", "🤣 100", "😣 8", "🙄 3", "😕 6", "🤯 0"]
       percentage = random.choice(percentages)
       await r.delete(f"hate_wait:{m.from_user.id}:{m.chat.id}")
       return await m.reply(plugins_fun_736(names[0], names[1], percentage))
     else:
       return await m.reply(plugins_fun_738(k))

   if text == "نسبه الصداقه" or text == "نسبة الصداقه" or text == "نسبه صداقه" or text == "نسبة صداقه":
     percentages = ["😂 10", "🤤 20", "😢 30", "😔 35", "😒 75", "🤩 34", "😗 66", "🤐 82", "😪 23", "😫 19", "😛 55", "😜 80", "😲 63", "😓 32", "🙂 27", "😎 89", "😋 99", "😁 98", "😀 79", "🤣 100", "😣 8", "🙄 3", "😕 6", "🤯 0"]
     percentage = random.choice(percentages)
     if m.reply_to_message:
       target = m.reply_to_message.from_user.mention()
       return await m.reply(plugins_fun_745(m.from_user.mention(), target, percentage))
     else:
       await r.setex(f"friend_wait:{m.from_user.id}:{m.chat.id}", 120, "true")
       return await m.reply(plugins_fun_748(k))

   if text and await r.get(f"friend_wait:{m.from_user.id}:{m.chat.id}"):
     names = text.split()
     if len(names) >= 2:
       percentages = ["😂 10", "🤤 20", "😢 30", "😔 35", "😒 75", "🤩 34", "😗 66", "🤐 82", "😪 23", "😫 19", "😛 55", "😜 80", "😲 63", "😓 32", "🙂 27", "😎 89", "😋 99", "😁 98", "😀 79", "🤣 100", "😣 8", "🙄 3", "😕 6", "🤯 0"]
       percentage = random.choice(percentages)
       await r.delete(f"friend_wait:{m.from_user.id}:{m.chat.id}")
       return await m.reply(plugins_fun_756(names[0], names[1], percentage))
     else:
       return await m.reply(plugins_fun_758(k))

   if text == "نسبه الذكاء" or text == "نسبة الذكاء" or text == "نسبه ذكاء" or text == "نسبة ذكاء":
     percentages = ["😂 10", "🤤 20", "😢 30", "😔 35", "😒 75", "🤩 34", "😗 66", "🤐 82", "😪 23", "😫 19", "😛 55", "😜 80", "😲 63", "😓 32", "🙂 27", "😎 89", "😋 99", "😁 98", "😀 79", "🤣 100", "😣 8", "🙄 3", "😕 6", "🤯 0"]
     percentage = random.choice(percentages)
     if m.reply_to_message:
       target = m.reply_to_message.from_user.mention()
       return await m.reply(plugins_fun_765(target, percentage))
     else:
       return await m.reply(plugins_fun_767(percentage))

   if text == "نسبه الغباء" or text == "نسبة الغباء" or text == "نسبه غباء" or text == "نسبة غباء":
     percentages = ["😂 10", "🤤 20", "😢 30", "😔 35", "😒 75", "🤩 34", "😗 66", "🤐 82", "😪 23", "😫 19", "😛 55", "😜 80", "😲 63", "😓 32", "🙂 27", "😎 89", "😋 99", "😁 98", "😀 79", "🤣 100", "😣 8", "🙄 3", "😕 6", "🤯 0"]
     percentage = random.choice(percentages)
     if m.reply_to_message:
       target = m.reply_to_message.from_user.mention()
       return await m.reply(plugins_fun_774(target, percentage))
     else:
       return await m.reply(plugins_fun_776(percentage))

   if text == "نسبه الرجوله" or text == "نسبة الرجوله" or text == "نسبه رجوله" or text == "نسبة رجولة":
     percentages = ["😂 10", "🤤 20", "😢 30", "😔 35", "😒 75", "🤩 34", "😗 66", "🤐 82", "😪 23", "😫 19", "😛 55", "😜 80", "😲 63", "😓 32", "🙂 27", "😎 89", "😋 99", "😁 98", "😀 79", "🤣 100", "😣 8", "🙄 3", "😕 6", "🤯 0"]
     percentage = random.choice(percentages)
     if m.reply_to_message:
       target = m.reply_to_message.from_user.mention()
       return await m.reply(plugins_fun_783(target, percentage))
     else:
       return await m.reply(plugins_fun_785(percentage))

   if text == "شخصيتي" or text == "نوع شخصيتي":
     personalities = ["شكاك", "متعاونة", "رومنسية", "اجتماعية", "كلاسيكية", "متردده", "ايجابية", "نرجسية", "قيادية", "محفزة", "مسالمة", "قوية", "ضعيفة", "غامضة", "عصبي"]
     personality = random.choice(personalities)
     return await m.reply(plugins_fun_790(personality))


   if text == "شبيهي":
     random_num = random.randint(2, 140)
     photo_url = f"https://t.me/VVVVBV1V/{random_num}"
     try:
       return await m.reply_photo(photo=photo_url, caption=f"{k} الصراحه اتفق هذا شبيهك 🤔🌚")
     except:
       return await m.reply(plugins_fun_799(k))

   if text == "شبيهتي":
     random_num = random.randint(2, 140)
     photo_url = f"https://t.me/VVVYVV4/{random_num}"
     try:
       return await m.reply_photo(photo=photo_url, caption=f"{k} الصراحه اتفق هذه شبيهتك 🤔🌚")
     except:
       return await m.reply(plugins_fun_807(k))


   if text == "ريمكس" or text == "ريماكس":
     random_num = random.randint(2, 400)
     voice_url = f"https://t.me/RemixWaTaN/{random_num}"
     buttons = InlineKeyboardMarkup([[InlineKeyboardButton(" ريمكس اخر ", callback_data="next_remix")]])
     caption = "⇜ تم اختيار مقطع ريمكس"
     try:
       return await m.reply_voice(voice=voice_url, caption=caption, reply_markup=buttons)
     except:
       return await m.reply(plugins_fun_818(k))

   if text == 'رفع لقلبي' and m.reply_to_message:
     return await m.reply(plugins_fun_958(k))
   
   if text == 'تنزيل من قلبي' and m.reply_to_message:
     return await m.reply(REPLIES['plugins_fun_824'])


@Client.on_callback_query(filters.regex(r"^(next_song|next_remix|next_fun|fun_)"), group=0)
async def fun_callback_handler(client, callback_query):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    data = callback_query.data
    k = await r.get(f'{Dev_FINAL}:botkey') or '•'
    
    if data == "next_song":
        random_num = random.randint(2, 140)
        voice_url = f"https://t.me/fkfnfnfn/{random_num}"
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton(" اغنية اخرى ", callback_data="next_song")]])
        await callback_query.message.reply_voice(voice=voice_url, caption=f"{k} 🎙", reply_markup=buttons)
        await callback_query.message.delete()
        await callback_query.answer()
        
    elif data == "next_remix":
        random_num = random.randint(2, 400)
        voice_url = f"https://t.me/RemixWaTaN/{random_num}"
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton(" ريمكس اخر ", callback_data="next_remix")]])
        caption = "⇜ تم اختيار مقطع ريمكس"
        await callback_query.message.reply_voice(voice=voice_url, caption=caption, reply_markup=buttons)
        await callback_query.message.delete()
        await callback_query.answer()
