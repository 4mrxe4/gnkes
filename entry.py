import html
import sys
import shutil

from helpers import redis
sys.modules['redis'] = redis
sys.modules['redis.asyncio'] = redis
sys.modules['redis_helper'] = redis

import time
import os
import json
import re
import asyncio
import importlib
import builtins

from aiogram import Bot as AioBot, Dispatcher, Router, F
from aiogram.enums import ParseMode as AioParseMode
from aiogram.client.default import DefaultBotProperties

from compat import CompatClient
from compat import filters as compat_filters
from compat import (
    MessageHandler,
    StopPropagation,
    ContinuePropagation,
    _HandlerSpec,
    collect_handlers,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from dotenv import load_dotenv
from cluster import bot_manager
from datetime import datetime
from zoneinfo import ZoneInfo
from helpers.context import (
    set_current_bot_id,
    update_global_context_sync,
    inject_bot_data,
    isolated_add_handlers,
    set_global_is_parent,
    _bot_contexts,
    sync_client_identity,
    FilteredList,
    FilteredSet,
    get_current_user_id,
)
from helpers.redis import RedisFake
from helpers.assistant import assistant_manager

from compat import Client

Client.bl_users = set()

load_dotenv()
if sys.platform != "win32":
    try:
        import resource
        _soft, _hard = resource.getrlimit(resource.RLIMIT_NOFILE)
        _target = min(65536, _hard)
        if _soft < _target:
            resource.setrlimit(resource.RLIMIT_NOFILE, (_target, _hard))
    except Exception:
        pass

current_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, current_dir)

API_ID = int(os.getenv("API_ID", "29914850"))
API_HASH = os.getenv("API_HASH", "de7b0ee6f49fff7b4a5f0e5c015972ce")
token = os.getenv("BOT_TOKEN")
owner_id = int(os.getenv("OWNER_ID", "0"))
LOGGER_ID = int(os.getenv("LOGGER_ID", "-1002926122970"))
MONGO_URL = os.getenv("MONGO_DB_URI", "")
ARCHIVE_CHANNEL = int(os.getenv("ARCHIVE_CHANNEL", "-1001828975467"))
DURATION_LIMIT = int(os.getenv("DURATION_LIMIT", "300")) * 60
QUEUE_LIMIT = int(os.getenv("QUEUE_LIMIT", "30"))
PLAYLIST_LIMIT = int(os.getenv("PLAYLIST_LIMIT", "20"))
SUPPORT_CHANNEL = os.getenv("SUPPORT_CHANNEL", "https://t.me/BBBZZZB")
SUPPORT_CHAT = os.getenv("SUPPORT_CHAT", "https://t.me/Z3ZZ_Z0")
SESSION1 = os.getenv("STRING_SESSION", "")
SESSION2 = os.getenv("STRING_SESSION2", "")
SESSION3 = os.getenv("STRING_SESSION3", "")
COOKIES_URL = os.getenv("COOKIE_URL", "").split()
EXCLUDED_USERNAMES = os.getenv("EXCLUDED_USERNAMES", "").split()
USERHASH = os.getenv("USERHASH", "3d9ce4bdd60daae777c186ff7")

if not token or owner_id == 0:
    print("Error: BOT_TOKEN and OWNER_ID must be set in .env file")
    sys.exit(1)

Dev_FINAL = token.split(':')[0]
main_bot_dir = f"bots_data/{Dev_FINAL}"
os.makedirs(main_bot_dir, exist_ok=True)
if main_bot_dir not in sys.path:
    sys.path.insert(0, main_bot_dir)

config_path = os.path.join(main_bot_dir, "settings.py")
config_exists = os.path.exists(config_path)

if config_exists:
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()

        session1_match = re.search(r'SESSION1 = "(.*?)"', content)
        session2_match = re.search(r'SESSION2 = "(.*?)"', content)
        session3_match = re.search(r'SESSION3 = "(.*?)"', content)

        if session1_match:
            SESSION1 = session1_match.group(1)
        if session2_match:
            SESSION2 = session2_match.group(1)
        if session3_match:
            SESSION3 = session3_match.group(1)
    except Exception as e:
        print(f"Failed to read existing config: {e}")

