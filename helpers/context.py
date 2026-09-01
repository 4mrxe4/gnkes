
from __future__ import annotations

import asyncio
import contextvars
import copy as copy_module
import inspect
import itertools
import json
import logging
import os
import sys
import time
import traceback
from typing import Any, Dict, List, Optional, Tuple

from aiogram import Bot, Dispatcher, F, Router
from aiogram.utils.magic_filter import MagicFilter
from aiogram.types import Message as AioMessage

from compat import (
    CompatClient as CompatClientClass,
    CompatMessage,
    CompatCallbackQuery,
    CompatChatMemberUpdated,
    CompatChatJoinRequest,
    CompatInlineQuery,
    _HandlerSpec,
    build_aiogram_filter,
    ContinuePropagation,
    StopPropagation,
)

logger = logging.getLogger("FinalMusic")



_current_bot_id_var: contextvars.ContextVar[str] = contextvars.ContextVar("current_bot_id", default=None)
_global_is_parent_var: contextvars.ContextVar[bool] = contextvars.ContextVar("global_is_parent", default=False)
_current_user_id_var: contextvars.ContextVar[Optional[int]] = contextvars.ContextVar("current_user_id", default=None)


def get_current_bot_id() -> Optional[str]:
    return _current_bot_id_var.get()


def set_current_bot_id(bot_id: str):
    _current_bot_id_var.set(bot_id)


def get_current_user_id() -> Optional[int]:
    return _current_user_id_var.get()


def set_current_user_id(user_id: Optional[int]):
    _current_user_id_var.set(user_id)


def set_global_is_parent(value: bool):
    _global_is_parent_var.set(bool(value))


def get_global_is_parent() -> bool:
    return _global_is_parent_var.get()



_bot_contexts: Dict[str, dict] = {}


def get_bot_context(bot_id: str = None) -> dict:
    if bot_id is None:
        bot_id = get_current_bot_id()
    if bot_id and bot_id in _bot_contexts:
        return _bot_contexts[bot_id]
    return {}


def get_dev_final(client=None) -> str:
    if client is not None:
        bid = getattr(client, "bot_id", None) or getattr(client, "dev_final", None)
        if bid:
            return str(bid)
    bid = get_current_bot_id()
    if bid:
        return str(bid)
    try:
        import settings
        return str(settings.Dev_FINAL)
    except Exception:
        return "unknown"


def get_redis(client=None):
    if client is not None:
        r = getattr(client, "redis", None)
        if r is not None:
            return r
    bot_id = get_current_bot_id()
    if bot_id and bot_id in _bot_contexts:
        r = _bot_contexts[bot_id].get("redis")
        if r is not None:
            return r
    try:
        import settings
        r = getattr(settings, "r", None)
        if r is not None:
            return r
    except Exception:
        pass
    return None


def get_isolated_redis(bot_id: str = None):
    from helpers.redis import RedisFake
    bid = bot_id or get_current_bot_id()
    if bid:
        return RedisFake(bot_id=bid)
    return RedisFake()


def get_config_from_client(client=None):
    if client is not None:
        cfg = getattr(client, "bot_config", None)
        if cfg is not None:
            return cfg
    bot_id = get_current_bot_id()
    if bot_id and bot_id in _bot_contexts:
        cfg = _bot_contexts[bot_id].get("config")
        if cfg is not None:
            return cfg
    try:
        import settings
        return settings.config
    except Exception:
        return None


def get_bot_from_client(client=None):
    if client is not None:
        b = getattr(client, "_bot", None)
        if b is not None:
            return b
    bot_id = get_current_bot_id()
    if bot_id and bot_id in _bot_contexts:
        return _bot_contexts[bot_id].get("client")
    return None


def get_config():
    return get_config_from_client(None)


def get_bot_client():
    bot_id = get_current_bot_id()
    if bot_id and bot_id in _bot_contexts:
        return _bot_contexts[bot_id].get("client")
    return None


def get_bot_owner():
    bot_id = get_current_bot_id()
    if bot_id and bot_id in _bot_contexts:
        return _bot_contexts[bot_id].get("owner_id")
    return None
    
def get_parent_client():
    """تُعيد كائن البوت الرئيسي/الأب أو None لتفادي خطأ ImportError عند الاستدماء"""
    from compat import Client
    return getattr(Client, "parent_client", None)


