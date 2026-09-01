
import html
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
    plugins_setrank_100,
    plugins_setrank_1008,
    plugins_setrank_1010,
    plugins_setrank_1017,
    plugins_setrank_1028,
    plugins_setrank_1030,
    plugins_setrank_1037,
    plugins_setrank_1046,
    plugins_setrank_1048,
    plugins_setrank_1053,
    plugins_setrank_1065,
    plugins_setrank_1067,
    plugins_setrank_1084,
    plugins_setrank_1086,
    plugins_setrank_1092,
    plugins_setrank_110,
    plugins_setrank_1107,
    plugins_setrank_1109,
    plugins_setrank_1115,
    plugins_setrank_1129,
    plugins_setrank_1131,
    plugins_setrank_1137,
    plugins_setrank_114,
    plugins_setrank_1149,
    plugins_setrank_1151,
    plugins_setrank_1158,
    plugins_setrank_1169,
    plugins_setrank_1171,
    plugins_setrank_1179,
    plugins_setrank_118,
    plugins_setrank_1188,
    plugins_setrank_1190,
    plugins_setrank_1198,
    plugins_setrank_1206,
    plugins_setrank_1208,
    plugins_setrank_122,
    plugins_setrank_134,
    plugins_setrank_143,
    plugins_setrank_150,
    plugins_setrank_152,
    plugins_setrank_159,
    plugins_setrank_163,
    plugins_setrank_173,
    plugins_setrank_177,
    plugins_setrank_183,
    plugins_setrank_187,
    plugins_setrank_201,
    plugins_setrank_210,
    plugins_setrank_217,
    plugins_setrank_219,
    plugins_setrank_225,
    plugins_setrank_229,
    plugins_setrank_240,
    plugins_setrank_244,
    plugins_setrank_250,
    plugins_setrank_254,
    plugins_setrank_267,
    plugins_setrank_276,
    plugins_setrank_283,
    plugins_setrank_285,
    plugins_setrank_292,
    plugins_setrank_296,
    plugins_setrank_303,
    plugins_setrank_308,
    plugins_setrank_314,
    plugins_setrank_318,
    plugins_setrank_328,
    plugins_setrank_337,
    plugins_setrank_344,
    plugins_setrank_348,
    plugins_setrank_352,
    plugins_setrank_356,
    plugins_setrank_363,
    plugins_setrank_369,
    plugins_setrank_373,
    plugins_setrank_377,
    plugins_setrank_386,
    plugins_setrank_395,
    plugins_setrank_402,
    plugins_setrank_406,
    plugins_setrank_411,
    plugins_setrank_415,
    plugins_setrank_422,
    plugins_setrank_428,
    plugins_setrank_433,
    plugins_setrank_437,
    plugins_setrank_446,
    plugins_setrank_45,
    plugins_setrank_456,
    plugins_setrank_463,
    plugins_setrank_469,
    plugins_setrank_471,
    plugins_setrank_475,
    plugins_setrank_48,
    plugins_setrank_482,
    plugins_setrank_489,
    plugins_setrank_493,
    plugins_setrank_497,
    plugins_setrank_51,
    plugins_setrank_537,
    plugins_setrank_543,
    plugins_setrank_547,
    plugins_setrank_55,
    plugins_setrank_553,
    plugins_setrank_563,
    plugins_setrank_570,
    plugins_setrank_574,
    plugins_setrank_578,
    plugins_setrank_58,
    plugins_setrank_582,
    plugins_setrank_590,
    plugins_setrank_594,
    plugins_setrank_600,
    plugins_setrank_609,
    plugins_setrank_61,
    plugins_setrank_616,
    plugins_setrank_624,
    plugins_setrank_628,
    plugins_setrank_634,
    plugins_setrank_642,
    plugins_setrank_646,
    plugins_setrank_652,
    plugins_setrank_661,
    plugins_setrank_668,
    plugins_setrank_675,
    plugins_setrank_679,
    plugins_setrank_686,
    plugins_setrank_695,
    plugins_setrank_702,
    plugins_setrank_708,
    plugins_setrank_71,
    plugins_setrank_712,
    plugins_setrank_723,
    plugins_setrank_727,
    plugins_setrank_733,
    plugins_setrank_742,
    plugins_setrank_749,
    plugins_setrank_757,
    plugins_setrank_761,
    plugins_setrank_765,
    plugins_setrank_775,
    plugins_setrank_779,
    plugins_setrank_785,
    plugins_setrank_794,
    plugins_setrank_80,
    plugins_setrank_801,
    plugins_setrank_807,
    plugins_setrank_811,
    plugins_setrank_821,
    plugins_setrank_825,
    plugins_setrank_831,
    plugins_setrank_840,
    plugins_setrank_847,
    plugins_setrank_854,
    plugins_setrank_858,
    plugins_setrank_862,
    plugins_setrank_87,
    plugins_setrank_870,
    plugins_setrank_874,
    plugins_setrank_880,
    plugins_setrank_89,
    plugins_setrank_890,
    plugins_setrank_897,
    plugins_setrank_906,
    plugins_setrank_908,
    plugins_setrank_925,
    plugins_setrank_927,
    plugins_setrank_933,
    plugins_setrank_948,
    plugins_setrank_950,
    plugins_setrank_954,
    plugins_setrank_96,
    plugins_setrank_968,
    plugins_setrank_970,
    plugins_setrank_976,
    plugins_setrank_988,
    plugins_setrank_990,
    plugins_setrank_997,
)



@Client.on_message(filters.text & filters.group, group=7)
async def ranksCommandsHandler(c,m):
   r = get_global_r()
   Dev_FINAL = get_global_dev()
   k = get_global_k()
   k = await r.get(f'{Dev_FINAL}:botkey')
   await ranks_reply_promote(c,m,k)
   

