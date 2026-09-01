# Plugins1/FinalMusic/fm_plugins/events/misc.py

from helpers.context import redis_proxy as r, dev_final_proxy as Dev_FINAL, k_proxy as k
from helpers.context import _bot_contexts, get_current_bot_id, set_current_bot_id
import asyncio
import time
from compat import Client, filters, types
from compat import StopPropagation
from compat import ChatType as enums
from plugins.FinalMusic import tune, app, config, logger, queue, tasks, userbot, yt
from plugins.FinalMusic.fm_helpers import buttons

@Client.on_message(filters.group & ~filters.bot, group=-1)
async def _maintenance_mode_check(_, m: types.Message):
    if not m.from_user or m.from_user.id in app.sudoers:
        return
    maintenance = await r.get(f"maintenance:{Dev_FINAL}")
    if maintenance:
        try:
            await m.reply_text("<blockquote><b>🔧 البوت في وضع الصيانة</b>\n\nيخضع البوت حالياً لأعمال صيانة جدولة.\nيرجى المحاولة مرة أخرى لاحقاً.</blockquote>")
        except:
            pass
        raise StopPropagation

@Client.on_message(filters.video_chat_started, group=19)
@Client.on_message(filters.video_chat_ended, group=20)
async def _watcher_vc(_, m: types.Message):
    await tune.stop(m.chat.id)

def _known_bot_ids():
    try:
        ids = [bid for bid in list(_bot_contexts.keys()) if bid]
    except Exception:
        ids = []
    if not ids:
        current = get_current_bot_id()
        ids = [current] if current else [None]
    return ids

async def auto_leave():
    while True:
        try:
            await asyncio.sleep(1800)
            outer_bot_id = get_current_bot_id()
            for bot_id in _known_bot_ids():
                if bot_id:
                    set_current_bot_id(bot_id)
                try:
                    for ub in userbot.clients:
                        left = 0
                        try:
                            async for dialog in ub.get_dialogs():
                                chat_id = dialog.chat.id
                                if left >= 20:
                                    break
                                try:
                                    logger_id = config.LOGGER_ID
                                except:
                                    logger_id = None
                                excluded = [logger_id] if logger_id else []
                                if chat_id in excluded:
                                    continue
                                if dialog.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
                                    if await r.get(f"call_active:{chat_id}:{Dev_FINAL}"):
                                        continue
                                    await ub.leave_chat(chat_id)
                                    left += 1
                                await asyncio.sleep(5)
                        except Exception as e:
                            logger.error(f"Auto-leave error: {e}")
                            continue
                except Exception as e:
                    logger.error(f"Auto-leave bot-loop error ({bot_id}): {e}")
                    continue
            if outer_bot_id:
                set_current_bot_id(outer_bot_id)
        except Exception as e:
            logger.error(f"Critical error in auto_leave task: {e}")
            await asyncio.sleep(60)
            continue

async def track_time():
    while True:
        try:
            await asyncio.sleep(1)
            outer_bot_id = get_current_bot_id()
            for bot_id in _known_bot_ids():
                if bot_id:
                    set_current_bot_id(bot_id)
                try:
                    active_calls = await r.keys(f"call_active:*:{Dev_FINAL}")
                    for key in active_calls:
                        try:
                            chat_id = int(key.split(":")[1])
                            media = queue.get_current(chat_id)
                            
                            if not media:
                                next_media = queue.get_next(chat_id)
                                if not next_media:
                                    if await r.get(f"call_active:{chat_id}:{Dev_FINAL}"):
                                        await tune.stop(chat_id)
                                continue
                            
                            playing_status = await r.get(f"playing:{chat_id}:{Dev_FINAL}")
                            
                            if playing_status and playing_status == "paused":
                                continue
                            
                            media.time += 1
                            
                            if not getattr(media, "is_live", False) and media.duration_sec and media.time >= media.duration_sec + 3:
                                next_media = queue.get_next(chat_id)
                                if next_media:
                                    asyncio.create_task(tune.play_next(chat_id))
                                else:
                                    await tune.stop(chat_id)
                        except Exception as e:
                            continue
                except Exception as e:
                    continue
            if outer_bot_id:
                set_current_bot_id(outer_bot_id)
        except Exception as e:
            logger.error(f"Critical error in track_time task: {e}")
            await asyncio.sleep(1)
            continue