_bot_k_cache: Dict[str, str] = {}


def _cache_bot_k(bot_id: str, value: str) -> None:
    """يخزّن آخر قيمة معروفة لـ botkey لبوت معيّن (يُستخدم داخل حلقة الحدث)."""
    try:
        if bot_id and value:
            _bot_k_cache[str(bot_id)] = str(value)
    except Exception:
        pass


def _resolve_bot_k_sync() -> str:
    """قراءة botkey من Redis للمفتاح المعزول {current_bot_id}:botkey.

    تعمل من سياق متزامن (حيث يستدعيها _LiveStrProxy / get_global_k /
    BotContext.get_global_k) عبر جدولة coroutine على حلقة الحدث الجارية أو
    run_coroutine_threadsafe خارجها. عند غياب القيمة تعيد الثابت '⇜' فقط.

    ملاحظة حرجة (إصلاح التجمّد): عندما تُستدعى هذه الدالة من نفس حلقة الحدث
    (نفس الخيط)، استدعاء run_coroutine_threadsafe(...).result() هو deadlock ذاتي
    — يَحجب الخيط الوحيد الذي يشغّل الحلقة فلا يكتمل الـ future أبداً. لذلك
    داخل حلقة تعمل نعيد آخر قيمة مخزّنة في _bot_k_cache (أو '⇜') دون أي حجب.
    """
    try:
        bot_id = get_current_bot_id()
        if not bot_id:
            return "\u21dc"
        r = get_redis()
        if r is None:
            return _bot_k_cache.get(bot_id, "\u21dc")

        import asyncio as _aio

        async def _read():
            try:
                val = await r.get(f"{bot_id}:botkey")
                if val is not None:
                    if isinstance(val, bytes):
                        val = val.decode("utf-8", "replace")
                    if val:
                        return str(val)
            except Exception:
                pass
            return "\u21dc"

        try:
            loop = _aio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop is not None and loop.is_running():
            # استدعاء متزامن من داخل حلقة الحدث نفسها:
            # لا يمكن استخدام run_coroutine_threadsafe(...).result() هنا
            # (self-deadlock → تجمّد المشروع). نعيد آخر قيمة معروفة فوراً،
            # ونُحدّث الكاش لاحقاً بشكل غير حاجب (background task).
            cached = _bot_k_cache.get(bot_id, "\u21dc")
            try:
                async def _warm_cache():
                    value = await _read()
                    _cache_bot_k(bot_id, value)
                loop.create_task(_warm_cache())
            except Exception:
                pass
            return cached
        else:
            try:
                value = _aio.run(_read())
                _cache_bot_k(bot_id, value)
                return value
            except Exception:
                return _bot_k_cache.get(bot_id, "\u21dc")
    except Exception:
        return "\u21dc"


def get_bot_k():
    return _resolve_bot_k_sync()


def get_queue():
    bot_id = get_current_bot_id()
    if bot_id and bot_id in _bot_contexts:
        return _bot_contexts[bot_id].get("queue")
    return None


def get_tune():
    bot_id = get_current_bot_id()
    if bot_id and bot_id in _bot_contexts:
        return _bot_contexts[bot_id].get("tune")
    return None


def get_yt():
    bot_id = get_current_bot_id()
    if bot_id and bot_id in _bot_contexts:
        return _bot_contexts[bot_id].get("yt")
    return None


def get_tg():
    bot_id = get_current_bot_id()
    if bot_id and bot_id in _bot_contexts:
        return _bot_contexts[bot_id].get("tg")
    return None


def get_preload():
    bot_id = get_current_bot_id()
    if bot_id and bot_id in _bot_contexts:
        return _bot_contexts[bot_id].get("preload")
    return None


def get_userbot():
    bot_id = get_current_bot_id()
    if bot_id and bot_id in _bot_contexts:
        return _bot_contexts[bot_id].get("userbot")
    return None


def get_sudoers():
    bot_id = get_current_bot_id()
    if bot_id and bot_id in _bot_contexts:
        return _bot_contexts[bot_id].get("sudoers")
    return None


async def is_sudoer(user_id: int) -> bool:
    sudoers = get_sudoers()
    if sudoers is not None:
        try:
            return int(user_id) in sudoers
        except Exception:
            return False
    bot_id = get_current_bot_id()
    if bot_id:
        from helpers.redis import RedisFake
        r = RedisFake(bot_id=bot_id)
        members = await r.smembers(f"sudoers:{bot_id}")
        return str(user_id) in members
    return False


