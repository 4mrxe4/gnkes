from helpers.context import get_global_r, get_global_dev, get_global_k
from helpers.gender import (
    set_user_gender, get_gender, get_gender_map, 
    add_gender_word, remove_gender_word, save_gender_map, DEFAULT_GENDER_MAP
)
from helpers.ranks import *
from compat import Client, filters
from helpers.replies_store import (
    plugins_gender_107,
    plugins_gender_109,
    plugins_gender_113,
    plugins_gender_126,
    plugins_gender_131,
    plugins_gender_133,
    plugins_gender_137,
    plugins_gender_140,
    plugins_gender_143,
    plugins_gender_151,
    plugins_gender_163,
    plugins_gender_169,
    plugins_gender_171,
    plugins_gender_175,
    plugins_gender_180,
    plugins_gender_182,
    plugins_gender_29,
    plugins_gender_33,
    plugins_gender_38,
    plugins_gender_40,
    plugins_gender_45,
    plugins_gender_49,
    plugins_gender_63,
    plugins_gender_66,
    plugins_gender_69,
    plugins_gender_77,
    plugins_gender_82,
    plugins_gender_86,
    plugins_gender_90,
    plugins_gender_95,
    plugins_gender_99,
)

@Client.on_message(filters.text & filters.group, group=-1235)
async def handle_gender_commands(c, m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    
    if not m.text or not m.from_user or m.from_user.is_bot:
        return
    
    txt = m.text.strip()
    user_id = m.from_user.id
    
    if not await check_global_restrictions(c, m, k):
        return
    
    if not await is_service_enabled(Dev_FINAL, 'sex'):
        return
    
    if txt in ["تحديد جنسي ولد", "تحديد الجنس ولد"]:
        await set_user_gender(user_id, "male")
        return await m.reply(plugins_gender_29(k))
        
    if txt in ["تحديد جنسي بنت", "تحديد الجنس بنت"]:
        await set_user_gender(user_id, "female")
        return await m.reply(plugins_gender_33(k))
    
    if txt == "جنسي":
        gender = await get_gender(user_id)
        if gender == "male":
            return await m.reply(plugins_gender_38(k))
        else:
            return await m.reply(plugins_gender_40(k))
    
    
    if txt in ["كلمات الجنس", "قائمة كلمات الجنس"]:
        if not await dev2_pls(user_id, m.chat.id):
            return await m.reply(plugins_gender_45(k))
        
        gender_map = await get_gender_map(Dev_FINAL)
        if not gender_map:
            return await m.reply(plugins_gender_49(k))
        
        msg = "قائمة كلمات الجنس:\n\n"
        count = 1
        sorted_items = sorted(gender_map.items(), key=lambda x: len(x[0]), reverse=True)
        for word, female in sorted_items:
            msg += f"{count} - {word} → {female}\n"
            count += 1
        
        msg += f"\n{k} العدد: {len(gender_map)}"
        return await m.reply(msg)
    
    if txt in ["اضف كلمة جنس", "اضف كلمه جنس"]:
        if not await dev2_pls(user_id, m.chat.id):
            return await m.reply(plugins_gender_63(k))
        
        if await r.get(f'{m.chat.id}:addGenderWord:{user_id}{Dev_FINAL}'):
            return await m.reply(plugins_gender_66(k))
        
        await r.set(f'{m.chat.id}:addGenderWord:{user_id}{Dev_FINAL}', 1, ex=600)
        return await m.reply(plugins_gender_69(k))
    
    step = await r.get(f'{m.chat.id}:addGenderWord:{user_id}{Dev_FINAL}')
    if step and await dev2_pls(user_id, m.chat.id):
        
        if txt == "الغاء":
            await r.delete(f'{m.chat.id}:addGenderWord:{user_id}{Dev_FINAL}')
            await r.delete(f'{m.chat.id}:addGenderWordOld:{user_id}{Dev_FINAL}')
            return await m.reply(plugins_gender_77(k))
        
        if step == "1":
            old_word = txt.strip()
            if len(old_word) < 1:
                return await m.reply(plugins_gender_82(k))
            
            gender_map = await get_gender_map(Dev_FINAL)
            if old_word.lower() in gender_map:
                return await m.reply(plugins_gender_86(k))
            
            await r.set(f'{m.chat.id}:addGenderWordOld:{user_id}{Dev_FINAL}', old_word)
            await r.set(f'{m.chat.id}:addGenderWord:{user_id}{Dev_FINAL}', "2")
            return await m.reply(plugins_gender_90(k, old_word))
        
        elif step == "2":
            new_word = txt.strip()
            if len(new_word) < 1:
                return await m.reply(plugins_gender_95(k))
            
            old_word = await r.get(f'{m.chat.id}:addGenderWordOld:{user_id}{Dev_FINAL}')
            if not old_word:
                return await m.reply(plugins_gender_99(k))
            
            result = await add_gender_word(old_word, new_word, Dev_FINAL)
            
            await r.delete(f'{m.chat.id}:addGenderWord:{user_id}{Dev_FINAL}')
            await r.delete(f'{m.chat.id}:addGenderWordOld:{user_id}{Dev_FINAL}')
            
            if result:
                return await m.reply(plugins_gender_107(k, old_word, new_word))
            else:
                return await m.reply(plugins_gender_109(k))
    
    if txt.startswith("حذف كلمة جنس "):
        if not await dev2_pls(user_id, m.chat.id):
            return await m.reply(plugins_gender_113(k))
        
        parts = txt.split(maxsplit=3)
        word_to_remove = parts[2] if len(parts) == 3 else parts[3]
        
        gender_map = await get_gender_map(Dev_FINAL)
        found = None
        for key in gender_map:
            if key.lower() == word_to_remove.lower():
                found = key
                break
        
        if not found:
            return await m.reply(plugins_gender_126(k))
        
        result = await remove_gender_word(found, Dev_FINAL)
        
        if result:
            return await m.reply(plugins_gender_131(k, found))
        else:
            return await m.reply(plugins_gender_133(k))
    
    if txt in ["حذف كلمة جنس", "مسح كلمة جنس"] and not txt.startswith("حذف كلمة جنس "):
        if not await dev2_pls(user_id, m.chat.id):
            return await m.reply(plugins_gender_137(k))
        
        if await r.get(f'{m.chat.id}:delGenderWord:{user_id}{Dev_FINAL}'):
            return await m.reply(plugins_gender_140(k))
        
        await r.set(f'{m.chat.id}:delGenderWord:{user_id}{Dev_FINAL}', 1, ex=600)
        return await m.reply(plugins_gender_143(k))
    
    if await r.get(f'{m.chat.id}:delGenderWord:{user_id}{Dev_FINAL}'):
        if not await dev2_pls(user_id, m.chat.id):
            return
        
        if txt == "الغاء":
            await r.delete(f'{m.chat.id}:delGenderWord:{user_id}{Dev_FINAL}')
            return await m.reply(plugins_gender_151(k))
        
        word_to_remove = txt.strip()
        gender_map = await get_gender_map(Dev_FINAL)
        
        found = None
        for key in gender_map:
            if key.lower() == word_to_remove.lower():
                found = key
                break
        
        if not found:
            return await m.reply(plugins_gender_163(k))
        
        result = await remove_gender_word(found, Dev_FINAL)
        await r.delete(f'{m.chat.id}:delGenderWord:{user_id}{Dev_FINAL}')
        
        if result:
            return await m.reply(plugins_gender_169(k, found))
        else:
            return await m.reply(plugins_gender_171(k))
    
    if txt in ["تصفير كلمات الجنس", "استعادة كلمات الجنس"]:
        if not await dev2_pls(user_id, m.chat.id):
            return await m.reply(plugins_gender_175(k))
        
        result = await save_gender_map(DEFAULT_GENDER_MAP, Dev_FINAL)
        
        if result:
            return await m.reply(plugins_gender_180(k, len(DEFAULT_GENDER_MAP)))
        else:
            return await m.reply(plugins_gender_182(k))