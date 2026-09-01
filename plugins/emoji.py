
from helpers.context import get_global_r, get_global_dev, get_global_k
from helpers.emoji import (
    get_custom_emoji_mappings,
    save_custom_emoji_mapping,
    delete_custom_emoji_mapping,
    clear_all_custom_emojis,
    detect_emoji_position,
    get_replacement_mappings,
    save_replacement_mapping,
    delete_replacement_mapping,
    clear_all_replacements,
    REPLACE_TYPE_EMOJI,
    REPLACE_TYPE_TEXT,
    REPLACE_TYPE_EMOJI_WITH_TEXT,
)
from helpers.ranks import *
from compat import Client, filters
from compat import MessageEntityType
from helpers.replies_store import (
    plugins_emoji_132,
    plugins_emoji_136,
    plugins_emoji_139,
    plugins_emoji_163,
    plugins_emoji_166,
    plugins_emoji_169,
    plugins_emoji_174,
    plugins_emoji_187,
    plugins_emoji_195,
    plugins_emoji_199,
    plugins_emoji_201,
    plugins_emoji_205,
    plugins_emoji_207,
    plugins_emoji_211,
    plugins_emoji_213,
    plugins_emoji_221,
    plugins_emoji_224,
    plugins_emoji_232,
    plugins_emoji_241,
    plugins_emoji_250,
    plugins_emoji_252,
    plugins_emoji_256,
    plugins_emoji_259,
    plugins_emoji_278,
    plugins_emoji_281,
    plugins_emoji_286,
    plugins_emoji_299,
    plugins_emoji_307,
    plugins_emoji_44,
    plugins_emoji_46,
    plugins_emoji_54,
    plugins_emoji_60,
    plugins_emoji_68,
    plugins_emoji_75,
)

user_sessions = {}

