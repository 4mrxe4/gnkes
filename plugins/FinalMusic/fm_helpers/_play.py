# Plugins1/FinalMusic/fm_helpers/_play.py

from helpers.context import is_sudoer, get_current_bot_id, set_current_bot_id, get_global_is_parent, redis_proxy as r, dev_final_proxy as Dev_FINAL, k_proxy as k
import os
import sqlite3
import asyncio
from compat import enums, errors, types
from compat import ChatMemberStatus
from compat import ChatAdminRequired, UserNotParticipant, UserAlreadyParticipant, ChatWriteForbidden, ChatSendPlainForbidden
from helpers.context import config_proxy as config
from ._admins import get_admins, is_auth

def checkUB(play):
    async def wrapper(client, m: types.Message):
        from plugins.FinalMusic import queue, yt, userbot
        
        old_bot_id = get_current_bot_id()
        
        try:
            bot_id = getattr(client, 'bot_id', None) or getattr(client, 'dev_final', None)
            if bot_id:
                set_current_bot_id(bot_id)
            
            async def safe_reply(text):
                try:
                    return await m.reply_text(text)
                except (errors.ChatWriteForbidden, errors.ChatSendPlainForbidden):
                    return None
                except Exception:
                    return None
            
            if not m.from_user:
                await safe_reply(m.lang["play_user_invalid"])
                return
            
            if m.chat.type != enums.ChatType.SUPERGROUP:
                await safe_reply(m.lang["play_chat_invalid"])
                return await client.leave_chat(m.chat.id)
            
            if not m.reply_to_message and (len(m.command) < 2 or (len(m.command) == 2 and m.command[1] == "-f")):
                await safe_reply(m.lang["play_usage"])
                return
            
            queue_limit = getattr(config, "QUEUE_LIMIT", 100)
            if len(queue.get_queue(m.chat.id)) >= queue_limit:
                await safe_reply(m.lang["play_queue_full"].format(queue_limit))
                return
            
            command = m.command[0].lower()
            force = command.endswith("force") or (len(m.command) > 1 and "-f" in m.command[1])
            cplay = command.startswith("c")
            video_requested = command.startswith("v") or command.startswith("cv")
            vplay_enabled = await r.get(f"vplay_enabled:{Dev_FINAL}")
            if video_requested and (not vplay_enabled or vplay_enabled == "disabled"):
                await safe_reply(m.lang["play_video_disabled"])
                return
            video = video_requested
            url = yt.url(m)
            if url and not m.reply_to_message and not yt.valid(url):
                return await m.reply_text(m.lang["play_unsupported"])
            
            play_mode = await r.get(f"play_mode:{m.chat.id}:{Dev_FINAL}")
            if play_mode == "enabled" or force:
                adminlist = await get_admins(m.chat.id)
                if (m.from_user.id not in adminlist and not await is_auth(m.chat.id, m.from_user.id) and not await is_sudoer(m.from_user.id)):
                    await safe_reply(m.lang["play_admin"])
                    return
            
            call_active = await r.get(f"call_active:{m.chat.id}:{Dev_FINAL}")
            if not call_active:
                assistant_client = await get_client(m.chat.id)
                if not assistant_client:
                    await safe_reply("⚠️ لا يوجد حساب مساعد متاح")
                    return
                try:
                    member = await client.get_chat_member(m.chat.id, assistant_client.app.id)
                    if member.status in [enums.ChatMemberStatus.BANNED, enums.ChatMemberStatus.RESTRICTED]:
                        try:
                            await client.unban_chat_member(chat_id=m.chat.id, user_id=assistant_client.app.id)
                        except:
                            await safe_reply(m.lang["play_banned"].format(client.name, assistant_client.app.id, assistant_client.app.mention, f"@{assistant_client.app.username}" if assistant_client.app.username else None))
                            return
                except errors.ChatAdminRequired:
                    await safe_reply("<blockquote><b>🔐 صلاحية المشرف مطلوبة للبوت</b></blockquote>\n\n<blockquote>لتشغيل الموسيقى في هذه المحادثة، يجب أن أكون <b>مشرفاً</b>.</blockquote>\n\n<blockquote><b>الصلاحيات المطلوبة:</b>\n• إدارة المحادثات المرئية\n• دعوة المستخدمين عبر الرابط\n• حذف الرسائل\n\nيرجى ترقيتي إلى مشرف مع تفعيل الصلاحيات المطلوبة.</blockquote>")
                    return
                except (errors.UserNotParticipant, errors.BadRequest) as _member_err:
                    if isinstance(_member_err, errors.BadRequest) and "PARTICIPANT_ID_INVALID" not in str(_member_err):
                        raise
                    if m.chat.username:
                        invite_link = m.chat.username
                        try:
                            await assistant_client.app.resolve_peer(invite_link)
                        except:
                            pass
                    else:
                        try:
                            invite_link = (await client.get_chat(m.chat.id)).invite_link
                            if not invite_link:
                                invite_link = await client.export_chat_invite_link(m.chat.id)
                        except errors.ChatAdminRequired:
                            await safe_reply("<blockquote><b>🔐 صلاحية المشرف مطلوبة للبوت</b></blockquote>\n\n<blockquote>لتشغيل الموسيقى في هذه المحادثة، يجب أن أكون <b>مشرفاً</b>.</blockquote>\n\n<blockquote><b>الصلاحيات المطلوبة:</b>\n• إدارة المحادثات المرئية\n• دعوة المستخدمين عبر الرابط\n• حذف الرسائل\n\nيرجى ترقيتي إلى مشرف مع تفعيل الصلاحيات المطلوبة.</blockquote>")
                            return
                        except Exception as ex:
                            await safe_reply(m.lang["play_invite_error"].format(type(ex).__name__))
                            return
                    umm = await safe_reply(m.lang["play_invite"].format(client.name))
                    if umm:
                        await asyncio.sleep(2)
                    try:
                        await assistant_client.app.join_chat(invite_link)
                    except errors.UserAlreadyParticipant:
                        pass
                    except errors.InviteRequestSent:
                        try:
                            await assistant_client.app.approve_chat_join_request(m.chat.id, assistant_client.app.id)
                        except errors.ChatAdminRequired:
                            if umm:
                                try:
                                    await umm.edit_text("<blockquote><b>🔐 صلاحية المشرف مطلوبة للبوت</b></blockquote>\n\n<blockquote>لتشغيل الموسيقى في هذه المحادثة، يجب أن أكون <b>مشرفاً</b>.</blockquote>\n\n<blockquote><b>الصلاحيات المطلوبة:</b>\n• إدارة المحادثات المرئية\n• دعوة المستخدمين عبر الرابط\n• حذف الرسائل\n\nيرجى ترقيتي إلى مشرف مع تفعيل الصلاحيات المطلوبة.</blockquote>")
                                except:
                                    pass
                            return
                        except Exception as ex:
                            if umm:
                                try:
                                    await umm.edit_text(m.lang["play_invite_error"].format(type(ex).__name__))
                                except:
                                    pass
                            return
                    except errors.ChatAdminRequired:
                        if umm:
                            try:
                                await umm.edit_text("<blockquote><b>🔐 صلاحية المشرف مطلوبة للبوت</b></blockquote>\n\n<blockquote>لتشغيل الموسيقى في هذه المحادثة، يجب أن أكون <b>مشرفاً</b>.</blockquote>\n\n<blockquote><b>الصلاحيات المطلوبة:</b>\n• إدارة المحادثات المرئية\n• دعوة المستخدمين عبر الرابط\n• حذف الرسائل\n\nيرجى ترقيتي إلى مشرف مع تفعيل الصلاحيات المطلوبة.</blockquote>")
                            except:
                                pass
                        return
                    except Exception as ex:
                        if umm:
                            try:
                                await umm.edit_text(m.lang["play_invite_error"].format(type(ex).__name__))
                            except:
                                pass
                        return
                    if umm:
                        try:
                            await umm.delete()
                        except:
                            pass
                    await assistant_client.app.resolve_peer(m.chat.id)
            try:
                await m.delete()
            except:
                pass
            
            if not video and not url and len(m.command) >= 2 and not m.reply_to_message:
                try:
                    query = " ".join(m.command[1:])
                    file_info = await yt.search(query, m.id)
                    if file_info and not file_info.is_live:
                        def _check_db():
                            conn = sqlite3.connect("songs.db")
                            cursor = conn.cursor()
                            cursor.execute("SELECT msg_id FROM songs WHERE yt_id = ?", (file_info.id,))
                            row = cursor.fetchone()
                            conn.close()
                            return bool(row)
                        if await asyncio.to_thread(_check_db):
                            file_info.file_path = f"downloads/{file_info.id}.mp3"
                except Exception:
                    pass
            
            return await play(client, m, force, url, cplay, video)
            
        finally:
            if old_bot_id:
                set_current_bot_id(old_bot_id)
    
    return wrapper

async def get_client(chat_id: int):
    from plugins.FinalMusic import tune, userbot
    
    old_bot_id = get_current_bot_id()
    
    try:
        bot_id = getattr(config, 'Dev_FINAL', None) or Dev_FINAL
        if bot_id and bot_id != 'unknown':
            set_current_bot_id(bot_id)
        

        if not userbot.clients:
            async for _ in userbot.boot():
                pass

        
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
        
        if hasattr(userbot, 'clients') and userbot.clients:
            if num <= len(userbot.clients):
                return userbot.clients[num - 1]
            return userbot.clients[0] if userbot.clients else None
        
        return None
        
    finally:
        if old_bot_id:
            set_current_bot_id(old_bot_id)