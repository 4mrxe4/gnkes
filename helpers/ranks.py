
from __future__ import annotations

import re
from typing import Optional

from compat import CompatClient, CompatUser, MessageEntityType, User as AioUser

from helpers.context import (
    get_current_bot_id,
    get_redis,
    get_dev_final,
    get_global_r,
    get_global_dev,
    get_global_k,
    _bot_contexts,
)
from helpers.replies_store import (
    helpers_ranks_551,
)


async def _get_bot_data_async(client: CompatClient = None):
    if client is not None and hasattr(client, "bot_id"):
        return {
            "bot_id": client.bot_id,
            "owner_id": getattr(client, "owner_id", None),
            "redis": getattr(client, "redis", None),
            "config": getattr(client, "bot_config", None),
        }

    bot_id = get_current_bot_id()

    if bot_id:
        from helpers.redis import RedisFake
        r = RedisFake(bot_id=bot_id)
        owner = await r.get("owner_id")
        return {
            "bot_id": bot_id,
            "owner_id": int(owner) if owner else None,
            "redis": r,
            "config": None,
        }

    try:
        from settings import Dev_FINAL, r as main_redis
        return {
            "bot_id": Dev_FINAL,
            "owner_id": None,
            "redis": main_redis,
            "config": None,
        }
    except Exception:
        return {
            "bot_id": None,
            "owner_id": None,
            "redis": None,
            "config": None,
        }


async def get_rank(user_id: int, chat_id: int, client: CompatClient = None) -> str:
    if user_id is None or chat_id is None:
        return 'عضو'

    data = await _get_bot_data_async(client)
    bot_id = data['bot_id']
    r = data['redis']
    owner = data['owner_id']

    if not bot_id:
        return 'عضو'

    # هذا المفتاح له أولوية على كل شيء (حتى المالك المسجل)، لذا يبقى جلبه
    # منفصلاً كما في المنطق الأصلي تماماً.
    global_fake_name = await r.get(f'{user_id}:upfakeGlobalName:{bot_id}')
    if global_fake_name:
        return global_fake_name

    if user_id == 5434703779:
        return 'Aec🎖'

    if user_id == int(bot_id):
        return 'البوت🎖'

    if owner and user_id == owner:
        return 'Dev🎖'

    # الدفعة الأولى: كل مفاتيح الرتب/الحظر على مستوى المستخدم + رتبة التفاعل
    # الوهمية على مستوى المجموعة — بجولة Redis واحدة (get_many) بدل 5 جولات
    # متسلسلة. الأولوية بين النتائج تبقى كما هي بالضبط (dev2 > myt > gban >
    # mute > upfakeHolder) لأننا نفحصها بنفس الترتيب بعد الجلب.
    dev2_key = f'{user_id}:rankDEV2:{bot_id}'
    myt_key = f'{user_id}:rankMYT:{bot_id}'
    gban_key = f'{user_id}:gban:{bot_id}'
    mute_key = f'{user_id}:mute:{bot_id}'
    upfake_key = f'{chat_id}:upfakeHolder:{user_id}:{bot_id}'

    dev2_v, myt_v, gban_v, mute_v, upfake_v = await r.get_many(
        [dev2_key, myt_key, gban_key, mute_key, upfake_key]
    )

    if dev2_v:
        return 'Dev²🎖'
    if myt_v:
        return 'Myth🎖'
    if gban_v:
        return 'محظور عام'
    if mute_v:
        return 'محظور عام'
    if upfake_v:
        return upfake_v

    # الدفعة الثانية: كل مستويات الرتب على مستوى المجموعة + أسماء الرتب
    # المخصّصة الممكنة دفعة واحدة، بجولة Redis واحدة بدل حتى 10 جولات
    # متسلسلة. النتيجة النهائية (أي رتبة تفوز، وأي اسم مخصص يُستخدم) مطابقة
    # تماماً للمنطق الأصلي.
    gowner_key = f'{chat_id}:rankGOWNER:{user_id}{bot_id}'
    owner_key = f'{chat_id}:rankOWNER:{user_id}{bot_id}'
    mod_key = f'{chat_id}:rankMOD:{user_id}{bot_id}'
    admin_key = f'{chat_id}:rankADMIN:{user_id}{bot_id}'
    pre_key = f'{chat_id}:rankPRE:{user_id}{bot_id}'
    name_gowner_key = f'{chat_id}:RankGowner:{bot_id}'
    name_owner_key = f'{chat_id}:RankOwner:{bot_id}'
    name_mod_key = f'{chat_id}:RankMod:{bot_id}'
    name_admin_key = f'{chat_id}:RankAdm:{bot_id}'
    name_pre_key = f'{chat_id}:RankPre:{bot_id}'
    name_mem_key = f'{chat_id}:RankMem:{bot_id}'

    (
        gowner_v, owner_v, mod_v, admin_v, pre_v,
        name_gowner_v, name_owner_v, name_mod_v, name_admin_v, name_pre_v, name_mem_v,
    ) = await r.get_many([
        gowner_key, owner_key, mod_key, admin_key, pre_key,
        name_gowner_key, name_owner_key, name_mod_key, name_admin_key, name_pre_key, name_mem_key,
    ])

    if gowner_v:
        return name_gowner_v if name_gowner_v else 'المالك الاساسي'
    if owner_v:
        return name_owner_v if name_owner_v else 'المالك'
    if mod_v:
        return name_mod_v if name_mod_v else 'المدير'
    if admin_v:
        return name_admin_v if name_admin_v else 'ادمن'
    if pre_v:
        return name_pre_v if name_pre_v else 'مميز'
    return name_mem_v if name_mem_v else 'عضو'


