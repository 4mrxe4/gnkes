from helpers.context import get_redis, get_dev_final
import time
import random
import asyncio
import aiohttp
from compat import Client, filters
from compat import InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions
from compat import MessageEntityType, ParseMode
from compat import MessageNotModified, MessageIdInvalid, MessageDeleteForbidden
from helpers.ranks import *
from helpers.emoji import render_custom_emoji_entities, utf16_offset_to_py_index
from .protect import _decode_if_bytes, get_top, get_emoji_bank, get_chat_score, get_chat_name_from_api
import settings
from helpers.replies_store import (
    REPLIES,
    plugins_interact_1137,
    plugins_interact_1146,
    plugins_interact_1169,
    plugins_interact_1171,
    plugins_interact_1194,
    plugins_interact_1196,
    plugins_interact_1255,
    plugins_interact_1269,
    plugins_interact_1283,
    plugins_interact_1307,
    plugins_interact_1321,
    plugins_interact_1335,
    plugins_interact_1359,
    plugins_interact_1373,
    plugins_interact_1387,
    plugins_interact_1406,
    plugins_interact_1418,
    plugins_interact_1430,
    plugins_interact_1442,
    plugins_interact_1454,
    plugins_interact_328,
    plugins_interact_332,
    plugins_interact_405,
    plugins_interact_676,
    plugins_interact_688,
)

_aiohttp_session = None

async def get_http_session():
    global _aiohttp_session
    if _aiohttp_session is None or _aiohttp_session.closed:
        _aiohttp_session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=15)
        )
    return _aiohttp_session

async def telegram_api_post(url, payload):
    session = await get_http_session()
    try:
        async with session.post(url, json=payload) as resp:
            data = await resp.json()
            return data
    except asyncio.TimeoutError:
        return {"ok": False, "description": "timeout"}
    except aiohttp.ClientError as e:
        return {"ok": False, "description": str(e)}

async def build_navigation_keyboard(current_page, user_id, chat_id, r_v2):
    buttons_map = {
        1: "①", 2: "②", 3: "③", 4: "④", 5: "⑤",
        6: "⑥", 7: "⑦"
    }
    
    layout = [
        [1, 2, 3],
        [4],
        [5, 6, 7],
    ]
    
    hidden_buttons = await r_v2.get(f"cmd_hidden:global") or ""
    if isinstance(hidden_buttons, bytes):
        hidden_buttons = hidden_buttons.decode("utf-8")
    hidden_list = [int(x) for x in hidden_buttons.split(",") if x.isdigit()]
    
    keyboard = []
    for row in layout:
        row_buttons = []
        for btn in row:
            if btn in hidden_list:
                continue
            
            if btn == current_page:
                btn_text = f"• {buttons_map[btn]} •"
                cb_data = "None"
            else:
                btn_text = buttons_map[btn]
                cb_data = f"commands{btn}:{user_id}"
            
            emoji_id = await r_v2.get(f"cmd_emoji:{btn}:global")
            if isinstance(emoji_id, bytes):
                emoji_id = emoji_id.decode("utf-8")
            
            button = InlineKeyboardButton(
                text=btn_text,
                callback_data=cb_data,
                icon_custom_emoji_id=emoji_id if emoji_id else None
            )
            
            style_config = await r_v2.get(f"cmd_style:global") or "default"
            if isinstance(style_config, bytes):
                style_config = style_config.decode("utf-8")
                
            if style_config == "style1":
                button.style = "danger" if btn == current_page else "default"
            elif style_config == "style2":
                button.style = "primary" if btn == current_page else "default"
            elif style_config == "style3":
                button.style = "primary" if btn == current_page else "danger"
            elif style_config == "style4":
                button.style = "danger" if btn == current_page else "success"
            elif style_config == "style5":
                button.style = "success" if btn == current_page else "primary"
            else:
                button.style = "default"
                
            row_buttons.append(button)
        if row_buttons:
            keyboard.append(row_buttons)
            
    keyboard.append([InlineKeyboardButton("اخفاء", callback_data=f"close_cmds:{user_id}")])
    return InlineKeyboardMarkup(keyboard)


async def edit_with_style(c, m, text, current_page):
    r = get_redis(c)
    Dev_FINAL = get_dev_final(c)
    bot_token = c.bot_token if hasattr(c, "bot_token") else settings.TOKEN 
    chat_id = m.message.chat.id
    
    try:
        user_id = int(m.data.split(":")[1])
    except Exception:
        user_id = m.from_user.id
    
    img_key = f"cmd_img:global"
    has_img = await r.get(img_key)
    if isinstance(has_img, bytes):
        has_img = has_img.decode("utf-8")
        
    nav_markup_obj = await build_navigation_keyboard(current_page, user_id, chat_id, r)
    
    raw_inline_keyboard = []
    for row in nav_markup_obj.inline_keyboard[:-1]:
        row_buttons = []
        for btn in row:
            btn_dict = {
                "text": btn.text,
                "callback_data": btn.callback_data
            }
            if hasattr(btn, "icon_custom_emoji_id") and btn.icon_custom_emoji_id:
                btn_dict["icon_custom_emoji_id"] = btn.icon_custom_emoji_id
            if hasattr(btn, "style") and btn.style is not None:
                if hasattr(btn.style, "value"):
                    btn_dict["style"] = str(btn.style.value)
                elif hasattr(btn.style, "name"):
                    btn_dict["style"] = str(btn.style.name).lower()
                else:
                    btn_dict["style"] = str(btn.style)
            row_buttons.append(btn_dict)
        raw_inline_keyboard.append(row_buttons)
        
    if current_page != 0:
        raw_inline_keyboard.append([{
            "text": "للقائمة الرئيسية",
            "callback_data": f"main_cmds:{user_id}"
        }])
        
    raw_inline_keyboard.append([{
        "text": "اخفاء",
        "callback_data": f"close_cmds:{user_id}"
    }])
    
    nav_markup = {"inline_keyboard": raw_inline_keyboard}
    
    
    if has_img:
        result = await telegram_api_post(
            f"https://api.telegram.org/bot{bot_token}/editMessageMedia",
            {
                "chat_id": chat_id,
                "message_id": m.message.id,
                "media": {
                    "type": "photo",
                    "media": has_img,
                    "caption": text,
                    "parse_mode": "HTML"
                },
                "reply_markup": nav_markup
            }
        )
    else:
        result = await telegram_api_post(
            f"https://api.telegram.org/bot{bot_token}/editMessageText",
            {
                "chat_id": chat_id,
                "message_id": m.message.id,
                "text": text,
                "parse_mode": "HTML",
                "reply_markup": nav_markup
            }
        )
    
    if result and not result.get("ok"):
        description = str(result.get("description", ""))
        if "not modified" not in description.lower():
            try:
                await c.delete_messages(chat_id, m.message.id)
            except (MessageDeleteForbidden, MessageIdInvalid):
                pass
            except Exception:
                pass
            
            if has_img:
                await telegram_api_post(
                    f"https://api.telegram.org/bot{bot_token}/sendPhoto",
                    {
                        "chat_id": chat_id,
                        "photo": has_img,
                        "caption": text,
                        "parse_mode": "HTML",
                        "reply_markup": nav_markup
                    }
                )
            else:
                await telegram_api_post(
                    f"https://api.telegram.org/bot{bot_token}/sendMessage",
                    {
                        "chat_id": chat_id,
                        "text": text,
                        "parse_mode": "HTML",
                        "reply_markup": nav_markup
                    }
                )


