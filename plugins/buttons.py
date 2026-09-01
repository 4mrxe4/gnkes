from helpers.context import get_global_r, get_global_dev, get_global_k
from helpers.emoji import utf16_offset_to_py_index
import asyncio
import json
import uuid
from compat import Client, filters
from compat import InlineKeyboardMarkup, InlineKeyboardButton
from compat import MessageEntityType
from helpers.ranks import *

ALL_BUTTONS = {}

def register_buttons(buttons_dict):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    global ALL_BUTTONS
    ALL_BUTTONS.update(buttons_dict)
    return True

def get_all_buttons():
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    return ALL_BUTTONS

async def get_button_custom(module, button_id):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    custom_name = await r.get(f"btn_name:{module}:{button_id}:global")
    if custom_name:
        return custom_name.decode("utf-8") if isinstance(custom_name, bytes) else custom_name
    return None

async def get_button_color(module, button_id):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    custom_color = await r.get(f"btn_color:{module}:{button_id}:global")
    if custom_color:
        return custom_color.decode("utf-8") if isinstance(custom_color, bytes) else custom_color
    return None

async def get_button_emoji(module, button_id):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    emoji_id = await r.get(f"btn_emoji:{module}:{button_id}:global")
    if emoji_id:
        return emoji_id.decode("utf-8") if isinstance(emoji_id, bytes) else emoji_id
    return None

async def get_button_emoji_char(module, button_id):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    emoji_char = await r.get(f"btn_emoji_char:{module}:{button_id}:global")
    if emoji_char:
        return emoji_char.decode("utf-8") if isinstance(emoji_char, bytes) else emoji_char
    return None

async def create_custom_button(module, button_id, default_text, callback_data=None):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    text = await get_button_custom(module, button_id) or default_text
    color = await get_button_color(module, button_id) or "default"
    emoji_id = await get_button_emoji(module, button_id)
    
    if callback_data:
        btn = InlineKeyboardButton(text=text, callback_data=callback_data)
    else:
        btn = InlineKeyboardButton(text=text, callback_data=f"{module}:{button_id}")
    
    if emoji_id:
        btn.icon_custom_emoji_id = emoji_id
    
    if color != "default":
        btn.style = color
    return btn

async def create_button(module, button_id, default_text, callback_data=None):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    return await create_custom_button(module, button_id, default_text, callback_data)

async def create_button_row(module, button_id, default_text, callback_data=None):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    return await create_custom_button(module, button_id, default_text, callback_data)

async def create_button_raw(module, button_id, default_text, **kwargs):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    
    if button_id.startswith("inline_global_") or button_id.startswith("inline_local_") or button_id.startswith("inline_member_"):
        lookup_id = f"btn_text_{default_text}"
        text = await get_button_custom("replies", lookup_id) or default_text
        color = await get_button_color("replies", lookup_id) or "default"
        emoji_id = await get_button_emoji("replies", lookup_id)
    else:
        text = await get_button_custom(module, button_id) or default_text
        color = await get_button_color(module, button_id) or "default"
        emoji_id = await get_button_emoji(module, button_id)
    
    btn_dict = {"text": text}
    
    if emoji_id:
        btn_dict["icon_custom_emoji_id"] = emoji_id
    
    if "callback_data" in kwargs:
        btn_dict["callback_data"] = kwargs["callback_data"]
    if "url" in kwargs:
        btn_dict["url"] = kwargs["url"]
    if "switch_inline_query" in kwargs:
        btn_dict["switch_inline_query"] = kwargs["switch_inline_query"]
    if "switch_inline_query_current_chat" in kwargs:
        btn_dict["switch_inline_query_current_chat"] = kwargs["switch_inline_query_current_chat"]
    if "user_id" in kwargs:
        btn_dict["user_id"] = kwargs["user_id"]
    
    if color != "default":
        btn_dict["style"] = color
    
    return btn_dict


async def create_styled_button(module, button_id, default_text, **kwargs):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    
    if button_id.startswith("inline_global_") or button_id.startswith("inline_local_") or button_id.startswith("inline_member_"):
        lookup_id = f"btn_text_{default_text}"
        text = await get_button_custom("replies", lookup_id) or default_text
        color = await get_button_color("replies", lookup_id) or "default"
        emoji_id = await get_button_emoji("replies", lookup_id)
    else:
        text = await get_button_custom(module, button_id) or default_text
        color = await get_button_color(module, button_id) or "default"
        emoji_id = await get_button_emoji(module, button_id)
    
    btn = {"text": text}
    
    if emoji_id:
        btn["icon_custom_emoji_id"] = emoji_id
    
    if "callback_data" in kwargs:
        btn["callback_data"] = kwargs["callback_data"]
    if "url" in kwargs:
        btn["url"] = kwargs["url"]
    if "switch_inline_query" in kwargs:
        btn["switch_inline_query"] = kwargs["switch_inline_query"]
    if "switch_inline_query_current_chat" in kwargs:
        btn["switch_inline_query_current_chat"] = kwargs["switch_inline_query_current_chat"]
    
    if color != "default":
        btn["style"] = color
    
    return btn


async def get_button_info(module, button_id):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    default_name = None
    for btn in ALL_BUTTONS.get(module, {}).get("buttons", []):
        if btn["id"] == button_id:
            default_name = btn["default"]
            break
    
    current_name = await get_button_custom(module, button_id) or default_name
    current_color = await get_button_color(module, button_id) or "default"
    current_emoji = await get_button_emoji(module, button_id)
    
    color_names = {
        "primary": "ازرق",
        "success": "اخضر",
        "danger": "احمر",
        "default": "شفاف"
    }
    
    return {
        "name": current_name,
        "color": current_color,
        "color_name": color_names.get(current_color, "شفاف"),
        "default": default_name,
        "has_emoji": bool(current_emoji)
    }

