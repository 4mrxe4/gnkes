
import html
from compat import Client, filters
from compat import ChatMemberStatus
from compat import errors
from helpers.channel import handle_channel_message, get_channel_info
from helpers.context import get_global_r, get_global_dev, get_global_k

async def sync_rank(r, chat_id, uid, Dev_FINAL, level):
    if level == 'OWNER':
        await r.set(f'{chat_id}:rankGOWNER:{uid}{Dev_FINAL}', 1)
        await r.sadd(f'{chat_id}:listGOWNER:{Dev_FINAL}', uid)
    elif level == 'ADMIN':
        await r.set(f'{chat_id}:rankADMIN:{uid}{Dev_FINAL}', 1)
        await r.sadd(f'{chat_id}:listADMIN:{Dev_FINAL}', uid)

async def resolve_revealed_publisher(c, m, r, Dev_FINAL):
    channel_id = m.chat.id
    user_id = m.from_user.id

    cache_key = f'channel_rank_check:{channel_id}:{user_id}:{Dev_FINAL}'
    cached = await r.get(cache_key)
    if cached:
        return cached

    try:
        member = await c.get_chat_member(channel_id, user_id)
    except (errors.UserNotParticipant, errors.ChatAdminRequired, errors.RPCError):
        return None
    except Exception:
        return None

    if member.status == ChatMemberStatus.OWNER:
        role = 'OWNER'
        await r.sadd(f'{user_id}:groups', channel_id)
    elif member.status == ChatMemberStatus.ADMINISTRATOR:
        role = 'ADMIN'
    else:
        return None

    await sync_rank(r, channel_id, user_id, Dev_FINAL, role)
    await r.set(cache_key, role, ex=600)
    return role

async def build_anonymous_publisher(m, r, Dev_FINAL):
    channel_id = m.chat.id
    virtual_id = m.sender_chat.id

    await sync_rank(r, channel_id, virtual_id, Dev_FINAL, 'ADMIN')

    m.from_user = type('User', (object,), {
        'id': virtual_id,
        'username': m.sender_chat.username or "NoUsername",
        'first_name': m.sender_chat.title,
        'last_name': "",
        'mention': f"<a href='https://t.me/{m.sender_chat.username}'>{html.escape(str(m.sender_chat.title))}</a>" if m.sender_chat.username else html.escape(str(m.sender_chat.title))
    })()

@Client.on_message(filters.channel, group=1)
async def channel_message_handler(c, m):
    Dev_FINAL = get_global_dev()
    r = get_global_r()
    k = get_global_k()

    channel_disabled = await r.get(f'disable_channel_handling:{Dev_FINAL}')
    if channel_disabled == '1':
        return

    channel_id = m.chat.id
    if not await r.sismember(f'channel_list:{Dev_FINAL}', str(channel_id)):
        await r.sadd(f'channel_list:{Dev_FINAL}', str(channel_id))
        channel_info = await get_channel_info(c, channel_id)
        owner = await r.get(f'{Dev_FINAL}botowner')
        if owner:
            try: await c.send_message(int(owner), f'تم تفعيل البوت في قناة جديدة: {channel_info["title"] if channel_info else channel_id}')
            except: pass

    sender = await handle_channel_message(c, m)
    if not sender:
        return

    if m.from_user and not m.from_user.is_bot:
        role = await resolve_revealed_publisher(c, m, r, Dev_FINAL)
        m.sender_role = role or 'ADMIN'
        m.is_anonymous_channel_sender = False
    elif m.sender_chat:
        await build_anonymous_publisher(m, r, Dev_FINAL)
        m.sender_role = 'ADMIN'
        m.is_anonymous_channel_sender = True
    else:
        return

    if m.text:
        from plugins.devs import SudosCommandsFunc
        channel = await r.get(f'{Dev_FINAL}:BotChannel') or ''
        try:
            await SudosCommandsFunc(c, m, k, r, channel, Dev_FINAL)
        except Exception as e:
            print(f"Error in channel command handling: {e}")