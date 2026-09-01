# helpers/_admins.py — rebuilt for botm_unified
# THE ONLY source of rank/authorization truth is the PARENT system
# (helpers.ranks). No independent rank system is kept here.
from functools import wraps

from helpers.context import is_sudoer, redis_proxy as r, dev_final_proxy as Dev_FINAL, k_proxy as k
from helpers.ranks import admin_pls, mod_pls, owner_pls, gowner_pls, dev_pls, pre_pls, get_rank
from compat import CompatMessage, CompatCallbackQuery


async def get_admins(chat_id: int) -> list[int]:
    """Best-effort chat admins via parent client; falls back to cached list.
    Rank checks themselves always go through helpers.ranks."""
    admins_data = await r.get(f"chat_admins:{chat_id}:{Dev_FINAL}")
    if admins_data:
        try:
            return eval(admins_data) if isinstance(admins_data, str) else admins_data
        except Exception:
            pass
    try:
        from helpers.context import get_bot_client
        client = get_bot_client()
        if client is None:
            return []
        count = await client.get_chat_members(chat_id)
        admins = []
        if isinstance(count, int):
            # Bot API has no full admin enumeration; fall back to rank map.
            pass
        await r.set(f"chat_admins:{chat_id}:{Dev_FINAL}", str(admins))
        await r.expire(f"chat_admins:{chat_id}:{Dev_FINAL}", 900)
        return admins
    except Exception:
        return []


async def reload_admins(chat_id: int) -> list[int]:
    return await get_admins(chat_id)


async def is_admin(chat_id: int, user_id: int) -> bool:
    return await admin_pls(user_id, chat_id)


async def is_admin_callback(query: CompatCallbackQuery) -> bool:
    if not query.from_user:
        return False
    user_id = query.from_user.id
    chat_id = query.message.chat.id
    if await is_sudoer(user_id):
        return True
    return await admin_pls(user_id, chat_id)


async def is_auth(chat_id: int, user_id: int) -> bool:
    """Kept for compatibility: authorized-user set is stored in Redis but is
    never the rank authority — admin_pls / parent ranks always take priority."""
    return await admin_pls(user_id, chat_id)


async def add_auth(chat_id: int, user_id: int) -> None:
    await r.sadd(f"auth_users:{chat_id}:{Dev_FINAL}", str(user_id))


async def rm_auth(chat_id: int, user_id: int) -> None:
    await r.srem(f"auth_users:{chat_id}:{Dev_FINAL}", str(user_id))


async def can_manage_vc_check(user_id: int, chat_id: int) -> bool:
    """Unified VC permission check — parent ranks are the only authority."""
    if await admin_pls(user_id, chat_id):
        return True
    if await is_sudoer(user_id):
        return True
    if await r.sismember(f"auth_users:{chat_id}:{Dev_FINAL}", str(user_id)):
        return True
    return False


def admin_check(func):
    @wraps(func)
    async def wrapper(_, update, *args, **kwargs):
        async def reply(text):
            if isinstance(update, CompatMessage):
                try:
                    return await update.reply_text(text)
                except Exception:
                    return
            else:
                try:
                    return await update.answer(text, show_alert=True)
                except Exception:
                    return
        if not update.from_user:
            return
        chat_id = update.chat.id if isinstance(update, CompatMessage) else update.message.chat.id
        user_id = update.from_user.id
        if await is_sudoer(user_id):
            return await func(_, update, *args, **kwargs)
        if await admin_pls(user_id, chat_id):
            return await func(_, update, *args, **kwargs)
        try:
            return await reply(update.lang["user_no_perms"])
        except Exception:
            return
    return wrapper


def can_manage_vc(func):
    @wraps(func)
    async def wrapper(_, update, *args, **kwargs):
        chat_id = update.chat.id if isinstance(update, CompatMessage) else update.message.chat.id
        if not update.from_user:
            return
        user_id = update.from_user.id
        if await can_manage_vc_check(user_id, chat_id):
            return await func(_, update, *args, **kwargs)
        if isinstance(update, CompatMessage):
            try:
                return await update.reply_text(update.lang["user_no_perms"])
            except Exception:
                return
        else:
            try:
                return await update.answer(update.lang["user_no_perms"], show_alert=True)
            except Exception:
                return
    return wrapper
