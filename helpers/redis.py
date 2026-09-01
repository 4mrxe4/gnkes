import os
import sys
import json
import time
import fnmatch
import asyncio as _asyncio

from dotenv import load_dotenv
load_dotenv()

try:
    import redis.asyncio as _real_aioredis
    from redis.exceptions import ResponseError as _RedisResponseError
    from redis.exceptions import RedisError as _RedisError
except ImportError as _e:
    raise ImportError(
        "مكتبة redis غير مثبتة. يرجى تنفيذ: pip install redis>=5.0.0"
    ) from _e

REDIS_URL = os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")

_pool = _real_aioredis.ConnectionPool.from_url(REDIS_URL, decode_responses=True)
_client = _real_aioredis.Redis(connection_pool=_pool)

_MIGRATION_DONE_KEY = "__lmdb_migration__:completed"
_MIGRATION_LOCK_KEY = "__lmdb_migration__:lock"
_INTERNAL_KEY_PREFIXES = ("__lmdb_migration__:",)


class ConnectionPoolFake:
    def __init__(self, *args, **kwargs):
        pass

    @classmethod
    def from_url(cls, *args, **kwargs):
        return cls()


async def _retry(coro_fn, *args, attempts: int = 3, base_delay: float = 0.05, **kwargs):
    last_err = None
    for attempt in range(attempts):
        try:
            return await coro_fn(*args, **kwargs)
        except (_RedisError, ConnectionError, OSError) as e:
            last_err = e
            try:
                await _asyncio.sleep(base_delay * (attempt + 1))
            except Exception:
                pass
    if last_err:
        raise last_err


