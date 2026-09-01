
import json
import re

from helpers.context import get_global_r, get_global_dev, get_current_bot_id
from helpers.redis import RedisFake


def get_redis_instance():
    try:
        r = get_global_r()
        if r:
            return r
    except Exception:
        pass

    try:
        dev = get_global_dev()
        if dev:
            return RedisFake(bot_id=dev)
    except Exception:
        pass

    return RedisFake()


r = get_redis_instance()

DEFAULT_GENDER_MAP = {
    "ابشر": "ابشري",
    "عزيزي": "عزيزتي",
    "انت": "انتي",
    "ادمن": "ادمنه",
    "مالك": "مالكه",
    "مدير": "مديره",
    "مميز": "مميزه",
    "رتبته": "رتبتها",
    "عضو": "عضوه",
    "تقدم": "تقدمي",
    "محظور": "محظوره",
    "مقيد": "مقيده",
    "مكتوم": "مكتومه",
    "المالك": "المالكه",
    "الاساسي": "الاساسيه",
    "ارسل": "ارسلي",
    "الحلو": "الحلوه",
    "رفعته": "رفعتها",
    "صار": "صارت",
    "المستخدم": "المستخدمه",
    "العضو": "العضوه",
    "إنذاراته": "انذاراتها",
}


async def get_gender_map(bot_id: str = None) -> dict:
    try:
        if bot_id is None:
            bot_id = get_current_bot_id()
            if bot_id is None:
                bot_id = get_global_dev()

        redis = get_redis_instance()
        key = f"gender_map:{bot_id}" if bot_id else "gender_map"

        data = await redis.get(key)
        if data:
            return json.loads(data)
        return DEFAULT_GENDER_MAP.copy()
    except Exception:
        return DEFAULT_GENDER_MAP.copy()


async def save_gender_map(gender_map: dict, bot_id: str = None) -> bool:
    try:
        if bot_id is None:
            bot_id = get_current_bot_id()
            if bot_id is None:
                bot_id = get_global_dev()

        redis = get_redis_instance()
        key = f"gender_map:{bot_id}" if bot_id else "gender_map"

        await redis.set(key, json.dumps(gender_map))
        return True
    except Exception:
        return False


async def add_gender_word(word: str, female_word: str, bot_id: str = None) -> bool:
    try:
        gender_map = await get_gender_map(bot_id)
        gender_map[word.lower().strip()] = female_word.lower().strip()
        return await save_gender_map(gender_map, bot_id)
    except Exception:
        return False


async def remove_gender_word(word: str, bot_id: str = None) -> bool:
    try:
        gender_map = await get_gender_map(bot_id)
        word_key = word.lower().strip()
        if word_key in gender_map:
            del gender_map[word_key]
            return await save_gender_map(gender_map, bot_id)
        return False
    except Exception:
        return False


async def get_gender(user_id: int, bot_id: str = None) -> str:
    try:
        if bot_id is None:
            bot_id = get_current_bot_id()
            if bot_id is None:
                bot_id = get_global_dev()

        redis = get_redis_instance()
        key = f"user_gender:{user_id}:{bot_id}" if bot_id else f"user_gender:{user_id}"
        gender = await redis.get(key)
        return gender if gender in ["male", "female"] else "male"
    except Exception:
        return "male"


async def genderize_text(text: str, user_id: int) -> str:
    if not text or not isinstance(text, str):
        return text

    try:
        bot_id = get_current_bot_id() or get_global_dev()
        gender = await get_gender(user_id, bot_id)

        if gender == "male":
            return text

        gender_map = await get_gender_map(bot_id)
        new_text = text

        sorted_items = sorted(gender_map.items(), key=lambda x: len(x[0]), reverse=True)

        for word, female in sorted_items:
            escaped_word = re.escape(word)
            if ' ' in word:
                pattern = r'(?<![^\s])' + escaped_word + r'(?![^\s])'
            else:
                pattern = r'\b' + escaped_word + r'\b'

            new_text = re.sub(pattern, female, new_text, flags=re.IGNORECASE)

        return new_text
    except Exception:
        return text


async def set_user_gender(user_id: int, gender: str, bot_id: str = None) -> bool:
    try:
        if gender not in ["male", "female"]:
            return False

        if bot_id is None:
            bot_id = get_current_bot_id()
            if bot_id is None:
                bot_id = get_global_dev()

        redis = get_redis_instance()
        key = f"user_gender:{user_id}:{bot_id}" if bot_id else f"user_gender:{user_id}"
        await redis.set(key, gender)
        return True
    except Exception:
        return False


async def delete_user_gender(user_id: int, bot_id: str = None) -> bool:
    try:
        if bot_id is None:
            bot_id = get_current_bot_id()
            if bot_id is None:
                bot_id = get_global_dev()

        redis = get_redis_instance()
        key = f"user_gender:{user_id}:{bot_id}" if bot_id else f"user_gender:{user_id}"
        await redis.delete(key)
        return True
    except Exception:
        return False


from helpers import redis
if not hasattr(redis, 'Redis'):
    redis.Redis = RedisFake
if not hasattr(redis, 'ConnectionPool'):
    redis.ConnectionPool = redis.ConnectionPoolFake

__all__ = [
    'get_gender',
    'genderize_text',
    'set_user_gender',
    'delete_user_gender',
    'get_gender_map',
    'save_gender_map',
    'add_gender_word',
    'remove_gender_word',
    'DEFAULT_GENDER_MAP',
]
