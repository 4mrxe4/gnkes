# Plugins1/FinalMusic/fm_core/calls.py

from helpers.context import get_config, get_current_bot_id as _get_current_bot_id, set_current_bot_id as _set_current_bot_id, get_global_is_parent, redis_proxy as r, dev_final_proxy as Dev_FINAL, k_proxy as k
import asyncio
import logging
from ntgcalls import ConnectionNotFound, TelegramServerError
from pyrogram import enums, errors
from pyrogram.errors import MessageIdInvalid
from pyrogram.types import InputMediaPhoto, Message
from pytgcalls import PyTgCalls, exceptions, types
from pytgcalls.pytgcalls_session import PyTgCallsSession

from helpers.context import config_proxy as config

from ..fm_helpers import Media, Track, buttons, thumb
from plugins.FinalMusic.fm_core.lang import lang

FALLBACK_THUMB = "https://files.catbox.moe/8czm1s.png"
logger = logging.getLogger("FinalMusic")

class PyTgCallsErrorFilter(logging.Filter):
    def filter(self, record):
        if 'UpdateGroupCall' in record.getMessage():
            return False
        if 'Connection with chat id' in record.getMessage() and 'not found' in record.getMessage():
            return False
        return True

logging.getLogger('pyrogram.dispatcher').addFilter(PyTgCallsErrorFilter())