class RedisFake:

    def __init__(self, *args, bot_id=None, **kwargs):
        self.bot_id = str(bot_id) if bot_id else None
        self.prefix = f"{self.bot_id}:" if self.bot_id else ""

    async def get_int(self, key: str, default: int = 0) -> int:
        """يقرأ مفتاحاً ويحوّله إلى int بأمان (fix B-1).

        يعيد default عند غياب المفتاح أو عدم إمكانية التحويل — يمنع
        TypeError: int() argument must be str, not NoneType.
        """
        try:
            raw = await self.get(key)
            if raw is None:
                return default
            return int(str(raw).strip())
        except (TypeError, ValueError):
            return default

    def _get_key(self, key: str) -> str:
        if not key:
            return key
        key_str = str(key)
        if self.bot_id and (
            key_str.startswith(f"{self.bot_id}:")
            or key_str.startswith(f"H:{self.bot_id}:")
            or key_str.startswith(f"S:{self.bot_id}:")
            or key_str.startswith(f"L:{self.bot_id}:")
            or key_str.startswith(f"Z:{self.bot_id}:")
        ):
            return key_str
        if self.prefix and key_str.startswith(self.prefix):
            return key_str
        return f"{self.prefix}{key_str}" if self.prefix else key_str

    def _is_youtube_key(self, key: str) -> bool:
        if not key:
            return False
        if key.startswith("music_cache:"):
            return True
        if ":file_id:" in key:
            return True
        if key.endswith(":titles"):
            return True
        if ":titles" in key:
            return True
        if key.startswith("file_id:"):
            return True
        return False

    def _serialize(self, value):
        if value is None:
            return None
        if isinstance(value, (str, int, float, bool)):
            return value
        if isinstance(value, dict):
            return {str(k): self._serialize(v) for k, v in value.items()}
        if isinstance(value, (list, tuple)):
            return [self._serialize(v) for v in value]
        try:
            json.dumps(value)
            return value
        except Exception:
            return str(value)

    def _to_str_value(self, value) -> str:
        val = self._serialize(value)
        return json.dumps(val) if not isinstance(val, str) else val

    async def get(self, key: str):
        full_key = self._get_key(key)
        wrong_type = False
        try:
            res = await _retry(_client.get, full_key)
            if res is not None:
                return res
            return None
        except _RedisResponseError:
            wrong_type = True
        except Exception:
            return None

        if not wrong_type:
            return None

        try:
            async with _client.pipeline(transaction=False) as pipe:
                pipe.hgetall(full_key)
                pipe.smembers(full_key)
                pipe.zrange(full_key, 0, -1, withscores=True)
                h, s, z = await pipe.execute()
        except Exception:
            return None

        if h:
            return json.dumps(h)
        if s:
            return json.dumps(list(s))
        if z:
            return json.dumps({m: sc for m, sc in z})
        return None

    async def mget(self, keys: list, *args, **kwargs) -> list:
        results = []
        for k in keys:
            results.append(await self.get(k))
        return results

    async def get_many(self, keys: list) -> list:
        """نسخة مُجمَّعة وآمنة من get() لعدة مفاتيح دفعة واحدة (فحص صلاحيات/رتب
        متعددة المفاتيح في نفس العملية) — بجولة Redis واحدة (Pipeline حقيقي)
        بدل استدعاء get() منفصل لكل مفتاح.

        تُرجع قائمة بنفس الترتيب والطول تماماً مثل استدعاء
        ``[await self.get(k) for k in keys]``، بما فيها نفس سلوك get() عند
        وجود مفتاح بنوع مختلف (hash/set/zset) — عبر جولة fallback ثانية
        محصورة فقط في المفاتيح التي فشلت (WRONGTYPE)، فلا يتغيّر أي ناتج،
        فقط يقل عدد الجولات."""
        if not keys:
            return []

        full_keys = [self._get_key(k) for k in keys]

        try:
            async with _client.pipeline(transaction=False) as pipe:
                for fk in full_keys:
                    pipe.get(fk)
                raw_results = await pipe.execute(raise_on_error=False)
        except Exception:
            # فشل الـ Pipeline نفسه (مثلاً انقطاع اتصال) — نرجع لطريقة get()
            # الفردية القديمة بدل فقدان النتيجة كاملة.
            return [await self.get(k) for k in keys]

        results = [None] * len(full_keys)
        wrongtype_idx = []
        for i, res in enumerate(raw_results):
            if isinstance(res, Exception):
                wrongtype_idx.append(i)
            else:
                results[i] = res

        if wrongtype_idx:
            try:
                async with _client.pipeline(transaction=False) as pipe2:
                    for i in wrongtype_idx:
                        pipe2.hgetall(full_keys[i])
                        pipe2.smembers(full_keys[i])
                        pipe2.zrange(full_keys[i], 0, -1, withscores=True)
                    fallback_raw = await pipe2.execute()
                for n, i in enumerate(wrongtype_idx):
                    h, s, z = fallback_raw[n * 3:n * 3 + 3]
                    if h:
                        results[i] = json.dumps(h)
                    elif s:
                        results[i] = json.dumps(list(s))
                    elif z:
                        results[i] = json.dumps({m: sc for m, sc in z})
            except Exception:
                pass

        return results

    async def mget_real(self, keys: list) -> list:
        if not keys:
            return []
        full_keys = [self._get_key(k) for k in keys]
        try:
            return await _retry(_client.mget, full_keys)
        except Exception:
            return [None] * len(keys)

    async def pipeline(self, commands: list):
        async with _client.pipeline(transaction=False) as pipe:
            for cmd, args, kwargs in commands:
                getattr(pipe, cmd)(*args, **kwargs)
            return await pipe.execute()

    async def set(self, key: str, value, *args, **kwargs) -> bool:
        full_key = self._get_key(key)
        nx = kwargs.get('nx', False)
        xx = kwargs.get('xx', False)
        ex = kwargs.get('ex', None)
        px = kwargs.get('px', None)
        val_str = self._to_str_value(value)
        try:
            result = await _retry(
                _client.set, full_key, val_str, nx=nx, xx=xx,
                ex=int(ex) if ex else None, px=int(px) if px else None,
            )
            return bool(result)
        except Exception:
            return False

    async def setex(self, key: str, time_sec: int, value) -> bool:
        try:
            full_key = self._get_key(key)
            val_str = self._to_str_value(value)
            await _retry(_client.setex, full_key, int(time_sec), val_str)
            return True
        except Exception:
            return False

    async def delete(self, *keys: str) -> int:
        deleted_count = 0
        for k in keys:
            full_key = self._get_key(k)
            if self._is_youtube_key(full_key):
                continue
            try:
                deleted_count += await _retry(_client.delete, full_key)
            except Exception:
                pass
        return deleted_count

    async def exists(self, *keys: str) -> int:
        count = 0
        for k in keys:
            full_key = self._get_key(k)
            try:
                if await _retry(_client.exists, full_key):
                    count += 1
            except Exception:
                pass
        return count

    async def expire(self, key: str, seconds: int) -> int:
        try:
            full_key = self._get_key(key)
            ok = await _retry(_client.expire, full_key, int(seconds))
            return 1 if ok else 0
        except Exception:
            return 0

    async def ttl(self, key: str) -> int:
        try:
            full_key = self._get_key(key)
            res = await _retry(_client.ttl, full_key)
            return res if res is not None else -2
        except Exception:
            return -2

    async def incr(self, key: str) -> int:
        return await self.incrby(key, 1)

    async def incrby(self, key: str, amount: int) -> int:
        try:
            full_key = self._get_key(key)
            return await _retry(_client.incrby, full_key, int(amount))
        except Exception:
            return 0

    async def scan_iter(self, match: str = "*", count: int = 100, *args, **kwargs):
        """مسح cursor-based (SCAN) بدل KEYS * — لا يمنع Redis أبداً.

        يعيد async generator يتنقل عبر SCAN بدفعات صغيرة (count=100) مع مطابقة
        النمط على مستوى الخادم، فلا يُحمَّل كامل المفاتيح في الذاكرة ولا يُحجب
        event loop. الاستخدام:
            async for key in r.scan_iter(match="foo:*"):
        """
        if match is None:
            match = "*"
        try:
            cursor = 0
            while True:
                cursor, batch = await _retry(_client.scan, cursor=cursor, match=match, count=int(count))
                for k in batch:
                    if any(k.startswith(p) for p in _INTERNAL_KEY_PREFIXES):
                        continue
                    if fnmatch.fnmatch(k, match) or fnmatch.fnmatch(k, f"*{match}*"):
                        yield k
                if cursor == 0:
                    break
        except Exception:
            return

    async def keys(self, pattern: str) -> list:
        matched_keys = []
        try:
            async for k in self.scan_iter(match=f"*{pattern}*", count=500):
                if k not in matched_keys:
                    matched_keys.append(k)
        except Exception:
            pass
        return matched_keys

    async def smembers(self, key: str) -> list:
        try:
            full_key = self._get_key(key)
            res = await _retry(_client.smembers, full_key)
            return list(res) if res else []
        except Exception:
            return []

    async def sadd(self, key: str, *values) -> int:
        try:
            full_key = self._get_key(key)
            if not values:
                return 0
            return await _retry(_client.sadd, full_key, *[str(v) for v in values])
        except Exception:
            return 0

    async def srem(self, key: str, *values) -> int:
        try:
            full_key = self._get_key(key)
            if not values:
                return 0
            return await _retry(_client.srem, full_key, *[str(v) for v in values])
        except Exception:
            return 0

    async def sismember(self, key: str, value) -> int:
        try:
            full_key = self._get_key(key)
            res = await _retry(_client.sismember, full_key, str(value))
            return 1 if res else 0
        except Exception:
            return 0

    async def scard(self, key: str) -> int:
        try:
            full_key = self._get_key(key)
            return await _retry(_client.scard, full_key)
        except Exception:
            return 0

    async def hset(self, name: str, key: str = None, value=None, mapping: dict = None) -> int:
        try:
            full_key = self._get_key(name)
            if mapping and isinstance(mapping, dict):
                data = {str(k): (str(v) if v is not None else "") for k, v in mapping.items()}
                if not data:
                    return 0
                return await _retry(_client.hset, full_key, mapping=data)
            elif key is not None:
                return await _retry(_client.hset, full_key, str(key), str(value) if value is not None else "")
            return 0
        except Exception:
            return 0

    async def hgetall(self, name: str) -> dict:
        try:
            full_key = self._get_key(name)
            res = await _retry(_client.hgetall, full_key)
            return res if res else {}
        except Exception:
            return {}

    async def hget(self, name: str, key: str):
        try:
            full_key = self._get_key(name)
            res = await _retry(_client.hget, full_key, str(key))
            return res
        except Exception:
            return None

    async def hdel(self, name: str, key: str) -> int:
        try:
            full_key = self._get_key(name)
            if self._is_youtube_key(full_key):
                return 0
            return await _retry(_client.hdel, full_key, str(key))
        except Exception:
            return 0

    async def hexists(self, name: str, key: str) -> int:
        try:
            full_key = self._get_key(name)
            res = await _retry(_client.hexists, full_key, str(key))
            return 1 if res else 0
        except Exception:
            return 0

    async def hincrby(self, name: str, key: str, amount: int) -> int:
        try:
            full_key = self._get_key(name)
            return await _retry(_client.hincrby, full_key, str(key), int(amount))
        except Exception:
            return 0

    async def lpush(self, key: str, *values) -> int:
        try:
            full_key = self._get_key(key)
            if not values:
                return await self.llen(key)
            return await _retry(_client.lpush, full_key, *[str(v) for v in values])
        except Exception:
            return 0

    async def rpush(self, key: str, *values) -> int:
        try:
            full_key = self._get_key(key)
            if not values:
                return await self.llen(key)
            return await _retry(_client.rpush, full_key, *[str(v) for v in values])
        except Exception:
            return 0

    async def lrange(self, key: str, start: int, end: int) -> list:
        try:
            full_key = self._get_key(key)
            res = await _retry(_client.lrange, full_key, start, end)
            return res if res else []
        except Exception:
            return []

    async def ltrim(self, key: str, start: int, end: int) -> bool:
        try:
            full_key = self._get_key(key)
            if self._is_youtube_key(full_key):
                return False
            await _retry(_client.ltrim, full_key, start, end)
            return True
        except Exception:
            return False

    async def rpop(self, key: str):
        try:
            full_key = self._get_key(key)
            return await _retry(_client.rpop, full_key)
        except Exception:
            return None

    async def llen(self, key: str) -> int:
        try:
            full_key = self._get_key(key)
            return await _retry(_client.llen, full_key)
        except Exception:
            return 0

    async def lindex(self, key: str, index: int):
        try:
            full_key = self._get_key(key)
            return await _retry(_client.lindex, full_key, index)
        except Exception:
            return None

    async def zadd(self, key: str, mapping: dict, *args, **kwargs) -> int:
        try:
            full_key = self._get_key(key)
            data = {str(m): float(s) for m, s in mapping.items()}
            if not data:
                return 0
            return await _retry(_client.zadd, full_key, data)
        except Exception:
            return 0

    async def zincrby(self, key: str, amount: int, member: str) -> float:
        try:
            full_key = self._get_key(key)
            new_score = await _retry(_client.zincrby, full_key, float(amount), str(member))
            if new_score is not None and new_score < 0:
                await _retry(_client.zadd, full_key, {str(member): 0})
                return 0.0
            return float(new_score) if new_score is not None else 0.0
        except Exception:
            return 0

    async def zrevrange(self, key: str, start: int, end: int, withscores: bool = False) -> list:
        try:
            full_key = self._get_key(key)
            res = await _retry(_client.zrevrange, full_key, start, end, withscores=withscores)
            if not res:
                return []
            if withscores:
                return [(str(m), float(s)) for m, s in res]
            return [str(m) for m in res]
        except Exception:
            return []

    async def zrevrank(self, key: str, member: str):
        try:
            full_key = self._get_key(key)
            return await _retry(_client.zrevrank, full_key, str(member))
        except Exception:
            return None

    async def zscore(self, key: str, member: str):
        try:
            full_key = self._get_key(key)
            res = await _retry(_client.zscore, full_key, str(member))
            return float(res) if res is not None else None
        except Exception:
            return None

    async def zrem(self, key: str, *members) -> int:
        try:
            full_key = self._get_key(key)
            if not members:
                return 0
            return await _retry(_client.zrem, full_key, *[str(m) for m in members])
        except Exception:
            return 0

    async def zremrangebyscore(self, key: str, min_score, max_score) -> int:
        try:
            full_key = self._get_key(key)
            if self._is_youtube_key(full_key):
                return 0
            return await _retry(_client.zremrangebyscore, full_key, float(min_score), float(max_score))
        except Exception:
            return 0

    async def zcard(self, key: str) -> int:
        try:
            full_key = self._get_key(key)
            return await _retry(_client.zcard, full_key)
        except Exception:
            return 0

    async def point(self, *args, **kwargs):
        return None

    async def music_get(self, video_id: str) -> dict | None:
        try:
            key = f"music_cache:{video_id}"
            data = await _retry(_client.hgetall, key)
            if data:
                return {"msg_id": int(data.get("msg_id", 0))}
            return None
        except Exception:
            return None

    async def music_set(self, video_id: str, msg_id: int) -> bool:
        try:
            key = f"music_cache:{video_id}"
            await _retry(_client.hset, key, mapping={"msg_id": str(msg_id)})
            await _retry(_client.expire, key, 2592000)
            return True
        except Exception:
            return False

    async def music_exists(self, video_id: str) -> bool:
        try:
            key = f"music_cache:{video_id}"
            return bool(await _retry(_client.hexists, key, "msg_id"))
        except Exception:
            return False

    async def music_delete(self, video_id: str) -> bool:
        try:
            key = f"music_cache:{video_id}"
            await _retry(_client.delete, key)
            return True
        except Exception:
            return False

    async def music_get_all(self) -> list:
        try:
            result = []
            async for key in self.scan_iter(match="music_cache:*", count=100):
                result.append(key)
            return result
        except Exception:
            return []

    async def music_count(self) -> int:
        try:
            count = 0
            async for _key in self.scan_iter(match="music_cache:*", count=100):
                count += 1
            return count
        except Exception:
            return 0

    async def get_file_id_l1(self, bot_id: str, video_id: str) -> str | None:
        try:
            key = f"{bot_id}:file_id:{video_id}"
            return await self.get(key)
        except Exception:
            return None

    async def set_file_id_l1(self, bot_id: str, video_id: str, file_id: str) -> bool:
        try:
            key = f"{bot_id}:file_id:{video_id}"
            await self.set(key, file_id)
            await self.expire(key, 86400 * 30)
            return True
        except Exception:
            return False

    async def delete_file_id_l1(self, bot_id: str, video_id: str) -> bool:
        try:
            key = f"{bot_id}:file_id:{video_id}"
            await self.delete(key)
            return True
        except Exception:
            return False

    async def get_titles_l1(self, bot_id: str) -> dict:
        try:
            key = f"{bot_id}:titles"
            return await self.hgetall(key)
        except Exception:
            return {}

    async def set_title_l1(self, bot_id: str, video_id: str, title: str) -> bool:
        try:
            key = f"{bot_id}:titles"
            await self.hset(key, video_id, title)
            return True
        except Exception:
            return False

    async def get_all_video_ids_l1(self, bot_id: str) -> list:
        try:
            key = f"{bot_id}:titles"
            data = await self.hgetall(key)
            return list(data.keys())
        except Exception:
            return []

    def get_isolated_redis(self, bot_id: str):
        if not bot_id:
            raise ValueError("bot_id مطلوب لإنشاء Redis معزول")
        return RedisFake(bot_id=bot_id)

    def get_bot_redis(self, bot_id: str = None):
        if bot_id is None:
            from helpers.context import get_current_bot_id
            bot_id = get_current_bot_id()
        if bot_id:
            return RedisFake(bot_id=bot_id)
        return RedisFake()