async def ranks_reply_promote(c,m,k):
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


    if text == 'تعطيل الرفع':
      if not await owner_pls(m.from_user.id, m.chat.id):
        return await m.reply(plugins_setrank_45(k))
      else:
        if await r.get(f'{m.chat.id}:disableRanks:{Dev_FINAL}'):
          return await m.reply(plugins_setrank_48(k, m.from_user.mention(), k))
        else:
          await r.set(f'{m.chat.id}:disableRanks:{Dev_FINAL}', 1)
          return await m.reply(plugins_setrank_51(k, m.from_user.mention(), k))
    
    if text == 'تفعيل الرفع':
      if not await owner_pls(m.from_user.id, m.chat.id):
        return await m.reply(plugins_setrank_55(k))
      else:
        if not await r.get(f'{m.chat.id}:disableRanks:{Dev_FINAL}'):
          return await m.reply(plugins_setrank_58(m.from_user.mention(), k))
        else:
          await r.delete(f'{m.chat.id}:disableRanks:{Dev_FINAL}')
          return await m.reply(plugins_setrank_61(k, m.from_user.mention(), k))
    
    cid = m.chat.id
    
    if await r.get(f'{m.chat.id}:disableRanks:{Dev_FINAL}'):  return
    rank = await get_rank(m.from_user.id, m.chat.id)
    if text.startswith('رفع Dev '):
        if not '@' in text and not re.findall('[0-9]+', text):
          return
        if not await devp_pls(m.from_user.id,m.chat.id):
          return await m.reply(plugins_setrank_71(k))
        if len(text.split()) == 4:
           user = text.split()[3]
           resolved_id = await resolve_user_id_from_arg(user)
           if not resolved_id:
              return await m.reply(plugins_setrank_80(k) if user.startswith('@') else plugins_setrank_87(k))
           try:
              get = await c.get_users(resolved_id)
              mention = f'<a href="tg://user?id={get.id}">{html.escape(str(get.first_name))}</a>'
              id = get.id
           except Exception:
              mention = f'<a href="tg://user?id={resolved_id}">{html.escape(str(resolved_id))}</a>'
              id = resolved_id
        if id == m.from_user.id:
           return await m.reply(plugins_setrank_89(k))
        
        if id == int(Dev_FINAL):
           return await m.reply(REPLIES['plugins_setrank_92'])
        
           
        if await r.get(f'{id}:rankDEV2:{Dev_FINAL}'):
          return await m.reply(plugins_setrank_96(mention, k))
        else:
          await r.set(f'{id}:rankDEV2:{Dev_FINAL}', 1)
          await r.sadd(f'{Dev_FINAL}DEV2', id)
          return await m.reply(plugins_setrank_100(k, mention, k))
          if await r.get(f'{id}:mute:{Dev_FINAL}'):
            await r.delete(f'{id}:mute:{Dev_FINAL}')
            await r.srem(f'listMUTE:{Dev_FINAL}', id)
          if await r.get(f'{id}:mute:{m.chat.id}{Dev_FINAL}'):
            await r.delete(f'{id}:mute:{m.chat.id}{Dev_FINAL}')
            await r.srem(f'{m.chat.id}:listMUTE:{Dev_FINAL}', id)
    
    if text == 'رفع Dev' and m.reply_to_message and m.reply_to_message.from_user:
        if not await devp_pls(m.from_user.id,m.chat.id):
          return await m.reply(plugins_setrank_110(k))
        id = m.reply_to_message.from_user.id
        mention = m.reply_to_message.from_user.mention()
        if id == m.from_user.id:
           return await m.reply(plugins_setrank_114(k))        
        if id == int(Dev_FINAL):
           return await m.reply(REPLIES['plugins_setrank_92'])           
        if await r.get(f'{id}:rankDEV2:{Dev_FINAL}'):
          return await m.reply(plugins_setrank_118(mention, k))
        else:
          await r.set(f'{id}:rankDEV2:{Dev_FINAL}', 1)
          await r.sadd(f'{Dev_FINAL}DEV2', id)
          return await m.reply(plugins_setrank_122(k, mention, k))
          if await r.get(f'{id}:mute:{Dev_FINAL}'):
            await r.delete(f'{id}:mute:{Dev_FINAL}')
            await r.srem(f'listMUTE:{Dev_FINAL}', id)
          if await r.get(f'{id}:mute:{m.chat.id}{Dev_FINAL}'):
            await r.delete(f'{id}:mute:{m.chat.id}{Dev_FINAL}')
            await r.srem(f'{m.chat.id}:listMUTE:{Dev_FINAL}', id)
          
    if text.startswith('رفع MY '):
        if not '@' in text and not re.findall('[0-9]+', text):
          return False
        if not await dev2_pls(m.from_user.id,m.chat.id):
           return await m.reply(plugins_setrank_134(k))
        if len(text.split()) == 3:
           user = text.split()[2]
           resolved_id = await resolve_user_id_from_arg(user)
           if not resolved_id:
              return await m.reply(plugins_setrank_143(k) if user.startswith('@') else plugins_setrank_150(k))
           try:
              get = await c.get_users(resolved_id)
              mention = f'<a href="tg://user?id={get.id}">{html.escape(str(get.first_name))}</a>'
              id = get.id
           except Exception:
              mention = f'<a href="tg://user?id={resolved_id}">{html.escape(str(resolved_id))}</a>'
              id = resolved_id
        if id == m.from_user.id:
           return await m.reply(plugins_setrank_152(k))
        if id == int(Dev_FINAL):
           return await m.reply(REPLIES['plugins_setrank_92'])
        
        if rank == await get_rank(id, cid):
           return await m.reply(REPLIES['plugins_setrank_157'])
        if await r.get(f'{id}:rankDEV:{Dev_FINAL}'):
          return await m.reply(plugins_setrank_159(mention, k))
        else:
          await r.set(f'{id}:rankDEV:{Dev_FINAL}', 1)
          await r.sadd(f'{Dev_FINAL}DEV', id)
          await m.reply(plugins_setrank_163(k, mention, k))
          if await r.get(f'{id}:mute:{Dev_FINAL}'):
            await r.delete(f'{id}:mute:{Dev_FINAL}')
            await r.srem(f'listMUTE:{Dev_FINAL}', id)
          if await r.get(f'{id}:mute:{m.chat.id}{Dev_FINAL}'):
            await r.delete(f'{id}:mute:{m.chat.id}{Dev_FINAL}')
            await r.srem(f'{m.chat.id}:listMUTE:{Dev_FINAL}', id)
    
    if text == 'رفع MY' and m.reply_to_message and m.reply_to_message.from_user:
        if not await dev2_pls(m.from_user.id,m.chat.id):
           return await m.reply(plugins_setrank_173(k))
        id = m.reply_to_message.from_user.id
        mention = m.reply_to_message.from_user.mention()
        if id == m.from_user.id:
           return await m.reply(plugins_setrank_177(k))
        if id == int(Dev_FINAL):
           return await m.reply(REPLIES['plugins_setrank_92'])        
        if rank == await get_rank(id, cid):
           return await m.reply(REPLIES['plugins_setrank_157'])
        if await r.get(f'{id}:rankDEV:{Dev_FINAL}'):
          return await m.reply(plugins_setrank_183(mention, k))
        else:
          await r.set(f'{id}:rankDEV:{Dev_FINAL}', 1)
          await r.sadd(f'{Dev_FINAL}DEV', id)
          await m.reply(plugins_setrank_187(k, mention, k))
          if await r.get(f'{id}:mute:{Dev_FINAL}'):
            await r.delete(f'{id}:mute:{Dev_FINAL}')
            await r.srem(f'listMUTE:{Dev_FINAL}', id)
          if await r.get(f'{id}:mute:{m.chat.id}{Dev_FINAL}'):
            await r.delete(f'{id}:mute:{m.chat.id}{Dev_FINAL}')
            await r.srem(f'{m.chat.id}:listMUTE:{Dev_FINAL}', id)
    
    cid = m.chat.id
    
    if text.startswith('رفع مالك اساسي '):
        if not '@' in text and not re.findall('[0-9]+', text):
          return
        if not await gowner_pls(m.from_user.id,m.chat.id):
          return await m.reply(plugins_setrank_201(k))
        if len(text.split()) == 4:
           user = text.split()[3]
           resolved_id = await resolve_user_id_from_arg(user)
           if not resolved_id:
              return await m.reply(plugins_setrank_210(k) if user.startswith('@') else plugins_setrank_217(k))
           try:
              get = await c.get_users(resolved_id)
              mention = f'<a href="tg://user?id={get.id}">{html.escape(str(get.first_name))}</a>'
              id = get.id
           except Exception:
              mention = f'<a href="tg://user?id={resolved_id}">{html.escape(str(resolved_id))}</a>'
              id = resolved_id
        if id == m.from_user.id:
           return await m.reply(plugins_setrank_219(k))
        if id == int(Dev_FINAL):
           return await m.reply(REPLIES['plugins_setrank_92'])
        if rank == await get_rank(id, cid):
           return await m.reply(REPLIES['plugins_setrank_157'])           
        if await r.get(f'{cid}:rankGOWNER:{id}{Dev_FINAL}'):
          return await m.reply(plugins_setrank_225(mention, k))
        else:
          await r.set(f'{cid}:rankGOWNER:{id}{Dev_FINAL}', 1)
          await r.sadd(f'{cid}:listGOWNER:{Dev_FINAL}', id)
          await m.reply(plugins_setrank_229(k, mention, k))
          if await r.get(f'{id}:mute:{Dev_FINAL}'):
            await r.delete(f'{id}:mute:{Dev_FINAL}')
            await r.srem(f'listMUTE:{Dev_FINAL}', id)
          if await r.get(f'{id}:mute:{m.chat.id}{Dev_FINAL}'):
            await r.delete(f'{id}:mute:{m.chat.id}{Dev_FINAL}')
            await r.srem(f'{m.chat.id}:listMUTE:{Dev_FINAL}', id)
          return 
    
    if text == 'رفع مالك اساسي' and m.reply_to_message and m.reply_to_message.from_user:
        if not await gowner_pls(m.from_user.id,m.chat.id):
          return await m.reply(plugins_setrank_240(k))
        id = m.reply_to_message.from_user.id
        mention = m.reply_to_message.from_user.mention()       
        if id == m.from_user.id:
           return await m.reply(plugins_setrank_244(k))
        if id == int(Dev_FINAL):
           return await m.reply(REPLIES['plugins_setrank_92'])
        if rank == await get_rank(id, cid):
           return await m.reply(REPLIES['plugins_setrank_157'])           
        if await r.get(f'{cid}:rankGOWNER:{id}{Dev_FINAL}'):
          return await m.reply(plugins_setrank_250(mention, k))
        else:
          await r.set(f'{cid}:rankGOWNER:{id}{Dev_FINAL}', 1)
          await r.sadd(f'{cid}:listGOWNER:{Dev_FINAL}', id)
          await m.reply(plugins_setrank_254(k, mention, k))
          if await r.get(f'{id}:mute:{Dev_FINAL}'):
            await r.delete(f'{id}:mute:{Dev_FINAL}')
            await r.srem(f'listMUTE:{Dev_FINAL}', id)
          if await r.get(f'{id}:mute:{m.chat.id}{Dev_FINAL}'):
            await r.delete(f'{id}:mute:{m.chat.id}{Dev_FINAL}')
            await r.srem(f'{m.chat.id}:listMUTE:{Dev_FINAL}', id)
          return 
    
    if text.startswith('رفع مالك '):
        if not '@' in text and not re.findall('[0-9]+', text):
          return
        if not await gowner_pls(m.from_user.id,m.chat.id):
          return await m.reply(plugins_setrank_267(k))
        if len(text.split()) == 3:
           user = text.split()[2]
           resolved_id = await resolve_user_id_from_arg(user)
           if not resolved_id:
              return await m.reply(plugins_setrank_276(k) if user.startswith('@') else plugins_setrank_283(k))
           try:
              get = await c.get_users(resolved_id)
              mention = f'<a href="tg://user?id={get.id}">{html.escape(str(get.first_name))}</a>'
              id = get.id
           except Exception:
              mention = f'<a href="tg://user?id={resolved_id}">{html.escape(str(resolved_id))}</a>'
              id = resolved_id
        if id == m.from_user.id:
           return await m.reply(plugins_setrank_285(k))
        if id == int(Dev_FINAL):
           return await m.reply(REPLIES['plugins_setrank_92'])
        
        if rank == await get_rank(id, cid):
           return await m.reply(REPLIES['plugins_setrank_157'])
        if await r.get(f'{cid}:rankOWNER:{id}{Dev_FINAL}'):
          return await m.reply(plugins_setrank_292(mention, k))
        else:
          await r.set(f'{cid}:rankOWNER:{id}{Dev_FINAL}', 1)
          await r.sadd(f'{cid}:listOWNER:{Dev_FINAL}', id)
          await m.reply(plugins_setrank_296(k, mention, k))
          if await r.get(f'{id}:mute:{m.chat.id}{Dev_FINAL}'):
            await r.delete(f'{id}:mute:{m.chat.id}{Dev_FINAL}')
            await r.srem(f'{m.chat.id}:listMUTE:{Dev_FINAL}', id)
    
    if text == 'رفع مالك' and m.reply_to_message and m.reply_to_message.from_user:
        if not await gowner_pls(m.from_user.id,m.chat.id):
          return await m.reply(plugins_setrank_303(k))
        if m.reply_to_message and m.reply_to_message.from_user:
           id = m.reply_to_message.from_user.id
           mention = m.reply_to_message.from_user.mention()
        if id == m.from_user.id:
           return await m.reply(plugins_setrank_308(k))
        if id == int(Dev_FINAL):
           return await m.reply(REPLIES['plugins_setrank_92'])
        if rank == await get_rank(id, cid):
           return await m.reply(REPLIES['plugins_setrank_157'])
        if await r.get(f'{cid}:rankOWNER:{id}{Dev_FINAL}'):
          return await m.reply(plugins_setrank_314(mention, k))
        else:
          await r.set(f'{cid}:rankOWNER:{id}{Dev_FINAL}', 1)
          await r.sadd(f'{cid}:listOWNER:{Dev_FINAL}', id)
          await m.reply(plugins_setrank_318(k, mention, k))
          if await r.get(f'{id}:mute:{m.chat.id}{Dev_FINAL}'):
            await r.delete(f'{id}:mute:{m.chat.id}{Dev_FINAL}')
            await r.srem(f'{m.chat.id}:listMUTE:{Dev_FINAL}', id)
    
    
    if text.startswith('رفع مدير '):
        if not '@' in text and not re.findall('[0-9]+', text):
          return
        if not await owner_pls(m.from_user.id,m.chat.id):
           return await m.reply(plugins_setrank_328(k))
        if len(text.split()) == 3:
           user = text.split()[2]
           resolved_id = await resolve_user_id_from_arg(user)
           if not resolved_id:
              return await m.reply(plugins_setrank_337(k) if user.startswith('@') else plugins_setrank_344(k))
           try:
              get = await c.get_users(resolved_id)
              mention = f'<a href="tg://user?id={get.id}">{html.escape(str(get.first_name))}</a>'
              id = get.id
           except Exception:
              mention = f'<a href="tg://user?id={resolved_id}">{html.escape(str(resolved_id))}</a>'
              id = resolved_id
        if id == int(Dev_FINAL):
           return await m.reply(REPLIES['plugins_setrank_92'])
        if id == m.from_user.id:
           return await m.reply(plugins_setrank_348(k))
        if rank == await get_rank(id, cid):
           return await m.reply(REPLIES['plugins_setrank_157'])           
        if await r.get(f'{cid}:rankMOD:{id}{Dev_FINAL}'):
          return await m.reply(plugins_setrank_352(mention, k))
        else:
          await r.set(f'{cid}:rankMOD:{id}{Dev_FINAL}', 1)
          await r.sadd(f'{cid}:listMOD:{Dev_FINAL}', id)
          await m.reply(plugins_setrank_356(k, mention, k))
          if await r.get(f'{id}:mute:{m.chat.id}{Dev_FINAL}'):
            await r.delete(f'{id}:mute:{m.chat.id}{Dev_FINAL}')
            await r.srem(f'{m.chat.id}:listMUTE:{Dev_FINAL}', id)
    
    if text == 'رفع مدير' and m.reply_to_message and m.reply_to_message.from_user:
        if not await owner_pls(m.from_user.id,m.chat.id):
           return await m.reply(plugins_setrank_363(k))
        id = m.reply_to_message.from_user.id
        mention = m.reply_to_message.from_user.mention()
        if id == int(Dev_FINAL):
           return await m.reply(REPLIES['plugins_setrank_92'])
        if id == m.from_user.id:
           return await m.reply(plugins_setrank_369(k))
        if rank == await get_rank(id, cid):
           return await m.reply(REPLIES['plugins_setrank_157'])           
        if await r.get(f'{cid}:rankMOD:{id}{Dev_FINAL}'):
          return await m.reply(plugins_setrank_373(mention, k))
        else:
          await r.set(f'{cid}:rankMOD:{id}{Dev_FINAL}', 1)
          await r.sadd(f'{cid}:listMOD:{Dev_FINAL}', id)
          await m.reply(plugins_setrank_377(k, mention, k))
          if await r.get(f'{id}:mute:{m.chat.id}{Dev_FINAL}'):
            await r.delete(f'{id}:mute:{m.chat.id}{Dev_FINAL}')
            await r.srem(f'{m.chat.id}:listMUTE:{Dev_FINAL}', id)
    
    if text.startswith('رفع ادمن '):
        if not '@' in text and not re.findall('[0-9]+', text):
          return
        if not await mod_pls(m.from_user.id,m.chat.id):
           return await m.reply(plugins_setrank_386(k))
        if len(text.split()) == 3:
           user = text.split()[2]
           resolved_id = await resolve_user_id_from_arg(user)
           if not resolved_id:
              return await m.reply(plugins_setrank_395(k) if user.startswith('@') else plugins_setrank_402(k))
           try:
              get = await c.get_users(resolved_id)
              mention = f'<a href="tg://user?id={get.id}">{html.escape(str(get.first_name))}</a>'
              id = get.id
           except Exception:
              mention = f'<a href="tg://user?id={resolved_id}">{html.escape(str(resolved_id))}</a>'
              id = resolved_id
        if id == int(Dev_FINAL):
           return await m.reply(REPLIES['plugins_setrank_92'])
        if id == m.from_user.id:
           return await m.reply(plugins_setrank_406(k))
        if rank == await get_rank(id, cid):
           return await m.reply(REPLIES['plugins_setrank_157'])
           
        if await r.get(f'{cid}:rankADMIN:{id}{Dev_FINAL}'):
          return await m.reply(plugins_setrank_411(mention, k))
        else:
          await r.set(f'{cid}:rankADMIN:{id}{Dev_FINAL}', 1)
          await r.sadd(f'{cid}:listADMIN:{Dev_FINAL}', id)
          await m.reply(plugins_setrank_415(k, mention, k))
          if await r.get(f'{id}:mute:{m.chat.id}{Dev_FINAL}'):
            await r.delete(f'{id}:mute:{m.chat.id}{Dev_FINAL}')
            await r.srem(f'{m.chat.id}:listMUTE:{Dev_FINAL}', id)
    
    if text == 'رفع ادمن' and m.reply_to_message and m.reply_to_message.from_user:        
        if not await mod_pls(m.from_user.id,m.chat.id):
           return await m.reply(plugins_setrank_422(k))
        id = m.reply_to_message.from_user.id
        mention = m.reply_to_message.from_user.mention()
        if id == int(Dev_FINAL):
           return await m.reply(REPLIES['plugins_setrank_92'])
        if id == m.from_user.id:
           return await m.reply(plugins_setrank_428(k))
        if rank == await get_rank(id, cid):
           return await m.reply(REPLIES['plugins_setrank_157'])
           
        if await r.get(f'{cid}:rankADMIN:{id}{Dev_FINAL}'):
          return await m.reply(plugins_setrank_433(mention, k))
        else:
          await r.set(f'{cid}:rankADMIN:{id}{Dev_FINAL}', 1)
          await r.sadd(f'{cid}:listADMIN:{Dev_FINAL}', id)
          await m.reply(plugins_setrank_437(k, mention, k))
          if await r.get(f'{id}:mute:{m.chat.id}{Dev_FINAL}'):
            await r.delete(f'{id}:mute:{m.chat.id}{Dev_FINAL}')
            await r.srem(f'{m.chat.id}:listMUTE:{Dev_FINAL}', id)
    
    if text.startswith('رفع مميز '):
      if not '@' in text and not re.findall('[0-9]+', text):
          return
      if not await admin_pls(m.from_user.id,m.chat.id):
        return await m.reply(plugins_setrank_446(k))
      else:
        if len(text.split()) == 3:
           user = text.split()[2]
           resolved_id = await resolve_user_id_from_arg(user)
           if not resolved_id:
              return await m.reply(plugins_setrank_456(k) if user.startswith('@') else plugins_setrank_463(k))
           try:
              get = await c.get_users(resolved_id)
              mention = f'<a href="tg://user?id={get.id}">{html.escape(str(get.first_name))}</a>'
              id = get.id
           except Exception:
              mention = f'<a href="tg://user?id={resolved_id}">{html.escape(str(resolved_id))}</a>'
              id = resolved_id
        if id == int(Dev_FINAL):
           return await m.reply(REPLIES['plugins_setrank_92'])
        if rank == await get_rank(id, cid):
           return await m.reply(REPLIES['plugins_setrank_157'])
        if id == m.from_user.id:
           return await m.reply(plugins_setrank_469(k))
        if await r.get(f'{cid}:rankPRE:{id}{Dev_FINAL}'):
          return await m.reply(plugins_setrank_471(mention, k))
        else:
          await r.set(f'{cid}:rankPRE:{id}{Dev_FINAL}', 1)
          await r.sadd(f'{cid}:listPRE:{Dev_FINAL}', id)
          await m.reply(plugins_setrank_475(k, mention, k))
          if await r.get(f'{id}:mute:{m.chat.id}{Dev_FINAL}'):
            await r.delete(f'{id}:mute:{m.chat.id}{Dev_FINAL}')
            await r.srem(f'{m.chat.id}:listMUTE:{Dev_FINAL}', id)
    
    if text == 'رفع مميز' and m.reply_to_message and m.reply_to_message.from_user:
      if not await admin_pls(m.from_user.id,m.chat.id):
        return await m.reply(plugins_setrank_482(k))
      else:
        id = m.reply_to_message.from_user.id
        mention = m.reply_to_message.from_user.mention()
        if id == int(Dev_FINAL):
           return await m.reply(REPLIES['plugins_setrank_92'])
        if id == m.from_user.id:
           return await m.reply(plugins_setrank_489(k))
        if rank == await get_rank(id, cid):
           return await m.reply(REPLIES['plugins_setrank_157'])
        if await r.get(f'{cid}:rankPRE:{id}{Dev_FINAL}'):
          return await m.reply(plugins_setrank_493(mention, k))
        else:
          await r.set(f'{cid}:rankPRE:{id}{Dev_FINAL}', 1)
          await r.sadd(f'{cid}:listPRE:{Dev_FINAL}', id)
          await m.reply(plugins_setrank_497(k, mention, k))
          if await r.get(f'{id}:mute:{m.chat.id}{Dev_FINAL}'):
            await r.delete(f'{id}:mute:{m.chat.id}{Dev_FINAL}')
            await r.srem(f'{m.chat.id}:listMUTE:{Dev_FINAL}', id)
          
    
    
    
