import html
from helpers.context import get_global_r, get_global_dev, get_global_k
r = get_global_r()
Dev_FINAL = get_global_dev()
k = get_global_k()

import re
import time
import pytz
from helpers.http import telegram_api_post
from random import choice as safe_choice
from datetime import datetime
from compat import *
from compat import *
from compat import *
from datetime import datetime
import settings
from helpers.ranks import *
from .buttons import *
from helpers.replies_store import (
    plugins_replies_1004,
    plugins_replies_1009,
    plugins_replies_1014,
    plugins_replies_1039,
    plugins_replies_1041,
    plugins_replies_1049,
    plugins_replies_1052,
    plugins_replies_1058,
    plugins_replies_1063,
    plugins_replies_1069,
    plugins_replies_1073,
    plugins_replies_1084,
    plugins_replies_1092,
    plugins_replies_1096,
    plugins_replies_1098,
    plugins_replies_1126,
    plugins_replies_1128,
    plugins_replies_1132,
    plugins_replies_1134,
    plugins_replies_1145,
    plugins_replies_1199,
    plugins_replies_1205,
    plugins_replies_1209,
    plugins_replies_1227,
    plugins_replies_1229,
    plugins_replies_1237,
    plugins_replies_1241,
    plugins_replies_1249,
    plugins_replies_1252,
    plugins_replies_1255,
    plugins_replies_1261,
    plugins_replies_1264,
    plugins_replies_1266,
    plugins_replies_1276,
    plugins_replies_1278,
    plugins_replies_1288,
    plugins_replies_1292,
    plugins_replies_1294,
    plugins_replies_1298,
    plugins_replies_1301,
    plugins_replies_1304,
    plugins_replies_1313,
    plugins_replies_1318,
    plugins_replies_1334,
    plugins_replies_1340,
    plugins_replies_1349,
    plugins_replies_1374,
    plugins_replies_1378,
    plugins_replies_1381,
    plugins_replies_1384,
    plugins_replies_1392,
    plugins_replies_1398,
    plugins_replies_1403,
    plugins_replies_1416,
    plugins_replies_1420,
    plugins_replies_1423,
    plugins_replies_1458,
    plugins_replies_1498,
    plugins_replies_1504,
    plugins_replies_1509,
    plugins_replies_1541,
    plugins_replies_1547,
    plugins_replies_1551,
    plugins_replies_1568,
    plugins_replies_1570,
    plugins_replies_1578,
    plugins_replies_1582,
    plugins_replies_1587,
    plugins_replies_1590,
    plugins_replies_1592,
    plugins_replies_1602,
    plugins_replies_1604,
    plugins_replies_1611,
    plugins_replies_1614,
    plugins_replies_1616,
    plugins_replies_1654,
    plugins_replies_1703,
    plugins_replies_1709,
    plugins_replies_1713,
    plugins_replies_1731,
    plugins_replies_1733,
    plugins_replies_1741,
    plugins_replies_1745,
    plugins_replies_1751,
    plugins_replies_1754,
    plugins_replies_1757,
    plugins_replies_1763,
    plugins_replies_1766,
    plugins_replies_1768,
    plugins_replies_1778,
    plugins_replies_1780,
    plugins_replies_1788,
    plugins_replies_1792,
    plugins_replies_1794,
    plugins_replies_1835,
    plugins_replies_1841,
    plugins_replies_1845,
    plugins_replies_1848,
    plugins_replies_1883,
    plugins_replies_1898,
    plugins_replies_1901,
    plugins_replies_1904,
    plugins_replies_1923,
    plugins_replies_1925,
    plugins_replies_1943,
    plugins_replies_1945,
    plugins_replies_1949,
    plugins_replies_1963,
    plugins_replies_1980,
    plugins_replies_1984,
    plugins_replies_1986,
    plugins_replies_1990,
    plugins_replies_1992,
    plugins_replies_224,
    plugins_replies_275,
    plugins_replies_280,
    plugins_replies_284,
    plugins_replies_309,
    plugins_replies_311,
    plugins_replies_315,
    plugins_replies_318,
    plugins_replies_321,
    plugins_replies_330,
    plugins_replies_335,
    plugins_replies_351,
    plugins_replies_357,
    plugins_replies_366,
    plugins_replies_391,
    plugins_replies_399,
    plugins_replies_403,
    plugins_replies_411,
    plugins_replies_416,
    plugins_replies_422,
    plugins_replies_426,
    plugins_replies_428,
    plugins_replies_432,
    plugins_replies_434,
    plugins_replies_438,
    plugins_replies_449,
    plugins_replies_459,
    plugins_replies_463,
    plugins_replies_465,
    plugins_replies_469,
    plugins_replies_472,
    plugins_replies_765,
    plugins_replies_802,
    plugins_replies_808,
    plugins_replies_813,
    plugins_replies_845,
    plugins_replies_850,
    plugins_replies_854,
    plugins_replies_872,
    plugins_replies_874,
    plugins_replies_882,
    plugins_replies_885,
    plugins_replies_890,
    plugins_replies_894,
    plugins_replies_905,
    plugins_replies_912,
    plugins_replies_916,
    plugins_replies_918,
    plugins_replies_953,
)

try:
    from plugins.games.addgame import get_custom_game_meta, get_custom_game_data, get_button_game_data
except ImportError:
    pass

try:
    from plugins.games.devgames import get_public_game_meta, get_public_game_data, get_public_button_game_data
except ImportError:
    pass

try:
    from helpers.emoji import get_custom_emoji_mappings, get_replacement_mappings
except ImportError:
    pass

try:
    from helpers.gender import get_gender_map
except ImportError:
    pass

def process_mentions_in_text(text, user, reply_to_user=None):
    if not text or not user:
        return text
    
    pattern = r'\(([^)]+)\)'
    
    def replace_match(match):
        content = match.group(1).strip()
        real_name = None
        user_id = None
        username = None
        parts = content.split()
        
        for part in parts:
            if part.isdigit():
                user_id = part
                break
        
        for part in parts:
            if part.startswith('@'):
                username = part.lstrip('@')
                break
        
        for part in parts:
            if part != user_id and not part.startswith('@'):
                real_name = part
                break
        
        if not real_name:
            real_name = content
        
        if real_name and user_id:
            try:
                user_id_int = int(user_id)
                if user_id_int > 0:
                    return f'<a href="tg://user?id={user_id}">{html.escape(str(real_name))}</a>'
                else:
                    return f'({content})'
            except ValueError:
                return f'({content})'
        
        elif real_name and username:
            return html.escape(real_name)
        
        elif username and not real_name:
            return html.escape(username)
        
        else:
            return f'({content})'
    
    result = re.sub(pattern, replace_match, text)
    return result


BUTTONS_DEFINITIONS = {
    "replies": {
        "name": "أزرار الردود",
        "buttons": [
            {"id": "inline_global_btn", "default": "اضف رد انلاين عام"},
        ]
    }
}

register_buttons(BUTTONS_DEFINITIONS)

async def refresh_dynamic_buttons(chat_id=None):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    
    if "replies" not in ALL_BUTTONS:
        ALL_BUTTONS["replies"] = {"name": "أزرار الردود", "buttons": []}
    
    global_filters = await r.smembers(f'Global:FiltersList:{Dev_FINAL}')
    
    for filter_key in global_filters:
        if isinstance(filter_key, bytes):
            filter_key = filter_key.decode('utf-8')
        
        filter_data = await r.get(f'Global:{filter_key}:filter:{Dev_FINAL}')
        if filter_data:
            if isinstance(filter_data, bytes):
                filter_data = filter_data.decode('utf-8')
            
            if filter_data.startswith('type=inline&'):
                import urllib.parse
                parsed = urllib.parse.parse_qs(filter_data)
                btn_text = parsed.get('btn', [filter_key])[0]
                
                btn_id = f"inline_global_{filter_key}"
                btn_exists = False
                for btn in ALL_BUTTONS["replies"]["buttons"]:
                    if btn["id"] == btn_id:
                        btn_exists = True
                        break
                
                if not btn_exists:
                    ALL_BUTTONS["replies"]["buttons"].append({
                        "id": btn_id,
                        "default": btn_text,
                        "dynamic": True,
                        "word": filter_key
                    })
    
    if chat_id:
        local_filters = await r.smembers(f'{chat_id}:FiltersList:{Dev_FINAL}')
        for filter_key in local_filters:
            if isinstance(filter_key, bytes):
                filter_key = filter_key.decode('utf-8')
            
            filter_data = await r.get(f'{filter_key}:filter:{Dev_FINAL}{chat_id}')
            if filter_data:
                if isinstance(filter_data, bytes):
                    filter_data = filter_data.decode('utf-8')
                
                if filter_data.startswith('type=inline&'):
                    import urllib.parse
                    parsed = urllib.parse.parse_qs(filter_data)
                    btn_text = parsed.get('btn', [filter_key])[0]
                    
                    btn_id = f"inline_local_{filter_key}"
                    btn_exists = False
                    for btn in ALL_BUTTONS["replies"]["buttons"]:
                        if btn["id"] == btn_id:
                            btn_exists = True
                            break
                    
                    if not btn_exists:
                        ALL_BUTTONS["replies"]["buttons"].append({
                            "id": btn_id,
                            "default": btn_text,
                            "dynamic": True,
                            "word": filter_key
                        })
    
    return True

async def is_user_adding(user_id, chat_id):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    keys = [
        f'{chat_id}:addFilter:{user_id}{Dev_FINAL}',
        f'{chat_id}:addFilter2:{user_id}{Dev_FINAL}',
        f'{chat_id}:addInlineStep:{user_id}{Dev_FINAL}',
        f'{chat_id}:addFilterM:{user_id}{Dev_FINAL}',
        f'{chat_id}:addFilterM2:{user_id}{Dev_FINAL}',
        f'{chat_id}:addFilterS:{user_id}{Dev_FINAL}',
        f'{chat_id}:addFilterS2:{user_id}{Dev_FINAL}',
        f'{chat_id}:addFilterG:{user_id}{Dev_FINAL}',
        f'{chat_id}:addFilterG2:{user_id}{Dev_FINAL}',
        f'{chat_id}:addInlineStepGlobal:{user_id}{Dev_FINAL}',
        f'{chat_id}:addFilterGM:{user_id}{Dev_FINAL}',
        f'{chat_id}:addFilterGM2:{user_id}{Dev_FINAL}',
        f'{chat_id}:addFilterGS:{user_id}{Dev_FINAL}',
        f'{chat_id}:addFilterGS2:{user_id}{Dev_FINAL}',
        f'{chat_id}:addFilterMM:{user_id}{Dev_FINAL}',
    ]
    for key in keys:
        if await r.get(key):
            return True
    return False

