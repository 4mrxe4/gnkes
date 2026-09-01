from helpers.context import get_global_r, get_global_dev, get_global_k
r = get_global_r()
Dev_FINAL = get_global_dev()
k = get_global_k()
from compat import *
from compat import *
from compat import *
from helpers.ranks import *
from .buttons import register_buttons, get_button_custom, get_button_color, create_button_raw, send_telegram_api
from datetime import datetime, timedelta
import json
from helpers.replies_store import (
    REPLIES,
    plugins_owners_182,
    plugins_owners_190,
    plugins_owners_192,
    plugins_owners_197,
    plugins_owners_204,
    plugins_owners_207,
    plugins_owners_217,
    plugins_owners_224,
    plugins_owners_228,
    plugins_owners_238,
    plugins_owners_245,
    plugins_owners_250,
    plugins_owners_258,
    plugins_owners_262,
    plugins_owners_280,
    plugins_owners_283,
    plugins_owners_290,
    plugins_owners_322,
    plugins_owners_328,
    plugins_owners_342,
    plugins_owners_358,
    plugins_owners_361,
    plugins_owners_365,
    plugins_owners_374,
    plugins_owners_386,
    plugins_owners_422,
)

BUTTONS_DEFINITIONS = {
    "admi": {
        "name": "أزرار gg",
        "buttons": [
            {"id": "ideal_btn", "default": "العضو المثالي"},
        ]
    }
}
register_buttons(BUTTONS_DEFINITIONS)

TYPES_AR = {"member": "عضو", "mod": "مشرف"}

def cleeshe_photo_key(chat_id, type_key):
    return f"{chat_id}:cleeshe_photo:{type_key}:{Dev_FINAL}"

def cleeshe_desc_key(chat_id, type_key):
    return f"{chat_id}:cleeshe_desc:{type_key}:{Dev_FINAL}"

def cleeshe_btn_key(chat_id, type_key):
    return f"{chat_id}:cleeshe_btn:{type_key}:{Dev_FINAL}"

def ideal_key(chat_id, type_key):
    return f"{chat_id}:ideal_{type_key}:{Dev_FINAL}"

async def clear_pending_state(user_id):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    await r.delete(
        f"{user_id}:cleeshe_state:{Dev_FINAL}",
        f"{user_id}:cleeshe_type:{Dev_FINAL}",
        f"{user_id}:cleeshe_chat:{Dev_FINAL}",
        f"{user_id}:cleeshe_photo_tmp:{Dev_FINAL}",
        f"{user_id}:cleeshe_desc_tmp:{Dev_FINAL}",
    )

def get_admin_stats_key(chat_id, admin_id, period):
    return f"{chat_id}:admin_stats:{admin_id}:{period}:{Dev_FINAL}"

def get_admin_stats_total_key(chat_id, admin_id):
    return f"{chat_id}:admin_stats_total:{admin_id}:{Dev_FINAL}"

def get_admin_actions_key(chat_id, admin_id, action, period):
    return f"{chat_id}:admin_actions:{admin_id}:{action}:{period}:{Dev_FINAL}"

def get_admin_actions_total_key(chat_id, admin_id, action):
    return f"{chat_id}:admin_actions_total:{admin_id}:{action}:{Dev_FINAL}"

async def increment_admin_action(chat_id, admin_id, action):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    
    today = datetime.now().strftime("%Y-%m-%d")
    week_start = (datetime.now() - timedelta(days=datetime.now().weekday())).strftime("%Y-%m-%d")
    
    day_key = get_admin_actions_key(chat_id, admin_id, action, f"day:{today}")
    await r.incr(day_key)
    await r.expire(day_key, 86400)
    
    week_key = get_admin_actions_key(chat_id, admin_id, action, f"week:{week_start}")
    await r.incr(week_key)
    await r.expire(week_key, 604800)
    
    total_key = get_admin_actions_total_key(chat_id, admin_id, action)
    await r.incr(total_key)

