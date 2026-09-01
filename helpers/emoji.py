
import json
import re

from compat import MessageEntityType as AioMessageEntityType

from helpers.context import get_global_r, get_global_dev, get_current_bot_id
from helpers.redis import RedisFake

_sync_cache = {}
_replacement_cache = {}


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


REPLACE_TYPE_EMOJI = "emoji"
REPLACE_TYPE_TEXT = "text"
REPLACE_TYPE_EMOJI_WITH_TEXT = "emoji_with_text"


async def get_custom_emoji_mappings(bot_id: str = None) -> dict:
    try:
        if bot_id is None:
            bot_id = get_current_bot_id() or get_global_dev()
        redis = get_redis_instance()
        key = f"custom_emoji_mappings:{bot_id}"
        data = await redis.get(key)
        mappings = json.loads(data) if data else {}
        _sync_cache[bot_id] = mappings
        return mappings
    except Exception:
        return _sync_cache.get(bot_id, {}) if bot_id else {}


async def get_replacement_mappings(bot_id: str = None) -> dict:
    try:
        if bot_id is None:
            bot_id = get_current_bot_id() or get_global_dev()
        redis = get_redis_instance()
        key = f"replacement_mappings:{bot_id}"
        data = await redis.get(key)
        return json.loads(data) if data else {}
    except Exception:
        return {}


async def save_replacement_mapping(
    old_text: str,
    replacement_text: str,
    custom_emoji_id: str = None,
    emoji_char: str = None,
    replace_type: str = REPLACE_TYPE_TEXT,
    bot_id: str = None
) -> bool:
    try:
        if bot_id is None:
            bot_id = get_current_bot_id() or get_global_dev()
        redis = get_redis_instance()
        key = f"replacement_mappings:{bot_id}"
        mappings = await get_replacement_mappings(bot_id)
        data = {
            "old_text": old_text,
            "replacement_text": replacement_text,
            "replace_type": replace_type
        }
        if custom_emoji_id:
            data["custom_emoji_id"] = custom_emoji_id
        if emoji_char:
            data["emoji_char"] = emoji_char
        mappings[old_text] = data
        await redis.set(key, json.dumps(mappings))
        _replacement_cache[bot_id] = mappings
        return True
    except Exception:
        return False


async def delete_replacement_mapping(old_text: str, bot_id: str = None) -> bool:
    try:
        if bot_id is None:
            bot_id = get_current_bot_id() or get_global_dev()
        redis = get_redis_instance()
        key = f"replacement_mappings:{bot_id}"
        mappings = await get_replacement_mappings(bot_id)
        if old_text in mappings:
            del mappings[old_text]
            await redis.set(key, json.dumps(mappings))
            _replacement_cache[bot_id] = mappings
            return True
        return False
    except Exception:
        return False


async def clear_all_replacements(bot_id: str = None) -> bool:
    try:
        if bot_id is None:
            bot_id = get_current_bot_id() or get_global_dev()
        redis = get_redis_instance()
        key = f"replacement_mappings:{bot_id}"
        await redis.delete(key)
        _replacement_cache[bot_id] = {}
        return True
    except Exception:
        return False


_TAG_SPLIT_RE = re.compile(r'(<[^>]+>)')


def _apply_outside_tags(text: str, transform) -> str:
    """يطبّق transform (دالة نصّ → نصّ) فقط على أجزاء النص الواقعة خارج
    أي وسم HTML موجود مسبقاً في النص (مثل <tg-emoji>, <b>, <a href=...>)،
    دون المساس بمحتوى الوسوم نفسها.

    بدون هذا الفصل: لو كانت الكلمة المستبدَلة (old_text) تطابق جزءاً من
    اسم وسم موجود بالفعل (مثال: كلمة "emoji" تقع داخل اسم الوسم
    "tg-emoji")، فإن الاستبدال يقع *داخل بنية الوسم ذاته* وينتج HTML
    فاسد مثل <tg-<tg-emoji ...> يرفضه تيليجرام بخطأ
    "Unsupported start tag"."""
    parts = _TAG_SPLIT_RE.split(text)
    for i, part in enumerate(parts):
        if i % 2 == 0:  # الأجزاء الزوجية = نص عادي، الفردية = وسوم HTML كاملة
            parts[i] = transform(part)
    return "".join(parts)