@Client.on_message(filters.group & ~filters.bot, group=-221)
async def normal_reply_handler(c, m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    k = await r.get(f'{Dev_FINAL}:botkey')
    await normal_reply(c, m, k)

async def normal_reply(c, m, k):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if not await check_global_restrictions(c, m, k, caller='reply'):
        return

    text = m.text

    if await r.get(f'{m.chat.id}:addFilter2:{m.from_user.id}{Dev_FINAL}') and (await mod_pls(m.from_user.id, m.chat.id) or await fake_rank_pls(m.from_user.id, m.chat.id, 'replies')):
        key = await r.get(f'{m.chat.id}:addFilter2:{m.from_user.id}{Dev_FINAL}')
        await r.delete(f'{m.chat.id}:addFilter2:{m.from_user.id}{Dev_FINAL}')

        if m.text and m.text == 'الغاء':
            return await m.reply(plugins_replies_224(k))

        TIME_ZONE = "Asia/Riyadh"
        ZONE = pytz.timezone(TIME_ZONE)
        TIME = datetime.now(ZONE)
        date = TIME.strftime("%d/%m/%Y %I:%M:%S %p")

        if m.text:
            await r.set(f'{key}:filter:{Dev_FINAL}{m.chat.id}', f'type=text&text={m.html}')
            await r.set(f'{key}:filtertype:{m.chat.id}{Dev_FINAL}', 'نص')
        elif m.photo:
            photo = m.photo.file_id
            caption = m.html if m.caption else 'None'
            await r.set(f'{key}:filter:{Dev_FINAL}{m.chat.id}', f'type=photo&photo={photo}&caption={caption}')
            await r.set(f'{key}:filtertype:{m.chat.id}{Dev_FINAL}', 'صوره')
        elif m.video:
            video = m.video.file_id
            caption = m.html if m.caption else 'None'
            await r.set(f'{key}:filter:{Dev_FINAL}{m.chat.id}', f'type=video&video={video}&caption={caption}')
            await r.set(f'{key}:filtertype:{m.chat.id}{Dev_FINAL}', 'فيديو')
        elif m.animation:
            anim = m.animation.file_id
            caption = m.html if m.caption else 'None'
            await r.set(f'{key}:filter:{Dev_FINAL}{m.chat.id}', f'type=animation&animation={anim}&caption={caption}')
            await r.set(f'{key}:filtertype:{m.chat.id}{Dev_FINAL}', 'متحركه')
        elif m.audio:
            aud = m.audio.file_id
            caption = m.html if m.caption else 'None'
            await r.set(f'{key}:filter:{Dev_FINAL}{m.chat.id}', f'type=audio&audio={aud}&caption={caption}')
            await r.set(f'{key}:filtertype:{m.chat.id}{Dev_FINAL}', 'صوت')
        elif m.voice:
            voice = m.voice.file_id
            caption = m.html if m.caption else 'None'
            await r.set(f'{key}:filter:{Dev_FINAL}{m.chat.id}', f'type=voice&voice={voice}&caption={caption}')
            await r.set(f'{key}:filtertype:{m.chat.id}{Dev_FINAL}', 'بصمه')
        elif m.document:
            doc = m.document.file_id
            caption = m.html if m.caption else 'None'
            await r.set(f'{key}:filter:{Dev_FINAL}{m.chat.id}', f'type=doc&doc={doc}&caption={caption}')
            await r.set(f'{key}:filtertype:{m.chat.id}{Dev_FINAL}', 'ملف')
        elif m.sticker:
            stic = m.sticker.file_id
            await r.set(f'{key}:filter:{Dev_FINAL}{m.chat.id}', f'type=sticker&sticker={stic}')
            await r.set(f'{key}:filtertype:{m.chat.id}{Dev_FINAL}', 'ستيكر')
        else:
            return

        await r.set(f'{key}:filterInfo:{m.chat.id}{Dev_FINAL}', f'by={m.from_user.id}&date={date}')
        await r.sadd(f'{m.chat.id}:FiltersList:{Dev_FINAL}', key)
        
        await refresh_dynamic_buttons(m.chat.id)
        return await m.reply(plugins_replies_275(key), parse_mode=ParseMode.HTML)

    if await r.get(f'{m.chat.id}:addFilter:{m.from_user.id}{Dev_FINAL}'):
        if text == 'الغاء':
            await r.delete(f'{m.chat.id}:addFilter:{m.from_user.id}{Dev_FINAL}')
            return await m.reply(plugins_replies_280(k))

        await r.set(f'{m.chat.id}:addFilter2:{m.from_user.id}{Dev_FINAL}', m.text)
        await r.delete(f'{m.chat.id}:addFilter:{m.from_user.id}{Dev_FINAL}')
        return await m.reply(
            plugins_replies_284(k, k),
            parse_mode=ParseMode.MARKDOWN
        )

    if not text: return

    name = await r.get(f'{Dev_FINAL}:BotName')
    if name and text.startswith(f'{name} '):
        text = text.replace(f'{name} ', '')

    if await r.get(f'{m.chat.id}:Custom:{m.chat.id}{Dev_FINAL}&text={text}'):
        text = await r.get(f'{m.chat.id}:Custom:{m.chat.id}{Dev_FINAL}&text={text}')
    if await r.get(f'Custom:{Dev_FINAL}&text={text}'):
        text = await r.get(f'Custom:{Dev_FINAL}&text={text}')

    if text == 'اضف رد' and not await r.get(f'{m.chat.id}:addFilter:{m.from_user.id}{Dev_FINAL}') and not await r.get(f'{m.chat.id}:addFilter2:{m.from_user.id}{Dev_FINAL}'):
        if not (await mod_pls(m.from_user.id, m.chat.id) or await fake_rank_pls(m.from_user.id, m.chat.id, 'replies')):
            return await m.reply(plugins_replies_309(k))
        await r.set(f'{m.chat.id}:addFilter:{m.from_user.id}{Dev_FINAL}', 1)
        return await m.reply(plugins_replies_311(k))

    if text == 'اضف رد انلاين':
        if not await gowner_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_replies_315(k))
        
        if await r.get(f'{m.chat.id}:addInlineStep:{m.from_user.id}{Dev_FINAL}'):
            return await m.reply(plugins_replies_318(k))
        
        await r.set(f'{m.chat.id}:addInlineStep:{m.from_user.id}{Dev_FINAL}', "1")
        return await m.reply(plugins_replies_321(k))

    step = await r.get(f'{m.chat.id}:addInlineStep:{m.from_user.id}{Dev_FINAL}')
    if step and await gowner_pls(m.from_user.id, m.chat.id):
        if text == 'الغاء':
            await r.delete(f'{m.chat.id}:addInlineStep:{m.from_user.id}{Dev_FINAL}')
            await r.delete(f'{m.chat.id}:addInlineWord:{m.from_user.id}{Dev_FINAL}')
            await r.delete(f'{m.chat.id}:addInlineText:{m.from_user.id}{Dev_FINAL}')
            await r.delete(f'{m.chat.id}:addInlineBttn:{m.from_user.id}{Dev_FINAL}')
            return await m.reply(plugins_replies_330(k))
        
        if step == "1":
            await r.set(f'{m.chat.id}:addInlineWord:{m.from_user.id}{Dev_FINAL}', m.text)
            await r.set(f'{m.chat.id}:addInlineStep:{m.from_user.id}{Dev_FINAL}', "2")
            return await m.reply(
                plugins_replies_335(k, k),
                parse_mode=ParseMode.MARKDOWN
            )
        
        elif step == "2":
            await r.set(f'{m.chat.id}:addInlineText:{m.from_user.id}{Dev_FINAL}', m.html)
            await r.set(f'{m.chat.id}:addInlineStep:{m.from_user.id}{Dev_FINAL}', "3")
            word = await r.get(f'{m.chat.id}:addInlineWord:{m.from_user.id}{Dev_FINAL}')
            return await m.reply(plugins_replies_351(k, word), parse_mode=ParseMode.HTML)
        
        elif step == "3":
            await r.set(f'{m.chat.id}:addInlineBttn:{m.from_user.id}{Dev_FINAL}', m.text)
            await r.set(f'{m.chat.id}:addInlineStep:{m.from_user.id}{Dev_FINAL}', "4")
            word = await r.get(f'{m.chat.id}:addInlineWord:{m.from_user.id}{Dev_FINAL}')
            return await m.reply(plugins_replies_357(k, word), parse_mode=ParseMode.HTML)
        
        elif step == "4":
            word = await r.get(f'{m.chat.id}:addInlineWord:{m.from_user.id}{Dev_FINAL}')
            rep_text = await r.get(f'{m.chat.id}:addInlineText:{m.from_user.id}{Dev_FINAL}')
            bttn_text = await r.get(f'{m.chat.id}:addInlineBttn:{m.from_user.id}{Dev_FINAL}')
            bttn_url = m.text
            
            if not bttn_url.startswith(('http://', 'https://')):
                return await m.reply(plugins_replies_366(k))
            
            import urllib.parse
            save_data = urllib.parse.urlencode({'type': 'inline', 'text': rep_text, 'btn': bttn_text, 'url': bttn_url})
            
            TIME_ZONE = "Asia/Riyadh"
            ZONE = pytz.timezone(TIME_ZONE)
            TIME = datetime.now(ZONE)
            date = TIME.strftime("%d/%m/%Y %I:%M:%S %p")
            
            await r.set(f'{word}:filter:{Dev_FINAL}{m.chat.id}', save_data)
            await r.set(f'{word}:filtertype:{m.chat.id}{Dev_FINAL}', 'انلاين')
            await r.set(f'{word}:filterInfo:{m.chat.id}{Dev_FINAL}', f'by={m.from_user.id}&date={date}')
            await r.sadd(f'{m.chat.id}:FiltersList:{Dev_FINAL}', word)
            
            btn_id = f"inline_local_{word}"
            await r.set(f'btn_id:inline_local:{word}:{m.chat.id}', btn_id)
            await r.set(f'btn_name:replies:{btn_id}:global', bttn_text)
            
            await r.delete(f'{m.chat.id}:addInlineStep:{m.from_user.id}{Dev_FINAL}')
            await r.delete(f'{m.chat.id}:addInlineWord:{m.from_user.id}{Dev_FINAL}')
            await r.delete(f'{m.chat.id}:addInlineText:{m.from_user.id}{Dev_FINAL}')
            await r.delete(f'{m.chat.id}:addInlineBttn:{m.from_user.id}{Dev_FINAL}')
            
            await refresh_dynamic_buttons(m.chat.id)
            return await m.reply(plugins_replies_391(k, word), parse_mode=ParseMode.HTML)
        
    if await is_user_adding(m.from_user.id, m.chat.id):
        return

    if await r.get(f'{m.chat.id}:delFilter:{m.from_user.id}{Dev_FINAL}'):
        if text == 'الغاء':
            await r.delete(f'{m.chat.id}:delFilter:{m.from_user.id}{Dev_FINAL}')
            return await m.reply(plugins_replies_399(k))
        if await mod_pls(m.from_user.id, m.chat.id):
            if not await r.get(f'{m.text}:filterInfo:{m.chat.id}{Dev_FINAL}'):
                await r.delete(f'{m.chat.id}:delFilter:{m.from_user.id}{Dev_FINAL}')
                return await m.reply(plugins_replies_403(k))
            await r.delete(f'{m.text}:filter:{Dev_FINAL}{m.chat.id}')
            await r.delete(f'{m.text}:filtertype:{m.chat.id}{Dev_FINAL}')
            await r.delete(f'{m.text}:filterInfo:{m.chat.id}{Dev_FINAL}')
            await r.srem(f'{m.chat.id}:FiltersList:{Dev_FINAL}', m.text)
            await r.delete(f'{m.chat.id}:delFilter:{m.from_user.id}{Dev_FINAL}')
            
            await refresh_dynamic_buttons(m.chat.id)
            return await m.reply(plugins_replies_411(m.text, k))

    if text.startswith('الرد ') and len(m.text.split()) > 1 and (await mod_pls(m.from_user.id, m.chat.id) or await fake_rank_pls(m.from_user.id, m.chat.id, 'replies')):
        reply = m.text.split(None, 1)[1]
        if not await r.get(f'{reply}:filterInfo:{m.chat.id}{Dev_FINAL}'):
            return await m.reply(plugins_replies_416(k))
        get = await r.get(f'{reply}:filterInfo:{m.chat.id}{Dev_FINAL}')
        split = get.split('by=')[1]
        by = split.split('&date=')[0]
        date = split.split('&date=')[1]
        type = await r.get(f'{reply}:filtertype:{m.chat.id}{Dev_FINAL}')
        return await m.reply(plugins_replies_422(k, by, html.escape(str(reply)), k, date, k, type))

    if text == 'تعطيل الردود' and (await mod_pls(m.from_user.id, m.chat.id) or await fake_rank_pls(m.from_user.id, m.chat.id, 'replies')):
        if await r.get(f'{m.chat.id}:lock_filter:{Dev_FINAL}'):
            return await m.reply(plugins_replies_426(k, m.from_user.mention(), k), parse_mode=ParseMode.HTML)
        await r.set(f'{m.chat.id}:lock_filter:{Dev_FINAL}', 1)
        return await m.reply(plugins_replies_428(k, m.from_user.mention(), k), parse_mode=ParseMode.HTML)

    if text == 'تفعيل الردود' and (await mod_pls(m.from_user.id, m.chat.id) or await fake_rank_pls(m.from_user.id, m.chat.id, 'replies')):
        if not await r.get(f'{m.chat.id}:lock_filter:{Dev_FINAL}'):
            return await m.reply(plugins_replies_432(k, m.from_user.mention(), k), parse_mode=ParseMode.HTML)
        await r.delete(f'{m.chat.id}:lock_filter:{Dev_FINAL}')
        return await m.reply(plugins_replies_434(k, m.from_user.mention(), k), parse_mode=ParseMode.HTML)

    if text == 'الردود' and (await mod_pls(m.from_user.id, m.chat.id) or await fake_rank_pls(m.from_user.id, m.chat.id, 'replies')):
        if not await r.smembers(f'{m.chat.id}:FiltersList:{Dev_FINAL}'):
            return await m.reply(plugins_replies_438(k))
        msg = 'ردود المجموعه:\n'
        count = 1
        for reply in await r.smembers(f'{m.chat.id}:FiltersList:{Dev_FINAL}'):
            type = await r.get(f'{reply}:filtertype:{m.chat.id}{Dev_FINAL}')
            msg += f'\n{count} - ( {reply} )  ( {type} )'
            count += 1
        return await m.reply(msg, disable_web_page_preview=True, parse_mode=ParseMode.HTML)

    if text == 'مسح الردود' and (await mod_pls(m.from_user.id, m.chat.id) or await fake_rank_pls(m.from_user.id, m.chat.id, 'replies')):
        if not await r.smembers(f'{m.chat.id}:FiltersList:{Dev_FINAL}'):
            return await m.reply(plugins_replies_449(k))
        total = 0
        for reply in await r.smembers(f'{m.chat.id}:FiltersList:{Dev_FINAL}'):
            await r.delete(f'{reply}:filter:{Dev_FINAL}{m.chat.id}')
            await r.delete(f'{reply}:filtertype:{m.chat.id}{Dev_FINAL}')
            await r.delete(f'{reply}:filterInfo:{m.chat.id}{Dev_FINAL}')
            await r.srem(f'{m.chat.id}:FiltersList:{Dev_FINAL}', reply)
            total += 1
        
        await refresh_dynamic_buttons(m.chat.id)
        return await m.reply(plugins_replies_459(k, total))

    if text == 'مسح رد' and not await r.get(f'{m.chat.id}:delFilter:{m.from_user.id}{Dev_FINAL}'):
        if not (await mod_pls(m.from_user.id, m.chat.id) or await fake_rank_pls(m.from_user.id, m.chat.id, 'replies')):
            return await m.reply(plugins_replies_463(k))
        await r.set(f'{m.chat.id}:delFilter:{m.from_user.id}{Dev_FINAL}', 1)
        return await m.reply(plugins_replies_465(k, k), parse_mode=ParseMode.HTML)

    if text == 'كشف الرد' or text == 'كشف الامر':
        if not await gowner_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_replies_469(k))
        
        if not m.reply_to_message or not m.reply_to_message.text:
            return await m.reply(plugins_replies_472(k))
        
        word = m.reply_to_message.text
        result = f'{k} الكلمة 「{word}」 مضافة لـ↤\n\n'
        found = False
        
        if await r.get(f'{word}:filterInfo:{m.chat.id}{Dev_FINAL}'):
            found = True
            type_f = await r.get(f'{word}:filtertype:{m.chat.id}{Dev_FINAL}')
            result += f'- 「 ردود عادية 」  \n'
            result += f'{k} نوع↤ {type_f}\n'
            result += f'{k} استخدم الامر ↤ مسح رد\n\n'
        
        filter_data = await r.get(f'{word}:filter:{Dev_FINAL}{m.chat.id}')
        if filter_data and filter_data.startswith('type=inline&'):
            found = True
            result += f'- 「 ردود انلاين 」  \n'
            result += f'{k} استخدم الامر ↤ مسح رد انلاين\n\n'
        
        if await r.get(f'{word}:multiFilter:{m.chat.id}{Dev_FINAL}'):
            found = True
            count = len(await r.smembers(f'{word}:multifilter:{m.chat.id}{Dev_FINAL}'))
            result += f'- 「 ردود متعدده 」  \n'
            result += f'{k} عدد الاجوبة: {count}\n'
            result += f'{k} استخدم الامر ↤ مسح رد متعدد\n\n'
        
        if await r.get(f'{word}:specialfilterInfo:{m.chat.id}{Dev_FINAL}'):
            found = True
            type_f = await r.get(f'{word}:specialfiltertype:{m.chat.id}{Dev_FINAL}')
            result += f'- 「 ردود مميزه 」  \n'
            result += f'{k} نوع↤ {type_f}\n'
            result += f'{k} استخدم الامر ↤ مسح رد مميز\n\n'
        
        if await r.get(f'{word}:filterMEM:{Dev_FINAL}{m.chat.id}'):
            found = True
            by = await r.get(f'{word}:filterMEM:{Dev_FINAL}{m.chat.id}')
            try:
                user = await c.get_users(int(by))
                mention = user.mention()
            except:
                mention = f'<a href="tg://user?id={by}">{html.escape(str(by))}</a>'
            result += f'- 「 ردود الاعضاء 」 \n'
            result += f'{k} مضافة بواسطة↤ {mention}\n'
            result += f'{k} استخدم الامر ↤ حذف رده\n\n'
        
        if await r.get(f'Global:{word}:filterInfo:{Dev_FINAL}'):
            found = True
            type_f = await r.get(f'Global:{word}:filtertype:{Dev_FINAL}')
            result += f'- 「 ردود عامه (عادية) 」 \n'
            result += f'{k} نوع↤ {type_f}\n'
            result += f'{k} استخدم الامر ↤ مسح رد عام\n\n'
        
        global_filter_data = await r.get(f'Global:{word}:filter:{Dev_FINAL}')
        if global_filter_data and global_filter_data.startswith('type=inline&'):
            found = True
            result += f'- 「 ردود انلاين عامه 」 \n'
            result += f'{k} استخدم الامر ↤ مسح رد انلاين عام\n\n'
        
        if await r.get(f'Global:{word}:multiFilter:{Dev_FINAL}'):
            found = True
            count = len(await r.smembers(f'Global:{word}:multifilter:{Dev_FINAL}'))
            result += f'- 「 ردود متعدده عامه 」  \n'
            result += f'{k} عدد الاجوبة: {count}\n'
            result += f'{k} استخدم الامر ↤ مسح رد متعدد عام\n\n'
        
        if await r.get(f'Global:{word}:specialfilterInfo:{Dev_FINAL}'):
            found = True
            type_f = await r.get(f'Global:{word}:specialfiltertype:{Dev_FINAL}')
            result += f'- 「 ردود مميزه عامه 」  \n'
            result += f'{k} نوع↤ {type_f}\n'
            result += f'{k} استخدم الامر ↤ مسح رد مميز عام\n\n'
        
        try:
            custom_game_meta = await get_custom_game_meta(word)
            if custom_game_meta:
                found = True
                game_data = await get_custom_game_data(word)
                media_count = len(game_data.get("media", [])) if game_data else 0
                result += f'- 「 لعبه مخصصه 」 \n'
                result += f'{k} النوع↤ {custom_game_meta.get("type", "غير معروف")}\n'
                result += f'{k} عدد المحتوى↤ {media_count}\n'
                if custom_game_meta.get("has_questions", False):
                    result += f'{k} يحتوي على اسئلة\n'
                if custom_game_meta.get("has_money", False):
                    result += f'{k} يحتوي على فلوس\n'
                result += f'{k} استخدم الامر ↤ مسح لعبه\n\n'
        except Exception as e:
            pass
        
        try:
            button_game_data = await get_button_game_data(word)
            if button_game_data:
                found = True
                questions_count = len(button_game_data.get("questions", []))
                result += f'- 「 لعبه ازرار مخصصه 」 \n'
                result += f'{k} النوع↤ {button_game_data.get("type", "غير معروف")}\n'
                result += f'{k} عدد الاسئلة↤ {questions_count}\n'
                if button_game_data.get("has_money", False):
                    result += f'{k} يحتوي على فلوس\n'
                result += f'{k} استخدم الامر ↤ مسح لعبه\n\n'
        except Exception as e:
            pass
        
        try:
            public_game_meta = await get_public_game_meta(word)
            if public_game_meta:
                found = True
                game_data = await get_public_game_data(word)
                media_count = len(game_data.get("media", [])) if game_data else 0
                result += f'- 「 لعبه عامه 」 \n'
                result += f'{k} النوع↤ {public_game_meta.get("type", "غير معروف")}\n'
                result += f'{k} عدد المحتوى↤ {media_count}\n'
                if public_game_meta.get("has_questions", False):
                    result += f'{k} يحتوي على اسئلة\n'
                if public_game_meta.get("has_money", False):
                    result += f'{k} يحتوي على فلوس\n'
                result += f'{k} استخدم الامر ↤ مسح لعبه عام\n\n'
        except Exception as e:
            pass
        
        try:
            public_button_data = await get_public_button_game_data(word)
            if public_button_data:
                found = True
                questions_count = len(public_button_data.get("questions", []))
                result += f'- 「 لعبه ازرار عامه 」 \n'
                result += f'{k} النوع↤ {public_button_data.get("type", "غير معروف")}\n'
                result += f'{k} عدد الاسئلة↤ {questions_count}\n'
                if public_button_data.get("has_money", False):
                    result += f'{k} يحتوي على فلوس\n'
                result += f'{k} استخدم الامر ↤ مسح لعبه عام\n\n'
        except Exception as e:
            pass
        
        if await r.get(f'{m.chat.id}:Custom:{m.chat.id}{Dev_FINAL}&text={word}'):
            found = True
            old_cmd = await r.get(f'{m.chat.id}:Custom:{m.chat.id}{Dev_FINAL}&text={word}')
            result += f'- 「 اوامر مضافه 」 \n'
            result += f'{k} الامر القديم↤ {old_cmd}\n'
            result += f'{k} استخدم الامر ↤ مسح امر\n\n'
        
        if await r.get(f'Custom:{Dev_FINAL}&text={word}'):
            found = True
            old_cmd = await r.get(f'Custom:{Dev_FINAL}&text={word}')
            result += f'- 「 اوامر عامه مضافه 」 \n'
            result += f'{k} الامر القديم↤ {old_cmd}\n'
            result += f'{k} استخدم الامر ↤ مسح امر عام\n\n'
        
        try:
            emoji_mappings = await get_custom_emoji_mappings(Dev_FINAL)
            if word in emoji_mappings:
                found = True
                data = emoji_mappings[word]
                if isinstance(data, dict):
                    new_text = data.get("new_text", "")
                    emoji_id = data.get("custom_emoji_id", "")
                    position = "بداية" if data.get("position", "end") == "start" else "نهاية"
                    if emoji_id:
                        result += f'- 「 ايموجي مميز مضاف 」 \n'
                        result += f'{k} النص الجديد↤ {new_text}\n'
                        result += f'{k} موقع الايموجي↤ {position}\n'
                        result += f'{k} استخدم الامر ↤ حذف ايموجي {word}\n\n'
                    else:
                        result += f'- 「 ايموجي مضاف 」 \n'
                        result += f'{k} النص الجديد↤ {new_text}\n'
                        result += f'{k} موقع الايموجي↤ {position}\n'
                        result += f'{k} استخدم الامر ↤ حذف ايموجي {word}\n\n'
        except Exception as e:
            pass
        
        try:
            replacement_mappings = await get_replacement_mappings(Dev_FINAL)
            if word in replacement_mappings:
                found = True
                data = replacement_mappings[word]
                replace_type = data.get("replace_type", "text")
                replacement = data.get("replacement_text", "")
                emoji_char = data.get("emoji_char", "")
                custom_emoji_id = data.get("custom_emoji_id", "")
                
                type_label = {
                    "emoji": "إيموجي مميز فقط",
                    "text": "نص فقط",
                    "emoji_text": "إيموجي + نص"
                }.get(replace_type, "نص")
                
                if custom_emoji_id and emoji_char:
                    emoji_tag = f'<tg-emoji emoji-id="{custom_emoji_id}">{emoji_char}</tg-emoji>'
                    if replacement:
                        result += f'- 「 كلمه مستبدله (ايموجي+نص) 」 \n'
                        result += f'{k} النص البديل↤ {emoji_tag} {replacement}\n'
                    else:
                        result += f'- 「 كلمه مستبدله (ايموجي) 」 \n'
                        result += f'{k} الايموجي↤ {emoji_tag}\n'
                else:
                    result += f'- 「 كلمه مستبدله (نص) 」 \n'
                    result += f'{k} النص البديل↤ {replacement}\n'
                
                result += f'{k} النوع↤ {type_label}\n'
                result += f'{k} استخدم الامر ↤ حذف استبدال {word}\n\n'
        except Exception as e:
            pass
        
        try:
            gender_map = await get_gender_map(Dev_FINAL)
            if word.lower() in gender_map:
                found = True
                female_word = gender_map[word.lower()]
                result += f'- 「 كلمه جنس 」 \n'
                result += f'{k} المذكر↤ {word}\n'
                result += f'{k} المؤنث↤ {female_word}\n'
                result += f'{k} استخدم الامر ↤ حذف كلمة جنس {word}\n\n'
        except Exception as e:
            pass
        
        try:
            btn_found = False
            btn_info = ""
            
            all_buttons = await get_all_buttons_with_dynamic()
            for module_id, module_data in all_buttons.items():
                if module_id == "replies":
                    for btn in module_data.get("buttons", []):
                        if btn.get("default") == word or btn.get("word") == word:
                            btn_id = btn.get("id")
                            if btn_id:
                                btn_found = True
                                btn_info += f'{k} معرف الزر↤ {btn_id}\n'
                                custom_name = await get_button_custom("replies", btn_id)
                                btn_info += f'{k} الاسم الحالي↤ {custom_name or word}\n'
                                break
                    if btn_found:
                        break
            
            if not btn_found:
                btn_id = f"inline_global_{word}"
                custom_name = await get_button_custom("replies", btn_id)
                if custom_name:
                    btn_found = True
                    btn_info += f'{k} معرف الزر↤ {btn_id}\n'
                    btn_info += f'{k} الاسم الحالي↤ {custom_name}\n'
            
            if not btn_found:
                btn_id = f"inline_local_{word}"
                custom_name = await get_button_custom("replies", btn_id)
                if custom_name:
                    btn_found = True
                    btn_info += f'{k} معرف الزر↤ {btn_id}\n'
                    btn_info += f'{k} الاسم الحالي↤ {custom_name}\n'
            
            if not btn_found:
                btn_id = f"inline_member_{word}"
                custom_name = await get_button_custom("replies", btn_id)
                if custom_name:
                    btn_found = True
                    btn_info += f'{k} معرف الزر↤ {btn_id}\n'
                    btn_info += f'{k} الاسم الحالي↤ {custom_name}\n'
            
            if not btn_found:
                btn_id = f"btn_text_{word}"
                custom_name = await get_button_custom("replies", btn_id)
                if custom_name:
                    btn_found = True
                    btn_info += f'{k} معرف الزر↤ {btn_id}\n'
                    btn_info += f'{k} الاسم الحالي↤ {custom_name}\n'
            
            if btn_found:
                found = True
                color = await get_button_color("replies", btn_id) or "default"
                emoji_id = await get_button_emoji("replies", btn_id)
                emoji_char = await get_button_emoji_char("replies", btn_id)
                
                color_names = {"primary": "ازرق", "success": "اخضر", "danger": "احمر", "default": "شفاف"}
                result += f'- 「 زر معدل 」 \n'
                result += btn_info
                result += f'{k} اللون↤ {color_names.get(color, "شفاف")}\n'
                if emoji_id and emoji_char:
                    result += f'{k} الايموجي↤ <tg-emoji emoji-id="{emoji_id}">{emoji_char}</tg-emoji>\n'
                result += f'{k} استخدم الامر ↤ تعديل زر (واختيار هذا الاسم)\n\n'
        except Exception as e:
            pass
        
        lock_key = f"{Dev_FINAL}locks-{m.chat.id}"
        if await r.hexists(lock_key, word):
            found = True
            rank_value = await r.hget(lock_key, word)
            rank_map = {0: "مالك اساسي", 1: "مالك", 2: "مدير", 3: "ادمن", 4: "مميز"}
            rank_name = rank_map.get(int(rank_value), "غير معروف")
            result += f'- 「 اوامر مقفوله 」 \n'
            result += f'{k} متاح لـ↤ {rank_name}\n'
            result += f'{k} استخدم الامر ↤ فتح امر\n\n'
        
        if not found:
            return await m.reply(plugins_replies_765(k, word))
        else:
            return await m.reply(result, disable_web_page_preview=True, parse_mode=ParseMode.HTML)
        
    if not await r.get(f'{m.chat.id}:lock_filter:{Dev_FINAL}'):
        for reply in await r.smembers(f'{m.chat.id}:FiltersList:{Dev_FINAL}'):
            if text == reply:
                data = await r.get(f'{reply}:filter:{Dev_FINAL}{m.chat.id}')
                if data:
                    if await send_filter_reply(c, m, data, k, reply):
                        return