@Client.on_message(filters.group & ~filters.bot, group=-133)
async def track_admin_messages_handler(c, m):
    if not m.from_user:
        return
    
    chat_id = m.chat.id
    admin_id = m.from_user.id
    
    if await gowner_pls(admin_id, chat_id):
        r = get_global_r()
        Dev_FINAL = get_global_dev()
        
        today = datetime.now().strftime("%Y-%m-%d")
        week_start = (datetime.now() - timedelta(days=datetime.now().weekday())).strftime("%Y-%m-%d")
        
        day_msg_key = f"{Dev_FINAL}{chat_id}:AdminDayMsgs:{admin_id}:{today}"
        await r.incr(day_msg_key)
        await r.expire(day_msg_key, 172800)
        
        week_msg_key = f"{Dev_FINAL}{chat_id}:AdminWeekMsgs:{admin_id}:{week_start}"
        await r.incr(week_msg_key)
        await r.expire(week_msg_key, 1209600)
        
        total_msg_key = f"{Dev_FINAL}{chat_id}:AdminTotalMsgs:{admin_id}"
        await r.incr(total_msg_key)

async def get_admin_stats(chat_id, admin_id):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    
    today = datetime.now().strftime("%Y-%m-%d")
    week_start = (datetime.now() - timedelta(days=datetime.now().weekday())).strftime("%Y-%m-%d")
    
    actions = ["ban", "kick", "mute", "restrict", "warn"]
    stats = {}
    
    for action in actions:
        key = get_admin_actions_key(chat_id, admin_id, action, f"day:{today}")
        val = await r.get(key) or 0
        stats[f"{action}_day"] = int(val)
    
    for action in actions:
        key = get_admin_actions_key(chat_id, admin_id, action, f"week:{week_start}")
        val = await r.get(key) or 0
        stats[f"{action}_week"] = int(val)
    
    for action in actions:
        key = get_admin_actions_total_key(chat_id, admin_id, action)
        val = await r.get(key) or 0
        stats[f"{action}_total"] = int(val)
    
    day_interaction = await r.get(f"{Dev_FINAL}{chat_id}:AdminDayMsgs:{admin_id}:{today}") or 0
    week_interaction = await r.get(f"{Dev_FINAL}{chat_id}:AdminWeekMsgs:{admin_id}:{week_start}") or 0
    total_interaction = await r.get(f"{Dev_FINAL}{chat_id}:AdminTotalMsgs:{admin_id}") or 0
    
    stats["interaction_day"] = int(day_interaction)
    stats["interaction_week"] = int(week_interaction)
    stats["interaction_total"] = int(total_interaction)
    
    return stats

async def show_admin_stats_text(chat_id, admin_user):
    k = get_global_k()
    admin_id = admin_user.id
    rank = await get_rank(admin_id, chat_id)
    stats = await get_admin_stats(chat_id, admin_id)
    
    text = f"""‹ إحصائيات المشرف ›

• اسمه ↢ {admin_user.mention()}
• ايديه ↢ `{admin_id}`
• رتبتة ↢ {rank}
• تفاعله اليوم ↢ {stats['interaction_day']}
• تفاعله الاسبوعي ↢ {stats['interaction_week']}
• مجموع تفاعله ↢ {stats['interaction_total']}
• عدد الحظر اليوم ↢ {stats['ban_day']}
• مجموع الحظر الاسبوعي ↢ {stats['ban_week']}
• عدد الكتم اليوم ↢ {stats['mute_day']}
• مجموع الكتم الاسبوعي ↢ {stats['mute_week']}
• عدد الطرد اليوم ↢ {stats['kick_day']}
• مجموع الطرد الاسبوعي ↢ {stats['kick_week']}
• عدد التقييد اليوم ↢ {stats['restrict_day']}
• مجموع التقييد الاسبوعي ↢ {stats['restrict_week']}
• عدد الانذارات اليوم ↢ {stats['warn_day']}
• مجموع الانذارات الاسبوعي ↢ {stats['warn_week']}"""
    
    return text

async def track_admin_action(chat_id, admin_id, action):
    try:
        await increment_admin_action(chat_id, admin_id, action)
    except Exception as e:
        print(f"[Admin Stats] خطأ في تسجيل إجراء {action} للمشرف {admin_id}: {e}")

