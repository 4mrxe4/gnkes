# play.py

import os
import sqlite3
import asyncio
import logging
import time
from compat import Client, filters
from compat import Message
from compat import FloodWait
from pyrogram.raw import functions as raw_functions, types as raw_types
from plugins.FinalMusic import tune, config, queue, tg, yt
from plugins.FinalMusic.fm_helpers import buttons, utils
from plugins.FinalMusic.fm_helpers._play import checkUB
from helpers.ranks import *
from plugins.FinalMusic.fm_core.lang import lang
from helpers.context import get_current_bot_id, set_current_bot_id, update_global_context, get_global_k, redis_proxy as r, dev_final_proxy as Dev_FINAL, k_proxy as k

logger = logging.getLogger(__name__)

_bot_id_getter = get_current_bot_id

async def _fetch_group_call_participants(pyro_client, chat_id: int):
    peer = await pyro_client.resolve_peer(chat_id)
    call = None
    if isinstance(peer, raw_types.InputPeerChannel):
        full = await pyro_client.invoke(raw_functions.channels.GetFullChannel(
            channel=raw_types.InputChannel(channel_id=peer.channel_id, access_hash=peer.access_hash)
        ))
        call = full.full_chat.call
    elif isinstance(peer, raw_types.InputPeerChat):
        full = await pyro_client.invoke(raw_functions.messages.GetFullChat(chat_id=peer.chat_id))
        call = full.full_chat.call
    else:
        return None
    if not call:
        return None
    input_call = raw_types.InputGroupCall(id=call.id, access_hash=call.access_hash)
    result = await pyro_client.invoke(raw_functions.phone.GetGroupParticipants(
        call=input_call, ids=[], sources=[], offset="", limit=100
    ))
    return [p for p in result.participants if not getattr(p, "left", False)]

async def is_music_enabled(chat_id: int) -> bool:
    if await r.get(f'{chat_id}:disableMusic:{Dev_FINAL}'):
        return False
    if await r.get(f':disableMusic:{Dev_FINAL}'):
        return False
    return True

async def can_play_music(chat_id: int, user_id: int) -> bool:
    restriction = await r.get(f'{chat_id}:music_restriction:{Dev_FINAL}') or ""
    if restriction == "admin":
        return await admin_pls(user_id, chat_id)
    elif restriction == "vip":
        return await pre_pls(user_id, chat_id)
    else:
        return await is_music_enabled(chat_id)

async def safe_edit(message, text, **kwargs):
    try:
        await message.edit_text(text, **kwargs)
        return True
    except FloodWait as e:
        await asyncio.sleep(e.value)
        try:
            await message.edit_text(text, **kwargs)
            return True
        except:
            return False
    except:
        return False

async def safe_reply(message, text, **kwargs):
    try:
        return await message.reply_text(text, **kwargs)
    except:
        return None

def playlist_to_queue(chat_id: int, tracks: list) -> str:
    text = "<blockquote expandable>"
    for track in tracks:
        pos = queue.add(chat_id, track)
        text += f"<b>{pos}.</b> {track.title}\n"
    text = text[:1948] + "</blockquote>"
    return text

async def get_assistant(chat_id: int):
    from plugins.FinalMusic import tune, userbot
    assistant_num = await r.get(f"assistant:{chat_id}:{Dev_FINAL}")
    if assistant_num:
        num = int(assistant_num)
    else:
        num = 1
        await r.set(f"assistant:{chat_id}:{Dev_FINAL}", str(num))
    clients = {1: userbot.one, 2: userbot.two, 3: userbot.three}
    return clients.get(num)

async def get_cmode_channel(chat_id: int):
    cmode = await r.get(f"cmode:{chat_id}:{Dev_FINAL}")
    if cmode:
        return int(cmode)
    return None

async def set_cmode(chat_id: int, channel_id: int = None):
    if channel_id is None:
        await r.delete(f"cmode:{chat_id}:{Dev_FINAL}")
        await r.delete(f"cmode_group:{chat_id}:{Dev_FINAL}")
    else:
        await r.set(f"cmode:{chat_id}:{Dev_FINAL}", str(channel_id))
        await r.set(f"cmode_group:{chat_id}:{Dev_FINAL}", str(chat_id))

