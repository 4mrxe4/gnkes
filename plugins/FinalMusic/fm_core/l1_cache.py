# l1_cache.py

import re
import asyncio as _asyncio

from helpers.context import redis_proxy as r, dev_final_proxy as Dev_FINAL, get_current_bot_id
from compat import Client

_bot_pyro_client = None

def clean_title(title: str) -> str:
    if not title:
        return "Audio Track"
    title = re.sub(r'#\w+', '', title)
    title = re.sub(r'[^\w\s]', '', title, flags=re.UNICODE)
    title = re.sub(r'\s+', ' ', title).strip()
    return title if title else "Audio Track"

def get_real_bot_id(c: Client = None) -> str:
    if c is not None:
        bot_id = getattr(c, 'bot_id', None) or getattr(c, 'dev_final', None)
        if bot_id:
            return str(bot_id)
    bot_id = get_current_bot_id()
    if bot_id:
        return str(bot_id)
    return str(Dev_FINAL)

async def get_real_pyro_client():
    try:
        from plugins.FinalMusic import userbot
        if not userbot.clients:
            try:
                await userbot.boot()
            except Exception:
                pass
        return userbot.one or (userbot.clients[0] if userbot.clients else None)
    except Exception:
        return None

_bot_pyro_lock = _asyncio.Lock()


async def get_bot_pyro_client():
    """
    ترجع عميل Pyrogram واحداً مشتركاً بين كل بوتات الكلاستر (لحل يوزرنيمات
    غير معروفة لـ aiogram)، ويبقى متصلاً طوال عمر العملية بدل إعادة إنشائه
    من الصفر (auth كامل + start) عند كل أمر.

    الإصلاح مقارنة بالنسخة السابقة:
    - لا تُستدعى get_me() (طلب شبكة فعلي) عند كل نداء؛ فقط نتحقق من
      is_connected المحلية (بلا أي طلب شبكة) لأن Pyrogram نفسه يدير إعادة
      الاتصال داخلياً بعد start() الأولى.
    - قفل asyncio.Lock يمنع تسابق عدة أوامر متزامنة (من بوتات/مجموعات
      مختلفة بنفس اللحظة) على إنشاء عدة عملاء منفصلين دفعة واحدة، وهو
      السبب الفعلي للبطء الملحوظ سابقاً "يفتح عملية جديدة بعد كل أمر".
    - اسم العميل ثابت (غير معتمد على البوت الحالي وقت الإنشاء) لأنه عميل
      مشترك واحد فعلياً، وليس عميلاً خاصاً بكل بوت.
    """
    global _bot_pyro_client

    if _bot_pyro_client is not None and getattr(_bot_pyro_client, "is_connected", False):
        return _bot_pyro_client

    async with _bot_pyro_lock:
        # بعد أخذ القفل، قد يكون عميل آخر (كان ينتظر نفس القفل) أنشأه بالفعل
        if _bot_pyro_client is not None and getattr(_bot_pyro_client, "is_connected", False):
            return _bot_pyro_client

        try:
            from plugins.FinalMusic import config
            from pyrogram import Client

            bot_token = getattr(config, 'TOKEN', None)
            api_id = getattr(config, 'API_ID', None)
            api_hash = getattr(config, 'API_HASH', None)

            if not bot_token or not api_id or not api_hash:
                return None

            if _bot_pyro_client is not None:
                try:
                    await _bot_pyro_client.start()
                    return _bot_pyro_client
                except ConnectionError:
                    # متصل فعلاً (pyrogram يرفع ConnectionError من start()
                    # لو كان الاتصال قائماً بالفعل) — استخدمه كما هو.
                    return _bot_pyro_client
                except Exception:
                    _bot_pyro_client = None

            _bot_pyro_client = Client(
                name="shared_bot_pyro_resolver",
                api_id=api_id,
                api_hash=api_hash,
                bot_token=bot_token,
                in_memory=True
            )

            await _bot_pyro_client.start()
            return _bot_pyro_client

        except Exception as e:
            print(f"[L2] فشل إنشاء/اتصال Pyrogram Client المشترك: {e}")
            return None