@Client.on_message(filters.group & ~filters.bot & filters.text, group=-132)
async def owners_group_commands(c, m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    k = await r.get(f'{Dev_FINAL}:botkey') or k
    text = (m.text or "").strip()

    if not await check_global_restrictions(c, m, k, caller='owners'):
        return False

    if text in ["ضع كليشه عضو", "ضع كليشه مشرف"]:
        if not await gowner_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_owners_182(k))

        type_key = "member" if text == "ضع كليشه عضو" else "mod"
        type_ar = TYPES_AR[type_key]

        try:
            me = await c.get_me()
            if not me.username:
                return await m.reply(plugins_owners_190(k))
        except Exception:
            return await m.reply(plugins_owners_192(k))

        payload = f"cleeshe_{type_key}_{m.chat.id}"
        url = f"https://t.me/{me.username}?start={payload}"
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton("اضغط هنا", url=url)]])
        return await m.reply(
            plugins_owners_197(k, type_ar),
            reply_markup=buttons
        )

    if text in ["رفع عضو مثالي", "رفع مشرف مثالي"]:
        if not await gowner_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_owners_204(k))

        if not m.reply_to_message or not m.reply_to_message.from_user:
            return await m.reply(plugins_owners_207(k))

        type_key = "member" if text == "رفع عضو مثالي" else "mod"
        type_ar = TYPES_AR[type_key]

        photo = await r.get(cleeshe_photo_key(m.chat.id, type_key))
        desc = await r.get(cleeshe_desc_key(m.chat.id, type_key))
        btn_text = await r.get(cleeshe_btn_key(m.chat.id, type_key))

        if not photo or not desc or not btn_text:
            return await m.reply(
                plugins_owners_217(k, type_ar, k, type_ar)
            )

        target = m.reply_to_message.from_user
        if target.is_bot:
            return await m.reply(plugins_owners_224(k))

        await r.set(ideal_key(m.chat.id, type_key), target.id)

        return await m.reply(
            plugins_owners_228(k, target.mention(), k, type_ar)
        )

    if text in ["العضو المثالي", "المشرف المثالي"]:
        type_key = "member" if text == "العضو المثالي" else "mod"
        type_ar = TYPES_AR[type_key]

        ideal_user_id = await r.get(ideal_key(m.chat.id, type_key))
        if not ideal_user_id:
            return await m.reply(plugins_owners_238(k, type_ar))

        photo = await r.get(cleeshe_photo_key(m.chat.id, type_key))
        desc = await r.get(cleeshe_desc_key(m.chat.id, type_key))
        btn_text = await r.get(cleeshe_btn_key(m.chat.id, type_key))

        if not photo or not desc or not btn_text:
            return await m.reply(plugins_owners_245(k))

        try:
            target_id = int(ideal_user_id)
        except Exception:
            return await m.reply(plugins_owners_250(k, type_ar))

        ideal_btn = await create_button_raw("admi", "ideal_btn", btn_text, user_id=target_id)
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(**ideal_btn)]])
        
        try:
            return await m.reply_photo(photo, caption=desc, reply_markup=reply_markup)
        except Exception:
            return await m.reply(plugins_owners_258(k, type_ar))

    if text == "تفاعل مشرف":
        if not await gowner_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_owners_262(k))
        
        target_user = None
        
        if m.reply_to_message and m.reply_to_message.from_user:
            target_user = m.reply_to_message.from_user
        else:
            parts = text.split()
            if len(parts) > 1:
                try:
                    if parts[1].startswith("@"):
                        target_user = await c.get_users(parts[1])
                    elif parts[1].isdigit():
                        target_user = await c.get_users(int(parts[1]))
                except:
                    pass
        
        if not target_user:
            return await m.reply(plugins_owners_280(k))
        
        if not await admin_pls(target_user.id, m.chat.id):
            return await m.reply(plugins_owners_283(k))
        
        requester_id = m.from_user.id
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("أضغط لرؤية تفاعل", callback_data=f"show_admin_stats:{m.chat.id}:{target_user.id}:{requester_id}")]
        ])
        
        return await m.reply(
            plugins_owners_290(target_user.mention()),
            reply_markup=buttons
        )