@Client.on_message(filters.group & ~filters.bot, group=-222)
async def multi_reply_handler(c, m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    k = await r.get(f'{Dev_FINAL}:botkey')
    await multi_reply(c, m, k)

async def multi_reply(c, m, k):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if not await check_global_restrictions(c, m, k, caller='reply'):
        return

    text = m.text

    if await r.get(f'{m.chat.id}:addFilterM2:{m.from_user.id}{Dev_FINAL}') and (await mod_pls(m.from_user.id, m.chat.id) or await fake_rank_pls(m.from_user.id, m.chat.id, 'replies')):
        key = await r.get(f'{m.chat.id}:addFilterM2:{m.from_user.id}{Dev_FINAL}')
        
        if m.text and (m.text == 'تم' or m.text == 'الغاء'):
            if m.text == 'الغاء':
                await r.delete(f'{m.chat.id}:addFilterM2:{m.from_user.id}{Dev_FINAL}')
                await r.delete(f'{key}:multifilter:{m.chat.id}{Dev_FINAL}')
                return await m.reply(plugins_replies_802(k))
            elif m.text == 'تم':
                count = len(await r.smembers(f'{key}:multifilter:{m.chat.id}{Dev_FINAL}'))
                await r.set(f'{key}:multiFilter:{m.chat.id}{Dev_FINAL}', 1)
                await r.sadd(f'{m.chat.id}:MFiltersList:{Dev_FINAL}', key)
                await r.delete(f'{m.chat.id}:addFilterM2:{m.from_user.id}{Dev_FINAL}')
                return await m.reply(plugins_replies_808(k, key, k, count), parse_mode=ParseMode.HTML)
        
        if m.text and m.text == 'الغاء':
            await r.delete(f'{m.chat.id}:addFilterM2:{m.from_user.id}{Dev_FINAL}')
            await r.delete(f'{key}:multifilter:{m.chat.id}{Dev_FINAL}')
            return await m.reply(plugins_replies_813(k))
        
        if m.text:
            await r.sadd(f'{key}:multifilter:{m.chat.id}{Dev_FINAL}', m.html)
        elif m.photo:
            photo = m.photo.file_id
            caption = m.html if m.caption else 'None'
            await r.sadd(f'{key}:multifilter:{m.chat.id}{Dev_FINAL}', f'type=photo&photo={photo}&caption={caption}')
        elif m.video:
            video = m.video.file_id
            caption = m.html if m.caption else 'None'
            await r.sadd(f'{key}:multifilter:{m.chat.id}{Dev_FINAL}', f'type=video&video={video}&caption={caption}')
        elif m.animation:
            anim = m.animation.file_id
            caption = m.html if m.caption else 'None'
            await r.sadd(f'{key}:multifilter:{m.chat.id}{Dev_FINAL}', f'type=animation&animation={anim}&caption={caption}')
        elif m.audio:
            aud = m.audio.file_id
            caption = m.html if m.caption else 'None'
            await r.sadd(f'{key}:multifilter:{m.chat.id}{Dev_FINAL}', f'type=audio&audio={aud}&caption={caption}')
        elif m.voice:
            voice = m.voice.file_id
            caption = m.html if m.caption else 'None'
            await r.sadd(f'{key}:multifilter:{m.chat.id}{Dev_FINAL}', f'type=voice&voice={voice}&caption={caption}')
        elif m.document:
            doc = m.document.file_id
            caption = m.html if m.caption else 'None'
            await r.sadd(f'{key}:multifilter:{m.chat.id}{Dev_FINAL}', f'type=doc&doc={doc}&caption={caption}')
        elif m.sticker:
            stic = m.sticker.file_id
            await r.sadd(f'{key}:multifilter:{m.chat.id}{Dev_FINAL}', f'type=sticker&sticker={stic}')
        
        return await m.reply(plugins_replies_845(k), parse_mode=ParseMode.MARKDOWN)

    if await r.get(f'{m.chat.id}:addFilterM:{m.from_user.id}{Dev_FINAL}'):
        if text == 'الغاء':
            await r.delete(f'{m.chat.id}:addFilterM:{m.from_user.id}{Dev_FINAL}')
            return await m.reply(plugins_replies_850(k))

        await r.set(f'{m.chat.id}:addFilterM2:{m.from_user.id}{Dev_FINAL}', m.text)
        await r.delete(f'{m.chat.id}:addFilterM:{m.from_user.id}{Dev_FINAL}')
        return await m.reply(
            plugins_replies_854(k),
            parse_mode=ParseMode.MARKDOWN
        )

    if not text: return

    name = await r.get(f'{Dev_FINAL}:BotName')
    if name and text.startswith(f'{name} '):
        text = text.replace(f'{name} ', '')

    if await r.get(f'{m.chat.id}:Custom:{m.chat.id}{Dev_FINAL}&text={text}'):
        text = await r.get(f'{m.chat.id}:Custom:{m.chat.id}{Dev_FINAL}&text={text}')
    if await r.get(f'Custom:{Dev_FINAL}&text={text}'):
        text = await r.get(f'Custom:{Dev_FINAL}&text={text}')

    if text == 'اضف رد متعدد' and not await r.get(f'{m.chat.id}:addFilterM:{m.from_user.id}{Dev_FINAL}') and not await r.get(f'{m.chat.id}:addFilterM2:{m.from_user.id}{Dev_FINAL}'):
        if not (await mod_pls(m.from_user.id, m.chat.id) or await fake_rank_pls(m.from_user.id, m.chat.id, 'replies')):
            return await m.reply(plugins_replies_872(k))
        await r.set(f'{m.chat.id}:addFilterM:{m.from_user.id}{Dev_FINAL}', 1)
        return await m.reply(plugins_replies_874(k))

    if await is_user_adding(m.from_user.id, m.chat.id):
        return

    if await r.get(f'{m.chat.id}:delFilterM:{m.from_user.id}{Dev_FINAL}') and await mod_pls(m.from_user.id, m.chat.id):
        if text == 'الغاء':
            await r.delete(f'{m.chat.id}:delFilterM:{m.from_user.id}{Dev_FINAL}')
            return await m.reply(plugins_replies_882(k))
        if not await r.get(f'{m.text}:multiFilter:{m.chat.id}{Dev_FINAL}'):
            await r.delete(f'{m.chat.id}:delFilterM:{m.from_user.id}{Dev_FINAL}')
            return await m.reply(plugins_replies_885(k))
        await r.delete(f'{m.text}:multiFilter:{m.chat.id}{Dev_FINAL}')
        await r.delete(f'{m.text}:multifilter:{m.chat.id}{Dev_FINAL}')
        await r.delete(f'{m.chat.id}:delFilterM:{m.from_user.id}{Dev_FINAL}')
        await r.srem(f'{m.chat.id}:MFiltersList:{Dev_FINAL}', m.text)
        return await m.reply(plugins_replies_890(k))

    if text == 'الردود المتعدده' and (await mod_pls(m.from_user.id, m.chat.id) or await fake_rank_pls(m.from_user.id, m.chat.id, 'replies')):
        if not await r.smembers(f'{m.chat.id}:MFiltersList:{Dev_FINAL}'):
            return await m.reply(plugins_replies_894(k))
        msg = 'الردود المتعدده:\n'
        count = 1
        for reply in await r.smembers(f'{m.chat.id}:MFiltersList:{Dev_FINAL}'):
            ttt = len(await r.smembers(f'{reply}:multifilter:{m.chat.id}{Dev_FINAL}'))
            msg += f'\n{count} - ( {reply} )  ( {ttt} )'
            count += 1
        return await m.reply(msg, disable_web_page_preview=True, parse_mode=ParseMode.HTML)

    if text == 'مسح الردود المتعدده' and (await mod_pls(m.from_user.id, m.chat.id) or await fake_rank_pls(m.from_user.id, m.chat.id, 'replies')):
        if not await r.smembers(f'{m.chat.id}:MFiltersList:{Dev_FINAL}'):
            return await m.reply(plugins_replies_905(k))
        count = 0
        for reply in await r.smembers(f'{m.chat.id}:MFiltersList:{Dev_FINAL}'):
            await r.delete(f'{reply}:multifilter:{m.chat.id}{Dev_FINAL}')
            await r.srem(f'{m.chat.id}:MFiltersList:{Dev_FINAL}', reply)
            await r.delete(f'{reply}:multiFilter:{m.chat.id}{Dev_FINAL}')
            count += 1
        return await m.reply(plugins_replies_912(k, count))

    if text == 'مسح رد متعدد' and not await r.get(f'{m.chat.id}:delFilterM:{m.from_user.id}{Dev_FINAL}'):
        if not (await mod_pls(m.from_user.id, m.chat.id) or await fake_rank_pls(m.from_user.id, m.chat.id, 'replies')):
            return await m.reply(plugins_replies_916(k))
        await r.set(f'{m.chat.id}:delFilterM:{m.from_user.id}{Dev_FINAL}', 1)
        return await m.reply(plugins_replies_918(k, k), parse_mode=ParseMode.HTML)

    if not await r.get(f'{m.chat.id}:lock_filter:{Dev_FINAL}'):
        for reply in await r.smembers(f'{m.chat.id}:MFiltersList:{Dev_FINAL}'):
            if text == reply:
                if await r.get(f'{reply}:multiFilter:{m.chat.id}{Dev_FINAL}'):
                    replies = await r.smembers(f'{reply}:multifilter:{m.chat.id}{Dev_FINAL}')
                    if replies:
                        chosen = safe_choice([x for x in replies])
                        await send_multi_reply(c, m, chosen, k, reply)
                        return


@Client.on_message(filters.group & ~filters.bot, group=-223)
async def special_reply_handler(c, m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    k = await r.get(f'{Dev_FINAL}:botkey')
    await special_reply(c, m, k)

async def special_reply(c, m, k):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if not await check_global_restrictions(c, m, k, caller='reply'):
        return

    text = m.text

    if await r.get(f'{m.chat.id}:addFilterS2:{m.from_user.id}{Dev_FINAL}') and (await mod_pls(m.from_user.id, m.chat.id) or await fake_rank_pls(m.from_user.id, m.chat.id, 'replies')):
        key = await r.get(f'{m.chat.id}:addFilterS2:{m.from_user.id}{Dev_FINAL}')
        
        if m.text and m.text == 'الغاء':
            await r.delete(f'{m.chat.id}:addFilterS2:{m.from_user.id}{Dev_FINAL}')
            return await m.reply(plugins_replies_953(k))
            
        await r.delete(f'{m.chat.id}:addFilterS2:{m.from_user.id}{Dev_FINAL}')

        TIME_ZONE = "Asia/Riyadh"
        ZONE = pytz.timezone(TIME_ZONE)
        TIME = datetime.now(ZONE)
        date = TIME.strftime("%d/%m/%Y %I:%M:%S %p")

        if m.text:
            await r.set(f'{key}:specialfilter:{Dev_FINAL}{m.chat.id}', f'type=text&text={m.html}')
            await r.set(f'{key}:specialfiltertype:{m.chat.id}{Dev_FINAL}', 'نص')
        elif m.photo:
            photo = m.photo.file_id
            caption = m.html if m.caption else 'None'
            await r.set(f'{key}:specialfilter:{Dev_FINAL}{m.chat.id}', f'type=photo&photo={photo}&caption={caption}')
            await r.set(f'{key}:specialfiltertype:{m.chat.id}{Dev_FINAL}', 'صوره')
        elif m.video:
            video = m.video.file_id
            caption = m.html if m.caption else 'None'
            await r.set(f'{key}:specialfilter:{Dev_FINAL}{m.chat.id}', f'type=video&video={video}&caption={caption}')
            await r.set(f'{key}:specialfiltertype:{m.chat.id}{Dev_FINAL}', 'فيديو')
        elif m.animation:
            anim = m.animation.file_id
            caption = m.html if m.caption else 'None'
            await r.set(f'{key}:specialfilter:{Dev_FINAL}{m.chat.id}', f'type=animation&animation={anim}&caption={caption}')
            await r.set(f'{key}:specialfiltertype:{m.chat.id}{Dev_FINAL}', 'متحركه')
        elif m.audio:
            aud = m.audio.file_id
            caption = m.html if m.caption else 'None'
            await r.set(f'{key}:specialfilter:{Dev_FINAL}{m.chat.id}', f'type=audio&audio={aud}&caption={caption}')
            await r.set(f'{key}:specialfiltertype:{m.chat.id}{Dev_FINAL}', 'صوت')
        elif m.voice:
            voice = m.voice.file_id
            caption = m.html if m.caption else 'None'
            await r.set(f'{key}:specialfilter:{Dev_FINAL}{m.chat.id}', f'type=voice&voice={voice}&caption={caption}')
            await r.set(f'{key}:specialfiltertype:{m.chat.id}{Dev_FINAL}', 'بصمه')
        elif m.document:
            doc = m.document.file_id
            caption = m.html if m.caption else 'None'
            await r.set(f'{key}:specialfilter:{Dev_FINAL}{m.chat.id}', f'type=doc&doc={doc}&caption={caption}')
            await r.set(f'{key}:specialfiltertype:{m.chat.id}{Dev_FINAL}', 'ملف')
        elif m.sticker:
            stic = m.sticker.file_id
            await r.set(f'{key}:specialfilter:{Dev_FINAL}{m.chat.id}', f'type=sticker&sticker={stic}')
            await r.set(f'{key}:specialfiltertype:{m.chat.id}{Dev_FINAL}', 'ستيكر')
        else:
            return

        await r.set(f'{key}:specialfilterInfo:{m.chat.id}{Dev_FINAL}', f'by={m.from_user.id}&date={date}')
        await r.sadd(f'{m.chat.id}:SFiltersList:{Dev_FINAL}', key)
        return await m.reply(plugins_replies_1004(key), parse_mode=ParseMode.HTML)

    if await r.get(f'{m.chat.id}:addFilterS:{m.from_user.id}{Dev_FINAL}'):
        if text == 'الغاء':
            await r.delete(f'{m.chat.id}:addFilterS:{m.from_user.id}{Dev_FINAL}')
            return await m.reply(plugins_replies_1009(k))

        if await mod_pls(m.from_user.id, m.chat.id):
            await r.delete(f'{m.chat.id}:addFilterS:{m.from_user.id}{Dev_FINAL}')
            await r.set(f'{m.chat.id}:addFilterS2:{m.from_user.id}{Dev_FINAL}', m.text)
            return await m.reply(
                plugins_replies_1014(k, k),
                parse_mode=ParseMode.MARKDOWN
            )

    if not text: return

    name = await r.get(f'{Dev_FINAL}:BotName')
    if name and text.startswith(f'{name} '):
        text = text.replace(f'{name} ', '')

    if await r.get(f'{m.chat.id}:Custom:{m.chat.id}{Dev_FINAL}&text={text}'):
        text = await r.get(f'{m.chat.id}:Custom:{m.chat.id}{Dev_FINAL}&text={text}')
    if await r.get(f'Custom:{Dev_FINAL}&text={text}'):
        text = await r.get(f'Custom:{Dev_FINAL}&text={text}')

    if text == 'اضف رد مميز' and not await r.get(f'{m.chat.id}:addFilterS:{m.from_user.id}{Dev_FINAL}') and not await r.get(f'{m.chat.id}:addFilterS2:{m.from_user.id}{Dev_FINAL}'):
        if not (await mod_pls(m.from_user.id, m.chat.id) or await fake_rank_pls(m.from_user.id, m.chat.id, 'replies')):
            return await m.reply(plugins_replies_1039(k))
        await r.set(f'{m.chat.id}:addFilterS:{m.from_user.id}{Dev_FINAL}', 1)
        return await m.reply(plugins_replies_1041(k))

    if await is_user_adding(m.from_user.id, m.chat.id):
        return

    if await r.get(f'{m.chat.id}:delFilterS:{m.from_user.id}{Dev_FINAL}') and await mod_pls(m.from_user.id, m.chat.id):
        if text == 'الغاء':
            await r.delete(f'{m.chat.id}:delFilterS:{m.from_user.id}{Dev_FINAL}')
            return await m.reply(plugins_replies_1049(k))
        if not await r.get(f'{m.text}:specialfilterInfo:{m.chat.id}{Dev_FINAL}'):
            await r.delete(f'{m.chat.id}:delFilterS:{m.from_user.id}{Dev_FINAL}')
            return await m.reply(plugins_replies_1052(k))
        await r.delete(f'{m.text}:specialfilter:{Dev_FINAL}{m.chat.id}')
        await r.delete(f'{m.text}:specialfiltertype:{m.chat.id}{Dev_FINAL}')
        await r.delete(f'{m.text}:specialfilterInfo:{m.chat.id}{Dev_FINAL}')
        await r.srem(f'{m.chat.id}:SFiltersList:{Dev_FINAL}', m.text)
        await r.delete(f'{m.chat.id}:delFilterS:{m.from_user.id}{Dev_FINAL}')
        return await m.reply(plugins_replies_1058(m.text, k))

    if text.startswith('الرد المميز ') and len(m.text.split()) > 2 and (await mod_pls(m.from_user.id, m.chat.id) or await fake_rank_pls(m.from_user.id, m.chat.id, 'replies')):
        reply = m.text.split(None, 2)[2]
        if not await r.get(f'{reply}:specialfilterInfo:{m.chat.id}{Dev_FINAL}'):
            return await m.reply(plugins_replies_1063(k))
        get = await r.get(f'{reply}:specialfilterInfo:{m.chat.id}{Dev_FINAL}')
        split = get.split('by=')[1]
        by = split.split('&date=')[0]
        date = split.split('&date=')[1]
        type = await r.get(f'{reply}:specialfiltertype:{m.chat.id}{Dev_FINAL}')
        return await m.reply(plugins_replies_1069(k, by, html.escape(str(reply)), k, date, k, type))

    if text == 'الردود المميزه' and (await mod_pls(m.from_user.id, m.chat.id) or await fake_rank_pls(m.from_user.id, m.chat.id, 'replies')):
        if not await r.smembers(f'{m.chat.id}:SFiltersList:{Dev_FINAL}'):
            return await m.reply(plugins_replies_1073(k))
        msg = 'الردود المميزه:\n'
        count = 1
        for reply in await r.smembers(f'{m.chat.id}:SFiltersList:{Dev_FINAL}'):
            type = await r.get(f'{reply}:specialfiltertype:{m.chat.id}{Dev_FINAL}')
            msg += f'\n{count} - ( {reply} )  ( {type} )'
            count += 1
        return await m.reply(msg, disable_web_page_preview=True, parse_mode=ParseMode.HTML)

    if text == 'مسح الردود المميزه' and (await mod_pls(m.from_user.id, m.chat.id) or await fake_rank_pls(m.from_user.id, m.chat.id, 'replies')):
        if not await r.smembers(f'{m.chat.id}:SFiltersList:{Dev_FINAL}'):
            return await m.reply(plugins_replies_1084(k))
        total = 0
        for reply in await r.smembers(f'{m.chat.id}:SFiltersList:{Dev_FINAL}'):
            await r.delete(f'{reply}:specialfilter:{Dev_FINAL}{m.chat.id}')
            await r.delete(f'{reply}:specialfiltertype:{m.chat.id}{Dev_FINAL}')
            await r.delete(f'{reply}:specialfilterInfo:{m.chat.id}{Dev_FINAL}')
            await r.srem(f'{m.chat.id}:SFiltersList:{Dev_FINAL}', reply)
            total += 1
        return await m.reply(plugins_replies_1092(k, total))

    if text == 'مسح رد مميز' and not await r.get(f'{m.chat.id}:delFilterS:{m.from_user.id}{Dev_FINAL}'):
        if not (await mod_pls(m.from_user.id, m.chat.id) or await fake_rank_pls(m.from_user.id, m.chat.id, 'replies')):
            return await m.reply(plugins_replies_1096(k))
        await r.set(f'{m.chat.id}:delFilterS:{m.from_user.id}{Dev_FINAL}', 1)
        return await m.reply(plugins_replies_1098(k, k), parse_mode=ParseMode.HTML)

    if not await r.get(f'{m.chat.id}:lock_filter:{Dev_FINAL}'):
        for reply in await r.smembers(f'{m.chat.id}:SFiltersList:{Dev_FINAL}'):
            if reply in text:
                data = await r.get(f'{reply}:specialfilter:{Dev_FINAL}{m.chat.id}')
                if data:
                    if await send_filter_reply(c, m, data, k, reply):
                        return


@Client.on_message(filters.group & ~filters.bot, group=-224)
async def global_reply_handler(c, m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    k = await r.get(f'{Dev_FINAL}:botkey')
    await global_reply(c, m, k)

async def global_reply(c, m, k):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()

    if not await check_global_restrictions(c, m, k, caller='reply'):
        return

    text = m.text

    if text == 'تعطيل الردود العامه' and await gowner_pls(m.from_user.id, m.chat.id):
        if await r.get(f'{m.chat.id}:lock_global_filter:{Dev_FINAL}'):
            return await m.reply(plugins_replies_1126(k, m.from_user.mention(), k), parse_mode=ParseMode.HTML)
        await r.set(f'{m.chat.id}:lock_global_filter:{Dev_FINAL}', 1)
        return await m.reply(plugins_replies_1128(k, m.from_user.mention(), k), parse_mode=ParseMode.HTML)

    if text == 'تفعيل الردود العامه' and await gowner_pls(m.from_user.id, m.chat.id):
        if not await r.get(f'{m.chat.id}:lock_global_filter:{Dev_FINAL}'):
            return await m.reply(plugins_replies_1132(k, m.from_user.mention(), k), parse_mode=ParseMode.HTML)
        await r.delete(f'{m.chat.id}:lock_global_filter:{Dev_FINAL}')
        return await m.reply(plugins_replies_1134(k, m.from_user.mention(), k), parse_mode=ParseMode.HTML)

    if await r.get(f'{m.chat.id}:lock_global_filter:{Dev_FINAL}'):
        return

    if await r.get(f'{m.chat.id}:addFilterG2:{m.from_user.id}{Dev_FINAL}'):
        if not await dev2_pls(m.from_user.id, m.chat.id): return
        key = await r.get(f'{m.chat.id}:addFilterG2:{m.from_user.id}{Dev_FINAL}')
        await r.delete(f'{m.chat.id}:addFilterG2:{m.from_user.id}{Dev_FINAL}')

        if m.text and m.text == 'الغاء':
            return await m.reply(plugins_replies_1145(k))

        TIME_ZONE = "Asia/Riyadh"
        ZONE = pytz.timezone(TIME_ZONE)
        TIME = datetime.now(ZONE)
        date = TIME.strftime("%d/%m/%Y %I:%M:%S %p")

        if m.text:
            if m.text.startswith('type=inline&'):
                await r.set(f'btn_id:inline_global:{key}:global', f"inline_global_{key}")
            
            await r.set(f'Global:{key}:filter:{Dev_FINAL}', f'type=text&text={m.html}')
            await r.set(f'Global:{key}:filtertype:{Dev_FINAL}', 'نص')
        elif m.photo:
            photo = m.photo.file_id
            caption = m.html if m.caption else 'None'
            await r.set(f'Global:{key}:filter:{Dev_FINAL}', f'type=photo&photo={photo}&caption={caption}')
            await r.set(f'Global:{key}:filtertype:{Dev_FINAL}', 'صوره')
        elif m.video:
            video = m.video.file_id
            caption = m.html if m.caption else 'None'
            await r.set(f'Global:{key}:filter:{Dev_FINAL}', f'type=video&video={video}&caption={caption}')
            await r.set(f'Global:{key}:filtertype:{Dev_FINAL}', 'فيديو')
        elif m.animation:
            anim = m.animation.file_id
            caption = m.html if m.caption else 'None'
            await r.set(f'Global:{key}:filter:{Dev_FINAL}', f'type=animation&animation={anim}&caption={caption}')
            await r.set(f'Global:{key}:filtertype:{Dev_FINAL}', 'متحركه')
        elif m.audio:
            aud = m.audio.file_id
            caption = m.html if m.caption else 'None'
            await r.set(f'Global:{key}:filter:{Dev_FINAL}', f'type=audio&audio={aud}&caption={caption}')
            await r.set(f'Global:{key}:filtertype:{Dev_FINAL}', 'صوت')
        elif m.voice:
            voice = m.voice.file_id
            caption = m.html if m.caption else 'None'
            await r.set(f'Global:{key}:filter:{Dev_FINAL}', f'type=voice&voice={voice}&caption={caption}')
            await r.set(f'Global:{key}:filtertype:{Dev_FINAL}', 'بصمه')
        elif m.document:
            doc = m.document.file_id
            caption = m.html if m.caption else 'None'
            await r.set(f'Global:{key}:filter:{Dev_FINAL}', f'type=doc&doc={doc}&caption={caption}')
            await r.set(f'Global:{key}:filtertype:{Dev_FINAL}', 'ملف')
        elif m.sticker:
            stic = m.sticker.file_id
            await r.set(f'Global:{key}:filter:{Dev_FINAL}', f'type=sticker&sticker={stic}')
            await r.set(f'Global:{key}:filtertype:{Dev_FINAL}', 'ستيكر')
        else:
            return

        await r.set(f'Global:{key}:filterInfo:{Dev_FINAL}', f'by={m.from_user.id}&date={date}')
        await r.sadd(f'Global:FiltersList:{Dev_FINAL}', key)
        
        await refresh_dynamic_buttons()
        return await m.reply(plugins_replies_1199(key), parse_mode=ParseMode.HTML)

    if await r.get(f'{m.chat.id}:addFilterG:{m.from_user.id}{Dev_FINAL}'):
        if not await dev2_pls(m.from_user.id, m.chat.id): return
        if text == 'الغاء':
            await r.delete(f'{m.chat.id}:addFilterG:{m.from_user.id}{Dev_FINAL}')
            return await m.reply(plugins_replies_1205(k))

        await r.set(f'{m.chat.id}:addFilterG2:{m.from_user.id}{Dev_FINAL}', m.text)
        await r.delete(f'{m.chat.id}:addFilterG:{m.from_user.id}{Dev_FINAL}')
        return await m.reply(
            plugins_replies_1209(k),
            parse_mode=ParseMode.MARKDOWN
        )

    if not text: return

    name = await r.get(f'{Dev_FINAL}:BotName')
    if name and text.startswith(f'{name} '):
        text = text.replace(f'{name} ', '')

    if await r.get(f'{m.chat.id}:Custom:{m.chat.id}{Dev_FINAL}&text={text}'):
        text = await r.get(f'{m.chat.id}:Custom:{m.chat.id}{Dev_FINAL}&text={text}')
    if await r.get(f'Custom:{Dev_FINAL}&text={text}'):
        text = await r.get(f'Custom:{Dev_FINAL}&text={text}')

    if text == 'اضف رد عام' and not await r.get(f'{m.chat.id}:addFilterG:{m.from_user.id}{Dev_FINAL}') and not await r.get(f'{m.chat.id}:addFilterG2:{m.from_user.id}{Dev_FINAL}'):
        if not await dev2_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_replies_1227(k))
        await r.set(f'{m.chat.id}:addFilterG:{m.from_user.id}{Dev_FINAL}', 1)
        return await m.reply(plugins_replies_1229(k))

    if await r.get(f'{m.chat.id}:delFilterG:{m.from_user.id}{Dev_FINAL}'):
        if text == 'الغاء':
            await r.delete(f'{m.chat.id}:delFilterG:{m.from_user.id}{Dev_FINAL}')
            return await m.reply(plugins_replies_1237(k))
        if await dev2_pls(m.from_user.id, m.chat.id):
            if not await r.get(f'Global:{m.text}:filterInfo:{Dev_FINAL}'):
                await r.delete(f'{m.chat.id}:delFilterG:{m.from_user.id}{Dev_FINAL}')
                return await m.reply(plugins_replies_1241(k))
            await r.delete(f'Global:{m.text}:filter:{Dev_FINAL}')
            await r.delete(f'Global:{m.text}:filtertype:{Dev_FINAL}')
            await r.delete(f'Global:{m.text}:filterInfo:{Dev_FINAL}')
            await r.srem(f'Global:FiltersList:{Dev_FINAL}', m.text)
            await r.delete(f'{m.chat.id}:delFilterG:{m.from_user.id}{Dev_FINAL}')
            
            await refresh_dynamic_buttons()
            return await m.reply(plugins_replies_1249(m.text, k))

    if text.startswith('الرد العام ') and len(m.text.split()) > 2:
        if not await dev2_pls(m.from_user.id, m.chat.id): return await m.reply(plugins_replies_1252(k))
        reply = m.text.split(None, 2)[2]
        if not await r.get(f'Global:{reply}:filterInfo:{Dev_FINAL}'):
            return await m.reply(plugins_replies_1255(k))
        get = await r.get(f'Global:{reply}:filterInfo:{Dev_FINAL}')
        split = get.split('by=')[1]
        by = split.split('&date=')[0]
        date = split.split('&date=')[1]
        type = await r.get(f'Global:{reply}:filtertype:{Dev_FINAL}')
        return await m.reply(plugins_replies_1261(k, by, html.escape(str(reply)), k, date, k, type))

    if text == 'الردود العامه':
        if not await dev2_pls(m.from_user.id, m.chat.id): return await m.reply(plugins_replies_1264(k))
        if not await r.smembers(f'Global:FiltersList:{Dev_FINAL}'):
            return await m.reply(plugins_replies_1266(k))
        msg = 'الردود العامه:\n'
        count = 1
        for reply in await r.smembers(f'Global:FiltersList:{Dev_FINAL}'):
            type = await r.get(f'Global:{reply}:filtertype:{Dev_FINAL}')
            msg += f'\n{count} - ( {reply} )  ( {type} )'
            count += 1
        return await m.reply(msg, disable_web_page_preview=True, parse_mode=ParseMode.HTML)

    if text == 'مسح الردود العامه':
        if not await dev2_pls(m.from_user.id, m.chat.id): return await m.reply(plugins_replies_1276(k))
        if not await r.smembers(f'Global:FiltersList:{Dev_FINAL}'):
            return await m.reply(plugins_replies_1278(k))
        total = 0
        for reply in await r.smembers(f'Global:FiltersList:{Dev_FINAL}'):
            await r.delete(f'Global:{reply}:filter:{Dev_FINAL}')
            await r.delete(f'Global:{reply}:filtertype:{Dev_FINAL}')
            await r.delete(f'Global:{reply}:filterInfo:{Dev_FINAL}')
            await r.srem(f'Global:FiltersList:{Dev_FINAL}', reply)
            total += 1
        
        await refresh_dynamic_buttons()
        return await m.reply(plugins_replies_1288(k, total))

    if text == 'مسح رد عام' and not await r.get(f'{m.chat.id}:delFilterG:{m.from_user.id}{Dev_FINAL}'):
        if not await dev2_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_replies_1292(k))
        await r.set(f'{m.chat.id}:delFilterG:{m.from_user.id}{Dev_FINAL}', 1)
        return await m.reply(plugins_replies_1294(k, k), parse_mode=ParseMode.HTML)

    if text == 'اضف رد انلاين عام':
        if not await dev2_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_replies_1298(k))
        
        if await r.get(f'{m.chat.id}:addInlineStepGlobal:{m.from_user.id}{Dev_FINAL}'):
            return await m.reply(plugins_replies_1301(k))
        
        await r.set(f'{m.chat.id}:addInlineStepGlobal:{m.from_user.id}{Dev_FINAL}', "1")
        return await m.reply(plugins_replies_1304(k))

    step_global = await r.get(f'{m.chat.id}:addInlineStepGlobal:{m.from_user.id}{Dev_FINAL}')
    if step_global and await dev2_pls(m.from_user.id, m.chat.id):
        if text == 'الغاء':
            await r.delete(f'{m.chat.id}:addInlineStepGlobal:{m.from_user.id}{Dev_FINAL}')
            await r.delete(f'{m.chat.id}:addInlineWordGlobal:{m.from_user.id}{Dev_FINAL}')
            await r.delete(f'{m.chat.id}:addInlineTextGlobal:{m.from_user.id}{Dev_FINAL}')
            await r.delete(f'{m.chat.id}:addInlineBttnGlobal:{m.from_user.id}{Dev_FINAL}')
            return await m.reply(plugins_replies_1313(k))
        
        if step_global == "1":
            await r.set(f'{m.chat.id}:addInlineWordGlobal:{m.from_user.id}{Dev_FINAL}', m.text)
            await r.set(f'{m.chat.id}:addInlineStepGlobal:{m.from_user.id}{Dev_FINAL}', "2")
            return await m.reply(
                plugins_replies_1318(k, k),
                parse_mode=ParseMode.MARKDOWN
            )
        
        elif step_global == "2":
            await r.set(f'{m.chat.id}:addInlineTextGlobal:{m.from_user.id}{Dev_FINAL}', m.html)
            await r.set(f'{m.chat.id}:addInlineStepGlobal:{m.from_user.id}{Dev_FINAL}', "3")
            word = await r.get(f'{m.chat.id}:addInlineWordGlobal:{m.from_user.id}{Dev_FINAL}')
            return await m.reply(plugins_replies_1334(k, word), parse_mode=ParseMode.HTML)
        
        elif step_global == "3":
            await r.set(f'{m.chat.id}:addInlineBttnGlobal:{m.from_user.id}{Dev_FINAL}', m.text)
            await r.set(f'{m.chat.id}:addInlineStepGlobal:{m.from_user.id}{Dev_FINAL}', "4")
            word = await r.get(f'{m.chat.id}:addInlineWordGlobal:{m.from_user.id}{Dev_FINAL}')
            return await m.reply(plugins_replies_1340(k, word), parse_mode=ParseMode.HTML)
        
        elif step_global == "4":
            word = await r.get(f'{m.chat.id}:addInlineWordGlobal:{m.from_user.id}{Dev_FINAL}')
            rep_text = await r.get(f'{m.chat.id}:addInlineTextGlobal:{m.from_user.id}{Dev_FINAL}')
            bttn_text = await r.get(f'{m.chat.id}:addInlineBttnGlobal:{m.from_user.id}{Dev_FINAL}')
            bttn_url = m.text
            
            if not bttn_url.startswith(('http://', 'https://')):
                return await m.reply(plugins_replies_1349(k))
            
            import urllib.parse
            save_data = urllib.parse.urlencode({'type': 'inline', 'text': rep_text, 'btn': bttn_text, 'url': bttn_url})
            
            TIME_ZONE = "Asia/Riyadh"
            ZONE = pytz.timezone(TIME_ZONE)
            TIME = datetime.now(ZONE)
            date = TIME.strftime("%d/%m/%Y %I:%M:%S %p")
            
            await r.set(f'Global:{word}:filter:{Dev_FINAL}', save_data)
            await r.set(f'Global:{word}:filtertype:{Dev_FINAL}', 'انلاين')
            await r.set(f'Global:{word}:filterInfo:{Dev_FINAL}', f'by={m.from_user.id}&date={date}')
            await r.sadd(f'Global:FiltersList:{Dev_FINAL}', word)
            
            btn_id = f"inline_global_{word}"
            await r.set(f'btn_id:inline_global:{word}:global', btn_id)
            await r.set(f'btn_name:replies:{btn_id}:global', bttn_text)
            
            await r.delete(f'{m.chat.id}:addInlineStepGlobal:{m.from_user.id}{Dev_FINAL}')
            await r.delete(f'{m.chat.id}:addInlineWordGlobal:{m.from_user.id}{Dev_FINAL}')
            await r.delete(f'{m.chat.id}:addInlineTextGlobal:{m.from_user.id}{Dev_FINAL}')
            await r.delete(f'{m.chat.id}:addInlineBttnGlobal:{m.from_user.id}{Dev_FINAL}')
            
            await refresh_dynamic_buttons()
            return await m.reply(plugins_replies_1374(k, word), parse_mode=ParseMode.HTML)

    if await is_user_adding(m.from_user.id, m.chat.id):
        return

    if text == 'مسح رد انلاين عام':
        if not await dev2_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_replies_1378(k))
        
        if await r.get(f'{m.chat.id}:delInlineGlobal:{m.from_user.id}{Dev_FINAL}'):
            return await m.reply(plugins_replies_1381(k))
        
        await r.set(f'{m.chat.id}:delInlineGlobal:{m.from_user.id}{Dev_FINAL}', 1)
        return await m.reply(plugins_replies_1384(k, k))

    if await r.get(f'{m.chat.id}:delInlineGlobal:{m.from_user.id}{Dev_FINAL}'):
        if not await dev2_pls(m.from_user.id, m.chat.id):
            return
        
        if text == 'الغاء':
            await r.delete(f'{m.chat.id}:delInlineGlobal:{m.from_user.id}{Dev_FINAL}')
            return await m.reply(plugins_replies_1392(k))
        
        word = text
        
        if not await r.get(f'Global:{word}:filterInfo:{Dev_FINAL}'):
            await r.delete(f'{m.chat.id}:delInlineGlobal:{m.from_user.id}{Dev_FINAL}')
            return await m.reply(plugins_replies_1398(k))
        
        filter_data = await r.get(f'Global:{word}:filter:{Dev_FINAL}')
        if not filter_data or not filter_data.startswith('type=inline&'):
            await r.delete(f'{m.chat.id}:delInlineGlobal:{m.from_user.id}{Dev_FINAL}')
            return await m.reply(plugins_replies_1403(k))
        
        await r.delete(f'Global:{word}:filter:{Dev_FINAL}')
        await r.delete(f'Global:{word}:filtertype:{Dev_FINAL}')
        await r.delete(f'Global:{word}:filterInfo:{Dev_FINAL}')
        await r.srem(f'Global:FiltersList:{Dev_FINAL}', word)
        await r.delete(f'btn_id:inline_global:{word}:global')
        await r.delete(f'btn_name:replies:inline_global_{word}:global')
        await r.delete(f'btn_color:replies:inline_global_{word}:global')
        
        await r.delete(f'{m.chat.id}:delInlineGlobal:{m.from_user.id}{Dev_FINAL}')
        
        await refresh_dynamic_buttons()
        return await m.reply(plugins_replies_1416(k, word))

    if text == 'كشف رد عام':
        if not await dev2_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_replies_1420(k))
        
        if not m.reply_to_message or not m.reply_to_message.text:
            return await m.reply(plugins_replies_1423(k))
        
        word = m.reply_to_message.text
        result = f'{k} الكلمة 「{word}」 مضافة لـ↤\n\n'
        found = False
        
        if await r.get(f'Global:{word}:filterInfo:{Dev_FINAL}'):
            found = True
            type_f = await r.get(f'Global:{word}:filtertype:{Dev_FINAL}')
            result += f'- 「 الردود العامه 」 \n'
            result += f'{k} نوع: {type_f}\n'
            result += f'{k} استخدم الامر ↤ مسح رد عام\n\n'
        
        if await r.get(f'Global:{word}:specialfilterInfo:{Dev_FINAL}'):
            found = True
            type_f = await r.get(f'Global:{word}:specialfiltertype:{Dev_FINAL}')
            result += f'- 「 الردود المميزه العامه 」 \n'
            result += f'{k} نوع: {type_f}\n'
            result += f'{k} استخدم الامر ↤ مسح رد مميز عام\n\n'
        
        if await r.get(f'Global:{word}:multiFilter:{Dev_FINAL}'):
            found = True
            count = len(await r.smembers(f'Global:{word}:multifilter:{Dev_FINAL}'))
            result += f'- 「 الردود المتعدده العامه 」 \n'
            result += f'{k} عدد الاجوبة: {count}\n'
            result += f'{k} استخدم الامر ↤ مسح رد متعدد عام\n\n'
        
        if await r.get(f'Custom:{Dev_FINAL}&text={word}'):
            found = True
            old_cmd = await r.get(f'Custom:{Dev_FINAL}&text={word}')
            result += f'- 「 الاوامر العامه 」 \n'
            result += f'{k} الامر القديم: {old_cmd}\n'
            result += f'{k} استخدم الامر ↤ مسح امر عام\n\n'
        
        if not found:
            return await m.reply(plugins_replies_1458(k, word))
        else:
            return await m.reply(result, disable_web_page_preview=True, parse_mode=ParseMode.HTML)

    if not await r.get(f'{m.chat.id}:lock_global_filter:{Dev_FINAL}'):
        for reply in await r.smembers(f'Global:FiltersList:{Dev_FINAL}'):
            if text == reply:
                data = await r.get(f'Global:{reply}:filter:{Dev_FINAL}')
                if data:
                    if await send_filter_reply(c, m, data, k, reply):
                        return