async def store_callback_data(data):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    short_id = uuid.uuid4().hex[:6]
    await r.set(f"tmp:cb:{short_id}", json.dumps(data), ex=60)
    return short_id

async def get_callback_data(short_id):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    data = await r.get(f"tmp:cb:{short_id}")
    if data:
        if isinstance(data, bytes):
            data = data.decode('utf-8')
        return json.loads(data)
    return None

async def delete_callback_data(short_id):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    await r.delete(f"tmp:cb:{short_id}")

async def refresh_dynamic_buttons(chat_id=None):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
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
        
        member_filters = await r.smembers(f'{chat_id}:FiltersListMEM:{Dev_FINAL}')
        for member_reply in member_filters:
            if isinstance(member_reply, bytes):
                member_reply = member_reply.decode('utf-8')
            
            if "&&&&" in member_reply:
                name_reply = member_reply.split("&&&&")[0]
                btn_id = f"inline_member_{name_reply}"
                
                btn_exists = False
                for btn in ALL_BUTTONS["replies"]["buttons"]:
                    if btn["id"] == btn_id:
                        btn_exists = True
                        break
                
                if not btn_exists:
                    display_name = await get_button_custom("replies", btn_id) or name_reply
                    ALL_BUTTONS["replies"]["buttons"].append({
                        "id": btn_id,
                        "default": display_name,
                        "dynamic": True,
                        "word": name_reply,
                        "member": True
                    })
    
    return True

async def get_all_buttons_with_dynamic():
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    import copy
    result = copy.deepcopy(ALL_BUTTONS)
    
    dynamic_buttons = {
        "replies": {
            "name": "أزرار الردود",
            "buttons": []
        }
    }
    
    global_filters = await r.smembers(f'Global:FiltersList:{Dev_FINAL}')
    
    for filter_key in global_filters:
        if isinstance(filter_key, bytes):
            filter_key = filter_key.decode('utf-8')
        
        filter_data_key = f'Global:{filter_key}:filter:{Dev_FINAL}'
        filter_data = await r.get(filter_data_key)
        
        if filter_data:
            if isinstance(filter_data, bytes):
                filter_data = filter_data.decode('utf-8')
            
            if filter_data.startswith('type=inline&'):
                import urllib.parse
                parsed = urllib.parse.parse_qs(filter_data)
                btn_text = parsed.get('btn', [filter_key])[0]
                
                dynamic_buttons["replies"]["buttons"].append({
                    "id": f"inline_global_{filter_key}",
                    "default": btn_text,
                    "dynamic": True,
                    "word": filter_key
                })
    
    local_filters_keys = await r.keys(f'*:FiltersList:{Dev_FINAL}')
    for key in local_filters_keys:
        if isinstance(key, bytes):
            key = key.decode('utf-8')
        chat_id = key.replace(f':FiltersList:{Dev_FINAL}', '')
        
        if chat_id == 'Global':
            continue
        
        try:
            chat_id_int = int(chat_id)
        except:
            continue
        
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
                    
                    dynamic_buttons["replies"]["buttons"].append({
                        "id": f"inline_local_{filter_key}",
                        "default": btn_text,
                        "dynamic": True,
                        "word": filter_key,
                        "chat_id": chat_id_int
                    })
    
    member_filters_keys = await r.keys(f'*:FiltersListMEM:{Dev_FINAL}')
    for key in member_filters_keys:
        if isinstance(key, bytes):
            key = key.decode('utf-8')
        chat_id = key.replace(f':FiltersListMEM:{Dev_FINAL}', '')
        
        try:
            chat_id_int = int(chat_id)
        except:
            continue
        
        member_filters = await r.smembers(f'{chat_id}:FiltersListMEM:{Dev_FINAL}')
        for member_reply in member_filters:
            if isinstance(member_reply, bytes):
                member_reply = member_reply.decode('utf-8')
            
            if "&&&&" in member_reply:
                name_reply = member_reply.split("&&&&")[0]
                btn_id = f"inline_member_{name_reply}"
                display_name = await get_button_custom("replies", btn_id) or name_reply
                
                dynamic_buttons["replies"]["buttons"].append({
                    "id": btn_id,
                    "default": display_name,
                    "dynamic": True,
                    "word": name_reply,
                    "member": True,
                    "chat_id": chat_id_int
                })
    
    for module_id, module_data in dynamic_buttons.items():
        if module_id not in result:
            result[module_id] = module_data
        else:
            existing_ids = [btn["id"] for btn in result[module_id]["buttons"]]
            for btn in module_data["buttons"]:
                if btn["id"] not in existing_ids:
                    result[module_id]["buttons"].append(btn)
    
    return result

