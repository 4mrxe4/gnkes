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
from helpers.ranks import *
from helpers.replies_store import (
    plugins_delrank_105,
    plugins_delrank_109,
    plugins_delrank_111,
    plugins_delrank_117,
    plugins_delrank_121,
    plugins_delrank_123,
    plugins_delrank_129,
    plugins_delrank_133,
    plugins_delrank_135,
    plugins_delrank_141,
    plugins_delrank_145,
    plugins_delrank_147,
    plugins_delrank_153,
    plugins_delrank_49,
    plugins_delrank_51,
    plugins_delrank_57,
    plugins_delrank_61,
    plugins_delrank_63,
    plugins_delrank_69,
    plugins_delrank_73,
    plugins_delrank_75,
    plugins_delrank_81,
    plugins_delrank_85,
    plugins_delrank_87,
    plugins_delrank_93,
    plugins_delrank_97,
    plugins_delrank_99,
)



@Client.on_message(filters.text & filters.group, group=13)
async def delRanksHandler(c,m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    k = await r.get(f'{Dev_FINAL}:botkey')
    await del_ranks_func(c,m,k)
    

async def del_ranks_func(c, m, k):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if not await check_global_restrictions(c, m, k):
        return
    text = m.text
    name = await r.get(f'{Dev_FINAL}:BotName') if await r.get(f'{Dev_FINAL}:BotName') else 'فاينل'
    if text.startswith(f'{name} '):
        text = text.replace(f'{name} ', '')
    if await r.get(f'{m.chat.id}:Custom:{m.chat.id}{Dev_FINAL}&text={text}'):
        text = await r.get(f'{m.chat.id}:Custom:{m.chat.id}{Dev_FINAL}&text={text}')
    if await r.get(f'Custom:{Dev_FINAL}&text={text}'):
        text = await r.get(f'Custom:{Dev_FINAL}&text={text}')
    if await check_and_guard_locked_command(c, m, k, text):
        return
    
    id = m.from_user.id
    cid = m.chat.id
    
    if text == 'مسح قائمه Dev':
        if not await devp_pls(id, cid):
            return await m.reply(plugins_delrank_49(k))
        if not await r.smembers(f'{Dev_FINAL}DEV2'):
            return await m.reply(plugins_delrank_51(k))
        count = 0
        for dev2 in await r.smembers(f'{Dev_FINAL}DEV2'):
            await r.srem(f'{Dev_FINAL}DEV2', int(dev2))
            await r.delete(f'{int(dev2)}:rankDEV2:{Dev_FINAL}')
            count += 1
        await m.reply(plugins_delrank_57(k, get_rank(id, cid), k, count, 'قائمة Dev'))
   
    if text == 'مسح قائمه MY':
        if not await dev2_pls(id, cid):
            return await m.reply(plugins_delrank_61(k))
        if not await r.smembers(f'{Dev_FINAL}DEV'):
            return await m.reply(plugins_delrank_63(k))
        count = 0
        for dev in await r.smembers(f'{Dev_FINAL}DEV'):
            await r.srem(f'{Dev_FINAL}DEV', int(dev))
            await r.delete(f'{int(dev)}:rankDEV:{Dev_FINAL}')
            count += 1
        await m.reply(plugins_delrank_69(k, get_rank(id, cid), k, count, 'قائمة MY'))
   
    if text == 'مسح المالكين الاساسيين':
        if not await dev_pls(id, cid):
            return await m.reply(plugins_delrank_73(k))
        if not await r.smembers(f'{cid}:listGOWNER:{Dev_FINAL}'):
            return await m.reply(plugins_delrank_75(k))
        count = 0
        for gowner in await r.smembers(f'{cid}:listGOWNER:{Dev_FINAL}'):
            await r.srem(f'{cid}:listGOWNER:{Dev_FINAL}', int(gowner))
            await r.delete(f'{cid}:rankGOWNER:{int(gowner)}{Dev_FINAL}')
            count += 1
        await m.reply(plugins_delrank_81(k, get_rank(id, cid), k, count, 'المالكين الاساسيين'))
   
    if text == 'مسح المالكين':
        if not await gowner_pls(id, cid):
            return await m.reply(plugins_delrank_85(k))
        if not await r.smembers(f'{cid}:listOWNER:{Dev_FINAL}'):
            return await m.reply(plugins_delrank_87(k))
        count = 0
        for owner in await r.smembers(f'{cid}:listOWNER:{Dev_FINAL}'):
            await r.srem(f'{cid}:listOWNER:{Dev_FINAL}', int(owner))
            await r.delete(f'{cid}:rankOWNER:{int(owner)}{Dev_FINAL}')
            count += 1
        await m.reply(plugins_delrank_93(k, get_rank(id, cid), k, count, 'المالكين'))
   
    if text == 'مسح المدراء':
        if not await owner_pls(id, cid):
            return await m.reply(plugins_delrank_97(k))
        if not await r.smembers(f'{cid}:listMOD:{Dev_FINAL}'):
            return await m.reply(plugins_delrank_99(k))
        count = 0
        for MOD in await r.smembers(f'{cid}:listMOD:{Dev_FINAL}'):
            await r.srem(f'{cid}:listMOD:{Dev_FINAL}', int(MOD))
            await r.delete(f'{cid}:rankMOD:{int(MOD)}{Dev_FINAL}')
            count += 1
        await m.reply(plugins_delrank_105(k, get_rank(id, cid), k, count, 'المدراء'))
   
    if text == 'مسح الادمنيه' or text == 'مسح الادمن':
        if not await mod_pls(id, cid):
            return await m.reply(plugins_delrank_109(k))
        if not await r.smembers(f'{cid}:listADMIN:{Dev_FINAL}'):
            return await m.reply(plugins_delrank_111(k))
        count = 0
        for ADM in await r.smembers(f'{cid}:listADMIN:{Dev_FINAL}'):
            await r.srem(f'{cid}:listADMIN:{Dev_FINAL}', int(ADM))
            await r.delete(f'{cid}:rankADMIN:{int(ADM)}{Dev_FINAL}')
            count += 1
        await m.reply(plugins_delrank_117(k, get_rank(id, cid), k, count, 'الادمن'))
   
    if text == 'مسح المميزين':
        if not await mod_pls(id, cid):
            return await m.reply(plugins_delrank_121(k))
        if not await r.smembers(f'{cid}:listPRE:{Dev_FINAL}'):
            return await m.reply(plugins_delrank_123(k))
        count = 0
        for MOD in await r.smembers(f'{cid}:listPRE:{Dev_FINAL}'):
            await r.srem(f'{cid}:listPRE:{Dev_FINAL}', int(MOD))
            await r.delete(f'{cid}:rankPRE:{int(MOD)}{Dev_FINAL}')
            count += 1
        await m.reply(plugins_delrank_129(k, get_rank(id, cid), k, count, 'المميزين'))
   
    if text == 'مسح المكتومين عام':
        if not await dev_pls(id, cid):
            return await m.reply(plugins_delrank_133(k))
        if not await r.smembers(f'listMUTE:{Dev_FINAL}'):
            return await m.reply(plugins_delrank_135(k))
        count = 0
        for MOD in await r.smembers(f'listMUTE:{Dev_FINAL}'):
            await r.srem(f'listMUTE:{Dev_FINAL}', int(MOD))
            await r.delete(f'{int(MOD)}:mute:{Dev_FINAL}')
            count += 1
        await m.reply(plugins_delrank_141(k, get_rank(id, cid), k, count, 'المكتومين عام'))
   
    if text == 'مسح المحظورين عام':
        if not await dev_pls(id, cid):
            return await m.reply(plugins_delrank_145(k))
        if not await r.smembers(f'listGBAN:{Dev_FINAL}'):
            return await m.reply(plugins_delrank_147(k))
        count = 0
        for MOD in await r.smembers(f'listGBAN:{Dev_FINAL}'):
            await r.srem(f'listGBAN:{Dev_FINAL}', int(MOD))
            await r.delete(f'{int(MOD)}:gban:{Dev_FINAL}')
            count += 1
        await m.reply(plugins_delrank_153(k, get_rank(id, cid), k, count, 'الحمير المحظورين عام'))