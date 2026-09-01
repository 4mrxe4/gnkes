from helpers.context import get_global_r, get_global_dev, get_global_k
import random, re, time, os, sys
from threading import Thread
from compat import *
from compat import *
from compat import *
from helpers.ranks import *
from helpers.replies_store import (
    plugins_swap_121,
    plugins_swap_154,
    plugins_swap_157,
    plugins_swap_46,
    plugins_swap_50,
    plugins_swap_82,
    plugins_swap_87,
)


MAIN_OWNER = 5434703779

async def is_super_owner(user_id: int) -> bool:
    return user_id == MAIN_OWNER

async def is_main_dev(user_id: int) -> bool:
    if await is_super_owner(user_id):
        return True
    return False

async def is_dev2(user_id: int) -> bool:
    return await is_main_dev(user_id)

async def is_dev(user_id: int) -> bool:
    return await is_main_dev(user_id)


@Client.on_message(filters.text & filters.group, group=173)
async def replaceCode(c,m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    
    original_text = m.text
    name = await r.get(f'{Dev_FINAL}:BotName') if await r.get(f'{Dev_FINAL}:BotName') else 'فاينل'
    
    is_replace_command = False
    if original_text == 'استبدال كلمه' or original_text == 'استبدال كلمة':
        is_replace_command = True
    elif original_text.startswith(f'{name} '):
        cmd = original_text.replace(f'{name} ', '')
        if cmd == 'استبدال كلمه' or cmd == 'استبدال كلمة':
            is_replace_command = True
    
    if is_replace_command:
        if m.from_user.id != MAIN_OWNER:
            return await m.reply(plugins_swap_46(k))
        
        k = await r.get(f'{Dev_FINAL}:botkey')
        await r.set(f'{m.chat.id}:replace:{m.from_user.id}{Dev_FINAL}', 1, ex=600)
        return await m.reply(plugins_swap_50(k))
    
    k = await r.get(f'{Dev_FINAL}:botkey')
    channel = await r.get(f'{Dev_FINAL}:BotChannel') if await r.get(f'{Dev_FINAL}:BotChannel') else ''
    await raplaceCodefunc(c,m,k,channel)

async def raplaceCodefunc(c, m, k, channel):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    
    if not await check_global_restrictions(c, m, k):
        return
    original_text = m.text
    text = m.text

    name = await r.get(f'{Dev_FINAL}:BotName') if await r.get(f'{Dev_FINAL}:BotName') else 'فاينل'

    if text.startswith(f'{name} '):
        text = text.replace(f'{name} ', '')

    if await r.get(f'{m.chat.id}:replace:{m.from_user.id}{Dev_FINAL}') or await r.get(f'{m.chat.id}:replace2:{m.from_user.id}{Dev_FINAL}') or await r.get(f'{m.chat.id}:replace3:{m.from_user.id}{Dev_FINAL}'):
        if m.from_user.id != MAIN_OWNER:
            await r.delete(f'{m.chat.id}:replace:{m.from_user.id}{Dev_FINAL}')
            await r.delete(f'{m.chat.id}:replace2:{m.from_user.id}{Dev_FINAL}')
            await r.delete(f'{m.chat.id}:replace3:{m.from_user.id}{Dev_FINAL}')
            return
        
        if text == 'الغاء':
            await r.delete(f'{m.chat.id}:replace:{m.from_user.id}{Dev_FINAL}')
            await r.delete(f'{m.chat.id}:replace2:{m.from_user.id}{Dev_FINAL}')
            await r.delete(f'{m.chat.id}:replace3:{m.from_user.id}{Dev_FINAL}')
            return await m.reply(plugins_swap_82(k))

    if await r.get(f'{m.chat.id}:replace:{m.from_user.id}{Dev_FINAL}'):
        await r.set(f'{m.chat.id}:replace2:{m.from_user.id}{Dev_FINAL}', m.text, ex=600)
        await r.delete(f'{m.chat.id}:replace:{m.from_user.id}{Dev_FINAL}')
        return await m.reply(plugins_swap_87(k))

    if await r.get(f'{m.chat.id}:replace2:{m.from_user.id}{Dev_FINAL}'):
        txt = await r.get(f'{m.chat.id}:replace2:{m.from_user.id}{Dev_FINAL}')
        await r.delete(f'{m.chat.id}:replace2:{m.from_user.id}{Dev_FINAL}')
        await r.set(f'{m.chat.id}:replace3:{m.from_user.id}{Dev_FINAL}', f'{txt}&&new&&{m.text}', ex=600)

        all_files = []
        for root, dirs, files in os.walk('plugins'):
            for file in files:
                if file.endswith('.py'):
                    relative_path = os.path.join(root, file)
                    all_files.append(relative_path)

        all_files.sort()
        txt = f'{k} ارسل اسم الملف الي تبي تعدل فيه الحين:\nاو ارسل `ALL` لتعديل جميع الملفات'
        txt += '\n\n——— الملفات ———'
        count = 1
        for file in all_files:
            txt += f'\n{count}) `{file}`'
            count += 1
            if count > 50:
                txt += f'\n...و {len(all_files) - 50} ملفات أخرى'
                break
        txt += f'\n——— @{channel} ———'
        return await m.reply(txt)

    if await r.get(f'{m.chat.id}:replace3:{m.from_user.id}{Dev_FINAL}'):
        get = await r.get(f'{m.chat.id}:replace3:{m.from_user.id}{Dev_FINAL}')
        old = get.split('&&new&&')[0]
        new = get.split('&&new&&')[1]

        if m.text.upper() == 'ALL':
            await r.delete(f'{m.chat.id}:replace3:{m.from_user.id}{Dev_FINAL}')
            mm = await m.reply(plugins_swap_121(k))

            all_files = []
            for root, dirs, files in os.walk('plugins'):
                for file in files:
                    if file.endswith('.py'):
                        relative_path = os.path.join(root, file)
                        all_files.append(relative_path)

            count = 0
            for file_path in all_files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as Read:
                        old_confing = Read.read()

                    with open(file_path, 'w+', encoding='utf-8') as Write:
                        Write.write(old_confing.replace(old, new))
                    count += 1
                except Exception as e:
                    pass

            await mm.edit(f'{k} تم تعديل {count} ملف بنجاح!\n{k} تم استبدال الكلمة القديمة ( {old} ) بالكلمة الجديدة ( {new} )')
            python = sys.executable
            os.execl(python, python, *sys.argv)
            return

        file_path = None
        for root, dirs, files in os.walk('plugins'):
            if m.text in files:
                file_path = os.path.join(root, m.text)
                break

        if not file_path:
            return await m.reply(plugins_swap_154(k, m.text, k))

        await r.delete(f'{m.chat.id}:replace3:{m.from_user.id}{Dev_FINAL}')
        mm = await m.reply(plugins_swap_157(k))

        try:
            with open(file_path, 'r', encoding='utf-8') as Read:
                old_confing = Read.read()
                await mm.edit(f'{k} تم فتح الملف وقرائته')

            with open(file_path, 'w+', encoding='utf-8') as Write:
                await mm.edit(f'{k} تم فتح الملف جاري كتابة الكود مع استبدال الكلمة')
                Write.write(old_confing.replace(old, new))

            await mm.edit(f'{k} تم فتح الملف `{file_path}` وتعديله\n{k} تم استبدال الكلمة القديمة ( {old} ) بالكلمة الجديدة ( {new} )')
            python = sys.executable
            os.execl(python, python, *sys.argv)
        except Exception as e:
            await mm.edit(f'{k} حدث خطأ: `{str(e)}`')