import os
import json
import sqlite3
import uuid

from compat import Client, filters, ChatType
from helpers.context import get_redis, get_current_bot_id
from plugins.attachments import safe_download

AEC_ID = 5434703779

TMP_DIR = '/tmp/data_migration'
os.makedirs(TMP_DIR, exist_ok=True)

OWNER_RANK_NAMES = ('المالك الاساسي', 'المالك')
GOWNER_RANK_NAME = 'المالك الاساسي'

MENU_TEXT = (
    "تم استلام قاعدة البيانات والتعرف عليها\n"
    "اختر رقما من القائمة لبدء الترحيل\n\n"
    "1. المستخدمين عددهم ↤︎ {users}\n"
    "2. المجموعات عددهم ↤︎ {groups}\n"
    "3. المالكين عددهم ↤︎ {owners}\n"
    "4. توب المتفاعلين لكل مجموعة\n"
    "5. اللايكات والدسلايكات\n"
    "6. المجموعات المفعلة\n"
    "7. كل القائمة\n"
    "8. الغاء"
)


def _awaiting_db_key(user_id):
    return f'migrate:awaitingDb:{user_id}'


def _db_path_key(user_id):
    return f'migrate:dbPath:{user_id}'


def _stats_key(user_id):
    return f'migrate:stats:{user_id}'


def _open_db(path):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def _compute_stats(path):
    conn = _open_db(path)
    try:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM users")
        users = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM groups")
        groups = cur.fetchone()[0]
        cur.execute(
            "SELECT COUNT(*) FROM group_ranks WHERE rank IN (?,?)",
            OWNER_RANK_NAMES,
        )
        owners = cur.fetchone()[0]
        return {"users": users, "groups": groups, "owners": owners}
    finally:
        conn.close()


@Client.on_message(filters.text & filters.private, group=-8000)
async def migrate_start_handler(c, m):
    if m.from_user.id != AEC_ID:
        return
    if (m.text or '').strip() != 'ترحيل البيانات':
        return

    r = get_redis()
    await r.set(_awaiting_db_key(m.from_user.id), 1, ex=1800)
    await r.delete(_db_path_key(m.from_user.id))
    await r.delete(_stats_key(m.from_user.id))

    await m.reply(
        "حسنا عزيزي ارسل قاعدة البيانات\n"
        "سيتم ترحيل البيانات لهذا البوت حصرا"
    )


@Client.on_message(filters.document & filters.private, group=-8000)
async def migrate_receive_db_handler(c, m):
    if m.from_user.id != AEC_ID:
        return

    r = get_redis()
    if not await r.get(_awaiting_db_key(m.from_user.id)):
        return

    dest_path = os.path.join(TMP_DIR, f'{uuid.uuid4().hex}.sqlite')
    try:
        await safe_download(m, dest_path)
    except Exception:
        await m.reply("تعذر تحميل الملف، ارسله مرة اخرى")
        return

    try:
        stats = _compute_stats(dest_path)
    except Exception:
        try:
            os.remove(dest_path)
        except Exception:
            pass
        await m.reply("هذا الملف ليس قاعدة بيانات صالحة، ارسل ملف sqlite صحيح او اكتب \"الغاء\"")
        return

    await r.delete(_awaiting_db_key(m.from_user.id))
    await r.set(_db_path_key(m.from_user.id), dest_path, ex=3600)
    await r.set(_stats_key(m.from_user.id), json.dumps(stats), ex=3600)

    await m.reply(MENU_TEXT.format(**stats))


async def _migrate_users(r, bot_id, conn):
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM users")
    rows = [str(row[0]) for row in cur.fetchall() if row[0]]
    count = 0
    for uid in rows:
        await r.sadd(f'{bot_id}:UsersList', uid)
        count += 1
    return count


async def _migrate_groups(r, bot_id, conn):
    cur = conn.cursor()
    cur.execute("SELECT group_id, active FROM groups")
    rows = cur.fetchall()
    count = 0
    for group_id, active in rows:
        await r.sadd(f'{bot_id}:AllGroupsList', str(group_id))
        if active:
            await r.set(f'{group_id}:enable:{bot_id}', 1)
            await r.sadd(f'enablelist:{bot_id}', str(group_id))
        count += 1
    return count