if not config_exists:
    to_config = f"""# settings.py - for main bot {Dev_FINAL}
import sys
from helpers import redis
sys.modules['redis.asyncio'] = redis
sys.modules['redis'] = redis
import os
from os import getenv
from typing import List
from dotenv import load_dotenv
load_dotenv()
Dev_FINAL = "{Dev_FINAL}"
TOKEN = "{token}"
OWNER_ID = {owner_id}
API_ID = {API_ID}
API_HASH = "{API_HASH}"
LOGGER_ID = {LOGGER_ID}
botUsername = None
SESSION1 = "{SESSION1}"
SESSION2 = "{SESSION2}"
SESSION3 = "{SESSION3}"
SUPPORT_CHANNEL = "{SUPPORT_CHANNEL}"
SUPPORT_CHAT = "{SUPPORT_CHAT}"
MONGO_URL = "{MONGO_URL}"
ARCHIVE_CHANNEL = {ARCHIVE_CHANNEL}
DURATION_LIMIT = {DURATION_LIMIT}
QUEUE_LIMIT = {QUEUE_LIMIT}
PLAYLIST_LIMIT = {PLAYLIST_LIMIT}
COOKIES_URL = {COOKIES_URL}
EXCLUDED_USERNAMES = {EXCLUDED_USERNAMES}
USERHASH = "{USERHASH}"
IS_PARENT = True
from helpers.redis import RedisFake
r = RedisFake(bot_id=Dev_FINAL)
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
    'config', 'r', 'RedisFake', 'IS_PARENT'
]
"""
    with open(config_path, 'w+', encoding='utf-8') as w:
        w.write(to_config)

import settings

aiogram_bot = AioBot(token=token, default=DefaultBotProperties(parse_mode=AioParseMode.HTML))
dispatcher = Dispatcher()
main_router = Router(name="main_bot_router")

app = CompatClient(
    aiogram_bot,
    bot_id=Dev_FINAL,
    bot_token=token,
    owner_id=owner_id,
    redis=settings.r,
    config=settings.config,
    is_parent=True,
)
app.bot = aiogram_bot
app.sudoers = FilteredSet()
app.bl_users = FilteredList()

builtins.unified_app_client = app
builtins.RedisFake = RedisFake

import inspect

from compat import MessageEntityType as AioMessageEntityType
from aiogram.types import Message as AioMessage, ChatMember as AioChatMember

from helpers.gender import genderize_text
from helpers.emoji import inject_custom_emojis, inject_custom_emojis_sync


class FakeUser:
    """محاكاة from_user للرسائل القادمة من القنوات (مثل الأصل)."""

    def __init__(self, chat_obj):
        self.id = chat_obj.id
        self.is_bot = False
        self.first_name = getattr(chat_obj, 'title', None) or getattr(chat_obj, 'first_name', None) or "Channel"
        self.last_name = getattr(chat_obj, 'last_name', "") or ""
        self.username = getattr(chat_obj, 'username', None) or "NoUsername"
        self.language_code = "ar"
        self.status = "offline"

    def mention(self, name=None, style=None):
        target_name = name if name else self.first_name
        if self.username and self.username != "NoUsername":
            return f"<a href='https://t.me/{self.username}'>{html.escape(str(target_name))}</a>"
        return f"<a href='tg://user?id={self.id}'>{html.escape(str(target_name))}</a>"


_original_bot_call = AioBot.__call__

# كاش داخلي (in-memory) لقوائم أدمنية المجموعات — get_chat_administrators
# كان يُستدعى حيًا من تيليجرام في كل أمر تحقق صلاحية (وجدنا 9 مواضع مختلفة
# في plugins/ تستدعيها لكل رسالة تقريبًا)، رغم أن قائمة الأدمن نادرًا ما
# تتغيّر خلال دقائق. الكاش هنا في الذاكرة (وليس Redis) عمداً لأن القيمة
# المرجعة كائنات aiogram معقدة (ChatMember)، وتخزينها هنا بنفس نوعها الحي
# أضمن وأبسط من تسلسلها JSON ثم إعادة بنائها — بلا أي مخاطرة على المنطق
# القائم في compat.py الذي يتوقع هذه الكائنات كما هي.
# TTL قصير (90 ثانية) كافٍ لإلغاء التكرار أثناء نشاط المستخدم العادي مع
# بقاء البيانات حديثة بما يكفي عمليًا.
_admin_cache: dict = {}
_ADMIN_CACHE_TTL = 90