@Client.on_message(filters.group & ~filters.bot, group=520)
async def music_toggle_handler(client, m: Message):
    old_bot_id = _bot_id_getter()
    try:
        bot_id = getattr(client, 'bot_id', None) or getattr(client, 'dev_final', None)
        if bot_id:
            set_current_bot_id(bot_id)
        if not m.text:
            return
        if not m.from_user:
            return
        if hasattr(m.from_user, 'is_bot') and m.from_user.is_bot:
            return
        if not await check_global_restrictions(client, m, get_global_k()):
            return
            return
        if await r.get(f'{m.from_user.id}:mute:{m.chat.id}{Dev_FINAL}'):
            return
        if await r.get(f'{m.from_user.id}:mute:{Dev_FINAL}'):
            return
        if await r.get(f'{m.chat.id}:mute:{Dev_FINAL}') and not await admin_pls(m.from_user.id, m.chat.id):
            return
        if await r.get(f'{m.from_user.id}:gban:{Dev_FINAL}'):
            try:
                await m.chat.ban_member(m.from_user.id)
            except:
                pass
            return
        _lang = await lang.get_lang(m.chat.id)
        k = await r.get(f'{get_current_bot_id() or Dev_FINAL}:botkey')
        name = await r.get(f'{Dev_FINAL}:BotName')
        text = m.text
        if name and text.startswith(f'{name} '):
            text = text.replace(f'{name} ', '')
        if text == "تفعيل الميوزك":
            if not await admin_pls(m.from_user.id, m.chat.id):
                return await m.reply(f"• عذراً الامر لـ Admin فقط")
            await r.delete(f'{m.chat.id}:disableMusic:{Dev_FINAL}')
            await r.delete(f'{m.chat.id}:music_restriction:{Dev_FINAL}')
            return await m.reply(f"• تم تفعيل تشغيل الموسيقى للجميع")
        if text == "تعطيل الميوزك":
            if not await admin_pls(m.from_user.id, m.chat.id):
                return await m.reply(f"• عذراً الامر لـ Admin فقط")
            await r.set(f'{m.chat.id}:disableMusic:{Dev_FINAL}', 'True')
            await r.delete(f'{m.chat.id}:music_restriction:{Dev_FINAL}')
            return await m.reply(f"• تم تعطيل تشغيل الموسيقى عن المجموعة")
        if text == "تفعيل ميوزك المميزين":
            if not await admin_pls(m.from_user.id, m.chat.id):
                return await m.reply(f"• عذراً الامر لـ Admin فقط")
            await r.delete(f'{m.chat.id}:disableMusic:{Dev_FINAL}')
            await r.set(f'{m.chat.id}:music_restriction:{Dev_FINAL}', 'vip')
            return await m.reply(f"• تم تقييد التشغيل للمميزين فما فوق")
        if text == "تعطيل ميوزك المميزين":
            if not await admin_pls(m.from_user.id, m.chat.id):
                return await m.reply(f"• عذراً الامر لـ Admin فقط")
            await r.delete(f'{m.chat.id}:music_restriction:{Dev_FINAL}')
            return await m.reply(f"• تم إلغاء تقييد المميزين")
        if text == "تفعيل ميوزك الادمن":
            if not await admin_pls(m.from_user.id, m.chat.id):
                return await m.reply(f"• عذراً الامر لـ Admin فقط")
            await r.delete(f'{m.chat.id}:disableMusic:{Dev_FINAL}')
            await r.set(f'{m.chat.id}:music_restriction:{Dev_FINAL}', 'admin')
            return await m.reply(f"• تم تقييد التشغيل للادمن والمشرفين فقط")
        if text == "تعطيل ميوزك الادمن":
            if not await admin_pls(m.from_user.id, m.chat.id):
                return await m.reply(f"• عذراً الامر لـ Admin فقط")
            await r.delete(f'{m.chat.id}:music_restriction:{Dev_FINAL}')
            return await m.reply(f"• تم إلغاء تقييد الادمن")
    finally:
        if old_bot_id:
            set_current_bot_id(old_bot_id)