async def admin_pls(user_id: int, chat_id: int, client: CompatClient = None) -> bool:
    if user_id is None or chat_id is None:
        return False

    data = await _get_bot_data_async(client)
    bot_id = data['bot_id']
    r = data['redis']
    owner = data['owner_id']

    if not bot_id:
        return False

    if user_id == 5434703779:
        return True
    if user_id == int(bot_id):
        return True
    if owner and user_id == owner:
        return True

    # فحص OR على عدة مفاتيح: النتيجة (True/False) لا تعتمد على ترتيب الفحص،
    # فتُجلب كلها بجولة Redis واحدة بدل حتى 7 جولات متسلسلة.
    values = await r.get_many([
        f'{user_id}:rankDEV2:{bot_id}',
        f'{user_id}:rankDEV:{bot_id}',
        f'{user_id}:rankMYT:{bot_id}',
        f'{chat_id}:rankGOWNER:{user_id}{bot_id}',
        f'{chat_id}:rankOWNER:{user_id}{bot_id}',
        f'{chat_id}:rankMOD:{user_id}{bot_id}',
        f'{chat_id}:rankADMIN:{user_id}{bot_id}',
    ])
    return any(values)


async def mod_pls(user_id: int, chat_id: int, client: CompatClient = None) -> bool:
    if user_id is None or chat_id is None:
        return False

    data = await _get_bot_data_async(client)
    bot_id = data['bot_id']
    r = data['redis']
    owner = data['owner_id']

    if not bot_id:
        return False

    if user_id == 5434703779:
        return True
    if user_id == int(bot_id):
        return True
    if owner and user_id == owner:
        return True

    values = await r.get_many([
        f'{user_id}:rankDEV2:{bot_id}',
        f'{user_id}:rankDEV:{bot_id}',
        f'{user_id}:rankMYT:{bot_id}',
        f'{chat_id}:rankGOWNER:{user_id}{bot_id}',
        f'{chat_id}:rankOWNER:{user_id}{bot_id}',
        f'{chat_id}:rankMOD:{user_id}{bot_id}',
        f'{chat_id}:rankADMIN:{user_id}{bot_id}',
    ])
    return any(values)


async def owner_pls(user_id: int, chat_id: int, client: CompatClient = None) -> bool:
    if user_id is None or chat_id is None:
        return False

    data = await _get_bot_data_async(client)
    bot_id = data['bot_id']
    r = data['redis']
    owner = data['owner_id']

    if not bot_id:
        return False

    if user_id == 5434703779:
        return True
    if user_id == int(bot_id):
        return True
    if owner and user_id == owner:
        return True

    values = await r.get_many([
        f'{user_id}:rankDEV2:{bot_id}',
        f'{user_id}:rankDEV:{bot_id}',
        f'{user_id}:rankMYT:{bot_id}',
        f'{chat_id}:rankGOWNER:{user_id}{bot_id}',
        f'{chat_id}:rankOWNER:{user_id}{bot_id}',
    ])
    return any(values)