@Client.on_message(filters.text & filters.group, group=-1475)
async def xxxx(c, m):
    r = get_redis(c)
    Dev_FINAL = get_dev_final(c)
    k = '⇜'
    k = await r.get(f"{Dev_FINAL}:botkey")
    if isinstance(k, bytes):
        k = k.decode("utf-8")
    await del_ran88ks_func(c, m, k)

async def del_ran88ks_func(c, m, k):
    r = get_redis(c)
    Dev_FINAL = get_dev_final(c)
    k = '⇜'
    
    if not await check_global_restrictions(c, m, k):
        return

    text = m.text
    
    name = await r.get(f'{Dev_FINAL}:BotName')
    if isinstance(name, bytes):
        name = name.decode("utf-8")
    if not name:
        name = 'فاينل'
    if text.startswith(f'{name} '):
        text = text.replace(f'{name} ', '')
    
    if await r.get(f'{m.chat.id}:Custom:{m.chat.id}{Dev_FINAL}&text={text}'):
        val = await r.get(f'{m.chat.id}:Custom:{m.chat.id}{Dev_FINAL}&text={text}')
        if isinstance(val, bytes):
            val = val.decode("utf-8")
        text = val
    if await r.get(f'Custom:{Dev_FINAL}&text={text}'):
        val = await r.get(f'Custom:{Dev_FINAL}&text={text}')
        if isinstance(val, bytes):
            val = val.decode("utf-8")
        text = val

    if text == "الاوامر" or (text and text.lower() == "/commands"):
        if await admin_pls(m.from_user.id, m.chat.id):
            channel = await r.get(f"{Dev_FINAL}:BotChannel")
            if channel and isinstance(channel, bytes):
                channel = channel.decode("utf-8")
            if not channel:
                channel = " "
                
            bot_token = c.bot_token if hasattr(c, "bot_token") else settings.TOKEN
            
            hidden_buttons = await r.get(f"cmd_hidden:global") or ""
            if isinstance(hidden_buttons, bytes):
                hidden_buttons = hidden_buttons.decode("utf-8")
            hidden_list = [int(x) for x in hidden_buttons.split(",") if x.isdigit()]
            
            commands_texts = {
                1: "¹ اوامر الادمنيه",
                2: "² اوامر الاعدادات",
                3: "³ اوامر القفل - الفتح",
                4: "⁴ اوامر التسلية",
                5: "⁵ اوامر الخدمية",
                6: "⁶ اوامر المطور",
                7: "⁷ اوامر الميوزك"
            }
            
            welcome_lines = ["اهليين فيك باوامر البوت\n"]
            for i in range(1, 8):
                if i not in hidden_list:
                    welcome_lines.append(commands_texts[i])
            
            welcome_text = "\n".join(welcome_lines)
            
            nav_markup_obj = await build_navigation_keyboard(0, m.from_user.id, m.chat.id, r)
            
            raw_inline_keyboard = []
            for row in nav_markup_obj.inline_keyboard:
                row_buttons = []
                for btn in row:
                    btn_dict = {"text": btn.text, "callback_data": btn.callback_data}
                    if hasattr(btn, "icon_custom_emoji_id") and btn.icon_custom_emoji_id:
                        btn_dict["icon_custom_emoji_id"] = btn.icon_custom_emoji_id
                    if hasattr(btn, "style") and btn.style is not None:
                        if hasattr(btn.style, "value"):
                            btn_dict["style"] = str(btn.style.value)
                        elif hasattr(btn.style, "name"):
                            btn_dict["style"] = str(btn.style.name).lower()
                        else:
                            btn_dict["style"] = str(btn.style)
                    row_buttons.append(btn_dict)
                raw_inline_keyboard.append(row_buttons)
            
            nav_markup = {"inline_keyboard": raw_inline_keyboard}
            
            has_img = await r.get(f"cmd_img:global")
            if isinstance(has_img, bytes):
                has_img = has_img.decode("utf-8")

            if has_img:
                await c.send_photo(
                    chat_id=m.chat.id,
                    photo=has_img,
                    caption=welcome_text,
                    parse_mode=ParseMode.HTML,
                    reply_markup=nav_markup_obj,
                    reply_to_message_id=m.id 
                )
            else:
                await c.send_message(
                    chat_id=m.chat.id,
                    text=welcome_text,
                    parse_mode=ParseMode.HTML,
                    reply_markup=nav_markup_obj,
                    reply_to_message_id=m.id 
                )
            return
        else:
            return await m.reply(plugins_interact_328(k))

    if text == "تعديل الاوامر":
        if not await dev2_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_interact_332(k))
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("اخفاء الازرار", callback_data=f"edit_panel:hide:{m.from_user.id}"),
             InlineKeyboardButton("لون الازرار", callback_data=f"edit_panel:color:{m.from_user.id}")],
            [InlineKeyboardButton("الكلايش", callback_data=f"edit_panel:texts_submenu:{m.from_user.id}")],
            [InlineKeyboardButton("صورة الاوامر", callback_data=f"edit_panel:photo_submenu:{m.from_user.id}"),
             InlineKeyboardButton("ايموجي الازرار", callback_data=f"edit_panel:emoji_submenu:{m.from_user.id}")],
            [InlineKeyboardButton("حفظ", callback_data=f"edit_panel:done:{m.from_user.id}")]
        ])
        await m.reply(REPLIES['plugins_interact_342'], reply_markup=keyboard)
        return

    state = await r.get(f"cmd_state:global:{m.from_user.id}")
    if isinstance(state, bytes):
        state = state.decode("utf-8")
        
    if state and state.startswith("waiting_text_"):
        if not await dev2_pls(m.from_user.id, m.chat.id):
            return
        
        page_target = state.replace("waiting_text_", "")
        
        final_text = m.text
        if m.entities:
            final_text = render_custom_emoji_entities(final_text, m.entities)
        
        await r.set(f"cmd_custom_text:{page_target}:global", final_text)
        await r.delete(f"cmd_state:global:{m.from_user.id}")
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("العودة للتعديل", callback_data=f"edit_panel:texts_submenu:{m.from_user.id}")],
            [InlineKeyboardButton("حفظ", callback_data=f"edit_panel:done:{m.from_user.id}")]
        ])
        await m.reply(REPLIES['plugins_interact_372'], reply_markup=keyboard)
        return
    
    if state and state.startswith("waiting_emoji_"):
        if not await dev2_pls(m.from_user.id, m.chat.id):
            return
        
        if m.text == "الغاء":
            await r.delete(f"cmd_state:global:{m.from_user.id}")
            return await m.reply(REPLIES['plugins_interact_381'])
        
        custom_entity = None
        if m.entities:
            for entity in m.entities:
                if entity.type == MessageEntityType.CUSTOM_EMOJI:
                    custom_entity = entity
                    break
        
        if not custom_entity:
            return await m.reply(REPLIES['plugins_interact_391'])
        
        custom_emoji_id = custom_entity.custom_emoji_id
        # offset/length من تيليجرام بوحدات UTF-16، لا بفهرسة Python — التحويل
        # يمنع اقتطاع حرف خاطئ عندما يسبق الإيموجي أحرف خارج BMP في m.text.
        _start = utf16_offset_to_py_index(m.text, custom_entity.offset)
        _end = utf16_offset_to_py_index(m.text, custom_entity.offset + custom_entity.length)
        emoji_char = m.text[_start:_end]
        
        target = state.replace("waiting_emoji_", "")
        await r.set(f"cmd_emoji:{target}:global", custom_emoji_id)
        await r.set(f"cmd_emoji_char:{target}:global", emoji_char)
        await r.delete(f"cmd_state:global:{m.from_user.id}")
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("العودة", callback_data=f"edit_panel:emoji_submenu:{m.from_user.id}")],
            [InlineKeyboardButton("حفظ", callback_data=f"edit_panel:done:{m.from_user.id}")]
        ])
        await m.reply(plugins_interact_405(target), reply_markup=keyboard)
        return