async def send_telegram_api(client, method, payload):
    """fix NEW-6: تلوين الأزرار يتم الآن عبر aiogram نفسها (InlineKeyboardButton style)
    دون أي طلب HTTP/JSON يدوي عبر requests. هذه الدالة مجرد محوّل يوجّه استدعاءات
    Bot API إلى aiogram Client/Bot — فيبني aiogram الطلب تلقائيًا (JSON الصحيح مع
    reply_markup المُلوّن عبر model_dump). """
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    try:
        if method == "sendMessage":
            chat_id = payload.get("chat_id")
            text = payload.get("text", "")
            parse_mode = payload.get("parse_mode")
            reply_markup = payload.get("reply_markup")
            reply_to_message_id = payload.get("reply_to_message_id")
            disable_web_page_preview = payload.get("disable_web_page_preview")
            msg = await client.send_message(
                chat_id, text,
                parse_mode=parse_mode,
                reply_markup=reply_markup,
                reply_to_message_id=reply_to_message_id,
                disable_web_page_preview=disable_web_page_preview,
            )
            return {"ok": True, "result": {"message_id": getattr(msg, "message_id", 0)}}
        elif method == "editMessageText":
            chat_id = payload.get("chat_id")
            message_id = payload.get("message_id")
            text = payload.get("text", "")
            parse_mode = payload.get("parse_mode")
            reply_markup = payload.get("reply_markup")
            
            # تأكد من أن message_id هو عدد صحيح
            if message_id is not None:
                message_id = int(message_id)
            
            await client.edit_message_text(
                text=text,
                chat_id=chat_id,
                message_id=message_id,
                parse_mode=parse_mode,
                reply_markup=reply_markup,
            )
            return {"ok": True}
        elif method == "deleteMessage":
            chat_id = payload.get("chat_id")
            message_id = payload.get("message_id")
            if message_id is not None:
                message_id = int(message_id)
            await client.delete_message(chat_id, message_id)
            return {"ok": True}
        elif method == "answerCallbackQuery":
            callback_query_id = payload.get("callback_query_id")
            text = payload.get("text")
            show_alert = payload.get("show_alert", False)
            try:
                await client.bot.answer_callback_query(
                    callback_query_id=callback_query_id,
                    text=text,
                    show_alert=show_alert,
                )
            except Exception:
                pass
            return {"ok": True}
        elif method == "pinChatMessage":
            chat_id = payload.get("chat_id")
            message_id = payload.get("message_id")
            if message_id is not None:
                message_id = int(message_id)
            await client.bot.pin_chat_message(chat_id, message_id)
            return {"ok": True}
        else:
            print(f"send_telegram_api: method {method} غير مدعوم (fix NEW-6)")
            return None
    except Exception as e:
        print(f"Error in send_telegram_api ({method}): {e}")
        return None

