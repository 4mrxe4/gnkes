import html
from helpers.context import get_global_r, get_global_dev, get_global_k
r = get_global_r()
Dev_FINAL = get_global_dev()
k = get_global_k()
import random, re, time, asyncio
from threading import Thread
from compat import *
from compat import *
from compat import *
from compat import *
from helpers.ranks import *
from helpers.replies_store import (
    plugins_globalban_137,
    plugins_globalban_140,
    plugins_globalban_142,
    plugins_globalban_146,
    plugins_globalban_152,
    plugins_globalban_163,
    plugins_globalban_166,
    plugins_globalban_168,
    plugins_globalban_174,
    plugins_globalban_180,
    plugins_globalban_192,
    plugins_globalban_195,
    plugins_globalban_199,
    plugins_globalban_205,
    plugins_globalban_217,
    plugins_globalban_220,
    plugins_globalban_224,
    plugins_globalban_279,
    plugins_globalban_284,
    plugins_globalban_286,
    plugins_globalban_290,
    plugins_globalban_294,
    plugins_globalban_299,
    plugins_globalban_301,
    plugins_globalban_305,
    plugins_globalban_309,
    plugins_globalban_314,
    plugins_globalban_316,
    plugins_globalban_322,
    plugins_globalban_326,
    plugins_globalban_331,
    plugins_globalban_333,
    plugins_globalban_337,
    plugins_globalban_341,
    plugins_globalban_346,
    plugins_globalban_348,
    plugins_globalban_352,
    plugins_globalban_356,
    plugins_globalban_361,
    plugins_globalban_363,
    plugins_globalban_367,
    plugins_globalban_49,
    plugins_globalban_60,
    plugins_globalban_63,
    plugins_globalban_65,
    plugins_globalban_69,
    plugins_globalban_77,
    plugins_globalban_89,
    plugins_globalban_92,
    plugins_globalban_96,
)