@Client.on_message(filters.photo & filters.group, group=-1476)
async def catch_command_photo(c, m):
    r = get_redis(c)
    Dev_FINAL = get_dev_final(c)
    if not m.photo:
        return
    state = await r.get(f"cmd_state:global:{m.from_user.id}")
    if isinstance(state, bytes):
        state = state.decode("utf-8")
        
    if state == "waiting_photo":
        if not await dev2_pls(m.from_user.id, m.chat.id):
            return
        
        photo_id = m.photo.file_id
        await r.set(f"cmd_img:global", photo_id)
        await r.delete(f"cmd_state:global:{m.from_user.id}")
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("العودة للتعديل", callback_data=f"edit_panel:photo_submenu:{m.from_user.id}")],
            [InlineKeyboardButton("حفظ", callback_data=f"edit_panel:done:{m.from_user.id}")]
        ])
        await m.reply(REPLIES['plugins_interact_431'], reply_markup=keyboard)
        return


@Client.on_callback_query(filters.regex(r"^(edit_panel:|edit_cliche:|cmd_emoji:|del_cmd_emoji:|set_style:|toggle_btn:|close_cmds:|main_cmds:|commands|yesVER|noVER|delAdminMSG|yes:|no:)"), group=-17225)
async def CallbackQueryHandler(c, m):
    r = get_redis(c)
    Dev_FINAL = get_dev_final(c)
    k = '⇜'
    k = await r.get(f"{Dev_FINAL}:botkey")
    if isinstance(k, bytes):
        k = k.decode("utf-8")
    channel = await r.get(f"{Dev_FINAL}:BotChannel")
    if channel and isinstance(channel, bytes):
        channel = channel.decode("utf-8")
    if not channel:
        channel = " "
    
    await m.answer()
    
    if m.data.startswith("close_cmds:"):
        parts_c = m.data.split(":")
        if len(parts_c) < 2 or not parts_c[1].isdigit():
            return await m.answer()
        u_id = int(parts_c[1])
        if m.from_user.id != u_id:
            return await m.answer(REPLIES['plugins_cleanup_759'], show_alert=True)
        await m.message.delete()
        return

    if m.data.startswith("main_cmds:"):
        parts_c = m.data.split(":")
        if len(parts_c) < 2 or not parts_c[1].isdigit():
            return await m.answer()
        u_id = int(parts_c[1])
        if m.from_user.id != u_id:
            return await m.answer(REPLIES['plugins_cleanup_759'], show_alert=True)
        
        hidden_buttons = await r.get(f"cmd_hidden:global") or ""
        if isinstance(hidden_buttons, bytes):
            hidden_buttons = hidden_buttons.decode("utf-8")
        hidden_list = [int(x) for x in hidden_buttons.split(",") if x.isdigit()]
        
        commands_texts = {
            1: "¹ اوامر الادمنيه",
            2: "² اوامر الاعدادات",
            3: "³ اوامر القفل - الفتح",
            4: "⁴ اوامر التسلية",
            5: "⁵ اوامر الخدمية",
            6: "⁶ اوامر المطور",
            7: "⁷ اوامر الميوزك"
        }
        
        welcome_lines = ["اهليين فيك باوامر البوت\n"]
        for i in range(1, 8):
            if i not in hidden_list:
                welcome_lines.append(commands_texts[i])
        
        welcome_text = "\n".join(welcome_lines)
        await edit_with_style(c, m, welcome_text, 0)
        return

    if m.data.startswith("commands"):
        try:
            cmd_part = m.data.split(":")[0]  
            page_num = int(cmd_part.replace("commands", "")) 
            u_id = int(m.data.split(":")[1])
        except Exception:
            return

        if m.from_user.id != u_id:
            return await m.answer(REPLIES['plugins_cleanup_759'], show_alert=True)

        await CallbackQueryResponse(c, m, channel)
        return

    if m.data.startswith("edit_panel:"):
        parts = m.data.split(":")
        action = parts[1] if len(parts) > 1 else ""
        if len(parts) >= 3:
            u_id = int(parts[2])
        else:
            u_id = m.from_user.id
        
        if m.from_user.id != u_id:
            return await m.answer(REPLIES['plugins_cleanup_759'], show_alert=True)
            
        if action == "main":
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("اخفاء الازرار", callback_data=f"edit_panel:hide:{u_id}"),
                 InlineKeyboardButton("لون الازرار", callback_data=f"edit_panel:color:{u_id}")],
                [InlineKeyboardButton("الكلايش", callback_data=f"edit_panel:texts_submenu:{u_id}")],
                [InlineKeyboardButton("صورة الاوامر", callback_data=f"edit_panel:photo_submenu:{u_id}"),
                 InlineKeyboardButton("ايموجي الازرار", callback_data=f"edit_panel:emoji_submenu:{u_id}")],
                [InlineKeyboardButton("حفظ", callback_data=f"edit_panel:done:{u_id}")]
            ])
            await m.message.edit_text(REPLIES['plugins_interact_342'], reply_markup=keyboard)
            return
            

        elif action == "color":
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("① ازرار شفافة ↤︎ النقر شفاف", callback_data=f"set_style:default:{u_id}")],
                [InlineKeyboardButton("② ازرار شفافة ↤︎ النقر احمر", callback_data=f"set_style:style1:{u_id}")],
                [InlineKeyboardButton("③ ازرار شفافة ↤︎ النقر ازرق", callback_data=f"set_style:style2:{u_id}")],
                [InlineKeyboardButton("④ ازرار زرقاء ↤︎ النقر احمر", callback_data=f"set_style:style3:{u_id}")],
                [InlineKeyboardButton("⑤ ازرار حمراء ↤︎ النقر اخضر", callback_data=f"set_style:style4:{u_id}")],
                [InlineKeyboardButton("⑥ ازرار خضراء ↤︎ النقر ازرق", callback_data=f"set_style:style5:{u_id}")],
                [InlineKeyboardButton("رجوع", callback_data=f"edit_panel:main:{u_id}")]
            ])
            await m.message.edit_text(REPLIES['plugins_interact_541'], reply_markup=keyboard)
            return
            
        elif action == "hide":
            hidden_buttons = await r.get(f"cmd_hidden:global") or ""
            if isinstance(hidden_buttons, bytes):
                hidden_buttons = hidden_buttons.decode("utf-8")
            hidden_list = [int(x) for x in hidden_buttons.split(",") if x.isdigit()]
            
            buttons_names = {
                1: "اوامر الادمنيه",
                2: "اوامر الاعدادات", 
                3: "اوامر القفل - الفتح",
                4: "اوامر التسلية",
                5: "اوامر الخدمية",
                6: "اوامر المطور",
                7: "اوامر الميوزك"
            }
            
            numbers = {
                1: "①", 2: "②", 3: "③", 4: "④", 5: "⑤", 6: "⑥", 7: "⑦"
            }
            
            keyboard_btns = []
            row = []
            for i in range(1, 8):
                status = "نعم" if i in hidden_list else "لا"
                num = numbers.get(i, str(i))
                name = buttons_names.get(i, f"قائمة {i}")
                row.append(InlineKeyboardButton(f"{num} {status}", callback_data=f"toggle_btn:{i}:{u_id}"))
                if len(row) == 2:
                    keyboard_btns.append(row)
                    row = []
            if row:
                keyboard_btns.append(row)
            
            keyboard_btns.append([InlineKeyboardButton("رجوع", callback_data=f"edit_panel:main:{u_id}")])
            await m.message.edit_text(
                REPLIES['plugins_interact_578'],
                reply_markup=InlineKeyboardMarkup(keyboard_btns)
            )
            return
            
        elif action == "photo_submenu":
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("اضف صورة", callback_data=f"edit_panel:photo:{u_id}"),
                 InlineKeyboardButton("حذف صورة", callback_data=f"edit_panel:delphoto:{u_id}")],
                [InlineKeyboardButton("رجوع", callback_data=f"edit_panel:main:{u_id}")]
            ])
            await m.message.edit_text(REPLIES['plugins_interact_590'], reply_markup=keyboard)
            return

        elif action == "photo":
            await r.set(f"cmd_state:global:{u_id}", "waiting_photo")
            await m.message.edit_text(REPLIES['plugins_interact_595'])
            return

        elif action == "delphoto":
            await r.delete(f"cmd_img:global")
            await m.answer(REPLIES['plugins_interact_600'], show_alert=True)
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("رجوع", callback_data=f"edit_panel:photo_submenu:{u_id}")]
            ])
            await m.message.edit_text(REPLIES['plugins_interact_604'], reply_markup=keyboard)
            return
            
        elif action == "texts_submenu":
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("قائمة 1", callback_data=f"edit_cliche:1:{u_id}"),
                 InlineKeyboardButton("قائمة 2", callback_data=f"edit_cliche:2:{u_id}")],
                [InlineKeyboardButton("قائمة 3", callback_data=f"edit_cliche:3:{u_id}"),
                 InlineKeyboardButton("قائمة 4", callback_data=f"edit_cliche:4:{u_id}")],
                [InlineKeyboardButton("قائمة 5", callback_data=f"edit_cliche:5:{u_id}"),
                 InlineKeyboardButton("قائمة 7", callback_data=f"edit_cliche:7:{u_id}")],
                [InlineKeyboardButton("الافتراضي", callback_data=f"edit_cliche:reset:{u_id}"),
                 InlineKeyboardButton("رجوع", callback_data=f"edit_panel:main:{u_id}")]
            ])
            await m.message.edit_text(REPLIES['plugins_interact_618'], reply_markup=keyboard)
            return

        elif action == "emoji_submenu":
            buttons_list = []
            
            for i in range(1, 8):
                emoji_char = await r.get(f"cmd_emoji_char:{i}:global")
                if emoji_char and isinstance(emoji_char, bytes):
                    emoji_char = emoji_char.decode("utf-8")
                
                status = "🟩" if emoji_char else "⬜"
                buttons_list.append((f"{status} زر {i}", f"cmd_emoji:{i}"))
                buttons_list.append((f"🗑 حذف {i}", f"del_cmd_emoji:{i}"))
            
            buttons_list.append(("رجوع", "edit_panel:main"))
            
            keyboard_btns = []
            row = []
            for text, callback in buttons_list:
                row.append(InlineKeyboardButton(text, callback_data=f"{callback}:{u_id}"))
                if len(row) == 2:
                    keyboard_btns.append(row)
                    row = []
            if row:
                keyboard_btns.append(row)
            
            await m.message.edit_text(
                REPLIES['plugins_interact_645'],
                reply_markup=InlineKeyboardMarkup(keyboard_btns)
            )
            return

        elif action == "done":
            await r.delete(f"cmd_state:global:{u_id}")
            await m.message.edit_text(REPLIES['plugins_interact_653'])
            return

    if m.data.startswith("edit_cliche:"):
        parts = m.data.split(":")
        target = parts[1]
        u_id = int(parts[2])
        
        if m.from_user.id != u_id:
            return await m.answer(REPLIES['plugins_cleanup_759'], show_alert=True)
            
        if target == "reset":
            keys = await r.keys(f"cmd_custom_text:*:global")
            for key in keys:
                await r.delete(key)
            await m.answer(REPLIES['plugins_interact_668'], show_alert=True)
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("رجوع", callback_data=f"edit_panel:texts_submenu:{u_id}")]
            ])
            await m.message.edit_text(REPLIES['plugins_interact_672'], reply_markup=keyboard)
            return
        else:
            await r.set(f"cmd_state:global:{u_id}", f"waiting_text_{target}")
            await m.message.edit_text(plugins_interact_676(target))
            return

    if m.data.startswith("cmd_emoji:"):
        parts = m.data.split(":")
        target = parts[1]
        u_id = int(parts[2])
        
        if m.from_user.id != u_id:
            return await m.answer(REPLIES['plugins_cleanup_759'], show_alert=True)
        
        await r.set(f"cmd_state:global:{u_id}", f"waiting_emoji_{target}")
        await m.message.edit_text(plugins_interact_688(target))
        return

    if m.data.startswith("del_cmd_emoji:"):
        parts = m.data.split(":")
        target = parts[1]
        u_id = int(parts[2])
        
        if m.from_user.id != u_id:
            return await m.answer(REPLIES['plugins_cleanup_759'], show_alert=True)
        
        await r.delete(f"cmd_emoji:{target}:global")
        await r.delete(f"cmd_emoji_char:{target}:global")
        await m.answer(REPLIES['plugins_interact_701'], show_alert=True)
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("رجوع", callback_data=f"edit_panel:emoji_submenu:{u_id}")]
        ])
        await m.message.edit_text(REPLIES['plugins_interact_706'], reply_markup=keyboard)
        return

    if m.data.startswith("set_style:"):
        parts = m.data.split(":")
        style_name = parts[1]
        u_id = int(parts[2])
        
        if m.from_user.id != u_id:
            return await m.answer(REPLIES['plugins_cleanup_759'], show_alert=True)
            
        await r.set(f"cmd_style:global", style_name)
        await m.answer(REPLIES['plugins_interact_718'], show_alert=True)
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("رجوع", callback_data=f"edit_panel:main:{u_id}")]
        ])
        await m.message.edit_text(REPLIES['plugins_interact_723'], reply_markup=keyboard)
        return

    if m.data.startswith("toggle_btn:"):
        parts = m.data.split(":")
        btn_num = int(parts[1])
        u_id = int(parts[2])
        
        if m.from_user.id != u_id:
            return await m.answer(REPLIES['plugins_cleanup_759'], show_alert=True)
            
        hidden_buttons = await r.get(f"cmd_hidden:global") or ""
        if isinstance(hidden_buttons, bytes):
            hidden_buttons = hidden_buttons.decode("utf-8")
        hidden_list = [int(x) for x in hidden_buttons.split(",") if x.isdigit()]
        
        if btn_num in hidden_list:
            hidden_list.remove(btn_num)
        else:
            hidden_list.append(btn_num)
            
        new_hidden_str = ",".join([str(x) for x in hidden_list])
        await r.set(f"cmd_hidden:global", new_hidden_str)
        
        buttons_names = {
            1: "اوامر الادمنيه",
            2: "اوامر الاعدادات", 
            3: "اوامر القفل - الفتح",
            4: "اوامر التسلية",
            5: "اوامر الخدمية",
            6: "اوامر المطور",
            7: "اوامر الميوزك"
        }
        
        numbers = {
            1: "①", 2: "②", 3: "③", 4: "④", 5: "⑤", 6: "⑥", 7: "⑦"
        }
        
        keyboard_btns = []
        row = []
        for i in range(1, 8):
            status = "نعم" if i in hidden_list else "لا"
            num = numbers.get(i, str(i))
            name = buttons_names.get(i, f"قائمة {i}")
            row.append(InlineKeyboardButton(f"{num} {status}", callback_data=f"toggle_btn:{i}:{u_id}"))
            if len(row) == 2:
                keyboard_btns.append(row)
                row = []
        if row:
            keyboard_btns.append(row)
        
        keyboard_btns.append([InlineKeyboardButton("رجوع", callback_data=f"edit_panel:main:{u_id}")])
        await m.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(keyboard_btns))
        return

    await CallbackQueryResponse(c, m, channel)