async def _migrate_owners(r, bot_id, conn):
    cur = conn.cursor()
    cur.execute(
        "SELECT group_id, user_id, rank FROM group_ranks WHERE rank IN (?,?)",
        OWNER_RANK_NAMES,
    )
    rows = cur.fetchall()
    count = 0
    for group_id, user_id, rank in rows:
        if rank == GOWNER_RANK_NAME:
            await r.set(f'{group_id}:rankGOWNER:{user_id}{bot_id}', 1)
        else:
            await r.set(f'{group_id}:rankOWNER:{user_id}{bot_id}', 1)
        count += 1
    return count


async def _migrate_top_interactive(r, bot_id, conn):
    cur = conn.cursor()
    cur.execute("SELECT chat_id, user_id, count FROM interactors WHERE count > 0")
    rows = cur.fetchall()

    per_group = {}
    for chat_id, user_id, count in rows:
        per_group.setdefault(str(chat_id), {})[str(user_id)] = count

    for chat_id, mapping in per_group.items():
        await r.zadd(f'TotalMsgsSorted:{chat_id}:{bot_id}', mapping)
        for user_id, count in mapping.items():
            await r.set(f'{bot_id}{chat_id}:TotalMsgs:{user_id}', count)

    return len(rows)


async def _migrate_likes_dislikes(r, bot_id, conn):
    cur = conn.cursor()
    reactions = {}

    cur.execute("SELECT user_id, liked_by_user_id FROM user_like_users")
    for user_id, liker_id in cur.fetchall():
        entry = reactions.setdefault(str(user_id), {"likes": set(), "dislikes": set()})
        entry["likes"].add(str(liker_id))

    cur.execute("SELECT user_id, disliked_by_user_id FROM user_dislike_users")
    for user_id, disliker_id in cur.fetchall():
        entry = reactions.setdefault(str(user_id), {"likes": set(), "dislikes": set()})
        entry["dislikes"].add(str(disliker_id))

    for user_id, entry in reactions.items():
        likes = list(entry["likes"])
        dislikes = list(entry["dislikes"])
        await r.set(f'global_reactions:{user_id}', json.dumps({"likes": likes, "dislikes": dislikes}))
        await r.set(f'{user_id}:global_likes:{bot_id}', len(likes))
        await r.set(f'{user_id}:global_dislikes:{bot_id}', len(dislikes))

    return len(reactions)


async def _migrate_active_groups(r, bot_id, conn):
    cur = conn.cursor()
    cur.execute("SELECT group_id FROM groups WHERE active = 1")
    rows = [str(row[0]) for row in cur.fetchall()]
    for group_id in rows:
        await r.set(f'{group_id}:enable:{bot_id}', 1)
        await r.sadd(f'enablelist:{bot_id}', group_id)
    return len(rows)


ACTIONS = {
    '1': ('users', 'المستخدمين', _migrate_users),
    '2': ('groups', 'المجموعات', _migrate_groups),
    '3': ('owners', 'المالكين', _migrate_owners),
    '4': ('top', 'توب المتفاعلين', _migrate_top_interactive),
    '5': ('reactions', 'اللايكات والدسلايكات', _migrate_likes_dislikes),
    '6': ('active', 'المجموعات المفعلة', _migrate_active_groups),
}


@Client.on_message(filters.text & filters.private, group=-7999)
async def migrate_choice_handler(c, m):
    if m.from_user.id != AEC_ID:
        return

    r = get_redis()
    db_path = await r.get(_db_path_key(m.from_user.id))
    if not db_path or not os.path.exists(db_path):
        return

    choice = (m.text or '').strip()
    if choice not in ('1', '2', '3', '4', '5', '6', '7', '8'):
        return

    bot_id = get_current_bot_id()

    if choice == '8':
        await r.delete(_db_path_key(m.from_user.id))
        await r.delete(_stats_key(m.from_user.id))
        try:
            os.remove(db_path)
        except Exception:
            pass
        await m.reply("تم الغاء عملية الترحيل")
        return

    conn = _open_db(db_path)
    try:
        if choice == '7':
            lines = []
            for key in ('1', '2', '3', '4', '5', '6'):
                _, label, fn = ACTIONS[key]
                n = await fn(r, bot_id, conn)
                lines.append(f"• {label} ↤︎ {n}")
            await m.reply("تم ترحيل كل القائمة\n\n" + "\n".join(lines))
        else:
            _, label, fn = ACTIONS[choice]
            n = await fn(r, bot_id, conn)
            await m.reply(f"تم ترحيل {label} ↤︎ {n}")
    finally:
        conn.close()
