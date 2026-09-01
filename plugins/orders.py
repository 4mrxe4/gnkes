from helpers.context import get_global_r, get_global_dev, get_global_k
r = get_global_r()
Dev_FINAL = get_global_dev()
k = get_global_k()
import re
from threading import Thread
from compat import Client, filters
from compat import InlineKeyboardMarkup, InlineKeyboardButton
import random, re, time, asyncio
from threading import Thread
from compat import *
from compat import *
from compat import *
from helpers.ranks import *
from helpers.replies_store import (
    REPLIES,
    plugins_orders_125,
    plugins_orders_129,
    plugins_orders_132,
    plugins_orders_147,
    plugins_orders_150,
    plugins_orders_157,
    plugins_orders_160,
    plugins_orders_191,
    plugins_orders_195,
    plugins_orders_199,
    plugins_orders_202,
    plugins_orders_218,
    plugins_orders_221,
    plugins_orders_227,
    plugins_orders_236,
    plugins_orders_265,
    plugins_orders_269,
    plugins_orders_272,
    plugins_orders_286,
    plugins_orders_289,
    plugins_orders_294,
    plugins_orders_304,
    plugins_orders_307,
    plugins_orders_330,
    plugins_orders_333,
    plugins_orders_337,
    plugins_orders_341,
    plugins_orders_345,
    plugins_orders_361,
    plugins_orders_385,
    plugins_orders_388,
    plugins_orders_396,
    plugins_orders_399,
    plugins_orders_46,
    plugins_orders_50,
    plugins_orders_54,
    plugins_orders_57,
    plugins_orders_73,
    plugins_orders_76,
    plugins_orders_82,
    plugins_orders_91,
)