async def add_pending_save(video_id: str, title: str = None, duration: int = 0):
    """يُبقي نفس السلوك الأصلي (تسجيل طلب حفظ مؤجل)."""
    try:
        bot_id = get_current_bot_id()
        if not bot_id:
            return
        from helpers.redis import RedisFake
        r = RedisFake(bot_id=bot_id)
        key = f"pending_saves:{bot_id}"
        data = {"video_id": video_id, "title": title, "duration": duration, "ts": time.time()}
        await r.rpush(key, json.dumps(data))
        await r.expire(key, 86400)
    except Exception:
        pass



def inject_bot_data(client, bot_id: str, owner_id: int, redis_instance, config_instance,
                    is_parent: bool = False):
    try:
        client.bot_id = bot_id
        client.dev_final = bot_id
        client.owner_id = owner_id
        client.redis = redis_instance
        client.bot_config = config_instance
        client.is_parent = is_parent
        client.owner = owner_id
    except Exception:
        pass


def update_global_context_sync():
    """مزامنة السياق العام (المستخدمة في تحميل الـ plugins)."""
    bot_id = get_current_bot_id()
    if bot_id and bot_id not in _bot_contexts:
        from helpers.redis import RedisFake
        _bot_contexts[bot_id] = {
            "bot_id": bot_id,
            "redis": RedisFake(bot_id=bot_id),
            "is_parent": get_global_is_parent(),
        }


async def update_global_context():
    bot_id = get_current_bot_id()
    if bot_id and bot_id not in _bot_contexts:
        from helpers.redis import RedisFake
        _bot_contexts[bot_id] = {
            "bot_id": bot_id,
            "redis": RedisFake(bot_id=bot_id),
            "is_parent": get_global_is_parent(),
        }


def get_global_r():
    bot_id = get_current_bot_id()
    if bot_id and bot_id in _bot_contexts:
        r = _bot_contexts[bot_id].get("redis")
        if r is not None:
            return r
    try:
        import settings
        r = getattr(settings, "r", None)
        if r is not None:
            return r
    except Exception:
        pass
    return None


def get_global_dev():
    return get_dev_final(None)


def get_global_k():
    return get_bot_k()


def reset_global_context():
    _current_bot_id_var.set(None)
    _global_is_parent_var.set(False)


def get_all_bot_contexts() -> Dict[str, dict]:
    return _bot_contexts


def get_bot_context_count() -> int:
    return len(_bot_contexts)



