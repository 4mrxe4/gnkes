"""
طبقة HTTP غير-محجوبة (non-blocking) موحّدة، تحل محل نداءات requests.* المباشرة
المنتشرة في الـ plugins، والتي كانت تجمّد كامل event loop (كل الكلسترات، كل
البوتات) لحظة كل استدعاء لأن مكتبة requests متزامنة (blocking).

كل الدوال هنا async وتستخدم جلسة aiohttp واحدة مشتركة معاد استخدامها
(connection pooling حقيقي) بدل فتح اتصال TCP/TLS جديد لكل طلب كما كان يحدث
سابقاً مع requests.

telegram_api_post تطبّق أيضاً نفس حقن الايموجي المميز والتحديد الجنسي
المطبّق في AioBot.__call__ (انظر entry.py) — لأن هذه المسارات كانت ترسل
JSON مباشرة لـ api.telegram.org متجاوزة aiogram بالكامل، فكانت تفوّت حقن
الايموجي/الجنس مهما كان محتوى الرسالة.
"""

import asyncio
import aiohttp

from helpers.emoji import inject_custom_emojis_sync
from helpers.gender import genderize_text
from helpers.context import get_current_user_id

_session: "aiohttp.ClientSession | None" = None
_session_lock = asyncio.Lock()

DEFAULT_TIMEOUT = aiohttp.ClientTimeout(total=20)


async def get_session() -> aiohttp.ClientSession:
    """يعيد جلسة aiohttp مشتركة واحدة (يعاد إنشاؤها فقط لو أُغلقت)."""
    global _session
    if _session is None or _session.closed:
        async with _session_lock:
            if _session is None or _session.closed:
                _session = aiohttp.ClientSession()
    return _session


async def close_session():
    global _session
    if _session is not None and not _session.closed:
        try:
            await _session.close()
        except Exception:
            pass


async def _apply_text_injection(payload: dict) -> None:
    """يطبّق التحديد الجنسي ثم الايموجي المميز على text/caption داخل الـ
    payload، بنفس منطق AioBot.__call__ تماماً — لتبقى المسارات المباشرة
    لـ Telegram API متوافقة مع نفس الميزتين."""
    try:
        user_id = get_current_user_id()
        for field in ("text", "caption"):
            val = payload.get(field)
            if isinstance(val, str) and val:
                new_val = val
                if user_id is not None:
                    try:
                        new_val = await genderize_text(new_val, user_id)
                    except Exception as ge:
                        print(f"[تحديد جنسي] فشل التحويل: {ge}")
                new_val = inject_custom_emojis_sync(new_val)
                if new_val != val:
                    payload[field] = new_val
                    if not payload.get("parse_mode"):
                        payload["parse_mode"] = "HTML"
    except Exception as e:
        print(f"[ايموجي مميز] فشل الحقن: {e}")


async def telegram_api_post(bot_token: str, method: str, payload: dict,
                             timeout: int = 20) -> dict:
    """بديل غير-محجوب لـ requests.post(f".../bot{token}/{method}", json=payload).
    يعيد dict مطابق لما كان `.json()` يعيده سابقاً — نفس الشكل، بدون تجميد
    الـ event loop، مع تطبيق حقن الايموجي/الجنس تلقائياً."""
    await _apply_text_injection(payload)
    session = await get_session()
    url = f"https://api.telegram.org/bot{bot_token}/{method}"
    try:
        async with session.post(
            url, json=payload,
            timeout=aiohttp.ClientTimeout(total=timeout) if timeout != 20 else DEFAULT_TIMEOUT,
        ) as resp:
            try:
                return await resp.json()
            except Exception:
                return {"ok": resp.status == 200, "status_code": resp.status}
    except Exception as e:
        print(f"[telegram_api_post] فشل الطلب ({method}): {e}")
        return {"ok": False, "error": str(e)}


async def http_get_json(url: str, **kwargs) -> dict:
    """بديل غير-محجوب لـ requests.get(url).json() لأي API خارجي (ليس تيليجرام)."""
    session = await get_session()
    timeout = kwargs.pop("timeout", None)
    aio_timeout = aiohttp.ClientTimeout(total=timeout) if timeout else DEFAULT_TIMEOUT
    async with session.get(url, timeout=aio_timeout, **kwargs) as resp:
        return await resp.json(content_type=None)


async def http_get_text(url: str, **kwargs) -> str:
    """بديل غير-محجوب لـ requests.get(url).text لأي API خارجي."""
    session = await get_session()
    timeout = kwargs.pop("timeout", None)
    aio_timeout = aiohttp.ClientTimeout(total=timeout) if timeout else DEFAULT_TIMEOUT
    async with session.get(url, timeout=aio_timeout, **kwargs) as resp:
        return await resp.text()


async def http_post_multipart(url: str, timeout: int = 25, **kwargs) -> dict:
    """بديل غير-محجوب لطلبات requests.post التي ترفع ملفات (multipart/form-data)،
    مثل OCR. يقبل نفس نمط kwargs (files/data) عبر aiohttp.FormData."""
    session = await get_session()
    aio_timeout = aiohttp.ClientTimeout(total=timeout)
    form = aiohttp.FormData()
    files = kwargs.pop("files", None) or {}
    data = kwargs.pop("data", None) or {}
    for field_name, file_obj in files.items():
        form.add_field(field_name, file_obj)
    for field_name, value in data.items():
        form.add_field(field_name, str(value))
    async with session.post(url, data=form, timeout=aio_timeout, **kwargs) as resp:
        try:
            return await resp.json(content_type=None)
        except Exception:
            return {"ok": resp.status == 200, "status_code": resp.status, "text": await resp.text()}
