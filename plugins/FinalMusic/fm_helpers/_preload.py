# _preload.py
from helpers.context import redis_proxy as r, dev_final_proxy as Dev_FINAL, k_proxy as k
import asyncio
import logging
from typing import Dict, Set
logger = logging.getLogger("FinalMusic")
class PreloadManager:
    def __init__(self):
        self._tasks: Dict[int, Dict[str, asyncio.Task]] = {}
        self._preloaded: Dict[int, Set[str]] = {}
    async def preload_next(self, chat_id: int, media) -> None:
        media_id = getattr(media, "id", None)
        if not media_id:
            return
        if chat_id not in self._tasks:
            self._tasks[chat_id] = {}
        if chat_id not in self._preloaded:
            self._preloaded[chat_id] = set()
        if media_id in self._preloaded[chat_id]:
            logger.debug(f"Track {media_id} already preloaded for chat {chat_id}")
            return
        existing = self._tasks[chat_id].get(media_id)
        if existing and not existing.done():
            return
        task = asyncio.create_task(self._preload_task(chat_id, media))
        self._tasks[chat_id][media_id] = task
    async def _preload_task(self, chat_id: int, media) -> None:
        try:
            from plugins.FinalMusic import yt
            logger.debug(f"Starting preload for chat {chat_id}: {media.title}")
            if not media.file_path:
                media.file_path = await yt.download(media.id, video=getattr(media, "video", False))
                if media.file_path:
                    self._preloaded.setdefault(chat_id, set()).add(media.id)
                logger.debug(f"Preload complete for chat {chat_id}: {media.title}")
            else:
                logger.debug(f"Track already has file_path for chat {chat_id}: {media.title}")
                self._preloaded.setdefault(chat_id, set()).add(media.id)
        except asyncio.CancelledError:
            logger.debug(f"Preload cancelled for chat {chat_id}")
            raise
        except Exception as e:
            logger.error(f"Preload error for chat {chat_id}: {e}")
        finally:
            media_tasks = self._tasks.get(chat_id)
            if media_tasks:
                media_tasks.pop(getattr(media, "id", None), None)
                if not media_tasks:
                    self._tasks.pop(chat_id, None)
    async def cancel_preload(self, chat_id: int) -> None:
        media_tasks = self._tasks.get(chat_id, {})
        if media_tasks:
            active = [task for task in media_tasks.values() if not task.done()]
            for task in active:
                task.cancel()
            if active:
                await asyncio.gather(*active, return_exceptions=True)
            logger.debug(f"Cancelled preload for chat {chat_id}")
        self._preloaded.pop(chat_id, None)
        self._tasks.pop(chat_id, None)
    def is_preloaded(self, chat_id: int, media_id: str) -> bool:
        return media_id in self._preloaded.get(chat_id, set())
    def clear(self, chat_id: int) -> None:
        self._preloaded.pop(chat_id, None)
        self._tasks.pop(chat_id, None)
    async def start_preload(self, chat_id: int, count: int = 2) -> None:
        try:
            from plugins.FinalMusic import queue
            all_tracks = queue.get_queue(chat_id)
            if len(all_tracks) > 1:
                upcoming = all_tracks[1:min(1 + count, len(all_tracks))]
                for media in upcoming:
                    if not media.file_path:
                        await self.preload_next(chat_id, media)
        except Exception as e:
            logger.debug(f"Error in start_preload for {chat_id}: {e}")