def _wrap_callback(original_callback, bot_id: str):
    """يلفّ الدالة الأصلية (c, m) لتعمل ضمن سياق aiogram وتلتقط الأخطاء."""

    async def wrapper(*args, **kwargs):
        aio_message = None
        aio_callback = None
        aio_event = None
        aio_query = None
        for arg in args:
            if isinstance(arg, AioMessage):
                aio_message = arg
            elif hasattr(arg, "__class__") and arg.__class__.__name__ == "CallbackQuery":
                aio_callback = arg
            elif hasattr(arg, "__class__") and arg.__class__.__name__ == "ChatMemberUpdated":
                aio_event = arg
            elif hasattr(arg, "__class__") and arg.__class__.__name__ == "ChatJoinRequest":
                aio_event = arg
            elif hasattr(arg, "__class__") and arg.__class__.__name__ == "InlineQuery":
                aio_query = arg
        for value in kwargs.values():
            if isinstance(value, AioMessage):
                aio_message = value
            elif hasattr(value, "__class__") and value.__class__.__name__ == "CallbackQuery":
                aio_callback = value
            elif hasattr(value, "__class__") and value.__class__.__name__ == "ChatMemberUpdated":
                aio_event = value
            elif hasattr(value, "__class__") and value.__class__.__name__ == "ChatJoinRequest":
                aio_event = value
            elif hasattr(value, "__class__") and value.__class__.__name__ == "InlineQuery":
                aio_query = value

        from aiogram import Bot as AioBot
        bot = None
        for arg in args:
            if isinstance(arg, AioBot):
                bot = arg
                break
        if bot is None:
            for value in kwargs.values():
                if isinstance(value, AioBot):
                    bot = value
                    break
        if bot is None:
            ctx = _bot_contexts.get(bot_id)
            if ctx:
                client = ctx.get("client")
                if client is not None:
                    bot = getattr(client, "_bot", None)
        if bot is None:
            try:
                from aiogram import Bot as AioBot2
                ctx = _bot_contexts.get(bot_id)
                if ctx:
                    bot = ctx.get("aiogram_bot")
            except Exception:
                bot = None

        if bot is None:
            return None

        client = CompatClientClass(bot, bot_id=bot_id, bot_token=getattr(bot, "token", None) or "",
                                   owner_id=None, redis=None)
        ctx = _bot_contexts.get(bot_id)
        if ctx:
            client.redis = ctx.get("redis")
            client.bot_config = ctx.get("config")
            client.owner_id = ctx.get("owner_id")
            client.is_parent = ctx.get("is_parent", False)
        else:
            client.redis = None

        if aio_message is not None:
            compat = CompatMessage(aio_message, client)
        elif aio_callback is not None:
            compat = CompatCallbackQuery(aio_callback, client)
        elif aio_event is not None:
            cls_name = aio_event.__class__.__name__
            if cls_name == "ChatMemberUpdated":
                compat = CompatChatMemberUpdated(aio_event, client)
            elif cls_name == "ChatJoinRequest":
                compat = CompatChatJoinRequest(aio_event, client)
            else:
                compat = None
        elif aio_query is not None:
            compat = CompatInlineQuery(aio_query, client)
        else:
            compat = None

        event_user_id = None
        for src in (aio_message, aio_callback, aio_event, aio_query):
            if src is not None and getattr(src, "from_user", None) is not None:
                event_user_id = src.from_user.id
                break

        old_bot_id = get_current_bot_id()
        old_is_parent = get_global_is_parent()
        old_user_id = get_current_user_id()
        try:
            set_current_bot_id(bot_id)
            set_current_user_id(event_user_id)
            # الإصلاح: set_global_is_parent() لم تكن تُضبط هنا لكل تحديث،
            # فكانت get_global_is_parent() أثناء معالجة الرسائل الفعلية تعكس
            # آخر قيمة ضُبطت وقت الإقلاع (لأي بوت كان يُهيَّأ حينها) بدل حالة
            # البوت الحالي الحقيقية. هذا يسبب سلوكاً غير متسق (مثل فروع
            # أرشفة/تخزين الميوزك المعتمدة على is_parent) بين البوت الأب
            # والأبناء أثناء التشغيل الفعلي.
            set_global_is_parent(bool(ctx.get("is_parent", False)) if ctx else False)
            if compat is not None:
                try:
                    sig = inspect.signature(original_callback)
                    required = [
                        p for p in sig.parameters.values()
                        if p.default is inspect.Parameter.empty
                        and p.kind in (inspect.Parameter.POSITIONAL_ONLY,
                                       inspect.Parameter.POSITIONAL_OR_KEYWORD)
                    ]
                    if len(required) >= 3:
                        return await original_callback(client, compat, get_bot_k())
                except (TypeError, ValueError):
                    pass
                return await original_callback(client, compat)
            return await original_callback(client, *args, **kwargs)
        except (StopPropagation, ContinuePropagation):
            raise
        except Exception as e:
            tb = traceback.extract_tb(e.__traceback__)
            last_frame = tb[-1] if tb else None
            logger.error(
                f"\n[معزول] خطأ في هاندلر:\n"
                f"    البوت: {bot_id}\n"
                f"    الملف: {last_frame.filename if last_frame else 'unknown'}\n"
                f"    السطر: {last_frame.lineno if last_frame else 0}\n"
                f"    الدالة: {last_frame.name if last_frame else 'unknown'}\n"
                f"    نوع الخطأ: {type(e).__name__}\n"
                f"    الرسالة: {str(e)}\n"
            )
            return None
        finally:
            if old_bot_id:
                set_current_bot_id(old_bot_id)
            else:
                set_current_bot_id(None)
            set_global_is_parent(old_is_parent)
            set_current_user_id(old_user_id)

    return wrapper



_KIND_TO_OBSERVER = {
    "message": "message",
    "edited_message": "edited_message",
    "callback_query": "callback_query",
    "chat_member_updated": ("chat_member", "my_chat_member"),
    "inline_query": "inline_query",
    "chat_join_request": "chat_join_request",
}