@Client.on_message(filters.private & filters.command("start"), group=-131)
async def owners_start_handler(c, m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()

    if not m.command or len(m.command) < 2:
        return

    args = m.command
    if not args[1].startswith("cleeshe_"):
        return

    parts = args[1].split("_")
    if len(parts) < 3:
        return

    type_key = parts[1]
    if type_key not in TYPES_AR:
        return

    try:
        chat_id = int(parts[2])
    except Exception:
        return

    if not await gowner_pls(m.from_user.id, chat_id):
        return await m.reply(plugins_owners_322(k))

    await r.set(f"{m.from_user.id}:cleeshe_state:{Dev_FINAL}", "awaiting_photo", ex=900)
    await r.set(f"{m.from_user.id}:cleeshe_type:{Dev_FINAL}", type_key, ex=900)
    await r.set(f"{m.from_user.id}:cleeshe_chat:{Dev_FINAL}", chat_id, ex=900)

    return await m.reply(plugins_owners_328(k))

@Client.on_message(filters.private & filters.photo, group=-130)
async def owners_photo_handler(c, m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()

    state = await r.get(f"{m.from_user.id}:cleeshe_state:{Dev_FINAL}")
    if state != "awaiting_photo":
        return

    await r.set(f"{m.from_user.id}:cleeshe_photo_tmp:{Dev_FINAL}", m.photo.file_id, ex=900)
    await r.set(f"{m.from_user.id}:cleeshe_state:{Dev_FINAL}", "awaiting_desc", ex=900)
    return await m.reply(plugins_owners_342(k))

@Client.on_message(filters.private & filters.text & ~filters.command("start"), group=-129)
async def owners_text_handler(c, m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()

    state = await r.get(f"{m.from_user.id}:cleeshe_state:{Dev_FINAL}")
    if not state:
        return

    text = m.text or ""

    if state == "awaiting_desc":
        if not text.strip():
            return await m.reply(plugins_owners_358(k))
        await r.set(f"{m.from_user.id}:cleeshe_desc_tmp:{Dev_FINAL}", text, ex=900)
        await r.set(f"{m.from_user.id}:cleeshe_state:{Dev_FINAL}", "awaiting_btn", ex=900)
        return await m.reply(plugins_owners_361(k))

    if state == "awaiting_btn":
        if not text.strip():
            return await m.reply(plugins_owners_365(k))

        chat_id = await r.get(f"{m.from_user.id}:cleeshe_chat:{Dev_FINAL}")
        type_key = await r.get(f"{m.from_user.id}:cleeshe_type:{Dev_FINAL}")
        photo = await r.get(f"{m.from_user.id}:cleeshe_photo_tmp:{Dev_FINAL}")
        desc = await r.get(f"{m.from_user.id}:cleeshe_desc_tmp:{Dev_FINAL}")

        if not chat_id or not type_key or not photo or not desc:
            await clear_pending_state(m.from_user.id)
            return await m.reply(plugins_owners_374(k))

        chat_id = int(chat_id)
        btn_text = text.strip()

        await r.set(cleeshe_photo_key(chat_id, type_key), photo)
        await r.set(cleeshe_desc_key(chat_id, type_key), desc)
        await r.set(cleeshe_btn_key(chat_id, type_key), btn_text)

        await clear_pending_state(m.from_user.id)

        type_ar = TYPES_AR[type_key]
        return await m.reply(
            plugins_owners_386(k, type_ar)
        )

@Client.on_callback_query(filters.regex(r"^show_admin_stats:"))
async def handle_admin_stats_callback(c, cb: CallbackQuery):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    k = await r.get(f'{Dev_FINAL}:botkey') or k
    
    parts = cb.data.split(":")
    if len(parts) < 3:
        return await cb.answer(REPLIES['plugins_owners_399'], show_alert=True)
    chat_id = int(parts[1])
    admin_id = int(parts[2])
    requester_id = int(parts[3]) if len(parts) > 3 and parts[3].isdigit() else None
    
    if requester_id and cb.from_user.id != requester_id:
        return await cb.answer(REPLIES['plugins_games_clubs_1060'], show_alert=True)
    
    if not await gowner_pls(cb.from_user.id, chat_id):
        return await cb.answer(REPLIES['plugins_owners_408'], show_alert=True)
    
    try:
        target_user = await c.get_users(admin_id)
    except:
        return await cb.answer(REPLIES['plugins_owners_413'], show_alert=True)
    
    stats_text = await show_admin_stats_text(chat_id, target_user)
    
    try:
        await c.send_message(chat_id=cb.from_user.id, text=stats_text)
    except Exception:
        return await cb.answer(REPLIES['plugins_owners_420'], show_alert=True)
    
    await cb.message.edit_text(plugins_owners_422(k, target_user.mention()))
    await cb.answer()

@Client.on_callback_query(filters.regex(r"^hide_admin_stats:"))
async def handle_hide_admin_stats(c, cb: CallbackQuery):
    await cb.message.delete()
    await cb.answer()