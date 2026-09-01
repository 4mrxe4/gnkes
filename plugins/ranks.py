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

import random
import re
import time
from threading import Thread
from compat import Client, filters
from compat import ChatType
from compat import Message
from .protect import run_async_in_thread
from helpers.replies_store import (
    REPLIES,
    plugins_ranks_104,
    plugins_ranks_107,
    plugins_ranks_112,
    plugins_ranks_134,
    plugins_ranks_138,
    plugins_ranks_141,
    plugins_ranks_143,
    plugins_ranks_154,
    plugins_ranks_157,
    plugins_ranks_170,
    plugins_ranks_173,
    plugins_ranks_177,
    plugins_ranks_180,
    plugins_ranks_232,
    plugins_ranks_52,
    plugins_ranks_98,
)


@Client.on_message(filters.text & filters.group, group=35)
async def customrankHandler(c: Client, m: Message):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    k = await r.get(f'{Dev_FINAL}:botkey') or '•'
    channel = await r.get(f'{Dev_FINAL}:BotChannel') or ''
    await customRankFunc(c, m, k, channel)

async def customRankFunc(c: Client, m: Message, k: str, channel: str):
   r = get_global_r()
   Dev_FINAL = get_global_dev()
   k = get_global_k()
   if not await check_global_restrictions(c, m, k):
       return
   text = m.text
   name = await r.get(f'{Dev_FINAL}:BotName') or 'فاينل'
   if text.startswith(f'{name} '):
      text = text.replace(f'{name} ','')
   if await r.get(f'{m.chat.id}:Custom:{m.chat.id}{Dev_FINAL}&text={text}'):
       text = await r.get(f'{m.chat.id}:Custom:{m.chat.id}{Dev_FINAL}&text={text}')
   if await r.get(f'Custom:{Dev_FINAL}&text={text}'):
       text = await r.get(f'Custom:{Dev_FINAL}&text={text}')
   if await check_and_guard_locked_command(c, m, k, text):
       return


   if text == 'الغاء':
     if await r.get(f'{m.from_user.id}:addRank2:{m.chat.id}{Dev_FINAL}') or await r.get(f'{m.from_user.id}:addRank:{m.chat.id}{Dev_FINAL}') or await r.get(f'{m.from_user.id}:delRank:{m.chat.id}{Dev_FINAL}'):
        await m.reply(plugins_ranks_52(k))
        await r.delete(f'{m.from_user.id}:addRank:{m.chat.id}{Dev_FINAL}')
        await r.delete(f'{m.from_user.id}:delRank:{m.chat.id}{Dev_FINAL}')
        await r.delete(f'{m.from_user.id}:addRank2:{m.chat.id}{Dev_FINAL}')

   if await r.get(f'{m.from_user.id}:addRank2:{m.chat.id}{Dev_FINAL}') and await mod_pls(m.from_user.id,m.chat.id) and len(m.text) <= 20:
     rank = await r.get(f'{m.from_user.id}:addRank2:{m.chat.id}{Dev_FINAL}')
     await r.delete(f'{m.from_user.id}:addRank2:{m.chat.id}{Dev_FINAL}')
     if rank == 'مالك اساسي':

       if await r.get(f'{m.chat.id}:RankGowner:{Dev_FINAL}'):
         rrr = await r.get(f'{m.chat.id}:RankGowner:{Dev_FINAL}')
         await r.srem(f'{m.chat.id}:ranklist:{Dev_FINAL}',f'{rank}&&newr={rrr}')
         await r.delete(f'{m.chat.id}:RankGowner:{Dev_FINAL}')
       await r.set(f'{m.chat.id}:RankGowner:{Dev_FINAL}',m.text)
     if rank == 'مالك':
       if await r.get(f'{m.chat.id}:RankOwner:{Dev_FINAL}'):
         rrr = await r.get(f'{m.chat.id}:RankOwner:{Dev_FINAL}')
         await r.srem(f'{m.chat.id}:ranklist:{Dev_FINAL}',f'{rank}&&newr={rrr}')
         await r.delete(f'{m.chat.id}:RankOwner:{Dev_FINAL}')
       await r.set(f'{m.chat.id}:RankOwner:{Dev_FINAL}',m.text)
     if rank == 'مدير':
       if await r.get(f'{m.chat.id}:RankMod:{Dev_FINAL}'):
         rrr = await r.get(f'{m.chat.id}:RankMod:{Dev_FINAL}')
         await r.srem(f'{m.chat.id}:ranklist:{Dev_FINAL}',f'{rank}&&newr={rrr}')
         await r.delete(f'{m.chat.id}:RankMod:{Dev_FINAL}')
       await r.set(f'{m.chat.id}:RankMod:{Dev_FINAL}',m.text)
     if rank == 'ادمن':
       if await r.get(f'{m.chat.id}:RankAdm:{Dev_FINAL}'):
         rrr = await r.get(f'{m.chat.id}:RankAdm:{Dev_FINAL}')
         await r.srem(f'{m.chat.id}:ranklist:{Dev_FINAL}',f'{rank}&&newr={rrr}')
         await r.delete(f'{m.chat.id}:RankAdm:{Dev_FINAL}')
       await r.set(f'{m.chat.id}:RankAdm:{Dev_FINAL}',m.text)
     if rank == 'مميز':
       if await r.get(f'{m.chat.id}:RankPre:{Dev_FINAL}'):
         rrr = await r.get(f'{m.chat.id}:RankPre:{Dev_FINAL}')
         await r.srem(f'{m.chat.id}:ranklist:{Dev_FINAL}',f'{rank}&&newr={rrr}')
         await r.delete(f'{m.chat.id}:RankPre:{Dev_FINAL}')
       await r.set(f'{m.chat.id}:RankPre:{Dev_FINAL}',m.text)
     if rank == 'عضو':
       if await r.get(f'{m.chat.id}:RankMem:{Dev_FINAL}'):
         rrr = await r.get(f'{m.chat.id}:RankMem:{Dev_FINAL}')
         await r.srem(f'{m.chat.id}:ranklist:{Dev_FINAL}',f'{rank}&&newr={rrr}')
         await r.delete(f'{m.chat.id}:RankMem:{Dev_FINAL}')
       await r.set(f'{m.chat.id}:RankMem:{Dev_FINAL}',m.text)
     await r.sadd(f'{m.chat.id}:ranklist:{Dev_FINAL}',f'{rank}&&newr={m.text}')
     return await m.reply(plugins_ranks_98(k, m.text))


   if await r.get(f'{m.from_user.id}:addRank:{m.chat.id}{Dev_FINAL}') and await mod_pls(m.from_user.id,m.chat.id):
     await r.delete(f'{m.from_user.id}:addRank:{m.chat.id}{Dev_FINAL}')
     if not m.text in ['مالك اساسي','مالك','مدير','ادمن','مميز','عضو']:
       return await m.reply(plugins_ranks_104(k))
     else:
       await r.set(f'{m.from_user.id}:addRank2:{m.chat.id}{Dev_FINAL}',m.text,ex=600)
       return await m.reply(plugins_ranks_107(k))

   if await r.get(f'{m.from_user.id}:delRank:{m.chat.id}{Dev_FINAL}') and await mod_pls(m.from_user.id,m.chat.id):
     await r.delete(f'{m.from_user.id}:delRank:{m.chat.id}{Dev_FINAL}')
     if not m.text in ['مالك اساسي','مالك','مدير','ادمن','مميز','عضو']:
       return await m.reply(plugins_ranks_112(k, m.text[:20]))
     else:
       rank = m.text
       if rank == 'مالك اساسي':
         rank2 = await r.get(f'{m.chat.id}:RankGowner:{Dev_FINAL}')
         await r.delete(f'{m.chat.id}:RankGowner:{Dev_FINAL}')
       if rank == 'مالك':
         rank2 = await r.get(f'{m.chat.id}:RankOwner:{Dev_FINAL}')
         await r.delete(f'{m.chat.id}:RankOwner:{Dev_FINAL}')
       if rank == 'مدير':
         rank2 = await r.get(f'{m.chat.id}:RankMod:{Dev_FINAL}')
         await r.delete(f'{m.chat.id}:RankMod:{Dev_FINAL}')
       if rank == 'ادمن':
         rank2 = await r.get(f'{m.chat.id}:RankAdm:{Dev_FINAL}')
         await r.delete(f'{m.chat.id}:RankAdm:{Dev_FINAL}')
       if rank == 'مميز':
         rank2 = await r.get(f'{m.chat.id}:RankPre:{Dev_FINAL}')
         await r.delete(f'{m.chat.id}:RankPre:{Dev_FINAL}')
       if rank == 'عضو':
         rank2 = await r.get(f'{m.chat.id}:RankMem:{Dev_FINAL}')
         await r.delete(f'{m.chat.id}:RankMem:{Dev_FINAL}')
       await r.srem(f'{m.chat.id}:ranklist:{Dev_FINAL}',f'{rank}&&newr={rank2}')
       return await m.reply(plugins_ranks_134(k, rank2))

   if text == 'مسح الرتب':
     if not await mod_pls(m.from_user.id,m.chat.id):
       return await m.reply(plugins_ranks_138(k))
     else:
       if not await r.smembers(f'{m.chat.id}:ranklist:{Dev_FINAL}'):
         return await m.reply(plugins_ranks_141(k))
       else:
         await m.reply(plugins_ranks_143(k))
         await r.delete(f'{m.chat.id}:RankGowner:{Dev_FINAL}')
         await r.delete(f'{m.chat.id}:RankOwner:{Dev_FINAL}')
         await r.delete(f'{m.chat.id}:RankMod:{Dev_FINAL}')
         await r.delete(f'{m.chat.id}:RankAdm:{Dev_FINAL}')
         await r.delete(f'{m.chat.id}:RankPre:{Dev_FINAL}')
         await r.delete(f'{m.chat.id}:RankMem:{Dev_FINAL}')
         return await r.delete(f'{m.chat.id}:ranklist:{Dev_FINAL}')

   if text == 'قائمه الرتب' or text == 'قائمة الرتب':
     if not await mod_pls(m.from_user.id,m.chat.id):
       return await m.reply(plugins_ranks_154(k))
     else:
       if not await r.smembers(f'{m.chat.id}:ranklist:{Dev_FINAL}'):
         return await m.reply(plugins_ranks_157(k))
       else:
         txt = 'قائمة الرتب:\n'
         count = 1
         for rrr in await r.smembers(f'{m.chat.id}:ranklist:{Dev_FINAL}'):
            rank = rrr.split('&&newr=')
            txt += f'{count}) {rank[0]} ~ ( {rank[1]} )\n'
            count += 1
         txt += '\n'
         return await m.reply(txt, disable_web_page_preview=True)

   if text == 'مسح رتبه' or text == 'مسح رتبة':
     if not await mod_pls(m.from_user.id,m.chat.id):
       return await m.reply(plugins_ranks_170(k))
     else:
       await r.set(f'{m.from_user.id}:delRank:{m.chat.id}{Dev_FINAL}',1,ex=600)
       return await m.reply(plugins_ranks_173(k))

   if text == 'تغيير رتبه' or text == 'تغيير رتبة':
     if not await mod_pls(m.from_user.id,m.chat.id):
       return await m.reply(plugins_ranks_177(k))
     else:
       await r.set(f'{m.from_user.id}:addRank:{m.chat.id}{Dev_FINAL}',1,ex=600)
       return await m.reply(plugins_ranks_180(k, k, k, k, k, k, k))