_bot_kind_handlers: Dict[Tuple[str, str], List[Tuple[int, Any, Any, _HandlerSpec]]] = {}


async def _check_filter(flt, event) -> bool:
    """يستدعي فلتر aiogram (أو مركّب and_f/or_f/invert_f أو MagicFilter أو
    فلتر مخصص) بأكثر شكل متوافق ممكن. بعض الفلاتر (Command/CommandStart)
    تحتاج وسيط bot إضافي، وبعضها (MagicFilter، الفلاتر المخصصة) تقبل قيمة
    الحدث فقط — لذا نجرّب مع bot أولاً ثم نتراجع بدونه."""
    if flt is None:
        return True
    if isinstance(flt, MagicFilter):
        try:
            return bool(flt.resolve(event))
        except Exception:
            return False
    bot = getattr(event, "bot", None)
    try:
        result = flt(event, bot=bot) if bot is not None else flt(event)
    except TypeError:
        try:
            result = flt(event)
        except Exception:
            return False
    except Exception:
        return False
    if inspect.isawaitable(result):
        try:
            result = await result
        except Exception:
            return False
    return bool(result)


def _make_group_dispatcher(bot_id: str, kind: str):
    """يبني نقطة الدخول الوحيدة لهذا (bot_id, kind) على الـ router والتي
    تحاكي دورة Pyrogram الكاملة عبر كل الـ groups."""

    async def _dispatch(event, **_kwargs):
        entries = _bot_kind_handlers.get((bot_id, kind), [])
        if not entries:
            return
        for _group, group_iter in itertools.groupby(entries, key=lambda e: e[0]):
            for _g, flt, cb, _spec in group_iter:
                try:
                    matched = await _check_filter(flt, event)
                except Exception:
                    matched = False
                if not matched:
                    continue
                try:
                    await cb(event)
                except StopPropagation:
                    return
                except ContinuePropagation:
                    continue
                except Exception:
                    logger.error(
                        f"[معزول] خطأ غير متوقع أثناء تنفيذ handler (bot={bot_id}, kind={kind}):\n"
                        f"{traceback.format_exc()}"
                    )
                    break
                else:
                    break

    return _dispatch


def isolated_add_handler(dispatcher_or_router, handler, group: int, bot_id: str):
    """يسجّل handler واحد ضمن سجل (bot_id, kind) الداخلي بدل تسجيله مباشرة
    كـ handler مستقل على aiogram Router (الذي يوقف الانتشار عند أول
    تطابق). يضمن أيضاً وجود نقطة دخول وحيدة لكل (router, kind) تُطبّق
    خوارزمية Pyrogram groups (انظر _make_group_dispatcher أعلاه)."""
    spec = handler
    if not isinstance(spec, _HandlerSpec):
        return None

    original_callback = getattr(spec, "callback", None)
    if original_callback is None and hasattr(spec, "_func"):
        original_callback = spec._func
    if original_callback is None:
        return None

    router = dispatcher_or_router
    wrapped = _wrap_callback(original_callback, bot_id)
    aio_filter = build_aiogram_filter(spec)

    observer_names = _KIND_TO_OBSERVER.get(spec.kind)
    if observer_names is None:
        return wrapped
    if router is None:
        return wrapped
    if isinstance(observer_names, str):
        observer_names = (observer_names,)

    key = (bot_id, spec.kind)
    entries = _bot_kind_handlers.setdefault(key, [])
    entries.append((int(group or 0), aio_filter, wrapped, spec))
    entries.sort(key=lambda e: e[0])

    installed = getattr(router, "_pyrogram_group_dispatch_installed", None)
    if installed is None:
        installed = set()
        try:
            router._pyrogram_group_dispatch_installed = installed
        except Exception:
            pass
    if key not in installed:
        for observer_name in observer_names:
            observer = getattr(router, observer_name, None)
            if observer is not None:
                observer.register(_make_group_dispatcher(bot_id, spec.kind))
        installed.add(key)

    return wrapped


def reset_bot_handlers(bot_id: str):
    """يمسح كل الـ handlers المسجّلة سابقاً لهذا bot_id من سجل الـ groups
    الداخلي. يجب استدعاؤها قبل إعادة إرفاق (attach) الـ plugins على بوت
    (مثلاً عند reload_bot) حتى لا تتراكم نسخ مكررة من نفس الـ handlers
    وتُنفَّذ أكثر من مرة لكل تحديث في كل مرة يُعاد فيها التشغيل."""
    for key in [k for k in _bot_kind_handlers if k[0] == bot_id]:
        del _bot_kind_handlers[key]


