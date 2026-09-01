
from helpers.context import get_global_r, get_global_dev


async def init_channel_handling():
    r = get_global_r()
    Dev_FINAL = get_global_dev()

    if not await r.exists(f'disable_channel_handling:{Dev_FINAL}'):
        await r.set(f'disable_channel_handling:{Dev_FINAL}', '0')

    if not await r.exists(f'channel_list:{Dev_FINAL}'):
        await r.sadd(f'channel_list:{Dev_FINAL}', 'init')
        await r.srem(f'channel_list:{Dev_FINAL}', 'init')

    return True