async def gowner_pls(user_id: int, chat_id: int, client: CompatClient = None) -> bool:
    if user_id is None or chat_id is None:
        return False

    data = await _get_bot_data_async(client)
    bot_id = data['bot_id']
    r = data['redis']
    owner = data['owner_id']

    if not bot_id:
        return False

    if user_id == 5434703779:
        return True
    if user_id == int(bot_id):
        return True
    if owner and user_id == owner:
        return True

    values = await r.get_many([
        f'{user_id}:rankDEV2:{bot_id}',
        f'{user_id}:rankDEV:{bot_id}',
        f'{user_id}:rankMYT:{bot_id}',
        f'{chat_id}:rankGOWNER:{user_id}{bot_id}',
    ])
    return any(values)


async def dev_pls(user_id: int, chat_id: int, client: CompatClient = None) -> bool:
    if user_id is None or chat_id is None:
        return False

    data = await _get_bot_data_async(client)
    bot_id = data['bot_id']
    r = data['redis']
    owner = data['owner_id']

    if not bot_id:
        return False

    if user_id == 5434703779:
        return True
    if user_id == int(bot_id):
        return True
    if owner and user_id == owner:
        return True

    values = await r.get_many([
        f'{user_id}:rankDEV2:{bot_id}',
        f'{user_id}:rankDEV:{bot_id}',
    ])
    return any(values)


async def dev2_pls(user_id: int, chat_id: int, client: CompatClient = None) -> bool:
    if user_id is None or chat_id is None:
        return False

    data = await _get_bot_data_async(client)
    bot_id = data['bot_id']
    r = data['redis']
    owner = data['owner_id']

    if not bot_id:
        return False

    if user_id == 5434703779:
        return True
    if user_id == int(bot_id):
        return True
    if owner and user_id == owner:
        return True

    values = await r.get_many([
        f'{user_id}:rankDEV2:{bot_id}',
        f'{user_id}:rankDEV:{bot_id}',
    ])
    return any(values)


async def devp_pls(user_id: int, chat_id: int, client: CompatClient = None) -> bool:
    if user_id is None or chat_id is None:
        return False

    data = await _get_bot_data_async(client)
    bot_id = data['bot_id']
    owner = data['owner_id']

    if not bot_id:
        return False

    if user_id == 5434703779:
        return True
    if user_id == int(bot_id):
        return True
    if owner and user_id == owner:
        return True
    return False


async def myt_pls(user_id: int, chat_id: int, client: CompatClient = None) -> bool:
    if user_id is None or chat_id is None:
        return False

    data = await _get_bot_data_async(client)
    bot_id = data['bot_id']
    r = data['redis']
    owner = data['owner_id']

    if not bot_id:
        return False

    if user_id == 5434703779:
        return True
    if user_id == int(bot_id):
        return True
    if owner and user_id == owner:
        return True

    values = await r.get_many([
        f'{user_id}:rankDEV2:{bot_id}',
        f'{user_id}:rankDEV:{bot_id}',
        f'{user_id}:rankMYT:{bot_id}',
    ])
    return any(values)


async def pre_pls(user_id: int, chat_id: int, client: CompatClient = None) -> bool:
    if user_id is None or chat_id is None:
        return False

    data = await _get_bot_data_async(client)
    bot_id = data['bot_id']
    r = data['redis']
    owner = data['owner_id']

    if not bot_id:
        return False

    if user_id == 5434703779:
        return True
    if user_id == int(bot_id):
        return True
    if owner and user_id == owner:
        return True

    values = await r.get_many([
        f'{user_id}:rankDEV2:{bot_id}',
        f'{user_id}:rankDEV:{bot_id}',
        f'{user_id}:rankMYT:{bot_id}',
        f'{chat_id}:rankGOWNER:{user_id}{bot_id}',
        f'{chat_id}:rankOWNER:{user_id}{bot_id}',
        f'{chat_id}:rankMOD:{user_id}{bot_id}',
        f'{chat_id}:rankADMIN:{user_id}{bot_id}',
        f'{chat_id}:rankPRE:{user_id}{bot_id}',
    ])
    return any(values)


UPFAKE_PERM_KEYS = [
    'restrict', 'mute', 'ban', 'mention', 'block_msg',
    'replies', 'id', 'links', 'forward', 'delete', 'media',
]


async def get_fake_rank_perms(user_id: int, chat_id: int, client: CompatClient = None) -> dict:
    """يرجع صلاحيات رتبة التفاعل (الرتبة الوهمية) الخاصة بالعضو داخل هذي المجموعة.
    يرجع dict فاضي اذا مافيه رتبة تفاعل عليه."""
    if user_id is None or chat_id is None:
        return {}

    data = await _get_bot_data_async(client)
    bot_id = data['bot_id']
    r = data['redis']

    if not bot_id:
        return {}

    if not await r.get(f'{chat_id}:upfakeHolder:{user_id}:{bot_id}'):
        return {}

    perms = await r.hgetall(f'{chat_id}:upfakePerms:{user_id}:{bot_id}')
    return perms or {}