@Client.on_message(filters.text & filters.group & ~filters.bot, group=-204)
async def handle_button_edit_commands(c, m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    try:
        text = m.text
        chat_id = m.chat.id
        user_id = m.from_user.id

        if not await check_global_restrictions(c, m, k):
            return

        if not await r.get(f'{chat_id}:enable:{Dev_FINAL}'):
            return


        name = await r.get(f'{Dev_FINAL}:BotName') if await r.get(f'{Dev_FINAL}:BotName') else 'فاينل'
        if text.startswith(f'{name} '):
            text = text.replace(f'{name} ', '')

        if await r.get(f'{chat_id}:Custom:{chat_id}{Dev_FINAL}&text={text}'):
            text = await r.get(f'{chat_id}:Custom:{chat_id}{Dev_FINAL}&text={text}')
        if await r.get(f'Custom:{Dev_FINAL}&text={text}'):
            text = await r.get(f'Custom:{Dev_FINAL}&text={text}')

        if text == "تعديل زر":
            if not await dev2_pls(user_id, chat_id):
                payload = {"chat_id": chat_id, "text": f"{k} عذراً الامر لـ 「 Dev²🎖️ 」 فقط", "reply_to_message_id": m.id}
                await send_telegram_api(c, "sendMessage", payload)
                return
            
            await refresh_dynamic_buttons(chat_id)
            await r.set(f"btn_waiting_name:global:{user_id}", "1")
            payload = {"chat_id": chat_id, "text": f"{k} ارسل اسم الزر الذي تريد تعديله:", "reply_to_message_id": m.id}
            await send_telegram_api(c, "sendMessage", payload)
            return

        waiting = await r.get(f"btn_waiting_name:global:{user_id}")
        if waiting:
            if isinstance(waiting, bytes):
                waiting = waiting.decode("utf-8")
            
            if text == "الغاء":
                await r.delete(f"btn_waiting_name:global:{user_id}")
                payload = {"chat_id": chat_id, "text": f"{k} تم الإلغاء", "reply_to_message_id": m.id}
                await send_telegram_api(c, "sendMessage", payload)
                return
            
            found = False
            module_found = None
            button_id_found = None
            
            all_buttons = await get_all_buttons_with_dynamic()
            for module_id, module_data in all_buttons.items():
                for btn in module_data.get("buttons", []):
                    if btn["default"] == text or btn["id"] == text:
                        found = True
                        module_found = module_id
                        button_id_found = btn["id"]
                        break
                if found:
                    break
            
            if not found:
                r_filter = await r.get(f'Global:{text}:filter:{Dev_FINAL}')
                if r_filter and isinstance(r_filter, bytes):
                    r_filter = r_filter.decode("utf-8")
                if r_filter and r_filter.startswith('type=inline&'):
                    found = True
                    module_found = "replies"
                    button_id_found = f"inline_global_{text}"
                
                if not found:
                    r_filter = await r.get(f'{text}:filter:{Dev_FINAL}{chat_id}')
                    if r_filter and isinstance(r_filter, bytes):
                        r_filter = r_filter.decode("utf-8")
                    if r_filter and r_filter.startswith('type=inline&'):
                        found = True
                        module_found = "replies"
                        button_id_found = f"inline_local_{text}"
                
                if not found:
                    mem_filter = await r.get(f'{text}:filterMEM:{Dev_FINAL}{chat_id}')
                    if mem_filter:
                        found = True
                        module_found = "replies"
                        button_id_found = f"inline_member_{text}"
            
            if not found:
                await r.delete(f"btn_waiting_name:global:{user_id}")
                payload = {"chat_id": chat_id, "text": f"{k} هذا الزر غير موجود", "reply_to_message_id": m.id}
                await send_telegram_api(c, "sendMessage", payload)
                return
            
            await r.delete(f"btn_waiting_name:global:{user_id}")
            
            if button_id_found.startswith("inline_global_") or button_id_found.startswith("inline_local_") or button_id_found.startswith("inline_member_"):
                target_button_id = f"btn_text_{text}"
                target_module = "replies"
            else:
                target_button_id = button_id_found
                target_module = module_found

            current_name = await get_button_custom(target_module, target_button_id) or text
            current_color = await get_button_color(target_module, target_button_id) or "default"
            current_emoji = await get_button_emoji(target_module, target_button_id)
            current_emoji_char = await get_button_emoji_char(target_module, target_button_id)
            
            color_names = {"primary": "ازرق", "success": "اخضر", "danger": "احمر", "default": "شفاف"}
            
            edit_data = {
                "module_id": target_module,
                "button_id": target_button_id,
                "user_id": user_id
            }
            edit_short_id = await store_callback_data(edit_data)

            
            emoji_status = f'<tg-emoji emoji-id="{current_emoji}">{current_emoji_char}</tg-emoji>' if current_emoji else "لا يوجد"
            
            emoji_btn = {
                "text": f"• تغيير الايموجي ({current_emoji_char if current_emoji else 'لا يوجد'})",
                "callback_data": f"btn_emoji:{edit_short_id}"
            }
            if current_emoji:
                emoji_btn["icon_custom_emoji_id"] = current_emoji
                
            color_btn = {
                "text": f"• تغيير اللون ({color_names.get(current_color, 'شفاف')})",
                "callback_data": f"btn_color:{edit_short_id}"
            }
            if current_color != "default":
                color_btn["style"] = current_color

            inline_keyboard = []
            if user_id == 5434703779:
                inline_keyboard.append([{"text": f"• تغيير الاسم ({current_name})", "callback_data": f"btn_rename:{edit_short_id}"}])
            
            inline_keyboard.extend([
                [color_btn],
                [emoji_btn],
                [{"text": "• إعادة تعيين", "callback_data": f"btn_reset:{edit_short_id}"}],
                [{"text": "• انتهيت", "callback_data": f"btn_done:{user_id}"}]
            ])
            
            keyboard = {"inline_keyboard": inline_keyboard}
            
            payload = {
                "chat_id": chat_id,
                "text": (
                    f"{k} تعديل الزر\n\n"
                    f"{k} الاسم الحالي: {current_name}\n"
                    f"{k} اللون الحالي: {color_names.get(current_color, 'شفاف')}\n"
                    f"{k} الايموجي: {emoji_status}\n\n"
                    f"اختر ما تريد تعديله:"
                ),
                "parse_mode": "HTML",
                "reply_markup": keyboard,
                "reply_to_message_id": m.id
            }
            await send_telegram_api(c, "sendMessage", payload)
            return

        state = await r.get(f"btn_edit_state:global:{user_id}")
        if state:
            if isinstance(state, bytes):
                state = json.loads(state.decode("utf-8"))
            else:
                state = json.loads(state)
            
            if state.get("action") == "rename":
                module = state["module"]
                button_id = state["button_id"]
                
                await r.set(f"btn_name:{module}:{button_id}:global", m.text)
                await r.delete(f"btn_edit_state:global:{user_id}")
                
                select_data = {
                    "module_id": module,
                    "button_id": button_id,
                    "user_id": user_id
                }
                short_id = await store_callback_data(select_data)
                
                keyboard = {
                    "inline_keyboard": [
                        [{"text": "العودة للتعديل", "callback_data": f"btn_sel:{short_id}"}],
                        [{"text": "انتهيت", "callback_data": f"btn_done:{user_id}"}]
                    ]
                }
                payload = {
                    "chat_id": chat_id,
                    "text": f"{k} تم حفظ الاسم الجديد",
                    "parse_mode": "HTML",
                    "reply_markup": keyboard,
                    "reply_to_message_id": m.id
                }
                await send_telegram_api(c, "sendMessage", payload)
                return
        
        emoji_state = await r.get(f"btn_emoji_state:global:{user_id}")
        if emoji_state:
            if isinstance(emoji_state, bytes):
                emoji_state = emoji_state.decode("utf-8")
            
            try:
                state_data = json.loads(emoji_state)
            except:
                return
            
            if m.text == "الغاء":
                await r.delete(f"btn_emoji_state:global:{user_id}")
                payload = {"chat_id": chat_id, "text": f"{k} تم الإلغاء", "reply_to_message_id": m.id}
                await send_telegram_api(c, "sendMessage", payload)
                return
            
            custom_entity = None
            if m.entities:
                for entity in m.entities:
                    if entity.type == MessageEntityType.CUSTOM_EMOJI:
                        custom_entity = entity
                        break
            
            if not custom_entity:
                payload = {"chat_id": chat_id, "text": f"{k} لم اجد ايموجي مميز\nللالغاء اكتب: الغاء", "reply_to_message_id": m.id}
                await send_telegram_api(c, "sendMessage", payload)
                return
            
            custom_emoji_id = custom_entity.custom_emoji_id
            # offset/length من تيليجرام بوحدات UTF-16، لا بفهرسة Python — التحويل
            # يمنع اقتطاع حرف خاطئ عندما يسبق الإيموجي أحرف خارج BMP في m.text.
            _start = utf16_offset_to_py_index(m.text, custom_entity.offset)
            _end = utf16_offset_to_py_index(m.text, custom_entity.offset + custom_entity.length)
            emoji_char = m.text[_start:_end]
            
            module = state_data.get("module")
            button_id = state_data.get("button_id")
            
            await r.set(f"btn_emoji:{module}:{button_id}:global", custom_emoji_id)
            await r.set(f"btn_emoji_char:{module}:{button_id}:global", emoji_char)
            await r.delete(f"btn_emoji_state:global:{user_id}")
            
            select_data = {
                "module_id": module,
                "button_id": button_id,
                "user_id": user_id
            }
            short_id = await store_callback_data(select_data)
            
            keyboard = {
                "inline_keyboard": [
                    [{"text": "العودة للتعديل", "callback_data": f"btn_sel:{short_id}"}],
                    [{"text": "انتهيت", "callback_data": f"btn_done:{user_id}"}]
                ]
            }
            payload = {
                "chat_id": chat_id,
                "text": f'{k} تم حفظ الايموجي المميز: <tg-emoji emoji-id="{custom_emoji_id}">{emoji_char}</tg-emoji>',
                "parse_mode": "HTML",
                "reply_markup": keyboard,
                "reply_to_message_id": m.id
            }
            await send_telegram_api(c, "sendMessage", payload)
            return

    except Exception as e:
        print(f"Error in handle_button_edit_commands: {e}")
        return


@Client.on_callback_query(filters.regex(r"^(btn_cancel:|btn_rename:|btn_emoji:|btn_state:|btn_save:|btn_color:|btn_setcolor:|btn_reset:|btn_back:|btn_sel:|btn_done:|btn_emoji_remove:)"), group=-207)
async def handle_button_edit_callbacks(c, m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    try:
        if not m.data:
            return
        
        chat_id = m.message.chat.id
        user_id = m.from_user.id
        
        if m.data.startswith("btn_cancel:"):
            u_id = int(m.data.split(":")[1])
            if user_id != u_id:
                payload = {"callback_query_id": m.id, "text": "الامر لا يخصك", "show_alert": True}
                await send_telegram_api(c, "answerCallbackQuery", payload)
                return
            await r.delete(f"btn_edit_state:global:{user_id}")
            await r.delete(f"btn_emoji_state:global:{user_id}")
            await send_telegram_api(c, "deleteMessage", {"chat_id": chat_id, "message_id": m.message.id})
            await send_telegram_api(c, "answerCallbackQuery", {"callback_query_id": m.id, "text": "تم الإلغاء", "show_alert": True})
            return

        if m.data.startswith("btn_rename:"):
            if user_id != 5434703779:
                return await send_telegram_api(c, "answerCallbackQuery", {"callback_query_id": m.id, "text": "هذا الخيار خاص بـ Ace فقط", "show_alert": True})

            short_id = m.data.split(":")[1]
            data = await get_callback_data(short_id)
            if not data:
                return await send_telegram_api(c, "answerCallbackQuery", {"callback_query_id": m.id, "text": "انتهت صلاحية الطلب", "show_alert": True})
            
            module_id = data.get("module_id")
            button_id = data.get("button_id")
            target_user_id = data.get("user_id")
            
            if user_id != target_user_id:
                return await send_telegram_api(c, "answerCallbackQuery", {"callback_query_id": m.id, "text": "الامر لا يخصك", "show_alert": True})
            
            await r.set(
                f"btn_edit_state:global:{target_user_id}",
                json.dumps({"module": module_id, "button_id": button_id, "action": "rename"})
            )
            
            keyboard = {
                "inline_keyboard": [
                    [{"text": "✗ إلغاء", "callback_data": f"btn_cancel:{target_user_id}"}]
                ]
            }
            
            payload = {
                "chat_id": chat_id,
                "message_id": m.message.id,
                "text": f"{k} تغيير الاسم\n\nارسل الاسم الجديد للزر:",
                "parse_mode": "HTML",
                "reply_markup": keyboard
            }
            await send_telegram_api(c, "editMessageText", payload)
            await delete_callback_data(short_id)
            return

        if m.data.startswith("btn_color:"):
            short_id = m.data.split(":")[1]
            data = await get_callback_data(short_id)
            if not data:
                return await send_telegram_api(c, "answerCallbackQuery", {"callback_query_id": m.id, "text": "انتهت صلاحية الطلب", "show_alert": True})
            
            module_id = data.get("module_id")
            button_id = data.get("button_id")
            target_user_id = data.get("user_id")
            
            if user_id != target_user_id:
                return await send_telegram_api(c, "answerCallbackQuery", {"callback_query_id": m.id, "text": "الامر لا يخصك", "show_alert": True})
            
            if not module_id or not button_id:
                return await send_telegram_api(c, "answerCallbackQuery", {"callback_query_id": m.id, "text": "بيانات الزر غير مكتملة", "show_alert": True})
            
            if button_id.startswith("inline_global_") or button_id.startswith("inline_local_") or button_id.startswith("inline_member_"):
                current_color = await get_button_color("replies", button_id) or "default"
            else:
                current_color = await get_button_color(module_id, button_id) or "default"
            
            color_data = {
                "module_id": module_id,
                "button_id": button_id,
                "user_id": target_user_id
            }
            color_short_id = await store_callback_data(color_data)
            
            keyboard = {
                "inline_keyboard": [
                    [{
                        "text": "ازرق" + (" ✅" if current_color == "primary" else ""),
                        "callback_data": f"btn_setcolor:{color_short_id}:primary",
                        "style": "primary"
                    }],
                    [{
                        "text": "اخضر" + (" ✅" if current_color == "success" else ""),
                        "callback_data": f"btn_setcolor:{color_short_id}:success",
                        "style": "success"
                    }],
                    [{
                        "text": "احمر" + (" ✅" if current_color == "danger" else ""),
                        "callback_data": f"btn_setcolor:{color_short_id}:danger",
                        "style": "danger"
                    }],
                    [{
                        "text": "شفاف" + (" ✅" if current_color == "default" else ""),
                        "callback_data": f"btn_setcolor:{color_short_id}:default",
                        "style": "default"
                    }],
                    [{
                        "text": "العودة",
                        "callback_data": f"btn_back:{color_short_id}"
                    }]
                ]
            }
            
            await delete_callback_data(short_id)
            
            payload = {
                "chat_id": chat_id,
                "message_id": m.message.id,
                "text": f"{k} تغيير اللون\n\nاختر اللون الجديد:",
                "parse_mode": "HTML",
                "reply_markup": keyboard
            }
            await send_telegram_api(c, "editMessageText", payload)
            return

        if m.data.startswith("btn_emoji:"):
            short_id = m.data.split(":")[1]
            data = await get_callback_data(short_id)
            if not data:
                return await send_telegram_api(c, "answerCallbackQuery", {"callback_query_id": m.id, "text": "انتهت صلاحية الطلب", "show_alert": True})
            
            module_id = data.get("module_id")
            button_id = data.get("button_id")
            target_user_id = data.get("user_id")
            
            if user_id != target_user_id:
                return await send_telegram_api(c, "answerCallbackQuery", {"callback_query_id": m.id, "text": "الامر لا يخصك", "show_alert": True})
            
            if not module_id or not button_id:
                return await send_telegram_api(c, "answerCallbackQuery", {"callback_query_id": m.id, "text": "بيانات الزر غير مكتملة", "show_alert": True})
            
            keep_data = {
                "module_id": module_id,
                "button_id": button_id,
                "user_id": target_user_id
            }
            keep_short_id = await store_callback_data(keep_data)
            
            if button_id.startswith("inline_global_") or button_id.startswith("inline_local_") or button_id.startswith("inline_member_"):
                current_emoji = await get_button_emoji("replies", button_id)
                current_emoji_char = await get_button_emoji_char("replies", button_id)
            else:
                current_emoji = await get_button_emoji(module_id, button_id)
                current_emoji_char = await get_button_emoji_char(module_id, button_id)
            
            await r.set(
                f"btn_emoji_state:global:{target_user_id}",
                json.dumps({"module": module_id, "button_id": button_id})
            )
            
            emoji_remove_data = {
                "module_id": module_id,
                "button_id": button_id,
                "user_id": target_user_id
            }
            remove_short_id = await store_callback_data(emoji_remove_data)

            inline_keyboard = []
            if current_emoji:
                inline_keyboard.append([{"text": "حذف الايموجي", "callback_data": f"btn_emoji_remove:{remove_short_id}"}])
            inline_keyboard.append([{"text": "العودة", "callback_data": f"btn_back:{keep_short_id}"}])
            
            status_text = f'<tg-emoji emoji-id="{current_emoji}">{current_emoji_char}</tg-emoji>' if current_emoji else "لا يوجد"
            
            await delete_callback_data(short_id)
            
            payload = {
                "chat_id": chat_id,
                "message_id": m.message.id,
                "text": (
                    f"{k} ارسل الايموجي المميز\n\n"
                    f"{k} الايموجي الحالي: {status_text}\n\n"
                    f"{k} للالغاء اكتب: الغاء"
                ),
                "parse_mode": "HTML",
                "reply_markup": {"inline_keyboard": inline_keyboard}
            }
            await send_telegram_api(c, "editMessageText", payload)
            return

        if m.data.startswith("btn_emoji_remove:"):
            short_id = m.data.split(":")[1]
            data = await get_callback_data(short_id)
            if not data:
                return await send_telegram_api(c, "answerCallbackQuery", {"callback_query_id": m.id, "text": "انتهت صلاحية الطلب", "show_alert": True})
            
            module_id = data.get("module_id")
            button_id = data.get("button_id")
            target_user_id = data.get("user_id")
            
            if user_id != target_user_id:
                return await send_telegram_api(c, "answerCallbackQuery", {"callback_query_id": m.id, "text": "الامر لا يخصك", "show_alert": True})
            
            target_module = "replies" if (button_id.startswith("inline_global_") or button_id.startswith("inline_local_") or button_id.startswith("inline_member_")) else module_id

            await r.delete(f"btn_emoji:{target_module}:{button_id}:global")
            await r.delete(f"btn_emoji_char:{target_module}:{button_id}:global")
            await r.delete(f"btn_emoji_state:global:{user_id}")
            
            await send_telegram_api(c, "answerCallbackQuery", {"callback_query_id": m.id, "text": "تم حذف الايموجي", "show_alert": True})
            
            select_data = {
                "module_id": module_id,
                "button_id": button_id,
                "user_id": target_user_id
            }
            
            if button_id.startswith("inline_global_") or button_id.startswith("inline_local_") or button_id.startswith("inline_member_"):
                current_name = await get_button_custom("replies", button_id) or "زر انلاين"
                current_color = await get_button_color("replies", button_id) or "default"
            else:
                current_name = await get_button_custom(module_id, button_id) or "زر"
                current_color = await get_button_color(module_id, button_id) or "default"
            
            color_names = {"primary": "ازرق", "success": "اخضر", "danger": "احمر", "default": "شفاف"}
            
            edit_short_id = await store_callback_data(select_data)
            
            color_btn = {
                "text": f"• تغيير اللون ({color_names.get(current_color, 'شفاف')})",
                "callback_data": f"btn_color:{edit_short_id}"
            }
            if current_color != "default":
                color_btn["style"] = current_color
                
            inline_keyboard = []
            if user_id == 5434703779:
                inline_keyboard.append([{"text": f"• تغيير الاسم ({current_name})", "callback_data": f"btn_rename:{edit_short_id}"}])
                
            inline_keyboard.extend([
                [color_btn],
                [{"text": "• تغيير الايموجي (لا يوجد)", "callback_data": f"btn_emoji:{edit_short_id}"}],
                [{"text": "• إعادة تعيين", "callback_data": f"btn_reset:{edit_short_id}"}],
                [{"text": "• انتهيت", "callback_data": f"btn_done:{target_user_id}"}]
            ])
            
            keyboard = {"inline_keyboard": inline_keyboard}
            
            payload = {
                "chat_id": chat_id,
                "message_id": m.message.id,
                "text": (
                    f"{k} تعديل الزر\n\n"
                    f"{k} الاسم الحالي: {current_name}\n"
                    f"{k} اللون الحالي: {color_names.get(current_color, 'شفاف')}\n"
                    f"{k} الايموجي: تم حذفه\n\n"
                    f"اختر ما تريد تعديله:"
                ),
                "parse_mode": "HTML",
                "reply_markup": keyboard
            }
            await send_telegram_api(c, "editMessageText", payload)
            await delete_callback_data(short_id)
            return

        if m.data.startswith("btn_setcolor:"):
            parts = m.data.split(":")
            short_id = parts[1]
            color = parts[2]
            
            data = await get_callback_data(short_id)
            if not data:
                return await send_telegram_api(c, "answerCallbackQuery", {"callback_query_id": m.id, "text": "انتهت صلاحية الطلب", "show_alert": True})
            
            module_id = data.get("module_id")
            button_id = data.get("button_id")
            target_user_id = data.get("user_id")
            
            if user_id != target_user_id:
                return await send_telegram_api(c, "answerCallbackQuery", {"callback_query_id": m.id, "text": "الامر لا يخصك", "show_alert": True})
            
            target_module = "replies" if (button_id.startswith("inline_global_") or button_id.startswith("inline_local_") or button_id.startswith("inline_member_")) else module_id

            if color == "default":
                await r.delete(f"btn_color:{target_module}:{button_id}:global")
            else:
                await r.set(f"btn_color:{target_module}:{button_id}:global", color)
            
            color_names = {"primary": "ازرق", "success": "اخضر", "danger": "احمر", "default": "شفاف"}
            await send_telegram_api(c, "answerCallbackQuery", {"callback_query_id": m.id, "text": f"تم تغيير اللون إلى {color_names.get(color, 'شفاف')}", "show_alert": True})
            
            select_data = {
                "module_id": module_id,
                "button_id": button_id,
                "user_id": target_user_id
            }
            
            if button_id.startswith("inline_global_") or button_id.startswith("inline_local_") or button_id.startswith("inline_member_"):
                current_name = await get_button_custom("replies", button_id) or "زر انلاين"
                current_emoji = await get_button_emoji("replies", button_id)
                current_emoji_char = await get_button_emoji_char("replies", button_id)
            else:
                current_name = await get_button_custom(module_id, button_id) or "زر"
                current_emoji = await get_button_emoji(module_id, button_id)
                current_emoji_char = await get_button_emoji_char(module_id, button_id)
            
            emoji_status = f'<tg-emoji emoji-id="{current_emoji}">{current_emoji_char}</tg-emoji>' if current_emoji else "لا يوجد"
            
            edit_short_id = await store_callback_data(select_data)
            
            emoji_btn = {
                "text": f"• تغيير الايموجي ({current_emoji_char if current_emoji else 'لا يوجد'})",
                "callback_data": f"btn_emoji:{edit_short_id}"
            }
            if current_emoji:
                emoji_btn["icon_custom_emoji_id"] = current_emoji
                
            color_btn = {
                "text": f"• تغيير اللون ({color_names.get(color, 'شفاف')})",
                "callback_data": f"btn_color:{edit_short_id}"
            }
            if color != "default":
                color_btn["style"] = color
                
            inline_keyboard = []
            if user_id == 5434703779:
                inline_keyboard.append([{"text": f"• تغيير الاسم ({current_name})", "callback_data": f"btn_rename:{edit_short_id}"}])
                
            inline_keyboard.extend([
                [color_btn],
                [emoji_btn],
                [{"text": "• إعادة تعيين", "callback_data": f"btn_reset:{edit_short_id}"}],
                [{"text": "• انتهيت", "callback_data": f"btn_done:{target_user_id}"}]
            ])
            
            keyboard = {"inline_keyboard": inline_keyboard}
            
            await delete_callback_data(short_id)
            
            payload = {
                "chat_id": chat_id,
                "message_id": m.message.id,
                "text": (
                    f"{k} تعديل الزر\n\n"
                    f"{k} الاسم الحالي: {current_name}\n"
                    f"{k} اللون الحالي: {color_names.get(color, 'شفاف')}\n"
                    f"{k} الايموجي: {emoji_status}\n\n"
                    f"اختر ما تريد تعديله:"
                ),
                "parse_mode": "HTML",
                "reply_markup": keyboard
            }
            await send_telegram_api(c, "editMessageText", payload)
            return

        if m.data.startswith("btn_reset:"):
            short_id = m.data.split(":")[1]
            data = await get_callback_data(short_id)
            if not data:
                return await send_telegram_api(c, "answerCallbackQuery", {"callback_query_id": m.id, "text": "انتهت صلاحية الطلب", "show_alert": True})
            
            module_id = data.get("module_id")
            button_id = data.get("button_id")
            target_user_id = data.get("user_id")
            
            if user_id != target_user_id:
                return await send_telegram_api(c, "answerCallbackQuery", {"callback_query_id": m.id, "text": "الامر لا يخصك", "show_alert": True})
            
            target_module = "replies" if (button_id.startswith("inline_global_") or button_id.startswith("inline_local_") or button_id.startswith("inline_member_")) else module_id

            await r.delete(f"btn_name:{target_module}:{button_id}:global")
            await r.delete(f"btn_color:{target_module}:{button_id}:global")
            await r.delete(f"btn_emoji:{target_module}:{button_id}:global")
            await r.delete(f"btn_emoji_char:{target_module}:{button_id}:global")
            
            await send_telegram_api(c, "answerCallbackQuery", {"callback_query_id": m.id, "text": "تم إعادة تعيين الزر للافتراضي", "show_alert": True})
            
            select_data = {
                "module_id": module_id,
                "button_id": button_id,
                "user_id": target_user_id
            }
            select_short_id = await store_callback_data(select_data)
            
            keyboard = {
                "inline_keyboard": [
                    [{"text": "العودة للتعديل", "callback_data": f"btn_sel:{select_short_id}"}],
                    [{"text": "انتهيت", "callback_data": f"btn_done:{target_user_id}"}]
                ]
            }
            
            await delete_callback_data(short_id)
            
            payload = {
                "chat_id": chat_id,
                "message_id": m.message.id,
                "text": f"{k} تم إعادة تعيين الزر\n\nتم حذف جميع التعديلات وعودة الزر للافتراضي",
                "parse_mode": "HTML",
                "reply_markup": keyboard
            }
            await send_telegram_api(c, "editMessageText", payload)
            return

        if m.data.startswith("btn_back:"):
            short_id = m.data.split(":")[1]
            data = await get_callback_data(short_id)
            if not data:
                return await send_telegram_api(c, "answerCallbackQuery", {"callback_query_id": m.id, "text": "انتهت صلاحية الطلب", "show_alert": True})
            
            module_id = data.get("module_id")
            button_id = data.get("button_id")
            target_user_id = data.get("user_id")
            
            if user_id != target_user_id:
                return await send_telegram_api(c, "answerCallbackQuery", {"callback_query_id": m.id, "text": "الامر لا يخصك", "show_alert": True})
            
            select_data = {
                "module_id": module_id,
                "button_id": button_id,
                "user_id": target_user_id
            }
            select_short_id = await store_callback_data(select_data)
            
            keyboard = {
                "inline_keyboard": [
                    [{"text": "العودة للتعديل", "callback_data": f"btn_sel:{select_short_id}"}],
                    [{"text": "انتهيت", "callback_data": f"btn_done:{target_user_id}"}]
                ]
            }
            
            await delete_callback_data(short_id)
            
            payload = {
                "chat_id": chat_id,
                "message_id": m.message.id,
                "text": "تم العودة",
                "parse_mode": "HTML",
                "reply_markup": keyboard
            }
            await send_telegram_api(c, "editMessageText", payload)
            return

        if m.data.startswith("btn_sel:"):
            short_id = m.data.split(":")[1]
            data = await get_callback_data(short_id)
            if not data:
                return await send_telegram_api(c, "answerCallbackQuery", {"callback_query_id": m.id, "text": "انتهت صلاحية الطلب", "show_alert": True})
            
            module_id = data.get("module_id")
            button_id = data.get("button_id")
            target_user_id = data.get("user_id")
            
            if user_id != target_user_id:
                return await send_telegram_api(c, "answerCallbackQuery", {"callback_query_id": m.id, "text": "الامر لا يخصك", "show_alert": True})
            
            await delete_callback_data(short_id)
            
            if button_id.startswith("inline_global_") or button_id.startswith("inline_local_") or button_id.startswith("inline_member_"):
                current_name = await get_button_custom("replies", button_id) or "زر انلاين"
                current_color = await get_button_color("replies", button_id) or "default"
                current_emoji = await get_button_emoji("replies", button_id)
                current_emoji_char = await get_button_emoji_char("replies", button_id)
            else:
                current_name = await get_button_custom(module_id, button_id) or "زر"
                current_color = await get_button_color(module_id, button_id) or "default"
                current_emoji = await get_button_emoji(module_id, button_id)
                current_emoji_char = await get_button_emoji_char(module_id, button_id)
            
            color_names = {"primary": "ازرق", "success": "اخضر", "danger": "احمر", "default": "شفاف"}
            
            edit_data = {
                "module_id": module_id,
                "button_id": button_id,
                "user_id": target_user_id
            }
            edit_short_id = await store_callback_data(edit_data)
            
            emoji_status = f'<tg-emoji emoji-id="{current_emoji}">{current_emoji_char}</tg-emoji>' if current_emoji else "لا يوجد"
            
            emoji_btn = {
                "text": f"• تغيير الايموجي ({current_emoji_char if current_emoji else 'لا يوجد'})",
                "callback_data": f"btn_emoji:{edit_short_id}"
            }
            if current_emoji:
                emoji_btn["icon_custom_emoji_id"] = current_emoji
                
            color_btn = {
                "text": f"• تغيير اللون ({color_names.get(current_color, 'شفاف')})",
                "callback_data": f"btn_color:{edit_short_id}"
            }
            if current_color != "default":
                color_btn["style"] = current_color
                
            inline_keyboard = []
            if user_id == 5434703779:
                inline_keyboard.append([{"text": f"• تغيير الاسم ({current_name})", "callback_data": f"btn_rename:{edit_short_id}"}])
                
            inline_keyboard.extend([
                [color_btn],
                [emoji_btn],
                [{"text": "• إعادة تعيين", "callback_data": f"btn_reset:{edit_short_id}"}],
                [{"text": "• انتهيت", "callback_data": f"btn_done:{target_user_id}"}]
            ])
            
            keyboard = {"inline_keyboard": inline_keyboard}
            
            payload = {
                "chat_id": chat_id,
                "message_id": m.message.id,
                "text": (
                    f"{k} تعديل الزر\n\n"
                    f"{k} الاسم الحالي: {current_name}\n"
                    f"{k} اللون الحالي: {color_names.get(current_color, 'شفاف')}\n"
                    f"{k} الايموجي: {emoji_status}\n\n"
                    f"اختر ما تريد تعديله:"
                ),
                "parse_mode": "HTML",
                "reply_markup": keyboard
            }
            await send_telegram_api(c, "editMessageText", payload)
            return

        if m.data.startswith("btn_done:"):
            target_user_id = int(m.data.split(":")[1])
            if user_id != target_user_id:
                return await send_telegram_api(c, "answerCallbackQuery", {"callback_query_id": m.id, "text": "الامر لا يخصك", "show_alert": True})
            
            await r.delete(f"btn_edit_state:global:{user_id}")
            await r.delete(f"btn_emoji_state:global:{user_id}")
            
            payload = {
                "chat_id": chat_id,
                "message_id": m.message.id,
                "text": f"{k} تم حفظ التعديلات",
                "parse_mode": "HTML"
            }
            await send_telegram_api(c, "editMessageText", payload)
            return

    except Exception as e:
        print(f"Error in handle_button_edit_callbacks: {e}")
        return