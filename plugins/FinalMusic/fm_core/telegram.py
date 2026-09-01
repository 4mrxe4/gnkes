# Plugins1/FinalMusic/fm_core/telegram.py

from helpers.context import get_config, redis_proxy as r, dev_final_proxy as Dev_FINAL, k_proxy as k
import asyncio
import os
import time
from compat import types
from compat import InlineKeyboardMarkup, InlineKeyboardButton

from helpers.context import config_proxy as config

from ..fm_helpers import Media, buttons, utils

FALLBACK_THUMB = "https://files.catbox.moe/8czm1s.png"

class Telegram:
    def __init__(self):
        self.active = []
        self.events = {}
        self.last_edit = {}
        self.active_tasks = {}
        self.sleep = 5
        # ✅ إضافة قفل لكل تحميل
        self._download_locks = {}
    
    def get_media(self, msg: types.Message) -> bool:
        return any([msg.audio, msg.document, msg.voice, msg.video])
    
    async def download(self, msg: types.Message, sent: types.Message) -> Media | None:
        from helpers.context import get_current_bot_id
        bot_id = get_current_bot_id() or 'unknown'
        chat_id = msg.chat.id
        
        # ✅ مفتاح فريد لكل بوت ومجموعة
        lock_key = f"{bot_id}:{chat_id}"
        
        # ✅ الحصول على قفل لمنع التنفيذ المتزامن لنفس البوت والمجموعة
        if lock_key not in self._download_locks:
            self._download_locks[lock_key] = asyncio.Lock()
        
        async with self._download_locks[lock_key]:
            msg_id = sent.id
            event = asyncio.Event()
            self.events[msg_id] = event
            self.last_edit[msg_id] = 0
            start_time = time.time()
            
            media = msg.audio or msg.voice or msg.video or msg.document
            is_video = bool(msg.video) or (msg.document and getattr(msg.document, "mime_type", "").startswith("video/"))
            file_id = getattr(media, "file_unique_id", None)
            file_ext = getattr(media, "file_name", "").split(".")[-1]
            file_size = getattr(media, "file_size", 0)
            file_title = getattr(media, "title", "Telegram File") or "Telegram File"
            duration = getattr(media, "duration", 0)
            
            DURATION_LIMIT = getattr(config, "DURATION_LIMIT", 3600)
            if duration > DURATION_LIMIT:
                try:
                    await sent.edit_text(sent.lang["play_duration_limit"].format(DURATION_LIMIT // 60))
                except (AttributeError, KeyError):
                    await sent.edit_text(f"⚠️ المدة طويلة جداً (حد أقصى {DURATION_LIMIT // 60} دقيقة)")
                return await sent.stop_propagation()
            
            if file_size > 200 * 1024 * 1024:
                try:
                    await sent.edit_text(sent.lang["dl_limit"])
                except (AttributeError, KeyError):
                    await sent.edit_text("⚠️ حجم الملف كبير جداً (حد أقصى 200 ميجابايت)")
                return await sent.stop_propagation()
            
            async def progress(current, total):
                if event.is_set():
                    return
                now = time.time()
                if now - self.last_edit[msg_id] < self.sleep:
                    return
                self.last_edit[msg_id] = now
                percent = current * 100 / total
                speed = current / (now - start_time or 1e-6)
                eta = utils.format_eta(int((total - current) / speed))
                try:
                    text = sent.lang["dl_progress"].format(utils.format_size(current), utils.format_size(total), percent, utils.format_size(speed), eta)
                    cancel_text = sent.lang.get("cancel", "إلغاء")
                except (AttributeError, KeyError):
                    text = f"📥 جاري التحميل: {percent:.1f}% | {utils.format_size(speed)}/ث | متبقي: {eta}"
                    cancel_text = "إلغاء"
                try:
                    await sent.edit_text(text, reply_markup=buttons.cancel_dl(cancel_text))
                except AttributeError:
                    await sent.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(cancel_text, callback_data="cancel_dl")]]))
            
            try:
                file_path = f"downloads/{file_id}.{file_ext}"
                file_added_to_active = False
                
                if not os.path.exists(file_path):
                    # ✅ التحقق من وجود الملف في قائمة التحميل النشطة
                    if file_id in self.active:
                        try:
                            await sent.edit_text(sent.lang["dl_active"])
                        except (AttributeError, KeyError):
                            await sent.edit_text("⚠️ الملف قيد التحميل بالفعل")
                        return await sent.stop_propagation()
                    
                    # ✅ إضافة الملف إلى القائمة النشطة
                    self.active.append(file_id)
                    file_added_to_active = True
                    
                    task = asyncio.create_task(msg.download(file_name=file_path, progress=progress))
                    self.active_tasks[msg_id] = task
                    await task
                
                if duration >= 3600:
                    duration_str = time.strftime("%H:%M:%S", time.gmtime(duration))
                else:
                    duration_str = time.strftime("%M:%S", time.gmtime(duration))
                
                return Media(
                    id=file_id, 
                    duration=duration_str, 
                    duration_sec=duration, 
                    file_path=file_path, 
                    message_id=sent.id, 
                    url=msg.link, 
                    title=file_title[:25], 
                    video=is_video
                )
                
            except asyncio.CancelledError:
                return await sent.stop_propagation()
            
            finally:
                # ✅ إزالة الملف من القائمة النشطة فقط إذا كان قد أضيف
                if file_id and file_added_to_active:
                    try:
                        self.active.remove(file_id)
                    except ValueError:
                        # ✅ تجاهل الخطأ إذا كان الملف غير موجود في القائمة
                        pass
                
                self.events.pop(msg_id, None)
                self.last_edit.pop(msg_id, None)
                self.active_tasks.pop(msg_id, None)
    
    async def cancel(self, query: types.CallbackQuery):
        event = self.events.get(query.message.id)
        task = self.active_tasks.pop(query.message.id, None)
        if event:
            event.set()
        if task and not task.done():
            task.cancel()
        if event or task:
            try:
                await query.edit_message_text(query.lang["dl_cancel"].format(query.from_user.mention))
            except (AttributeError, KeyError):
                await query.edit_message_text(f"✓ تم إلغاء التحميل بواسطة {query.from_user.mention}")
        else:
            try:
                await query.answer(query.lang["dl_not_found"], show_alert=True)
            except (AttributeError, KeyError):
                await query.answer("⚠️ لا يوجد تحميل نشط", show_alert=True)