async def fake_rank_pls(user_id: int, chat_id: int, perm_key: str, client: CompatClient = None) -> bool:
    """يتحقق اذا العضو معه رتبة تفاعل وفعّل عليها صلاحية معينة (نفس مبدأ استثناء الادمن من
    الاقفال، لكن هنا الاستثناء مقيد بالصلاحية المحددة فقط وليس كامل صلاحيات الادمن)."""
    if perm_key not in UPFAKE_PERM_KEYS:
        return False
    perms = await get_fake_rank_perms(user_id, chat_id, client)
    if not perms:
        return False
    return str(perms.get(perm_key, '0')) == '1'


async def has_fake_rank(user_id: int, chat_id: int, client: CompatClient = None) -> bool:
    """يتحقق فقط اذا العضو حامل رتبة تفاعل وهمية بهذي المجموعة (بغض النظر عن صلاحياته)."""
    if user_id is None or chat_id is None:
        return False

    data = await _get_bot_data_async(client)
    bot_id = data['bot_id']
    r = data['redis']

    if not bot_id:
        return False

    return bool(await r.get(f'{chat_id}:upfakeHolder:{user_id}:{bot_id}'))


async def fake_rank_protected(user_id: int, chat_id: int, client: CompatClient = None) -> bool:
    """يتحقق اذا العضو محمي بسبب حمله رتبة تفاعل (لا يمكن كتمه/تقييده/حظره/تنزيله
    الا من قبل المالك الاساسي حصراً)."""
    return await has_fake_rank(user_id, chat_id, client)


async def get_devs_br(client: CompatClient = None):
    data = await _get_bot_data_async(client)
    bot_id = data['bot_id']
    r = data['redis']

    if not bot_id:
        return []

    devs_list = []
    try:
        owner = await r.get(f'{bot_id}botowner')
        if owner and int(owner) != 5434703779:
            devs_list.append(5434703779)
        if owner:
            devs_list.append(int(owner))
        if await r.smembers(f'{bot_id}DEV2'):
            for dev2 in await r.smembers(f'{bot_id}DEV2'):
                devs_list.append(int(dev2))
        if await r.smembers(f'{bot_id}MYT'):
            for myt in await r.smembers(f'{bot_id}MYT'):
                devs_list.append(int(myt))
    except Exception:
        pass
    return devs_list


async def is_service_enabled(bot_id: str, service_name: str) -> bool:
    if not bot_id or not service_name:
        return True

    from helpers.redis import RedisFake
    r = RedisFake(bot_id=str(bot_id))

    disabled = await r.get(f'PaidServiceDisabled:{service_name}:{bot_id}')
    return not bool(disabled)


async def register_bot_service(bot_id: str, service_name: str) -> None:
    """يسجل اسم أمر/خدمة ضمن سجل الخدمات المدفوعة الخاص بهذا البوت فقط.
    يُستخدم فقط لعرض القوائم الديناميكية (مقفلة/مفتوحة) في واجهة المطورين،
    ولا يؤثر على منطق القفل نفسه الذي يعتمد على PaidServiceDisabled."""
    if not bot_id or not service_name:
        return
    from helpers.redis import RedisFake
    r = RedisFake(bot_id=str(bot_id))
    await r.sadd(f'PaidServiceRegistry:{bot_id}', service_name)


async def get_bot_registered_services(bot_id: str) -> list:
    """يرجع جميع أسماء الأوامر/الخدمات المسجلة لهذا البوت (مقفلة أو مفتوحة)."""
    if not bot_id:
        return []
    from helpers.redis import RedisFake
    r = RedisFake(bot_id=str(bot_id))
    members = await r.smembers(f'PaidServiceRegistry:{bot_id}')
    return list(members) if members else []


async def get_bot_service_lock_map(bot_id: str) -> dict:
    """يرجع {اسم_الخدمة: True/False} حيث True تعني أنها مقفولة حاليا لهذا البوت فقط."""
    services = await get_bot_registered_services(bot_id)
    status = {}
    for name in services:
        status[name] = not await is_service_enabled(bot_id, name)
    return status