async def get_sudoers_async(bot_id: str) -> set:
    try:
        r = RedisFake(bot_id=bot_id)
        sudoers_list = await r.smembers(f"sudoers:{bot_id}")
        return set([int(s) for s in sudoers_list]) if sudoers_list else set()
    except Exception:
        return set()


async def is_sudoer_async(user_id: int, bot_id: str) -> bool:
    sudoers = await get_sudoers_async(bot_id)
    return user_id in sudoers


async def redis_healthcheck() -> tuple[bool, str]:
    try:
        pong = await _retry(_client.ping, attempts=3, base_delay=0.5)
        if pong:
            return True, f"متصل بنجاح بـ Redis ({REDIS_URL})"
        return False, f"فشل الاتصال بـ Redis ({REDIS_URL})"
    except Exception as e:
        return False, f"تعذر الاتصال بـ Redis على {REDIS_URL}: {e}"


async def migrate_lmdb_to_redis(lmdb_path: str = "rfinal_lmdb_data", force: bool = False) -> dict:
    stats = {
        "ran": False,
        "already_done": False,
        "found_dir": os.path.exists(lmdb_path),
        "total_raw_entries": 0,
        "migrated_keys": 0,
        "skipped_existing": 0,
        "skipped_expired": 0,
        "errors": 0,
    }

    if not stats["found_dir"]:
        return stats

    if not force:
        try:
            already = await _retry(_client.get, _MIGRATION_DONE_KEY)
            if already:
                stats["already_done"] = True
                return stats
        except Exception:
            pass

    try:
        got_lock = await _retry(_client.set, _MIGRATION_LOCK_KEY, "1", nx=True, ex=3600)
    except Exception:
        got_lock = True
    if not got_lock and not force:
        stats["already_done"] = True
        return stats

    try:
        import lmdb
    except ImportError:
        return stats

    stats["ran"] = True

    strings_data = {}
    hash_data = {}
    set_data = {}
    list_data = {}
    zset_data = {}
    ttl_data = {}

    try:
        env = lmdb.open(lmdb_path, map_size=2 * 1024 * 1024 * 1024, readonly=True, lock=False)
        with env.begin() as txn:
            cursor = txn.cursor()
            for raw_key, raw_val in cursor:
                stats["total_raw_entries"] += 1
                try:
                    k_str = raw_key.decode("utf-8")
                except Exception:
                    continue

                if k_str.startswith("TTL:"):
                    orig_key = k_str[len("TTL:"):]
                    try:
                        ttl_data[orig_key] = float(raw_val.decode("utf-8"))
                    except Exception:
                        pass
                    continue

                if k_str.startswith("H:"):
                    orig_key = k_str[2:]
                    try:
                        hash_data[orig_key] = json.loads(raw_val.decode("utf-8"))
                    except Exception:
                        stats["errors"] += 1
                    continue

                if k_str.startswith("S:"):
                    orig_key = k_str[2:]
                    try:
                        set_data[orig_key] = json.loads(raw_val.decode("utf-8"))
                    except Exception:
                        stats["errors"] += 1
                    continue

                if k_str.startswith("L:"):
                    orig_key = k_str[2:]
                    try:
                        list_data[orig_key] = json.loads(raw_val.decode("utf-8"))
                    except Exception:
                        stats["errors"] += 1
                    continue

                if k_str.startswith("Z:"):
                    orig_key = k_str[2:]
                    try:
                        zset_data[orig_key] = json.loads(raw_val.decode("utf-8"))
                    except Exception:
                        stats["errors"] += 1
                    continue

                try:
                    strings_data[k_str] = raw_val.decode("utf-8")
                except Exception:
                    stats["errors"] += 1
        env.close()
    except Exception as e:
        try:
            await _retry(_client.delete, _MIGRATION_LOCK_KEY)
        except Exception:
            pass
        return stats

    now = time.time()

    def _is_expired(k):
        exp = ttl_data.get(k)
        return exp is not None and now > exp

    async def _apply_ttl(k):
        exp = ttl_data.get(k)
        if exp is None:
            return
        remaining_ms = int((exp - now) * 1000)
        if remaining_ms > 0:
            try:
                await _retry(_client.pexpire, k, remaining_ms)
            except Exception:
                pass

    for k, v in strings_data.items():
        if _is_expired(k):
            stats["skipped_expired"] += 1
            continue
        try:
            if await _retry(_client.exists, k):
                stats["skipped_existing"] += 1
                continue
            await _retry(_client.set, k, v)
            await _apply_ttl(k)
            stats["migrated_keys"] += 1
        except Exception:
            stats["errors"] += 1

    for k, v in hash_data.items():
        if _is_expired(k):
            stats["skipped_expired"] += 1
            continue
        try:
            if await _retry(_client.exists, k):
                stats["skipped_existing"] += 1
                continue
            mapping = {str(fk): str(fv) for fk, fv in v.items()}
            if mapping:
                await _retry(_client.hset, k, mapping=mapping)
                await _apply_ttl(k)
                stats["migrated_keys"] += 1
        except Exception:
            stats["errors"] += 1

    for k, v in set_data.items():
        if _is_expired(k):
            stats["skipped_expired"] += 1
            continue
        try:
            if await _retry(_client.exists, k):
                stats["skipped_existing"] += 1
                continue
            members = [str(m) for m in v]
            if members:
                await _retry(_client.sadd, k, *members)
                await _apply_ttl(k)
                stats["migrated_keys"] += 1
        except Exception:
            stats["errors"] += 1

    for k, v in list_data.items():
        if _is_expired(k):
            stats["skipped_expired"] += 1
            continue
        try:
            if await _retry(_client.exists, k):
                stats["skipped_existing"] += 1
                continue
            items = [str(i) for i in v]
            if items:
                await _retry(_client.rpush, k, *items)
                await _apply_ttl(k)
                stats["migrated_keys"] += 1
        except Exception:
            stats["errors"] += 1

    for k, v in zset_data.items():
        if _is_expired(k):
            stats["skipped_expired"] += 1
            continue
        try:
            if await _retry(_client.exists, k):
                stats["skipped_existing"] += 1
                continue
            mapping = {str(m): float(s) for m, s in v.items()}
            if mapping:
                await _retry(_client.zadd, k, mapping)
                await _apply_ttl(k)
                stats["migrated_keys"] += 1
        except Exception:
            stats["errors"] += 1

    if stats["errors"] == 0:
        try:
            await _retry(_client.set, _MIGRATION_DONE_KEY, "1")
        except Exception:
            pass

    try:
        await _retry(_client.delete, _MIGRATION_LOCK_KEY)
    except Exception:
        pass

    return stats


