from helpers.context import get_global_r, get_global_dev, get_global_k
r = get_global_r()
Dev_FINAL = get_global_dev()
k = get_global_k()
from helpers.redis import r as _shared_r

"""
[ = This plugin is a part from Rfinal Source code = ]
{"Developer":"https://t.me/i0i0ii"}
"""
import asyncio
import time
import random
import os
import requests
from compat import ChatAction
from pydub import AudioSegment
import speech_recognition as sr
from gtts import gTTS
import re
import pytz
import gtts
from hijri_converter import Hijri, Gregorian
from datetime import datetime
from threading import Thread
from compat import *
from compat import *
from compat import *
# NOTE: compat.py does `import datetime` (the module) and its __all__
# doesn't exclude that name, so "from compat import *" above re-exports
# the module and overwrites the class imported by
# "from datetime import datetime" earlier in this file. That's what made
# datetime.now(...) fail with "module 'datetime' has no attribute 'now'" —
# it was actually calling module.now() instead of class.now().
# Re-import the class last so it wins.
from datetime import datetime
from helpers.ranks import *
from helpers.persian import persianInformation
from .welcome import *
from PIL import Image
from asyncio import run as RUN
from Python_ARQ import ARQ
from aiohttp import ClientSession
from mutagen.mp3 import MP3 as mutagenMP3


ARQ_API_KEY = "OZJRWV-SAURXD-PMBUKF-GMVSNS-ARQ"
ARQ_API_URL = "https://arq.hamker.dev"

list_UwU = [
    "كس",
    "كسمك",
    "كسختك",
    "عير",
    "كسخالتك",
    "خرا بالله",
    "عير بالله",
    "كسخواتكم",
    "كحاب",
    "مناويج",
    "مناويج",
    "كحبه",
    "ابن الكحبه",
    "فرخ",
    "فروخ",
    "طيزك",
    "طيزختك",
    "كسمك",
    "يا ابن الخول",
    "المتناك",
    "شرموط",
    "شرموطه",
    "ابن الشرموطه",
    "ابن الخول",
    "ابن العرص",
    "منايك",
    "متناك",
    "ابن المتناكه",
    "زبك",
    "عرص",
    "زبي",
    "خول",
    "لبوه",
    "لباوي",
    "ابن اللبوه",
    "منيوك",
    "كسمكك",
    "متناكه",
    "يا عرص",
    "يا خول",
    "قحبه",
    "القحبه",
    "شراميط",
    "العلق",
    "العلوق",
    "العلقه",
    "كسمك",
    "يا ابن الخول",
    "المتناك",
    "شرموط",
    "شرموطه",
    "ابن الشرموطه",
    "ابن الخول",
    "االمنيوك",
    "كسمككك",
    "الشرموطه",
    "ابن العرث",
    "ابن الحيضانه",
    "زبك",
    "خول",
    "زبي",
    "قاحب",
]

list_Shiaa = [
    "يا علي",
    "يا حسين",
    "ياعلي",
    "ياحسين",
    "علي ولي الله",
    "عليا ولي الله",
    "عائشه زانيه",
    "عائشة زانية",
    "عائشة عاهرة",
    "عائشه عاهره",
    "خرب ربك",
    "خرب الله",
    "يلعن ربك",
    "يلعن الله",
    "يا عمر",
    "ياعمر",
    "يا محمد",
    "يامحمد",
    "زوجات الرسول",
    "عير بالسنة",
    "عير بالسنه",
    "خرب السنه",
    "خرا بالسنه",
    "خرب السنة",
    "خرا بالسنة",
    "والحسين",
    "والعباس",
    "وعلي",
    "والامام علي",
    "ربنا علي",
    "علي الله",
    "الله علي",
    "رب علي",
    "علي رب",
]

def Find(text):
    m = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(m, text)
    return [x[0] for x in url]

import os
import json
from helpers.replies_store import (
    plugins_protect_423,
)