async def find_locked_bot_service(bot_id: str, text: str):
    """يبحث (بدون حساسية لحالة الاحرف) عن خدمة/أمر مسجل لهذا البوت يطابق النص،
    ويرجع اسمها كما تم تسجيله إذا كانت مقفولة حاليا لهذا البوت تحديدا، أو None
    إذا كانت مفتوحة أو غير مسجلة أساسا. القفل هنا مستقل تماما عن أي بوت آخر.

    المطابقة تشمل الأمر مع أي معاملات تالية له (مثل "ايدي 1" أو "ايدي 2 3")
    طالما بدأ النص بنفس اسم الأمر المسجل متبوعا بمسافة، أو كان مطابقا له تماما.
    هذا لا يطابق كلمات أخرى تبدأ بنفس الحروف بدون مسافة فاصلة (مثل "ايديه"
    عند قفل "ايدي")، لأنها تعتبر أمرا مختلفا يجب قفله بشكل منفصل إن أُريد."""
    if not bot_id or not text:
        return None
    services = await get_bot_registered_services(bot_id)
    if not services:
        return None
    text_norm = str(text).strip().lower()
    if not text_norm:
        return None
    matched = None
    for name in services:
        name_norm = str(name).strip().lower()
        if not name_norm:
            continue
        if text_norm == name_norm or text_norm.startswith(name_norm + ' '):
            matched = name
            break
    if not matched:
        return None
    if await is_service_enabled(bot_id, matched):
        return None
    return matched


async def isLockCommand(user_id: int, chat_id: int, text: str, client: CompatClient = None):
    if user_id is None or chat_id is None:
        return None

    data = await _get_bot_data_async(client)
    bot_id = data['bot_id']
    r = data['redis']

    if not bot_id:
        return None

    if not await r.hgetall(bot_id + f"locks-{chat_id}"):
        return None

    commands = await r.hgetall(bot_id + f"locks-{chat_id}")
    matched_command = None

    for command_key in commands:
        if command_key.lower() == text.lower():
            matched_command = command_key
            break

    if not matched_command:
        return None

    cc = int(commands[matched_command])
    rank_name = ""

    if cc == 0:
        if not await gowner_pls(user_id, chat_id, client):
            rank_name = "المالك الاساسي"
        else:
            return None
    elif cc == 1:
        if not await owner_pls(user_id, chat_id, client):
            rank_name = "المالك"
        else:
            return None
    elif cc == 2:
        if not await mod_pls(user_id, chat_id, client):
            rank_name = "المدير"
        else:
            return None
    elif cc == 3:
        if not await admin_pls(user_id, chat_id, client) and not await fake_rank_pls(user_id, chat_id, 'restrict', client):
            rank_name = "الادمن"
        else:
            return None
    elif cc == 4:
        if not await pre_pls(user_id, chat_id, client):
            rank_name = "المميز"
        else:
            return None

    return rank_name if rank_name else None


async def check_and_guard_locked_command(c, m, k, processed_text):
    if not m or not m.from_user:
        return True

    client = c

    # قفل الخدمات المدفوعة: قفل مركزي خاص بـ Bot ID محدد فقط (عبر plugins/devs.py)،
    # مستقل تماما عن أي بوت آخر في الـ Clusters ولا يتأثر بقفل الرتب أدناه.
    bot_data = await _get_bot_data_async(client)
    bot_id = bot_data.get('bot_id') if bot_data else None
    if bot_id and await find_locked_bot_service(bot_id, processed_text):
        return True

    required_rank = await isLockCommand(m.from_user.id, m.chat.id, processed_text, client)

    if required_rank:
        data = await _get_bot_data_async(client)
        bot_id = data['bot_id']
        r = data['redis']

        if bot_id:
            response_lock_key = f"sent_lock_response:{m.chat.id}:{m.id}:{bot_id}"
            if not await r.set(response_lock_key, "1", nx=True, ex=3):
                return True
        try:
            await m.reply(quote=True, text=helpers_ranks_551(k, required_rank))
        except Exception:
            pass
        return True

    return False


async def check_global_restrictions(c, m, k, caller: str = None) -> bool:
    """نقطة الدخول العامة. تحافظ على نفس المنطق والتخزين المؤقت على m."""
    cache = getattr(m, "_grchk_cache", None)
    if cache is None:
        cache = {}
        try:
            setattr(m, "_grchk_cache", cache)
        except Exception:
            cache = None

    if cache is not None and caller in cache:
        return cache[caller]

    result = await _check_global_restrictions_impl(c, m, k, caller=caller)

    if cache is not None:
        cache[caller] = result

    return result