async def _dump_key(key: str) -> dict | None:
    try:
        key_type = await _retry(_client.type, key)
        if key_type == "string":
            value = await _retry(_client.get, key)
        elif key_type == "hash":
            value = await _retry(_client.hgetall, key)
        elif key_type == "set":
            value = list(await _retry(_client.smembers, key))
        elif key_type == "list":
            value = await _retry(_client.lrange, key, 0, -1)
        elif key_type == "zset":
            pairs = await _retry(_client.zrange, key, 0, -1, withscores=True)
            value = {m: s for m, s in pairs}
        else:
            return None
        ttl = await _retry(_client.ttl, key)
        return {"type": key_type, "value": value, "ttl": ttl}
    except Exception:
        return None


async def export_by_scan(match: str = "*") -> dict:
    result = {}
    cursor = 0
    while True:
        cursor, batch = await _retry(_client.scan, cursor=cursor, match=match, count=500)
        for k in batch:
            if any(k.startswith(p) for p in _INTERNAL_KEY_PREFIXES):
                continue
            dumped = await _dump_key(k)
            if dumped is not None:
                result[k] = dumped
        if cursor == 0:
            break
    return result


async def export_all() -> dict:
    return await export_by_scan("*")


async def export_bot(bot_id: str) -> dict:
    return await export_by_scan(f"{bot_id}:*")