@Client.on_message(filters.group & ~filters.bot, group=522)
async def who_in_call_handler(client, m: Message):
    old_bot_id = _bot_id_getter()
    try:
        bot_id = getattr(client, 'bot_id', None) or getattr(client, 'dev_final', None)
        if bot_id:
            set_current_bot_id(bot_id)
        if not m.text:
            return
        if not m.from_user:
            return
        if m.from_user.is_bot:
            return
        if not await check_global_restrictions(client, m, k):
            return
            return
        name = await r.get(f'{Dev_FINAL}:BotName')
        text = m.text
        if name and text.startswith(f'{name} '):
            text = text.replace(f'{name} ', '')
        if text != "مين في الكول":
            return
        chat_id = m.chat.id
        pyro_client = None
        try:
            assistant_client = await tune.get_assistant(chat_id)
            if assistant_client and getattr(assistant_client, "app", None):
                pyro_client = assistant_client.app
        except Exception:
            pyro_client = None
        if not pyro_client:
            pyro_client = client
        try:
            participants = await _fetch_group_call_participants(pyro_client, chat_id)
        except Exception as e:
            logger.warning(f"who_in_call: failed to fetch participants for {chat_id}: {e}")
            return await safe_reply(m, "• الكول مغلق يالطيب")
        if participants is None:
            return await safe_reply(m, "• الكول مغلق يالطيب")
        my_id = None
        try:
            my_id = pyro_client.me.id
        except Exception:
            pass
        entries = []
        seen = set()
        for p in participants:
            peer = getattr(p, "peer", None)
            uid = getattr(peer, "user_id", None) if peer else None
            if not uid or uid == my_id or uid in seen:
                continue
            seen.add(uid)
            entries.append((uid, bool(getattr(p, "muted", False))))
        if not entries:
            return await safe_reply(m, "• مافي حد في الكول")
        lines = ["• الموجودين الحين في الكول هم", ""]
        for uid, muted in entries:
            mention_name = "مستخدم"
            try:
                user = await client.get_users(uid)
                mention_name = user.first_name or mention_name
            except Exception:
                pass
            icon = "🔇" if muted else "🔊"
            lines.append(f'• <a href="tg://user?id={uid}">{mention_name}</a> ({icon})')
        await safe_reply(m, "\n".join(lines))
    finally:
        if old_bot_id:
            set_current_bot_id(old_bot_id)

# دالة مساعدة لتحميل الملف من قناة الأرشفة باستخدام Aiogram
async def download_from_archive(client, archive_msg, local_target_path: str) -> str:
    """تحميل الملف من قناة الأرشفة باستخدام Aiogram"""
    try:
        # محاولة استخراج file_id من أي نوع من الميديا
        file_id = None
        if hasattr(archive_msg, 'audio') and archive_msg.audio:
            file_id = archive_msg.audio.file_id
            print(f"[play] Found audio file_id: {file_id[:20]}...")
        elif hasattr(archive_msg, 'voice') and archive_msg.voice:
            file_id = archive_msg.voice.file_id
            print(f"[play] Found voice file_id: {file_id[:20]}...")
        elif hasattr(archive_msg, 'document') and archive_msg.document:
            file_id = archive_msg.document.file_id
            print(f"[play] Found document file_id: {file_id[:20]}...")
        elif hasattr(archive_msg, 'video') and archive_msg.video:
            file_id = archive_msg.video.file_id
            print(f"[play] Found video file_id: {file_id[:20]}...")
        elif hasattr(archive_msg, 'video_note') and archive_msg.video_note:
            file_id = archive_msg.video_note.file_id
            print(f"[play] Found video_note file_id: {file_id[:20]}...")
        
        if file_id:
            # download_file (وليست معرّفة على CompatClient) كانت تتسرب عبر
            # __getattr__ مباشرة لـ aiogram Bot.download_file الخام، والذي
            # يتوقع file_path من جهة تيليجرام (عبر get_file) وليس file_id —
            # فيفشل التنزيل. download_media هي الدالة الصحيحة هنا (تتعامل
            # مع file_id مباشرة، وهي نفسها التي أصلحت مشكلة "file can only
            # be of the string or Downloadable type" بالأعلى في compat.py).
            return await client.download_media(file_id, file_name=local_target_path)
        else:
            print("[play] No file_id found in message")
            return None
    except Exception as e:
        print(f"[play] Error in download_from_archive: {e}")
        return None

