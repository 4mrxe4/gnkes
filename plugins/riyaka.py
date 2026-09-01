from helpers.context import get_global_r, get_global_dev, get_global_k
r = get_global_r()
Dev_FINAL = get_global_dev()
k = get_global_k()
import re
import json
from compat import *
from compat import *
from compat import *
from helpers.ranks import *
from helpers.replies_store import (
    REPLIES,
    plugins_riyaka_128,
    plugins_riyaka_145,
    plugins_riyaka_201,
    plugins_riyaka_209,
    plugins_riyaka_221,
    plugins_riyaka_44,
    plugins_riyaka_60,
    plugins_riyaka_62,
    plugins_riyaka_67,
    plugins_riyaka_69,
    plugins_riyaka_74,
    plugins_riyaka_77,
    plugins_riyaka_82,
    plugins_riyaka_88,
    plugins_riyaka_95,
)


ALLOWED_REACTIONS = [
    "👍", "👎", "❤️", "🔥", "🥰", "👏", "😁", "🤔", "🤯", "😱",
    "🤬", "😢", "🎉", "🤩", "🤮", "💩", "🙏", "👌", "🕊", "🤡",
    "🥱", "🥴", "😍", "🐳", "❤‍🔥", "🌚", "🌭", "💯", "🤣", "⚡️",
    "🍌", "🏆", "💔", "🤨", "😐", "🍓", "🍾", "💋", "🖕", "😈",
    "😴", "😭", "🤓", "👻", "👨‍💻", "👀", "🎃", "🙈", "😇", "😨",
    "🤝", "✍️", "🤗", "🫡", "🎅", "🎄", "☃️", "💅", "🤪", "🗿",
    "🆒", "💘", "🙉", "🦄", "😘", "💊", "🙊", "😎", "👾",
    "🤷‍♂️", "🤷", "🤷‍♀️", "😡"
]

# صيغة أمر رتب التفاعل التلقائية من plugins/upfake.py (مثال: ضع تفاعل 500 مالك)
# محجوزة، ولازم نستثنيها هنا حتى لا نتعامل معها كتفاعل نصي مخصص
# تعبير منتظم للتحقق مما إذا كان الأمر يخص تفاعل الرتب التلقائي (الرقم في البداية أو النهاية مع رتبة)
_AUTO_RANK_TIER_CMD = re.compile(r'^ضع تفاعل\s+(\d+\s+(مميز|ادمن|مدير|مالك)|(مميز|ادمن|مدير|مالك)\s+\d+)$')

@Client.on_message(filters.group & filters.text, group=626)
async def reaction_commands(c, m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    text = m.text.strip()
    commands = ['فتح التفاعل', 'قفل التفاعل']

    # استثناء أوامر تفاعل الرتب التلقائية سواء كان الرقم بداخله في البداية أو النهاية
    if text.startswith('ضع تفاعل ') and _AUTO_RANK_TIER_CMD.match(text):
        return

    if text in commands or text.startswith('ضع تفاعل ') or text.startswith('حذف تفاعل '):
        k = await r.get(f'{Dev_FINAL}:botkey')
        if not await dev2_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_riyaka_44(k))
        await reaction_cmds(c, m, k)


async def reaction_cmds(c, m, k):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if not await check_global_restrictions(c, m, k):
        return
    
    text = m.text.strip()
    
    if text == 'فتح التفاعل':
        if await r.get(f'{m.chat.id}:lock_reactions:{Dev_FINAL}'):
            await r.delete(f'{m.chat.id}:lock_reactions:{Dev_FINAL}')
            return await m.reply(plugins_riyaka_60(k))
        else:
            return await m.reply(plugins_riyaka_62(k))
    
    elif text == 'قفل التفاعل':
        if not await r.get(f'{m.chat.id}:lock_reactions:{Dev_FINAL}'):
            await r.set(f'{m.chat.id}:lock_reactions:{Dev_FINAL}', '1')
            return await m.reply(plugins_riyaka_67(k))
        else:
            return await m.reply(plugins_riyaka_69(k))
    
    elif text.startswith('ضع تفاعل '):
        reactgg = text.replace('ضع تفاعل ', '').strip()
        if not reactgg:
            return await m.reply(plugins_riyaka_74(k))
        
        await r.set(f'{m.chat.id}:reaction_wait:{m.from_user.id}:{Dev_FINAL}', reactgg)
        return await m.reply(plugins_riyaka_77(k))
    
    elif text.startswith('حذف تفاعل '):
        reactgg = text.replace('حذف تفاعل ', '').strip()
        if not reactgg:
            return await m.reply(plugins_riyaka_82(k))
        
        reaction_key = f'global:reaction:{reactgg}:{Dev_FINAL}'
        if await r.get(reaction_key):
            await r.delete(reaction_key)
            await r.srem(f'global:reactions_list:{Dev_FINAL}', reactgg)
            return await m.reply(plugins_riyaka_88(k, reactgg))
        else:
            return 
    
    elif text == 'الغاء':
        if await r.get(f'{m.chat.id}:reaction_wait:{m.from_user.id}:{Dev_FINAL}'):
            await r.delete(f'{m.chat.id}:reaction_wait:{m.from_user.id}:{Dev_FINAL}')
            return await m.reply(plugins_riyaka_95(k))