def _apply_replacement(text: str, mappings: dict) -> str:
    def _do(segment: str) -> str:
        new_text = segment
        for old_text, mapping_data in mappings.items():
            if not isinstance(mapping_data, dict):
                continue
            replace_type = mapping_data.get("replace_type", REPLACE_TYPE_TEXT)
            replacement_text = mapping_data.get("replacement_text", "")
            custom_emoji_id = mapping_data.get("custom_emoji_id")
            emoji_char = mapping_data.get("emoji_char", "")
            if replace_type == REPLACE_TYPE_EMOJI and custom_emoji_id and emoji_char:
                replacement = f'<tg-emoji emoji-id="{custom_emoji_id}">{emoji_char}</tg-emoji>'
            elif replace_type == REPLACE_TYPE_EMOJI_WITH_TEXT and custom_emoji_id and emoji_char:
                replacement = f'<tg-emoji emoji-id="{custom_emoji_id}">{emoji_char}</tg-emoji> {replacement_text}'
            else:
                replacement = replacement_text
            pattern = r'(?<![a-zA-Z\u0600-\u06FF])' + re.escape(old_text) + r'(?![a-zA-Z\u0600-\u06FF])'
            new_text = re.sub(pattern, replacement, new_text)
        return new_text
    return _apply_outside_tags(text, _do)


def _inject_from_mappings(text: str, mappings: dict) -> str:
    def _do(segment: str) -> str:
        new_text = segment
        for old_text, mapping_data in mappings.items():
            if not isinstance(mapping_data, dict):
                continue
            custom_emoji_id = mapping_data.get("custom_emoji_id", "")
            emoji_char = mapping_data.get("emoji_char", "")
            position = mapping_data.get("position", "end")
            if not (custom_emoji_id and emoji_char):
                continue
            pattern = r'(?<![a-zA-Z\u0600-\u06FF])' + re.escape(old_text) + r'(?![a-zA-Z\u0600-\u06FF])'
            emoji_tag = f'<tg-emoji emoji-id="{custom_emoji_id}">{emoji_char}</tg-emoji>'
            if position == "start":
                replacement = f'{emoji_tag} \\g<0>'
            else:
                replacement = f'\\g<0> {emoji_tag}'
            new_text = re.sub(pattern, replacement, new_text)
        return new_text
    return _apply_outside_tags(text, _do)


def utf16_offset_to_py_index(text: str, utf16_offset: int) -> int:
    """يحوّل موضعاً بوحدات UTF-16 (offset/length في كيانات تيليجرام) إلى
    فهرس Python الصحيح (مفهرس بنقاط شيفرة Unicode لا وحدات UTF-16).

    أي حرف خارج BMP — ومنها معظم الرموز التعبيرية والخطوط الرياضية
    الزخرفية (𝖭𝖠𝖬𝖤 𝖴𝖲𝖤 ...) الشائعة في قوالب الشكل — يُمثَّل في UTF-16
    بزوج بديل يشغل وحدتين بينما يشغل نقطة كود Python واحدة فقط. دون هذا
    التحويل، كل حرف من هذا النوع يسبق الكيان يزيح القص خانة كاملة، فيُقتطع
    حرف خاطئ كـ emoji_char ويرفضه تيليجرام كإيموجي مميز غير صالح — وهذا
    ما كان يسبّب اختفاء كل الإيموجيات المميزة دفعة واحدة عند تراكم عدة
    أحرف زخرفية قبلها في القالب."""
    py_index = 0
    units = 0
    for ch in text:
        if units >= utf16_offset:
            break
        units += 2 if ord(ch) > 0xFFFF else 1
        py_index += 1
    return py_index


def render_custom_emoji_entities(text: str, entities) -> str:
    """يحوّل كيانات CUSTOM_EMOJI داخل النص إلى وسوم <tg-emoji> الصحيحة،
    عبر القص حسب الموضع (offset/length) لا البحث النصي الشامل.

    البديل السابق (منتشر في عدة plugins) كان يستخدم
    text.replace(emoji_char, ...) الذي يستبدل *كل* ظهور لنفس الرمز في
    النص — فإذا تكرر نفس الإيموجي المميز أكثر من مرة في رسالة واحدة، كانت
    كل حلقة تعيد تغليف ما غلّفته الحلقات السابقة أيضاً (لأن الرمز الأصلي
    يبقى داخل الوسم الجديد)، فينمو طول النص أُسّياً حتى يستهلك كل الذاكرة
    المتاحة (MemoryError). القص بالموضع هنا يعالج كل كيان في مكانه الدقيق
    فقط بلا أي تأثير على بقية النص، بمعالجة الكيانات من أعلى offset إلى
    أدناه حتى لا تنزاح المواضع الأصغر بعد كل عملية قص."""
    if not text or not entities:
        return text
    custom_entities = [e for e in entities if getattr(e, "type", None) == AioMessageEntityType.CUSTOM_EMOJI]
    if not custom_entities:
        return text
    result = text
    for entity in sorted(custom_entities, key=lambda e: e.offset, reverse=True):
        # start/end بفهرسة Python الصحيحة (انظر _utf16_offset_to_py_index) —
        # تُحسَب من result الحالي في كل تكرار، وبما أن المعالجة تسير من
        # أعلى offset إلى أدناه، فإن الجزء الذي يسبق الكيان الحالي لم يتغيّر
        # بعد (التعديلات السابقة وقعت كلها في الذيل)، فالتحويل يبقى صحيحاً.
        start = utf16_offset_to_py_index(result, entity.offset)
        end = utf16_offset_to_py_index(result, entity.offset + entity.length)
        emoji_char = result[start:end]
        result = (
            result[:start]
            + f'<tg-emoji emoji-id="{entity.custom_emoji_id}">{emoji_char}</tg-emoji>'
            + result[end:]
        )
    return result