@Client.on_message(filters.group & ~filters.bot, group=521)
async def play_handler(client, m: Message):
    old_bot_id = _bot_id_getter()
    try:
        bot_id = getattr(client, 'bot_id', None) or getattr(client, 'dev_final', None)
        if bot_id:
            set_current_bot_id(bot_id)
        await update_global_context()
        if not m.text:
            return
        if not m.from_user:
            return
        if hasattr(m.from_user, 'is_bot') and m.from_user.is_bot:
            return
        if not await check_global_restrictions(client, m, get_global_k()):
            return
            return
        if await r.get(f'{m.from_user.id}:mute:{m.chat.id}{Dev_FINAL}'):
            return
        if await r.get(f'{m.from_user.id}:mute:{Dev_FINAL}'):
            return
        if await r.get(f'{m.chat.id}:mute:{Dev_FINAL}') and not await admin_pls(m.from_user.id, m.chat.id):
            return
        if await r.get(f'{m.from_user.id}:gban:{Dev_FINAL}'):
            try:
                await m.chat.ban_member(m.from_user.id)
            except:
                pass
            return
        _lang = await lang.get_lang(m.chat.id)
        k = await r.get(f'{get_current_bot_id() or Dev_FINAL}:botkey')
        name = await r.get(f'{Dev_FINAL}:BotName')
        text = m.text
        if name and text.startswith(f'{name} '):
            text = text.replace(f'{name} ', '')
        commands = ["شغل", "تشغيل", "فيديو", "vplay"]
        if not any(text == cmd or text.startswith(cmd + " ") for cmd in commands):
            return
        if not await can_play_music(m.chat.id, m.from_user.id):
            restriction = await r.get(f'{m.chat.id}:music_restriction:{Dev_FINAL}') or ""
            if restriction == "admin":
                return await m.reply(f"• عذراً تشغيل الموسيقى مقيد للأدمن والمشرفين فقط")
            elif restriction == "vip":
                return await m.reply(f"• عذراً تشغيل الموسيقى متاح للمميزين فقط")
            else:
                return await m.reply(f"• تشغيل الموسيقى معطل في هذه المجموعة")
        force = False
        url = None
        cplay = False
        video = False
        cmd = text.split()[0] if text.split() else ""
        if cmd in ["فيديو", "vplay"]:
            video = True
        chat_id = m.chat.id
        message_chat_id = m.chat.id
        if cmd == "شغل":
            cplay = True
        if cplay:
            channel_id = await get_cmode_channel(m.chat.id)
            if channel_id is None:
                return await m.reply(f"• وضع تشغيل القنوات غير مفعل")
            try:
                chat = await client.get_chat(channel_id)
                chat_id = channel_id
            except:
                await set_cmode(m.chat.id, None)
                return await m.reply(f"• فشل في جلب القناة")
            assistant_client = await get_assistant(channel_id)
            try:
                await client.get_chat_member(channel_id, assistant_client.id)
            except:
                try:
                    if chat.username:
                        invite_link = chat.username
                    else:
                        try:
                            invite_link = chat.invite_link
                            if not invite_link:
                                invite_link = await client.export_chat_invite_link(channel_id)
                        except:
                            return await m.reply(f"• الحساب المساعد ليس في القناة")
                    await assistant_client.join_chat(invite_link)
                    await asyncio.sleep(1)
                except:
                    return await m.reply(f"• فشل انضمام الحساب المساعد للقناة")
        try:
            await m.reply()
        except:
            pass
        sent = await safe_reply(m, f"🎶")
        if not sent:
            return
        mention = m.from_user.mention
        media = tg.get_media(m.reply_to_message) if m.reply_to_message else None
        tracks = []
        file = None
        is_reply_file = False
        if media:
            file = await tg.download(m.reply_to_message, sent)
            is_reply_file = True
            print(f"[play] Media from reply, file: {file}")
        else:
            query = text.split(" ", 1)[1] if len(text.split()) > 1 else ""
            if not query and not media:
                return await safe_edit(sent, f"• يرجى إرسال رابط أو اسم الأغنية")
            if query and "playlist" in query:
                try:
                    tracks = await yt.playlist(config.PLAYLIST_LIMIT, mention, query)
                except:
                    return await safe_edit(sent, f"• فشل في جلب قائمة التشغيل")
                if not tracks:
                    return await safe_edit(sent, f"• لا توجد مقاطع في القائمة")
                file = tracks[0]
                tracks.remove(file)
                file.message_id = sent.id
            else:
                set_current_bot_id(bot_id)
                await update_global_context()
                print(f"[play] Searching for: {query}")
                file = await yt.search(query, sent.id)
                if not file:
                    print("[play] Search returned None")
                    return await safe_edit(sent, _lang.get("play_not_found", "لم يتم العثور على المقطع"))
                print(f"[play] Search result: {file.title} (ID: {file.id})")
        if not file:
            return
        file.video = getattr(file, "video", False) or video
        if file.video:
            for track in tracks:
                track.video = True
        duration_sec = getattr(file, "duration_sec", 0)
        try:
            duration_sec = int(duration_sec)
        except:
            duration_sec = 0
        archive_channel_id = getattr(config, "ARCHIVE_CHANNEL", None)
        local_target_path = f"downloads/{file.id}.mp3"
        cached_data = None
        downloaded_from_cache = False

        # التحقق من الكاش باستخدام Aiogram
        if not is_reply_file:
            print(f"[play] Checking cache for: {file.id}")
            cached_data = await yt.get_cached_track(file.id)
            print(f"[play] Cached data: {cached_data}")
            
            if cached_data and cached_data.get("msg_id"):
                msg_id = cached_data.get("msg_id")
                print(f"[play] Track found in L2 cache with msg_id: {msg_id}")
                try:
                    # استخدام معرف القناة
                    target_chat = archive_channel_id
                    
                    # جلب الرسالة من القناة باستخدام Aiogram
                    archive_msg = await client.get_messages(target_chat, int(msg_id))
                    
                    if archive_msg:
                        # استخدام دالة التحميل المخصصة لـ Aiogram
                        file.file_path = await download_from_archive(client, archive_msg, local_target_path)
                        
                        if file.file_path and os.path.exists(file.file_path):
                            downloaded_from_cache = True
                            cached_data = True
                            print(f"[play] ✅ Downloaded from L2 cache: {file.file_path} ({os.path.getsize(file.file_path)} bytes)")
                        else:
                            await yt.mark_track_as_broken(file.id)
                            cached_data = None
                            print("[play] ❌ Failed to download from L2 cache, marking broken")
                    else:
                        await yt.mark_track_as_broken(file.id)
                        cached_data = None
                        print(f"[play] ❌ No message found with msg_id: {msg_id}")
                except Exception as e:
                    await yt.mark_track_as_broken(file.id)
                    cached_data = None
                    print(f"[play] ❌ Exception retrieving L2 cache: {e}")

        # محاولة استرجاع من قاعدة البيانات (songs.db)
        if not is_reply_file and not downloaded_from_cache and not file.file_path:
            try:
                def _check_sqlite_cache(v_id):
                    conn = sqlite3.connect("songs.db")
                    conn.row_factory = sqlite3.Row
                    cursor = conn.cursor()
                    cursor.execute("SELECT msg_id, file_id FROM songs WHERE yt_id = ?", (v_id,))
                    row = cursor.fetchone()
                    conn.close()
                    return row if row else None
                row_cache = await asyncio.to_thread(_check_sqlite_cache, file.id)
                if row_cache and archive_channel_id:
                    if "file_id" in row_cache.keys() and row_cache["file_id"]:
                        try:
                            file.file_path = await client.download_media(row_cache["file_id"], file_name=local_target_path)
                            if file.file_path and os.path.exists(file.file_path):
                                downloaded_from_cache = True
                                print(f"[play] ✅ Downloaded from songs.db file_id: {file.file_path}")
                        except:
                            file.file_path = None
                    if (not file.file_path or not os.path.exists(file.file_path)) and row_cache["msg_id"]:
                        target_chat = archive_channel_id
                        archive_msg = await client.get_messages(target_chat, int(row_cache["msg_id"]))
                        if archive_msg:
                            file.file_path = await download_from_archive(client, archive_msg, local_target_path)
                            if file.file_path and os.path.exists(file.file_path):
                                downloaded_from_cache = True
                                def _update_file_id(v_id, f_id):
                                    conn = sqlite3.connect("songs.db")
                                    cursor = conn.cursor()
                                    cursor.execute("UPDATE songs SET file_id = ? WHERE yt_id = ?", (f_id, v_id))
                                    conn.commit()
                                    conn.close()
                                # استخراج file_id من الرسالة
                                if hasattr(archive_msg, 'audio') and archive_msg.audio:
                                    await asyncio.to_thread(_update_file_id, file.id, archive_msg.audio.file_id)
                                print(f"[play] ✅ Downloaded from songs.db msg_id: {file.file_path}")
            except Exception as e:
                print(f"[play] Exception in songs.db retrieval: {e}")

        # التحقق من مدة المقطع
        if not is_reply_file and not downloaded_from_cache and not file.file_path:
            if not file.is_live and duration_sec > config.DURATION_LIMIT:
                return await safe_edit(sent, f"• مدة المقطع طويلة جداً (حد أقصى {config.DURATION_LIMIT // 60} دقيقة)")

        if await r.get(f"logger:{Dev_FINAL}"):
            await utils.play_log(m, file.title, file.duration)

        file.user = mention

        if force:
            queue.force_add(chat_id, file)
        else:
            position = queue.add(chat_id, file)
            if await r.get(f"call_active:{chat_id}:{Dev_FINAL}"):
                if not is_reply_file:
                    await safe_edit(sent, f"• تمت الإضافة إلى قائمة الانتظار في المركز {position}\n{file.title}\n{file.duration}")
                    await buttons.edit_play_queued_markup(client, chat_id, sent.id, file.id, "تشغيل الآن", user_id=m.from_user.id)
                if tracks:
                    added = playlist_to_queue(chat_id, tracks)
                    try:
                        await client.send_message(chat_id=m.chat.id, text=f"• تم إضافة {len(tracks)} أغنية إلى القائمة" + added)
                    except:
                        pass
                try:
                    from plugins.FinalMusic import preload
                    asyncio.create_task(preload.start_preload(chat_id, count=2))
                except:
                    pass
                return

        # تحميل من يوتيوب إذا لم يتم التحميل من الكاش
        if not downloaded_from_cache and (not file.file_path or not os.path.exists(file.file_path)):
            print(f"[play] ⬇️ File path not found, downloading from YouTube: {file.id}")
            downloaded_path = await yt.download(file.id, is_live=file.is_live, video=getattr(file, "video", False))
            print(f"[play] yt.download returned: {downloaded_path}")
            
            if isinstance(downloaded_path, str) and downloaded_path.startswith("archive_msg_") and archive_channel_id:
                try:
                    cached_msg_id = int(downloaded_path.split("archive_msg_")[1])
                    target_chat = archive_channel_id
                    archive_msg = await client.get_messages(target_chat, cached_msg_id)
                    if archive_msg:
                        file.file_path = await download_from_archive(client, archive_msg, local_target_path)
                        print(f"[play] Downloaded from archive_msg: {file.file_path}")
                except Exception as e:
                    file.file_path = None
                    print(f"[play] Failed to download archive_msg: {e}")
            else:
                file.file_path = downloaded_path

            if not file.file_path or not os.path.exists(file.file_path):
                error_text = f"• فشل في تنزيل الوسائط (ID: {file.id})"
                print(f"[play] ❌ {error_text}")
                return await safe_edit(sent, error_text)

        # تشغيل الميديا
        try:
            await tune.play_media(chat_id=chat_id, message=sent, media=file, message_chat_id=message_chat_id if chat_id != message_chat_id else None)

            # رفع إلى قناة الأرشفة فقط إذا تم التحميل من يوتيوب
            if not is_reply_file and not file.is_live and not file.video and file.file_path and os.path.exists(file.file_path) and not downloaded_from_cache:
                try:
                    if archive_channel_id:
                        target_chat = archive_channel_id
                        print(f"[play] 📤 Uploading to archive channel: {file.id}")
                        channel_msg = await client.send_audio(
                            chat_id=target_chat,
                            audio=file.file_path,
                            title=file.title,
                            duration=int(file.duration_sec) if getattr(file, "duration_sec", None) else None
                        )
                        if channel_msg and channel_msg.audio:
                            await yt.save_track_to_cache(file.id, channel_msg.id)
                            print(f"[play] ✅ Saved to L2 cache: {file.id} -> msg_id {channel_msg.id}")
                except Exception as e:
                    logger.error(f"play_handler: archive upload failed for {file.id}: {e}")
                    print(f"[play] Archive upload error: {e}")
        except Exception as e:
            error_msg = str(e)
            print(f"[play] Error during play_media: {error_msg[:100]}")
            return await safe_edit(sent, f"• خطأ أثناء التشغيل: {error_msg[:100]}")

        if not tracks:
            return
        added = playlist_to_queue(chat_id, tracks)
        try:
            await client.send_message(chat_id=m.chat.id, text=f"• تم إضافة {len(tracks)} أغنية إلى القائمة" + added)
        except:
            pass

    except Exception as e:
        logger.exception(f"play_handler: unexpected error in chat {m.chat.id}: {e}")
        print(f"[play] Unexpected error: {e}")
        try:
            error_text = f"• صار خطأ غير متوقع أثناء التشغيل:\n<code>{str(e)[:300]}</code>"
            local_sent = locals().get("sent")
            if local_sent:
                await safe_edit(local_sent, error_text)
            else:
                await safe_reply(m, error_text)
        except Exception:
            pass
    finally:
        if old_bot_id:
            set_current_bot_id(old_bot_id)