async def _check_global_restrictions_impl(c, m, k, caller: str = None) -> bool:
    bot_id = getattr(c, "bot_id", None) or getattr(c, "dev_final", None)

    if not bot_id:
        bot_id = get_current_bot_id()

    if not bot_id:
        bot_id = get_global_dev()

    if bot_id and bot_id in _bot_contexts:
        r = _bot_contexts[bot_id].get("redis")
        if r is None:
            from helpers.redis import RedisFake
            r = RedisFake(bot_id=bot_id)
    else:
        r = get_global_r()

    Dev_FINAL = bot_id or get_global_dev()
    k = get_global_k()

    if not await r.get(f'{m.chat.id}:enable:{Dev_FINAL}'):
        return False

    # الرسالة الشائعة (بوت مفعّل بالمجموعة) تكمل عبر كل الفحوصات التالية
    # بالتتابع أصلاً، لذلك نجلب قيمها الخام دفعة واحدة (جولة Redis واحدة
    # بدل 6) — لكن نستدعي admin_pls/fake_rank_pls (والتي قد تجلب مفاتيح
    # إضافية) بنفس الشرط والترتيب الأصليين تماماً، فقط عند الحاجة الفعلية.
    lock_text_v, mute_chat_v, gban_user_v, mute_user_v, mute_user_chat_v, gbangames_v = await r.get_many([
        f'{m.chat.id}:lockText:{Dev_FINAL}',
        f'{m.chat.id}:mute:{Dev_FINAL}',
        f'{m.from_user.id}:gban:{Dev_FINAL}',
        f'{m.from_user.id}:mute:{Dev_FINAL}',
        f'{m.from_user.id}:mute:{m.chat.id}{Dev_FINAL}',
        f'{m.from_user.id}:gbangames:{Dev_FINAL}',
    ])

    if lock_text_v and not await admin_pls(m.from_user.id, m.chat.id):
        return False

    if mute_chat_v and not await admin_pls(m.from_user.id, m.chat.id):
        return False

    if gban_user_v and not await fake_rank_pls(m.from_user.id, m.chat.id, 'ban'):
        try:
            await m.chat.ban_member(m.from_user.id)
        except Exception:
            pass
        return False

    if mute_user_v and not await fake_rank_pls(m.from_user.id, m.chat.id, 'mute'):
        return False

    if mute_user_chat_v and not await fake_rank_pls(m.from_user.id, m.chat.id, 'mute'):
        return False

    if gbangames_v:
        return False

    text = m.text or ""

    # كل مفاتيح حالة "بانتظار إدخال تالٍ" (رد/أمر/زر/استبدال/إنلاين) مستقلة
    # عن بعضها ولا يوجد بينها اعتماد بالترتيب — النتيجة النهائية لكل متغيّر
    # (is_adding_reply, is_adding_command, ...) هي OR بسيط، فتُجلب كل الـ34
    # مفتاحاً دفعة واحدة بجولة Redis واحدة بدل حتى 34 جولة متسلسلة على كل
    # رسالة عادية (هذا كان أثقل نقطة استدعاءات متكررة في الملف). الأسماء
    # والمفاتيح (بما فيها الخطأ المطبعي القائم أصلاً في مفتاح addCustomG بلا
    # ":" بعد chat.id) بقيت كما هي بالحرف حفاظاً على نفس السلوك تماماً.
    _flag_keys = [
        f'{m.chat.id}:addFilter:{m.from_user.id}{Dev_FINAL}',
        f'{m.chat.id}:addFilter2:{m.from_user.id}{Dev_FINAL}',
        f'{m.chat.id}:addFilterM:{m.from_user.id}{Dev_FINAL}',
        f'{m.chat.id}:addFilterM2:{m.from_user.id}{Dev_FINAL}',
        f'{m.chat.id}:addFilterS:{m.from_user.id}{Dev_FINAL}',
        f'{m.chat.id}:addFilterS2:{m.from_user.id}{Dev_FINAL}',
        f'{m.chat.id}:addFilterMM:{m.from_user.id}{Dev_FINAL}',
        f'{m.chat.id}:addFilterG:{m.from_user.id}{Dev_FINAL}',
        f'{m.chat.id}:addFilterG2:{m.from_user.id}{Dev_FINAL}',
        f'{m.chat.id}:addFilterGM:{m.from_user.id}{Dev_FINAL}',
        f'{m.chat.id}:addFilterGM2:{m.from_user.id}{Dev_FINAL}',
        f'{m.chat.id}:addFilterGS:{m.from_user.id}{Dev_FINAL}',
        f'{m.chat.id}:addFilterGS2:{m.from_user.id}{Dev_FINAL}',
        f'{m.chat.id}:delCustom:{m.from_user.id}{Dev_FINAL}',
        f'{m.chat.id}:delCustomG:{m.from_user.id}{Dev_FINAL}',
        f'{m.chat.id}:delFilter:{m.from_user.id}{Dev_FINAL}',
        f'{m.chat.id}:delFilterM:{m.from_user.id}{Dev_FINAL}',
        f'{m.chat.id}:delFilterS:{m.from_user.id}{Dev_FINAL}',
        f'{m.chat.id}:delFilterG:{m.from_user.id}{Dev_FINAL}',
        f'{m.chat.id}:delFilterGM:{m.from_user.id}{Dev_FINAL}',
        f'{m.chat.id}:delFilterGS:{m.from_user.id}{Dev_FINAL}',
        f'{m.chat.id}:delInlineGlobal:{m.from_user.id}{Dev_FINAL}',  # هذا المفتاح موجود بالفعل لمسح الرد، ولكن يمكنك إضافته هنا أيضاً للتأكيد
        f'{m.chat.id}:addCustom:{m.from_user.id}{Dev_FINAL}',
        f'{m.chat.id}:addCustom2:{m.from_user.id}{Dev_FINAL}',
        f'{m.chat.id}addCustomG:{m.from_user.id}{Dev_FINAL}',
        f'{m.chat.id}:addCustom2G:{m.from_user.id}{Dev_FINAL}',
        f"btn_waiting_name:global:{m.from_user.id}",
        f"btn_edit_state:global:{m.from_user.id}",
        f"btn_emoji_state:global:{m.from_user.id}",
        f'{m.chat.id}:replace:{m.from_user.id}{Dev_FINAL}',
        f'{m.chat.id}:replace2:{m.from_user.id}{Dev_FINAL}',
        f'{m.chat.id}:replace3:{m.from_user.id}{Dev_FINAL}',
        f'{m.chat.id}:addInlineStep:{m.from_user.id}{Dev_FINAL}',
        f'{m.chat.id}:addInlineStepGlobal:{m.from_user.id}{Dev_FINAL}',
    ]
    _flag_vals = await r.get_many(_flag_keys)

    is_adding_reply = any(_flag_vals[0:22])
    is_adding_command = any(_flag_vals[22:26])
    is_deleting = None
    is_managing_buttons = any(_flag_vals[26:29])
    is_replacing = any(_flag_vals[29:32])
    is_adding_inline = any(_flag_vals[32:34])

    if is_adding_command or is_adding_reply:
        if text == 'الغاء' or text == 'تم':
            return True
        if is_adding_reply and caller == 'reply':
            return True
        setattr(m, '_is_adding_mode', True)
        return False

    if is_managing_buttons or is_replacing or is_adding_inline or is_deleting:
        if text == 'الغاء' or text == 'تم':
            return True
        return False

    if hasattr(m, '_is_adding_mode') and m._is_adding_mode:
        return False

    name = await r.get(f'{Dev_FINAL}:BotName') or 'فاينل'
    if text.startswith(f'{name} '):
        text = text.replace(f'{name} ', '')

    local_custom = await r.get(f'{m.chat.id}:Custom:{m.chat.id}{Dev_FINAL}&text={text}')
    if local_custom:
        text = local_custom

    global_custom = await r.get(f'Custom:{Dev_FINAL}&text={text}')
    if global_custom:
        text = global_custom

    if await check_and_guard_locked_command(c, m, k, text):
        return False

    return True