@Client.on_message(filters.text & filters.group, group=14)
async def mutesHandler(c,m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    k = await r.get(f'{Dev_FINAL}:botkey')
    await mute_func(c,m,k)
    
    
async def mute_func(c,m,k):
   r = get_global_r()
   Dev_FINAL = get_global_dev()
   k = get_global_k()
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


   
   if re.match("^كتم عام (.*?)$", text) and len(text.split()) ==  3:
      if not '@' in text and not re.findall('[0-9]+', text):
          return
      if not await dev_pls(m.from_user.id,m.chat.id):
           return await m.reply(plugins_globalban_49(k))      
      user = text.split()[2]
      id = await resolve_user_id_from_arg(user)
      if not id:
         return await m.reply(plugins_globalban_60(k))
      try:
         get = await c.get_users(id)
         mention = f'<a href="tg://user?id={get.id}">{html.escape(str(get.first_name))}</a>'
      except Exception:
         mention = f'<a href="tg://user?id={id}">{html.escape(str(id))}</a>'
      if await dev_pls(id, m.chat.id):
         rrank = await get_rank(id,m.chat.id)
         return await m.reply(plugins_globalban_63(k, rank))
      if await r.get(f'{id}:mute:{Dev_FINAL}'):
          return await m.reply(plugins_globalban_65(mention, k))
      else:
          await r.set(f'{id}:mute:{Dev_FINAL}', 1)
          await r.sadd(f'listMUTE:{Dev_FINAL}', id)
          return await m.reply(plugins_globalban_69(mention, k))


   
   if re.match("^الغاء الكتم العام (.*?)$", text) and len(text.split()) ==  4:
      if not '@' in text and not re.findall('[0-9]+', text):
          return
      if not await dev_pls(m.from_user.id,m.chat.id):
           return await m.reply(plugins_globalban_77(k))
      user = text.split()[3]
      id = await resolve_user_id_from_arg(user)
      if not id:
         return await m.reply(plugins_globalban_89(k))
      try:
         get = await c.get_users(id)
         mention = f'<a href="tg://user?id={get.id}">{html.escape(str(get.first_name))}</a>'
      except Exception:
         mention = f'<a href="tg://user?id={id}">{html.escape(str(id))}</a>'
      if not await r.get(f'{id}:mute:{Dev_FINAL}'):
          return await m.reply(plugins_globalban_92(mention, k))
      else:
          await r.delete(f'{id}:mute:{Dev_FINAL}')
          await r.srem(f'listMUTE:{Dev_FINAL}',id)
          return await m.reply(plugins_globalban_96(mention, k))

   if re.match("^حظر عام (.*?)$", text) and len(text.split()) ==  3:
      if not '@' in text and not re.findall('[0-9]+', text):
          return
      if not await dev_pls(m.from_user.id,m.chat.id):
           return await m.reply(plugins_globalban_126(k))      
      user = text.split()[2]
      id = await resolve_user_id_from_arg(user)
      if not id:
         return await m.reply(plugins_globalban_137(k))
      try:
         get = await c.get_users(id)
         mention = f'<a href="tg://user?id={get.id}">{html.escape(str(get.first_name))}</a>'
      except Exception:
         mention = f'<a href="tg://user?id={id}">{html.escape(str(id))}</a>'
      if await dev_pls(id, m.chat.id):
         rrank = await get_rank(id,m.chat.id)
         return await m.reply(plugins_globalban_140(k, rank))
      if await r.get(f'{id}:gban:{Dev_FINAL}'):
          return await m.reply(plugins_globalban_142(k, mention, k))
      else:
          await r.set(f'{id}:gban:{Dev_FINAL}', 1)
          await r.sadd(f'listGBAN:{Dev_FINAL}', id)
          return await m.reply(plugins_globalban_146(k, mention, k))
   
   if re.match("^حظر عام من الالعاب (.*?)$", text) and len(text.split()) ==  5:
      if not '@' in text and not re.findall('[0-9]+', text):
          return
      if not await dev_pls(m.from_user.id,m.chat.id):
           return await m.reply(plugins_globalban_152(k))
      user = text.split()[4]
      id = await resolve_user_id_from_arg(user)
      if not id:
         return await m.reply(plugins_globalban_163(k))
      try:
         get = await c.get_users(id)
         mention = f'<a href="tg://user?id={get.id}">{html.escape(str(get.first_name))}</a>'
      except Exception:
         mention = f'<a href="tg://user?id={id}">{html.escape(str(id))}</a>'
      if await dev_pls(id, m.chat.id):
         rrank = await get_rank(id,m.chat.id)
         return await m.reply(plugins_globalban_166(k, rank))
      if await r.get(f'{id}:gbangames:{Dev_FINAL}'):
          return await m.reply(plugins_globalban_168(k, mention, k))
      else:
          await r.set(f'{id}:gbangames:{Dev_FINAL}', 1)
          await r.sadd(f'listGBANGAMES:{Dev_FINAL}', id)
          await r.delete(f'{id}:Floos')
          await r.srem("BankList",id)
          return await m.reply(plugins_globalban_174(k, mention, k))
   
   if re.match("^الغاء الحظر العام من الالعاب (.*?)$", text) and len(text.split()) ==  6:
      if not '@' in text and not re.findall('[0-9]+', text):
          return
      if not await dev_pls(m.from_user.id,m.chat.id):
           return await m.reply(plugins_globalban_180(k))
      user = text.split()[5]
      id = await resolve_user_id_from_arg(user)
      if not id:
         return await m.reply(plugins_globalban_192(k))
      try:
         get = await c.get_users(id)
         mention = f'<a href="tg://user?id={get.id}">{html.escape(str(get.first_name))}</a>'
      except Exception:
         mention = f'<a href="tg://user?id={id}">{html.escape(str(id))}</a>'
      if not await r.get(f'{id}:gbangames:{Dev_FINAL}'):
          return await m.reply(plugins_globalban_195(mention, k))
      else:
          await r.delete(f'{id}:gbangames:{Dev_FINAL}')
          await r.srem(f'listGBANGAMES:{Dev_FINAL}',id)
          return await m.reply(plugins_globalban_199(mention, k))

   if re.match("^الغاء الحظر العام (.*?)$", text) and len(text.split()) ==  4:
      if not '@' in text and not re.findall('[0-9]+', text):
          return
      if not await dev_pls(m.from_user.id,m.chat.id):
           return await m.reply(plugins_globalban_205(k))
      user = text.split()[3]
      id = await resolve_user_id_from_arg(user)
      if not id:
         return await m.reply(plugins_globalban_217(k))
      try:
         get = await c.get_users(id)
         mention = f'<a href="tg://user?id={get.id}">{html.escape(str(get.first_name))}</a>'
      except Exception:
         mention = f'<a href="tg://user?id={id}">{html.escape(str(id))}</a>'
      if not await r.get(f'{id}:gban:{Dev_FINAL}'):
          return await m.reply(plugins_globalban_220(mention, k))
      else:
          await r.delete(f'{id}:gban:{Dev_FINAL}')
          await r.srem(f'listGBAN:{Dev_FINAL}',id)
          return await m.reply(plugins_globalban_224(mention, k))

@Client.on_message(filters.group, group=15)
async def muteResponse(c,m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    await del_formutes(c,m)
    
async def del_formutes(c,m):
   r = get_global_r()
   Dev_FINAL = get_global_dev()
   k = get_global_k()
   if await r.get(f'{m.from_user.id}:gban:{Dev_FINAL}'):
     try:
        await m.chat.ban_member(m.from_user.id)
     except:
        await m.delete()
   if await r.get(f'{m.from_user.id}:mute:{m.chat.id}{Dev_FINAL}') or await r.get(f'{m.from_user.id}:mute:{Dev_FINAL}'):
     try:
       await m.delete()
     except FloodWait as x:
       await asyncio.sleep(x.value)
     except Exception:
       pass




@Client.on_message(filters.text & filters.group, group=16)
async def mutesHandlerG(c,m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    k = await r.get(f'{Dev_FINAL}:botkey')
    await mute_funcg(c,m,k)
    
    
async def mute_funcg(c,m,k):
   r = get_global_r()
   Dev_FINAL = get_global_dev()
   k = get_global_k()
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
       
   if text == 'كتم عام' and m.reply_to_message and m.reply_to_message.from_user:
        if not await dev_pls(m.from_user.id,m.chat.id):
          return await m.reply(plugins_globalban_279(k))
        id = m.reply_to_message.from_user.id
        mention = m.reply_to_message.from_user.mention()
        if await dev_pls(id, m.chat.id):
           rrank = await get_rank(id,m.chat.id)
           return await m.reply(plugins_globalban_284(k, rank))
        if await r.get(f'{id}:mute:{Dev_FINAL}'):
          return await m.reply(plugins_globalban_286(mention, k))
        else:
          await r.set(f'{id}:mute:{Dev_FINAL}', 1)
          await r.sadd(f'listMUTE:{Dev_FINAL}', id)
          return await m.reply(plugins_globalban_290(mention, k))
      
   if text == 'حظر عام' and m.reply_to_message and m.reply_to_message.from_user:
        if not await dev_pls(m.from_user.id,m.chat.id):
          return await m.reply(plugins_globalban_294(k))
        id = m.reply_to_message.from_user.id
        mention = m.reply_to_message.from_user.mention()
        if await dev_pls(id, m.chat.id):
           rank = await get_rank(id,m.chat.id)
           return await m.reply(plugins_globalban_299(k, rank))
        if await r.get(f'{id}:gban:{Dev_FINAL}'):
          return await m.reply(plugins_globalban_301(k, mention, k))
        else:
          await r.set(f'{id}:gban:{Dev_FINAL}', 1)
          await r.sadd(f'listGBAN:{Dev_FINAL}', id)
          return await m.reply(plugins_globalban_305(k, mention, k))
   
   if text == 'حظر عام من الالعاب' and m.reply_to_message and m.reply_to_message.from_user:
        if not await dev_pls(m.from_user.id,m.chat.id):
          return await m.reply(plugins_globalban_309(k))
        id = m.reply_to_message.from_user.id
        mention = m.reply_to_message.from_user.mention()
        if await dev_pls(id, m.chat.id):
           rrank = await get_rank(id,m.chat.id)
           return await m.reply(plugins_globalban_314(k, rank))
        if await r.get(f'{id}:gbangames:{Dev_FINAL}'):
          return await m.reply(plugins_globalban_316(k, mention, k))
        else:
          await r.set(f'{id}:gbangames:{Dev_FINAL}', 1)
          await r.sadd(f'listGBANGAMES:{Dev_FINAL}', id)
          await r.delete(f'{id}:Floos')
          await r.srem("BankList",id)
          return await m.reply(plugins_globalban_322(k, mention, k))

   if text == 'الغاء الكتم العام' and m.reply_to_message and m.reply_to_message.from_user:
        if not await dev_pls(m.from_user.id,m.chat.id):
          return await m.reply(plugins_globalban_326(k))
        id = m.reply_to_message.from_user.id
        mention = m.reply_to_message.from_user.mention()
        if await dev_pls(id, m.chat.id):
           rrank = await get_rank(id,m.chat.id)
           return await m.reply(plugins_globalban_331(k, rank))
        if not await r.get(f'{id}:mute:{Dev_FINAL}'):
          return await m.reply(plugins_globalban_333(mention, k))
        else:
          await r.delete(f'{id}:mute:{Dev_FINAL}')
          await r.srem(f'listMUTE:{Dev_FINAL}', id)
          return await m.reply(plugins_globalban_337(mention, k))
   
   if text == 'الغاء الحظر العام من الالعاب' and m.reply_to_message and m.reply_to_message.from_user:
        if not await dev_pls(m.from_user.id,m.chat.id):
          return await m.reply(plugins_globalban_341(k))
        id = m.reply_to_message.from_user.id
        mention = m.reply_to_message.from_user.mention()
        if await dev_pls(id, m.chat.id):
           rrank = await get_rank(id,m.chat.id)
           return await m.reply(plugins_globalban_346(k, rank))
        if not await r.get(f'{id}:gbangames:{Dev_FINAL}'):
          return await m.reply(plugins_globalban_348(mention, k))
        else:
          await r.delete(f'{id}:gbangames:{Dev_FINAL}')
          await r.srem(f'listGBANGAMES:{Dev_FINAL}', id)
          return await m.reply(plugins_globalban_352(mention, k))

   if text == 'الغاء الحظر العام' and m.reply_to_message and m.reply_to_message.from_user:
        if not await dev_pls(m.from_user.id,m.chat.id):
          return await m.reply(plugins_globalban_356(k))
        id = m.reply_to_message.from_user.id
        mention = m.reply_to_message.from_user.mention()
        if await dev_pls(id, m.chat.id):
           rrank = await get_rank(id,m.chat.id)
           return await m.reply(plugins_globalban_361(k, rank))
        if not await r.get(f'{id}:gban:{Dev_FINAL}'):
          return await m.reply(plugins_globalban_363(mention, k))
        else:
          await r.delete(f'{id}:gban:{Dev_FINAL}')
          await r.srem(f'listGBAN:{Dev_FINAL}', id)
          return await m.reply(plugins_globalban_367(mention, k))