async def CallbackQueryResponse(c, m, channel):
    r = get_redis(c)
    Dev_FINAL = get_dev_final(c)
    k = '⇜'
    k = await r.get(f"{Dev_FINAL}:botkey")
    if isinstance(k, bytes):
        k = k.decode("utf-8")
    
    try:
        u_id = int(m.data.split(":")[1])
    except:
        u_id = m.from_user.id
    
    if m.data == f"commands1:{u_id}":
        custom = await r.get(f"cmd_custom_text:1:global")
        if custom:
            text = custom.decode("utf-8") if isinstance(custom, bytes) else custom
        else:
            text = f"""• اهلا بك في اوامر الادمنيه:
━━━━━━━━━━━━
• اوامر الرفع والتنزيل:

• رفع - تنزيل مالك اساسي
• رفع - تنزيل مالك
• رفع - تنزيل مدير
• رفع - تنزيل ادمن
• رفع - تنزيل مشرف
• رفع - تنزيل مميز
• تنزيل الكل - لازالة جميع الرتب اعلاه

━━━━━━━━━━━━
• اوامر المسح:

• مسح الكل
• مسح المالكين
• مسح المدراء
• مسح الادمنيه
• مسح المميزين
• مسح المحظورين
• مسح المكتومين
• مسح قائمة المنع
• مسح الردود
• مسح الاوامر
• مسح الترحيب
• مسح الرابط
• مسح + العدد
• مسح بالرد
• مسح الايدي

━━━━━━━━━━━━
• اوامر الطرد والحظر:

• حظر - طرد
• كتم - تقييد
• الغاء الحظر
• الغاء الكتم
• الغاء التقييد
• رفع القيود
• منع الكلمة
• منع حزمه
• منع بالرد
• طرد البوتات
• كشف البوتات
_"""
        await edit_with_style(c, m, text, 1)
        return

    if m.data == f"commands2:{u_id}":
        custom = await r.get(f"cmd_custom_text:2:global")
        if custom:
            text = custom.decode("utf-8") if isinstance(custom, bytes) else custom
        else:
            text = f"""• اهلا بك في اوامر الاعدادات:
━━━━━━━━━━━━
• المطورين
• المالكيين الاساسيين
• المالكيين
• المدراء
• الادمنيه
• المشرفين
• المميزين
• المكتومين
• قائمه المنع
• القوانين
• الرابط
• انشاء رابط
• صلاحياتي
• صلاحيات
• الاعدادات
• التنظيف
• المجموعه
• الساعة
• التاريخ
• لقبي
━━━━━━━━━━━━
- اوامر وضع الاعدادات :
• مسح الرابط
• انشاء رابط
• تعيين الايدي
• وضع ترحيب
• وضع قوانين
• اضف امر
• التوديع - ضع التوديع - ضع صورة التوديع
• الترحيب الذكي - ضع صورة الترحيب - ضع الترحيب الذكي

━━━━━━━━━━━━
اوامر التحميل:
• تفعيل - تعطيل اليوت
• يوت + اسم الاغنية
• شازام (بالرد)
-"""
        await edit_with_style(c, m, text, 2)
        return

    if m.data == f"commands3:{u_id}":
        custom = await r.get(f"cmd_custom_text:3:global")
        if custom:
            text = custom.decode("utf-8") if isinstance(custom, bytes) else custom
        else:
            text = f"""• اهلا بك في اوامر القفل والفتح:
━━━━━━━━━━━━
• قفل - فتح الكلايش ~ الصور
• قفل - فتح الروابط ~ البوتات
• قفل - فتح اليوزرات ~ التعديل
• قفل - فتح تعديل الميديا ~ الفيديو
• قفل - فتح الملصقات ~ المتحركات
• قفل - فتح الفويسات ~ الملفات
• قفل - فتح الدخول ~ الصوت
• قفل - فتح الهشتاق ~ الإشعارات
• قفل - فتح الكلام الكثير ~ التكرار
• قفل - فتح التوجيه ~ الانلاين
• قفل - فتح الجهات ~ السب
• قفل - فتح الإضافة ~ القنوات
• قفل - فتح الفارسية ~ الايراني
• قفل - فتح الإباحي ~ الجمثون
• قفل - فتح الملصقات المميزه
• قفل - فتح التوجيه بالتقييد
• قفل - فتح الروابط بالتقييد
• قفل - فتح المتحركه بالتقييد
• قفل - فتح الصور بالتقييد
• قفل - فتح الفيديو بالتقييد

━━━━━━━━━━━━
• اوامر التفعيل - تعطيل

• الترحيب
• الردود
• التحقق
• الايدي
• اطردني
• الحماية
• التحذير
• انطق
• شازام
• المنشن
• اليوتيوب
• استبدال الحزم
• تحويل الصيغ
• التيك
• اشعارات البوت
• رفع المشرفين
• الردود العامه
• اسباب المشرفين
_"""
        await edit_with_style(c, m, text, 3)
        return

    if m.data == f"commands4:{u_id}":
        custom = await r.get(f"cmd_custom_text:4:global")
        if custom:
            text = custom.decode("utf-8") if isinstance(custom, bytes) else custom
        else:
            text = f"""• اهلا بك في اوامر التسليه :
━━━━━━━━━━━━
- اوامر تسلية تظهر بالايدي :

• رفع - تنزيل : هطف : الهطوف
• رفع - تنزيل : بثر : البثرين
• رفع - تنزيل : حمار : الحمير
• رفع - تنزيل : كلب : الكلاب
• رفع - تنزيل : كلبه : الكلبات
• رفع - تنزيل : عتوي : العتوين
• رفع - تنزيل : عتويه : العتويات
• رفع - تنزيل : لحجي : اللحوج
• رفع - تنزيل : لحجيه : اللحجيات
• رفع - تنزيل : خروف : الخرفان
• رفع - تنزيل : خفيفه : الخفيفات
• رفع - تنزيل : خفيف : الخفيفين
• رفع بقلبي  : تنزيل من قلبي
━━━━━━━━━━━━
للقروب:
رفع + اسم اختياري 
• مسح رتب التسليه
• رتب التسليه
• تعطيل التسليه
━━━━━━━━━━━━
للعام:
• رفع عام +اسم اختياري
• رتب التسليه عام
• مسح رتب التسليه
━━━━━━━━━━━━
• طلاق - زواج 
• زوجي - زوجتي
• تتزوجني
━━━━━━━━━━━━
•اكتموه (تصويت)
• تعطيل - تفعيل : اكتموه
• تعطيل - تفعيل : زوجني
_"""
        await edit_with_style(c, m, text, 4)
        return

    if m.data == f"commands5:{u_id}":
        custom = await r.get(f"cmd_custom_text:5:global")
        if custom:
            text = custom.decode("utf-8") if isinstance(custom, bytes) else custom
        else:
            text = f"""• اهلا بك في الاوامر الخدمية:
━━━━━━━━━━━━            
• نسبه الحب - الكره
• نسبه الصداقه - الذكاء
• نسبه الغباء - شخصيتي
• شبيهي - شبيهتي
• ريمكس - اطربني
• لو خيروك - صراحه
• انطقي + الكلمة
• وش يقول؟ بالرد
• افتاري • صوره
• افتار ↢ باليوزر او بالرد
• بايو • مين ضافني؟
• شازام بالرد
• ايدي - الانشاء
• مجموعاتي - ابلاغ
• نادي المطور
• قران
• اذكار
• شعر
• اقتباسات
• قصص
• اطربني
• اغاني
• ميمز
• ايدت

━━━━━━━━━━━━
• الردود
• اضف رد متعدد
• اضف رد مميز
• اضف رد
• اضف رد انلاين
• مسح رد - انلاين - متعدد - مميز

━━━━━━━━━━━━
• التحميل:
• ساوند + الرابط
• تيك + الرابط
• تحويل الصيغ:
- فويس بالرد على ملف mp3 
- اوديو بالرد على فويس 
- ملصق بالرد على صورة 
- صورة بالرد على ملصق 
- ملصق متحركة بالرد على قيف 
- متحركة بالرد على فيديو او ملصق 
- صوت بالرد على فيديو 
- وش مكتوب بالرد على صورة
_"""
        await edit_with_style(c, m, text, 5)
        return

    if m.data == f"commands6:{u_id}":
        text = f"""• اهلا بك في اوامر المطور:
━━━━━━━━━━━━

• ترحيب البوت
• حذف رد تواصل
• ردود التواصل
• تعطيل
• اسم بوتك + غادر
• مسح المالكين الاساسيين
• مسح صوره الترحيب
• اذاعه + ايدي المجموعه - بالرد
• فتح - قفل ردود MY
• رفع - تنزيل Dev
• فتح - قفل الاحصائيات
• حظر - كتم عام
• حظر - الغاء حظر بالرد
• المحظورين عام
• الغاء كتم عام - الغاء عام
• مسح المكتومين عام
• مسح المحظورين عام
• قائمه الرتب العامه
• تغير الرتب العام
• مسح رتب العام
• مسح رتبه عام
• الردود العامه
• الردود المتعدده العامه
• مسح الردود العامه
• مسح الردود المتعدده العامه
• اضف رد عام
• اضف رد متعدد عام
• اضف رد انلاين عام
• اضف رد مميز عام
• اضف لعبه عام
• تعديل الاوامر
• تعديل زر
• تحديث
• اضف ايموجي مميز
• اضف كلمه جنس
• تعطيل اشراف المطورين
_"""
        await edit_with_style(c, m, text, 6)
        return

    if m.data == f"commands7:{u_id}":
        custom = await r.get(f"cmd_custom_text:7:global")
        if custom:
            text = custom.decode("utf-8") if isinstance(custom, bytes) else custom
        else:
            text = f"""• اهلا بك في اوامر الميوزك:
━━━━━━━━━━━━
• تشغيل ↢ بالاسم او الرد او الرابط
• فيديو ↢ بالاسم او الرد او الرابط
• وقف
• كمل
• تخطي
• ايقاف
• رفع مشغل 
• تنزيل مشغل
• المشغلين
• مين في الكول 
_"""
        await edit_with_style(c, m, text, 7)
        return

    if m.data == "delAdminMSG":
        if str(m.from_user.id) in m.message.html:
            return await m.message.delete()

    if m.data == f"yes:{m.from_user.id}":
        try:
            await c.restrict_chat_member(
                m.message.chat.id,
                m.from_user.id,
                ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_other_messages=True,
                    can_send_polls=True,
                    can_invite_users=True,
                    can_add_web_page_previews=True,
                    can_change_info=True,
                    can_pin_messages=True,
                ),
            )
        except:
            return False
        await m.edit_message_text(
            plugins_interact_1137(k),
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🧚‍♀️", url=f"t.me/{channel}")]]
            ),
        )
        return

    if m.data == f"no:{m.from_user.id}":
        await m.edit_message_text(
            plugins_interact_1146(k),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "رفع التقييد",
                            callback_data=f"yesVER:{m.from_user.id}",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "طرد", callback_data=f"noVER:{m.from_user.id}"
                        )
                    ],
                ]
            ),
        )
        return

    if m.data.startswith("yesVER"):
        user_id = int(m.data.split(":")[1])
        if not await admin_pls(m.from_user.id, m.message.chat.id):
            return await m.answer(plugins_interact_1169(k), show_alert=True)
        else:
            await m.edit_message_text(plugins_interact_1171(k))
            try:
                await c.restrict_chat_member(
                    m.message.chat.id,
                    user_id,
                    ChatPermissions(
                        can_send_messages=True,
                        can_send_media_messages=True,
                        can_send_other_messages=True,
                        can_send_polls=True,
                        can_invite_users=True,
                        can_add_web_page_previews=True,
                        can_change_info=True,
                        can_pin_messages=True,
                    ),
                )
            except:
                return False
        return

    if m.data.startswith("noVER"):
        user_id = int(m.data.split(":")[1])
        if not await admin_pls(m.from_user.id, m.message.chat.id):
            return await m.answer(plugins_interact_1194(k), show_alert=True)
        else:
            await m.edit_message_text(plugins_interact_1196(k))
            try:
                await m.message.chat.ban_member(user_id)
                await m.message.chat.unban_member(user_id)
            except:
                pass
        return

    if m.data == "yes:del:bank":
        if not await devp_pls(m.from_user.id, m.message.chat.id):
            return await m.answer(REPLIES['plugins_interact_1206'])
        else:
            await m.edit_message_text(REPLIES['plugins_interact_1208'])
            keys = await r.keys("*:Floos")
            for a in keys:
                await r.delete(a)
            for a in await r.keys("*:BankWait"):
                await r.delete(a)
            for a in await r.keys("*:BankWaitB5"):
                await r.delete(a)
            for a in await r.keys("*:BankWaitZRF"):
                await r.delete(a)
            for a in await r.keys("*:BankWaitEST"):
                await r.delete(a)
            for a in await r.keys("*:BankWaitHZ"):
                await r.delete(a)
            for a in await r.keys("*:BankWait3JL"):
                await r.delete(a)
            for a in await r.keys("*:Zrf"):
                await r.delete(a)
            await r.delete("BankTop")
            await r.delete("BankTopZRF")
            return True

    if m.data == "no:del:bank":
        if not await devp_pls(m.from_user.id, m.message.chat.id):
            return await m.answer(REPLIES['plugins_interact_1206'])
        else:
            await m.message.delete()
        return

    name = await r.get(f"{Dev_FINAL}:BotName")
    if name and isinstance(name, bytes):
        name = name.decode("utf-8")
    if not name:
        name = "فاينل"
    
    if m.data == f"RPS:rock++{m.from_user.id}":
        RPS = ["paper", "scissors", "rock"]
        kk = random.choice(RPS)
        if kk == "scissors":
            if await r.get(f"{m.from_user.id}:Floos"):
                get = int((await r.get(f"{m.from_user.id}:Floos")) or 0)
                await r.set(f"{m.from_user.id}:Floos", get + 1)
            else:
                await r.set(f"{m.from_user.id}:Floos", 1)
            rep = InlineKeyboardMarkup(
                [[InlineKeyboardButton("🧚‍♀️", url=f"t.me/{channel}")]]
            )
            await m.edit_message_text(
                plugins_interact_1255(m.from_user.first_name),
                disable_web_page_preview=True,
                reply_markup=rep,
            )
        if kk == "paper":
            rep = InlineKeyboardMarkup(
                [[InlineKeyboardButton("🧚‍♀️", url=f"t.me/{channel}")]]
            )
            await m.edit_message_text(
                plugins_interact_1269(name.replace("*","").replace("`","").replace("|","").replace("#","").replace("<","").replace(">","").replace("_","")),
                disable_web_page_preview=True,
                reply_markup=rep,
            )
        if kk == "rock":
            rep = InlineKeyboardMarkup(
                [[InlineKeyboardButton("🧚‍♀️", url=f"t.me/{channel}")]]
            )
            await m.edit_message_text(
                plugins_interact_1283(name.replace("*","").replace("`","").replace("|","").replace("#","").replace("<","").replace(">","").replace("_","")),
                disable_web_page_preview=True,
                reply_markup=rep,
            )
        return

    if m.data == f"RPS:paper++{m.from_user.id}":
        RPS = ["paper", "scissors", "rock"]
        kk = random.choice(RPS)
        if kk == "rock":
            if await r.get(f"{m.from_user.id}:Floos"):
                get = int((await r.get(f"{m.from_user.id}:Floos")) or 0)
                await r.set(f"{m.from_user.id}:Floos", get + 1)
            else:
                await r.set(f"{m.from_user.id}:Floos", 1)
            rep = InlineKeyboardMarkup(
                [[InlineKeyboardButton("🧚‍♀️", url=f"t.me/{channel}")]]
            )
            await m.edit_message_text(
                plugins_interact_1307(m.from_user.first_name),
                disable_web_page_preview=True,
                reply_markup=rep,
            )
        if kk == "scissors":
            rep = InlineKeyboardMarkup(
                [[InlineKeyboardButton("🧚‍♀️", url=f"t.me/{channel}")]]
            )
            await m.edit_message_text(
                plugins_interact_1321(name.replace("*","").replace("`","").replace("|","").replace("#","").replace("<","").replace(">","").replace("_","")),
                disable_web_page_preview=True,
                reply_markup=rep,
            )
        if kk == "paper":
            rep = InlineKeyboardMarkup(
                [[InlineKeyboardButton("🧚‍♀️", url=f"t.me/{channel}")]]
            )
            await m.edit_message_text(
                plugins_interact_1335(name.replace("*","").replace("`","").replace("|","").replace("#","").replace("<","").replace(">","").replace("_","")),
                disable_web_page_preview=True,
                reply_markup=rep,
            )
        return

    if m.data == f"RPS:scissors++{m.from_user.id}":
        RPS = ["paper", "scissors", "rock"]
        kk = random.choice(RPS)
        if kk == "paper":
            if await r.get(f"{m.from_user.id}:Floos"):
                get = int((await r.get(f"{m.from_user.id}:Floos")) or 0)
                await r.set(f"{m.from_user.id}:Floos", get + 1)
            else:
                await r.set(f"{m.from_user.id}:Floos", 1)
            rep = InlineKeyboardMarkup(
                [[InlineKeyboardButton("🧚‍♀️", url=f"t.me/{channel}")]]
            )
            await m.edit_message_text(
                plugins_interact_1359(m.from_user.first_name),
                disable_web_page_preview=True,
                reply_markup=rep,
            )
        if kk == "rock":
            rep = InlineKeyboardMarkup(
                [[InlineKeyboardButton("🧚‍♀️", url=f"t.me/{channel}")]]
            )
            await m.edit_message_text(
                plugins_interact_1373(name.replace("*","").replace("`","").replace("|","").replace("#","").replace("<","").replace(">","").replace("_","")),
                disable_web_page_preview=True,
                reply_markup=rep,
            )
        if kk == "scissors":
            rep = InlineKeyboardMarkup(
                [[InlineKeyboardButton("🧚‍♀️", url=f"t.me/{channel}")]]
            )
            await m.edit_message_text(
                plugins_interact_1387(name.replace("*","").replace("`","").replace("|","").replace("#","").replace("<","").replace(">","").replace("_","")),
                disable_web_page_preview=True,
                reply_markup=rep,
            )
        return

    if m.data == f"gowner+{m.from_user.id}":
        if not await gowner_pls(m.from_user.id, m.message.chat.id):
            await m.answer(REPLIES['plugins_interact_1401'], show_alert=True)
            return await m.message.delete()
        else:
            command = m.message.reply_to_message.text.split(None, 2)[2]
            await r.hset(Dev_FINAL + f"locks-{m.message.chat.id}", command, 0)
            await m.edit_message_text(
                plugins_interact_1406(command)
            )
            return

    if m.data == f"owner+{m.from_user.id}":
        if not await gowner_pls(m.from_user.id, m.message.chat.id):
            await m.answer(REPLIES['plugins_interact_1401'], show_alert=True)
            return await m.message.delete()
        else:
            command = m.message.reply_to_message.text.split(None, 2)[2]
            await r.hset(Dev_FINAL + f"locks-{m.message.chat.id}", command, 1)
            await m.edit_message_text(
                plugins_interact_1418(command)
            )
            return

    if m.data == f"mod+{m.from_user.id}":
        if not await gowner_pls(m.from_user.id, m.message.chat.id):
            await m.answer(REPLIES['plugins_interact_1401'], show_alert=True)
            return await m.message.delete()
        else:
            command = m.message.reply_to_message.text.split(None, 2)[2]
            await r.hset(Dev_FINAL + f"locks-{m.message.chat.id}", command, 2)
            await m.edit_message_text(
                plugins_interact_1430(command)
            )
            return

    if m.data == f"admin+{m.from_user.id}":
        if not await gowner_pls(m.from_user.id, m.message.chat.id):
            await m.answer(REPLIES['plugins_interact_1401'], show_alert=True)
            return await m.message.delete()
        else:
            command = m.message.reply_to_message.text.split(None, 2)[2]
            await r.hset(Dev_FINAL + f"locks-{m.message.chat.id}", command, 3)
            await m.edit_message_text(
                plugins_interact_1442(command)
            )
            return

    if m.data == f"pre+{m.from_user.id}":
        if not await gowner_pls(m.from_user.id, m.message.chat.id):
            await m.answer(REPLIES['plugins_interact_1401'], show_alert=True)
            return await m.message.delete()
        else:
            command = m.message.reply_to_message.text.split(None, 2)[2]
            await r.hset(Dev_FINAL + f"locks-{m.message.chat.id}", command, 4)
            await m.edit_message_text(
                plugins_interact_1454(command)
            )
            return