async def update_timer(length=10):
    chat_tasks = {}
    async def _preload_next(chat_id, next_media):
        try:
            next_media.file_path = await yt.download(next_media.id, video=getattr(next_media, "video", False))
        except:
            pass
    async def update_chat_timer(chat_id, bot_id):
        UPDATE_INTERVAL = 30
        first_tick = True
        last_message_id = None
        last_update_time = 0.0
        remove_sent = False
        while True:
            try:
                await asyncio.sleep(3 if first_tick else 1)
                first_tick = False
                if bot_id:
                    set_current_bot_id(bot_id)
                playing_status = await r.get(f"playing:{chat_id}:{Dev_FINAL}")
                if not playing_status or playing_status == "paused":
                    break
                media = queue.get_current(chat_id)
                if not media:
                    break
                if not hasattr(media, 'time') or media.time is None:
                    media.time = 0
                duration, message_id = media.duration_sec, media.message_id
                if not duration or not message_id:
                    continue
                if message_id != last_message_id:
                    last_message_id = message_id
                    last_update_time = 0.0
                    remove_sent = False
                message_chat_id = chat_id
                try:
                    chat = await app.get_chat(chat_id)
                    if chat.type == enums.ChatType.CHANNEL:
                        group_id = await r.get(f"cmode_group:{chat_id}:{Dev_FINAL}")
                        if group_id:
                            message_chat_id = int(group_id)
                except:
                    pass
                played = media.time
                remaining = duration - played
                bar_length = 12
                if duration == 0:
                    percentage = 0
                else:
                    percentage = min((played / duration) * 100, 100)
                filled = int(round(bar_length * percentage / 100))
                timer_bar = "—" * filled + "●" + "—" * (bar_length - filled)
                if remaining <= 30:
                    next = queue.get_next(chat_id, check=True)
                    if next and not next.file_path:
                        asyncio.create_task(_preload_next(chat_id, next))
                near_end = remaining < 10
                now = time.monotonic()
                if near_end:
                    if remove_sent:
                        continue
                elif (now - last_update_time) < UPDATE_INTERVAL:
                    continue
                last_update_time = now
                if near_end:
                    remove = True
                    remove_sent = True
                    timer_text = timer_bar
                else:
                    remove = False
                    if duration >= 3600:
                        played_time = time.strftime('%H:%M:%S', time.gmtime(played))
                        total_time = time.strftime('%H:%M:%S', time.gmtime(duration))
                    else:
                        played_time = time.strftime('%M:%S', time.gmtime(played))
                        total_time = time.strftime('%M:%S', time.gmtime(duration))
                    timer_text = f"{played_time} {timer_bar} {total_time}"
                try:
                    target_chat_id = message_chat_id if message_chat_id != chat_id else chat_id
                    resp = await buttons.edit_controls_markup(app, target_chat_id, message_id, timer=timer_text, remove=remove)
                    if not resp or not resp.get("ok"):
                        raise Exception(resp.get("description", "edit_controls_markup failed") if resp else "edit_controls_markup failed")
                except Exception as e:
                    error_str = str(e)
                    if not any(err in error_str for err in ["MESSAGE_NOT_MODIFIED", "MESSAGE_ID_INVALID", "MESSAGE_DELETE", "MESSAGE_AUTHOR_REQUIRED", "CHAT_ADMIN_REQUIRED", "CHANNEL_PRIVATE"]):
                        logger.warning(f"update_timer error for chat {chat_id}: {e}")
                    if "CHANNEL_PRIVATE" in error_str or "MESSAGE_ID_INVALID" in error_str:
                        break
                    await asyncio.sleep(1)
            except Exception as e:
                error_str = str(e)
                if not any(err in error_str for err in ["MESSAGE_NOT_MODIFIED", "MESSAGE_ID_INVALID", "MESSAGE_DELETE", "MESSAGE_AUTHOR_REQUIRED", "CHAT_ADMIN_REQUIRED", "CHANNEL_PRIVATE"]):
                    logger.warning(f"update_timer error for chat {chat_id}: {e}")
                if "CHANNEL_PRIVATE" in error_str or "MESSAGE_ID_INVALID" in error_str:
                    break
                await asyncio.sleep(1)
    while True:
        await asyncio.sleep(2)
        outer_bot_id = get_current_bot_id()
        for bot_id in _known_bot_ids():
            if bot_id:
                set_current_bot_id(bot_id)
            try:
                active_calls = await r.keys(f"call_active:*:{Dev_FINAL}")
                for key in active_calls:
                    try:
                        chat_id = int(key.split(":")[1])
                    except:
                        continue
                    if chat_id not in chat_tasks:
                        task = asyncio.create_task(update_chat_timer(chat_id, bot_id))
                        chat_tasks[chat_id] = task
            except Exception as e:
                logger.warning(f"update_timer scan error ({bot_id}): {e}")
                continue
        if outer_bot_id:
            set_current_bot_id(outer_bot_id)
        finished_chats = [cid for cid, task in chat_tasks.items() if task.done()]
        for chat_id in finished_chats:
            chat_tasks.pop(chat_id, None)