async def inject_custom_emojis(text: str, entities=None, bot_id: str = None):
    if not text or not isinstance(text, str):
        return text, entities
    try:
        bot_id = bot_id or get_current_bot_id() or get_global_dev()
        new_text = text
        replacement_mappings = await get_replacement_mappings(bot_id)
        if replacement_mappings:
            new_text = _apply_replacement(new_text, replacement_mappings)
        emoji_mappings = await get_custom_emoji_mappings(bot_id)
        if emoji_mappings:
            new_text = _inject_from_mappings(new_text, emoji_mappings)
        return new_text, entities
    except Exception:
        return text, entities


def inject_custom_emojis_sync(text: str, bot_id: str = None) -> str:
    if not text or not isinstance(text, str):
        return text
    try:
        bot_id = bot_id or get_current_bot_id() or get_global_dev()
        new_text = text
        replacement_mappings = _replacement_cache.get(bot_id, {})
        if replacement_mappings:
            new_text = _apply_replacement(new_text, replacement_mappings)
        emoji_mappings = _sync_cache.get(bot_id, {})
        if emoji_mappings:
            new_text = _inject_from_mappings(new_text, emoji_mappings)
        return new_text
    except Exception:
        return text


async def save_custom_emoji_mapping(old_text: str, new_text: str, custom_emoji_id: str, emoji_position: str, bot_id: str = None) -> bool:
    try:
        if bot_id is None:
            bot_id = get_current_bot_id() or get_global_dev()
        redis = get_redis_instance()
        key = f"custom_emoji_mappings:{bot_id}"
        mappings = await get_custom_emoji_mappings(bot_id)
        emoji_char = ""
        for char in new_text:
            if ord(char) > 0xFFFF or (0x1F000 <= ord(char) <= 0x1FFFF):
                emoji_char = char
                break
        mappings[old_text] = {
            "new_text": new_text,
            "custom_emoji_id": custom_emoji_id,
            "emoji_char": emoji_char,
            "position": emoji_position
        }
        await redis.set(key, json.dumps(mappings))
        _sync_cache[bot_id] = mappings
        return True
    except Exception:
        return False


async def delete_custom_emoji_mapping(old_text: str, bot_id: str = None) -> bool:
    try:
        if bot_id is None:
            bot_id = get_current_bot_id() or get_global_dev()
        redis = get_redis_instance()
        key = f"custom_emoji_mappings:{bot_id}"
        mappings = await get_custom_emoji_mappings(bot_id)
        if old_text in mappings:
            del mappings[old_text]
            await redis.set(key, json.dumps(mappings))
            _sync_cache[bot_id] = mappings
            return True
        return False
    except Exception:
        return False


async def clear_all_custom_emojis(bot_id: str = None) -> bool:
    try:
        if bot_id is None:
            bot_id = get_current_bot_id() or get_global_dev()
        redis = get_redis_instance()
        key = f"custom_emoji_mappings:{bot_id}"
        await redis.delete(key)
        _sync_cache[bot_id] = {}
        return True
    except Exception:
        return False


def detect_emoji_position(text: str, entities: list) -> str:
    if not entities:
        return "end"
    for entity in entities:
        etype = getattr(entity, "type", None)
        if etype == AioMessageEntityType.CUSTOM_EMOJI:
            return "start" if entity.offset < len(text) * 0.3 else "end"
    return "end"


__all__ = [
    'render_custom_emoji_entities',
    'utf16_offset_to_py_index',
    'get_custom_emoji_mappings',
    'save_custom_emoji_mapping',
    'delete_custom_emoji_mapping',
    'clear_all_custom_emojis',
    'inject_custom_emojis',
    'inject_custom_emojis_sync',
    'detect_emoji_position',
    'get_replacement_mappings',
    'save_replacement_mapping',
    'delete_replacement_mapping',
    'clear_all_replacements',
    'REPLACE_TYPE_EMOJI',
    'REPLACE_TYPE_TEXT',
    'REPLACE_TYPE_EMOJI_WITH_TEXT',
]