JSON_DATA_PATH = "group_data/"

def save_group_data(chat_id, data):
    # التأكد من وجود المجلد، وإنشاؤه إذا لم يكن موجودًا
    os.makedirs(JSON_DATA_PATH, exist_ok=True)
    
    file_path = f"{JSON_DATA_PATH}{chat_id}.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_group_data(chat_id):
    file_path = f"{JSON_DATA_PATH}{chat_id}.json"
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

def get_for_verify(me):
    for_verify = [
        {
            "question": "ماهو الحيوان الذي ينتهي اسمه بحرف الباء ؟",
            "key": InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("فأر", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("وشق", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("بشار الأسد", callback_data=f"no:{me.id}"),
                    ],
                    [
                        InlineKeyboardButton("حمار", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("كلب", callback_data=f"yes:{me.id}"),
                        InlineKeyboardButton("قطة", callback_data=f"no:{me.id}"),
                    ],
                ]
            ),
        },
        {
            "question": "ماهي عاصمة فرنسا؟",
            "key": InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("دمشق", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("الرياض", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("باريس", callback_data=f"yes:{me.id}"),
                    ],
                    [
                        InlineKeyboardButton("الكويت", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("القاهرة", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("ماشا والدب", callback_data=f"no:{me.id}"),
                    ],
                ]
            ),
        },
        {
            "question": "نادي يبدأ بحرف الباء :",
            "key": InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("برشلونا", callback_data=f"yes:{me.id}"),
                        InlineKeyboardButton("الهلال", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("النصر", callback_data=f"no:{me.id}"),
                    ],
                    [
                        InlineKeyboardButton("الزمالك", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("﷼ مدريد", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("مانشستر", callback_data=f"no:{me.id}"),
                    ],
                ]
            ),
        },
        {
            "question": "دولة يبدأ اسمها بحرف التاء :",
            "key": InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("قطر", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("امريكا", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("سوريا", callback_data=f"no:{me.id}"),
                    ],
                    [
                        InlineKeyboardButton("مصر", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("الصين", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("تركيا", callback_data=f"yes:{me.id}"),
                    ],
                ]
            ),
        },
        {
            "question": "اختر هذا الايموجي - 🤑 -",
            "key": InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🍭", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("🤑", callback_data=f"yes:{me.id}"),
                        InlineKeyboardButton("🏆", callback_data=f"no:{me.id}"),
                    ],
                    [
                        InlineKeyboardButton("🌀", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("🪨", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("💎", callback_data=f"no:{me.id}"),
                    ],
                ]
            ),
        },
        {
            "question": "اختر هذا الايموجي - 🔓 -",
            "key": InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🏆", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("💎", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("🙄", callback_data=f"no:{me.id}"),
                    ],
                    [
                        InlineKeyboardButton("💸", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("💣", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("🔓", callback_data=f"yes:{me.id}"),
                    ],
                ]
            ),
        },
        {
            "question": "اختر هذا الايموجي - 🌠 -",
            "key": InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("☄️", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("🙈", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("🦄", callback_data=f"no:{me.id}"),
                    ],
                    [
                        InlineKeyboardButton("🌠", callback_data=f"yes:{me.id}"),
                        InlineKeyboardButton("🌈", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("🧑‍💻", callback_data=f"no:{me.id}"),
                    ],
                ]
            ),
        },
        {
            "question": "ماهي عاصمة سوريا",
            "key": InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("دمشق", callback_data=f"yes:{me.id}"),
                        InlineKeyboardButton("دير الزور", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("ادلب", callback_data=f"no:{me.id}"),
                    ],
                    [
                        InlineKeyboardButton("فاينل ميسي", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("الرياض", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("مزة فيلات", callback_data=f"no:{me.id}"),
                    ],
                ]
            ),
        },
        {
            "question": "ماهي عملة الولايات المتحدة الأمريكية",
            "key": InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("الروبية", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("الجنيه", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("الليرة", callback_data=f"no:{me.id}"),
                    ],
                    [
                        InlineKeyboardButton("الدولار", callback_data=f"yes:{me.id}"),
                        InlineKeyboardButton("الدينار", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("الين", callback_data=f"no:{me.id}"),
                    ],
                ]
            ),
        },
        {
            "question": "اسم مذكر يبدأ بحرف ز",
            "key": InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("زيد", callback_data=f"yes:{me.id}"),
                        InlineKeyboardButton("علي", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("محمد", callback_data=f"no:{me.id}"),
                    ],
                    [
                        InlineKeyboardButton("عمر", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("المريخ", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("احمد", callback_data=f"no:{me.id}"),
                    ],
                ]
            ),
        },
        {
            "question": "اسم مؤنث ينتهي بحرف ي",
            "key": InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("لورين", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("ماجدة", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("علياء", callback_data=f"no:{me.id}"),
                    ],
                    [
                        InlineKeyboardButton("أماني", callback_data=f"yes:{me.id}"),
                        InlineKeyboardButton("فرح", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("أمل", callback_data=f"no:{me.id}"),
                    ],
                ]
            ),
        },
        {
            "question": "اسم مؤنث يبدأ بحرف أ",
            "key": InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("لورين", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("ماجدة", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("علياء", callback_data=f"no:{me.id}"),
                    ],
                    [
                        InlineKeyboardButton("أمل", callback_data=f"yes:{me.id}"),
                        InlineKeyboardButton("فرح", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("يمنى", callback_data=f"no:{me.id}"),
                    ],
                ]
            ),
        },
        {
            "question": "الأسبوع كم يوم؟",
            "key": InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("1", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("2", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("3", callback_data=f"no:{me.id}"),
                    ],
                    [
                        InlineKeyboardButton("4", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("5", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("6", callback_data=f"no:{me.id}"),
                    ],
                    [
                        InlineKeyboardButton("7", callback_data=f"yes:{me.id}"),
                        InlineKeyboardButton("8", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("9", callback_data=f"no:{me.id}"),
                    ],
                ]
            ),
        },
    ]
    return random.choice(for_verify)

async def scanR(c, m, id, file):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    await scan4(c, m, id, file)

async def scan4(c, m, id, file):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    session = ClientSession()
    arq = ARQ(ARQ_API_URL, ARQ_API_KEY, session)
    resp = await arq.nsfw_scan(file=file)
    if resp.result.is_nsfw:
        await m.delete()
        k = await r.get(f"{Dev_FINAL}:botkey")
        await m.reply(
            plugins_protect_423(m.from_user.mention(), k)
        )
    os.remove(file)
    await session.close()

def get_top(users):
    users.sort(key=lambda x: x["money"], reverse=True)
    return users

def get_emoji_bank(count):
    if count == 1:
        return "🥇 "
    elif count == 2:
        return "🥈 "
    elif count == 3:
        return "🥉 "
    else:
        return ""

async def get_chat_score(chat_id):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    score = await r.get(f'{chat_id}:quiz_score:{Dev_FINAL}')
    return int(score) if score else 0

async def get_chat_name_from_api(chat_id, client):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    try:
        chat = await client.get_chat(chat_id)
        title = chat.title
        await r.set(f'{chat_id}:chat_title:{Dev_FINAL}', title)
        return title
    except Exception:
        return f"Chat {chat_id}"

def _decode_if_bytes(value):
    if isinstance(value, bytes):
        return value.decode('utf-8')
    return value

def run_async_in_thread(coro):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)

def get_top_by_key(users, sort_key='money'):
    if not users:
        return []
    users.sort(key=lambda x: x.get(sort_key, 0), reverse=True)
    return users


async def claim_event_once(dedup_key: str, ttl_seconds: int = 300) -> bool:
    """
    يضمن تنفيذ أي حدث مرة واحدة فقط، مهما تكرر استدعاؤه (بسبب أكثر من بوت/هاندلر
    يعالج نفس الرسالة الفعلية داخل نفس المجموعة، أو بسبب إعادة تشغيل/تحميل).

    يرجع True فقط لأول استدعاء بنفس dedup_key، وأي استدعاء لاحق بنفس المفتاح
    (خلال مدة ttl_seconds) يرجع False ولا يجب تنفيذ أي عملية تسجيل/إضافة عندها.

    العملية ذرية بالكامل (sadd ترجع 1 فقط لأول من يضيف العضو، 0 لأي تكرار لاحق)
    ولا تحتاج قفل خارجي.

    يستخدم مخزن Redis المشترك (غير المعزول لكل بوت) عمداً: أي dedup_key يحتاج أن
    يبقى محلياً لكل بوت (مثل تفاعل الأعضاء المحلي) يُضمّن معرف البوت داخل نص
    المفتاح نفسه من قِبل المستدعي، بينما أي dedup_key عام (مثل groupmsg/gameearn)
    يعمل بشكل صحيح كمنع تكرار موحّد بين كل بوتات الكلاستر فقط عند استخدام مخزن مشترك.
    """
    key = f"evtclaim:{dedup_key}"
    claimed = await _shared_r.sadd(key, "1")
    if claimed:
        await _shared_r.expire(key, ttl_seconds)
    return bool(claimed)


GLOBAL_TOP_NS = "GLOBAL"


async def update_chat_title_cache(chat_id, title: str):
    """
    تحديث اسم المجموعة المخزّن بشكل مشترك (عام) بين كل البوتات، يُستخدم في
    توبات المجموعات المشتركة. يكتب فقط عند وجود فرق فعلي لتقليل الحمل على قاعدة البيانات.
    يستخدم مخزن Redis المشترك (غير المعزول) عمداً - وليس get_global_r() - حتى لا
    يُخزَّن اسم كل مجموعة بشكل منفصل تحت معرف كل بوت.
    """
    if not title:
        return
    title_key = f'{chat_id}:chat_title:{GLOBAL_TOP_NS}'
    cached = _decode_if_bytes(await _shared_r.get(title_key))
    if cached != title:
        await _shared_r.set(title_key, title)


async def record_group_interaction(chat_id, message_id, title: str = None):
    """
    تسجيل ذري لتفاعل مجموعة واحدة ضمن 'توب القروبات الأكثر تفاعلاً'،
    مع تحديث اسم المجموعة تلقائياً، ومحمي بالكامل من التكرار عند تعدد
    البوتات/الهاندلرات في نفس المجموعة لنفس الرسالة الفعلية.

    المفتاح مشترك (لا يعتمد على Dev_FINAL، ويُكتب عبر مخزن Redis المشترك غير
    المعزول) ليكون توب القروبات موحداً وعاماً بين جميع بوتات الكلاسترز - بما فيها
    البوت الأب - وليس محلياً لكل بوت على حدة.
    """
    if not await claim_event_once(f"groupmsg:{chat_id}:{message_id}"):
        return
    await _shared_r.incrby(f'{GLOBAL_TOP_NS}:TotalGroupMsgs:{chat_id}', 1)
    if title:
        await update_chat_title_cache(chat_id, title)


def extract_id_before_marker(raw_key: str, marker: str) -> int:
    """
    يستخرج رقماً (مثل chat_id) من مفتاح Redis خام قبل marker معيّن، بغض النظر
    عن أي بادئة عزل إضافية (مثل بادئة معرف البوت) قد تسبقه في المفتاح الفعلي.
    مثال: 'BOT123:987654:game_earnings:BOT123' + marker=':game_earnings:' → 987654
    """
    part = raw_key.split(marker)[0]
    part = part.rsplit(':', 1)[-1]
    return int(part)


