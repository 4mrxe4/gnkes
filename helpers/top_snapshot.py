"""
طبقة Snapshot موحّدة لنظام "التوب" (plugins/games/top.py).

الهدف: فصل حساب/تجميع بيانات كل توب عن لحظة عرضه للمستخدم، بحيث يكون
هناك مصدر بيانات واحد (Snapshot) يُستخدم من كل من:
  - التوب النصي (مثال: "توب المتفاعلين")
  - التوب بالأزرار (مثال: "توب" ثم تصفح الأزرار)

بدون أي فرق بين الاثنين في الترتيب أو الأسماء أو الأرقام أو وقت التحديث —
الفرق الوحيد هو طريقة العرض.

تصنيف الأنواع:
- GLOBAL_TYPES: أنواع على مستوى البوت كامل (بلا chat_id): money, thieves,
  donations, farmers, marriage_global, likes, dislikes, groups_interactive,
  groups_players. هذه تُحدَّث تلقائياً كل SNAPSHOT_TTL ثانية في الخلفية عبر
  start_periodic_refresh لكل بوت — مهمة واحدة فقط لكل bot_id، لا تتكرر ولا
  ترتبط بأي رسالة مستخدم.
- LOCAL_TYPES: أنواع خاصة بمجموعة معينة (interactive, genius,
  marriage_local). هذه لا تُحسب مسبقاً لكل مجموعات البوت (قد تكون آلاف
  المجموعات وأغلبها غير نشط) بل بأسلوب cache-aside كسول: أول طلب بعد انتهاء
  الـTTL يبني Snapshot جديد لتلك المجموعة تحديداً، ويُشارَك بعدها بين كل
  مستخدمي نفس المجموعة لبقية الـTTL — بدل إعادة حسابه لكل مستخدم يطلبه.

في الحالتين يُخزَّن الـSnapshot بيانات خام (قائمة/نتيجة get_*_data_fast كما
هي بدون أي تنسيق نصي)، لكي يبني منه المتصل نص التوب أو أزراره حسب حاجته دون
إعادة حساب من Redis في كل مرة.

هذه الطبقة لا تُغيّر منطق حساب أي توب (get_*_data_fast تبقى كما هي تماماً في
plugins/games/top.py) — فقط تُغيّر متى وأين يُستدعى هذا الحساب.
"""

from __future__ import annotations

import asyncio
import json
import logging
import time
from typing import Any, Callable, Optional

from helpers.context import get_current_bot_id
from helpers.redis import RedisFake

logger = logging.getLogger(__name__)

# مدة صلاحية الـSnapshot المنطقية (10 دقائق كما طُلب).
SNAPSHOT_TTL = 600
# هامش بسيط فوق الـTTL المنطقي لصلاحية المفتاح في Redis نفسه (احتياط فقط).
SNAPSHOT_REDIS_TTL = SNAPSHOT_TTL + 90

GLOBAL_TYPES = (
    "money", "thieves", "donations", "farmers", "marriage_global",
    "likes", "dislikes", "groups_interactive", "groups_players",
)
LOCAL_TYPES = ("interactive", "genius", "marriage_local")

# آخر وقت نجح فيه تحديث دفعة الأنواع "العامة" لكل بوت — للتشخيص فقط
# (يُستخدم مثلاً في أوامر المطورين لعرض حالة الجدولة)، لا يؤثر على أي منطق.
_LAST_GLOBAL_REFRESH: dict[str, float] = {}


def _snapshot_key(data_type: str, bot_id: str, chat_id=None) -> str:
    if chat_id is not None:
        return f"topsnap:{data_type}:{chat_id}:{bot_id}"
    return f"topsnap:{data_type}:{bot_id}"


async def _store_snapshot(bot_id: str, data_type: str, payload: Any, chat_id=None) -> None:
    r = RedisFake(bot_id=bot_id)
    key = _snapshot_key(data_type, bot_id, chat_id)
    body = json.dumps({"ts": time.time(), "payload": payload}, ensure_ascii=False, default=str)
    try:
        await r.setex(key, SNAPSHOT_REDIS_TTL, body)
    except Exception:
        logger.warning(f"[top_snapshot] فشل حفظ snapshot لـ {data_type} (bot={bot_id})")


async def _load_snapshot(bot_id: str, data_type: str, chat_id=None) -> Optional[Any]:
    r = RedisFake(bot_id=bot_id)
    key = _snapshot_key(data_type, bot_id, chat_id)
    try:
        raw = await r.get(key)
    except Exception:
        return None
    if not raw:
        return None
    try:
        obj = json.loads(raw)
    except Exception:
        return None
    ts = obj.get("ts", 0)
    if time.time() - ts > SNAPSHOT_TTL:
        # منتهي منطقياً (حتى لو لم يُمسح بعد من Redis) — نعتبره غير موجود
        # ليُعاد بناؤه.
        return None
    return obj.get("payload")