@Client.on_message(filters.group, group=-1236)
async def handle_custom_emoji_commands(c, m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if not await check_global_restrictions(c, m, k):
        return
    if not m.from_user or m.from_user.is_bot:
        return

    user_id = m.from_user.id
    chat_id = m.chat.id
    txt = (m.text or "").strip()

    if not await r.get(f'{m.chat.id}:enable:{Dev_FINAL}'):
        return

    session_key = f"{Dev_FINAL}:{chat_id}:{user_id}"

    if txt == "استبدال نص":
        if not await dev2_pls(user_id, m.chat.id):
            return await m.reply(plugins_emoji_44(k))
        user_sessions[session_key] = {'step': 1}
        return await m.reply(plugins_emoji_46(k))

    if session_key in user_sessions and user_sessions[session_key].get('step') == 1:
        if not await dev2_pls(user_id, m.chat.id):
            user_sessions.pop(session_key, None)
            return
        if txt == "الغاء":
            user_sessions.pop(session_key, None)
            return await m.reply(plugins_emoji_54(k))
        
        user_sessions[session_key] = {
            'step': 2,
            'old_text': txt
        }
        return await m.reply(plugins_emoji_60(k))

    if session_key in user_sessions and user_sessions[session_key].get('step') == 2:
        if not await dev2_pls(user_id, m.chat.id):
            user_sessions.pop(session_key, None)
            return
        if txt == "الغاء":
            user_sessions.pop(session_key, None)
            return await m.reply(plugins_emoji_68(k))

        old_text = user_sessions[session_key].get('old_text')
        new_text = txt
        
        if not old_text:
            user_sessions.pop(session_key, None)
            return await m.reply(plugins_emoji_75(k))
        
        custom_entities = [e for e in (m.entities or []) if e.type == MessageEntityType.CUSTOM_EMOJI]
        
        emoji_char = ""
        for char in new_text:
            if ord(char) > 0xFFFF or (0x1F000 <= ord(char) <= 0x1FFFF):
                emoji_char = char
                break
        
        clean_text = new_text
        if emoji_char:
            clean_text = new_text.replace(emoji_char, "").strip()
        
        if custom_entities and emoji_char:
            custom_emoji_id = custom_entities[0].custom_emoji_id
            
            if clean_text:
                success = await save_replacement_mapping(
                    old_text=old_text,
                    replacement_text=clean_text,
                    custom_emoji_id=custom_emoji_id,
                    emoji_char=emoji_char,
                    replace_type=REPLACE_TYPE_EMOJI_WITH_TEXT,
                    bot_id=Dev_FINAL
                )
                emoji_tag = f'<tg-emoji emoji-id="{custom_emoji_id}">{emoji_char}</tg-emoji>'
                new_display = f"{emoji_tag} {clean_text}"
                old_display = old_text
            else:
                success = await save_replacement_mapping(
                    old_text=old_text,
                    replacement_text="",
                    custom_emoji_id=custom_emoji_id,
                    emoji_char=emoji_char,
                    replace_type=REPLACE_TYPE_EMOJI,
                    bot_id=Dev_FINAL
                )
                emoji_tag = f'<tg-emoji emoji-id="{custom_emoji_id}">{emoji_char}</tg-emoji>'
                new_display = emoji_tag
                old_display = old_text
        else:
            success = await save_replacement_mapping(
                old_text=old_text,
                replacement_text=new_text,
                replace_type=REPLACE_TYPE_TEXT,
                bot_id=Dev_FINAL
            )
            new_display = new_text
            old_display = old_text

        user_sessions.pop(session_key, None)

        if success:
            reply_text = f"{k} تم استبدال\nالسابق ⇜ <code>{old_display}</code>\nالجديد ⇜ {new_display}"
            return await m.reply(reply_text)
        else:
            return await m.reply(plugins_emoji_132(k))

    if txt in ["عرض الاستبدال", "استبدالات", "الاستبدالات"]:
        if not await dev2_pls(user_id, m.chat.id):
            return await m.reply(plugins_emoji_136(k))
        mappings = await get_replacement_mappings(Dev_FINAL)
        if not mappings:
            return await m.reply(plugins_emoji_139(k))
        text = f"{k} <b>الاستبدالات الحالية:</b>\n\n"
        for old, data in mappings.items():
            replace_type = data.get("replace_type", REPLACE_TYPE_TEXT)
            replacement = data.get("replacement_text", "")
            emoji_char = data.get("emoji_char", "")
            custom_emoji_id = data.get("custom_emoji_id", "")
            type_label = {
                REPLACE_TYPE_EMOJI: "إيموجي مميز",
                REPLACE_TYPE_TEXT: "نص",
                REPLACE_TYPE_EMOJI_WITH_TEXT: "إيموجي + نص"
            }.get(replace_type, "نص")
            if custom_emoji_id and emoji_char:
                emoji_tag = f'<tg-emoji emoji-id="{custom_emoji_id}">{emoji_char}</tg-emoji>'
                if replacement:
                    text += f"<code>{old}</code> ↢ {emoji_tag} {replacement} [{type_label}]\n"
                else:
                    text += f"<code>{old}</code> ↢ {emoji_tag} [{type_label}]\n"
            else:
                text += f"<code>{old}</code> ↢ {replacement} [{type_label}]\n"
        return await m.reply(text)

    if txt.startswith("حذف استبدال "):
        if not await dev2_pls(user_id, m.chat.id):
            return await m.reply(plugins_emoji_163(k))
        old_text_to_delete = txt[11:].strip()
        if not old_text_to_delete:
            return await m.reply(plugins_emoji_166(k))
        success = await delete_replacement_mapping(old_text_to_delete, Dev_FINAL)
        if success:
            return await m.reply(plugins_emoji_169(k, old_text_to_delete))
        mappings = await get_custom_emoji_mappings(Dev_FINAL)
        if old_text_to_delete in mappings:
            success = await delete_custom_emoji_mapping(old_text_to_delete, Dev_FINAL)
            if success:
                return await m.reply(plugins_emoji_174(k, old_text_to_delete))
        found = []
        search_words = old_text_to_delete.split()
        all_mappings = await get_replacement_mappings(Dev_FINAL)
        for key in all_mappings.keys():
            key_words = key.split()
            for word in search_words:
                if word in key_words:
                    found.append(key)
                    break
        if len(found) == 1:
            success = await delete_replacement_mapping(found[0], Dev_FINAL)
            if success:
                return await m.reply(plugins_emoji_187(k, found[0]))
        elif len(found) > 1:
            text = f"{k} وجدت عدة تطابقات:\n\n"
            for i, key in enumerate(found, 1):
                text += f"{i}. <code>{key}</code>\n"
            text += f"\nاستخدم: <code>حذف استبدال [النص بالضبط]</code>"
            return await m.reply(text)
        else:
            return await m.reply(plugins_emoji_195(k))

    if txt in ["مسح الاستبدالات", "تصفير الاستبدالات"]:
        if not await dev2_pls(user_id, m.chat.id):
            return await m.reply(plugins_emoji_199(k))
        await clear_all_replacements(Dev_FINAL)
        return await m.reply(plugins_emoji_201(k))

    if txt in ["تصفير الايموجيات المميزة", "حذف كل الايموجيات المميزة"]:
        if not await dev2_pls(user_id, m.chat.id):
            return await m.reply(plugins_emoji_205(k))
        await clear_all_custom_emojis(Dev_FINAL)
        return await m.reply(plugins_emoji_207(k))

    if txt in ["اضف ايموجي مميز", "إضافة ايموجي مميز"]:
        if not await dev2_pls(user_id, m.chat.id):
            return await m.reply(plugins_emoji_211(k))
        user_sessions[session_key] = {'step': 3}
        return await m.reply(plugins_emoji_213(k))

    if session_key in user_sessions and user_sessions[session_key].get('step') == 3:
        if not await dev2_pls(user_id, m.chat.id):
            user_sessions.pop(session_key, None)
            return
        if txt == "الغاء":
            user_sessions.pop(session_key, None)
            return await m.reply(plugins_emoji_221(k))
        user_sessions[session_key]['old_text'] = txt
        user_sessions[session_key]['step'] = 4
        return await m.reply(plugins_emoji_224(k))

    if session_key in user_sessions and user_sessions[session_key].get('step') == 4:
        if not await dev2_pls(user_id, m.chat.id):
            user_sessions.pop(session_key, None)
            return
        if txt == "الغاء":
            user_sessions.pop(session_key, None)
            return await m.reply(plugins_emoji_232(k))

        old_text = user_sessions[session_key]['old_text']
        new_text = txt

        custom_entity = next(
            (e for e in (m.entities or []) if e.type == MessageEntityType.CUSTOM_EMOJI), None
        )
        if not custom_entity:
            return await m.reply(plugins_emoji_241(k))

        custom_emoji_id = custom_entity.custom_emoji_id
        emoji_position = detect_emoji_position(new_text, m.entities)
        
        success = await save_custom_emoji_mapping(old_text, new_text, custom_emoji_id, emoji_position, Dev_FINAL)
        user_sessions.pop(session_key, None)
        
        if success:
            return await m.reply(plugins_emoji_250(k))
        else:
            return await m.reply(plugins_emoji_252(k))

    if txt in ["عرض الايموجيات المميزه", "الايموجيات المخصصة", "عرض الايموجيات"]:
        if not await dev2_pls(user_id, m.chat.id):
            return await m.reply(plugins_emoji_256(k))
        mappings = await get_custom_emoji_mappings(Dev_FINAL)
        if not mappings:
            return await m.reply(plugins_emoji_259(k))
        text = f"{k} <b>الايموجيات المخصصة:</b>\n\n"
        for old, data in mappings.items():
            if isinstance(data, dict):
                new_text = data.get("new_text", "")
                emoji_id = data.get("custom_emoji_id", "")
                position = "بداية" if data.get("position", "end") == "start" else "نهاية"
            else:
                new_text = str(data)
                emoji_id = ""
                position = "نهاية"
            if emoji_id:
                text += f"<code>{old}</code> ↢ {new_text} [{position}]\n"
            else:
                text += f"<code>{old}</code> ↢ {new_text} [{position}]\n"
        return await m.reply(text)

    if txt.startswith("حذف ايموجي "):
        if not await dev2_pls(user_id, m.chat.id):
            return await m.reply(plugins_emoji_278(k))
        old_text_to_delete = txt[10:].strip()
        if not old_text_to_delete:
            return await m.reply(plugins_emoji_281(k))
        mappings = await get_custom_emoji_mappings(Dev_FINAL)
        if old_text_to_delete in mappings:
            success = await delete_custom_emoji_mapping(old_text_to_delete, Dev_FINAL)
            if success:
                return await m.reply(plugins_emoji_286(k, old_text_to_delete))
        found = []
        search_words = old_text_to_delete.split()
        for key in mappings.keys():
            key_words = key.split()
            for word in search_words:
                if word in key_words:
                    found.append(key)
                    break
        found = list(dict.fromkeys(found))
        if len(found) == 1:
            success = await delete_custom_emoji_mapping(found[0], Dev_FINAL)
            if success:
                return await m.reply(plugins_emoji_299(k, found[0]))
        elif len(found) > 1:
            text = f"{k} وجدت عدة تطابقات:\n\n"
            for i, key in enumerate(found, 1):
                text += f"{i}. <code>{key}</code>\n"
            text += f"\nاستخدم: <code>حذف ايموجي [النص بالضبط]</code>"
            return await m.reply(text)
        else:
            return await m.reply(plugins_emoji_307(k))