async def _patched_bot_call(self, method, request_timeout=None):
    method_name = type(method).__name__
    if method_name == "GetChatAdministrators":
        cache_key = (id(self), getattr(method, "chat_id", None))
        cached = _admin_cache.get(cache_key)
        if cached is not None:
            ts, result = cached
            if time.time() - ts < _ADMIN_CACHE_TTL:
                return result
        result = await _original_bot_call(self, method, request_timeout=request_timeout)
        _admin_cache[cache_key] = (time.time(), result)
        return result

    try:
        user_id = get_current_user_id()
        for field in ("text", "caption"):
            if hasattr(method, field):
                val = getattr(method, field)
                if isinstance(val, str) and val:
                    new_val = val
                    if user_id is not None:
                        try:
                            new_val = await genderize_text(new_val, user_id)
                        except Exception as ge:
                            print(f"[تحديد جنسي] فشل التحويل: {ge}")
                    new_val = inject_custom_emojis_sync(new_val)
                    if new_val != val:
                        setattr(method, field, new_val)
                        if not getattr(method, "parse_mode", None):
                            setattr(method, "parse_mode", AioParseMode.HTML)
    except Exception as e:
        print(f"[ايموجي مميز] فشل الحقن: {e}")
    return await _original_bot_call(self, method, request_timeout=request_timeout)


AioBot.__call__ = _patched_bot_call



async def register_main_bot():
    main_bot_id = token.split(':')[0]
    set_current_bot_id(main_bot_id)
    set_global_is_parent(True)
    cluster_id = bot_manager.get_or_create_cluster()
    bot_manager.bots[main_bot_id] = {
        'client': app,
        'aiogram_bot': aiogram_bot,
        'dispatcher': dispatcher,
        'router': main_router,
        'loop': asyncio.get_event_loop(),
        'cluster_id': cluster_id,
        'owner_id': owner_id,
        'token': token,
        'started_at': time.time(),
        'expiry': time.time() + (365 * 86400),
        'status': 'running',
        'is_parent': True
    }


async def restore_sub_bots():
    r = RedisFake()
    all_bots = await r.hgetall('subscribed_bots')

    if not all_bots:
        print("No subscribed bots found")
        return

    print(f"Restoring {len(all_bots)} sub bots...")

    for bot_id, data in all_bots.items():
        try:
            if bot_id in bot_manager.bots:
                bot_info = bot_manager.bots[bot_id]
                if bot_info.get('status') == 'running':
                    print(f"Bot {bot_id} already running, skipping")
                    continue

            bot_info = json.loads(data)
            token_ = bot_info.get('token')

            if not token_:
                print(f"Bot {bot_id} has no token")
                continue

            expiry = datetime.fromisoformat(bot_info['expiry_date'])
            if expiry.tzinfo is None:
                expiry = expiry.replace(tzinfo=ZoneInfo('Asia/Baghdad'))
            if expiry < datetime.now(ZoneInfo('Asia/Baghdad')):
                print(f"Bot {bot_id} expired, skipping")
                await r.hdel('subscribed_bots', bot_id)
                continue

            success, message = await bot_manager.start_isolated_bot(bot_id, token_, is_parent=False)

            if success:
                print(f"Restored bot {bot_id}")
            else:
                print(f"Failed to restore bot {bot_id}: {message}")

        except Exception as e:
            print(f"Error restoring bot {bot_id}: {e}")



def load_plugin_handlers_to_router(router: Router, bot_id: str):
    """يجمع handlers من الوحدات المحملة (obj.handlers) ويسجلها على router.

    - main bot: الوحدات المحملة عبر importlib (plugins.*)
    - sub bots: الوحدات المعزولة (module_{bot_id})
    """
    seen = set()
    for module_name, module in list(sys.modules.items()):
        if not module_name.startswith("plugins"):
            continue
        if module_name.endswith(f"_{bot_id}"):
            pass
        elif not bot_id:
            continue

        for attr_name in dir(module):
            if attr_name.startswith("__") and attr_name.endswith("__"):
                continue
            try:
                obj = getattr(module, attr_name)
            except Exception:
                continue
            if hasattr(obj, "handlers") and isinstance(obj.handlers, list):
                key = id(obj)
                if key in seen:
                    continue
                seen.add(key)
                try:
                    isolated_add_handlers(None, obj.handlers, bot_id)
                except Exception as e:
                    print(f"Failed to add handlers from {module_name}.{attr_name}: {e}")