@Client.on_message(filters.group & ~filters.bot, group=-225)
async def global_multi_reply_handler(c, m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    k = await r.get(f'{Dev_FINAL}:botkey')
    await global_multi_reply(c, m, k)

async def global_multi_reply(c, m, k):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()

    if not await check_global_restrictions(c, m, k, caller='reply'):
        return

    if await r.get(f'{m.chat.id}:lock_global_filter:{Dev_FINAL}'):
        return

    text = m.text

    if await r.get(f'{m.chat.id}:addFilterGM2:{m.from_user.id}{Dev_FINAL}'):
        if not await dev2_pls(m.from_user.id, m.chat.id): return
        key = await r.get(f'{m.chat.id}:addFilterGM2:{m.from_user.id}{Dev_FINAL}')
        
        if m.text and (m.text == 'تم' or m.text == 'الغاء'):
            if m.text == 'الغاء':
                await r.delete(f'{m.chat.id}:addFilterGM2:{m.from_user.id}{Dev_FINAL}')
                await r.delete(f'Global:{key}:multifilter:{Dev_FINAL}')
                return await m.reply(plugins_replies_1498(k))
            elif m.text == 'تم':
                count = len(await r.smembers(f'Global:{key}:multifilter:{Dev_FINAL}'))
                await r.set(f'Global:{key}:multiFilter:{Dev_FINAL}', 1)
                await r.sadd(f'Global:MFiltersList:{Dev_FINAL}', key)
                await r.delete(f'{m.chat.id}:addFilterGM2:{m.from_user.id}{Dev_FINAL}')
                return await m.reply(plugins_replies_1504(k, key, k, count), parse_mode=ParseMode.HTML)
        
        if m.text and m.text == 'الغاء':
            await r.delete(f'{m.chat.id}:addFilterGM2:{m.from_user.id}{Dev_FINAL}')
            await r.delete(f'Global:{key}:multifilter:{Dev_FINAL}')
            return await m.reply(plugins_replies_1509(k))
        
        if m.text:
            await r.sadd(f'Global:{key}:multifilter:{Dev_FINAL}', m.html)
        elif m.photo:
            photo = m.photo.file_id
            caption = m.html if m.caption else 'None'
            await r.sadd(f'Global:{key}:multifilter:{Dev_FINAL}', f'type=photo&photo={photo}&caption={caption}')
        elif m.video:
            video = m.video.file_id
            caption = m.html if m.caption else 'None'
            await r.sadd(f'Global:{key}:multifilter:{Dev_FINAL}', f'type=video&video={video}&caption={caption}')
        elif m.animation:
            anim = m.animation.file_id
            caption = m.html if m.caption else 'None'
            await r.sadd(f'Global:{key}:multifilter:{Dev_FINAL}', f'type=animation&animation={anim}&caption={caption}')
        elif m.audio:
            aud = m.audio.file_id
            caption = m.html if m.caption else 'None'
            await r.sadd(f'Global:{key}:multifilter:{Dev_FINAL}', f'type=audio&audio={aud}&caption={caption}')
        elif m.voice:
            voice = m.voice.file_id
            caption = m.html if m.caption else 'None'
            await r.sadd(f'Global:{key}:multifilter:{Dev_FINAL}', f'type=voice&voice={voice}&caption={caption}')
        elif m.document:
            doc = m.document.file_id
            caption = m.html if m.caption else 'None'
            await r.sadd(f'Global:{key}:multifilter:{Dev_FINAL}', f'type=doc&doc={doc}&caption={caption}')
        elif m.sticker:
            stic = m.sticker.file_id
            await r.sadd(f'Global:{key}:multifilter:{Dev_FINAL}', f'type=sticker&sticker={stic}')
            
        return await m.reply(plugins_replies_1541(k), parse_mode=ParseMode.MARKDOWN)

    if await r.get(f'{m.chat.id}:addFilterGM:{m.from_user.id}{Dev_FINAL}'):
        if not await dev2_pls(m.from_user.id, m.chat.id): return
        if text == 'الغاء':
            await r.delete(f'{m.chat.id}:addFilterGM:{m.from_user.id}{Dev_FINAL}')
            return await m.reply(plugins_replies_1547(k))

        await r.set(f'{m.chat.id}:addFilterGM2:{m.from_user.id}{Dev_FINAL}', m.text)
        await r.delete(f'{m.chat.id}:addFilterGM:{m.from_user.id}{Dev_FINAL}')
        return await m.reply(
            plugins_replies_1551(k),
            parse_mode=ParseMode.MARKDOWN
        )

    if not text: return

    name = await r.get(f'{Dev_FINAL}:BotName')
    if name and text.startswith(f'{name} '):
        text = text.replace(f'{name} ', '')

    if await r.get(f'{m.chat.id}:Custom:{m.chat.id}{Dev_FINAL}&text={text}'):
        text = await r.get(f'{m.chat.id}:Custom:{m.chat.id}{Dev_FINAL}&text={text}')
    if await r.get(f'Custom:{Dev_FINAL}&text={text}'):
        text = await r.get(f'Custom:{Dev_FINAL}&text={text}')

    if text == 'اضف رد متعدد عام' and not await r.get(f'{m.chat.id}:addFilterGM:{m.from_user.id}{Dev_FINAL}') and not await r.get(f'{m.chat.id}:addFilterGM2:{m.from_user.id}{Dev_FINAL}'):
        if not await dev2_pls(m.from_user.id, m.chat.id): return await m.reply(plugins_replies_1568(k))
        await r.set(f'{m.chat.id}:addFilterGM:{m.from_user.id}{Dev_FINAL}', 1)
        return await m.reply(plugins_replies_1570(k))

    if await is_user_adding(m.from_user.id, m.chat.id):
        return

    if await r.get(f'{m.chat.id}:delFilterGM:{m.from_user.id}{Dev_FINAL}'):
        if text == 'الغاء':
            await r.delete(f'{m.chat.id}:delFilterGM:{m.from_user.id}{Dev_FINAL}')
            return await m.reply(plugins_replies_1578(k))
        if await dev2_pls(m.from_user.id, m.chat.id):
            if not await r.get(f'Global:{m.text}:multiFilter:{Dev_FINAL}'):
                await r.delete(f'{m.chat.id}:delFilterGM:{m.from_user.id}{Dev_FINAL}')
                return await m.reply(plugins_replies_1582(k))
            await r.delete(f'Global:{m.text}:multiFilter:{Dev_FINAL}')
            await r.delete(f'Global:{m.text}:multifilter:{Dev_FINAL}')
            await r.delete(f'{m.chat.id}:delFilterGM:{m.from_user.id}{Dev_FINAL}')
            await r.srem(f'Global:MFiltersList:{Dev_FINAL}', m.text)
            return await m.reply(plugins_replies_1587(k))

    if text == 'الردود المتعدده العامه':
        if not await dev2_pls(m.from_user.id, m.chat.id): return await m.reply(plugins_replies_1590(k))
        if not await r.smembers(f'Global:MFiltersList:{Dev_FINAL}'):
            return await m.reply(plugins_replies_1592(k))
        msg = 'الردود المتعدده العامه:\n'
        count = 1
        for reply in await r.smembers(f'Global:MFiltersList:{Dev_FINAL}'):
            ttt = len(await r.smembers(f'Global:{reply}:multifilter:{Dev_FINAL}'))
            msg += f'\n{count} - ( {reply} )  ( {ttt} )'
            count += 1
        return await m.reply(msg, disable_web_page_preview=True, parse_mode=ParseMode.HTML)

    if text == 'مسح الردود المتعدده العامه':
        if not await dev2_pls(m.from_user.id, m.chat.id): return await m.reply(plugins_replies_1602(k))
        if not await r.smembers(f'Global:MFiltersList:{Dev_FINAL}'):
            return await m.reply(plugins_replies_1604(k))
        count = 0
        for reply in await r.smembers(f'Global:MFiltersList:{Dev_FINAL}'):
            await r.delete(f'Global:{reply}:multifilter:{Dev_FINAL}')
            await r.srem(f'Global:MFiltersList:{Dev_FINAL}', reply)
            await r.delete(f'Global:{reply}:multiFilter:{Dev_FINAL}')
            count += 1
        return await m.reply(plugins_replies_1611(k, count))

    if text == 'مسح رد متعدد عام' and not await r.get(f'{m.chat.id}:delFilterGM:{m.from_user.id}{Dev_FINAL}'):
        if not await dev2_pls(m.from_user.id, m.chat.id): return await m.reply(plugins_replies_1614(k))
        await r.set(f'{m.chat.id}:delFilterGM:{m.from_user.id}{Dev_FINAL}', 1)
        return await m.reply(plugins_replies_1616(k, k), parse_mode=ParseMode.HTML)

    if not await r.get(f'{m.chat.id}:lock_global_filter:{Dev_FINAL}'):
        for reply in await r.smembers(f'Global:MFiltersList:{Dev_FINAL}'):
            if text == reply:
                if await r.get(f'Global:{reply}:multiFilter:{Dev_FINAL}'):
                    replies = await r.smembers(f'Global:{reply}:multifilter:{Dev_FINAL}')
                    if replies:
                        chosen = safe_choice([x for x in replies])
                        await send_multi_reply(c, m, chosen, k, reply)
                        return


@Client.on_message(filters.group & ~filters.bot, group=-226)
async def global_special_reply_handler(c, m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    k = await r.get(f'{Dev_FINAL}:botkey')
    await global_special_reply(c, m, k)

async def global_special_reply(c, m, k):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()

    if not await check_global_restrictions(c, m, k, caller='reply'):
        return

    if await r.get(f'{m.chat.id}:lock_global_filter:{Dev_FINAL}'):
        return

    text = m.text

    if await r.get(f'{m.chat.id}:addFilterGS2:{m.from_user.id}{Dev_FINAL}'):
        if not await dev2_pls(m.from_user.id, m.chat.id): return
        key = await r.get(f'{m.chat.id}:addFilterGS2:{m.from_user.id}{Dev_FINAL}')
        await r.delete(f'{m.chat.id}:addFilterGS2:{m.from_user.id}{Dev_FINAL}')

        if m.text and m.text == 'الغاء':
            return await m.reply(plugins_replies_1654(k))

        TIME_ZONE = "Asia/Riyadh"
        ZONE = pytz.timezone(TIME_ZONE)
        TIME = datetime.now(ZONE)
        date = TIME.strftime("%d/%m/%Y %I:%M:%S %p")

        if m.text:
            await r.set(f'Global:{key}:specialfilter:{Dev_FINAL}', f'type=text&text={m.html}')
            await r.set(f'Global:{key}:specialfiltertype:{Dev_FINAL}', 'نص')
        elif m.photo:
            photo = m.photo.file_id
            caption = m.html if m.caption else 'None'
            await r.set(f'Global:{key}:specialfilter:{Dev_FINAL}', f'type=photo&photo={photo}&caption={caption}')
            await r.set(f'Global:{key}:specialfiltertype:{Dev_FINAL}', 'صوره')
        elif m.video:
            video = m.video.file_id
            caption = m.html if m.caption else 'None'
            await r.set(f'Global:{key}:specialfilter:{Dev_FINAL}', f'type=video&video={video}&caption={caption}')
            await r.set(f'Global:{key}:specialfiltertype:{Dev_FINAL}', 'فيديو')
        elif m.animation:
            anim = m.animation.file_id
            caption = m.html if m.caption else 'None'
            await r.set(f'Global:{key}:specialfilter:{Dev_FINAL}', f'type=animation&animation={anim}&caption={caption}')
            await r.set(f'Global:{key}:specialfiltertype:{Dev_FINAL}', 'متحركه')
        elif m.audio:
            aud = m.audio.file_id
            caption = m.html if m.caption else 'None'
            await r.set(f'Global:{key}:specialfilter:{Dev_FINAL}', f'type=audio&audio={aud}&caption={caption}')
            await r.set(f'Global:{key}:specialfiltertype:{Dev_FINAL}', 'صوت')
        elif m.voice:
            voice = m.voice.file_id
            caption = m.html if m.caption else 'None'
            await r.set(f'Global:{key}:specialfilter:{Dev_FINAL}', f'type=voice&voice={voice}&caption={caption}')
            await r.set(f'Global:{key}:specialfiltertype:{Dev_FINAL}', 'بصمه')
        elif m.document:
            doc = m.document.file_id
            caption = m.html if m.caption else 'None'
            await r.set(f'Global:{key}:specialfilter:{Dev_FINAL}', f'type=doc&doc={doc}&caption={caption}')
            await r.set(f'Global:{key}:specialfiltertype:{Dev_FINAL}', 'ملف')
        elif m.sticker:
            stic = m.sticker.file_id
            await r.set(f'Global:{key}:specialfilter:{Dev_FINAL}', f'type=sticker&sticker={stic}')
            await r.set(f'Global:{key}:specialfiltertype:{Dev_FINAL}', 'ستيكر')
        else:
            return

        await r.set(f'Global:{key}:specialfilterInfo:{Dev_FINAL}', f'by={m.from_user.id}&date={date}')
        await r.sadd(f'Global:SFiltersList:{Dev_FINAL}', key)
        return await m.reply(plugins_replies_1703(key), parse_mode=ParseMode.HTML)

    if await r.get(f'{m.chat.id}:addFilterGS:{m.from_user.id}{Dev_FINAL}'):
        if not await dev2_pls(m.from_user.id, m.chat.id): return
        if text == 'الغاء':
            await r.delete(f'{m.chat.id}:addFilterGS:{m.from_user.id}{Dev_FINAL}')
            return await m.reply(plugins_replies_1709(k))

        await r.set(f'{m.chat.id}:addFilterGS2:{m.from_user.id}{Dev_FINAL}', m.text)
        await r.delete(f'{m.chat.id}:addFilterGS:{m.from_user.id}{Dev_FINAL}')
        return await m.reply(
            plugins_replies_1713(k),
            parse_mode=ParseMode.MARKDOWN
        )

    if not text: return

    name = await r.get(f'{Dev_FINAL}:BotName')
    if name and text.startswith(f'{name} '):
        text = text.replace(f'{name} ', '')

    if await r.get(f'{m.chat.id}:Custom:{m.chat.id}{Dev_FINAL}&text={text}'):
        text = await r.get(f'{m.chat.id}:Custom:{m.chat.id}{Dev_FINAL}&text={text}')
    if await r.get(f'Custom:{Dev_FINAL}&text={text}'):
        text = await r.get(f'Custom:{Dev_FINAL}&text={text}')

    if text == 'اضف رد مميز عام' and not await r.get(f'{m.chat.id}:addFilterGS:{m.from_user.id}{Dev_FINAL}') and not await r.get(f'{m.chat.id}:addFilterGS2:{m.from_user.id}{Dev_FINAL}'):
        if not await dev2_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_replies_1731(k))
        await r.set(f'{m.chat.id}:addFilterGS:{m.from_user.id}{Dev_FINAL}', 1)
        return await m.reply(plugins_replies_1733(k))

    if await is_user_adding(m.from_user.id, m.chat.id):
        return

    if await r.get(f'{m.chat.id}:delFilterGS:{m.from_user.id}{Dev_FINAL}'):
        if text == 'الغاء':
            await r.delete(f'{m.chat.id}:delFilterGS:{m.from_user.id}{Dev_FINAL}')
            return await m.reply(plugins_replies_1741(k))
        if await dev2_pls(m.from_user.id, m.chat.id):
            if not await r.get(f'Global:{m.text}:specialfilterInfo:{Dev_FINAL}'):
                await r.delete(f'{m.chat.id}:delFilterGS:{m.from_user.id}{Dev_FINAL}')
                return await m.reply(plugins_replies_1745(k))
            await r.delete(f'Global:{m.text}:specialfilter:{Dev_FINAL}')
            await r.delete(f'Global:{m.text}:specialfiltertype:{Dev_FINAL}')
            await r.delete(f'Global:{m.text}:specialfilterInfo:{Dev_FINAL}')
            await r.srem(f'Global:SFiltersList:{Dev_FINAL}', m.text)
            await r.delete(f'{m.chat.id}:delFilterGS:{m.from_user.id}{Dev_FINAL}')
            return await m.reply(plugins_replies_1751(m.text, k))

    if text.startswith('الرد المميز العام ') and len(m.text.split()) > 3:
        if not await dev2_pls(m.from_user.id, m.chat.id): return await m.reply(plugins_replies_1754(k))
        reply = m.text.split(None, 3)[3]
        if not await r.get(f'Global:{reply}:specialfilterInfo:{Dev_FINAL}'):
            return await m.reply(plugins_replies_1757(k))
        get = await r.get(f'Global:{reply}:specialfilterInfo:{Dev_FINAL}')
        split = get.split('by=')[1]
        by = split.split('&date=')[0]
        date = split.split('&date=')[1]
        type = await r.get(f'Global:{reply}:specialfiltertype:{Dev_FINAL}')
        return await m.reply(plugins_replies_1763(k, by, html.escape(str(reply)), k, date, k, type))

    if text == 'الردود المميزه العامه':
        if not await dev2_pls(m.from_user.id, m.chat.id): return await m.reply(plugins_replies_1766(k))
        if not await r.smembers(f'Global:SFiltersList:{Dev_FINAL}'):
            return await m.reply(plugins_replies_1768(k))
        msg = 'الردود المميزه العامه:\n'
        count = 1
        for reply in await r.smembers(f'Global:SFiltersList:{Dev_FINAL}'):
            type = await r.get(f'Global:{reply}:specialfiltertype:{Dev_FINAL}')
            msg += f'\n{count} - ( {reply} )  ( {type} )'
            count += 1
        return await m.reply(msg, disable_web_page_preview=True, parse_mode=ParseMode.HTML)

    if text == 'مسح الردود المميزه العامه':
        if not await dev2_pls(m.from_user.id, m.chat.id): return await m.reply(plugins_replies_1778(k))
        if not await r.smembers(f'Global:SFiltersList:{Dev_FINAL}'):
            return await m.reply(plugins_replies_1780(k))
        total = 0
        for reply in await r.smembers(f'Global:SFiltersList:{Dev_FINAL}'):
            await r.delete(f'Global:{reply}:specialfilter:{Dev_FINAL}')
            await r.delete(f'Global:{reply}:specialfiltertype:{Dev_FINAL}')
            await r.delete(f'Global:{reply}:specialfilterInfo:{Dev_FINAL}')
            await r.srem(f'Global:SFiltersList:{Dev_FINAL}', reply)
            total += 1
        return await m.reply(plugins_replies_1788(k, total))

    if text == 'مسح رد مميز عام' and not await r.get(f'{m.chat.id}:delFilterGS:{m.from_user.id}{Dev_FINAL}'):
        if not await dev2_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_replies_1792(k))
        await r.set(f'{m.chat.id}:delFilterGS:{m.from_user.id}{Dev_FINAL}', 1)
        return await m.reply(plugins_replies_1794(k, k), parse_mode=ParseMode.HTML)

    if not await r.get(f'{m.chat.id}:lock_global_filter:{Dev_FINAL}'):
        for reply in await r.smembers(f'Global:SFiltersList:{Dev_FINAL}'):
            if reply in text:
                data = await r.get(f'Global:{reply}:specialfilter:{Dev_FINAL}')
                if data:
                    if await send_filter_reply(c, m, data, k, reply):
                        return