class TgCall(PyTgCalls):
    def __init__(self):
        self.clients = []
        self._play_next_locks = {}
        self._stream_end_cache = {}
        self._seeking = set()
    
    async def _edit_media_with_retry(self, message: Message, media_obj: InputMediaPhoto, reply_markup):
        if not media_obj:
            return None
        try:
            return await message.edit_media(media=media_obj, reply_markup=reply_markup)
        except errors.FloodWait as fw:
            await asyncio.sleep(fw.value + 1)
            try:
                return await message.edit_media(media=media_obj, reply_markup=reply_markup)
            except Exception:
                return None
        except errors.MessageNotModified:
            return None
        except Exception:
            return None
    
    async def _send_photo_with_retry(self, chat_id: int, photo, caption: str, reply_markup):
        if not photo:
            photo = FALLBACK_THUMB
        try:
            from plugins.FinalMusic import app
            return await app.send_photo(chat_id=chat_id, photo=photo, caption=caption, reply_markup=reply_markup)
        except errors.FloodWait as fw:
            await asyncio.sleep(fw.value + 1)
            try:
                from plugins.FinalMusic import app
                return await app.send_photo(chat_id=chat_id, photo=photo, caption=caption, reply_markup=reply_markup)
            except Exception as e:
                logger.error(f"_send_photo_with_retry: retry failed for {chat_id}: {e}")
                return None
        except Exception as e:
            logger.error(f"_send_photo_with_retry: failed for {chat_id}: {e}")
            return None
    
    async def get_assistant(self, chat_id: int):
        from plugins.FinalMusic import tune, userbot
        
        old_bot_id = _get_current_bot_id()
        is_parent = get_global_is_parent()
        
        try:
            if is_parent:
                bot_id = getattr(config, 'Dev_FINAL', None) or Dev_FINAL
                if bot_id and bot_id != 'unknown':
                    _set_current_bot_id(bot_id)
            
            if not userbot.clients:
                await userbot.boot()

            # الإصلاح: userbot.boot() يعبّئ فقط userbot.clients (عملاء pyrogram
            # الخام)، بينما التشغيل الفعلي يحتاج tune.clients/self.clients
            # (نفس العملاء لكن ملفوفين بـ PyTgCalls). بدون هذا الاستدعاء تبقى
            # هذه القائمة فاضية دائماً وتظهر "لا يوجد حساب مساعد متاح" حتى لو
            # الحساب المساعد اشتغل ونجح فعلاً.
            if not self.clients:
                await self.boot()

            assistant_num = await r.get(f"assistant:{chat_id}:{Dev_FINAL}")
            if assistant_num:
                if isinstance(assistant_num, bytes):
                    num = int(assistant_num.decode('utf-8'))
                else:
                    num = int(assistant_num)
            else:
                num = 1
                await r.set(f"assistant:{chat_id}:{Dev_FINAL}", str(num))
            
            if hasattr(tune, 'clients') and tune.clients:
                if num <= len(tune.clients):
                    return tune.clients[num - 1]
                return tune.clients[0] if tune.clients else None
            
            if hasattr(self, 'clients') and self.clients:
                if num <= len(self.clients):
                    return self.clients[num - 1]
                return self.clients[0] if self.clients else None
            
            return None
            
        finally:
            if old_bot_id:
                _set_current_bot_id(old_bot_id)
    
    async def pause(self, chat_id: int) -> bool:
        client = await self.get_assistant(chat_id)
        if not client:
            logger.error(f"No client available for {chat_id}")
            return False
        try:
            await client.pause(chat_id)
            await r.set(f"playing:{chat_id}:{Dev_FINAL}", "paused")
            return True
        except (ConnectionNotFound, exceptions.NotInCallError):
            await r.delete(f"playing:{chat_id}:{Dev_FINAL}")
            await r.delete(f"call_active:{chat_id}:{Dev_FINAL}")
            from plugins.FinalMusic import queue
            queue.clear(chat_id)
            logger.warning(f"Pause requested but assistant not in call for {chat_id}, syncing state")
            return False
        except Exception as e:
            logger.error(f"Pause failed for {chat_id}: {e}")
            return False
    
    async def resume(self, chat_id: int) -> bool:
        client = await self.get_assistant(chat_id)
        if not client:
            logger.error(f"No client available for {chat_id}")
            return False
        try:
            await client.resume(chat_id)
            await r.set(f"playing:{chat_id}:{Dev_FINAL}", "playing")
            return True
        except (ConnectionNotFound, exceptions.NotInCallError):
            await r.delete(f"playing:{chat_id}:{Dev_FINAL}")
            await r.delete(f"call_active:{chat_id}:{Dev_FINAL}")
            from plugins.FinalMusic import queue
            queue.clear(chat_id)
            logger.warning(f"Resume requested but assistant not in call for {chat_id}, syncing state")
            return False
        except Exception as e:
            logger.error(f"Resume failed for {chat_id}: {e}")
            return False
    
    async def stop(self, chat_id: int) -> None:
        client = await self.get_assistant(chat_id)
        from plugins.FinalMusic import preload
        try:
            await preload.cancel_preload(chat_id)
        except Exception as e:
            logger.debug(f"Error cancelling preload for {chat_id}: {e}")
        try:
            from plugins.FinalMusic import queue
            queue.clear(chat_id)
            await r.delete(f"call_active:{chat_id}:{Dev_FINAL}")
            await r.delete(f"playing:{chat_id}:{Dev_FINAL}")
            await r.delete(f"loop:{chat_id}:{Dev_FINAL}")
        except Exception as e:
            logger.warning(f"Error clearing queue/call for {chat_id}: {e}")
        if client:
            try:
                await client.leave_call(chat_id, close=False)
                await asyncio.sleep(0.5)
            except (ConnectionNotFound, exceptions.NotInCallError):
                pass
            except Exception as e:
                error_msg = str(e).lower()
                if not any(ignore in error_msg for ignore in ["not in a call", "not in the group call", "groupcall_forbidden", "no active group call", "call was already stopped", "call already disconnected"]):
                    logger.warning(f"Error leaving call for {chat_id}: {e}")
    
    async def get_call(self, chat_id: int) -> bool:
        return await r.get(f"call_active:{chat_id}:{Dev_FINAL}") is not None

    async def _get_bot_card_thumb(self, media) -> str:
        """صورة مصغرة لتشغيل الرد على ملف موجود (لا بيانات يوتيوب لها):
        نفس تصميم اللوحة لكن بصورة/يوزر/اسم البوت. تُبنى مرة واحدة لكل بوت
        وتُخزَّن، فلا حاجة لإعادة جلبها أو توليدها من الصفر في كل مرة."""
        from plugins.FinalMusic import app
        try:
            bot_id = _get_current_bot_id() or Dev_FINAL
            bot_user = getattr(app, "me", None) or await app.get_me()
            bot_name = (getattr(bot_user, "first_name", None) or getattr(bot_user, "username", None) or "Music Bot")
            bot_username = getattr(bot_user, "username", None)
            return await thumb.generate_bot_card(bot_id, bot_name, bot_username, media, app)
        except Exception as e:
            logger.warning(f"_get_bot_card_thumb failed: {e}")
            return FALLBACK_THUMB
    
    async def play_media(self, chat_id: int, message: Message | None, media: Media | Track, seek_time: int = 0, message_chat_id: int = None) -> None:
        from plugins.FinalMusic import app, queue
        _lang = await lang.get_lang(chat_id)
        client = await self.get_assistant(chat_id)
        if not client:
            if message:
                await message.edit_text(_lang.get("error_no_client", "لا يوجد حساب مساعد متاح. يرجى المحاولة مرة أخرى."))
            logger.error(f"No client available for {chat_id}")
            return
        target_chat_for_messages = message_chat_id if message_chat_id else chat_id
        thumb_gen = getattr(config, 'THUMB_GEN', True)
        if thumb_gen and isinstance(media, Track):
            _thumb = await thumb.generate(media)
        elif thumb_gen:
            _thumb = await self._get_bot_card_thumb(media)
        else:
            _thumb = getattr(config, 'DEFAULT_THUMB', FALLBACK_THUMB)
        if not _thumb:
            _thumb = FALLBACK_THUMB
            logger.warning(f"Using fallback thumbnail for {getattr(media, 'id', 'unknown')}")
        if not media.file_path and hasattr(media, "id") and media.id:
            try:
                cached = await r.get(f"audio_cache:{media.id}:{Dev_FINAL}")
                if cached:
                    import json
                    cached_data = json.loads(cached)
                    if cached_data.get("catbox_url"):
                        media.file_path = cached_data["catbox_url"]
            except Exception as e:
                logger.error(f"Error recovering path from cache: {e}")
        if not media.file_path:
            if message:
                support_chat = getattr(config, 'SUPPORT_CHAT', 'NwSupport')
                return await message.edit_text(_lang.get("error_no_file").format(support_chat))
            else:
                logger.error(f"No file path for media in {chat_id}")
                return
        
        try:
            chat = await app.get_chat(chat_id)
            # الإصلاح: chat.type هنا كائن من compat.ChatType (طبقة التوافق فوق
            # aiogram)، وليس pyrogram.enums.ChatType كما يفترض الكود الأصلي —
            # فالمقارنة بقيم pyrogram كانت تفشل دائماً حتى مع مجموعات سوبرقروب
            # حقيقية، فيظهر خطأ "يمكن التشغيل فقط في المجموعات والقنوات" دائماً.
            chat_type_value = str(getattr(chat.type, "value", chat.type)).lower()
            if chat_type_value not in ("supergroup", "group", "channel"):
                logger.error(f"Invalid chat type for {chat_id}: {chat.type}")
                if message:
                    await message.edit_text(_lang.get("error_chat_type", "يمكن التشغيل فقط في المجموعات والقنوات."))
                return

            userbot_client = await self.get_assistant(chat_id)
            if not userbot_client:
                logger.error(f"No userbot client available for {chat_id}")
                if message:
                    await message.edit_text(_lang.get("error_assistant_unavailable", "الحساب المساعد غير متوفر."))
                return

            need_join = False
            try:
                assistant_member = await app.get_chat_member(chat_id, userbot_client.app.me.id)
                if str(getattr(assistant_member.status, 'value', assistant_member.status)).lower() == 'kicked':
                    logger.error(f"Assistant banned in chat {chat_id}")
                    if message:
                        await message.edit_text(_lang.get("error_assistant_banned", "الحساب المساعد محظور في هذه المحادثة."))
                    if str(getattr(chat.type, 'value', chat.type)).lower() == 'channel':
                        await r.delete(f"cmode:{chat_id}:{Dev_FINAL}")
                    return
            except errors.RPCError as e:
                if any(err in str(e) for err in ["CHANNEL_INVALID", "USER_NOT_PARTICIPANT", "CHAT_ADMIN_REQUIRED", "PARTICIPANT_ID_INVALID"]):
                    need_join = True
                else:
                    raise

            if need_join:
                try:
                    invitelink = await app.export_chat_invite_link(chat_id)
                    await userbot_client.app.join_chat(invitelink)
                    logger.info(f"Assistant successfully auto-joined chat {chat_id} via invite link.")
                except errors.RPCError as join_err:
                    logger.error(f"Failed auto-joining assistant to {chat_id}: {join_err}")
                    assistant_username = userbot_client.app.me.username or f"ID: {userbot_client.app.me.id}"
                    if message:
                        await message.edit_text(
                            _lang.get(
                                "error_assistant_not_in_channel",
                                "ماقدرت اضيف الحساب المساعد تلقائيا يمكن قناتك خاصة\n"
                                "جرب انت تضيفه بشكل يدوي\nالحساب المساعد @{}"
                            ).format(assistant_username)
                        )
                    if str(getattr(chat.type, 'value', chat.type)).lower() == 'channel':
                        await r.delete(f"cmode:{chat_id}:{Dev_FINAL}")
                    return

        except errors.RPCError as e:
            if "CHANNEL_INVALID" in str(e):
                logger.error(f"Invalid channel {chat_id}: {e}")
                if message:
                    await message.edit_text(_lang.get("error_channel_invalid", "القناة غير صالحة. تم تعطيل التشغيل في القناة."))
                await r.delete(f"cmode:{chat_id}:{Dev_FINAL}")
                return
            raise

        is_http_stream = str(media.file_path).startswith("http://") or str(media.file_path).startswith("https://")
        if is_http_stream:
            if seek_time > 1:
                ffmpeg_params = f"-ss {seek_time} -reconnect 1 -reconnect_at_eof 1 -reconnect_streamed 1 -reconnect_delay_max 5 -probesize 10M -analyzeduration 5M -rtbufsize 5M -fflags +genpts+igndts"
            else:
                ffmpeg_params = "-reconnect 1 -reconnect_at_eof 1 -reconnect_streamed 1 -reconnect_delay_max 5 -probesize 10M -analyzeduration 5M -rtbufsize 5M -fflags +genpts+igndts -sync ext"
        else:
            if seek_time > 1:
                ffmpeg_params = f"-ss {seek_time} -probesize 10M -analyzeduration 5M -rtbufsize 5M -fflags +genpts+igndts"
            else:
                ffmpeg_params = "-probesize 10M -analyzeduration 5M -rtbufsize 5M -fflags +genpts+igndts -sync ext"
        is_video = getattr(media, "video", False)
        video_flags = types.MediaStream.Flags.AUTO_DETECT if is_video else types.MediaStream.Flags.IGNORE
        stream = types.MediaStream(
            media_path=media.file_path,
            audio_parameters=types.AudioQuality.STUDIO,
            audio_flags=types.MediaStream.Flags.REQUIRED,
            video_flags=video_flags,
            ffmpeg_parameters=ffmpeg_params,
        )
        try:
            call = await client.get_call(chat_id)
            if call:
                logger.debug(f"Already connected to {chat_id}, leaving before reconnecting...")
                await client.leave_call(chat_id, close=False)
        except (ConnectionNotFound, exceptions.NotInCallError):
            pass
        except Exception as e:
            logger.debug(f"Error checking connection state for {chat_id}: {e}")
        max_retries = 3
        retry_delay = 1
        try:
            for attempt in range(max_retries):
                try:
                    await client.play(chat_id=chat_id, stream=stream, config=types.GroupCallConfig(auto_start=True))
                    break
                except (exceptions.NoActiveGroupCall, errors.RPCError) as e:
                    error_msg = str(e)
                    if "GROUPCALL_INVALID" in error_msg or "GROUPCALL" in error_msg or isinstance(e, exceptions.NoActiveGroupCall):
                        if attempt < max_retries - 1:
                            logger.debug(f"Group call transitioning for {chat_id}, retrying in {retry_delay}s... (attempt {attempt + 1}/{max_retries})")
                            await asyncio.sleep(retry_delay)
                            continue
                        else:
                            raise
                    else:
                        raise
                except Exception as e:
                    error_msg = str(e).lower()
                    if "cannot be initialized more than once" in error_msg or "connection" in error_msg:
                        if attempt < max_retries - 1:
                            logger.debug(f"Connection error for {chat_id}, leaving and retrying... (attempt {attempt + 1}/{max_retries})")
                            try:
                                await client.leave_call(chat_id, close=False)
                                await asyncio.sleep(retry_delay)
                            except Exception:
                                pass
                            continue
                        else:
                            raise
                    else:
                        raise
            if seek_time:
                media.time = seek_time
            else:
                media.time = 1
            if not seek_time:
                await r.set(f"call_active:{chat_id}:{Dev_FINAL}", "1")
                await r.set(f"playing:{chat_id}:{Dev_FINAL}", "playing")
                text = _lang.get("play_media").format(
                    media.url,
                    media.title,
                    media.duration,
                    media.user,
                )
                if not media.is_live and media.duration_sec:
                    import time as time_module
                    played = media.time
                    duration = media.duration_sec
                    bar_length = 12
                    if duration == 0:
                        percentage = 0
                    else:
                        percentage = min((played / duration) * 100, 100)
                    filled = int(round(bar_length * percentage / 100))
                    timer_bar = "—" * filled + "●" + "—" * (bar_length - filled)
                    if duration >= 3600:
                        played_time = time_module.strftime('%H:%M:%S', time_module.gmtime(played))
                        total_time = time_module.strftime('%H:%M:%S', time_module.gmtime(duration))
                    else:
                        played_time = time_module.strftime('%M:%S', time_module.gmtime(played))
                        total_time = time_module.strftime('%M:%S', time_module.gmtime(duration))
                    timer_text = f"{played_time} {timer_bar} {total_time}"
                else:
                    timer_text = None
                if message:
                    try:
                        await message.delete()
                    except Exception:
                        pass
                sent_photo = await self._send_photo_with_retry(chat_id=target_chat_for_messages, photo=_thumb, caption=text, reply_markup=None)
                if sent_photo:
                    media.message_id = sent_photo.id
                    from plugins.FinalMusic import app
                    try:
                        if timer_text:
                            await buttons.edit_controls_markup(app, target_chat_for_messages, sent_photo.id, timer=timer_text)
                        else:
                            await buttons.edit_controls_markup(app, target_chat_for_messages, sent_photo.id)
                    except Exception as e:
                        logger.error(f"play_media: edit_controls_markup failed for {chat_id}: {e}")
                else:
                    logger.error(f"play_media: _send_photo_with_retry returned None for {chat_id} — no card/buttons sent at all")
                from plugins.FinalMusic import preload
                try:
                    asyncio.create_task(preload.start_preload(chat_id, count=2))
                except Exception as e:
                    logger.debug(f"Error starting preload for {chat_id}: {e}")
                
                async def _monitor_track_end(chat_id, media):
                    try:
                        from plugins.FinalMusic import queue
                        duration = getattr(media, "duration_sec", 0)
                        if duration and duration > 0:
                            await asyncio.sleep(duration + 5)
                            if await r.get(f"call_active:{chat_id}:{Dev_FINAL}"):
                                current_media = queue.get_current(chat_id)
                                if current_media and current_media.id == media.id:
                                    logger.info(f"Monitor: track {media.id} should have ended, forcing play_next for {chat_id}")
                                    next_media = queue.get_next(chat_id)
                                    if next_media:
                                        await self.play_next(chat_id)
                                    else:
                                        await self.stop(chat_id)
                    except Exception as e:
                        logger.warning(f"Monitor error for {chat_id}: {e}")
                
                asyncio.create_task(_monitor_track_end(chat_id, media))
                
        except FileNotFoundError:
            if message:
                support_chat = getattr(config, 'SUPPORT_CHAT', 'NwSupport')
                try:
                    await message.edit_text(_lang.get("error_no_file").format(support_chat))
                except Exception:
                    pass
            await self.play_next(chat_id)
        except exceptions.NoActiveGroupCall:
            await self.stop(chat_id)
            if message:
                try:
                    await message.edit_text(_lang.get("error_vc_disabled", "لا توجد محادثة صوتية نشطة. يرجى بدء المحادثة أولاً."))
                except Exception:
                    pass
        except errors.RPCError as e:
            error_str = str(e)
            if any(x in error_str for x in ["CHAT_ADMIN_REQUIRED", "phone.CreateGroupCall", "GROUPCALL_FORBIDDEN", "GROUPCALL_CREATE_FORBIDDEN", "VOICE_MESSAGES_FORBIDDEN"]):
                await self.stop(chat_id)
                if message:
                    try:
                        await message.edit_text(_lang.get("error_vc_permission", "لا توجد صلاحية لإنشاء محادثة صوتية."))
                    except Exception:
                        pass
            elif "GROUPCALL_INVALID" in error_str or "GROUPCALL" in error_str:
                await self.stop(chat_id)
                if message:
                    try:
                        await message.edit_text(_lang.get("error_vc_invalid", "المحادثة الصوتية غير صالحة. يرجى إعادة إنشائها."))
                    except Exception:
                        pass
            else:
                logger.error(f"RPC error in play_media for {chat_id}: {e}")
                await self.stop(chat_id)
        except exceptions.NoAudioSourceFound:
            if message:
                try:
                    await message.edit_text(_lang.get("error_no_audio", "لا يوجد مصدر صوتي. يرجى التحقق من الملف."))
                except Exception:
                    pass
            await self.play_next(chat_id)
        except (ConnectionNotFound, TelegramServerError):
            await self.stop(chat_id)
            if message:
                try:
                    await message.edit_text(_lang.get("error_tg_server", "خطأ في الاتصال بخوادم تليجرام. يرجى المحاولة مرة أخرى."))
                except Exception:
                    pass
        except TimeoutError as e:
            error_msg = str(e)
            logger.warning(f"Timeout joining voice chat {chat_id}: {error_msg}")
            await self.stop(chat_id)
            if message:
                try:
                    await message.edit_text(_lang.get("error_timeout", "انتهت مهلة الاتصال. يرجى التحقق من الشبكة والمحاولة مرة أخرى."))
                except Exception:
                    pass
            await asyncio.sleep(2)
            await self.play_next(chat_id)
        except Exception as e:
            logger.error(f"Unexpected error in play_media for {chat_id}: {e}", exc_info=True)
            await self.stop(chat_id)
            if message:
                try:
                    await message.edit_text(_lang.get("error_unexpected", "✗ خطأ أثناء التشغيل: {}").format(str(e)[:100]))
                except Exception:
                    pass

    
    async def replay(self, chat_id: int) -> None:
        from plugins.FinalMusic import app, queue
        _lang = await lang.get_lang(chat_id)
        try:
            if not await self.get_call(chat_id):
                return
            message_chat_id = None
            try:
                chat = await app.get_chat(chat_id)
                if str(getattr(chat.type, 'value', chat.type)).lower() == 'channel':
                    group_id = await r.get(f"cmode_group:{chat_id}:{Dev_FINAL}")
                    if group_id:
                        message_chat_id = int(group_id)
            except Exception:
                pass
            media = queue.get_current(chat_id)
            target_chat = message_chat_id if message_chat_id else chat_id
            msg = await app.send_message(chat_id=target_chat, text=_lang.get("play_again", "🔄 جاري إعادة التشغيل..."))
            await self.play_media(chat_id, msg, media, message_chat_id=message_chat_id)
        except Exception as e:
            logger.error(f"Error in replay for {chat_id}: {e}", exc_info=True)
    
    async def seek_stream(self, chat_id: int, seconds: int) -> bool:
        from plugins.FinalMusic import app, queue
        try:
            if not await self.get_call(chat_id):
                return False
            media = queue.get_current(chat_id)
            if not media or media.is_live:
                return False
            if not media.file_path:
                logger.warning(f"Seek stream failed for {chat_id}: no file path")
                return False
            message_chat_id = None
            try:
                chat = await app.get_chat(chat_id)
                if str(getattr(chat.type, 'value', chat.type)).lower() == 'channel':
                    group_id = await r.get(f"cmode_group:{chat_id}:{Dev_FINAL}")
                    if group_id:
                        message_chat_id = int(group_id)
            except Exception:
                pass
            media.time = seconds
            target_chat = message_chat_id if message_chat_id else chat_id
            # ===== الإصلاح الجذري =====
            # سابقاً كان هذا يستدعي play_media() الذي يعيد إنشاء التيار بالكامل
            # (leave_call ثم play) فيُصدر StreamEnded وهمياً من pytgcalls، فيظن
            # المعالج أن المقطع انتهى ويعيد إرسال بطاقة "بدأ البث" الكاملة
            # (الصورة + العنوان + المدة + الذوق) قبل سطر التقديم/التأخير.
            # الحل: تطبيق التقديم/التأخير مباشرة على التيار الحالي عبر
            # change_stream (أو play بدون leave) بنفس نقطة البداية الجديدة —
            # دون إرسال أي بطاقة، ودون إعادة تحميل، ودون إنشاء بث جديد.
            is_http_stream = str(media.file_path).startswith("http://") or str(media.file_path).startswith("https://")
            if is_http_stream:
                ffmpeg_params = f"-ss {seconds} -reconnect 1 -reconnect_at_eof 1 -reconnect_streamed 1 -reconnect_delay_max 5 -probesize 10M -analyzeduration 5M -rtbufsize 5M -fflags +genpts+igndts"
            else:
                ffmpeg_params = f"-ss {seconds} -probesize 10M -analyzeduration 5M -rtbufsize 5M -fflags +genpts+igndts"
            is_video = getattr(media, "video", False)
            video_flags = types.MediaStream.Flags.AUTO_DETECT if is_video else types.MediaStream.Flags.IGNORE
            stream = types.MediaStream(
                media_path=media.file_path,
                audio_parameters=types.AudioQuality.STUDIO,
                audio_flags=types.MediaStream.Flags.REQUIRED,
                video_flags=video_flags,
                ffmpeg_parameters=ffmpeg_params,
            )
            client = await self.get_assistant(chat_id)
            if not client:
                return False
            # حماية إضافية: تجاهل أي StreamEnded وهمي أثناء تبديل التيار
            self._seeking.add(chat_id)
            try:
                if hasattr(client, "change_stream"):
                    await client.change_stream(chat_id, stream)
                else:
                    await client.play(chat_id=chat_id, stream=stream, config=types.GroupCallConfig(auto_start=True))
            finally:
                async def _clear_seeking_flag():
                    await asyncio.sleep(10)
                    self._seeking.discard(chat_id)
                asyncio.create_task(_clear_seeking_flag())
            return True
        except Exception as e:
            logger.warning(f"Seek stream failed for {chat_id}: {e}")
            return False
    
    async def play_next(self, chat_id: int) -> None:
        from plugins.FinalMusic import app, queue, yt, preload
        _lang = await lang.get_lang(chat_id)
        if chat_id not in self._play_next_locks:
            self._play_next_locks[chat_id] = asyncio.Lock()
        lock = self._play_next_locks[chat_id]
        if lock.locked():
            logger.info(f"play_next already running for {chat_id}, skipping duplicate call")
            return
        async with lock:
            try:
                if not await self.get_call(chat_id):
                    return
                message_chat_id = None
                try:
                    chat = await app.get_chat(chat_id)
                    if str(getattr(chat.type, 'value', chat.type)).lower() == 'channel':
                        group_id = await r.get(f"cmode_group:{chat_id}:{Dev_FINAL}")
                        if group_id:
                            message_chat_id = int(group_id)
                except Exception:
                    pass
                target_chat = message_chat_id if message_chat_id else chat_id
                loop_mode = await r.get(f"loop:{chat_id}:{Dev_FINAL}")
                if loop_mode == "1":
                    media = queue.get_current(chat_id)
                    if media:
                        try:
                            msg = await app.send_message(chat_id=target_chat, text=_lang.get("play_again", "🔄 جاري إعادة التشغيل..."))
                            await self.play_media(chat_id, msg, media, message_chat_id=message_chat_id)
                        except errors.ChannelPrivate:
                            logger.warning(f"Bot removed from {chat_id}, cleaning up")
                            try:
                                await self.leave_call(chat_id)
                            except Exception:
                                pass
                            await r.delete(f"call_active:{chat_id}:{Dev_FINAL}")
                            await r.delete(f"playing:{chat_id}:{Dev_FINAL}")
                            await r.delete(f"loop:{chat_id}:{Dev_FINAL}")
                        return
                media = queue.get_next(chat_id)
                if not media and loop_mode == "10":
                    all_items = queue.get_all(chat_id)
                    if all_items:
                        first_track = all_items[0]
                        try:
                            msg = await app.send_message(chat_id=target_chat, text=_lang.get("play_loop_queue", "🔁 جاري تكرار قائمة التشغيل..."))
                            if not first_track.file_path and hasattr(first_track, "id") and first_track.id:
                                cached = await r.get(f"audio_cache:{first_track.id}:{Dev_FINAL}")
                                if cached:
                                    import json
                                    cached_data = json.loads(cached)
                                    if cached_data.get("catbox_url"):
                                        first_track.file_path = cached_data["catbox_url"]
                            if not first_track.file_path:
                                is_live = getattr(first_track, 'is_live', False)
                                first_track.file_path = await yt.download(first_track.id, is_live=is_live, video=getattr(first_track, 'video', False))
                            first_track.message_id = msg.id
                            await self.play_media(chat_id, msg, first_track, message_chat_id=message_chat_id)
                        except errors.ChannelPrivate:
                            logger.warning(f"Bot removed from {chat_id}, cleaning up")
                            await self.leave_call(chat_id)
                            await r.delete(f"call_active:{chat_id}:{Dev_FINAL}")
                            await r.delete(f"playing:{chat_id}:{Dev_FINAL}")
                            await r.delete(f"loop:{chat_id}:{Dev_FINAL}")
                        return
                try:
                    if media and media.message_id:
                        await app.delete_messages(chat_id=chat_id, message_ids=media.message_id, revoke=True)
                        media.message_id = 0
                except Exception as e:
                    logger.debug(f"Could not delete previous message in {chat_id}: {e}")
                if not media:
                    logger.info(f"No queued tracks left for {chat_id}, stopping and leaving the call.")
                    try:
                        await app.send_message(chat_id=chat_id, text=_lang.get("auto_end", "✅ اكتملت قائمة التشغيل. تم إنهاء البث تلقائياً."))
                    except Exception as e:
                        logger.debug(f"Could not send auto_end message in {chat_id}: {e}")
                    await self.stop(chat_id)
                    return
                msg = None
                if not media.file_path and hasattr(media, "id") and media.id:
                    cached = await r.get(f"audio_cache:{media.id}:{Dev_FINAL}")
                    if cached:
                        import json
                        cached_data = json.loads(cached)
                        if cached_data.get("catbox_url"):
                            media.file_path = cached_data["catbox_url"]
                if not media.file_path:
                    is_live = getattr(media, 'is_live', False)
                    media.file_path = await yt.download(media.id, is_live=is_live, video=getattr(media, 'video', False))
                    if not media.file_path:
                        await self.stop(chat_id)
                        return
                try:
                    msg = await app.send_message(chat_id=target_chat, text=_lang.get("play_next", "⏩ جاري تشغيل التالي..."))
                except errors.FloodWait as fw:
                    logger.warning(f"FloodWait in play_next for {chat_id}: skipping status message ({fw.value}s)")
                    msg = None
                except errors.ChannelPrivate:
                    logger.warning(f"Bot removed from {chat_id}, cleaning up")
                    await self.leave_call(chat_id)
                    await r.delete(f"call_active:{chat_id}:{Dev_FINAL}")
                    await r.delete(f"playing:{chat_id}:{Dev_FINAL}")
                    await r.delete(f"loop:{chat_id}:{Dev_FINAL}")
                    return
                except Exception as e:
                    logger.error(f"Failed to send play_next message for {chat_id}: {e}")
                    msg = None
                media.message_id = msg.id if msg else 0
                if msg:
                    await self.play_media(chat_id, msg, media, message_chat_id=message_chat_id)
                else:
                    logger.info(f"Playing next track for {chat_id} without message update")
                    await self.play_media(chat_id, None, media, message_chat_id=message_chat_id)
                try:
                    asyncio.create_task(preload.start_preload(chat_id, count=2))
                except Exception as e:
                    logger.debug(f"Error starting preload after play_next for {chat_id}: {e}")
            except Exception as e:
                logger.error(f"Error in play_next for {chat_id}: {e}", exc_info=True)
                try:
                    await self.stop(chat_id)
                except Exception:
                    pass
    
    async def ping(self) -> float:
        pings = [client.ping for client in self.clients]
        return round(sum(pings) / len(pings), 2)
    
    async def decorators(self, client: PyTgCalls) -> None:
        @client.on_update()
        async def update_handler(_, update: types.Update) -> None:
            if isinstance(update, types.StreamEnded):
                if update.stream_type == types.StreamEnded.Type.AUDIO:
                    from plugins.FinalMusic import queue
                    chat_id = update.chat_id
                    if chat_id in self._seeking:
                        logger.debug(f"Ignoring StreamEnded for {chat_id}: seek in progress")
                        return
                    current_time = asyncio.get_event_loop().time()
                    if chat_id in self._stream_end_cache:
                        if current_time - self._stream_end_cache[chat_id] < 0.5:
                            return
                    self._stream_end_cache[chat_id] = current_time
                    self._stream_end_cache = {cid: t for cid, t in self._stream_end_cache.items() if current_time - t < 5.0}
                    logger.info(f"StreamEnded event received for chat {chat_id}")
                    next_media = queue.get_next(chat_id)
                    if next_media:
                        await self.play_next(chat_id)
                    else:
                        logger.info(f"No next track for {chat_id}, stopping call immediately")
                        await self.stop(chat_id)
            elif isinstance(update, types.ChatUpdate):
                if update.status in [types.ChatUpdate.Status.KICKED, types.ChatUpdate.Status.LEFT_GROUP, types.ChatUpdate.Status.CLOSED_VOICE_CHAT]:
                    await self.stop(update.chat_id)
    
    async def boot(self) -> None:
        old_bot_id = _get_current_bot_id()
        is_parent = get_global_is_parent()
        
        try:
            if is_parent:
                bot_id = getattr(config, 'Dev_FINAL', None) or Dev_FINAL
                if bot_id and bot_id != 'unknown':
                    _set_current_bot_id(bot_id)
            
            PyTgCallsSession.notice_displayed = True
            from plugins.FinalMusic import userbot
            
            if hasattr(self, 'clients'):
                for client in self.clients:
                    try:
                        await client.stop()
                    except:
                        pass
                self.clients = []
            
            if not userbot.clients:
                await userbot.boot()
            
            for ub in userbot.clients:
                try:
                    client = PyTgCalls(ub, cache_duration=100)
                    client.app = ub
                    await client.start()
                    self.clients.append(client)
                    await self.decorators(client)
                except Exception as e:
                    logger.error(f"Failed to start PyTgCalls for assistant: {e}")
            
            from plugins.FinalMusic import tune
            tune.clients = self.clients
            logger.info("PyTgCalls client(s) started.")
            
        finally:
            if old_bot_id:
                _set_current_bot_id(old_bot_id)