def isolated_add_handlers(client, handlers_list, bot_id):
    """يسجّل قائمة handlers على الـ dispatcher المربوط بالـ client.

    handlers_list قد يكون:
      - قائمة tuples (handler, group) — كما في الأصل
      - قائمة _HandlerSpec — من جمعنا
    """
    from helpers.redis import RedisFake
    ctx = _bot_contexts.get(bot_id)
    router = None
    if ctx:
        router = ctx.get("router")
    if router is None:
        from aiogram import Router as AioRouter
        router = AioRouter(name=f"bot_{bot_id}")
        _bot_contexts[bot_id]["router"] = router

    for item in handlers_list:
        if isinstance(item, tuple):
            handler, group = item
        else:
            handler = item
            group = getattr(handler, "group", 0)
        isolated_add_handler(router, handler, group, bot_id)


def sync_client_identity(client, me):
    """مزامنة هوية العميل مع بيانات المستخدم (تُستخدم بعد get_me)."""
    try:
        if client and me:
            if hasattr(client, "set_me"):
                client.set_me(me)
            if not hasattr(client, "bot_id"):
                bot_id = get_current_bot_id()
                if bot_id:
                    client.bot_id = bot_id
            if hasattr(client, "bot_id") and client.bot_id and getattr(me, "username", None):
                r = get_redis(client)
                if r:
                    try:
                        loop = asyncio.get_running_loop()
                        loop.create_task(r.set(f"{client.bot_id}:bot_username", me.username))
                    except RuntimeError:
                        try:
                            asyncio.run_coroutine_threadsafe(
                                r.set(f"{client.bot_id}:bot_username", me.username),
                                asyncio.get_event_loop(),
                            )
                        except Exception:
                            pass
            return True
    except Exception:
        pass
    return False



class _LiveProxy:
    __slots__ = ("_getter", "_label")

    def __init__(self, getter, label: str):
        object.__setattr__(self, "_getter", getter)
        object.__setattr__(self, "_label", label)

    def _target(self):
        return self._getter()

    def __getattr__(self, name):
        target = self._target()
        if target is None:
            bot_id = get_current_bot_id()
            raise AttributeError(
                f"[{self._label}] لا يوجد سياق بوت نشط حالياً "
                f"(current_bot_id={bot_id!r}) عند الوصول إلى '{name}'"
            )
        try:
            return getattr(target, name)
        except AttributeError as e:
            raise AttributeError(
                f"[{self._label}] الكائن {target.__class__.__name__} لا يحتوي على الخاصية '{name}'"
            ) from e

    def __setattr__(self, name, value):
        target = self._target()
        if target is None:
            raise AttributeError(
                f"[{self._label}] لا يوجد سياق بوت نشط حالياً لضبط '{name}'"
            )
        setattr(target, name, value)

    def __call__(self, *args, **kwargs):
        target = self._target()
        if target is None:
            raise RuntimeError(f"[{self._label}] لا يوجد سياق بوت نشط حالياً")
        return target(*args, **kwargs)

    def __bool__(self):
        return self._target() is not None

    def __repr__(self):
        return f"<LiveProxy[{self._label}] -> {self._target()!r}>"

    def __getitem__(self, item):
        return self._target()[item]

    def __setitem__(self, item, value):
        self._target()[item] = value

    def __iter__(self):
        return iter(self._target())

    def __contains__(self, item):
        return item in self._target()

    def __len__(self):
        return len(self._target())


class _LiveStrProxy:
    __slots__ = ("_getter", "_label", "_default")

    def __init__(self, getter, label: str, default: str = ""):
        object.__setattr__(self, "_getter", getter)
        object.__setattr__(self, "_label", label)
        object.__setattr__(self, "_default", default)

    def _value(self) -> str:
        v = self._getter()
        return v if v is not None else self._default

    def __str__(self):
        return str(self._value())

    def __repr__(self):
        return repr(self._value())

    def __format__(self, spec):
        return format(str(self._value()), spec)

    def __eq__(self, other):
        return str(self._value()) == other

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(str(self._value()))

    def __add__(self, other):
        return str(self._value()) + other

    def __radd__(self, other):
        return other + str(self._value())

    def __contains__(self, item):
        return item in str(self._value())

    def __len__(self):
        return len(str(self._value()))

    def __bool__(self):
        return bool(self._value())

    def __iter__(self):
        return iter(str(self._value()))

    def __getitem__(self, item):
        return str(self._value())[item]


