# plugins/FinalMusic/__init__.py
# Music module integrated into botm_unified.
# All context objects come from the PARENT system (helpers.context) so music
# shares the same cluster/bot isolation, Redis, ranks and lifecycle as every
# other part of botm_unified. No separate cluster / bot / event loop is created.

import asyncio
import logging
import os
import sys
import time
from logging.handlers import RotatingFileHandler
from typing import List

from helpers.context import (
    get_config,
    get_bot_client,
    get_bot_context,
    get_current_bot_id,
    set_current_bot_id,
    get_global_is_parent,
    _bot_contexts,
    redis_proxy,
    config_proxy,
    app_proxy,
    queue_proxy,
    tune_proxy,
    yt_proxy,
    tg_proxy,
    preload_proxy,
    userbot_proxy,
    dev_final_proxy,
    k_proxy,
    get_queue,
    get_tune,
    get_yt,
    get_tg,
    get_preload,
    get_userbot,
)

logging.basicConfig(
    format="[%(asctime)s - %(levelname)s] - %(name)s: %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler("log.txt", maxBytes=10485760, backupCount=5),
        logging.StreamHandler(),
    ],
    level=logging.ERROR,  # الإصلاح: كان INFO فيطبع كل حدث/تحديث (aiogram.event،
                          # aiogram.dispatcher، وكل استدعاء logger.info بأي
                          # مكان بالمشروع). المطلوب فقط أخطاء (ERROR/CRITICAL).
)
logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("ntgcalls").setLevel(logging.CRITICAL)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("pytgcalls").setLevel(logging.ERROR)
logger = logging.getLogger("FinalMusic")

tasks: List = []
boot: float = time.time()

r = redis_proxy
Dev_FINAL = dev_final_proxy
k = k_proxy
config = config_proxy
app = app_proxy
queue = queue_proxy
tune = tune_proxy
yt = yt_proxy
tg = tg_proxy
preload = preload_proxy
userbot = userbot_proxy

# Real music components (rebuilt under the parent architecture)
from .fm_core.userbot import Userbot
from .fm_core.lang import Language
from .fm_core.telegram import Telegram
from .fm_core.youtube import YouTube
from .fm_core.preload import PreloadManager
from .fm_helpers import Queue, Media, Track, buttons, thumb, utils
from .fm_core.calls import TgCall
from .fm_core.dir import ensure_dirs


def _ensure_bootstrap_context() -> dict:
    """Ensure the current bot context has all music service objects wired to
    the parent _bot_contexts registry (per bot_id isolation)."""
    bot_id = get_current_bot_id()
    if bot_id is None:
        try:
            import settings as _bare_config
            _dev = getattr(_bare_config, "Dev_FINAL", None)
            if _dev is not None:
                bot_id = str(_dev)
                set_current_bot_id(bot_id)
            else:
                bot_id = "__standalone__"
                set_current_bot_id(bot_id)
        except Exception:
            bot_id = "__standalone__"
            set_current_bot_id(bot_id)

    ctx = get_bot_context(bot_id)
    if bot_id not in _bot_contexts:
        _bot_contexts[bot_id] = {}

    if ctx.get('client') is None:
        client = get_bot_client()
        if client is None:
            try:
                client = sys.modules.get('builtins').unified_app_client
            except Exception:
                client = None
        if client is not None:
            _bot_contexts[bot_id]['client'] = client

    if ctx.get('config') is None:
        cfg = get_config()
        if cfg is None:
            try:
                import settings as _bare_config
                cfg = _bare_config
            except ImportError:
                cfg = None
        _bot_contexts[bot_id]['config'] = cfg

    if ctx.get('queue') is None:
        _bot_contexts[bot_id]['queue'] = Queue()
    if ctx.get('tune') is None:
        _bot_contexts[bot_id]['tune'] = TgCall()
    if ctx.get('yt') is None:
        _bot_contexts[bot_id]['yt'] = YouTube()
    if ctx.get('tg') is None:
        _bot_contexts[bot_id]['tg'] = Telegram()
    if ctx.get('preload') is None:
        try:
            _bot_contexts[bot_id]['preload'] = PreloadManager()
        except NotImplementedError:
            _bot_contexts[bot_id]['preload'] = None
    if ctx.get('userbot') is None:
        _bot_contexts[bot_id]['userbot'] = Userbot()

    return _bot_contexts[bot_id]


_ensure_bootstrap_context()
ensure_dirs()  # الإصلاح: كانت مستوردة فقط بدون استدعاء، فمجلد cache/ (اللازم
                # لحفظ الصور المصغّرة المولّدة) لم يكن يُنشأ أبداً، فتفشل
                # عملية حفظ الصورة بصمت وترجع دائماً للصورة الاحتياطية العامة.

lang = Language()

import sqlite3


def init_local_songs_db() -> None:
    try:
        conn = sqlite3.connect("songs.db")
        cursor = conn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS songs (yt_id TEXT PRIMARY KEY, msg_id INTEGER, file_id TEXT DEFAULT '')"
        )
        conn.commit()
        conn.close()
    except Exception as e:
        logger.warning(f"init_local_songs_db: {e}")


init_local_songs_db()


async def stop() -> None:
    logger.info("🛑 Stopping bot...")
    for task in tasks:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
        except Exception:
            pass
    try:
        await userbot.exit()
    except Exception:
        pass
    logger.info("✅ Bot stopped successfully.\n")


__all__ = [
    'r',
    'Dev_FINAL',
    'k',
    'config',
    'app',
    'queue',
    'tune',
    'yt',
    'tg',
    'preload',
    'userbot',
    'lang',
    'tasks',
    'boot',
    'logger',
    'stop',
    'Queue',
    'Media',
    'Track',
    'buttons',
    'thumb',
    'utils',
    'TgCall',
    'Userbot',
    'Language',
    'Telegram',
    'YouTube',
    'PreloadManager',
    'ensure_dirs',
]
