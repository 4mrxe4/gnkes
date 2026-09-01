
from __future__ import annotations

import asyncio
import builtins
import importlib
import json
import os
import re
import shutil
import sys
import threading
import time
import types
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple

from aiogram import Bot as AioBot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode as AioParseMode

from compat import CompatClient

from helpers.top_snapshot import start_periodic_refresh, stop_periodic_refresh

from helpers.context import (
    inject_bot_data,
    set_current_bot_id,
    isolated_add_handlers,
    reset_bot_handlers,
    set_global_is_parent,
    _bot_contexts,
    get_current_bot_id,
    sync_client_identity,
)
from helpers.redis import RedisFake
from helpers.assistant import assistant_manager
from dotenv import load_dotenv


class BotClusterManager:

    def __init__(self):
        self.clusters: Dict[int, dict] = {}
        self.bots: Dict[str, dict] = {}
        self.MAX_BOTS_PER_CLUSTER = 3
        self.cluster_counter = 0
        self._lock = asyncio.Lock()
        self._bot_locks: Dict[str, asyncio.Lock] = {}
        self._polling_tasks: Dict[str, asyncio.Task] = {}
        self._polling_generations: Dict[str, int] = {}
        self._cluster_threads: Dict[int, threading.Thread] = {}

    def _get_bot_lock(self, bot_id: str) -> asyncio.Lock:
        """يعيد قفلاً مخصصاً لكل bot_id (fix B-8 — يمنع Race Condition بين
        Start/Stop/Reload المتزامنة لنفس البوت)."""
        if bot_id not in self._bot_locks:
            self._bot_locks[bot_id] = asyncio.Lock()
        return self._bot_locks[bot_id]

    def _start_top_snapshot_scheduler(self, bot_id: str) -> None:
        """يبدأ مهمة تحديث توبات هذا البوت كل 10 دقائق في الخلفية (مهمة
        واحدة فقط لكل bot_id — start_periodic_refresh نفسها تمنع التكرار).
        get_client يُستدعى في كل دورة تحديث بدل التقاط عميل ثابت الآن، حتى
        يبقى صحيحاً بعد أي إعادة تشغيل/تحديث توكن لنفس البوت."""
        start_periodic_refresh(bot_id, lambda: self.bots.get(bot_id, {}).get('client'))

    def get_or_create_cluster(self) -> int:
        for cluster_id in list(self.clusters.keys()):
            bots_in_cluster = sum(1 for b in self.bots.values() if b.get('cluster_id') == cluster_id)
            if bots_in_cluster < self.MAX_BOTS_PER_CLUSTER:
                return cluster_id

        self.cluster_counter += 1
        self.clusters[self.cluster_counter] = {
            'bots': [],
            'created_at': time.time(),
        }
        return self.cluster_counter

    def _assign_cluster(self, bot_id: str) -> int:
        cluster_id = self.get_or_create_cluster()
        if cluster_id in self.clusters:
            self.clusters[cluster_id]['bots'].append(bot_id)
        return cluster_id

    async def reload_bot_config(self, bot_id: str) -> Optional[types.ModuleType]:
        if bot_id not in self.bots:
            print(f"Bot {bot_id} not found for reload")
            return None

        bot_info = self.bots[bot_id]
        bot_dir = f"bots_data/{bot_id}"
        config_path = os.path.join(bot_dir, "settings.py")

        if not os.path.exists(config_path):
            print(f"Config file not found for bot {bot_id}")
            return None

        try:
            with open(config_path, "r", encoding="utf-8") as f:
                code = f.read()

            config_module_name = f"config_{bot_id}"
            if config_module_name in sys.modules:
                del sys.modules[config_module_name]

            new_config = types.ModuleType(config_module_name)
            exec(code, new_config.__dict__)
            sys.modules[config_module_name] = new_config

            if bot_id in _bot_contexts:
                _bot_contexts[bot_id]['config'] = new_config
                if hasattr(new_config, 'r'):
                    _bot_contexts[bot_id]['redis'] = new_config.r

            bot_info['config'] = new_config
            if hasattr(new_config, 'r'):
                bot_info['redis'] = new_config.r

            if 'config' in sys.modules:
                sys.modules['settings'] = new_config

            print(f"Config reloaded for bot {bot_id}")
            return new_config

        except Exception as e:
            print(f"Failed to reload config for bot {bot_id}: {e}")
            return None

    def _create_aiogram_objects(self, bot_token: str, bot_id: str, owner_id=None,
                                redis_instance=None, config_instance=None, is_parent: bool = False):
        """ينشئ Bot/Dispatcher/Router ويعيد (aiogram_bot, dispatcher, router, compat_client)."""
        aiogram_bot = AioBot(token=bot_token, default=DefaultBotProperties(parse_mode=AioParseMode.HTML))

        dispatcher = Dispatcher()
        router = Router(name=f"bot_{bot_id}_router")

        compat_client = CompatClient(
            aiogram_bot,
            bot_id=bot_id,
            bot_token=bot_token,
            owner_id=owner_id,
            redis=redis_instance,
            config=config_instance,
            is_parent=is_parent,
        )

        _bot_contexts[bot_id] = {
            'bot_id': bot_id,
            'client': compat_client,
            'aiogram_bot': aiogram_bot,
            'dispatcher': dispatcher,
            'router': router,
            'redis': redis_instance,
            'config': config_instance,
            'owner_id': owner_id,
            'is_parent': is_parent,
        }

        return aiogram_bot, dispatcher, router, compat_client

    def _find_bot_by_token(self, bot_token: str) -> Optional[str]:
        """يرجع bot_id الذي يستخدم نفس التوكن حاليًا (إن وُجد). يمنع تشغيل نسختين
        من نفس التوكن في آنٍ واحد — وهو أصل TelegramConflictError."""
        if not bot_token:
            return None
        token_id = str(bot_token).split(':')[0]
        for bid, info in self.bots.items():
            info_token = info.get('token')
            if info_token:
                if str(info_token) == str(bot_token):
                    return str(bid)
                if str(info_token).split(':')[0] == token_id:
                    return str(bid)
        return None

    def _polling_generation(self, bot_id: str) -> int:
        """جيل (generation) polling الحالي للبوت — يُستخدم للكشف عن أي مهمة قديمة
        (من إعادة تحميل سابقة) ما زالت حية، بغضّ النظر عن تسجيلها في _polling_tasks."""
        if bot_id not in self._polling_generations:
            self._polling_generations[bot_id] = 0
        return self._polling_generations[bot_id]

    async def _stop_polling_clean(self, bot_id: str, dispatcher: Optional[Dispatcher],
                                  aiogram_bot: Optional[AioBot],
                                  task: Optional[asyncio.Task] = None) -> None:
        """يوقف polling بوت واحد إيقافًا نظيفًا وكاملًا — الترتيب جوهري:

        1) dispatcher.stop_polling(): يطلب من aiogram إنهاء حلقة getUpdates
           بشكل تعاوني (يُخرج _listen_updates من انتظار getUpdates، يُنهي
           start_polling ويطلق shutdown hooks). هذا يحرّر قفل getUpdates على
           مستوى تيليجرام فعليًا.
        2) إلغاء المهمة task (احتياط إذا لم تستجب للإيقاف التعاوني) وانتظار
           خروجها الفعلي — يضمن عدم بقاء أي coroutine يقرأ updates.
        3) إغلاق جلسة HTTP الخاصة بالبوت — فقط بعد انتهاء الـ poller من
           استخدامها، حتى لا يبقى poller قديم يعيد فتحها ويواصل getUpdates.
        لا يُستخدم أي sleep — الإيقاف مبني على إشارات/أحداث حقيقية، وعدم
        البدء الجديد قبل العودة من هذه الدالة يضمن عدم وجود فترتين من
        getUpdates لنفس التوكن في أي لحظة."""
        gen = self._polling_generation(bot_id)
        self._polling_generations[bot_id] = gen + 1  # bump: أي مهمة قديمة تُنشأ لاحقًا سترى جيلًا مختلفًا

        # يُوقَف تحديث توبات هذا البوت هنا أيضاً (نفس نقطة إيقاف الـ polling
        # تماماً) — فلا تبقى مهمة تحديث دورية تعمل لبوت متوقف، ولا تتكرر عند
        # إعادة التشغيل لاحقاً لأن start_periodic_refresh تُنشئ مهمة جديدة.
        stop_periodic_refresh(bot_id)

        # 1) إيقاف تعاوني عبر aiogram (يُنهي getUpdates ويُطلق الـ lock)
        if dispatcher is not None:
            try:
                await dispatcher.stop_polling()
            except RuntimeError:
                pass  # polling غير مُشغّل أصلًا
            except Exception as e:
                print(f"[cluster] stop_polling error for bot {bot_id}: {e}")

        # 2) إلغاء المهمة المسجلة وانتظار خروجها الفعلي
        if task is None:
            task = self._polling_tasks.pop(bot_id, None)
        else:
            if self._polling_tasks.get(bot_id) is task:
                self._polling_tasks.pop(bot_id, None)
        if task is not None and not task.done():
            task.cancel()
            try:
                await task
            except (asyncio.CancelledError, Exception):
                pass

        # 3) إغلاق جلسة HTTP — بعد توقف الـ poller نهائيًا عن استخدامها
        if aiogram_bot is not None:
            try:
                await aiogram_bot.session.close()
            except Exception:
                pass

    async def start_isolated_bot(self, bot_id: str, bot_token: str, is_parent: bool = False) -> Tuple[bool, str]:
        async with self._lock:
            if bot_id in self.bots:
                bot_info = self.bots[bot_id]
                if bot_info.get('status') == 'running':
                    print(f"Bot {bot_id} is already running, skipping")
                    return True, "Bot already running"
                else:
                    del self.bots[bot_id]

            # منع تشغيل نسختين من نفس التوكن في آنٍ واحد (أصل Conflict).
            # عند الإقلاع/الاستعادة: إذا كان بوت آخر يستخدم نفس التوكن فلا نبدأ
            # نسخة جديدة إطلاقًا — يجب إيقاف القديم أولاً عبر stop/reload.
            existing = self._find_bot_by_token(bot_token)
            if existing is not None and str(existing) != str(bot_id):
                print(f"[cluster] start_isolated_bot: token {bot_id} already in use by bot {existing}, refusing to start duplicate poller")
                return False, f"Token already in use by bot {existing}"

            try:
                r_fake = RedisFake(bot_id=bot_id)

                # Restore per-bot owner (Dev) identity so rankDEV and botowner
                # are (re)written on start — without this, restored children
                # never get {owner_id}:rankDEV:{bot_id} and the Dev panel
                # treats the owner as a normal member ("هلا بك عضو").
                saved_owner_id = None
                try:
                    global_r = RedisFake()
                    saved_data = await global_r.hget('subscribed_bots', bot_id)
                    if saved_data:
                        saved_info = json.loads(saved_data)
                        saved_owner_id = saved_info.get('owner_id')
                    else:
                        saved_data2 = await r_fake.hget('subscribed_bots', bot_id)
                        if saved_data2:
                            saved_info2 = json.loads(saved_data2)
                            saved_owner_id = saved_info2.get('owner_id')
                    if saved_owner_id is None:
                        raw_owner = await r_fake.get(f'{bot_id}botowner')
                        if raw_owner:
                            saved_owner_id = int(raw_owner)
                    if saved_owner_id is None:
                        raw_owner2 = await r_fake.get('owner_id')
                        if raw_owner2:
                            saved_owner_id = int(raw_owner2)
                except Exception as e:
                    print(f"[cluster] Failed to read saved owner_id for {bot_id}: {e}")

                bot_dir = f"bots_data/{bot_id}"
                os.makedirs(bot_dir, exist_ok=True)
                config_path = os.path.join(bot_dir, "settings.py")
                if not os.path.exists(config_path):
                    try:
                        await self._create_bot_files(bot_id, bot_token, owner_id=saved_owner_id, is_parent=is_parent)
                        print(f"[cluster] Generated missing settings.py for bot {bot_id}")
                    except Exception as e:
                        print(f"[cluster] Failed to generate settings.py for bot {bot_id}: {e}")
                        import traceback
                        traceback.print_exc()
                        return False, f"Failed to generate settings: {str(e)}"

                assistant_client = await assistant_manager.create_assistant_client(bot_id)

                aiogram_bot, dispatcher, router, bot_client = self._create_aiogram_objects(
                    bot_token, bot_id, saved_owner_id, r_fake, None, is_parent
                )

                loop = asyncio.get_running_loop()

                try:
                    me = await aiogram_bot.get_me()
                    bot_username = me.username or "unknown"
                    sync_client_identity(bot_client, me)
                except Exception:
                    bot_username = "unknown"

                set_current_bot_id(bot_id)
                set_global_is_parent(is_parent)

                inject_bot_data(bot_client, bot_id, saved_owner_id, r_fake, None, is_parent)
                _bot_contexts[bot_id]['redis'] = r_fake
                _bot_contexts[bot_id]['owner_id'] = saved_owner_id
                _bot_contexts[bot_id]['assistant'] = assistant_client
                _bot_contexts[bot_id]['is_parent'] = is_parent

                cluster_id = self._assign_cluster(bot_id)
                self.bots[bot_id] = {
                    'client': bot_client,
                    'aiogram_bot': aiogram_bot,
                    'dispatcher': dispatcher,
                    'router': router,
                    'assistant': assistant_client,
                    'cluster_id': cluster_id,
                    'owner_id': saved_owner_id,
                    'token': bot_token,
                    'started_at': time.time(),
                    'status': 'running',
                    'is_parent': is_parent,
                    'bot_id': bot_id,
                    'bot_username': bot_username
                }

                await r_fake.set(f"{bot_id}:is_active", "true")
                await r_fake.set(f"{bot_id}:status", "running")
                await r_fake.set('bot_id', bot_id)
                await r_fake.set('dev_final', bot_id)
                await r_fake.set('bot_username', bot_username)

                # NOTE: handlers must be attached to `router` BEFORE polling
                # starts. aiogram's Dispatcher.start_polling() resolves which
                # update types to request from Telegram (allowed_updates) by
                # inspecting which observers (router.message,
                # router.callback_query, router.inline_query, ...) have
                # handlers registered, and it does this once, right when
                # polling begins — not per get_updates() call. Previously,
                # start_polling() was scheduled as a background task (via
                # create_task) BEFORE _attach_handlers() ran, and since
                # _attach_handlers() itself awaits network calls
                # (client.get_me(), etc.), the polling task frequently got a
                # chance to run — and take that allowed_updates snapshot —
                # while the router still had zero handlers registered for
                # some event kinds. Whichever handler kind lost that race
                # (e.g. inline_query, only registered by a couple of plugins
                # and so attached later than the many message handlers) would
                # then be silently excluded from Telegram's updates for the
                # entire polling session, with no exception anywhere — Telegram
                # just never delivers that update type at all. Attaching
                # handlers first removes the race for every update kind.
                success = await self._attach_handlers(bot_client, bot_id, owner_id=saved_owner_id, is_parent=is_parent)

                if not success:
                    return False, "Failed to attach handlers"

                polling_task = loop.create_task(self._run_bot_polling(bot_id, aiogram_bot, dispatcher))
                self._polling_tasks[bot_id] = polling_task
                self._start_top_snapshot_scheduler(bot_id)

                return True, "Bot started successfully"

            except Exception as e:
                print(f"Failed to start bot {bot_id}: {e}")
                import traceback
                traceback.print_exc()
                return False, str(e)

    async def _run_bot_polling(self, bot_id: str, aiogram_bot: AioBot, dispatcher: Dispatcher):
        """يعمل polling آمن لكل بوت — أي خطأ لا يقتل العملية.

        يحمل (يلتقط) جيل polling الحالي عند بدئه: إذا استُدعي إيقاف نظيف
        (_stop_polling_clean) وزاد الجيل، فهذه المهمة أصبحت قديمة ويجب أن
        تتوقف فورًا حتى لو لم تُلغَ مباشرة (مثلاً إذا لم تكن مسجلة في
        _polling_tasks وقت الإلغاء). هذا يمنع بقاء poller قديم يعيد فتح
        جلسته ويواصل getUpdates لنفس التوكن بعد تحديث البوت."""
        my_gen = self._polling_generation(bot_id)
        try:
            await dispatcher.start_polling(aiogram_bot, handle_signals=False, close_bot_session=False)
        except asyncio.CancelledError:
            pass
        except Exception as e:
            # TelegramConflictError تعني أن نسخة أخرى من نفس التوكن تسحب
            # getUpdates — هذا ليس خطأ شبكة عابرًا بل حالة معمارية خاطئة.
            # نطبعها بوضوح ولا نحاول إعادة المحاولة (retry) لإخفائها.
            if "Conflict" in type(e).__name__ or "terminated by other getUpdates" in str(e):
                print(f"[cluster] FATAL polling conflict for bot {bot_id}: {e}")
            else:
                print(f"[cluster] polling error for bot {bot_id}: {e}")
                import traceback
                traceback.print_exc()
        finally:
            if self._polling_generation(bot_id) == my_gen:
                # لم يُستدعَ إيقاف نظيف لهذا البوت — أغلِق الجلسة (لو أُغلقها
                # _stop_polling_clean بالفعل فالاستدعاء المزدوج آمن).
                try:
                    await aiogram_bot.session.close()
                except Exception:
                    pass

    async def reload_bot(self, bot_id: str) -> Tuple[bool, str]:
        async with self._get_bot_lock(bot_id):
            return await self._reload_bot_locked(bot_id)

    async def _reload_bot_locked(self, bot_id: str) -> Tuple[bool, str]:
        if bot_id not in self.bots:
            return False, "Bot not found"

        try:
            bot_info = self.bots[bot_id]
            token = bot_info['token']
            is_parent = bot_info.get('is_parent', False)

            # ===== الإيقاف النظيف الكامل للنسخة القديمة =====
            # الترتيب الحرج الذي يمنع TelegramConflictError نهائيًا:
            #   1) dispatcher.stop_polling() — يطلب من aiogram إنهاء حلقة
            #      getUpdates بشكل تعاوني (يُخرج _listen_updates من انتظاره،
            #      ينهي start_polling ويطلق shutdown hooks). هذا وحده يحرر
            #      قفل getUpdates على مستوى تيليجرام.
            #   2) إلغاء مهمة الـ polling المسجلة وانتظار خروجها الفعلي —
            #      نضمن عدم بقاء أي coroutine يقرأ updates من هذا البوت.
            #   3) إغلاق جلسة HTTP القديمة — بعد توقف الـ poller نهائيًا عن
            #      استخدامها، فلا يمكن أن يعيد poller قديم فتحها ويواصل
            #      getUpdates.
            # لا يوجد أي sleep: البوت الجديد لا يبدأ إلا بعد عودة هذا
            # الإيقاف، أي لا توجد لحظة يكون فيها pollerان لنفس التوكن أحياء.
            old_dispatcher = bot_info.get('dispatcher')
            old_bot = bot_info.get('aiogram_bot')
            old_task = self._polling_tasks.get(bot_id)
            await self._stop_polling_clean(bot_id, old_dispatcher, old_bot, task=old_task)

            print(f"[cluster] reload_bot: old poller fully stopped for bot_id={bot_id}, starting new poller")

            # منع أي ازدواج: لا يجوز أن يوجد بوت آخر بنفس التوكن أثناء الإقلاع
            existing = self._find_bot_by_token(token)
            if existing is not None and str(existing) != str(bot_id):
                print(f"[cluster] reload_bot: token {bot_id} already in use by bot {existing}, aborting reload")
                return False, f"Token conflict: bot {existing} already uses this token"

            aiogram_bot, dispatcher, router, bot_client = self._create_aiogram_objects(
                token, bot_id, bot_info.get('owner_id'), None, None, is_parent
            )

            bot_info['client'] = bot_client
            bot_info['aiogram_bot'] = aiogram_bot
            bot_info['dispatcher'] = dispatcher
            bot_info['router'] = router
            bot_info['status'] = 'running'

            # See start_isolated_bot for why handlers must be attached before
            # polling starts (allowed_updates race — a kind like inline_query
            # can silently never be delivered for the whole session otherwise).
            success = await self._attach_handlers(bot_client, bot_id, owner_id=bot_info.get('owner_id'),
                                                  is_parent=is_parent)
            if not success:
                bot_info['status'] = 'stopped'
                return False, "Failed to attach handlers"

            loop = asyncio.get_running_loop()
            polling_task = loop.create_task(self._run_bot_polling(bot_id, aiogram_bot, dispatcher))
            self._polling_tasks[bot_id] = polling_task
            self._start_top_snapshot_scheduler(bot_id)

            return True, "Bot reloaded successfully"

        except Exception as e:
            print(f"Failed to reload bot {bot_id}: {e}")
            import traceback
            traceback.print_exc()
            return False, str(e)

    async def start_bot(self, token: str, owner_id: int, days: int = 30, is_parent: bool = False) -> Tuple[bool, str]:
        bot_id = token.split(':')[0]

        async with self._get_bot_lock(bot_id):
            return await self._start_bot_locked(token, owner_id, days, is_parent, bot_id)

    async def _start_bot_locked(self, token: str, owner_id: int, days: int = 30,
                                is_parent: bool = False, bot_id: str = None) -> Tuple[bool, str]:
        if bot_id is None:
            bot_id = token.split(':')[0]

        async with self._lock:
            if bot_id in self.bots:
                return False, "Bot already exists"

        await self._isolate_bot_data(bot_id)

        bot_dir = f"bots_data/{bot_id}"
        os.makedirs(bot_dir, exist_ok=True)

        await self._create_bot_files(bot_id, token, owner_id, is_parent)

        r_fake = RedisFake(bot_id=bot_id)
        config_instance = None
        try:
            config_module_name = f"config_{bot_id}"
            if config_module_name in sys.modules:
                del sys.modules[config_module_name]
            new_config = types.ModuleType(config_module_name)
            config_path = os.path.join(bot_dir, "settings.py")
            with open(config_path, "r", encoding="utf-8") as f:
                exec(f.read(), new_config.__dict__)
            sys.modules[config_module_name] = new_config
            config_instance = new_config
            if hasattr(new_config, 'r'):
                r_fake = new_config.r
        except Exception as e:
            print(f"Failed to load config for bot {bot_id}: {e}")
            return False, f"Failed to load config: {str(e)}"

        aiogram_bot, dispatcher, router, bot_client = self._create_aiogram_objects(
            token, bot_id, owner_id, r_fake, config_instance, is_parent
        )

        loop = asyncio.get_running_loop()

        try:
            me = await aiogram_bot.get_me()
            bot_username = me.username or "unknown"
            config_instance.botUsername = bot_username
            sync_client_identity(bot_client, me)
        except Exception:
            bot_username = "unknown"

        # See start_isolated_bot for why handlers must be attached before
        # polling starts (allowed_updates race — a kind like inline_query
        # can silently never be delivered for the whole session otherwise).
        await self._attach_handlers(bot_client, bot_id, owner_id=owner_id, is_parent=is_parent)

        polling_task = loop.create_task(self._run_bot_polling(bot_id, aiogram_bot, dispatcher))
        self._polling_tasks[bot_id] = polling_task

        async with self._lock:
            self.bots[bot_id] = {
                'client': bot_client,
                'aiogram_bot': aiogram_bot,
                'dispatcher': dispatcher,
                'router': router,
                'loop': loop,
                'cluster_id': 1,
                'owner_id': owner_id,
                'token': token,
                'started_at': time.time(),
                'expiry': time.time() + (days * 86400),
                'status': 'running',
                'is_parent': is_parent,
                'bot_username': bot_username
            }

        await self._save_bot_data(bot_id, token, owner_id, days, bot_username, is_parent)
        self._start_top_snapshot_scheduler(bot_id)

        return True, "Bot started in Cluster 1"

    async def _create_bot_files(self, bot_id: str, token: str, owner_id: int, is_parent: bool = False):
        bot_dir = f"bots_data/{bot_id}"
        os.makedirs(bot_dir, exist_ok=True)

        config_path = os.path.join(bot_dir, "settings.py")

        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                session1_match = re.search(r'SESSION1 = "(.*?)"', content)
                session2_match = re.search(r'SESSION2 = "(.*?)"', content)
                session3_match = re.search(r'SESSION3 = "(.*?)"', content)

                session1 = session1_match.group(1) if session1_match else ""
                session2 = session2_match.group(1) if session2_match else ""
                session3 = session3_match.group(1) if session3_match else ""

                await self._write_config_file(bot_id, token, owner_id, session1, session2, session3, is_parent)
                return

            except Exception as e:
                print(f"Failed to read existing config for bot {bot_id}: {e}")

        load_dotenv()

        session1 = os.getenv("STRING_SESSION", "")
        session2 = os.getenv("STRING_SESSION2", "")
        session3 = os.getenv("STRING_SESSION3", "")

        if not is_parent:
            session1 = ""
            session2 = ""
            session3 = ""

        await self._write_config_file(bot_id, token, owner_id, session1, session2, session3, is_parent)

    async def _write_config_file(self, bot_id: str, token: str, owner_id: int, session1: str, session2: str,
                                 session3: str, is_parent: bool = False):
        bot_dir = f"bots_data/{bot_id}"
        config_path = os.path.join(bot_dir, "settings.py")

        config_content = f'''# settings.py - for bot {bot_id}

import sys
from helpers import redis
sys.modules['redis.asyncio'] = redis
sys.modules['redis'] = redis

import os
from os import getenv
from typing import List
from dotenv import load_dotenv

load_dotenv()

Dev_FINAL = "{bot_id}"
TOKEN = "{token}"
OWNER_ID = {owner_id}
API_ID = 29914850
API_HASH = "de7b0ee6f49fff7b4a5f0e5c015972ce"
LOGGER_ID = int(getenv("LOGGER_ID", "-1002926122970"))
botUsername = None

SESSION1 = "{session1}"
SESSION2 = "{session2}"
SESSION3 = "{session3}"

SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/BBBZZZB")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/Z3ZZ_Z0")

MONGO_URL = getenv("MONGO_DB_URI", "")

ARCHIVE_CHANNEL = int(getenv("ARCHIVE_CHANNEL", "-1001828975467"))

DURATION_LIMIT = int(getenv("DURATION_LIMIT", "300")) * 60
QUEUE_LIMIT = int(getenv("QUEUE_LIMIT", "30"))
PLAYLIST_LIMIT = int(getenv("PLAYLIST_LIMIT", "20"))

COOKIES_URL = []
EXCLUDED_USERNAMES = []
USERHASH = getenv("USERHASH", "3d9ce4bdd60daae777c186ff7")
IS_PARENT = {str(is_parent)}

from helpers.redis import RedisFake
r = RedisFake(bot_id=Dev_FINAL)

from kvsqlite.sync import Client as DB
ytdb = DB('ytdb.sqlite')
sounddb = DB('sounddb.sqlite')
wsdb = DB('wsdb.sqlite')

class Config:
    def __init__(self):
        self.API_ID = API_ID
        self.API_HASH = API_HASH
        self.BOT_TOKEN = TOKEN
        self.OWNER_ID = OWNER_ID
        self.SESSION1 = SESSION1
        self.SESSION2 = SESSION2
        self.SESSION3 = SESSION3
        self.LOGGER_ID = LOGGER_ID
        self.MONGO_URL = MONGO_URL
        self.ARCHIVE_CHANNEL = ARCHIVE_CHANNEL
        self.DURATION_LIMIT = DURATION_LIMIT
        self.QUEUE_LIMIT = QUEUE_LIMIT
        self.PLAYLIST_LIMIT = PLAYLIST_LIMIT
        self.SUPPORT_CHANNEL = SUPPORT_CHANNEL
        self.SUPPORT_CHAT = SUPPORT_CHAT
        self.EXCLUDED_CHATS = []
        self.AUTO_END = False
        self.AUTO_LEAVE = False
        self.THUMB_GEN = True
        self.VIDEO_PLAY = True
        self.VIDEO_MAX_HEIGHT = 1080
        self.COOKIES_URL = COOKIES_URL
        self.DEFAULT_THUMB = getenv("DEFAULT_THUMB", "https://files.catbox.moe/8czm1s.png")
        self.PING_IMG = getenv("PING_IMG", "https://files.catbox.moe/8e4f78.jpg")
        self.START_IMG = getenv("START_IMG", "https://files.catbox.moe/8e4f78.jpg")
        self.RADIO_IMG = getenv("RADIO_IMG", "https://files.catbox.moe/8e4f78.jpg")
        self.EXCLUDED_USERNAMES = EXCLUDED_USERNAMES
        self.USERHASH = USERHASH
        self.IS_PARENT = IS_PARENT

config = Config()

__all__ = [
    'Dev_FINAL', 'TOKEN', 'OWNER_ID', 'API_ID', 'API_HASH',
    'botUsername', 'SESSION1', 'SESSION2', 'SESSION3',
    'SUPPORT_CHANNEL', 'SUPPORT_CHAT', 'MONGO_URL',
    'ARCHIVE_CHANNEL', 'DURATION_LIMIT', 'QUEUE_LIMIT', 'PLAYLIST_LIMIT',
    'COOKIES_URL', 'EXCLUDED_USERNAMES', 'USERHASH',
    'config', 'ytdb', 'sounddb', 'wsdb', 'r', 'RedisFake', 'IS_PARENT'
]
'''

        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(config_content)

        init_path = os.path.join(bot_dir, "__init__.py")
        with open(init_path, 'w', encoding='utf-8') as f:
            f.write(f'# Package for bot {bot_id}\n')

    async def load_module_isolated(self, module_path: str, b_id: str, is_parent: bool = False) -> Optional[types.ModuleType]:
        try:
            unique_name = f"{module_path}_{b_id}"

            if unique_name in sys.modules:
                del sys.modules[unique_name]

            original_module = importlib.import_module(module_path)

            new_module = types.ModuleType(unique_name)

            for attr_name in dir(original_module):
                if attr_name.startswith('__') and attr_name.endswith('__'):
                    continue

                attr_value = getattr(original_module, attr_name)

                if isinstance(attr_value, type):
                    setattr(new_module, attr_name, attr_value)
                elif callable(attr_value):
                    setattr(new_module, attr_name, attr_value)
                elif isinstance(attr_value, (list, dict, set, tuple)):
                    setattr(new_module, attr_name, attr_value.__class__(attr_value))
                else:
                    setattr(new_module, attr_name, attr_value)

            sys.modules[unique_name] = new_module

            new_module.__bot_id__ = b_id
            new_module.__is_isolated__ = True

            return new_module

        except Exception as e:
            print(f"Failed to load module {module_path} for bot {b_id}: {e}")
            return None

    async def initialize_bot_objects(self, b_id: str, is_parent: bool = False):
        """يهيئ كائنات الموسيقى الحقيقية داخل سياق البوت (per-bot isolation).
        الكائنات تُبنى من plugins.FinalMusic وتُخزَّن في _bot_contexts[bot_id]
        بحيث تعمل كل الـ proxies (get_queue/get_tune/get_yt/...) على نفس المصدر."""
        try:
            set_current_bot_id(b_id)
            set_global_is_parent(is_parent)
            if b_id not in _bot_contexts:
                _bot_contexts[b_id] = {}
            bot_context = _bot_contexts[b_id]

            from plugins.FinalMusic.fm_helpers import Queue
            from plugins.FinalMusic.fm_core.calls import TgCall
            from plugins.FinalMusic.fm_core.youtube import YouTube
            from plugins.FinalMusic.fm_core.telegram import Telegram
            from plugins.FinalMusic.fm_core.preload import PreloadManager
            from plugins.FinalMusic.fm_core.userbot import Userbot

            if bot_context.get('queue') is None:
                bot_context['queue'] = Queue()
            if bot_context.get('tune') is None:
                bot_context['tune'] = TgCall()
            if bot_context.get('yt') is None:
                bot_context['yt'] = YouTube()
            if bot_context.get('tg') is None:
                bot_context['tg'] = Telegram()
            if bot_context.get('preload') is None:
                try:
                    bot_context['preload'] = PreloadManager()
                except Exception:
                    bot_context['preload'] = None
            if bot_context.get('userbot') is None:
                bot_context['userbot'] = Userbot()
        except Exception as e:
            print(f"Failed to create objects for bot {b_id}: {e}")
            import traceback
            traceback.print_exc()

    async def _attach_handlers(self, client, bot_id: str, owner_id: int = None,
                               loop: asyncio.AbstractEventLoop = None,
                               is_parent: bool = False):
        bot_config_dir = os.path.abspath(f"bots_data/{bot_id}")

        config_path = os.path.join(bot_config_dir, "settings.py")
        bot_config = None
        old_config = None
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                code = f.read()

            bot_config = types.ModuleType(f"config_{bot_id}")
            exec(code, bot_config.__dict__)
            sys.modules[f"config_{bot_id}"] = bot_config

            old_config = sys.modules.get('settings')
            sys.modules['settings'] = bot_config

            redis_instance = bot_config.r

        except Exception as e:
            print(f"Failed to load settings.py for bot {bot_id}: {e}")
            return False

        try:
            me = await client.get_me()
            bot_config.botUsername = me.username
            await redis_instance.set('bot_username', me.username)
            sync_client_identity(client, me)
        except Exception as e:
            pass

        set_current_bot_id(bot_id)
        set_global_is_parent(is_parent)

        reset_bot_handlers(bot_id)

        inject_bot_data(client, bot_id, owner_id, redis_instance, bot_config, is_parent)

        if bot_id not in _bot_contexts:
            _bot_contexts[bot_id] = {}

        _bot_contexts[bot_id]['config'] = bot_config
        _bot_contexts[bot_id]['bot_id'] = bot_id
        _bot_contexts[bot_id]['owner_id'] = owner_id
        _bot_contexts[bot_id]['client'] = client
        _bot_contexts[bot_id]['redis'] = redis_instance
        _bot_contexts[bot_id]['is_parent'] = is_parent

        await redis_instance.set('bot_id', bot_id)
        await redis_instance.set('dev_final', bot_id)
        await redis_instance.set('is_parent', str(is_parent))

        if owner_id:
            await redis_instance.set(f'{owner_id}:rankDEV:{bot_id}', '1')
            await redis_instance.set(f'{bot_id}botowner', str(owner_id))
            await redis_instance.set('owner_id', str(owner_id))
            await redis_instance.set('owner_rank', 'DEV')

        try:
            me = await client.get_me()
            username = me.username
            await redis_instance.set('bot_username', username)
            if bot_config and hasattr(bot_config, 'botUsername'):
                bot_config.botUsername = username
            if bot_id in self.bots:
                self.bots[bot_id]['bot_username'] = username
            sync_client_identity(client, me)
        except Exception:
            pass

        if not hasattr(builtins, 'bot_instances'):
            builtins.bot_instances = {}
        builtins.bot_instances[bot_id] = {
            'client': client,
            'config': bot_config,
            'redis': redis_instance,
            'owner_id': owner_id,
            'dev_final': bot_id,
            'is_parent': is_parent
        }

        if not hasattr(builtins, 'bot_clients'):
            builtins.bot_clients = {}
        builtins.bot_clients[bot_id] = client

        router = _bot_contexts[bot_id].get('router')
        if router is None:
            router = Router(name=f"bot_{bot_id}_router")
            _bot_contexts[bot_id]['router'] = router
        dispatcher = _bot_contexts[bot_id].get('dispatcher')
        if dispatcher is None:
            dispatcher = Dispatcher()
            _bot_contexts[bot_id]['dispatcher'] = dispatcher

        try:
            if os.path.exists("plugins"):
                for file in os.listdir("plugins"):
                    if file.endswith(".py") and not file.startswith("__") and file != "FinalMusic":
                        module_name = file[:-3]
                        await self.load_module_isolated(f"plugins.{module_name}", bot_id, is_parent)

                plays_path = os.path.join("plugins", "games")
                if os.path.exists(plays_path):
                    for file in os.listdir(plays_path):
                        if file.endswith(".py") and not file.startswith("__"):
                            module_name = file[:-3]
                            await self.load_module_isolated(f"plugins.games.{module_name}", bot_id, is_parent)

                hasii_path = os.path.join("plugins", "FinalMusic")
                if os.path.exists(hasii_path):
                    cookies_source = os.path.join(hasii_path, "cookies")
                    cookies_dest = os.path.join(bot_config_dir, "cookies")

                    if os.path.exists(cookies_source):
                        try:
                            if os.path.exists(cookies_dest):
                                shutil.rmtree(cookies_dest)
                            shutil.copytree(cookies_source, cookies_dest)
                        except Exception:
                            pass
                    else:
                        os.makedirs(cookies_dest, exist_ok=True)

                    try:
                        set_current_bot_id(bot_id)
                        set_global_is_parent(is_parent)

                        hasii_module = await self.load_module_isolated("plugins.FinalMusic", bot_id, is_parent)

                        if hasii_module:
                            if hasattr(hasii_module, 'config'):
                                hasii_module.config.IS_PARENT = is_parent
                                hasii_module.config.Dev_FINAL = bot_id

                            try:
                                from plugins.FinalMusic.fm_plugins import all_modules
                            except Exception:
                                all_modules = []

                            for component in ["fm_core", "fm_helpers", "locales"]:
                                comp_path = os.path.join(hasii_path, component)
                                if os.path.exists(comp_path):
                                    for file in os.listdir(comp_path):
                                        if file.endswith(".py") and not file.startswith("__"):
                                            sub_module = file[:-3]
                                            await self.load_module_isolated(f"plugins.FinalMusic.{component}.{sub_module}", bot_id, is_parent)

                            for file in os.listdir(hasii_path):
                                if file.endswith(".py") and not file.startswith("__"):
                                    module_name = file[:-3]
                                    if module_name in ["fm_core", "fm_helpers", "fm_plugins", "locales"]:
                                        continue
                                    await self.load_module_isolated(f"plugins.FinalMusic.{module_name}", bot_id, is_parent)

                            for module in all_modules:
                                try:
                                    await self.load_module_isolated(f"plugins.FinalMusic.fm_plugins.{module}", bot_id, is_parent)
                                except Exception as e:
                                    print(f"Failed to load module {module}: {e}")

                            await self.initialize_bot_objects(bot_id, is_parent)

                    except Exception as e:
                        print(f"Error loading FinalMusic for bot {bot_id}: {e}")
                        import traceback
                        traceback.print_exc()

            for module_name, module in list(sys.modules.items()):
                if module_name.endswith(f"_{bot_id}"):
                    for attr_name in dir(module):
                        try:
                            obj = getattr(module, attr_name)
                        except Exception:
                            continue
                        if hasattr(obj, "handlers") and isinstance(obj.handlers, list):
                            try:
                                isolated_add_handlers(client, obj.handlers, bot_id)
                            except Exception as e:
                                print(f"Failed to add handlers from {module_name}: {e}")

            dispatcher.include_router(router)

        finally:
            if old_config:
                sys.modules['settings'] = old_config
            else:
                if 'config' in sys.modules:
                    del sys.modules['settings']

        return True

    async def _save_bot_data(self, bot_id: str, token: str, owner_id: int, days: int,
                             bot_username: str, is_parent: bool = False):
        r = RedisFake()

        from zoneinfo import ZoneInfo
        baghdad_tz = ZoneInfo('Asia/Baghdad')
        expiry_date = (datetime.now(baghdad_tz) + timedelta(days=days)).isoformat()

        bot_data = {
            'token': token,
            'owner_id': owner_id,
            'bot_id': bot_id,
            'bot_username': bot_username,
            'expiry_date': expiry_date,
            'days': days,
            'created_at': datetime.now(baghdad_tz).isoformat(),
            'is_parent': is_parent
        }

        # \u0627\u0644\u0625\u0635\u0644\u0627\u062d: \u0636\u0645 \u0627\u0644\u0631\u0645\u0632 \u0627\u0644\u062d\u0627\u0644\u064a (botkey) \u0625\u0644\u0649 \u0628\u064a\u0627\u0646\u0627\u062a \u0627\u0644\u0627\u0634\u062a\u0631\u0627\u0643
        # \u062d\u062a\u0649 \u064a\u064f\u0633\u062a\u0639\u0627\u062f \u0645\u0639 owner_id/bot_username \u0639\u0646\u062f \u0625\u0639\u0627\u062f\u0629 \u0627\u0644\u0625\u0642\u0644\u0627\u0639
        # (\u0646\u0641\u0633 \u0646\u0645\u0637 \u0627\u0633\u0645 \u0627\u0644\u0628\u0648\u062a \u0627\u0644\u0645\u0633\u062a\u0642\u0644).
        try:
            bot_r = RedisFake(bot_id=bot_id)
            saved_key = await bot_r.get(f'{bot_id}:botkey')
            if saved_key:
                bot_data['botkey'] = str(saved_key)
        except Exception:
            pass

        await r.hset('subscribed_bots', bot_id, json.dumps(bot_data))

        bot_r = RedisFake(bot_id=bot_id)
        await bot_r.hset('subscribed_bots', bot_id, json.dumps(bot_data))

    async def stop_bot(self, bot_id: str, delete_permanent: bool = False) -> tuple:
        async with self._get_bot_lock(bot_id):
            return await self._stop_bot_locked(bot_id, delete_permanent)

    async def _stop_bot_locked(self, bot_id: str, delete_permanent: bool = False) -> tuple:
        async with self._lock:
            if bot_id not in self.bots:
                return False, "Bot not found"

            bot_info = self.bots[bot_id]

            try:
                # إيقاف نظيف كامل للـ poller (stop_polling + إلغاء المهمة +
                # إغلاق الجلسة) — نفس الآلية المستخدمة في reload_bot، حتى لا
                # يبقى poller قديم يواصل getUpdates لنفس التوكن بعد إيقاف البوت.
                old_dispatcher = bot_info.get('dispatcher')
                old_bot = bot_info.get('aiogram_bot')
                old_task = self._polling_tasks.get(bot_id)
                await self._stop_polling_clean(bot_id, old_dispatcher, old_bot, task=old_task)

                if bot_info.get('assistant'):
                    try:
                        await assistant_manager.stop_assistant(bot_id)
                    except Exception:
                        pass

                del self.bots[bot_id]

                r_global = RedisFake()
                r_bot = RedisFake(bot_id=bot_id)

                await r_bot.hdel('subscribed_bots', bot_id)

                if delete_permanent:
                    await r_global.hdel('subscribed_bots', bot_id)

                    bot_dir = f"bots_data/{bot_id}"
                    if os.path.exists(bot_dir):
                        shutil.rmtree(bot_dir)

                    await r_bot.delete('owner_id')
                    await r_bot.delete('bot_id')
                    await r_bot.delete('dev_final')
                    await r_bot.delete('is_parent')

                    async for key in r_bot.scan_iter(match='*', count=100):
                        await r_bot.delete(key)

                if hasattr(builtins, 'bot_instances') and bot_id in builtins.bot_instances:
                    del builtins.bot_instances[bot_id]

                if hasattr(builtins, 'bot_clients') and bot_id in builtins.bot_clients:
                    del builtins.bot_clients[bot_id]

                if bot_id in _bot_contexts:
                    del _bot_contexts[bot_id]

                return True, f"Bot {bot_id} stopped" + (" and deleted permanently" if delete_permanent else "")
            except Exception as e:
                return False, f"Failed to stop bot: {str(e)}"

    def get_status(self) -> dict:
        status = {
            'total_bots': len(self.bots),
            'total_clusters': len(self.clusters),
            'bots': {},
            'clusters': {}
        }

        for bot_id, info in self.bots.items():
            status['bots'][bot_id] = {
                'owner': info.get('owner_id'),
                'cluster': info.get('cluster_id'),
                'status': info.get('status', 'running'),
                'started': time.ctime(info.get('started_at', time.time())),
                'is_parent': info.get('is_parent', False),
                'bot_username': info.get('bot_username', 'unknown')
            }

        for cluster_id in self.clusters:
            bots_in_cluster = [b for b in self.bots.values() if b.get('cluster_id') == cluster_id]
            status['clusters'][cluster_id] = {
                'bots_count': len(bots_in_cluster),
                'max_bots': self.MAX_BOTS_PER_CLUSTER,
                'bots': [bid for bid, info in self.bots.items() if info.get('cluster_id') == cluster_id]
            }

        return status

    async def _isolate_bot_data(self, bot_id: str):
        try:
            bot_r = RedisFake(bot_id=bot_id)

            existing_data = await bot_r.hget('subscribed_bots', bot_id)
            if existing_data:
                # \u0627\u0644\u0625\u0635\u0644\u0627\u062d: \u0625\u0639\u0627\u062f\u0629 \u0643\u062a\u0627\u0628\u0629 \u0627\u0644\u0631\u0645\u0632 \u0627\u0644\u0645\u062d\u0641\u0648\u0638
                # (botkey) \u0625\u0630\u0627 \u0643\u0627\u0646 \u0645\u062e\u0632\u0646\u0627\u064b \u0641\u064a \u0628\u064a\u0627\u0646\u0627\u062a \u0627\u0644\u0627\u0634\u062a\u0631\u0627\u0643\u060c
                # \u062d\u062a\u0649 \u0644\u0627 \u064a\u0641\u0642\u062f \u0627\u0644\u0628\u0648\u062a \u0631\u0645\u0632\u0647 \u0628\u0639\u062f \u0625\u0639\u0627\u062f\u0629 \u0627\u0644\u0625\u0642\u0644\u0627\u0639.
                try:
                    existing_data_dict = json.loads(existing_data)
                except Exception:
                    existing_data_dict = {}
                saved_key = existing_data_dict.get('botkey')
                if saved_key:
                    await bot_r.set(f'{bot_id}:botkey', str(saved_key))
                return True

            from zoneinfo import ZoneInfo
            baghdad_tz = ZoneInfo('Asia/Baghdad')
            expiry_date = (datetime.now(baghdad_tz) + timedelta(days=30)).isoformat()

            await bot_r.hset('subscribed_bots', bot_id, json.dumps({
                'bot_id': bot_id,
                'created_at': datetime.now(baghdad_tz).isoformat(),
                'expiry_date': expiry_date,
                'days': 30,
                'is_isolated': True,
                'is_parent': False
            }))

            await bot_r.sadd(f'enablelist:{bot_id}', 'init')
            await bot_r.srem(f'enablelist:{bot_id}', 'init')

            await bot_r.sadd(f'{bot_id}:UsersList', 'init')
            await bot_r.srem(f'{bot_id}:UsersList', 'init')

            await bot_r.sadd(f'{bot_id}DEV2', 'init')
            await bot_r.srem(f'{bot_id}DEV2', 'init')

            # \u0627\u0644\u0625\u0635\u0644\u0627\u062d: \u0644\u0627 \u0646\u0643\u062a\u0628 \u0641\u0648\u0642 \u0642\u064a\u0645\u0629 botkey \u0627\u0644\u0645\u0648\u062c\u0648\u062f\u0629 \u0645\u0633\u0628\u0642\u0627\u064b
            # (set nx) \u2014 \u062a\u064f\u062d\u0641\u064e\u0638 \u0642\u064a\u0645\u0629 \u0627\u0644\u0645\u0637\u0648\u0651\u0631 \u0625\u0646 \u0648\u062c\u062f\u062a\u060c \u0648\u064a\u064f\u0643\u062a\u0628
            # \u0627\u0644\u0627\u0641\u062a\u0631\u0627\u0636\u064a '\u21dc' \u0641\u0642\u0637 \u0639\u0646\u062f \u063a\u064a\u0627\u0628 \u0627\u0644\u0645\u0641\u062a\u0627\u062d.
            await bot_r.set(f'{bot_id}:botkey', '\u21dc', nx=True)
            await bot_r.set(f'{bot_id}:BotName', '\u0641\u0627\u064a\u0641\u0644', nx=True)
            await bot_r.set(f'{bot_id}:BotChannel', 'i0i0ii')

            return True

        except Exception as e:
            print(f"Error isolating bot data for {bot_id}: {e}")
            return False


bot_manager = BotClusterManager()