@Client.on_message(filters.group & filters.text & ~filters.bot, group=-228)
async def member_reply_handler(c, m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    k = await r.get(f'{Dev_FINAL}:botkey')
    await member_reply(c, m, k)

FORBIDDEN_NAMES = [
    'المدير', 'مدير', 'Admin', 'admin',
    'المالك', 'مالك', 'Owner', 'owner',
    'المطور', 'مطور', 'Developer', 'developer',
    'الادمن', 'ادمن', 'ادمني', 'ادمنية',
    'المنشئ', 'منشئ', 'مالك اساسي', 'مالكه',
    'Myth', 'مميز', 'عضو', 'المالك الاساسي',
    'اضف ردي', 'الغاء', 'تعديل', 'Dev'
]

async def member_reply(c, m, k):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if not await check_global_restrictions(c, m, k, caller='reply'):
        return

    text = m.text

    if await r.get(f'{m.chat.id}:addFilterMM:{m.from_user.id}{Dev_FINAL}'):
        if text == 'الغاء':
            await r.delete(f'{m.chat.id}:addFilterMM:{m.from_user.id}{Dev_FINAL}')
            return await m.reply(plugins_replies_1835(k))
    
        if len(m.text) <= 50:
            name_reply = m.text
            
            if name_reply in FORBIDDEN_NAMES:
                return await m.reply(plugins_replies_1841(k, name_reply))
            
            for forbidden in FORBIDDEN_NAMES:
                if name_reply.lower() == forbidden.lower():
                    return await m.reply(plugins_replies_1845(k, name_reply))
            
            if await r.get(f'{name_reply}:filterMEM:{Dev_FINAL}{m.chat.id}'):
                return await m.reply(plugins_replies_1848(k))
    
            await r.sadd(f'{m.chat.id}:FiltersListMEM:{Dev_FINAL}', f"{name_reply}&&&&{m.from_user.id}")
            await r.sadd(f'{m.chat.id}:FiltersListMEMM:{Dev_FINAL}', m.from_user.id)
            await r.set(f'{name_reply}:filterMEM:{Dev_FINAL}{m.chat.id}', m.from_user.id)
            await r.set(f"{m.from_user.id}:FILT:{m.chat.id}{Dev_FINAL}", name_reply)
            
            btn_id = f"inline_member_{name_reply}"
            await r.set(f'btn_id:inline_member:{name_reply}:{m.chat.id}', btn_id)
            user_full_name = m.from_user.first_name or name_reply
            if m.from_user.last_name:
                user_full_name += f" {m.from_user.last_name}"
            await r.set(f'btn_name:replies:{btn_id}:global', user_full_name)
            
            if "replies" not in ALL_BUTTONS:
                ALL_BUTTONS["replies"] = {"name": "أزرار الردود", "buttons": []}
            
            btn_exists = False
            for btn in ALL_BUTTONS["replies"]["buttons"]:
                if btn["id"] == btn_id:
                    btn_exists = True
                    break
            
            if not btn_exists:
                ALL_BUTTONS["replies"]["buttons"].append({
                    "id": btn_id,
                    "default": user_full_name,
                    "dynamic": True,
                    "word": name_reply,
                    "member": True
                })
            
            await refresh_dynamic_buttons(m.chat.id)
            
            await r.delete(f'{m.chat.id}:addFilterMM:{m.from_user.id}{Dev_FINAL}')
            return await m.reply(plugins_replies_1883(k, name_reply))

    if not text: return

    name = await r.get(f'{Dev_FINAL}:BotName')
    if name and text.startswith(f'{name} '):
        text = text.replace(f'{name} ', '')

    if await r.get(f'{m.chat.id}:Custom:{m.chat.id}{Dev_FINAL}&text={text}'):
        text = await r.get(f'{m.chat.id}:Custom:{m.chat.id}{Dev_FINAL}&text={text}')
    if await r.get(f'Custom:{Dev_FINAL}&text={text}'):
        text = await r.get(f'Custom:{Dev_FINAL}&text={text}')

    if text == 'اضف ردي':
        if await r.get(f'{m.chat.id}:lock_filterMEM:{Dev_FINAL}'):
            return await m.reply(plugins_replies_1898(k))
        if await r.get(f"{m.from_user.id}:FILT:{m.chat.id}{Dev_FINAL}"):
            name_exist = await r.get(f"{m.from_user.id}:FILT:{m.chat.id}{Dev_FINAL}")
            return await m.reply(plugins_replies_1901(k, name_exist))
        
        await r.set(f'{m.chat.id}:addFilterMM:{m.from_user.id}{Dev_FINAL}', 1, ex=600)
        return await m.reply(plugins_replies_1904(k))

    if await is_user_adding(m.from_user.id, m.chat.id):
        return

    if text == 'حذف ردي' or text == 'مسح ردي':
        if await r.get(f"{m.from_user.id}:FILT:{m.chat.id}{Dev_FINAL}"):
            rep = await r.get(f"{m.from_user.id}:FILT:{m.chat.id}{Dev_FINAL}")
            await r.delete(f'{rep}:filterMEM:{Dev_FINAL}{m.chat.id}')
            await r.srem(f'{m.chat.id}:FiltersListMEM:{Dev_FINAL}', f"{rep}&&&&{m.from_user.id}")
            await r.delete(f"{m.from_user.id}:FILT:{m.chat.id}{Dev_FINAL}")
            
            btn_id = f"inline_member_{rep}"
            if "replies" in ALL_BUTTONS:
                ALL_BUTTONS["replies"]["buttons"] = [
                    btn for btn in ALL_BUTTONS["replies"]["buttons"] 
                    if btn["id"] != btn_id
                ]
            
            return await m.reply(plugins_replies_1923(k, rep))
        else:
            return await m.reply(plugins_replies_1925(k))

    if text == 'حذف رده' and m.reply_to_message:
        if await gowner_pls(m.from_user.id, m.chat.id) or await owner_pls(m.from_user.id, m.chat.id):
            target_user_id = m.reply_to_message.from_user.id
            if await r.get(f"{target_user_id}:FILT:{m.chat.id}{Dev_FINAL}"):
                rep = await r.get(f"{target_user_id}:FILT:{m.chat.id}{Dev_FINAL}")
                await r.delete(f'{rep}:filterMEM:{Dev_FINAL}{m.chat.id}')
                await r.srem(f'{m.chat.id}:FiltersListMEM:{Dev_FINAL}', f"{rep}&&&&{target_user_id}")
                await r.delete(f"{target_user_id}:FILT:{m.chat.id}{Dev_FINAL}")
                
                btn_id = f"inline_member_{rep}"
                if "replies" in ALL_BUTTONS:
                    ALL_BUTTONS["replies"]["buttons"] = [
                        btn for btn in ALL_BUTTONS["replies"]["buttons"] 
                        if btn["id"] != btn_id
                    ]
                
                return await m.reply(plugins_replies_1943(k, rep))
            else:
                return await m.reply(plugins_replies_1945(k))

    if text == 'ردود الاعضاء' and await mod_pls(m.from_user.id, m.chat.id):
        if not await r.smembers(f'{m.chat.id}:FiltersListMEM:{Dev_FINAL}'):
            return await m.reply(plugins_replies_1949(k))
        msg = 'ردود الاعضاء:\n'
        count = 1
        for reply in await r.smembers(f'{m.chat.id}:FiltersListMEM:{Dev_FINAL}'):
            rep = reply.split("&&&&")[0]
            user_id = reply.split("&&&&")[1]
            try: mention = (await c.get_users(int(user_id))).mention()
            except: mention = f'<a href="tg://user?id={user_id}">{html.escape(str(user_id))}</a>'
            msg += f'\n{count} - ( {rep} )  ( {mention} )'
            count += 1
        return await m.reply(msg, disable_web_page_preview=True, parse_mode=ParseMode.HTML)

    if text == 'مسح ردود الاعضاء' and await mod_pls(m.from_user.id, m.chat.id):
        if not await r.smembers(f'{m.chat.id}:FiltersListMEM:{Dev_FINAL}'):
            return await m.reply(plugins_replies_1963(k))
        total = 0
        for reply in await r.smembers(f'{m.chat.id}:FiltersListMEM:{Dev_FINAL}'):
            rep = reply.split("&&&&")[0]
            user_id = reply.split("&&&&")[1]
            await r.delete(f'{rep}:filterMEM:{Dev_FINAL}{m.chat.id}')
            await r.srem(f'{m.chat.id}:FiltersListMEM:{Dev_FINAL}', reply)
            await r.delete(f"{user_id}:FILT:{m.chat.id}{Dev_FINAL}")
            
            btn_id = f"inline_member_{rep}"
            if "replies" in ALL_BUTTONS:
                ALL_BUTTONS["replies"]["buttons"] = [
                    btn for btn in ALL_BUTTONS["replies"]["buttons"] 
                    if btn["id"] != btn_id
                ]
            
            total += 1
        return await m.reply(plugins_replies_1980(k, total))

    if text == 'تفعيل ردود الاعضاء' and await mod_pls(m.from_user.id, m.chat.id):
        if not await r.get(f'{m.chat.id}:lock_filterMEM:{Dev_FINAL}'):
            return await m.reply(plugins_replies_1984(k, m.from_user.mention(), k), parse_mode=ParseMode.HTML)
        await r.delete(f'{m.chat.id}:lock_filterMEM:{Dev_FINAL}')
        return await m.reply(plugins_replies_1986(k, m.from_user.mention(), k), parse_mode=ParseMode.HTML)

    if text == 'تعطيل ردود الاعضاء' and await mod_pls(m.from_user.id, m.chat.id):
        if await r.get(f'{m.chat.id}:lock_filterMEM:{Dev_FINAL}'):
            return await m.reply(plugins_replies_1990(k, m.from_user.mention(), k), parse_mode=ParseMode.HTML)
        await r.set(f'{m.chat.id}:lock_filterMEM:{Dev_FINAL}', 1)
        return await m.reply(plugins_replies_1992(k, m.from_user.mention(), k), parse_mode=ParseMode.HTML)
    
    if not await r.get(f'{m.chat.id}:lock_filterMEM:{Dev_FINAL}'):
        creator_id = await r.get(f'{text}:filterMEM:{Dev_FINAL}{m.chat.id}')
        if creator_id:
            creator_id = int(creator_id)
            try:
                user_info = await c.get_chat(creator_id)
                
                user_full_name = user_info.first_name or "مستخدم"
                if user_info.last_name:
                    user_full_name += f" {user_info.last_name}"
                
                user_bio = user_info.bio if user_info.bio else "لا توجد نبذة تعريفية."
                
                btn_id = f"inline_member_{text}"
                
                btn_dict = await create_button_raw(
                    "replies",
                    btn_id,
                    user_full_name,
                    url=f"tg://user?id={creator_id}"
                )
                
                user_mention = f'<a href="tg://user?id={creator_id}">{html.escape(str(user_full_name))}</a>'
                
                caption_text = (
                    f"• Use ↤ {user_mention}\n\n"
                    f"• Bio ↤ <code>{user_bio}</code>"
                )
                
                bot_token = c.bot_token if hasattr(c, "bot_token") else settings.TOKEN
                
                photo_found = False
                async for photo in c.get_chat_photos(creator_id, limit=1):
                    await telegram_api_post(bot_token, "sendPhoto", {
                            "chat_id": m.chat.id,
                            "photo": photo.file_id,
                            "caption": caption_text,
                            "parse_mode": "HTML",
                            "disable_web_page_preview": True,
                            "reply_to_message_id": m.id,
                            "reply_markup": {
                                "inline_keyboard": [[btn_dict]]
                            }
                        })
                    photo_found = True
                    return
                if not photo_found:
                    await telegram_api_post(bot_token, "sendMessage", {
                            "chat_id": m.chat.id,
                            "text": caption_text,
                            "parse_mode": "HTML",
                            "disable_web_page_preview": True,
                            "reply_to_message_id": m.id,
                            "reply_markup": {
                                "inline_keyboard": [[btn_dict]]
                            }
                        })
                    return
                    
            except Exception as e:
                print(f"Error in Member Reply: {e}")
                fallback_text = f"• Use ↤ {text}\n\n• Bio ↤ الحساب مخفي أو خاص."
                
                await telegram_api_post(bot_token, "sendMessage", {
                        "chat_id": m.chat.id,
                        "text": fallback_text,
                        "parse_mode": "HTML",
                        "disable_web_page_preview": True,
                        "reply_to_message_id": m.id
                    })
                return


async def send_filter_reply(c, m, data, k, reply):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    try:
        user = m.from_user
        reply_to_user = m.reply_to_message.from_user if m.reply_to_message else None

        if data.startswith('type=inline&'):
            import urllib.parse
            parsed = urllib.parse.parse_qs(data)
            inline_text = parsed.get('text', [''])[0]
            btn_text = parsed.get('btn', [''])[0]
            btn_url = parsed.get('url', [''])[0]

            user_mention = f'<a href="tg://user?id={user.id}">{html.escape(str(user.first_name))}</a>'
            reply_mention = f'<a href="tg://user?id={reply_to_user.id}">{html.escape(str(reply_to_user.first_name))}</a>' if reply_to_user else ''

            inline_text = inline_text.replace('#اسمي', user.first_name if user else '')
            inline_text = inline_text.replace('#منشنه', reply_mention)
            inline_text = inline_text.replace('#منشني', user_mention)
            inline_text = inline_text.replace('#الايدي', str(reply_to_user.id if reply_to_user else ''))
            inline_text = inline_text.replace('#ايديي', str(user.id if user else ''))
            inline_text = inline_text.replace('#الاسم', reply_to_user.first_name if reply_to_user else '')

            btn_text = btn_text.replace('#اسمي', user.first_name if user else '')
            btn_text = btn_text.replace('#منشنه', reply_mention)
            btn_text = btn_text.replace('#منشني', user_mention)
            btn_text = btn_text.replace('#الايدي', str(reply_to_user.id if reply_to_user else ''))
            btn_text = btn_text.replace('#ايديي', str(user.id if user else ''))
            btn_text = btn_text.replace('#الاسم', reply_to_user.first_name if reply_to_user else '')

            inline_text = process_mentions_in_text(inline_text, user, reply_to_user)
            btn_text = process_mentions_in_text(btn_text, user, reply_to_user)

            global_key = f'Global:{reply}:filter:{Dev_FINAL}'
            local_key = f'{reply}:filter:{Dev_FINAL}{m.chat.id}'
            
            if await r.get(global_key):
                btn_id = f"inline_global_{reply}"
            elif await r.get(local_key):
                btn_id = f"inline_local_{reply}"
            else:
                btn_id = f"inline_global_{reply}"
            
            btn = await create_styled_button(
                "replies", 
                btn_id, 
                btn_text,
                url=btn_url
            )
            
            bot_token = c.bot_token if hasattr(c, "bot_token") else settings.TOKEN
            chat_id = m.chat.id
            
            await refresh_dynamic_buttons(chat_id)
            
            await telegram_api_post(bot_token, "sendMessage", {
                    "chat_id": chat_id,
                    "text": inline_text,
                    "parse_mode": "HTML",
                    "disable_web_page_preview": True,
                    "reply_to_message_id": m.id,
                    "reply_markup": {
                        "inline_keyboard": [[btn]]
                    }
                })
            return True

        user_mention = f'<a href="tg://user?id={user.id}">{html.escape(str(user.first_name))}</a>'
        reply_mention = f'<a href="tg://user?id={reply_to_user.id}">{html.escape(str(reply_to_user.first_name))}</a>' if reply_to_user else ''

        data = data.replace('#اسمي', user.first_name if user else '')
        data = data.replace('#منشنه', reply_mention)
        data = data.replace('#منشني', user_mention)
        data = data.replace('#الايدي', str(reply_to_user.id if reply_to_user else ''))
        data = data.replace('#ايديي', str(user.id if user else ''))
        data = data.replace('#الاسم', reply_to_user.first_name if reply_to_user else '')

        data = process_mentions_in_text(data, user, reply_to_user)

        if data.startswith('type=text&text='):
            text = data.replace('type=text&text=', '')
            await m.reply(text, disable_web_page_preview=True)
        elif data.startswith('type=photo&photo='):
            parts = data.split('&caption=')
            photo = parts[0].replace('type=photo&photo=', '')
            caption = parts[1] if len(parts) > 1 else ''
            if caption == 'None': caption = ''
            await m.reply_photo(photo, caption=caption)
        elif data.startswith('type=video&video='):
            parts = data.split('&caption=')
            video = parts[0].replace('type=video&video=', '')
            caption = parts[1] if len(parts) > 1 else ''
            if caption == 'None': caption = ''
            await m.reply_video(video, caption=caption)
        elif data.startswith('type=animation&animation='):
            parts = data.split('&caption=')
            anim = parts[0].replace('type=animation&animation=', '')
            caption = parts[1] if len(parts) > 1 else ''
            if caption == 'None': caption = ''
            await m.reply_animation(anim, caption=caption)
        elif data.startswith('type=audio&audio='):
            parts = data.split('&caption=')
            audio = parts[0].replace('type=audio&audio=', '')
            caption = parts[1] if len(parts) > 1 else ''
            if caption == 'None': caption = ''
            await m.reply_audio(audio, caption=caption)
        elif data.startswith('type=voice&voice='):
            parts = data.split('&caption=')
            voice = parts[0].replace('type=voice&voice=', '')
            caption = parts[1] if len(parts) > 1 else ''
            if caption == 'None': caption = ''
            await m.reply_voice(voice, caption=caption)
        elif data.startswith('type=doc&doc='):
            parts = data.split('&caption=')
            doc = parts[0].replace('type=doc&doc=', '')
            caption = parts[1] if len(parts) > 1 else ''
            if caption == 'None': caption = ''
            await m.reply_document(doc, caption=caption)
        elif data.startswith('type=sticker&sticker='):
            sticker = data.replace('type=sticker&sticker=', '')
            await m.reply_sticker(sticker)
            
        return False
    except Exception as e:
        print(f"Error in send_filter_reply: {e}")
        return False


async def send_multi_reply(c, m, data, k, reply):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    try:
        user = m.from_user
        reply_to_user = m.reply_to_message.from_user if m.reply_to_message else None

        user_mention = f'<a href="tg://user?id={user.id}">{html.escape(str(user.first_name))}</a>'
        reply_mention = f'<a href="tg://user?id={reply_to_user.id}">{html.escape(str(reply_to_user.first_name))}</a>' if reply_to_user else ''

        if isinstance(data, str):
            data = data.replace('#اسمي', user.first_name if user else '')
            data = data.replace('#منشنه', reply_mention)
            data = data.replace('#منشني', user_mention)
            data = data.replace('#الايدي', str(reply_to_user.id if reply_to_user else ''))
            data = data.replace('#ايديي', str(user.id if user else ''))
            data = data.replace('#الاسم', reply_to_user.first_name if reply_to_user else '')

            data = process_mentions_in_text(data, user, reply_to_user)

        if not data.startswith('type='):
            await m.reply(data, disable_web_page_preview=True)
        elif data.startswith('type=photo&photo='):
            parts = data.split('&caption=')
            photo = parts[0].replace('type=photo&photo=', '')
            caption = parts[1] if len(parts) > 1 else ''
            if caption == 'None': caption = ''
            await m.reply_photo(photo, caption=caption)
        elif data.startswith('type=video&video='):
            parts = data.split('&caption=')
            video = parts[0].replace('type=video&video=', '')
            caption = parts[1] if len(parts) > 1 else ''
            if caption == 'None': caption = ''
            await m.reply_video(video, caption=caption)
        elif data.startswith('type=animation&animation='):
            parts = data.split('&caption=')
            anim = parts[0].replace('type=animation&animation=', '')
            caption = parts[1] if len(parts) > 1 else ''
            if caption == 'None': caption = ''
            await m.reply_animation(anim, caption=caption)
        elif data.startswith('type=audio&audio='):
            parts = data.split('&caption=')
            audio = parts[0].replace('type=audio&audio=', '')
            caption = parts[1] if len(parts) > 1 else ''
            if caption == 'None': caption = ''
            await m.reply_audio(audio, caption=caption)
        elif data.startswith('type=voice&voice='):
            parts = data.split('&caption=')
            voice = parts[0].replace('type=voice&voice=', '')
            caption = parts[1] if len(parts) > 1 else ''
            if caption == 'None': caption = ''
            await m.reply_voice(voice, caption=caption)
        elif data.startswith('type=doc&doc='):
            parts = data.split('&caption=')
            doc = parts[0].replace('type=doc&doc=', '')
            caption = parts[1] if len(parts) > 1 else ''
            if caption == 'None': caption = ''
            await m.reply_document(doc, caption=caption)
        elif data.startswith('type=sticker&sticker='):
            sticker = data.replace('type=sticker&sticker=', '')
            await m.reply_sticker(sticker)
    except Exception as e:
        print(f"Error in send_multi_reply: {e}")