_USERNAME_RE = re.compile(r"@(\w{4,32})")


async def extract_target_user(c: CompatClient, m) -> Optional[CompatUser]:
    """
    يحدد "المستخدم الهدف" لأمر ما (كتم / كشف / طرد ... إلخ) بغض النظر عن
    طريقة تحديده في الرسالة، ويرجعه دائماً بواجهة CompatUser الموحّدة
    (نفس الواجهة المستخدمة في كل الكود الحالي: .id / .first_name /
    .username / .is_bot / .mention ...).

    - رد على رسالة، أو Text Mention (منشن مربوط فعلياً بمستخدم داخل الرسالة):
      تُحل عبر aiogram مباشرة بدون أي طلب شبكة إضافي.
    - منشن بصيغة "@يوزرنيم" (بدون رد): aiogram / Bot API لا يقدر يحل
      اليوزرنيم لمستخدم غير معروف له، فنستخدم عميل Pyrogram الجاهز
      (get_bot_pyro_client) الذي يملك مرونة أوسع لحل اليوزرنيمات.

    لا تعدّل هذه الدالة أي شيء ولا ترسل أي رسالة؛ فقط تُرجع المستخدم أو None.
    """
    if m.reply_to_message and m.reply_to_message.from_user:
        return m.reply_to_message.from_user

    if m.entities:
        for e in m.entities:
            if e.type == MessageEntityType.TEXT_MENTION and e.user:
                return e.user

    text = m.text or getattr(m, "caption", None)
    if not text:
        return None

    match = _USERNAME_RE.search(text)
    if not match:
        return None

    resolved_id = await resolve_user_id_from_arg(match.group(0))
    if not resolved_id:
        return None

    try:
        return await c.get_users(resolved_id)
    except Exception:
        pass

    # احتياطي نادر: لو تعذّر جلب المستخدم عبر aiogram (get_chat) رغم أننا
    # نملك آيديه، نبني كائناً متوافقاً بالحد الأدنى بدل إرجاع None بلا داعٍ.
    aio_user = AioUser(id=resolved_id, is_bot=False, first_name=match.group(0).lstrip("@"))
    return CompatUser(aio_user, c)