async def export_music_cache() -> dict:
    return await export_by_scan("music_cache:*")


r = RedisFake()

Redis = RedisFake
ConnectionPool = ConnectionPoolFake

# ==== خريطة يوزرنيم <-> آيدي مشتركة بين كل البوتات (بدون عزل bot_id) ====
# الهدف: أي مستخدم يُرى ولو مرة واحدة (برسالة عادية) من أي بوت بالكلاستر
# يُحفَظ آيدي@يوزرنيم الخاص به هنا، فتتوفر لاحقاً لكل البوتات عبر aiogram
# مباشرة دون أي حاجة لطلب Pyrogram في كل مرة لنفس المستخدم.
_USERNAME_MAP_TTL = 30 * 24 * 3600  # 30 يوماً (اليوزرنيمات قد تتغيّر لاحقاً)


async def cache_username_id(username: str, user_id) -> None:
    if not username or not user_id:
        return
    try:
        uname = str(username).lstrip('@').strip().lower()
        if not uname:
            return
        await r.setex(f"usermap:u:{uname}", _USERNAME_MAP_TTL, str(int(user_id)))
    except Exception:
        pass


async def get_cached_username_id(username: str):
    if not username:
        return None
    try:
        uname = str(username).lstrip('@').strip().lower()
        if not uname:
            return None
        val = await r.get(f"usermap:u:{uname}")
        if val is None:
            return None
        return int(str(val).strip())
    except Exception:
        return None


__all__ = [
    'Redis',
    'ConnectionPool',
    'r',
    'RedisFake',
    'get_isolated_redis',
    'get_bot_redis',
    'get_sudoers_async',
    'is_sudoer_async',
    'redis_healthcheck',
    'migrate_lmdb_to_redis',
    'export_all',
    'export_bot',
    'export_music_cache',
    'REDIS_URL',
    'cache_username_id',
    'get_cached_username_id',
]

sys.modules['helpers.redis_helper.asyncio'] = sys.modules['helpers.redis']