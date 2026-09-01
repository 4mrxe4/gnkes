# Plugins1/FinalMusic/fm_core/userbot.py

from helpers.context import get_config, get_current_bot_id, set_current_bot_id, get_global_is_parent, redis_proxy as r, dev_final_proxy as Dev_FINAL, k_proxy as k
from pyrogram import Client
import logging
import json

from helpers.context import config_proxy as config

logger = logging.getLogger("FinalMusic")

class Userbot(Client):
    def __init__(self):
        self.clients = []
        self.one = None
        self.two = None
        self.three = None
        self._initialized = False
        self._assistant_loaded = False
    
    async def _get_assistant_session(self, num: int) -> str:
        """Assistant session comes from the PARENT config (SESSION1..3) or from
        the parent assistant_manager registry — the single source of truth for
        assistant sessions in botm_unified."""
        try:
            bot_id = getattr(config, 'Dev_FINAL', None) or Dev_FINAL
            if not bot_id or bot_id == 'unknown':
                return ""

            # Ask the parent assistant manager first (single source of truth).
            try:
                from helpers.assistant import assistant_manager
                data = await assistant_manager.get_assistant(str(bot_id))
                if data and data.get('session'):
                    session = data['session']
                    logger.info(f"✅ تم جلب جلسة المساعد من assistant_manager للبوت {bot_id}")
                    return session
            except Exception:
                pass

            session_key = f"{bot_id}:assistant_session"
            session = await r.get(session_key)
            if session:
                if isinstance(session, bytes):
                    session = session.decode('utf-8')
                logger.info(f"✅ تم جلب جلسة المساعد من Redis للبوت {bot_id}")
                return session
        except Exception as e:
            logger.warning(f"⚠️ فشل جلب جلسة المساعد من Redis: {e}")

        session_keys = {1: "SESSION1", 2: "SESSION2", 3: "SESSION3"}
        return getattr(config, session_keys.get(num, "SESSION1"), "")
    
    async def boot_client(self, num: int):
        if num == 1:
            session = await self._get_assistant_session(num)
        else:
            session_keys = {2: "SESSION2", 3: "SESSION3"}
            session = getattr(config, session_keys.get(num, ""), "")
        
        if not session:
            if num == 1:
                logger.info(f"ℹ️ لا توجد جلسة للحساب المساعد {num}")
            return
        
        name = f"HasiiTuneUB{num}"
        try:
            client = Client(
                name=name,
                api_id=config.API_ID,
                api_hash=config.API_HASH,
                session_string=session,
                in_memory=True
            )
            await client.start()
            
            if num == 1:
                self.one = client
            elif num == 2:
                self.two = client
            elif num == 3:
                self.three = client
            
            if client not in self.clients:
                self.clients.append(client)
            
            try:
                await client.send_message(config.LOGGER_ID, f"✅ الحساب المساعد {num} اشتغل")
            except Exception as e:
                logger.warning(f"⚠️ لم يتمكن الحساب المساعد {num} من إرسال رسالة إلى مجموعة السجلات: {e}")
            
            logger.info(f"👤 Assistant {num} started as @{client.me.username if client.me else 'unknown'}")
            
        except Exception as e:
            logger.error(f"❌ فشل تشغيل الحساب المساعد {num}: {e}")
    
    async def boot(self):
        old_bot_id = get_current_bot_id()
        is_parent = get_global_is_parent()
        
        try:
            if is_parent:
                bot_id = getattr(config, 'Dev_FINAL', None) or Dev_FINAL
                if bot_id and bot_id != 'unknown':
                    set_current_bot_id(bot_id)
            
            if self._initialized:
                return
            self._initialized = True
            
            for client in self.clients:
                try:
                    if client and hasattr(client, 'is_connected') and client.is_connected:
                        await client.stop()
                except:
                    pass
            self.clients.clear()
            self.one = None
            self.two = None
            self.three = None
            
            await self.boot_client(1)
            
            if getattr(config, 'SESSION2', ''):
                await self.boot_client(2)
            if getattr(config, 'SESSION3', ''):
                await self.boot_client(3)
            
            if not self.clients:
                logger.warning("⚠️ لا يوجد حسابات مساعدة متاحة")
                
        finally:
            if old_bot_id:
                set_current_bot_id(old_bot_id)
    
    async def exit(self):
        for client in self.clients:
            try:
                if client and hasattr(client, 'is_connected') and client.is_connected:
                    await client.stop()
            except Exception as e:
                logger.warning(f"Error stopping assistant: {e}")
        self.clients.clear()
        self.one = None
        self.two = None
        self.three = None
        self._initialized = False
        logger.info("Assistants stopped.")