redis_proxy = _LiveProxy(lambda: get_redis(), "redis")
config_proxy = _LiveProxy(lambda: get_config(), "config")
app_proxy = _LiveProxy(lambda: get_bot_client(), "app")
queue_proxy = _LiveProxy(lambda: get_queue(), "queue")
tune_proxy = _LiveProxy(lambda: get_tune(), "tune")
yt_proxy = _LiveProxy(lambda: get_yt(), "yt")
tg_proxy = _LiveProxy(lambda: get_tg(), "tg")
preload_proxy = _LiveProxy(lambda: get_preload(), "preload")
userbot_proxy = _LiveProxy(lambda: get_userbot(), "userbot")
dev_final_proxy = _LiveStrProxy(lambda: get_dev_final(), "Dev_FINAL", default="unknown")
k_proxy = _LiveStrProxy(lambda: get_bot_k(), "k", default="\u21dc")



class FilteredList(list):
    def __init__(self, iterable=None):
        super().__init__(iterable or [])

    def filter(self, predicate=None):
        if predicate is None:
            return FilteredList(self)
        return FilteredList([i for i in self if predicate(i)])

    def exclude(self, *items):
        return FilteredList([i for i in self if i not in items])


class FilteredSet(set):
    def __init__(self, iterable=None):
        super().__init__(iterable or [])

    def filter(self, predicate=None):
        if predicate is None:
            return FilteredSet(self)
        return FilteredSet(i for i in self if predicate(i))

    def exclude(self, *items):
        return FilteredSet(i for i in self if i not in items)



class BotContext:
    @staticmethod
    def get_current_bot() -> Optional[str]:
        return get_current_bot_id()

    @staticmethod
    def set_current_bot(bot_id: str):
        set_current_bot_id(bot_id)

    @staticmethod
    def get_dev_final(client=None) -> str:
        return get_dev_final(client)

    @staticmethod
    def get_redis(client=None):
        return get_redis(client)

    @staticmethod
    def get_isolated_redis(bot_id: str = None):
        return get_isolated_redis(bot_id)

    @staticmethod
    def get_config_from_client(client=None):
        return get_config_from_client(client)

    @staticmethod
    def get_bot_from_client(client=None):
        return get_bot_from_client(client)

    @staticmethod
    def get_global_r():
        return get_global_r()

    @staticmethod
    def get_global_dev():
        return get_global_dev()

    @staticmethod
    def get_global_k():
        return get_global_k()

    @staticmethod
    def get_all_bot_contexts():
        return _bot_contexts

    @staticmethod
    def get_bot_context_count():
        return len(_bot_contexts)


__all__ = [
    "get_current_bot_id",
    "get_current_user_id",
    "set_current_user_id",
    "set_current_bot_id",
    "set_global_is_parent",
    "get_global_is_parent",
    "get_bot_context",
    "get_dev_final",
    "get_redis",
    "get_isolated_redis",
    "get_config_from_client",
    "get_bot_from_client",
    "get_config",
    "get_bot_client",
    "get_bot_owner",
    "get_bot_k",
    "get_queue",
    "get_tune",
    "get_yt",
    "get_tg",
    "get_preload",
    "get_userbot",
    "get_sudoers",
    "is_sudoer",
    "add_pending_save",
    "inject_bot_data",
    "update_global_context_sync",
    "update_global_context",
    "get_global_r",
    "get_global_dev",
    "get_global_k",
    "reset_global_context",
    "get_all_bot_contexts",
    "get_bot_context_count",
    "isolated_add_handler",
    "isolated_add_handlers",
    "reset_bot_handlers",
    "sync_client_identity",
    "redis_proxy",
    "config_proxy",
    "app_proxy",
    "queue_proxy",
    "tune_proxy",
    "yt_proxy",
    "tg_proxy",
    "preload_proxy",
    "userbot_proxy",
    "dev_final_proxy",
    "k_proxy",
    "FilteredList",
    "FilteredSet",
    "BotContext",
    "_bot_contexts",
]