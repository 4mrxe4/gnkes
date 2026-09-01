# _dataclass.py
from helpers.context import redis_proxy as r, dev_final_proxy as Dev_FINAL, k_proxy as k
from dataclasses import dataclass
@dataclass
class Media:
    id: str
    duration: str
    duration_sec: int
    file_path: str
    message_id: int
    title: str
    url: str
    time: int = 0
    user: str = None
    is_live: bool = False
    video: bool = False
@dataclass
class Track:
    id: str
    channel_name: str
    duration: str
    duration_sec: int
    title: str
    url: str
    file_path: str = None
    message_id: int = 0
    time: int = 0
    thumbnail: str = None
    user: str = None
    view_count: str = None
    is_live: bool = False
    video: bool = False