@Client.on_message(filters.group & filters.text, group=627)
async def handle_reaction_emoji(c, m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    text = m.text.strip()
    
    # تجاهل رسائل ضع تفاعل إذا كانت تخص رتب الأعداد (سواء الرقم بالبداية أو النهاية)
    if text.startswith('ضع تفاعل ') and _AUTO_RANK_TIER_CMD.match(text):
        return
    if text.startswith('ضع تفاعل '):
        return
        
    k = await r.get(f'{Dev_FINAL}:botkey')
    await reaction_emoji_handler(c, m, k)


async def reaction_emoji_handler(c, m, k):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if not await check_global_restrictions(c, m, k):
        return
    wait_key = f'{m.chat.id}:reaction_wait:{m.from_user.id}:{Dev_FINAL}'
    reactgg = await r.get(wait_key)
    
    if not reactgg:
        return
    
    text = m.text.strip()
    
    if text == 'الغاء':
        await r.delete(wait_key)
        return await m.reply(plugins_riyaka_128(k))
    
    cleaned_text = text.replace('\ufe0f', '').replace('\ufe0e', '')
    allowed_cleaned = [e.replace('\ufe0f', '').replace('\ufe0e', '') for e in ALLOWED_REACTIONS]
    
    if cleaned_text not in allowed_cleaned:
        return await m.reply(
            REPLIES['plugins_riyaka_134']
        )
    
    reaction_key = f'global:reaction:{reactgg}:{Dev_FINAL}'
    await r.set(reaction_key, text)
    await r.sadd(f'global:reactions_list:{Dev_FINAL}', reactgg)
    
    await r.delete(wait_key)
    
    await m.reply(
        plugins_riyaka_145(k, k, reactgg, k, text, k, reactgg)        
    )

@Client.on_message(filters.group & filters.text, group=628)
async def auto_reaction(c, m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    k = await r.get(f'{Dev_FINAL}:botkey')
    await auto_react_handler(c, m, k)

async def auto_react_handler(c, m, k):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if not await check_global_restrictions(c, m, k):
        return
    
    text = m.text.strip()
    
    reactions_list = await r.smembers(f'global:reactions_list:{Dev_FINAL}')
    
    if not reactions_list:
        return
    
    for reactgg in reactions_list:
        pattern = rf'(?<!\S){re.escape(reactgg)}(?!\S)'
        if re.search(pattern, text, flags=re.IGNORECASE):
            emoji = await r.get(f'global:reaction:{reactgg}:{Dev_FINAL}')
            if emoji:
                try:
                    await m.react(emoji)
                except Exception as e:
                    print(f"Error putting reaction: {e}")
                break

@Client.on_message(filters.group & filters.text, group=629)
async def list_reactions(c, m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    k = await r.get(f'{Dev_FINAL}:botkey')
    await list_reactions_cmd(c, m, k)

async def list_reactions_cmd(c, m, k):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if not await check_global_restrictions(c, m, k):
        return
    if m.text.strip() != 'التفاعلات':
        return

    if not await dev2_pls(m.from_user.id, m.chat.id):
        return await m.reply(plugins_riyaka_201(k))
    
    if not await r.get(f'{m.chat.id}:enable:{Dev_FINAL}'):
        return
    
    reactions_list = await r.smembers(f'global:reactions_list:{Dev_FINAL}')
    
    if not reactions_list:
        return await m.reply(plugins_riyaka_209(k))
    
    text = 'هاي قائمة التفاعلات العامة المحفوظه\n\n'
    count = 1
    
    for reactgg in reactions_list:
        emoji = await r.get(f'global:reaction:{reactgg}:{Dev_FINAL}')
        if emoji:
            text += f'{count}. `{reactgg}` → {emoji}\n'
            count += 1
    
    if count == 1:
        return await m.reply(plugins_riyaka_221(k))
    
    await m.reply(text)