async def start_unified_bot():
    from helpers.redis import redis_healthcheck, migrate_lmdb_to_redis

    ok, msg = await redis_healthcheck()
    print(f"[redis] {msg}")
    if not ok:
        print("[redis] تعذر الاتصال بـ Redis. تأكد من متغير البيئة REDIS_URL "
              "(مثال: redis://127.0.0.1:6379/0) ومن أن خادم Redis يعمل، ثم أعد التشغيل.")
        sys.exit(1)

    migration_stats = await migrate_lmdb_to_redis()
    if migration_stats.get("ran"):
        print(f"[redis] نتيجة ترحيل LMDB: {migration_stats}")

    set_current_bot_id(Dev_FINAL)
    set_global_is_parent(True)
    parent_redis = RedisFake(bot_id=Dev_FINAL)

    inject_bot_data(app, Dev_FINAL, owner_id, parent_redis, settings.config, is_parent=True)
    _bot_contexts[Dev_FINAL] = {
        'config': settings.config,
        'bot_id': Dev_FINAL,
        'owner_id': owner_id,
        'client': app,
        'aiogram_bot': aiogram_bot,
        'dispatcher': dispatcher,
        'router': main_router,
        'redis': parent_redis,
        'is_parent': True
    }

    # الإصلاح (قديم، غير كافٍ): كان يُستدعى _ensure_bootstrap_context() هنا
    # مباشرة، قبل اكتمال register_main_bot() (أي قبل أن يكون app/aiogram_bot
    # جاهزين فعلياً)، ومغلّفاً بـ try/except يبتلع أي استثناء بصمت (مثلاً لو
    # فشل بناء Userbot() لأن جلسة Pyrogram لم تكن جاهزة بعد في هذه اللحظة
    # المبكرة). عند فشله بصمت، تبقى _bot_contexts[Dev_FINAL] بلا مفاتيح
    # queue/tune/yt/tg/userbot، فيفشل تشغيل/تحميل الصوت للبوت الأب تحديداً
    # (بينما الأبناء يحصلون على تهيئة موثوقة عبر bot_manager.initialize_bot_objects
    # في cluster.py). الإصلاح الفعلي: تأجيل هذا الاستدعاء لما بعد
    # register_main_bot() (بعد أن يصبح كل شيء جاهزاً)، واستخدام نفس آلية
    # bot_manager.initialize_bot_objects الموثوقة المستخدمة مع الأبناء، مع طباعة
    # الاستثناء كاملاً بدل ابتلاعه بصمت.
    await register_main_bot()

    # ===== الإصلاح 2: إزالة التهيئة المبكرة للموسيقى =====
    # كانت الكتلة التالية تبني كائنات الموسيقى فقط (queue/tune/yt/...) بدون
    # تسجيل أي handlers، فتبقى _bot_contexts[Dev_FINAL] سياقاً ناقصاً.
    # الآن تُهيَّأ الكائنات + handlers معاً عبر كتلة hasii_path الموحدة
    # (نفس مسار الأبناء في cluster.py) في موضع لاحق من هذه الدالة.
    r = RedisFake()
    all_bots = await r.hgetall('subscribed_bots')
    expired_bots = []

    for bot_id_, data in all_bots.items():
        try:
            bot_info = json.loads(data)
            expiry = datetime.fromisoformat(bot_info['expiry_date'])
            if expiry.tzinfo is None:
                expiry = expiry.replace(tzinfo=ZoneInfo('Asia/Baghdad'))
            if expiry < datetime.now(ZoneInfo('Asia/Baghdad')):
                expired_bots.append(bot_id_)
                await r.hdel('subscribed_bots', bot_id_)
                bot_r = RedisFake(bot_id=bot_id_)
                await bot_r.hdel('subscribed_bots', bot_id_)
                bot_dir = f"bots_data/{bot_id_}"
                if os.path.exists(bot_dir):
                    import shutil
                    shutil.rmtree(bot_dir)
        except Exception:
            pass

    await restore_sub_bots()

    # \u0627\u0644\u0625\u0635\u0644\u0627\u062d: \u0643\u062a\u0627\u0628\u0629 \u0634\u0631\u0637\u064a\u0629 (\u0644\u0627 \u0646\u0643\u062a\u0628 \u0641\u0648\u0642 \u0642\u064a\u0645\u0629 \u0645\u0648\u062c\u0648\u062f\u0629)
    # \u062d\u062a\u0649 \u0644\u0627 \u0646\u064f\u0645\u0633\u062d \u0631\u0645\u0632 \u0627\u0644\u0633\u0648\u0631\u0633 \u0627\u0644\u0630\u064a \u0639\u064a\u0651\u0646\u0647 \u0627\u0644\u0645\u0637\u0648\u0651\u0631 \u0633\u0627\u0628\u0642\u0627\u064b.
    if not await r.get(f'{Dev_FINAL}:botkey'):
        await r.set(f'{Dev_FINAL}:botkey', '\u21dc', nx=True)
    if not await r.get(f'{Dev_FINAL}botname'):
        await r.set(f'{Dev_FINAL}botname', 'فاينل')
    if not await r.get(f'{Dev_FINAL}botchannel'):
        await r.set(f'{Dev_FINAL}botchannel', 'eFFb0t')

    from helpers.channel_init import init_channel_handling
    await init_channel_handling()

    set_current_bot_id(Dev_FINAL)
    set_global_is_parent(True)

    try:
        me = await aiogram_bot.get_me()
        username = me.username or ""
        settings.config.botUsername = username
        sync_client_identity(app, me)
        builtins.botUsername = username
    except Exception:
        pass

    set_current_bot_id(Dev_FINAL)
    set_global_is_parent(True)

    if os.path.exists("plugins"):
        for file in os.listdir("plugins"):
            if file.endswith(".py") and not file.startswith("__") and file != "FinalMusic":
                module_name = file[:-3]
                try:
                    set_current_bot_id(Dev_FINAL)
                    update_global_context_sync()
                    mod = importlib.import_module(f"plugins.{module_name}")
                    for name in dir(mod):
                        obj = getattr(mod, name)
                        if hasattr(obj, "handlers") and isinstance(obj.handlers, list):
                            isolated_add_handlers(None, obj.handlers, Dev_FINAL)
                except Exception as e:
                    print(f"Failed to load {module_name} from plugins: {e}")

        plays_path = os.path.join("plugins", "games")
        if os.path.exists(plays_path):
            for file in os.listdir(plays_path):
                if file.endswith(".py") and not file.startswith("__"):
                    module_name = file[:-3]
                    try:
                        set_current_bot_id(Dev_FINAL)
                        update_global_context_sync()
                        mod = importlib.import_module(f"plugins.games.{module_name}")
                        for name in dir(mod):
                            obj = getattr(mod, name)
                            if hasattr(obj, "handlers") and isinstance(obj.handlers, list):
                                isolated_add_handlers(None, obj.handlers, Dev_FINAL)
                    except Exception as e:
                        print(f"Failed to load game {module_name}: {e}")

        # ===== \u0627\u0644\u0625\u0635\u0644\u0627\u062d 2: \u062a\u0648\u062d\u064a\u062f \u0645\u0633\u0627\u0631 \u062a\u062d\u0645\u064a\u0644 FinalMusic \u0644\u0644\u0628\u0648\u062a \u0627\u0644\u0623\u0628 =====
        # \u0633\u0627\u0628\u0642\u0627\u064b \u0643\u0627\u0646\u062a \u0627\u0644\u062d\u0644\u0642\u0629 \u0627\u0644\u064a\u062f\u0648\u064a\u0629 \u062a\u0633\u062a\u062b\u0646\u064a \u0645\u062c\u0644\u062f FinalMusic \u0648\u0645\u0643\u0648\u0646\u0627\u062a\u0647
        # (fm_core/fm_helpers/fm_plugins/locales) \u0641\u064a \u0645\u0633\u0627\u0631 \u0627\u0644\u0623\u0628\u060c \u0644\u0630\u0627 \u0643\u0627\u0646\u062a
        # \u0627\u0644\u0645\u0648\u0633\u064a\u0642\u0649 \u062a\u0639\u0645\u0644 \u0641\u064a \u0627\u0644\u0623\u0628\u0646\u0627\u0621 \u0641\u0642\u0637.
        # \u0627\u0644\u0622\u0646 \u0646\u0633\u062a\u062e\u062f\u0645 \u0646\u0641\u0633 \u0643\u062a\u0644\u0629 hasii_path \u0645\u0646 cluster.py
        # (load_module_isolated + isolated_add_handlers + initialize_bot_objects)
        # \u062d\u062a\u0649 \u064a\u062d\u0635\u0644 \u0627\u0644\u0623\u0628 \u0639\u0644\u0649 handlers \u0645\u0648\u0633\u064a\u0642\u064a\u0629 \u0643\u0627\u0645\u0644\u0629
        # \u0645\u0639\u0632\u0648\u0644\u0629 \u0628\u0646\u0641\u0633 \u0637\u0631\u064a\u0642\u0629 \u0627\u0644\u0623\u0628\u0646\u0627\u0621.
        hasii_path = os.path.join("plugins", "FinalMusic")
        if os.path.exists(hasii_path):
            bot_config_dir = f"bots_data/{Dev_FINAL}"
            cookies_source = os.path.join(hasii_path, "cookies")
            cookies_dest = os.path.join(bot_config_dir, "cookies")
            try:
                if os.path.exists(cookies_source):
                    if os.path.exists(cookies_dest):
                        shutil.rmtree(cookies_dest)
                    shutil.copytree(cookies_source, cookies_dest)
                else:
                    os.makedirs(cookies_dest, exist_ok=True)
            except Exception:
                pass

            try:
                set_current_bot_id(Dev_FINAL)
                set_global_is_parent(True)

                hasii_module = await bot_manager.load_module_isolated("plugins.FinalMusic", Dev_FINAL, True)

                if hasii_module:
                    if hasattr(hasii_module, 'config'):
                        hasii_module.config.IS_PARENT = True
                        hasii_module.config.Dev_FINAL = Dev_FINAL

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
                                    await bot_manager.load_module_isolated(f"plugins.FinalMusic.{component}.{sub_module}", Dev_FINAL, True)

                    for file in os.listdir(hasii_path):
                        if file.endswith(".py") and not file.startswith("__"):
                            module_name = file[:-3]
                            if module_name in ["fm_core", "fm_helpers", "fm_plugins", "locales"]:
                                continue
                            await bot_manager.load_module_isolated(f"plugins.FinalMusic.{module_name}", Dev_FINAL, True)

                    for module in all_modules:
                        try:
                            await bot_manager.load_module_isolated(f"plugins.FinalMusic.fm_plugins.{module}", Dev_FINAL, True)
                        except Exception as e:
                            print(f"Failed to load module {module}: {e}")

                    await bot_manager.initialize_bot_objects(Dev_FINAL, True)

                    for module_name, module in list(sys.modules.items()):
                        if module_name.endswith(f"_{Dev_FINAL}"):
                            for attr_name in dir(module):
                                try:
                                    obj = getattr(module, attr_name)
                                except Exception:
                                    continue
                                if hasattr(obj, "handlers") and isinstance(obj.handlers, list):
                                    try:
                                        isolated_add_handlers(None, obj.handlers, Dev_FINAL)
                                    except Exception as e:
                                        print(f"Failed to add handlers from {module_name}: {e}")
            except Exception as e:
                print(f"Error loading FinalMusic for main bot {Dev_FINAL}: {e}")
                import traceback
                traceback.print_exc()

    r2 = RedisFake(bot_id=Dev_FINAL)
    app.owner = owner_id
    sudoers_list = await r2.smembers(f"sudoers:{Dev_FINAL}")
    if not sudoers_list:
        sudoers_list = [str(owner_id)]
    elif str(owner_id) not in sudoers_list:
        sudoers_list.append(str(owner_id))
    app.sudoers = FilteredSet([int(s) for s in sudoers_list])
    app.sudo_filter = compat_filters.user(list(app.sudoers))
    blacklisted_users = await r2.smembers(f"blacklist_users:{Dev_FINAL}")
    app.bl_users = FilteredList([int(b) for b in blacklisted_users]) if blacklisted_users else FilteredList()

    dispatcher.include_router(main_router)

    print('Unified Bot started successfully')

    # تسخين عميل Pyrogram المشترك (لحل يوزرنيمات @user) فور الإقلاع بدل
    # الانتظار حتى أول أمر يحتاجه فعلياً — هذا الأمر كان سابقاً يدفع أول
    # مستخدم يستخدم أمراً بيوزرنيم إلى الانتظار لحين اكتمال عملية تسجيل
    # دخول MTProto كاملة. لا يوقف الإقلاع إن فشل (مهمة خلفية معزولة).
    async def _warmup_shared_pyro_client():
        try:
            from plugins.FinalMusic.fm_core.l1_cache import get_bot_pyro_client
            await get_bot_pyro_client()
        except Exception as e:
            print(f"[Boot] تعذّر تسخين عميل Pyrogram المشترك: {e}")

    asyncio.create_task(_warmup_shared_pyro_client())

    r3 = RedisFake(bot_id=Dev_FINAL)
    if await r3.get(f'DevGroup:{Dev_FINAL}'):
        try:
            await app.send_message(int((await r3.get(f'DevGroup:{Dev_FINAL}')) or 0), "Unified bot started successfully")
        except Exception:
            pass

    # الإصلاح الجذري لمشكلة "تحديث البوت" على البوت الأب (Conflict متكرر
    # بلا توقف):
    #
    # سابقاً كان الـ polling للبوت الأب يُشغَّل هنا مباشرة بـ
    # `await dispatcher.start_polling(...)` كمهمة غير مسجَّلة في
    # bot_manager._polling_tasks. لكن register_main_bot() يسجّل هذا البوت في
    # bot_manager.bots، فيصبح مؤهلاً لزر "تحديث البوت" الذي يستدعي
    # cluster.reload_bot(bot_id). داخل reload_bot، يحاول الكود إيقاف الـ
    # poller القديم عبر `self._polling_tasks.pop(bot_id, None)` — لكن بما أن
    # poller البوت الأب لم يكن مسجَّلاً هناك أصلاً، لم يكن يُلغى أبداً؛ فقط
    # جلسته (session) تُغلق. جلسة aiogram المغلقة تُعاد فتحها تلقائياً عند أول
    # طلب get_updates تالٍ، فيستمر الـ poller القديم بالعمل فعلياً إلى الأبد،
    # بينما ينشئ reload_bot poller جديداً كلياً لنفس التوكن. ينتج عن هذا
    # عمليتا getUpdates دائمتان لنفس البوت في آن واحد، فتتصادمان مع بعضهما
    # على مستوى تيليجرام إلى ما لا نهاية (TelegramConflictError متكرر بلا
    # توقف ذاتي) — بخلاف الأبناء، الذين يعمل تحديثهم بلا مشاكل لأن pollerهم
    # مسجَّل بشكل صحيح في _polling_tasks منذ البداية عبر _start_bot_locked.
    #
    # الحل: تشغيل poller البوت الأب عبر نفس الآلية المُتّبعة مع الأبناء
    # (bot_manager._run_bot_polling) وتسجيله في bot_manager._polling_tasks
    # فور إنشائه، بحيث يرى reload_bot المهمة الحقيقية ويستطيع إلغاءها فعلياً
    # قبل بدء أي poller جديد. بعدها، ننتظر المهمة المسجَّلة ضمن حلقة: إذا
    # استبدلها reload_bot بمهمة جديدة (بعد إعادة تحميل ناجحة) نتابع انتظار
    # المهمة الجديدة بدل الخروج من الدالة (والذي كان سيُنهي asyncio.run()
    # بأكمله ويوقف كل بوتات الكلاستر، أبناءً وأباً).
    loop = asyncio.get_running_loop()
    initial_task = loop.create_task(bot_manager._run_bot_polling(Dev_FINAL, aiogram_bot, dispatcher))
    bot_manager._polling_tasks[Dev_FINAL] = initial_task

    current_task = initial_task
    while True:
        try:
            await current_task
        except asyncio.CancelledError:
            pass
        except Exception as e:
            print(f"Polling error: {e}")
            import traceback
            traceback.print_exc()

        tracked_task = bot_manager._polling_tasks.get(Dev_FINAL)
        if tracked_task is None or tracked_task is current_task:
            # لم يستبدل reload_bot المهمة بأخرى جديدة، أي أن التوقف هنا
            # ليس نتيجة "تحديث البوت" بل توقف حقيقي غير متوقع — لا داعٍ
            # للاستمرار في الانتظار.
            break
        current_task = tracked_task


if __name__ == "__main__":
    try:
        asyncio.run(start_unified_bot())
    except KeyboardInterrupt:
        print("Bot stopped by user")