@Client.on_message(filters.text & filters.group & ~filters.bot & ~filters.me, group=999)
async def customCummandHandler(c,m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    k = await r.get(f'{Dev_FINAL}:botkey')
    await addcommand(c,m,k)
   
   
async def addcommand(c,m,k):
   r = get_global_r()
   Dev_FINAL = get_global_dev()
   k = get_global_k()
   if not await check_global_restrictions(c, m, k):
       return
   if not await r.get(f'{m.chat.id}:enable:{Dev_FINAL}'):  return
   if await r.get(f'{m.from_user.id}:mute:{m.chat.id}{Dev_FINAL}'):  return 
   if await r.get(f'{m.from_user.id}:mute:{Dev_FINAL}'):  return  
   if await r.get(f'{m.chat.id}:mute:{Dev_FINAL}') and not await admin_pls(m.from_user.id,m.chat.id):  return
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

   if await r.get(f'{m.chat.id}:addCustom:{m.from_user.id}{Dev_FINAL}') and text == 'الغاء':
     await r.delete(f'{m.chat.id}:addCustom:{m.from_user.id}{Dev_FINAL}')
     return await m.reply(quote=True,text=plugins_orders_46(k))
   
   if await r.get(f'{m.chat.id}:addCustom2:{m.from_user.id}{Dev_FINAL}') and text == 'الغاء':
     await r.delete(f'{m.chat.id}:addCustom2:{m.from_user.id}{Dev_FINAL}')
     return await m.reply(quote=True,text=plugins_orders_50(k))

   if text == 'الاوامر المضافه' or text == 'الاوامر المضافة':
      if not await owner_pls(m.from_user.id, m.chat.id):
          return await m.reply(quote=True,text=plugins_orders_54(k))
      else:
          if not await r.smembers(f'{m.chat.id}:listCustom:{m.chat.id}{Dev_FINAL}'):
            return await m.reply(quote=True,text=plugins_orders_57(k))
          else:
              text_msg = 'الاوامر المضافة:\n'
              count = 0
              for cmnd in await r.smembers(f'{m.chat.id}:listCustom:{m.chat.id}{Dev_FINAL}'):
                 count += 1
                 command = cmnd
                 cc = await r.get(f'{m.chat.id}:Custom:{m.chat.id}{Dev_FINAL}&text={command}')
                 old_c = cc
                 text_msg += f'{count}) {command} ~ ( {old_c} )\n'
              text_msg += '\n༄'
              return await m.reply(quote=True,text=text_msg)
   
   if text == 'اضف امر' or text == 'تغيير امر':
     if not await r.get(f'{m.chat.id}:addCustom:{m.from_user.id}{Dev_FINAL}'):
       if not await owner_pls(m.from_user.id, m.chat.id):
          return await m.reply(quote=True,text=plugins_orders_73(k))
       else:
          await r.set(f'{m.chat.id}:addCustom:{m.from_user.id}{Dev_FINAL}',1)
          await m.reply(quote=True,text=plugins_orders_76(k))
          return

   if await r.get(f'{m.chat.id}:addCustom:{m.from_user.id}{Dev_FINAL}') and await admin_pls(m.from_user.id, m.chat.id) and len(m.text) < 50:
      await r.delete(f'{m.chat.id}:addCustom:{m.from_user.id}{Dev_FINAL}')
      await r.set(f'{m.chat.id}:addCustom2:{m.from_user.id}{Dev_FINAL}', m.text)
      await m.reply(quote=True,text=plugins_orders_82(k, m.text, k))
      return
   
   if await r.get(f'{m.chat.id}:addCustom2:{m.from_user.id}{Dev_FINAL}') and await admin_pls(m.from_user.id, m.chat.id) and len(m.text) < 50:
      command_o = await r.get(f'{m.chat.id}:addCustom2:{m.from_user.id}{Dev_FINAL}')
      command_n = m.text
      await r.delete(f'{m.chat.id}:addCustom2:{m.from_user.id}{Dev_FINAL}')
      await r.set(f'{m.chat.id}:Custom:{m.chat.id}{Dev_FINAL}&text={command_n}', command_o)
      await r.sadd(f'{m.chat.id}:listCustom:{m.chat.id}{Dev_FINAL}', command_n)
      await m.reply(quote=True,text=plugins_orders_91(k, command_o, k, command_n))
      return 


@Client.on_message(filters.text & filters.group & ~filters.bot & ~filters.me, group=1000)
async def delCustomCommandHandler(c,m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    k = await r.get(f'{Dev_FINAL}:botkey')
    await delcommand(c,m,k)
   
   
async def delcommand(c,m,k):
   r = get_global_r()
   Dev_FINAL = get_global_dev()
   k = get_global_k()
   if not await check_global_restrictions(c, m, k):
       return
   if not await r.get(f'{m.chat.id}:enable:{Dev_FINAL}'):  return
   if await r.get(f'{m.from_user.id}:mute:{m.chat.id}{Dev_FINAL}'):  return 
   if await r.get(f'{m.from_user.id}:mute:{Dev_FINAL}'):  return 
   if await r.get(f'{m.chat.id}:mute:{Dev_FINAL}') and not await admin_pls(m.from_user.id,m.chat.id):  return
   if await r.get(f'{m.chat.id}addCustomG:{m.from_user.id}{Dev_FINAL}'):  return
   text = m.text
   if await r.get(f'{m.chat.id}:Custom:{m.chat.id}{Dev_FINAL}&text={m.text}'):
       text = await r.get(f'{m.chat.id}:Custom:{m.chat.id}{Dev_FINAL}&text={m.text}')
   
   if await r.get(f'Custom:{Dev_FINAL}&text={m.text}'):
       text = await r.get(f'Custom:{Dev_FINAL}&text={m.text}')
   
   if await check_and_guard_locked_command(c, m, k, text):
       return

   if await r.get(f'{m.chat.id}:delCustom:{m.from_user.id}{Dev_FINAL}') and text == 'الغاء':
     await r.delete(f'{m.chat.id}:delCustom:{m.from_user.id}{Dev_FINAL}')
     return await m.reply(quote=True,text=plugins_orders_125(k))

   if text == 'مسح الاوامر' or text == 'مسح الاوامر المضافة':
     if not await mod_pls(m.from_user.id, m.chat.id):
       return await m.reply(quote=True,text=plugins_orders_129(k)) 
     else:
       if not await r.smembers(f'{m.chat.id}:listCustom:{m.chat.id}{Dev_FINAL}'):
         return await m.reply(quote=True,text=plugins_orders_132(k))
       else:
         count = 0
         for cmnd in await r.smembers(f'{m.chat.id}:listCustom:{m.chat.id}{Dev_FINAL}'):
           command = cmnd
           await r.delete(f'{m.chat.id}:Custom:{m.chat.id}{Dev_FINAL}&text={command}')
           await r.srem(f'{m.chat.id}:listCustom:{m.chat.id}{Dev_FINAL}', command)
           count += 1
         text_msg = f'من「 {m.from_user.mention()} 」\n{k} ابشر مسحت {count} أمر\n'
         return await m.reply(quote=True,text=text_msg)
       
   
   if text == 'مسح امر':
     if not await r.get(f'{m.chat.id}:delCustom:{m.from_user.id}{Dev_FINAL}'):
       if not await mod_pls(m.from_user.id, m.chat.id):
          return await m.reply(quote=True,text=plugins_orders_147(k))
       else:
          await r.set(f'{m.chat.id}:delCustom:{m.from_user.id}{Dev_FINAL}',1)
          await m.reply(quote=True,text=plugins_orders_150(k))
          return
      

   if await r.get(f'{m.chat.id}:delCustom:{m.from_user.id}{Dev_FINAL}') and await admin_pls(m.from_user.id, m.chat.id) and len(m.text) < 50:
      await r.delete(f'{m.chat.id}:delCustom:{m.from_user.id}{Dev_FINAL}')
      if not await r.get(f'{m.chat.id}:Custom:{m.chat.id}{Dev_FINAL}&text={m.text}'):
         return await m.reply(quote=True,text=plugins_orders_157(k))
      await r.srem(f'{m.chat.id}:listCustom:{m.chat.id}{Dev_FINAL}', m.text)
      await r.delete(f'{m.chat.id}:Custom:{m.chat.id}{Dev_FINAL}&text={m.text}')
      await m.reply(quote=True,text=plugins_orders_160(k, m.from_user.mention(), k))
      return
   
   
      
      



@Client.on_message(filters.text & filters.group & ~filters.bot & ~filters.me, group=1001)
async def customCummandGlobalHandler(c,m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    k = await r.get(f'{Dev_FINAL}:botkey')
    await addcommandg(c,m,k)
   
   
async def addcommandg(c,m,k):
   r = get_global_r()
   Dev_FINAL = get_global_dev()
   k = get_global_k()
   if not await check_global_restrictions(c, m, k):
       return
   if await r.get(f'{m.from_user.id}:mute:{m.chat.id}{Dev_FINAL}'):  return 
   if await r.get(f'{m.from_user.id}:mute:{Dev_FINAL}'):  return 
   if await r.get(f'{m.chat.id}:mute:{Dev_FINAL}') and not await admin_pls(m.from_user.id,m.chat.id):  return
   text = m.text
   if await r.get(f'Custom:{Dev_FINAL}&text={m.text}'):
       text = await r.get(f'Custom:{Dev_FINAL}&text={m.text}')
   
   if await r.get(f'{m.chat.id}addCustomG:{m.from_user.id}{Dev_FINAL}') and text == 'الغاء':
     await r.delete(f'{m.chat.id}addCustomG:{m.from_user.id}{Dev_FINAL}')
     return await m.reply(quote=True,text=plugins_orders_191(k))
   
   if await r.get(f'{m.chat.id}:addCustom2G:{m.from_user.id}{Dev_FINAL}') and text == 'الغاء':
     await r.delete(f'{m.chat.id}:addCustom2G:{m.from_user.id}{Dev_FINAL}')
     return await m.reply(quote=True,text=plugins_orders_195(k))

   if text == 'الاوامر العامه' or text == 'الاوامر المضافه العامه' and not m.chat.type == ChatType.PRIVATE:
      if not await dev_pls(m.from_user.id, m.chat.id):
          return await m.reply(quote=True,text=plugins_orders_199(k))
      else:
          if not await r.smembers(f'listCustom:{Dev_FINAL}'):
            return await m.reply(quote=True,text=plugins_orders_202(k))
          else:
              text_msg = 'الاوامر العامه:\n'
              count = 0
              for cmnd in await r.smembers(f'listCustom:{Dev_FINAL}'):
                 count += 1
                 command = cmnd
                 cc = await r.get(f'Custom:{Dev_FINAL}&text={command}')
                 old_c = cc
                 text_msg += f'{count}) {command} ~ ( {old_c} )\n'
              text_msg += '\n'
              return await m.reply(quote=True,text=text_msg)
   
   if text == 'اضف امر عام' or text == 'تغيير امر عام':
     if not await r.get(f'{m.chat.id}addCustomG:{m.from_user.id}{Dev_FINAL}'):
       if not await dev_pls(m.from_user.id, m.chat.id):
          return await m.reply(quote=True,text=plugins_orders_218(k))
       else:
          await r.set(f'{m.chat.id}addCustomG:{m.from_user.id}{Dev_FINAL}',1)
          await m.reply(quote=True,text=plugins_orders_221(k))
          return

   if await r.get(f'{m.chat.id}addCustomG:{m.from_user.id}{Dev_FINAL}') and await dev_pls(m.from_user.id, m.chat.id) and len(m.text) < 50:
      await r.delete(f'{m.chat.id}addCustomG:{m.from_user.id}{Dev_FINAL}')
      await r.set(f'{m.chat.id}:addCustom2G:{m.from_user.id}{Dev_FINAL}', m.text)
      await m.reply(quote=True,text=plugins_orders_227(k, m.text, k))
      return
   
   if await r.get(f'{m.chat.id}:addCustom2G:{m.from_user.id}{Dev_FINAL}') and await dev_pls(m.from_user.id, m.chat.id) and len(m.text) < 50:
      command_o = await r.get(f'{m.chat.id}:addCustom2G:{m.from_user.id}{Dev_FINAL}')
      command_n = m.text
      await r.delete(f'{m.chat.id}:addCustom2G:{m.from_user.id}{Dev_FINAL}')
      await r.set(f'Custom:{Dev_FINAL}&text={command_n}', command_o)
      await r.sadd(f'listCustom:{Dev_FINAL}', command_n)
      await m.reply(quote=True,text=plugins_orders_236(k, command_o, k, command_n))
      return 





@Client.on_message(filters.text & filters.group & ~filters.bot & ~filters.me, group=1002)
async def delCustomCommandGHandler(c, m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    k = await r.get(f'{Dev_FINAL}:botkey')
    await delcommandg(c, m, k)


async def delcommandg(c, m, k):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if not await check_global_restrictions(c, m, k):
        return
    if await r.get(f'{m.from_user.id}:mute:{m.chat.id}{Dev_FINAL}'): return
    if await r.get(f'{m.chat.id}:mute:{Dev_FINAL}') and not await admin_pls(m.from_user.id, m.chat.id): return
    if await r.get(f'{m.from_user.id}:mute:{Dev_FINAL}'): return
    text = m.text
    if await r.get(f'Custom:{Dev_FINAL}&text={m.text}'):
        text = await r.get(f'Custom:{Dev_FINAL}&text={m.text}')

    if await r.get(f'{m.chat.id}:delCustomG:{m.from_user.id}{Dev_FINAL}') and text == 'الغاء':
        await r.delete(f'{m.chat.id}:delCustomG:{m.from_user.id}{Dev_FINAL}')
        return await m.reply(quote=True, text=plugins_orders_265(k))

    if text == 'مسح الاوامر العامه':
        if not await dev_pls(m.from_user.id, m.chat.id):
            return await m.reply(quote=True, text=plugins_orders_269(k))
        else:
            if not await r.smembers(f'listCustom:{Dev_FINAL}'):
                return await m.reply(quote=True, text=plugins_orders_272(k))
            else:
                count = 0
                for cmnd in await r.smembers(f'listCustom:{Dev_FINAL}'):
                    command = cmnd
                    await r.delete(f'Custom:{Dev_FINAL}&text={command}')
                    await r.srem(f'listCustom:{Dev_FINAL}', command)
                    count += 1
                text_msg = f'من「 {m.from_user.mention()} 」\n{k} ابشر مسحت {count} أمر عام\n'
                return await m.reply(quote=True, text=text_msg)

    if text == 'مسح امر عام':
        if not await r.get(f'{m.chat.id}:delCustomG:{m.from_user.id}{Dev_FINAL}'):
            if not await dev_pls(m.from_user.id, m.chat.id):
                return await m.reply(quote=True, text=plugins_orders_286(k))
            else:
                await r.set(f'{m.chat.id}:delCustomG:{m.from_user.id}{Dev_FINAL}', 1)
                await m.reply(quote=True, text=plugins_orders_289(k))
                return

    if re.match("^فتح امر ", text):
        if not await gowner_pls(m.from_user.id, m.chat.id):
            return await m.reply(quote=True, text=plugins_orders_294(k))
        else:
            txt = text.split(None, 2)[2]
            if not await r.hget(Dev_FINAL + f"locks-{m.chat.id}", txt):
                return await m.reply(REPLIES['plugins_orders_298'])
            await r.hdel(Dev_FINAL + f"locks-{m.chat.id}", txt)
            return await m.reply(REPLIES['plugins_orders_300'])

    if text == "الاوامر المقفوله":
        if not await gowner_pls(m.from_user.id, m.chat.id):
            return await m.reply(quote=True, text=plugins_orders_304(k))
        else:
            if not await r.hgetall(Dev_FINAL + f"locks-{m.chat.id}"):
                return await m.reply(plugins_orders_307(k))
            else:
                commands = await r.hgetall(Dev_FINAL + f"locks-{m.chat.id}")
                txt = "الاوامر المقفوله:\n\n"
                count = 1
                for command, rank_value in commands.items():
                    cc = int(rank_value)
                    if cc == 0:
                        rank = "مالك اساسي"
                    elif cc == 1:
                        rank = "مالك"
                    elif cc == 2:
                        rank = "مدير"
                    elif cc == 3:
                        rank = "ادمن"
                    elif cc == 4:
                        rank = "مميز"
                    txt += f"{count} ) {command} - ( {rank} )\n"
                    count += 1
                return await m.reply(txt, disable_web_page_preview=True)

    if text == "مسح الاوامر المقفوله":
        if not await gowner_pls(m.from_user.id, m.chat.id):
            return await m.reply(quote=True, text=plugins_orders_330(k))
        else:
            if not await r.hgetall(Dev_FINAL + f"locks-{m.chat.id}"):
                return await m.reply(plugins_orders_333(k))
            else:
                count = len(list((await r.hgetall(Dev_FINAL + f"locks-{m.chat.id}")).keys()))
                await r.delete(Dev_FINAL + f"locks-{m.chat.id}")
                return await m.reply(plugins_orders_337(k, count))

    if re.match("^قفل امر ", text):
        if not await gowner_pls(m.from_user.id, m.chat.id):
            return await m.reply(quote=True, text=plugins_orders_341(k))
        else:
            command_to_lock = text.split(None, 2)[2]
            await r.set(f'{m.from_user.id}:temp_lock_command:{m.chat.id}', command_to_lock)
            return await m.reply(
                plugins_orders_345(k, command_to_lock, k)
            )

    if await r.get(f'{m.from_user.id}:temp_lock_command:{m.chat.id}') and text == 'الغاء':
        await r.delete(f'{m.from_user.id}:temp_lock_command:{m.chat.id}')
        return await m.reply(quote=True, text=plugins_orders_361(k))

    if await r.get(f'{m.from_user.id}:temp_lock_command:{m.chat.id}'):
        command_to_lock = await r.get(f'{m.from_user.id}:temp_lock_command:{m.chat.id}')
        rank_text = m.text.strip()
        rank_value = -1
        rank_name = ""

        if rank_text == "مالك اساسي":
            rank_value = 0
            rank_name = "مالك اساسي"
        elif rank_text == "مالك":
            rank_value = 1
            rank_name = "مالك"
        elif rank_text == "مدير":
            rank_value = 2
            rank_name = "مدير"
        elif rank_text == "ادمن":
            rank_value = 3
            rank_name = "ادمن"
        elif rank_text == "مميز":
            rank_value = 4
            rank_name = "مميز"
        else:
            return await m.reply(plugins_orders_385(k, k))

        await r.hset(Dev_FINAL + f"locks-{m.chat.id}", command_to_lock, rank_value)
        await m.reply(plugins_orders_388(k, command_to_lock, k, rank_name))
        await r.delete(f'{m.from_user.id}:temp_lock_command:{m.chat.id}')
        return

    if await r.get(f'{m.chat.id}:delCustomG:{m.from_user.id}{Dev_FINAL}') and await dev_pls(m.from_user.id, m.chat.id) and len(
            m.text) < 50:
        await r.delete(f'{m.chat.id}:delCustomG:{m.from_user.id}{Dev_FINAL}')
        if not await r.get(f'Custom:{Dev_FINAL}&text={m.text}'):
            return await m.reply(quote=True, text=plugins_orders_396(k))
        await r.srem(f'listCustom:{Dev_FINAL}', m.text)
        await r.delete(f'Custom:{Dev_FINAL}&text={m.text}')
        await m.reply(quote=True, text=plugins_orders_399(k, m.from_user.mention(), k))
        return
