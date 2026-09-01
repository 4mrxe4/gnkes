# _queue.py
from helpers.context import redis_proxy as r, dev_final_proxy as Dev_FINAL, k_proxy as k
import os
import glob
from collections import defaultdict, deque
from typing import Union
import asyncio
from ._dataclass import Media, Track
MediaItem = Union[Media, Track]
class Queue:
    def __init__(self):
        self.queues: dict[int, deque[MediaItem]] = defaultdict(deque)
    def add(self, chat_id: int, item: MediaItem) -> int:
        self.queues[chat_id].append(item)
        return len(self.queues[chat_id]) - 1
    def check_item(self, chat_id: int, item_id: str) -> tuple[int, MediaItem | None]:
        pos, track = next(
            (
                (i, track)
                for i, track in enumerate(list(self.queues[chat_id]))
                if track.id == item_id
            ),
            (-1, None),
        )
        return pos, track
    def force_add(self, chat_id: int, item: MediaItem, remove: int | bool = False) -> None:
        self.remove_current(chat_id)
        self.queues[chat_id].appendleft(item)
        if remove:
            self.queues[chat_id].rotate(-remove)
            self.queues[chat_id].popleft()
            self.queues[chat_id].rotate(remove)
    def get_current(self, chat_id: int) -> MediaItem | None:
        return self.queues[chat_id][0] if self.queues[chat_id] else None
    def get_next(self, chat_id: int, check: bool = False) -> MediaItem | None:
        if not self.queues[chat_id]:
            return None
        if check:
            return self.queues[chat_id][1] if len(self.queues[chat_id]) > 1 else None
        current_item = self.queues[chat_id][0]
        self.queues[chat_id].popleft()
        if current_item:
            self._clean_file_silently(chat_id, current_item)
        return self.queues[chat_id][0] if self.queues[chat_id] else None
    def get_queue(self, chat_id: int) -> list[MediaItem]:
        return list(self.queues[chat_id])
    def get_all(self, chat_id: int) -> list[MediaItem]:
        return self.get_queue(chat_id)
    def remove_current(self, chat_id: int) -> None:
        if self.queues[chat_id]:
            current_item = self.queues[chat_id].popleft()
            if current_item:
                self._clean_file_silently(chat_id, current_item)
    def clear(self, chat_id: int) -> None:
        current_queue = list(self.queues[chat_id])
        self.queues[chat_id].clear()
        for item in current_queue:
            self._clean_file_silently(chat_id, item, force_clear=True)
    def peek_next(self, chat_id: int, count: int = 2) -> list[MediaItem]:
        if not self.queues[chat_id] or len(self.queues[chat_id]) <= 1:
            return []
        queue_list = list(self.queues[chat_id])
        return queue_list[1:min(len(queue_list), count + 1)]
    @staticmethod
    def is_downloaded(item: MediaItem) -> bool:
        return bool(getattr(item, 'file_path', None))
    def _clean_file_silently(self, chat_id: int, item: MediaItem, force_clear: bool = False) -> None:
        try:
            file_id = getattr(item, "id", None)
            if not file_id:
                return
            file_path_str = getattr(item, "file_path", "")
            if file_path_str and "archive_msg_" in str(file_path_str):
                return
            async def _async_clean():
                try:
                    if not force_clear:
                        current_loop = await r.get(f"loop:{chat_id}:{Dev_FINAL}")
                        if current_loop and current_loop != "0":
                            return
                        remaining_queue = self.queues.get(chat_id, deque())
                        is_duplicated = any(getattr(q_item, "id", None) == file_id for q_item in remaining_queue)
                        if is_duplicated:
                            return
                    pattern = os.path.join("downloads", f"{file_id}.*")
                    for local_file in glob.glob(pattern):
                        if local_file.endswith((".part", ".ytdl", ".info.json", ".temp")):
                            continue
                        if os.path.exists(local_file):
                            os.remove(local_file)
                except Exception:
                    pass
            try:
                loop = asyncio.get_running_loop()
                loop.create_task(_async_clean())
            except RuntimeError:
                asyncio.run(_async_clean())
        except Exception:
            pass