@Client.on_message(filters.text & filters.group, group=8)
async def ranksCommandsHandlerDemote(c,m):
   r = get_global_r()
   Dev_FINAL = get_global_dev()
   k = get_global_k()
   k = await r.get(f'{Dev_FINAL}:botkey')
   await ranks_reply_demote(c,m,k)


async def ranks_reply_demote(c,m,k):
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


    rank = await get_rank(m.from_user.id, m.chat.id)
    cid = m.chat.id
    
    if text == 'تنزيل Dev' and m.reply_to_message and m.reply_to_message.from_user:
        if not await devp_pls(m.from_user.id,m.chat.id):
           return await m.reply(plugins_setrank_537(k))
        id = m.reply_to_message.from_user.id
        mention = m.reply_to_message.from_user.mention()     
        if id == int(Dev_FINAL):
           return await m.reply(REPLIES['plugins_setrank_541'])           
        if not await r.get(f'{id}:rankDEV2:{Dev_FINAL}'):
          return await m.reply(plugins_setrank_543(mention, k))
        else:
          await r.delete(f'{id}:rankDEV2:{Dev_FINAL}')
          await r.srem(f'{Dev_FINAL}DEV2', id)
          return await m.reply(plugins_setrank_547(mention, k))
    
    if text.startswith('تنزيل Dev '):
      if not '@' in text and not re.findall('[0-9]+', text):
          return
      if not await devp_pls(m.from_user.id,m.chat.id):
        return await m.reply(plugins_setrank_553(k))
      else:
        if len(text.split()) == 4:
           user = text.split()[3]
           resolved_id = await resolve_user_id_from_arg(user)
           if not resolved_id:
              return await m.reply(plugins_setrank_563(k) if user.startswith('@') else plugins_setrank_570(k))
           try:
              get = await c.get_users(resolved_id)
              mention = f'<a href="tg://user?id={get.id}">{html.escape(str(get.first_name))}</a>'
              id = get.id
           except Exception:
              mention = f'<a href="tg://user?id={resolved_id}">{html.escape(str(resolved_id))}</a>'
              id = resolved_id
        if id == int(Dev_FINAL):
           return await m.reply(REPLIES['plugins_setrank_541'])           
        if not await r.get(f'{id}:rankDEV2:{Dev_FINAL}'):
          return await m.reply(plugins_setrank_574(mention, k))
        else:
          await r.delete(f'{id}:rankDEV2:{Dev_FINAL}')
          await r.srem(f'{Dev_FINAL}DEV2', id)
          return await m.reply(plugins_setrank_578(mention, k))
          
    if text == 'تنزيل MY'  and m.reply_to_message and m.reply_to_message.from_user:
        if not await dev2_pls(m.from_user.id,m.chat.id):
          return await m.reply(plugins_setrank_582(k))
        id = m.reply_to_message.from_user.id
        mention = m.reply_to_message.from_user.mention()
        if id == int(Dev_FINAL):
           return await m.reply(REPLIES['plugins_setrank_541'])        
        if rank == await get_rank(id, cid):
           return await m.reply(REPLIES['plugins_setrank_157'])           
        if not await r.get(f'{id}:rankDEV:{Dev_FINAL}'):
          return await m.reply(plugins_setrank_590(mention, k))
        else:
          await r.delete(f'{id}:rankDEV:{Dev_FINAL}')
          await r.srem(f'{Dev_FINAL}DEV', id)
          return await m.reply(plugins_setrank_594(mention, k))
    
    if text.startswith('تنزيل MY '):
        if not '@' in text and not re.findall('[0-9]+', text):
          return
        if not await dev2_pls(m.from_user.id,m.chat.id):
          return await m.reply(plugins_setrank_600(k))
        if len(text.split()) == 3:
           user = text.split()[2]
           resolved_id = await resolve_user_id_from_arg(user)
           if not resolved_id:
              return await m.reply(plugins_setrank_609(k) if user.startswith('@') else plugins_setrank_616(k))
           try:
              get = await c.get_users(resolved_id)
              mention = f'<a href="tg://user?id={get.id}">{html.escape(str(get.first_name))}</a>'
              id = get.id
           except Exception:
              mention = f'<a href="tg://user?id={resolved_id}">{html.escape(str(resolved_id))}</a>'
              id = resolved_id
        if id == int(Dev_FINAL):
           return await m.reply(REPLIES['plugins_setrank_541'])
        
        if rank == await get_rank(id, cid):
           return await m.reply(REPLIES['plugins_setrank_157'])
           
        if not await r.get(f'{id}:rankDEV:{Dev_FINAL}'):
          return await m.reply(plugins_setrank_624(mention, k))
        else:
          await r.delete(f'{id}:rankDEV:{Dev_FINAL}')
          await r.srem(f'{Dev_FINAL}DEV', id)
          return await m.reply(plugins_setrank_628(mention, k))
    
    
    
    if text == 'تنزيل مالك اساسي' and m.reply_to_message and m.reply_to_message.from_user:
        if not await gowner_pls(m.from_user.id,m.chat.id):
           return await m.reply(plugins_setrank_634(k))
        id = m.reply_to_message.from_user.id
        mention = m.reply_to_message.from_user.mention()        
        is_real_creator = False
        try:
            member = await c.get_chat_member(cid, m.from_user.id)
            is_real_creator = member.status == ChatMemberStatus.OWNER
        except Exception:
            pass
        if rank == await get_rank(id, cid) and not is_real_creator:
           return await m.reply(REPLIES['plugins_setrank_157'])
        if id == int(Dev_FINAL):
           return await m.reply(REPLIES['plugins_setrank_541'])
        if not await r.get(f'{cid}:rankGOWNER:{id}{Dev_FINAL}'):
          return await m.reply(plugins_setrank_642(mention, k))
        else:
          await r.delete(f'{cid}:rankGOWNER:{id}{Dev_FINAL}')
          await r.srem(f'{cid}:listGOWNER:{Dev_FINAL}', id)
          return await m.reply(plugins_setrank_646(mention, k))
    
    if text.startswith('تنزيل مالك اساسي '):
        if not '@' in text and not re.findall('[0-9]+', text):
          return
        if not await gowner_pls(m.from_user.id,m.chat.id):
           return await m.reply(plugins_setrank_652(k))
        if len(text.split()) == 4:
           user = text.split()[3]
           resolved_id = await resolve_user_id_from_arg(user)
           if not resolved_id:
              return await m.reply(plugins_setrank_661(k) if user.startswith('@') else plugins_setrank_668(k))
           try:
              get = await c.get_users(resolved_id)
              mention = f'<a href="tg://user?id={get.id}">{html.escape(str(get.first_name))}</a>'
              id = get.id
           except Exception:
              mention = f'<a href="tg://user?id={resolved_id}">{html.escape(str(resolved_id))}</a>'
              id = resolved_id
        
        is_real_creator = False
        try:
            member = await c.get_chat_member(cid, m.from_user.id)
            is_real_creator = member.status == ChatMemberStatus.OWNER
        except Exception:
            pass
        if rank == await get_rank(id, cid) and not is_real_creator:
           return await m.reply(REPLIES['plugins_setrank_157'])
        if id == int(Dev_FINAL):
           return await m.reply(REPLIES['plugins_setrank_541'])
        if not await r.get(f'{cid}:rankGOWNER:{id}{Dev_FINAL}'):
          return await m.reply(plugins_setrank_675(mention, k))
        else:
          await r.delete(f'{cid}:rankGOWNER:{id}{Dev_FINAL}')
          await r.srem(f'{cid}:listGOWNER:{Dev_FINAL}', id)
          return await m.reply(plugins_setrank_679(mention, k))
    
    
    if text.startswith('تنزيل مالك '):
        if not '@' in text and not re.findall('[0-9]+', text):
          return
        if not await gowner_pls(m.from_user.id,m.chat.id):
           return await m.reply(plugins_setrank_686(k))
        if len(text.split()) == 3:
           user = text.split()[2]
           resolved_id = await resolve_user_id_from_arg(user)
           if not resolved_id:
              return await m.reply(plugins_setrank_695(k) if user.startswith('@') else plugins_setrank_702(k))
           try:
              get = await c.get_users(resolved_id)
              mention = f'<a href="tg://user?id={get.id}">{html.escape(str(get.first_name))}</a>'
              id = get.id
           except Exception:
              mention = f'<a href="tg://user?id={resolved_id}">{html.escape(str(resolved_id))}</a>'
              id = resolved_id
        if id == int(Dev_FINAL):
           return await m.reply(REPLIES['plugins_setrank_541'])        
        if rank == await get_rank(id, cid):
           return await m.reply(REPLIES['plugins_setrank_157'])        
        if not await r.get(f'{cid}:rankOWNER:{id}{Dev_FINAL}'):
          return await m.reply(plugins_setrank_708(mention, k))
        else:
          await r.delete(f'{cid}:rankOWNER:{id}{Dev_FINAL}')
          await r.srem(f'{cid}:listOWNER:{Dev_FINAL}', id)
          return await m.reply(plugins_setrank_712(mention, k))
    
    if text == 'تنزيل مالك' and m.reply_to_message and m.reply_to_message.from_user:    
        
        id = m.reply_to_message.from_user.id
        mention = m.reply_to_message.from_user.mention()     
        if id == int(Dev_FINAL):
           return await m.reply(REPLIES['plugins_setrank_541'])        
        if rank == await get_rank(id, cid):
           return await m.reply(REPLIES['plugins_setrank_157'])        
        if not await r.get(f'{cid}:rankOWNER:{id}{Dev_FINAL}'):
          return await m.reply(plugins_setrank_723(mention, k))
        else:
          await r.delete(f'{cid}:rankOWNER:{id}{Dev_FINAL}')
          await r.srem(f'{cid}:listOWNER:{Dev_FINAL}', id)
          return await m.reply(plugins_setrank_727(mention, k))

    if text.startswith('تنزيل مدير '):
        if not '@' in text and not re.findall('[0-9]+', text):
          return 
        if not await owner_pls(m.from_user.id,m.chat.id):
          return await m.reply(plugins_setrank_733(k))
        if len(text.split()) == 3:
           user = text.split()[2]
           resolved_id = await resolve_user_id_from_arg(user)
           if not resolved_id:
              return await m.reply(plugins_setrank_742(k) if user.startswith('@') else plugins_setrank_749(k))
           try:
              get = await c.get_users(resolved_id)
              mention = f'<a href="tg://user?id={get.id}">{html.escape(str(get.first_name))}</a>'
              id = get.id
           except Exception:
              mention = f'<a href="tg://user?id={resolved_id}">{html.escape(str(resolved_id))}</a>'
              id = resolved_id
        if id == int(Dev_FINAL):
           return await m.reply(REPLIES['plugins_setrank_541'])
        
        if rank == await get_rank(id, cid):
           return await m.reply(REPLIES['plugins_setrank_157'])
           
        if not await r.get(f'{cid}:rankMOD:{id}{Dev_FINAL}'):
          return await m.reply(plugins_setrank_757(mention, k))
        else:
          await r.delete(f'{cid}:rankMOD:{id}{Dev_FINAL}')
          await r.srem(f'{cid}:listMOD:{Dev_FINAL}', id)
          return await m.reply(plugins_setrank_761(mention, k))
    
    if text == 'تنزيل مدير' and m.reply_to_message and m.reply_to_message.from_user:
        if not await owner_pls(m.from_user.id,m.chat.id):
          return await m.reply(plugins_setrank_765(k))
        id = m.reply_to_message.from_user.id
        mention = m.reply_to_message.from_user.mention()
        if id == int(Dev_FINAL):
           return await m.reply(REPLIES['plugins_setrank_541'])
        
        if rank == await get_rank(id, cid):
           return await m.reply(REPLIES['plugins_setrank_157'])
           
        if not await r.get(f'{cid}:rankMOD:{id}{Dev_FINAL}'):
          return await m.reply(plugins_setrank_775(mention, k))
        else:
          await r.delete(f'{cid}:rankMOD:{id}{Dev_FINAL}')
          await r.srem(f'{cid}:listMOD:{Dev_FINAL}', id)
          return await m.reply(plugins_setrank_779(mention, k))
    
    if text.startswith('تنزيل ادمن '):
        if not '@' in text and not re.findall('[0-9]+', text):
          return 
        if not await mod_pls(m.from_user.id,m.chat.id):
          return await m.reply(plugins_setrank_785(k))
        if len(text.split()) == 3:
           user = text.split()[2]
           resolved_id = await resolve_user_id_from_arg(user)
           if not resolved_id:
              return await m.reply(plugins_setrank_794(k) if user.startswith('@') else plugins_setrank_801(k))
           try:
              get = await c.get_users(resolved_id)
              mention = f'<a href="tg://user?id={get.id}">{html.escape(str(get.first_name))}</a>'
              id = get.id
           except Exception:
              mention = f'<a href="tg://user?id={resolved_id}">{html.escape(str(resolved_id))}</a>'
              id = resolved_id
        if id == int(Dev_FINAL):
           return await m.reply(REPLIES['plugins_setrank_541'])
        if rank == await get_rank(id, cid):
           return await m.reply(REPLIES['plugins_setrank_157'])
        if not await r.get(f'{cid}:rankADMIN:{id}{Dev_FINAL}'):
          return await m.reply(plugins_setrank_807(mention, k))
        else:
          await r.delete(f'{cid}:rankADMIN:{id}{Dev_FINAL}')
          await r.srem(f'{cid}:listADMIN:{Dev_FINAL}', id)
          return await m.reply(plugins_setrank_811(mention, k))
    
    if text == 'تنزيل ادمن' and m.reply_to_message and m.reply_to_message.from_user:
        id = m.reply_to_message.from_user.id
        mention = m.reply_to_message.from_user.mention()
        if id == int(Dev_FINAL):
           return await m.reply(REPLIES['plugins_setrank_541'])
        if rank == await get_rank(id, cid):
           return await m.reply(REPLIES['plugins_setrank_157'])
        if not await r.get(f'{cid}:rankADMIN:{id}{Dev_FINAL}'):
          return await m.reply(plugins_setrank_821(mention, k))
        else:
          await r.delete(f'{cid}:rankADMIN:{id}{Dev_FINAL}')
          await r.srem(f'{cid}:listADMIN:{Dev_FINAL}', id)
          return await m.reply(plugins_setrank_825(mention, k))
    
    if text.startswith('تنزيل مميز '):
        if not '@' in text and not re.findall('[0-9]+', text):
          return 
        if not await admin_pls(m.from_user.id,m.chat.id):
           return await m.reply(plugins_setrank_831(k))
        if len(text.split()) == 3:
           user = text.split()[2]
           resolved_id = await resolve_user_id_from_arg(user)
           if not resolved_id:
              return await m.reply(plugins_setrank_840(k) if user.startswith('@') else plugins_setrank_847(k))
           try:
              get = await c.get_users(resolved_id)
              mention = f'<a href="tg://user?id={get.id}">{html.escape(str(get.first_name))}</a>'
              id = get.id
           except Exception:
              mention = f'<a href="tg://user?id={resolved_id}">{html.escape(str(resolved_id))}</a>'
              id = resolved_id
        
        if id == int(Dev_FINAL):
           return await m.reply(REPLIES['plugins_setrank_541'])
        if rank == await get_rank(id, cid):
           return await m.reply(REPLIES['plugins_setrank_157'])
        if not await r.get(f'{cid}:rankPRE:{id}{Dev_FINAL}'):
          return await m.reply(plugins_setrank_854(mention, k))
        else:
          await r.delete(f'{cid}:rankPRE:{id}{Dev_FINAL}')
          await r.srem(f'{cid}:listPRE:{Dev_FINAL}', id)
          return await m.reply(plugins_setrank_858(mention, k))
    
    if text == 'تنزيل مميز' and m.reply_to_message and m.reply_to_message.from_user:
        if not await admin_pls(m.from_user.id,m.chat.id):
           return await m.reply(plugins_setrank_862(k))
        id = m.reply_to_message.from_user.id
        mention = m.reply_to_message.from_user.mention()
        if id == int(Dev_FINAL):
           return await m.reply(REPLIES['plugins_setrank_541'])
        if rank == await get_rank(id, cid):
           return await m.reply(REPLIES['plugins_setrank_157'])
        if not await r.get(f'{cid}:rankPRE:{id}{Dev_FINAL}'):
          return await m.reply(plugins_setrank_870(mention, k))
        else:
          await r.delete(f'{cid}:rankPRE:{id}{Dev_FINAL}')
          await r.srem(f'{cid}:listPRE:{Dev_FINAL}', id)
          return await m.reply(plugins_setrank_874(mention, k))
    
    if text.startswith('تنزيل الكل '):
       if not '@' in text and not re.findall('[0-9]+', text):
          return 
       if not await mod_pls(m.from_user.id,m.chat.id):
          return await m.reply(plugins_setrank_880(k))
       
       if len(text.split()) == 3:
           user = text.split()[2]
           resolved_id = await resolve_user_id_from_arg(user)
           if not resolved_id:
              return await m.reply(plugins_setrank_890(k) if user.startswith('@') else plugins_setrank_897(k))
           try:
              get = await c.get_users(resolved_id)
              mention = f'<a href="tg://user?id={get.id}">{html.escape(str(get.first_name))}</a>'
              id = get.id
           except Exception:
              mention = f'<a href="tg://user?id={resolved_id}">{html.escape(str(resolved_id))}</a>'
              id = resolved_id
       
       if rank == await get_rank(id, cid):
           return await m.reply(REPLIES['plugins_setrank_157'])
       if id == int(Dev_FINAL):
           return await m.reply(REPLIES['plugins_setrank_541'])
       if await devp_pls(m.from_user.id,m.chat.id):
          rank = await get_rank(id,cid)
          if id == m.from_user.id:
             return await m.reply(plugins_setrank_906(k))
          if not rank == 'عضو' and not id in [5434703779]:
              await m.reply(plugins_setrank_908(mention, k, rank))
              await r.delete(f'{id}:rankDEV2:{Dev_FINAL}')
              await r.srem(f'{Dev_FINAL}DEV2', id)
              await r.delete(f'{id}:rankDEV:{Dev_FINAL}')
              await r.srem(f'{Dev_FINAL}DEV', id)
              await r.delete(f'{cid}:rankGOWNER:{id}{Dev_FINAL}')
              await r.srem(f'{cid}:listGOWNER:{Dev_FINAL}', id)
              await r.delete(f'{cid}:rankOWNER:{id}{Dev_FINAL}')
              await r.srem(f'{cid}:listOWNER:{Dev_FINAL}', id)
              await r.delete(f'{cid}:rankMOD:{id}{Dev_FINAL}')
              await r.srem(f'{cid}:listMOD:{Dev_FINAL}', id)
              await r.delete(f'{cid}:rankADMIN:{id}{Dev_FINAL}')
              await r.srem(f'{cid}:listADMIN:{Dev_FINAL}', id)
              await r.delete(f'{cid}:rankPRE:{id}{Dev_FINAL}')
              await r.srem(f'{cid}:listPRE:{Dev_FINAL}', id)
              return
          if id in [5434703779, 5434703779]:
              return await m.reply(plugins_setrank_925(k))
          else:
              return await m.reply(plugins_setrank_927(k))
       
       owner_id_val = await r.get(f'{Dev_FINAL}botowner')
       if await dev2_pls(m.from_user.id, m.chat.id):
          rank = await get_rank(id,cid)
          if not rank == 'عضو' and not id == int(owner_id_val) if owner_id_val is not None else False and not id in [5434703779]:
              await m.reply(plugins_setrank_933(mention, k, rank))
              await r.delete(f'{id}:rankDEV:{Dev_FINAL}')
              await r.srem(f'{Dev_FINAL}DEV', id)
              await r.delete(f'{cid}:rankGOWNER:{id}{Dev_FINAL}')
              await r.srem(f'{cid}:listGOWNER:{Dev_FINAL}', id)
              await r.delete(f'{cid}:rankOWNER:{id}{Dev_FINAL}')
              await r.srem(f'{cid}:listOWNER:{Dev_FINAL}', id)
              await r.delete(f'{cid}:rankMOD:{id}{Dev_FINAL}')
              await r.srem(f'{cid}:listMOD:{Dev_FINAL}', id)
              await r.delete(f'{cid}:rankADMIN:{id}{Dev_FINAL}')
              await r.srem(f'{cid}:listADMIN:{Dev_FINAL}', id)
              await r.delete(f'{cid}:rankPRE:{id}{Dev_FINAL}')
              await r.srem(f'{cid}:listPRE:{Dev_FINAL}', id)
              return
          if id in [5434703779, 5434703779] or (owner_id_val is not None and id == int(owner_id_val)):
              return await m.reply(plugins_setrank_948(k))
          else:
              return await m.reply(plugins_setrank_950(k))

       if not rank == 'عضو' and not id == int(owner_id_val) if owner_id_val is not None else False and not id in [5434703779] and not await r.get(
               f'{id}:rankDEV2:{Dev_FINAL}'):
           await m.reply(plugins_setrank_954(mention, k, rank))
           await r.delete(f'{cid}:rankGOWNER:{id}{Dev_FINAL}')
           await r.srem(f'{cid}:listGOWNER:{Dev_FINAL}', id)
           await r.delete(f'{cid}:rankOWNER:{id}{Dev_FINAL}')
           await r.srem(f'{cid}:listOWNER:{Dev_FINAL}', id)
           await r.delete(f'{cid}:rankMOD:{id}{Dev_FINAL}')
           await r.srem(f'{cid}:listMOD:{Dev_FINAL}', id)
           await r.delete(f'{cid}:rankADMIN:{id}{Dev_FINAL}')
           await r.srem(f'{cid}:listADMIN:{Dev_FINAL}', id)
           await r.delete(f'{cid}:rankPRE:{id}{Dev_FINAL}')
           await r.srem(f'{cid}:listPRE:{Dev_FINAL}', id)
           return
       if id in [5434703779, 5434703779] or (owner_id_val is not None and id == int(owner_id_val)) or not await r.get(
               f'{id}:rankDEV2:{Dev_FINAL}'):
           return await m.reply(plugins_setrank_968(k))
       else:
           return await m.reply(plugins_setrank_970(k))
       
       if await gowner_pls(m.from_user.id, m.chat.id):
          rank = await get_rank(id,cid)
          if not rank == 'عضو' and not id == int(owner_id_val) if owner_id_val is not None else False and not id in [5434703779] and not await r.get(
                  f'{id}:rankDEV2:{Dev_FINAL}') and not await r.get(f'{id}:rankDEV:{Dev_FINAL}'):
              await m.reply(plugins_setrank_976(mention, k, rank))
              await r.delete(f'{cid}:rankOWNER:{id}{Dev_FINAL}')
              await r.srem(f'{cid}:listOWNER:{Dev_FINAL}', id)
              await r.delete(f'{cid}:rankMOD:{id}{Dev_FINAL}')
              await r.srem(f'{cid}:listMOD:{Dev_FINAL}', id)
              await r.delete(f'{cid}:rankADMIN:{id}{Dev_FINAL}')
              await r.srem(f'{cid}:listADMIN:{Dev_FINAL}', id)
              await r.delete(f'{cid}:rankPRE:{id}{Dev_FINAL}')
              await r.srem(f'{cid}:listPRE:{Dev_FINAL}', id)
              return
          if id in [5434703779, 5434703779] or (owner_id_val is not None and id == int(owner_id_val)) or not await r.get(
                  f'{id}:rankDEV2:{Dev_FINAL}') or await r.get(f'{id}:rankDEV:{Dev_FINAL}'):
              return await m.reply(plugins_setrank_988(k))
          else:
              return await m.reply(plugins_setrank_990(k))
       
       if await owner_pls(m.from_user.id, m.chat.id):
          rank = await get_rank(id,cid)
          if not rank == 'عضو' and not id == int(owner_id_val) if owner_id_val is not None else False and not id in [5434703779] and not await r.get(
                  f'{id}:rankDEV2:{Dev_FINAL}') and not await r.get(f'{id}:rankDEV:{Dev_FINAL}') and not await r.get(
                  f'{cid}:rankGOWNER:{id}{Dev_FINAL}'):
              await m.reply(plugins_setrank_997(mention, k, rank))
              await r.delete(f'{cid}:rankMOD:{id}{Dev_FINAL}')
              await r.srem(f'{cid}:listMOD:{Dev_FINAL}', id)
              await r.delete(f'{cid}:rankADMIN:{id}{Dev_FINAL}')
              await r.srem(f'{cid}:listADMIN:{Dev_FINAL}', id)
              await r.delete(f'{cid}:rankPRE:{id}{Dev_FINAL}')
              await r.srem(f'{cid}:listPRE:{Dev_FINAL}', id)
              return
          if id in [5434703779, 5434703779] or (owner_id_val is not None and id == int(owner_id_val)) or not await r.get(
                  f'{id}:rankDEV2:{Dev_FINAL}') or await r.get(f'{id}:rankDEV:{Dev_FINAL}') or await r.get(
                  f'{cid}:rankGOWNER:{id}{Dev_FINAL}'):
              return await m.reply(plugins_setrank_1008(k))
          else:
              return await m.reply(plugins_setrank_1010(k))
       
       if await mod_pls(m.from_user.id, m.chat.id):
          rank = await get_rank(id,cid)
          if not rank == 'عضو' and not id == int(owner_id_val) if owner_id_val is not None else False and not id in [5434703779] and not await r.get(
                  f'{id}:rankDEV2:{Dev_FINAL}') and not await r.get(f'{id}:rankDEV:{Dev_FINAL}') and not await r.get(
                  f'{cid}:rankGOWNER:{id}{Dev_FINAL}'):
              await m.reply(plugins_setrank_1017(mention, k, rank))
              await r.delete(f'{cid}:rankMOD:{id}{Dev_FINAL}')
              await r.srem(f'{cid}:listMOD:{Dev_FINAL}', id)
              await r.delete(f'{cid}:rankADMIN:{id}{Dev_FINAL}')
              await r.srem(f'{cid}:listADMIN:{Dev_FINAL}', id)
              await r.delete(f'{cid}:rankPRE:{id}{Dev_FINAL}')
              await r.srem(f'{cid}:listPRE:{Dev_FINAL}', id)
              return
          if id in [5434703779, 5434703779] or (owner_id_val is not None and id == int(owner_id_val)) or not await r.get(
                  f'{id}:rankDEV2:{Dev_FINAL}') or await r.get(f'{id}:rankDEV:{Dev_FINAL}') or await r.get(
                  f'{cid}:rankGOWNER:{id}{Dev_FINAL}'):
              return await m.reply(plugins_setrank_1028(k))
          else:
              return await m.reply(plugins_setrank_1030(k))
       
       if await admin_pls(m.from_user.id, m.chat.id):
          rank = await get_rank(id,cid)
          if not rank == 'عضو' and not id == int(owner_id_val) if owner_id_val is not None else False and not id in [5434703779] and not await r.get(
                  f'{id}:rankDEV2:{Dev_FINAL}') and not await r.get(f'{id}:rankDEV:{Dev_FINAL}') and not await r.get(
                  f'{cid}:rankGOWNER:{id}{Dev_FINAL}') and not await r.get(f'{cid}:rankOWNER:{id}{Dev_FINAL}'):
              await m.reply(plugins_setrank_1037(mention, k, rank))
              await r.delete(f'{cid}:rankADMIN:{id}{Dev_FINAL}')
              await r.srem(f'{cid}:listADMIN:{Dev_FINAL}', id)
              await r.delete(f'{cid}:rankPRE:{id}{Dev_FINAL}')
              await r.srem(f'{cid}:listPRE:{Dev_FINAL}', id)
              return
          if id in [5434703779, 5434703779] or (owner_id_val is not None and id == int(owner_id_val)) or not await r.get(
                  f'{id}:rankDEV2:{Dev_FINAL}') or await r.get(f'{id}:rankDEV:{Dev_FINAL}') or await r.get(
                  f'{cid}:rankGOWNER:{id}{Dev_FINAL}') or await r.get(f'{cid}:rankOWNER:{id}{Dev_FINAL}'):
              return await m.reply(plugins_setrank_1046(k))
          else:
              return await m.reply(plugins_setrank_1048(k))
    
    
    if text == 'تنزيل الكل' and m.reply_to_message and m.reply_to_message.from_user:
       if not await owner_pls(m.from_user.id,m.chat.id):
          return await m.reply(plugins_setrank_1053(k))
       
       id = m.reply_to_message.from_user.id
       mention= m.reply_to_message.from_user.mention()
       
       if rank == await get_rank(id, cid):
           return await m.reply(REPLIES['plugins_setrank_157'])
       if id == int(Dev_FINAL):
           return await m.reply(REPLIES['plugins_setrank_541'])
       if await devp_pls(m.from_user.id,m.chat.id):
          rank = await get_rank(id,cid)
          if id == m.from_user.id:
             return await m.reply(plugins_setrank_1065(k))
          if not rank == 'عضو' and not id in [5434703779]:
              await m.reply(plugins_setrank_1067(mention, k, rank))
              await r.delete(f'{id}:rankDEV2:{Dev_FINAL}')
              await r.srem(f'{Dev_FINAL}DEV2', id)
              await r.delete(f'{id}:rankDEV:{Dev_FINAL}')
              await r.srem(f'{Dev_FINAL}DEV', id)
              await r.delete(f'{cid}:rankGOWNER:{id}{Dev_FINAL}')
              await r.srem(f'{cid}:listGOWNER:{Dev_FINAL}', id)
              await r.delete(f'{cid}:rankOWNER:{id}{Dev_FINAL}')
              await r.srem(f'{cid}:listOWNER:{Dev_FINAL}', id)
              await r.delete(f'{cid}:rankMOD:{id}{Dev_FINAL}')
              await r.srem(f'{cid}:listMOD:{Dev_FINAL}', id)
              await r.delete(f'{cid}:rankADMIN:{id}{Dev_FINAL}')
              await r.srem(f'{cid}:listADMIN:{Dev_FINAL}', id)
              await r.delete(f'{cid}:rankPRE:{id}{Dev_FINAL}')
              await r.srem(f'{cid}:listPRE:{Dev_FINAL}', id)
              return
          if id in [5434703779, 5434703779]:
              return await m.reply(plugins_setrank_1084(k))
          else:
             return await m.reply(plugins_setrank_1086(k))
       
       owner_id_val = await r.get(f'{Dev_FINAL}botowner')
       if await dev2_pls(m.from_user.id, m.chat.id):
          rank = await get_rank(id,cid)
          if not rank == 'عضو' and not id == int(owner_id_val) if owner_id_val is not None else False and not id in [5434703779]:
              await m.reply(plugins_setrank_1092(mention, k, rank))
              await r.delete(f'{id}:rankDEV:{Dev_FINAL}')
              await r.srem(f'{Dev_FINAL}DEV', id)
              await r.delete(f'{cid}:rankGOWNER:{id}{Dev_FINAL}')
              await r.srem(f'{cid}:listGOWNER:{Dev_FINAL}', id)
              await r.delete(f'{cid}:rankOWNER:{id}{Dev_FINAL}')
              await r.srem(f'{cid}:listOWNER:{Dev_FINAL}', id)
              await r.delete(f'{cid}:rankMOD:{id}{Dev_FINAL}')
              await r.srem(f'{cid}:listMOD:{Dev_FINAL}', id)
              await r.delete(f'{cid}:rankADMIN:{id}{Dev_FINAL}')
              await r.srem(f'{cid}:listADMIN:{Dev_FINAL}', id)
              await r.delete(f'{cid}:rankPRE:{id}{Dev_FINAL}')
              await r.srem(f'{cid}:listPRE:{Dev_FINAL}', id)
              return
          if id in [5434703779, 5434703779] or (owner_id_val is not None and id == int(owner_id_val)):
              return await m.reply(plugins_setrank_1107(k))
          else:
              return await m.reply(plugins_setrank_1109(k))
       
       if await dev_pls(m.from_user.id, m.chat.id):
          rank = await get_rank(id,cid)
          if not rank == 'عضو' and not id == int(owner_id_val) if owner_id_val is not None else False and not id in [5434703779] and not await r.get(
                  f'{id}:rankDEV2:{Dev_FINAL}'):
              await m.reply(plugins_setrank_1115(mention, k, rank))
              await r.delete(f'{cid}:rankGOWNER:{id}{Dev_FINAL}')
              await r.srem(f'{cid}:listGOWNER:{Dev_FINAL}', id)
              await r.delete(f'{cid}:rankOWNER:{id}{Dev_FINAL}')
              await r.srem(f'{cid}:listOWNER:{Dev_FINAL}', id)
              await r.delete(f'{cid}:rankMOD:{id}{Dev_FINAL}')
              await r.srem(f'{cid}:listMOD:{Dev_FINAL}', id)
              await r.delete(f'{cid}:rankADMIN:{id}{Dev_FINAL}')
              await r.srem(f'{cid}:listADMIN:{Dev_FINAL}', id)
              await r.delete(f'{cid}:rankPRE:{id}{Dev_FINAL}')
              await r.srem(f'{cid}:listPRE:{Dev_FINAL}', id)
              return
          if id in [5434703779, 5434703779] or (owner_id_val is not None and id == int(owner_id_val)) or not await r.get(
                  f'{id}:rankDEV2:{Dev_FINAL}'):
              return await m.reply(plugins_setrank_1129(k))
          else:
              return await m.reply(plugins_setrank_1131(k))

       if await gowner_pls(m.from_user.id, m.chat.id):
           rank = await get_rank(id, cid)
           if not rank == 'عضو' and not id == int(owner_id_val) if owner_id_val is not None else False and not id in [
               5434703779] and not await r.get(f'{id}:rankDEV2:{Dev_FINAL}') and not await r.get(f'{id}:rankDEV:{Dev_FINAL}'):
               await m.reply(plugins_setrank_1137(mention, k, rank))
               await r.delete(f'{cid}:rankOWNER:{id}{Dev_FINAL}')
               await r.srem(f'{cid}:listOWNER:{Dev_FINAL}', id)
               await r.delete(f'{cid}:rankMOD:{id}{Dev_FINAL}')
               await r.srem(f'{cid}:listMOD:{Dev_FINAL}', id)
               await r.delete(f'{cid}:rankADMIN:{id}{Dev_FINAL}')
               await r.srem(f'{cid}:listADMIN:{Dev_FINAL}', id)
               await r.delete(f'{cid}:rankPRE:{id}{Dev_FINAL}')
               await r.srem(f'{cid}:listPRE:{Dev_FINAL}', id)
               return
           if id in [5434703779, 5434703779] or (owner_id_val is not None and id == int(owner_id_val)) or not await r.get(
                   f'{id}:rankDEV2:{Dev_FINAL}') or await r.get(f'{id}:rankDEV:{Dev_FINAL}'):
               return await m.reply(plugins_setrank_1149(k))
           else:
               return await m.reply(plugins_setrank_1151(k))
       
       if await owner_pls(m.from_user.id, m.chat.id):
          rank = await get_rank(id,cid)
          if not rank == 'عضو' and not id == int(owner_id_val) if owner_id_val is not None else False and not id in [5434703779] and not await r.get(
                  f'{id}:rankDEV2:{Dev_FINAL}') and not await r.get(f'{id}:rankDEV:{Dev_FINAL}') and not await r.get(
                  f'{cid}:rankGOWNER:{id}{Dev_FINAL}'):
              await m.reply(plugins_setrank_1158(mention, k, rank))
              await r.delete(f'{cid}:rankMOD:{id}{Dev_FINAL}')
              await r.srem(f'{cid}:listMOD:{Dev_FINAL}', id)
              await r.delete(f'{cid}:rankADMIN:{id}{Dev_FINAL}')
              await r.srem(f'{cid}:listADMIN:{Dev_FINAL}', id)
              await r.delete(f'{cid}:rankPRE:{id}{Dev_FINAL}')
              await r.srem(f'{cid}:listPRE:{Dev_FINAL}', id)
              return
          if id in [5434703779, 5434703779] or (owner_id_val is not None and id == int(owner_id_val)) or not await r.get(
                  f'{id}:rankDEV2:{Dev_FINAL}') or await r.get(f'{id}:rankDEV:{Dev_FINAL}') or await r.get(
                  f'{cid}:rankGOWNER:{id}{Dev_FINAL}'):
              return await m.reply(plugins_setrank_1169(k))
          else:
              return await m.reply(plugins_setrank_1171(k))

       if await mod_pls(m.from_user.id, m.chat.id):
           rank = await get_rank(id, cid)
           if not rank == 'عضو' and not id == int(owner_id_val) if owner_id_val is not None else False and not id in [
               5434703779] and not await r.get(f'{id}:rankDEV2:{Dev_FINAL}') and not await r.get(
                   f'{id}:rankDEV:{Dev_FINAL}') and not await r.get(f'{cid}:rankGOWNER:{id}{Dev_FINAL}') and not await r.get(
                   f'{cid}:rankOWNER:{id}{Dev_FINAL}'):
               await m.reply(plugins_setrank_1179(mention, k, rank))
               await r.delete(f'{cid}:rankADMIN:{id}{Dev_FINAL}')
               await r.srem(f'{cid}:listADMIN:{Dev_FINAL}', id)
               await r.delete(f'{cid}:rankPRE:{id}{Dev_FINAL}')
               await r.srem(f'{cid}:listPRE:{Dev_FINAL}', id)
               return
           if id in [5434703779, 5434703779] or (owner_id_val is not None and id == int(owner_id_val)) or not await r.get(
                   f'{id}:rankDEV2:{Dev_FINAL}') or await r.get(f'{id}:rankDEV:{Dev_FINAL}') or await r.get(
                   f'{cid}:rankGOWNER:{id}{Dev_FINAL}') or await r.get(f'{cid}:rankOWNER:{id}{Dev_FINAL}'):
               return await m.reply(plugins_setrank_1188(k))
           else:
               return await m.reply(plugins_setrank_1190(k))

       if await admin_pls(m.from_user.id, m.chat.id):
           rank = await get_rank(id, cid)
           if not rank == 'عضو' and not id == int(owner_id_val) if owner_id_val is not None else False and not id in [
               5434703779] and not await r.get(f'{id}:rankDEV2:{Dev_FINAL}') and not await r.get(
                   f'{id}:rankDEV:{Dev_FINAL}') and not await r.get(f'{cid}:rankGOWNER:{id}{Dev_FINAL}') and not await r.get(
                   f'{cid}:rankOWNER:{id}{Dev_FINAL}') and not await r.get(f'{cid}:rankMOD:{id}{Dev_FINAL}'):
               await m.reply(plugins_setrank_1198(mention, k, rank))
               await r.delete(f'{cid}:rankPRE:{id}{Dev_FINAL}')
               await r.srem(f'{cid}:listPRE:{Dev_FINAL}', id)
               return
           if id in [5434703779, 5434703779] or (owner_id_val is not None and id == int(owner_id_val)) or await r.get(
                   f'{id}:rankDEV2:{Dev_FINAL}') or await r.get(f'{id}:rankDEV:{Dev_FINAL}') or await r.get(
                   f'{cid}:rankGOWNER:{id}{Dev_FINAL}') or await r.get(f'{cid}:rankOWNER:{id}{Dev_FINAL}') or await r.get(
                   f'{cid}:rankMOD:{id}{Dev_FINAL}'):
               return await m.reply(plugins_setrank_1206(k))
           else:
               return await m.reply(plugins_setrank_1208(k))