@Client.on_message(filters.text & filters.group, group=36)
async def funRankHandler(client: Client, message: Message):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if message.chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
        return

    if not await check_global_restrictions(client, message, k):
        return

    if await r.get(f'{message.chat.id}:disableFun:{Dev_FINAL}'):
        return

    text = message.text.lower()

    if text.startswith('رفع عام '):
        return

    if text.startswith('رفع '):
        parts = text.split(' ', 1)
        if len(parts) == 2:
            rank_name = parts[1].strip()
            forbidden_words = [
                'كيكه', 'كيكة', 'كيك', 'عسل', 'زق', 'حمار', 'بقره', 'بقرة', 'كلب',
                'قرد', 'تيس', 'ثور', 'هكر', 'دجاجه', 'دجاجة', 'ملكه', 'ملكة', 'ملك',
                'صياد', 'خاروف', 'لقلبي', 'مشرف', 'مالك اساسي', 'مالك', 'مدير', 'منشئ',
                'ادمن', 'مميز', 'عضو','القيود','Dev','Myth','مشغل','عام','dev'
            ]
            is_forbidden = any(word in rank_name for word in forbidden_words)
            if is_forbidden:
                return

            defined_ranks = await r.smembers(f'{message.chat.id}:upfakeDefs:{Dev_FINAL}')
            if defined_ranks and rank_name.lower() in [str(d).lower() for d in defined_ranks]:
                return

            if message.reply_to_message:
                user_id = message.reply_to_message.from_user.id
                await r.set(f'{message.chat.id}:funrank:{user_id}:{Dev_FINAL}', rank_name)
                await message.reply(plugins_ranks_232(message.reply_to_message.from_user.mention(), rank_name))

    elif text == 'مسح رتب التسليه':
        if await mod_pls(message.from_user.id, message.chat.id):
            keys = []
            async for key in r.scan_iter(match=f'*{message.chat.id}:funrank:*:{Dev_FINAL}', count=100):
                keys.append(key)
            if keys:
                await r.delete(*keys)
                await message.reply(REPLIES['plugins_ranks_241'])
            else:
                await message.reply(REPLIES['plugins_ranks_243'])
        else:
            await message.reply(REPLIES['plugins_ranks_245'])

    elif text.startswith('تنزيل '):
        parts = text.split(' ', 1)
        if len(parts) == 2:
            rank_name = parts[1].strip()
            if not message.reply_to_message:
                return 
            user_id = message.reply_to_message.from_user.id
            current = await r.get(f'{message.chat.id}:funrank:{user_id}:{Dev_FINAL}')
            if not current or str(current).lower() != rank_name.lower():
                return 
            await r.delete(f'{message.chat.id}:funrank:{user_id}:{Dev_FINAL}')
            await message.reply(
                f'• تم تنزيل {message.reply_to_message.from_user.mention()} من رتبة "{rank_name}"'
            )