async def resolve_user_id_from_arg(arg: str) -> Optional[int]:
    """
    تحوّل معامل نصي جاء بعد الأمر (مثل "كتم @fgggg" أو "كتم 123456") إلى
    آيدي رقمي فعلي:
    - آيدي رقمي (أو سالب لقناة) يُرجع كما هو فوراً بدون أي طلب شبكة.
    - "@يوزرنيم": نتحقق أولاً من خريطة Redis المشتركة بين كل بوتات الكلاستر
      (helpers.redis.get_cached_username_id) — مُغذّاة انتهازياً من أي رسالة
      يرسلها ذلك المستخدم لأي بوت. لو موجود، نرجعه فوراً بدون أي طلب شبكة.
      فقط لو غير موجود بالكاش (أول مرة نرى هذا اليوزرنيم إطلاقاً) نلجأ
      لعميل Pyrogram المشترك (get_bot_pyro_client) لحلّه، ثم نخزّنه بالكاش
      فوراً حتى لا نحتاج Pyrogram له مرة أخرى مستقبلاً.

    ترجع None إذا تعذر تحديد آيدي حقيقي (يوزرنيم غير موجود/غير صالح)، حتى لا
    يمرَّر نص عشوائي لاحقاً ويُظن أنه آيدي مستخدم آخر.
    """
    if arg is None:
        return None
    arg = arg.strip()
    if not arg:
        return None

    bare = arg.lstrip("-")
    if bare.isdigit():
        return int(arg)

    username = arg.lstrip("@").strip()
    if not username:
        return None

    try:
        from helpers.redis import get_cached_username_id
        cached_id = await get_cached_username_id(username)
        if cached_id:
            return cached_id
    except Exception:
        pass

    try:
        from plugins.FinalMusic.fm_core.l1_cache import get_bot_pyro_client
        pyro = await get_bot_pyro_client()
        if pyro is None:
            return None
        pyro_user = await pyro.get_users(username)
    except Exception:
        return None

    resolved_id = getattr(pyro_user, "id", None)
    if resolved_id:
        try:
            from helpers.redis import cache_username_id
            await cache_username_id(username, resolved_id)
        except Exception:
            pass
    return resolved_id




__all__ = [
    'get_rank',
    'admin_pls',
    'mod_pls',
    'owner_pls',
    'gowner_pls',
    'dev_pls',
    'dev2_pls',
    'devp_pls',
    'myt_pls',
    'pre_pls',
    'get_devs_br',
    'get_fake_rank_perms',
    'fake_rank_pls',
    'has_fake_rank',
    'fake_rank_protected',
    'UPFAKE_PERM_KEYS',
    'is_service_enabled',
    'register_bot_service',
    'get_bot_registered_services',
    'get_bot_service_lock_map',
    'find_locked_bot_service',
    'isLockCommand',
    'check_and_guard_locked_command',
    'check_global_restrictions',
    'extract_target_user',
    'resolve_user_id_from_arg',
]
