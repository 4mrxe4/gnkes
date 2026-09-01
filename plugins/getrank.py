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
    plugins_getrank_100,
    plugins_getrank_125,
    plugins_getrank_127,
    plugins_getrank_152,
    plugins_getrank_154,
    plugins_getrank_179,
    plugins_getrank_181,
    plugins_getrank_206,
    plugins_getrank_224,
    plugins_getrank_226,
    plugins_getrank_43,
    plugins_getrank_45,
    plugins_getrank_70,
    plugins_getrank_72,
    plugins_getrank_98,
)



@Client.on_message(filters.text & filters.group, group=12)
async def getRanksHandler(c,m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    k = await r.get(f'{Dev_FINAL}:botkey')
    channel = await r.get(f'{Dev_FINAL}:BotChannel') if await r.get(f'{Dev_FINAL}:BotChannel') else ''
    await get_ranks_func(c,m,k,channel)
    
async def get_ranks_func(c, m, k, channel):
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

    if text == 'قائمه Dev':
        if not await devp_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_getrank_43(k))
        if not await r.smembers(f'{Dev_FINAL}DEV2'):
            return await m.reply(plugins_getrank_45(k))
        text = '- قائمة  Dev²🎖:\n\n'
        count = 1
        for dev2 in await r.smembers(f'{Dev_FINAL}DEV2'):
            if count == 101: break
            try:
                user = await c.get_users(int(dev2))
                mention = user.mention()
                id = user.id
                username = user.username
                if user.username:
                    text += f'{count} - @{username} - 「 `{id}` 」\n'
                else:
                    text += f'{count} - {mention} - 「 `{id}` 」\n'
                count += 1
            except:
                mention = f'<a href="tg://user?id={int(dev2)}">@{html.escape(str(channel))}</a>'
                id = int(dev2)
                text += f'{count} - {mention} - 「 `{id}` 」\n'
                count += 1
        text += '\n'
        await m.reply(text)
   
    if text == 'قائمه MY':
        if not await dev2_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_getrank_70(k))
        if not await r.smembers(f'{Dev_FINAL}DEV'):
            return await m.reply(plugins_getrank_72(k))
        text = '- قائمة Myth🎖️:\n\n'
        count = 1
        for dev in await r.smembers(f'{Dev_FINAL}DEV'):
            if count == 101: break
            try:
                user = await c.get_users(int(dev))
                mention = user.mention()
                id = user.id
                username = user.username
                if user.username:
                    text += f'{count} - @{username} - 「 `{id}` 」\n'
                else:
                    text += f'{count} - {mention} - 「 `{id}` 」\n'
                count += 1
            except:
                mention = f'<a href="tg://user?id={int(dev)}">@{html.escape(str(channel))}</a>'
                id = int(dev)
                text += f'{count} - {mention} - 「 `{id}` 」\n'
                count += 1
        text += '\n'
        await m.reply(text)
          
    cid = m.chat.id
    if text == 'المالكين الاساسيين':
        if not await dev_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_getrank_98(k))
        if not await r.smembers(f'{cid}:listGOWNER:{Dev_FINAL}'):
            return await m.reply(plugins_getrank_100(k))
        text = '- المالكين الاساسيين:\n\n'
        count = 1
        for gowner in await r.smembers(f'{cid}:listGOWNER:{Dev_FINAL}'):
            if count == 101: break
            try:
                user = await c.get_users(int(gowner))
                mention = user.mention()
                id = user.id
                username = user.username
                if user.username:
                    text += f'{count} - @{username} - 「 `{id}` 」\n'
                else:
                    text += f'{count} - {mention} - 「 `{id}` 」\n'
                count += 1
            except:
                mention = f'<a href="tg://user?id={int(gowner)}">@{html.escape(str(channel))}</a>'
                id = int(gowner)
                text += f'{count} - {mention} - 「 `{id}` 」\n'
                count += 1
        text += '\n'
        await m.reply(text)
          
    if text == 'المالكين':
        if not await gowner_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_getrank_125(k))
        if not await r.smembers(f'{cid}:listOWNER:{Dev_FINAL}'):
            return await m.reply(plugins_getrank_127(k))
        text = '- المالكيين:\n\n'
        count = 1
        for owner in await r.smembers(f'{cid}:listOWNER:{Dev_FINAL}'):
            if count == 101: break
            try:
                user = await c.get_users(int(owner))
                mention = user.mention()
                id = user.id
                username = user.username
                if user.username:
                    text += f'{count} - @{username} - 「 `{id}` 」\n'
                else:
                    text += f'{count} - {mention} - 「 `{id}` 」\n'
                count += 1
            except:
                mention = f'<a href="tg://user?id={int(owner)}">@{html.escape(str(channel))}</a>'
                id = int(owner)
                text += f'{count} - {mention} - 「 `{id}` 」\n'
                count += 1
        text += '\n'
        await m.reply(text)
   
    if text == 'المدراء':
        if not await owner_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_getrank_152(k))
        if not await r.smembers(f'{cid}:listMOD:{Dev_FINAL}'):
            return await m.reply(plugins_getrank_154(k))
        text = '- المدراء:\n\n'
        count = 1
        for mod in await r.smembers(f'{cid}:listMOD:{Dev_FINAL}'):
            if count == 101: break
            try:
                user = await c.get_users(int(mod))
                mention = user.mention()
                id = user.id
                username = user.username
                if user.username:
                    text += f'{count} - @{username} - 「 `{id}` 」\n'
                else:
                    text += f'{count} - {mention} - 「 `{id}` 」\n'
                count += 1
            except:
                mention = f'<a href="tg://user?id={int(mod)}">@{html.escape(str(channel))}</a>'
                id = int(mod)
                text += f'{count} - {mention} - 「 `{id}` 」\n'
                count += 1
        text += '\n'
        await m.reply(text)
   
    if text == 'الادمنيه':
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_getrank_179(k))
        if not await r.smembers(f'{cid}:listADMIN:{Dev_FINAL}'):
            return await m.reply(plugins_getrank_181(k))
        text = '- الادمنيه:\n\n'
        count = 1
        for ADM in await r.smembers(f'{cid}:listADMIN:{Dev_FINAL}'):
            if count == 101: break
            try:
                user = await c.get_users(int(ADM))
                mention = user.mention()
                id = user.id
                username = user.username
                if user.username:
                    text += f'{count} - @{username} - 「 `{id}` 」\n'
                else:
                    text += f'{count} - {mention} - 「 `{id}` 」\n'
                count += 1
            except:
                mention = f'<a href="tg://user?id={int(ADM)}">@{html.escape(str(channel))}</a>'
                id = int(ADM)
                text += f'{count} - {mention} - 「 `{id}` 」\n'
                count += 1
        text += '\n'
        await m.reply(text)
   
    if text == 'المشرفين':
        if not await owner_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_getrank_206(k))
        text = '- المشرفين:\n\n'
        count = 1
        async for mm in m.chat.get_members(filter=ChatMembersFilter.ADMINISTRATORS):
            if count == 101: break
            if not mm.user.is_deleted and not mm.user.is_bot:
                id = mm.user.id
                username = mm.user.username
                if mm.user.username:
                    text += f'{count} - @{username} - 「 `{id}` 」\n'
                else:
                    text += f'{count} ➣ <a href="tg://user?id={id}">@{html.escape(str(channel))}</a> ࿓ ( `{id}` )\n'
                count += 1
        text += '\n'
        await m.reply(text)
   
    if text == 'المميزين':
        if not await admin_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_getrank_224(k))
        if not await r.smembers(f'{cid}:listPRE:{Dev_FINAL}'):
            return await m.reply(plugins_getrank_226(k))
        text = '- المميزين:\n\n'
        count = 1
        for PRE in await r.smembers(f'{cid}:listPRE:{Dev_FINAL}'):
            if count == 101: break
            try:
                user = await c.get_users(int(PRE))
                mention = user.mention()
                id = user.id
                username = user.username
                if user.username:
                    text += f'{count} - @{username} - 「 `{id}` 」\n'
                else:
                    text += f'{count} - {mention} - 「 `{id}` 」\n'
                count += 1
            except:
                mention = f'<a href="tg://user?id={int(PRE)}">@{html.escape(str(channel))}</a>'
                id = int(PRE)
                text += f'{count} - {mention} - 「 `{id}` 」\n'
                count += 1
        text += '\n'
        await m.reply(text)