
import json

from aiogram.enums import ChatType

from compat import CompatMessage

from helpers.context import get_global_r, get_global_dev, get_global_k


async def get_channel_info(c, chat_id):
    try:
        chat = await c.get_chat(chat_id)
        channel_info = {
            'id': chat.id,
            'title': chat.title,
            'type': chat.type,
            'username': chat.username,
            'linked_chat_id': None,
            'is_channel': chat.type == ChatType.CHANNEL,
            'is_discussion_group': False
        }

        if hasattr(chat, 'linked_chat') and chat.linked_chat:
            channel_info['linked_chat_id'] = chat.linked_chat.id
            channel_info['is_discussion_group'] = True

        if chat.type == ChatType.SUPERGROUP and hasattr(chat, 'linked_chat') and chat.linked_chat:
            channel_info['linked_chat_id'] = chat.linked_chat.id

        return channel_info
    except Exception as e:
        return None


async def get_safe_sender(c, m: CompatMessage):
    if not m:
        return None

    r = get_global_r()
    Dev_FINAL = get_global_dev()

    if m.from_user:
        return {
            'id': m.from_user.id,
            'first_name': m.from_user.first_name or '',
            'last_name': m.from_user.last_name or '',
            'username': m.from_user.username or '',
            'is_bot': m.from_user.is_bot or False,
            'type': 'user',
            'chat_id': m.chat.id if m.chat else None,
            'is_virtual': False
        }

    if m.chat and m.chat.type == ChatType.CHANNEL:
        channel_disabled = await r.get(f'disable_channel_handling:{Dev_FINAL}')
        if channel_disabled:
            return None

        virtual_user_id = f"channel_{m.chat.id}"
        channel_info = await get_channel_info(c, m.chat.id)

        return {
            'id': virtual_user_id,
            'first_name': f"قناة {m.chat.title or 'غير معروفة'}",
            'last_name': '',
            'username': m.chat.username or '',
            'is_bot': False,
            'type': 'channel',
            'chat_id': m.chat.id,
            'channel_info': channel_info,
            'is_virtual': True
        }

    return {
        'id': f"service_{m.chat.id if m.chat else 'unknown'}",
        'first_name': 'خدمة النظام',
        'last_name': '',
        'username': '',
        'is_bot': True,
        'type': 'service',
        'chat_id': m.chat.id if m.chat else None,
        'is_virtual': True
    }


async def notify_dev_about_channel(c, channel_id, Dev_FINAL):
    r = get_global_r()
    k = get_global_k()

    try:
        channel_info = await get_channel_info(c, channel_id)
        if not channel_info:
            return

        dev_group = await r.get(f'DevGroup:{Dev_FINAL}')

        text = f'تم تفعيل البوت في قناة جديدة\n\n'
        text += f'اسم القناة: {channel_info["title"]}\n'
        text += f'ايدي القناة: {channel_info["id"]}\n'
        if channel_info["username"]:
            text += f'يوزر القناة: @{channel_info["username"]}\n'
        else:
            text += f'يوزر القناة: لا يوجد\n'

        if channel_info["linked_chat_id"]:
            try:
                linked_chat = await c.get_chat(channel_info["linked_chat_id"])
                text += f'\nمجموعة المناقشة: {linked_chat.title}\n'
                text += f'ايدي المجموعة: {linked_chat.id}\n'
                if linked_chat.username:
                    text += f'يوزر المجموعة: @{linked_chat.username}\n'
            except Exception:
                text += f'\nمجموعة المناقشة: غير متاحة\n'
        else:
            text += f'\nلا توجد مجموعة مناقشة مرتبطة بالقناة\n'

        if dev_group:
            try:
                await c.send_message(int(dev_group), text)
            except Exception:
                pass

        owner = await r.get(f'{Dev_FINAL}botowner')
        if owner:
            try:
                await c.send_message(int(owner), text)
            except Exception:
                pass

        await r.sadd(f'channel_list:{Dev_FINAL}', str(channel_id))

    except Exception as e:
        print(f"Error notifying dev about channel: {e}")


async def handle_channel_message(c, m: CompatMessage):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()

    if not m.chat or m.chat.type != ChatType.CHANNEL:
        return

    channel_disabled = await r.get(f'disable_channel_handling:{Dev_FINAL}')
    if channel_disabled:
        return

    channel_id = m.chat.id

    is_new_channel = not await r.sismember(f'channel_list:{Dev_FINAL}', str(channel_id))
    if is_new_channel:
        await notify_dev_about_channel(c, channel_id, Dev_FINAL)

    sender = await get_safe_sender(c, m)
    if not sender:
        return

    return sender


async def is_channel_disabled(Dev_FINAL):
    r = get_global_r()
    return await r.get(f'disable_channel_handling:{Dev_FINAL}')


async def set_channel_handling(Dev_FINAL, enabled: bool):
    r = get_global_r()
    if enabled:
        await r.delete(f'disable_channel_handling:{Dev_FINAL}')
        return True
    else:
        await r.set(f'disable_channel_handling:{Dev_FINAL}', '1')
        return False