async def _fetch_raw(data_type: str, client, chat_id=None) -> Any:
    """يستدعي دالة get_*_data_fast الأصلية المطابقة من plugins/games/top.py
    دون أي تعديل على منطقها الداخلي — فقط توجيه حسب نوع التوب."""
    # استيراد مؤجَّل لتفادي أي حلقة استيراد (plugins.games.top يستورد من
    # هذا الملف بدوره).
    from plugins.games import top as top_module

    if data_type == "money":
        return await top_module.get_money_data_fast(client)
    if data_type == "thieves":
        return await top_module.get_thieves_data_fast(client)
    if data_type == "donations":
        return await top_module.get_donations_data_fast(client)
    if data_type == "farmers":
        return await top_module.get_farmers_data_fast(client)
    if data_type == "marriage_global":
        return await top_module.get_marriage_data_fast(client=client, is_global=True)
    if data_type == "likes":
        return await top_module.get_likes_data_fast("likes", client)
    if data_type == "dislikes":
        return await top_module.get_likes_data_fast("dislikes", client)
    if data_type == "groups_interactive":
        return await top_module.get_groups_interactive_data_fast(client=client)
    if data_type == "groups_players":
        return await top_module.get_groups_players_data_fast(client=client)
    if data_type == "interactive":
        return await top_module.get_interactive_data_fast(chat_id, client)
    if data_type == "genius":
        return await top_module.get_genius_data_fast(chat_id, client)
    if data_type == "marriage_local":
        return await top_module.get_marriage_data_fast(chat_id, client=client)
    raise ValueError(f"unknown top data_type: {data_type}")


async def get_top_snapshot(data_type: str, client, chat_id=None, bot_id: str = None) -> Any:
    """المصدر الوحيد للبيانات الخام لأي توب — يُستخدم من التوب النصي وأزرار
    التوب على حدٍّ سواء، فتُشاهد نفس البيانات تماماً من كليهما.

    - إن وُجد Snapshot صالح (لم تنتهِ صلاحيته): يُعاد مباشرة بدون أي حساب.
    - غير ذلك: يُبنى مرة واحدة ويُخزَّن، ليُقرأ جاهزاً من كل طلب لاحق خلال
      الـ10 دقائق التالية (سواء كان طلباً نصياً أو ضغطة زر).
    """
    bot_id = bot_id or get_current_bot_id()
    if not bot_id:
        # لا يوجد سياق بوت معروف (حالة نادرة) — نحسب مباشرة بدون تخزين.
        return await _fetch_raw(data_type, client, chat_id)

    cached = await _load_snapshot(bot_id, data_type, chat_id)
    if cached is not None:
        return cached

    payload = await _fetch_raw(data_type, client, chat_id)
    await _store_snapshot(bot_id, data_type, payload, chat_id)
    return payload


async def refresh_global_snapshots(bot_id: str, client) -> dict:
    """تُحدّث كل الأنواع "العامة" (GLOBAL_TYPES) دفعة واحدة لبوت معيّن.
    تُستدعى فقط من المهمة الدورية في الخلفية (start_periodic_refresh) — لا
    تُستدعى أبداً من داخل معالجة رسالة/ضغطة مستخدم."""
    results = {}
    for data_type in GLOBAL_TYPES:
        try:
            payload = await _fetch_raw(data_type, client)
            await _store_snapshot(bot_id, data_type, payload)
            results[data_type] = "ok"
        except Exception as e:
            results[data_type] = f"error: {e}"
            logger.warning(f"[top_snapshot] فشل تحديث {data_type} للبوت {bot_id}: {e}")
    _LAST_GLOBAL_REFRESH[bot_id] = time.time()
    return results


def get_last_global_refresh(bot_id: str) -> Optional[float]:
    return _LAST_GLOBAL_REFRESH.get(bot_id)


# ==== الجدولة الدورية (Background updater) — واحدة فقط لكل بوت ====

_scheduler_tasks: dict[str, "asyncio.Task"] = {}


async def _scheduler_loop(bot_id: str, get_client: Callable[[], Any]) -> None:
    # مهلة بدء صغيرة تتيح للبوت إكمال الإقلاع (get_me، إلخ) قبل أول تحديث.
    try:
        await asyncio.sleep(15)
    except asyncio.CancelledError:
        raise

    while True:
        try:
            client = get_client()
            if client is not None:
                await refresh_global_snapshots(bot_id, client)
        except asyncio.CancelledError:
            raise
        except Exception as e:
            logger.warning(f"[top_snapshot] خطأ في مهمة التحديث الدورية للبوت {bot_id}: {e}")

        try:
            await asyncio.sleep(SNAPSHOT_TTL)
        except asyncio.CancelledError:
            raise


def start_periodic_refresh(bot_id: str, get_client: Callable[[], Any]) -> None:
    """يبدأ مهمة تحديث دورية (كل SNAPSHOT_TTL ثانية) لبوت معيّن — مرة واحدة
    فقط لكل bot_id، حتى لو استُدعيت الدالة أكثر من مرة (لا Scheduler مكرر).

    get_client: دالة بلا معاملات تُرجع عميل البوت الحالي وقت الحاجة (وليس
    عميلاً واحداً يُلتقط الآن) — لأن عميل/سياق البوت قد يتغيّر بين تشغيلة
    وأخرى دون إعادة إنشاء المهمة نفسها."""
    existing = _scheduler_tasks.get(bot_id)
    if existing is not None and not existing.done():
        return
    loop = asyncio.get_event_loop()
    task = loop.create_task(_scheduler_loop(bot_id, get_client))
    _scheduler_tasks[bot_id] = task


def stop_periodic_refresh(bot_id: str) -> None:
    task = _scheduler_tasks.pop(bot_id, None)
    if task is not None and not task.done():
        task.cancel()


__all__ = [
    "SNAPSHOT_TTL",
    "GLOBAL_TYPES",
    "LOCAL_TYPES",
    "get_top_snapshot",
    "refresh_global_snapshots",
    "get_last_global_refresh",
    "start_periodic_refresh",
    "stop_periodic_refresh",
]
