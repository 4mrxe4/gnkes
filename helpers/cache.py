"""
طبقة كاش عامة (cache-aside) فوق Redis — الهدف تعميم نفس الفكرة المطبّقة
يدوياً على أمر "المالك" في plugins/handlers.py على أي مكان آخر في الكود
يجلب بيانات مكلفة (نداء شبكة لتيليجرام، أو حساب/تجميع من عدة مفاتيح Redis)
نادراً ما تتغيّر.

الفكرة: بدل إعادة الجلب في كل استدعاء، نخزّن النتيجة في Redis بمدة صلاحية
(TTL) مناسبة لطبيعة البيانات، ولا نعيد الجلب إلا بعد انتهاء تلك المدة —
أو عند إلغاء الكاش يدوياً بسبب تغيير فعلي معروف (invalidate_cache).

الاستخدام المباشر (الأنسب لمعظم الحالات في هذا المشروع):

    from helpers.cache import cached_fetch

    async def get_owner_info(chat_id, dev_id):
        return await cached_fetch(
            key=f"{chat_id}:ownerInfoCache:{dev_id}",
            fetch=lambda: _fetch_owner_live(chat_id, dev_id),
            ttl=86400,
        )

fetch يُستدعى فقط عند غياب/انتهاء الكاش. القيمة تُخزَّن كـ JSON تلقائياً.

للاستخدام كديكوريتر على دالة كاملة (مفيد لدوال بلا حاجة لصياغة مفتاح يدوياً
في كل موضع استدعاء):

    from helpers.cache import redis_cached

    @redis_cached(ttl=120, key_func=lambda chat_id: f"{chat_id}:admins")
    async def get_cached_admins(chat_id, bot):
        return await bot.get_chat_administrators(chat_id)

ملاحظة TTL مقترحة حسب طبيعة البيانات (دليل عام وليس قاعدة صارمة):
- بيانات شبه ثابتة (اسم/صورة مالك، إعدادات بوت): ساعات إلى يوم كامل.
- بيانات تتغيّر أحياناً (قائمة أدمنية مجموعة): دقيقة إلى بضع دقائق.
- بيانات حيّة (حالة عداد، نتيجة لعبة): لا تُكاش إطلاقاً أو TTL قصير جداً (ثوانٍ).
"""

import json
from typing import Any, Awaitable, Callable, Optional

from helpers.context import redis_proxy as r


def _serialize(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, default=str)


def _deserialize(raw) -> Any:
    if raw is None:
        return None
    text = raw.decode("utf-8") if isinstance(raw, bytes) else raw
    try:
        return json.loads(text)
    except Exception:
        # قيمة نصية بسيطة غير JSON (نادر، لكن نتعامل معه بأمان)
        return text


async def cached_fetch(key: str, fetch: Callable[[], Awaitable[Any]],
                        ttl: int = 300, force_refresh: bool = False) -> Any:
    """يقرأ `key` من Redis. لو موجود (ولم تنته صلاحيته) يعيده مباشرة بدون
    استدعاء `fetch`. غير ذلك يستدعي `fetch()` (async)، يخزّن الناتج بـ TTL،
    ويعيده. force_refresh=True يتجاوز الكاش ويجلب من جديد (مفيد بعد تغيير
    مؤكد لا يستحق انتظار انتهاء الـ TTL)."""
    if not force_refresh:
        try:
            cached = await r.get(key)
        except Exception:
            cached = None
        if cached is not None:
            value = _deserialize(cached)
            if value is not None:
                return value

    value = await fetch()
    try:
        await r.set(key, _serialize(value), ex=ttl)
    except Exception:
        pass
    return value


async def invalidate_cache(key: str) -> None:
    """يحذف مفتاح كاش يدوياً — يُستخدم عند حدوث تغيير معروف (مثال: تغيّر
    المالك، تعديل إعداد) بدل انتظار انتهاء الـ TTL طبيعياً."""
    try:
        await r.delete(key)
    except Exception:
        pass


def redis_cached(ttl: int = 300, key_func: Optional[Callable[..., str]] = None,
                  key_prefix: Optional[str] = None):
    """ديكوريتر لدالة async: يكاش ناتجها في Redis حسب مفتاح مُشتق من
    `key_func(*args, **kwargs)`، أو من `key_prefix` + تمثيل نصي للوسائط
    لو لم يُمرَّر key_func."""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            if key_func is not None:
                key = key_func(*args, **kwargs)
            else:
                prefix = key_prefix or func.__name__
                key = f"{prefix}:{args}:{sorted(kwargs.items())}"

            async def _fetch():
                return await func(*args, **kwargs)

            return await cached_fetch(key, _fetch, ttl=ttl)
        wrapper.__name__ = getattr(func, "__name__", "wrapped")
        wrapper.cache_invalidate = lambda *a, **kw: invalidate_cache(
            key_func(*a, **kw) if key_func else f"{key_prefix or func.__name__}:{a}:{sorted(kw.items())}"
        )
        return wrapper
    return decorator