async def vc_watcher(sleep=10):
    alone_times = {}
    LEAVE_TIMEOUT = 40
    while True:
        await asyncio.sleep(sleep)
        current_time = time.time()
        outer_bot_id = get_current_bot_id()
        for bot_id in _known_bot_ids():
            if bot_id:
                set_current_bot_id(bot_id)
            try:
                active_calls = await r.keys(f"call_active:*:{Dev_FINAL}")
            except Exception as e:
                logger.warning(f"vc_watcher scan error ({bot_id}): {e}")
                continue
            for key in active_calls:
                try:
                    chat_id = int(key.split(":")[1])
                except:
                    continue
                try:
                    current_media = queue.get_current(chat_id)
                    if not current_media:
                        alone_times.pop(chat_id, None)
                        continue
                    call_client = await tune.get_assistant(chat_id)
                    if not call_client:
                        alone_times.pop(chat_id, None)
                        continue
                    try:
                        participants = await call_client.get_participants(chat_id)
                    except Exception as e:
                        logger.warning(f"vc_watcher: get_participants failed for {chat_id}, keeping alone-timer state: {e}")
                        continue
                    if len(participants) < 2:
                        if chat_id not in alone_times:
                            alone_times[chat_id] = current_time
                        else:
                            alone_duration = current_time - alone_times[chat_id]
                            if alone_duration >= LEAVE_TIMEOUT:
                                alone_times.pop(chat_id, None)
                                try:
                                    if current_media.message_id:
                                        await buttons.edit_controls_markup(app, chat_id, current_media.message_id, status="متوقف", remove=True)
                                except Exception:
                                    pass
                                try:
                                    await tune.stop(chat_id)
                                except Exception as e:
                                    logger.warning(f"vc_watcher: failed to stop/leave {chat_id}: {e}")
                                try:
                                    await app.send_message(chat_id=chat_id, text="مافي احد يستمع طفشت ونزلت")
                                except Exception:
                                    pass
                    else:
                        alone_times.pop(chat_id, None)
                except Exception as e:
                    logger.warning(f"vc_watcher error for {chat_id}: {e}")
                    alone_times.pop(chat_id, None)
                    continue
        if outer_bot_id:
            set_current_bot_id(outer_bot_id)

tasks.append(asyncio.create_task(vc_watcher()))
tasks.append(asyncio.create_task(auto_leave()))
tasks.append(asyncio.create_task(track_time()))
tasks.append(asyncio.create_task(update_timer()))