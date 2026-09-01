import html
from helpers.context import get_global_r, get_global_dev, get_global_k
r = get_global_r()
Dev_FINAL = get_global_dev()
k = get_global_k()
import re
import random
import time
import json
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
from .restrict import handle_warn_commands, handle_ban_commands, handle_general_commands, check_all_restrictions, handle_warn_buttons
from .owners import track_admin_action
from helpers.replies_store import (
    REPLIES,
    plugins_supervision_107,
    plugins_supervision_1087,
    plugins_supervision_1109,
    plugins_supervision_1111,
    plugins_supervision_1115,
    plugins_supervision_1121,
    plugins_supervision_1132,
    plugins_supervision_1134,
    plugins_supervision_1326,
    plugins_supervision_196,
    plugins_supervision_198,
    plugins_supervision_202,
    plugins_supervision_204,
    plugins_supervision_208,
    plugins_supervision_210,
    plugins_supervision_214,
    plugins_supervision_216,
    plugins_supervision_221,
    plugins_supervision_226,
    plugins_supervision_231,
    plugins_supervision_236,
    plugins_supervision_245,
    plugins_supervision_271,
    plugins_supervision_282,
    plugins_supervision_285,
    plugins_supervision_287,
    plugins_supervision_289,
    plugins_supervision_295,
    plugins_supervision_303,
    plugins_supervision_313,
    plugins_supervision_319,
    plugins_supervision_331,
    plugins_supervision_334,
    plugins_supervision_336,
    plugins_supervision_338,
    plugins_supervision_349,
    plugins_supervision_353,
    plugins_supervision_359,
    plugins_supervision_362,
    plugins_supervision_364,
    plugins_supervision_375,
    plugins_supervision_381,
    plugins_supervision_390,
    plugins_supervision_392,
    plugins_supervision_401,
    plugins_supervision_407,
    plugins_supervision_411,
    plugins_supervision_420,
    plugins_supervision_424,
    plugins_supervision_437,
    plugins_supervision_443,
    plugins_supervision_447,
    plugins_supervision_459,
    plugins_supervision_465,
    plugins_supervision_474,
    plugins_supervision_476,
    plugins_supervision_485,
    plugins_supervision_489,
    plugins_supervision_494,
    plugins_supervision_503,
    plugins_supervision_505,
    plugins_supervision_509,
    plugins_supervision_521,
    plugins_supervision_524,
    plugins_supervision_526,
    plugins_supervision_528,
    plugins_supervision_552,
    plugins_supervision_556,
    plugins_supervision_563,
    plugins_supervision_566,
    plugins_supervision_568,
    plugins_supervision_592,
    plugins_supervision_596,
    plugins_supervision_605,
    plugins_supervision_607,
    plugins_supervision_629,
    plugins_supervision_633,
    plugins_supervision_637,
    plugins_supervision_659,
    plugins_supervision_663,
    plugins_supervision_676,
    plugins_supervision_682,
    plugins_supervision_686,
    plugins_supervision_714,
    plugins_supervision_720,
    plugins_supervision_774,
    plugins_supervision_776,
    plugins_supervision_778,
    plugins_supervision_782,
    plugins_supervision_832,
    plugins_supervision_834,
    plugins_supervision_836,
    plugins_supervision_840,
    plugins_supervision_867,
    plugins_supervision_873,
    plugins_supervision_898,
    plugins_supervision_900,
    plugins_supervision_904,
    plugins_supervision_933,
    plugins_supervision_935,
    plugins_supervision_939,
    plugins_supervision_976,
    plugins_supervision_993,
    plugins_supervision_996,
)

async def show_user_restrictions(c, m, target_user, k):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    
    target_id = target_user.id
    target_mention = target_user.first_name
    target_username = f"@{target_user.username}" if target_user.username else "لا يوجد يوزر"
    
    is_muted = await r.sismember(f"{m.chat.id}:listMUTE:{Dev_FINAL}", target_id)
    is_restricted = await r.sismember(f"{m.chat.id}:listRESTRICTED:{Dev_FINAL}", target_id)
    ban_admin_id = await r.get(f"{target_id}:ban_admin:{m.chat.id}{Dev_FINAL}")
    
    try:
        member = await m.chat.get_member(target_id)
        status = member.status
    except:
        status = None

    has_restrictions = False
    res_text = f"↢ برنت لجميع قيود ↤ {target_mention}\n↢ يوزره ↤ {target_username}\n↢ ايديه ↤ {target_id}\n\n"
    
    if is_muted:
        has_restrictions = True
        admin_id = await r.get(f"{target_id}:mute_admin:{m.chat.id}{Dev_FINAL}")
        msg_id = await r.get(f"{target_id}:mute_msg:{m.chat.id}{Dev_FINAL}")
        date_str = await r.get(f"{target_id}:mute_date:{m.chat.id}{Dev_FINAL}") or "2026/06/21"
        time_str = await r.get(f"{target_id}:mute_time:{m.chat.id}{Dev_FINAL}") or "05:34PM"
        
        if admin_id:
            try:
                admin_user = await c.get_users(int(admin_id))
                admin_mention = f'<a href="tg://user?id={admin_id}">{html.escape(str(admin_user.first_name))}</a>'
            except:
                admin_mention = f'<a href="tg://user?id={admin_id}">{html.escape(str(admin_id))}</a>'
        else:
            admin_mention = "البوت"
            
        msg_link = f'<a href="https://t.me/c/{str(m.chat.id).replace("-100", "")}/{msg_id}">{msg_id}</a>' if msg_id else "لا يوجد"
        res_text += f"↢ : الكتم\n↢ من ↤ {admin_mention}\n↢ التاريخ ↤ {date_str}\n↢ الساعة ↤ {time_str}\n↢ الرسالة ↤ {msg_link}\n\n"
        
    if is_restricted or status == ChatMemberStatus.RESTRICTED:
        has_restrictions = True
        admin_id = await r.get(f"{target_id}:restrict_admin:{m.chat.id}{Dev_FINAL}")
        msg_id = await r.get(f"{target_id}:restrict_msg:{m.chat.id}{Dev_FINAL}")
        date_str = await r.get(f"{target_id}:restrict_date:{m.chat.id}{Dev_FINAL}") or "2026/06/21"
        time_str = await r.get(f"{target_id}:restrict_time:{m.chat.id}{Dev_FINAL}") or "05:34PM"
        
        if admin_id:
            try:
                admin_user = await c.get_users(int(admin_id))
                admin_mention = f'<a href="tg://user?id={admin_id}">{html.escape(str(admin_user.first_name))}</a>'
            except:
                admin_mention = f'<a href="tg://user?id={admin_id}">{html.escape(str(admin_id))}</a>'
        else:
            admin_mention = "البوت"
            
        msg_link = f'<a href="https://t.me/c/{str(m.chat.id).replace("-100", "")}/{msg_id}">{msg_id}</a>' if msg_id else "لا يوجد"
        res_text += f"↢ : التقييد\n↢ من ↤ {admin_mention}\n↢ التاريخ ↤ {date_str}\n↢ الساعة ↤ {time_str}\n↢ الرسالة ↤ {msg_link}\n\n"
        
    if status == ChatMemberStatus.BANNED or ban_admin_id:
        has_restrictions = True
        msg_id = await r.get(f"{target_id}:ban_msg:{m.chat.id}{Dev_FINAL}")
        reason = await r.get(f"{target_id}:ban_reason:{m.chat.id}{Dev_FINAL}") or "لا يوجد سبب"
        date_str = await r.get(f"{target_id}:ban_date:{m.chat.id}{Dev_FINAL}") or "2026/06/21"
        time_str = await r.get(f"{target_id}:ban_time:{m.chat.id}{Dev_FINAL}") or "05:34PM"
        
        if ban_admin_id:
            try:
                admin_user = await c.get_users(int(ban_admin_id))
                admin_mention = f'<a href="tg://user?id={ban_admin_id}">{html.escape(str(admin_user.first_name))}</a>'
            except:
                admin_mention = f'<a href="tg://user?id={ban_admin_id}">{html.escape(str(ban_admin_id))}</a>'
        else:
            admin_mention = "البوت"
            
        msg_link = f'<a href="https://t.me/c/{str(m.chat.id).replace("-100", "")}/{msg_id}">{msg_id}</a>' if msg_id else "لا يوجد"
        type_k = "الحظر" if status == ChatMemberStatus.BANNED else "الطرد"
        res_text += f"↢ : {type_k}\n↢ من ↤ {admin_mention}\n↢ السبب ↤ {reason}\n↢ التاريخ ↤ {date_str}\n↢ الساعة ↤ {time_str}\n↢ الرسالة ↤ {msg_link}\n\n"
        
    if not has_restrictions:
        return await m.reply(plugins_supervision_107(k))
    
    return await m.reply(res_text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)

async def is_anti_spam_kick_blocked(chat_id, user_id):
    """فحص للقراءة فقط (بدون تسجيل) يستخدم قبل تنفيذ امر حظر/طرد يدوي،
    للتأكد ان هذا المشرف لم يتجاوز الحد مسبقا. لا يقوم بأي تسجيل حتى لا يتم
    احتساب نفس العملية مرتين (مرة يدويا ومرة عبر سجل الادمنز/الاحداث)."""
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    if not await r.get(f"{chat_id}:AntiSpamKick:{Dev_FINAL}"):
        return False
    if await gowner_pls(user_id, chat_id):
        return False
    now = int(time.time())
    await r.zremrangebyscore(f"{chat_id}:KickCount:{user_id}", 0, now - 3600)
    kicks = await r.zcard(f"{chat_id}:KickCount:{user_id}")
    return kicks > 3

async def check_anti_spam_kick(c, chat_id, user_id, user_mention):
    """المصدر الوحيد لتسجيل عمليات الحظر/الطرد (يعتمد على سجل الادمنز الحقيقي
    عبر حدث on_chat_member_updated) لتفادي مشكلة الاعتماد على استعلامات مثل
    chat.get_members(filter=ChatMembersFilter.BANNED) التي قد تسبب ازدواجية
    او عدم دقة، ولضمان عدم احتساب نفس العملية مرتين."""
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if await r.get(f"{chat_id}:AntiSpamKick:{Dev_FINAL}"):
        if not await gowner_pls(user_id, chat_id):
            now = int(time.time())
            await r.zadd(f"{chat_id}:KickCount:{user_id}", {str(now): now})
            await r.zremrangebyscore(f"{chat_id}:KickCount:{user_id}", 0, now - 3600)
            kicks = await r.zcard(f"{chat_id}:KickCount:{user_id}")
            if kicks > 3:
                try:
                    await c.promote_chat_member(
                        chat_id,
                        user_id,
                        privileges=ChatPrivileges(
                            can_manage_chat=False,
                            can_delete_messages=False,
                            can_manage_video_chats=False,
                            can_restrict_members=False,
                            can_promote_members=False,
                            can_pin_messages=False,
                            can_change_info=False,
                            can_invite_users=False,
                            can_post_stories=False,
                            can_edit_stories=False,
                            can_delete_stories=False,
                            can_manage_topics=False,
                            can_manage_tags=False
                        )
                    )
                except:
                    pass
                await r.srem(f"{chat_id}:listOWNER:{Dev_FINAL}", user_id)
                await r.srem(f"{chat_id}:listMOD:{Dev_FINAL}", user_id)
                await r.srem(f"{chat_id}:listADMIN:{Dev_FINAL}", user_id)
                await r.sadd(f"{chat_id}:listPRE:{Dev_FINAL}", user_id)
                await r.delete(f"{chat_id}:KickCount:{user_id}")
                await c.send_message(
                    chat_id, 
                    f"{k}  المشرف 「 {user_mention} 」 \n {k}  تجاوز حد الحظر/الطرد المسموح به\n {k}  تم تنزيله من الإشراف واصبح مميز فقط"
                )
                return True
    return False

@Client.on_chat_member_updated()
async def watch_manual_kicks(c, cb: ChatMemberUpdated):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if not cb.new_chat_member or not cb.old_chat_member:
        return
    if cb.new_chat_member.status in [ChatMemberStatus.BANNED, ChatMemberStatus.LEFT]:
        if cb.old_chat_member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER, ChatMemberStatus.RESTRICTED]:
            actor = cb.from_user
            if actor and not actor.is_bot:
                await check_anti_spam_kick(c, cb.chat.id, actor.id, actor.mention())

async def handle_moderation_commands(c, m, k, text):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if not await check_global_restrictions(c, m, k):
        return    
    if text == "تعطيل اشراف المطورين":
        if not await devp_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_supervision_196(k))
        await r.set(f"DevAdminStatus:{Dev_FINAL}", "disabled")
        return await m.reply(plugins_supervision_198(k))

    if text == "تفعيل اشراف المطورين":
        if not await devp_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_supervision_202(k))
        await r.delete(f"DevAdminStatus:{Dev_FINAL}")
        return await m.reply(plugins_supervision_204(k))

    if text == "تعطيل رفع المشرفين":
        if not await gowner_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_supervision_208(k))
        await r.set(f"{m.chat.id}:LockPromote:{Dev_FINAL}", "disabled")
        return await m.reply(plugins_supervision_210(k))

    if text == "تفعيل رفع المشرفين":
        if not await gowner_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_supervision_214(k))
        await r.delete(f"{m.chat.id}:LockPromote:{Dev_FINAL}")
        return await m.reply(plugins_supervision_216(k))

    if text in ["قفل الخيانه", "تفعيل حمايه الاعضاء"]:
        if await owner_pls(m.from_user.id, m.chat.id):
            await r.set(f"{m.chat.id}:AntiSpamKick:{Dev_FINAL}", "on")
            return await m.reply(plugins_supervision_221(k))

    if text in ["فتح الخيانه", "تعطيل حمايه الاعضاء"]:
        if await owner_pls(m.from_user.id, m.chat.id):
            await r.delete(f"{m.chat.id}:AntiSpamKick:{Dev_FINAL}")
            return await m.reply(plugins_supervision_226(k))

    if text == "تفعيل اسباب المشرفين":
        if await gowner_pls(m.from_user.id, m.chat.id):
            await r.set(f"{m.chat.id}:BanReasonStatus:{Dev_FINAL}", "on")
            return await m.reply(plugins_supervision_231(k, k))

    if text == "تعطيل اسباب المشرفين":
        if await gowner_pls(m.from_user.id, m.chat.id):
            await r.delete(f"{m.chat.id}:BanReasonStatus:{Dev_FINAL}")
            return await m.reply(plugins_supervision_236(k))

    if text.startswith("حظر") or text.startswith("طرد"):
        if text.startswith("حظر عام"):
            return
        
        parts = text.split()
        cmd = parts[0]
        if not (await admin_pls(m.from_user.id, m.chat.id) or await fake_rank_pls(m.from_user.id, m.chat.id, 'ban')):
            return await m.reply(plugins_supervision_245(k))
        target_user = None
        reason = None
        is_reply = False
        if len(parts) > 1:
            first_param = parts[1]
            if first_param.startswith("@") or first_param.isdigit() or (first_param.startswith("-") and first_param[1:].isdigit()):
                target_user = first_param.replace("@", "")
                if len(parts) > 2:
                    reason = text.split(None, 2)[2]
            else:
                if m.reply_to_message:
                    is_reply = True
                    reason = text.split(None, 1)[1]
        else:
            if m.reply_to_message:
                is_reply = True
        if is_reply:
            if m.reply_to_message.from_user:
                target_user = m.reply_to_message.from_user.id
            else:
                return
        if not target_user:
            return
        reasons_enabled = await r.get(f"{m.chat.id}:BanReasonStatus:{Dev_FINAL}")
        if reasons_enabled and not reason:
            return await m.reply(plugins_supervision_271(k, k))
        if not reason:
            reason = "لا يوجد سبب"
        try:
            if isinstance(target_user, str):
                target_user = await resolve_user_id_from_arg(target_user)
            get = await m.chat.get_member(target_user)
            if m.from_user.id == get.user.id:
                return await m.reply(REPLIES['plugins_supervision_279'])
            if await admin_pls(get.user.id, m.chat.id):
                rank = await get_rank(get.user.id, m.chat.id)
                return await m.reply(plugins_supervision_282(k, rank))
            if await fake_rank_protected(get.user.id, m.chat.id) and not await gowner_pls(m.from_user.id, m.chat.id):
                rank = await get_rank(get.user.id, m.chat.id)
                return await m.reply(plugins_supervision_285(k, rank))
        except:
            return await m.reply(plugins_supervision_287(k))
        if await is_anti_spam_kick_blocked(m.chat.id, m.from_user.id):
            return await m.reply(plugins_supervision_289(k))
        now = datetime.now()
        date_str = now.strftime("%Y/%m/%d")
        time_str = now.strftime("%I:%M%p")
        if cmd == "حظر":
            if get.status == ChatMemberStatus.BANNED:
                return await m.reply(plugins_supervision_295(get.user.mention(), k))
            await m.chat.ban_member(get.user.id)
            await r.set(f"{get.user.id}:ban_admin:{m.chat.id}{Dev_FINAL}", m.from_user.id)
            await r.set(f"{get.user.id}:ban_msg:{m.chat.id}{Dev_FINAL}", m.id)
            await r.set(f"{get.user.id}:ban_reason:{m.chat.id}{Dev_FINAL}", reason)
            await r.set(f"{get.user.id}:ban_date:{m.chat.id}{Dev_FINAL}", date_str)
            await r.set(f"{get.user.id}:ban_time:{m.chat.id}{Dev_FINAL}", time_str)
            await track_admin_action(m.chat.id, m.from_user.id, "ban")
            return await m.reply(plugins_supervision_303(get.user.mention(), reason))
        elif cmd == "طرد":
            await m.chat.ban_member(get.user.id)
            await m.chat.unban_member(get.user.id)
            await r.set(f"{get.user.id}:ban_admin:{m.chat.id}{Dev_FINAL}", m.from_user.id)
            await r.set(f"{get.user.id}:ban_msg:{m.chat.id}{Dev_FINAL}", m.id)
            await r.set(f"{get.user.id}:ban_reason:{m.chat.id}{Dev_FINAL}", reason)
            await r.set(f"{get.user.id}:ban_date:{m.chat.id}{Dev_FINAL}", date_str)
            await r.set(f"{get.user.id}:ban_time:{m.chat.id}{Dev_FINAL}", time_str)
            await track_admin_action(m.chat.id, m.from_user.id, "kick")
            return await m.reply(plugins_supervision_313(get.user.mention(), reason))

    if text.startswith("كتم ") and len(text.split()) == 2:
        if text.startswith("كتم عام"):
            return        
        if not (await admin_pls(m.from_user.id, m.chat.id) or await fake_rank_pls(m.from_user.id, m.chat.id, 'mute')):
            return await m.reply(plugins_supervision_319(k))
        else:
            user = await resolve_user_id_from_arg(text.split()[1])
            try:
                get = await m.chat.get_member(user)
                if m.from_user.id == get.user.id:
                    return await m.reply(REPLIES['plugins_supervision_559'])
                if await admin_pls(get.user.id, m.chat.id):
                    rank = await get_rank(get.user.id, m.chat.id)
                    return await m.reply(plugins_supervision_331(k, rank))
                if await fake_rank_protected(get.user.id, m.chat.id) and not await gowner_pls(m.from_user.id, m.chat.id):
                    rank = await get_rank(get.user.id, m.chat.id)
                    return await m.reply(plugins_supervision_334(k, rank))
                if await r.sismember(f"{m.chat.id}:listMUTE:{Dev_FINAL}", get.user.id):
                    return await m.reply(plugins_supervision_336(get.user.mention(), k))
            except:
                return await m.reply(plugins_supervision_338(k))
            now = datetime.now()
            date_str = now.strftime("%Y/%m/%d")
            time_str = now.strftime("%I:%M%p")
            await r.set(f"{get.user.id}:mute:{m.chat.id}{Dev_FINAL}", 1)
            await r.sadd(f"{m.chat.id}:listMUTE:{Dev_FINAL}", get.user.id)
            await r.set(f"{get.user.id}:mute_admin:{m.chat.id}{Dev_FINAL}", m.from_user.id)
            await r.set(f"{get.user.id}:mute_msg:{m.chat.id}{Dev_FINAL}", m.id)
            await r.set(f"{get.user.id}:mute_date:{m.chat.id}{Dev_FINAL}", date_str)
            await r.set(f"{get.user.id}:mute_time:{m.chat.id}{Dev_FINAL}", time_str)
            await track_admin_action(m.chat.id, m.from_user.id, "mute")
            return await m.reply(plugins_supervision_349(get.user.mention(), k))

    if text == "كتم" and m.reply_to_message and m.reply_to_message.from_user:
        if not (await admin_pls(m.from_user.id, m.chat.id) or await fake_rank_pls(m.from_user.id, m.chat.id, 'mute')):
            return await m.reply(plugins_supervision_353(k))
        else:
            if m.from_user.id == m.reply_to_message.from_user.id:
                return await m.reply(REPLIES['plugins_supervision_356'])
            if await admin_pls(m.reply_to_message.from_user.id, m.chat.id):
                rank = await get_rank(m.reply_to_message.from_user.id, m.chat.id)
                return await m.reply(plugins_supervision_359(k, rank))
            if await fake_rank_protected(m.reply_to_message.from_user.id, m.chat.id) and not await gowner_pls(m.from_user.id, m.chat.id):
                rank = await get_rank(m.reply_to_message.from_user.id, m.chat.id)
                return await m.reply(plugins_supervision_362(k, rank))
            if await r.sismember(f"{m.chat.id}:listMUTE:{Dev_FINAL}", m.reply_to_message.from_user.id):
                return await m.reply(plugins_supervision_364(m.reply_to_message.from_user.mention(), k))
            now = datetime.now()
            date_str = now.strftime("%Y/%m/%d")
            time_str = now.strftime("%I:%M%p")
            await r.set(f"{m.reply_to_message.from_user.id}:mute:{m.chat.id}{Dev_FINAL}", 1)
            await r.sadd(f"{m.chat.id}:listMUTE:{Dev_FINAL}", m.reply_to_message.from_user.id)
            await r.set(f"{m.reply_to_message.from_user.id}:mute_admin:{m.chat.id}{Dev_FINAL}", m.from_user.id)
            await r.set(f"{m.reply_to_message.from_user.id}:mute_msg:{m.chat.id}{Dev_FINAL}", m.id)
            await r.set(f"{m.reply_to_message.from_user.id}:mute_date:{m.chat.id}{Dev_FINAL}", date_str)
            await r.set(f"{m.reply_to_message.from_user.id}:mute_time:{m.chat.id}{Dev_FINAL}", time_str)
            await track_admin_action(m.chat.id, m.from_user.id, "mute")
            return await m.reply(plugins_supervision_375(m.reply_to_message.from_user.mention(), k))

    if text.startswith("الغاء الكتم ") and len(text.split()) == 3:
        if text.startswith("الغاء الكتم عام"):
            return            
        if not (await admin_pls(m.from_user.id, m.chat.id) or await fake_rank_pls(m.from_user.id, m.chat.id, 'mute')):
            return await m.reply(plugins_supervision_381(k))
        else:
            user = await resolve_user_id_from_arg(text.split()[2])
            try:
                get = await m.chat.get_member(user)
            except:
                return await m.reply(plugins_supervision_390(k))
            if not await r.sismember(f"{m.chat.id}:listMUTE:{Dev_FINAL}", get.user.id):
                return await m.reply(plugins_supervision_392(get.user.mention(), k))
            await r.delete(f"{get.user.id}:mute:{m.chat.id}{Dev_FINAL}")
            await r.srem(f"{m.chat.id}:listMUTE:{Dev_FINAL}", get.user.id)
            await r.delete(
                f"{get.user.id}:mute_admin:{m.chat.id}{Dev_FINAL}",
                f"{get.user.id}:mute_msg:{m.chat.id}{Dev_FINAL}",
                f"{get.user.id}:mute_date:{m.chat.id}{Dev_FINAL}",
                f"{get.user.id}:mute_time:{m.chat.id}{Dev_FINAL}"
            )
            return await m.reply(plugins_supervision_401(get.user.mention(), k))

    if text == "الغاء الكتم" and m.reply_to_message and m.reply_to_message.from_user:
        if text.startswith("الغاء الكتم عام"):
            return            
        if not (await admin_pls(m.from_user.id, m.chat.id) or await fake_rank_pls(m.from_user.id, m.chat.id, 'mute')):
            return await m.reply(plugins_supervision_407(k))
        else:
            get = await m.chat.get_member(m.reply_to_message.from_user.id)
            if not await r.sismember(f"{m.chat.id}:listMUTE:{Dev_FINAL}", get.user.id):
                return await m.reply(plugins_supervision_411(m.reply_to_message.from_user.mention(), k))
            await r.delete(f"{get.user.id}:mute:{m.chat.id}{Dev_FINAL}")
            await r.srem(f"{m.chat.id}:listMUTE:{Dev_FINAL}", get.user.id)
            await r.delete(
                f"{get.user.id}:mute_admin:{m.chat.id}{Dev_FINAL}",
                f"{get.user.id}:mute_msg:{m.chat.id}{Dev_FINAL}",
                f"{get.user.id}:mute_date:{m.chat.id}{Dev_FINAL}",
                f"{get.user.id}:mute_time:{m.chat.id}{Dev_FINAL}"
            )
            return await m.reply(plugins_supervision_420(m.reply_to_message.from_user.mention(), k))

    if text == "المكتومين":
        if not await admin_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_supervision_424(k))
        else:
            count = 1
            text_result = "المكتومين:\n\n"
            for user in await r.smembers(f"{m.chat.id}:listMUTE:{Dev_FINAL}"):
                try:
                    user_obj = (await c.get_chat_member(m.chat.id, int(user))).user
                    user_mention = f"@{user_obj.username}" if user_obj.username else user_obj.mention()
                    text_result += f"{count} - {user_mention}\n"
                    count += 1
                except:
                    pass
            if count == 1:
                return await m.reply(plugins_supervision_437(k))
            else:
                return await m.reply(text_result)

    if text == "مسح المكتومين":
        if not await admin_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_supervision_443(k))
        else:
            muted_users = await r.smembers(f"{m.chat.id}:listMUTE:{Dev_FINAL}")
            if not muted_users:
                return await m.reply(plugins_supervision_447(k))
            co = 0
            for user_id in muted_users:
                co += 1
                await r.delete(f"{user_id}:mute:{m.chat.id}{Dev_FINAL}")
                await r.srem(f"{m.chat.id}:listMUTE:{Dev_FINAL}", user_id)
                await r.delete(
                    f"{user_id}:mute_admin:{m.chat.id}{Dev_FINAL}",
                    f"{user_id}:mute_msg:{m.chat.id}{Dev_FINAL}",
                    f"{user_id}:mute_date:{m.chat.id}{Dev_FINAL}",
                    f"{user_id}:mute_time:{m.chat.id}{Dev_FINAL}"
                )
            return await m.reply(plugins_supervision_459(k, co))

    if text.startswith("رفع الحظر ") or text.startswith("الغاء الحظر ") and len(text.split()) == 3:
        if not "@" in text and not re.findall("[0-9]+", text):
            return
        if not (await admin_pls(m.from_user.id, m.chat.id) or await fake_rank_pls(m.from_user.id, m.chat.id, 'ban')):
            return await m.reply(plugins_supervision_465(k))
        else:
            user = await resolve_user_id_from_arg(text.split()[2])
            try:
                get = await m.chat.get_member(user)
                if not get.status == ChatMemberStatus.BANNED:
                    return await m.reply(plugins_supervision_474(get.user.mention(), k))
            except:
                return await m.reply(plugins_supervision_476(k))
            await m.chat.unban_member(get.user.id)
            await r.delete(
                f"{get.user.id}:ban_admin:{m.chat.id}{Dev_FINAL}",
                f"{get.user.id}:ban_msg:{m.chat.id}{Dev_FINAL}",
                f"{get.user.id}:ban_reason:{m.chat.id}{Dev_FINAL}",
                f"{get.user.id}:ban_date:{m.chat.id}{Dev_FINAL}",
                f"{get.user.id}:ban_time:{m.chat.id}{Dev_FINAL}"
            )
            return await m.reply(plugins_supervision_485(get.user.mention(), k))

    if text == "رفع الحظر" or text == "الغاء الحظر" and m.reply_to_message and m.reply_to_message.from_user:
        if not (await admin_pls(m.from_user.id, m.chat.id) or await fake_rank_pls(m.from_user.id, m.chat.id, 'ban')):
            return await m.reply(plugins_supervision_489(k))
        else:
            try:
                get = await m.chat.get_member(m.reply_to_message.from_user.id)
                if not get.status == ChatMemberStatus.BANNED:
                    return await m.reply(plugins_supervision_494(m.reply_to_message.from_user.mention(), k))
                await m.chat.unban_member(m.reply_to_message.from_user.id)
                await r.delete(
                    f"{get.user.id}:ban_admin:{m.chat.id}{Dev_FINAL}",
                    f"{get.user.id}:ban_msg:{m.chat.id}{Dev_FINAL}",
                    f"{get.user.id}:ban_reason:{m.chat.id}{Dev_FINAL}",
                    f"{get.user.id}:ban_date:{m.chat.id}{Dev_FINAL}",
                    f"{get.user.id}:ban_time:{m.chat.id}{Dev_FINAL}"
                )
                return await m.reply(plugins_supervision_503(m.reply_to_message.from_user.mention(), k))
            except:
                return await m.reply(plugins_supervision_505(k))

    if text.startswith("تقييد ") and len(text.split()) == 2:
        if not (await admin_pls(m.from_user.id, m.chat.id) or await fake_rank_pls(m.from_user.id, m.chat.id, 'restrict')):
            return await m.reply(plugins_supervision_509(k))
        else:
            user = await resolve_user_id_from_arg(text.split()[1])
            try:
                get = await m.chat.get_member(user)
                if m.from_user.id == get.user.id:
                    return await m.reply(REPLIES['plugins_supervision_559'])
                if await admin_pls(get.user.id, m.chat.id):
                    rank = await get_rank(get.user.id, m.chat.id)
                    return await m.reply(plugins_supervision_521(k, rank))
                if await fake_rank_protected(get.user.id, m.chat.id) and not await gowner_pls(m.from_user.id, m.chat.id):
                    rank = await get_rank(get.user.id, m.chat.id)
                    return await m.reply(plugins_supervision_524(k, rank))
                if await r.sismember(f"{m.chat.id}:listRESTRICTED:{Dev_FINAL}", get.user.id):
                    return await m.reply(plugins_supervision_526(get.user.mention(), k))
            except:
                return await m.reply(plugins_supervision_528(k))
            now = datetime.now()
            date_str = now.strftime("%Y/%m/%d")
            time_str = now.strftime("%I:%M%p")
            await c.restrict_chat_member(
                m.chat.id,
                get.user.id,
                ChatPermissions(
                    can_send_messages=False,
                    can_send_media_messages=False,
                    can_send_other_messages=False,
                    can_send_polls=False,
                    can_add_web_page_previews=False,
                    can_invite_users=False,
                    can_change_info=False,
                    can_pin_messages=False
                )
            )
            await r.sadd(f"{m.chat.id}:listRESTRICTED:{Dev_FINAL}", get.user.id)
            await r.set(f"{get.user.id}:restrict_admin:{m.chat.id}{Dev_FINAL}", m.from_user.id)
            await r.set(f"{get.user.id}:restrict_msg:{m.chat.id}{Dev_FINAL}", m.id)
            await r.set(f"{get.user.id}:restrict_date:{m.chat.id}{Dev_FINAL}", date_str)
            await r.set(f"{get.user.id}:restrict_time:{m.chat.id}{Dev_FINAL}", time_str)
            await track_admin_action(m.chat.id, m.from_user.id, "restrict")
            return await m.reply(plugins_supervision_552(get.user.mention(), k))

    if text == "تقييد" and m.reply_to_message and m.reply_to_message.from_user:
        if not (await admin_pls(m.from_user.id, m.chat.id) or await fake_rank_pls(m.from_user.id, m.chat.id, 'restrict')):
            return await m.reply(plugins_supervision_556(k))
        else:
            if m.from_user.id == m.reply_to_message.from_user.id:
                return await m.reply(REPLIES['plugins_supervision_559'])
            get = await m.chat.get_member(m.reply_to_message.from_user.id)
            if await admin_pls(m.reply_to_message.from_user.id, m.chat.id):
                rank = await get_rank(m.reply_to_message.from_user.id, m.chat.id)
                return await m.reply(plugins_supervision_563(k, rank))
            if await fake_rank_protected(m.reply_to_message.from_user.id, m.chat.id) and not await gowner_pls(m.from_user.id, m.chat.id):
                rank = await get_rank(m.reply_to_message.from_user.id, m.chat.id)
                return await m.reply(plugins_supervision_566(k, rank))
            if await r.sismember(f"{m.chat.id}:listRESTRICTED:{Dev_FINAL}", m.reply_to_message.from_user.id):
                return await m.reply(plugins_supervision_568(m.reply_to_message.from_user.mention(), k))
            now = datetime.now()
            date_str = now.strftime("%Y/%m/%d")
            time_str = now.strftime("%I:%M%p")
            await c.restrict_chat_member(
                m.chat.id,
                m.reply_to_message.from_user.id,
                ChatPermissions(
                    can_send_messages=False,
                    can_send_media_messages=False,
                    can_send_other_messages=False,
                    can_send_polls=False,
                    can_add_web_page_previews=False,
                    can_invite_users=False,
                    can_change_info=False,
                    can_pin_messages=False
                )
            )
            await r.sadd(f"{m.chat.id}:listRESTRICTED:{Dev_FINAL}", m.reply_to_message.from_user.id)
            await r.set(f"{m.reply_to_message.from_user.id}:restrict_admin:{m.chat.id}{Dev_FINAL}", m.from_user.id)
            await r.set(f"{m.reply_to_message.from_user.id}:restrict_msg:{m.chat.id}{Dev_FINAL}", m.id)
            await r.set(f"{m.reply_to_message.from_user.id}:restrict_date:{m.chat.id}{Dev_FINAL}", date_str)
            await r.set(f"{m.reply_to_message.from_user.id}:restrict_time:{m.chat.id}{Dev_FINAL}", time_str)
            await track_admin_action(m.chat.id, m.from_user.id, "restrict")
            return await m.reply(plugins_supervision_592(m.reply_to_message.from_user.mention(), k))

    if text.startswith("الغاء تقييد ") or text.startswith("الغاء التقييد ") and len(text.split()) == 3:
        if not (await admin_pls(m.from_user.id, m.chat.id) or await fake_rank_pls(m.from_user.id, m.chat.id, 'restrict')):
            return await m.reply(plugins_supervision_596(k))
        else:
            user = await resolve_user_id_from_arg(text.split()[2])
            try:
                get = await m.chat.get_member(user)
                if not get.status == ChatMemberStatus.RESTRICTED:
                    return await m.reply(plugins_supervision_605(get.user.mention(), k))
            except:
                return await m.reply(plugins_supervision_607(k))
            await c.restrict_chat_member(
                m.chat.id,
                get.user.id,
                ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_other_messages=True,
                    can_send_polls=True,
                    can_invite_users=True,
                    can_add_web_page_previews=True,
                    can_change_info=True,
                    can_pin_messages=True,
                ),
            )
            await r.srem(f"{m.chat.id}:listRESTRICTED:{Dev_FINAL}", get.user.id)
            await r.delete(
                f"{get.user.id}:restrict_admin:{m.chat.id}{Dev_FINAL}",
                f"{get.user.id}:restrict_msg:{m.chat.id}{Dev_FINAL}",
                f"{get.user.id}:restrict_date:{m.chat.id}{Dev_FINAL}",
                f"{get.user.id}:restrict_time:{m.chat.id}{Dev_FINAL}"
            )
            return await m.reply(plugins_supervision_629(get.user.mention(), k))

    if text == "الغاء تقييد" or text == "الغاء التقييد" and m.reply_to_message and m.reply_to_message.from_user:
        if not (await admin_pls(m.from_user.id, m.chat.id) or await fake_rank_pls(m.from_user.id, m.chat.id, 'restrict')):
            return await m.reply(plugins_supervision_633(k))
        else:
            get = await m.chat.get_member(m.reply_to_message.from_user.id)
            if not get.status == ChatMemberStatus.RESTRICTED:
                return await m.reply(plugins_supervision_637(m.reply_to_message.from_user.mention(), k))
            await c.restrict_chat_member(
                m.chat.id,
                m.reply_to_message.from_user.id,
                ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_other_messages=True,
                    can_send_polls=True,
                    can_invite_users=True,
                    can_add_web_page_previews=True,
                    can_change_info=True,
                    can_pin_messages=True,
                ),
            )
            await r.srem(f"{m.chat.id}:listRESTRICTED:{Dev_FINAL}", m.reply_to_message.from_user.id)
            await r.delete(
                f"{get.user.id}:restrict_admin:{m.chat.id}{Dev_FINAL}",
                f"{get.user.id}:restrict_msg:{m.chat.id}{Dev_FINAL}",
                f"{get.user.id}:restrict_date:{m.chat.id}{Dev_FINAL}",
                f"{get.user.id}:restrict_time:{m.chat.id}{Dev_FINAL}"
            )
            return await m.reply(plugins_supervision_659(m.reply_to_message.from_user.mention(), k))

    if text == "المقيدين":
        if not await admin_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_supervision_663(k))
        else:
            count = 1
            text_result = "المقيدين:\n\n"
            for user_id in await r.smembers(f"{m.chat.id}:listRESTRICTED:{Dev_FINAL}"):
                try:
                    user_obj = (await c.get_chat_member(m.chat.id, int(user_id))).user
                    user_mention = f"@{user_obj.username}" if user_obj.username else user_obj.mention()
                    text_result += f"{count} - {user_mention}\n"
                    count += 1
                except:
                    pass
            if count == 1:
                return await m.reply(plugins_supervision_676(k))
            else:
                return await m.reply(text_result)

    if text == "مسح المقيدين":
        if not await admin_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_supervision_682(k))
        else:
            restricted_users = await r.smembers(f"{m.chat.id}:listRESTRICTED:{Dev_FINAL}")
            if not restricted_users:
                return await m.reply(plugins_supervision_686(k))
            co = 0
            for user_id in restricted_users:
                co += 1
                try:
                    await c.restrict_chat_member(
                        m.chat.id,
                        int(user_id),
                        ChatPermissions(
                            can_send_messages=True,
                            can_send_media_messages=True,
                            can_send_other_messages=True,
                            can_send_polls=True,
                            can_invite_users=True,
                            can_add_web_page_previews=True,
                            can_change_info=True,
                            can_pin_messages=True,
                        ),
                    )
                except:
                    pass
                await r.srem(f"{m.chat.id}:listRESTRICTED:{Dev_FINAL}", user_id)
                await r.delete(
                    f"{user_id}:restrict_admin:{m.chat.id}{Dev_FINAL}",
                    f"{user_id}:restrict_msg:{m.chat.id}{Dev_FINAL}",
                    f"{user_id}:restrict_date:{m.chat.id}{Dev_FINAL}",
                    f"{user_id}:restrict_time:{m.chat.id}{Dev_FINAL}"
                )
            return await m.reply(plugins_supervision_714(k, co))

    if text.startswith("رفع القيود ") and len(text.split()) == 3:
        if not "@" in text and not re.findall("[0-9]+", text):
            return
        if not await admin_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_supervision_720(k))
        else:
            user = await resolve_user_id_from_arg(text.split()[2])
            co = 0
            text_result = ""
            try:
                get = await m.chat.get_member(user)
                if get.status == ChatMemberStatus.BANNED:
                    await m.chat.unban_member(get.user.id)
                    text_result += "حظر\n"
                    co += 1
                if get.status == ChatMemberStatus.RESTRICTED:
                    await c.restrict_chat_member(
                        m.chat.id,
                        get.user.id,
                        ChatPermissions(
                            can_send_messages=True,
                            can_send_media_messages=True,
                            can_send_other_messages=True,
                            can_send_polls=True,
                            can_invite_users=True,
                            can_add_web_page_previews=True,
                            can_change_info=True,
                            can_pin_messages=True,
                        ),
                    )
                    await r.srem(f"{m.chat.id}:listRESTRICTED:{Dev_FINAL}", get.user.id)
                    text_result += "تقييد\n"
                    co += 1
                if await r.sismember(f"{m.chat.id}:listMUTE:{Dev_FINAL}", get.user.id):
                    await r.delete(f"{get.user.id}:mute:{m.chat.id}{Dev_FINAL}")
                    await r.srem(f"{m.chat.id}:listMUTE:{Dev_FINAL}", get.user.id)
                    text_result += "كتم\n"
                    co += 1
                
                await r.delete(
                    f"{get.user.id}:ban_admin:{m.chat.id}{Dev_FINAL}",
                    f"{get.user.id}:ban_msg:{m.chat.id}{Dev_FINAL}",
                    f"{get.user.id}:ban_reason:{m.chat.id}{Dev_FINAL}",
                    f"{get.user.id}:ban_date:{m.chat.id}{Dev_FINAL}",
                    f"{get.user.id}:ban_time:{m.chat.id}{Dev_FINAL}",
                    f"{get.user.id}:mute_admin:{m.chat.id}{Dev_FINAL}",
                    f"{get.user.id}:mute_msg:{m.chat.id}{Dev_FINAL}",
                    f"{get.user.id}:mute_date:{m.chat.id}{Dev_FINAL}",
                    f"{get.user.id}:mute_time:{m.chat.id}{Dev_FINAL}",
                    f"{get.user.id}:restrict_admin:{m.chat.id}{Dev_FINAL}",
                    f"{get.user.id}:restrict_msg:{m.chat.id}{Dev_FINAL}",
                    f"{get.user.id}:restrict_date:{m.chat.id}{Dev_FINAL}",
                    f"{get.user.id}:restrict_time:{m.chat.id}{Dev_FINAL}"
                )
                if co > 0:
                    return await m.reply(plugins_supervision_774(text_result))
                else:
                    return await m.reply(plugins_supervision_776(get.user.mention(), k))
            except:
                return await m.reply(plugins_supervision_778(k))

    if text == "رفع القيود" and m.reply_to_message and m.reply_to_message.from_user:
        if not await admin_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_supervision_782(k))
        else:
            try:
                text_result = ""
                co = 0
                get = await m.chat.get_member(m.reply_to_message.from_user.id)
                if get.status == ChatMemberStatus.BANNED:
                    await m.chat.unban_member(get.user.id)
                    text_result += "حظر\n"
                    co += 1
                if get.status == ChatMemberStatus.RESTRICTED:
                    await c.restrict_chat_member(
                        m.chat.id,
                        get.user.id,
                        ChatPermissions(
                            can_send_messages=True,
                            can_send_media_messages=True,
                            can_send_other_messages=True,
                            can_send_polls=True,
                            can_invite_users=True,
                            can_add_web_page_previews=True,
                            can_change_info=True,
                            can_pin_messages=True,
                        ),
                    )
                    await r.srem(f"{m.chat.id}:listRESTRICTED:{Dev_FINAL}", get.user.id)
                    text_result += "تقييد\n"
                    co += 1
                if await r.sismember(f"{m.chat.id}:listMUTE:{Dev_FINAL}", get.user.id):
                    await r.delete(f"{get.user.id}:mute:{m.chat.id}{Dev_FINAL}")
                    await r.srem(f"{m.chat.id}:listMUTE:{Dev_FINAL}", get.user.id)
                    text_result += "كتم\n"
                    co += 1
                
                await r.delete(
                    f"{get.user.id}:ban_admin:{m.chat.id}{Dev_FINAL}",
                    f"{get.user.id}:ban_msg:{m.chat.id}{Dev_FINAL}",
                    f"{get.user.id}:ban_reason:{m.chat.id}{Dev_FINAL}",
                    f"{get.user.id}:ban_date:{m.chat.id}{Dev_FINAL}",
                    f"{get.user.id}:ban_time:{m.chat.id}{Dev_FINAL}",
                    f"{get.user.id}:mute_admin:{m.chat.id}{Dev_FINAL}",
                    f"{get.user.id}:mute_msg:{m.chat.id}{Dev_FINAL}",
                    f"{get.user.id}:mute_date:{m.chat.id}{Dev_FINAL}",
                    f"{get.user.id}:mute_time:{m.chat.id}{Dev_FINAL}",
                    f"{get.user.id}:restrict_admin:{m.chat.id}{Dev_FINAL}",
                    f"{get.user.id}:restrict_msg:{m.chat.id}{Dev_FINAL}",
                    f"{get.user.id}:restrict_date:{m.chat.id}{Dev_FINAL}",
                    f"{get.user.id}:restrict_time:{m.chat.id}{Dev_FINAL}"
                )
                if co > 0:
                    return await m.reply(plugins_supervision_832(text_result))
                else:
                    return await m.reply(plugins_supervision_834(get.user.mention(), k))
            except:
                return await m.reply(plugins_supervision_836(k))

    if text == "المحظورين":
        if not await admin_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_supervision_840(k))
        else:
            co = 0
            cc = 1
            text_result = "\u0627\u0644\u0645\u062d\u0638\u0648\u0631\u064a\u0646:\n\n"
            ban_keys = []
            async for key in r.scan_iter(match=f"*:ban_reason:{m.chat.id}{Dev_FINAL}", count=100):
                ban_keys.append(key)
            for key in ban_keys:
                if co >= 100:
                    break
                try:
                    user_id_str = key.split(":ban_reason:")[0]
                    user_id = int(user_id_str)
                except Exception:
                    continue
                co += 1
                username = None
                try:
                    u = await c.get_chat(user_id)
                    username = u.username if u else None
                except Exception:
                    username = None
                user = f"@{username}" if username else f"<a href='tg://user?id={user_id}'>@{html.escape(str(channel))}</a>"
                text_result += f"{cc} \u2022 {user} \u21a4\ufe0e \u300c `{user_id}` \u300d \\n"
                cc += 1
            if co == 0:
                return await m.reply(plugins_supervision_867(k))
            else:
                return await m.reply(text_result)

    if text == "مسح المحظورين":
        if not await admin_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_supervision_873(k))
        else:
            co = 0
            ban_keys = []
            async for key in r.scan_iter(match=f"*:ban_reason:{m.chat.id}{Dev_FINAL}", count=100):
                ban_keys.append(key)
            for key in ban_keys:
                try:
                    user_id_str = key.split(":ban_reason:")[0]
                    user_id = int(user_id_str)
                except Exception:
                    continue
                co += 1
                try:
                    await c.unban_chat_member(m.chat.id, user_id)
                except Exception:
                    pass
                await r.delete(
                    f"{user_id}:ban_admin:{m.chat.id}{Dev_FINAL}",
                    f"{user_id}:ban_msg:{m.chat.id}{Dev_FINAL}",
                    f"{user_id}:ban_reason:{m.chat.id}{Dev_FINAL}",
                    f"{user_id}:ban_date:{m.chat.id}{Dev_FINAL}",
                    f"{user_id}:ban_time:{m.chat.id}{Dev_FINAL}"
                )
            if co == 0:
                return await m.reply(plugins_supervision_898(k))
            else:
                return await m.reply(plugins_supervision_900(k, co))

    if text == "طرد البوتات":
        if not await owner_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_supervision_904(k))
        else:
            co = 0
            bot_ids = set()
            try:
                admins = await c.bot.get_chat_administrators(m.chat.id)
                for adm in admins:
                    if getattr(adm.user, "is_bot", False):
                        bot_ids.add(adm.user.id)
            except Exception:
                pass
            try:
                bot_keys = []
                async for key in r.scan_iter(match=f"*:bot_member:{m.chat.id}{Dev_FINAL}", count=100):
                    bot_keys.append(key)
                for key in bot_keys:
                    try:
                        bot_ids.add(int(key.split(":bot_member:")[0]))
                    except Exception:
                        continue
            except Exception:
                pass
            for bot_id in bot_ids:
                try:
                    await m.chat.ban_member(bot_id)
                    co += 1
                except Exception:
                    pass
            if co == 0:
                return await m.reply(plugins_supervision_933(k))
            else:
                return await m.reply(plugins_supervision_935(k, co))

    if text == "كشف البوتات":
        if not await admin_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_supervision_939(k))
        else:
            co = 0
            text_result = "\u0628\u0648\u062a\u0627\u062a \u0627\u0644\u0645\u062c\u0645\u0648\u0639\u0629:\n\n"
            cc = 1
            bot_ids = set()
            try:
                admins = await c.bot.get_chat_administrators(m.chat.id)
                for adm in admins:
                    if getattr(adm.user, "is_bot", False):
                        bot_ids.add(adm.user.id)
            except Exception:
                pass
            try:
                bot_keys = []
                async for key in r.scan_iter(match=f"*:bot_member:{m.chat.id}{Dev_FINAL}", count=100):
                    bot_keys.append(key)
                for key in bot_keys:
                    try:
                        bot_ids.add(int(key.split(":bot_member:")[0]))
                    except Exception:
                        continue
            except Exception:
                pass
            for bot_id in bot_ids:
                if co == 100:
                    break
                co += 1
                try:
                    u = await c.get_chat(bot_id)
                    mention = f'<a href="tg://user?id={bot_id}">{html.escape(str(u.first_name if u else bot_id))}</a>'
                except Exception:
                    mention = f'<a href="tg://user?id={bot_id}">{html.escape(str(bot_id))}</a>'
                text_result += f"{cc}) {mention}"
                text_result += "\n"
                cc += 1
            if co == 0:
                return await m.reply(plugins_supervision_976(k))
            else:
                return await m.reply(text_result)

    if text == "رفع مشرف" and m.reply_to_message and m.reply_to_message.from_user:
        is_dev_disabled = await r.get(f"DevAdminStatus:{Dev_FINAL}")
        if is_dev_disabled == "disabled":
            if await dev2_pls(m.from_user.id, m.chat.id) and not await devp_pls(m.from_user.id, m.chat.id):
                try:
                    user_tg_member = await m.chat.get_member(m.from_user.id)
                    if user_tg_member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                        return
                except:
                    return

        is_promote_locked = await r.get(f"{m.chat.id}:LockPromote:{Dev_FINAL}")
        if is_promote_locked == "disabled":
            return await m.reply(plugins_supervision_993(k))

        if not await dev2_pls(m.from_user.id, m.chat.id) and not await gowner_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_supervision_996(k))

        get = await m.chat.get_member(c.id)
        if get.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return await m.reply(REPLIES['plugins_supervision_1000'])
        priv_ok = (
            get.can_manage_chat
            and get.can_delete_messages
            and get.can_restrict_members
            and get.can_pin_messages
            and get.can_invite_users
            and get.can_change_info
            and get.can_promote_members
        )
        if not priv_ok:
            return await m.reply(REPLIES['plugins_supervision_1000'])
        else:
            target_id = m.reply_to_message.from_user.id
            await r.set(f"{m.from_user.id}:promote_target:{m.chat.id}", target_id, ex=600)
            
            current_priv = {
                "can_change_info": False,
                "can_delete_messages": False,
                "can_restrict_members": False,
                "can_invite_users": False,
                "can_promote_members": False,
                "can_pin_messages": False,
                "can_edit_stories": False,
                "can_post_stories": False,
                "can_delete_stories": False,
                "can_manage_topics": False,
                "can_manage_tags": False,
                "can_manage_video_chats": False
            }
            
            try:
                target_member = await m.chat.get_member(target_id)
                if target_member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                    current_priv = {
                        "can_change_info": target_member.can_change_info or False,
                        "can_delete_messages": target_member.can_delete_messages or False,
                        "can_restrict_members": target_member.can_restrict_members or False,
                        "can_invite_users": target_member.can_invite_users or False,
                        "can_promote_members": target_member.can_promote_members or False,
                        "can_pin_messages": target_member.can_pin_messages or False,
                        "can_edit_stories": target_member.can_edit_stories or False,
                        "can_post_stories": target_member.can_post_stories or False,
                        "can_delete_stories": target_member.can_delete_stories or False,
                        "can_manage_topics": target_member.can_manage_topics or False,
                        "can_manage_tags": target_member.can_manage_tags or False,
                        "can_manage_video_chats": target_member.can_manage_video_chats or False
                    }
            except:
                pass
            
            await r.set(f"{m.from_user.id}:promote_privileges:{m.chat.id}", json.dumps(current_priv), ex=600)
            current_privileges = current_priv
            
            buttons = [
                [
                    InlineKeyboardButton(f"{'✓' if current_privileges.get('can_change_info', False) else '✗'} تغيير المعلومات", callback_data=f"promote_toggle_info:{target_id}"),
                    InlineKeyboardButton(f"{'✓' if current_privileges.get('can_delete_messages', False) else '✗'} حذف الرسائل", callback_data=f"promote_toggle_del:{target_id}")
                ],
                [
                    InlineKeyboardButton(f"{'✓' if current_privileges.get('can_restrict_members', False) else '✗'} حظر المستخدمين", callback_data=f"promote_toggle_ban:{target_id}"),
                    InlineKeyboardButton(f"{'✓' if current_privileges.get('can_manage_video_chats', False) else '✗'} ادارة المكالمات", callback_data=f"promote_toggle_calls:{target_id}")
                ],
                [
                    InlineKeyboardButton(f"{'✓' if current_privileges.get('can_invite_users', False) else '✗'} دعوة المستخدمين", callback_data=f"promote_toggle_invite:{target_id}"),
                    InlineKeyboardButton(f"{'✓' if current_privileges.get('can_promote_members', False) else '✗'} اضافة مشرفين", callback_data=f"promote_toggle_promote:{target_id}")
                ],
                [
                    InlineKeyboardButton(f"{'✓' if current_privileges.get('can_pin_messages', False) else '✗'} تثبيت الرسائل", callback_data=f"promote_toggle_pin:{target_id}"),
                    InlineKeyboardButton(f"{'✓' if current_privileges.get('can_edit_stories', False) else '✗'} تعديل القصص", callback_data=f"promote_toggle_edit_stories:{target_id}")
                ],
                [
                    InlineKeyboardButton(f"{'✓' if current_privileges.get('can_post_stories', False) else '✗'} نشر القصص", callback_data=f"promote_toggle_post_stories:{target_id}"),
                    InlineKeyboardButton(f"{'✓' if current_privileges.get('can_delete_stories', False) else '✗'} حذف القصص", callback_data=f"promote_toggle_delete_stories:{target_id}")
                ],
                [
                    InlineKeyboardButton(f"{'✓' if current_privileges.get('can_manage_topics', False) else '✗'} ادارة المواضيع", callback_data=f"promote_toggle_manage_topics:{target_id}"),
                    InlineKeyboardButton(f"{'✓' if current_privileges.get('can_manage_tags', False) else '✗'} ادارة الوسوم", callback_data=f"promote_toggle_manage_tags:{target_id}")
                ],
                [InlineKeyboardButton("جميع الصلاحيات", callback_data=f"promote_all:{target_id}")],
                [InlineKeyboardButton("رفع بالمحدد", callback_data=f"promote_apply:{target_id}")],
                [InlineKeyboardButton("اخفاء الرسالة", callback_data=f"promote_hide:{target_id}")]
            ]
            return await m.reply(REPLIES['plugins_supervision_1083'], reply_markup=InlineKeyboardMarkup(buttons))

    if text == "تنزيل مشرف" and m.reply_to_message and m.reply_to_message.from_user:
        if not await owner_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_supervision_1087(k))
        else:
            try:
                await c.promote_chat_member(
                    m.chat.id,
                    m.reply_to_message.from_user.id,
                    privileges=ChatPrivileges(
                        can_manage_chat=False,
                        can_delete_messages=False,
                        can_manage_video_chats=False,
                        can_restrict_members=False,
                        can_promote_members=False,
                        can_pin_messages=False,
                        can_change_info=False,
                        can_invite_users=False,
                        can_post_stories=False,
                        can_edit_stories=False,
                        can_delete_stories=False,
                        can_manage_topics=False,
                        can_manage_tags=False
                    )
                )
                return await m.reply(plugins_supervision_1109(m.reply_to_message.from_user.mention(), k))
            except:
                return await m.reply(plugins_supervision_1111(m.reply_to_message.from_user.mention(), k))

    if text == "برنت" and m.reply_to_message and m.reply_to_message.from_user:
        if not await admin_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_supervision_1115(k))
        target = m.reply_to_message.from_user
        await show_user_restrictions(c, m, target, k)
    
    elif text.startswith("برنت ") and len(text.split()) == 2:
        if not await admin_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_supervision_1121(k))
        
        target_input = text.split()[1]
        target = None
        
        try:
            if target_input.startswith("@"):
                target = await c.get_users(target_input)
            elif target_input.isdigit() or (target_input.startswith("-") and target_input[1:].isdigit()):
                target = await c.get_users(int(target_input))
            else:
                return await m.reply(plugins_supervision_1132(k))
        except Exception as e:
            return await m.reply(plugins_supervision_1134(k))
        
        await show_user_restrictions(c, m, target, k)

    return None

@Client.on_callback_query(filters.regex(r"^promote_"), group=-1431)
async def handle_promote_buttons(c, cb: CallbackQuery):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    k = await r.get(f'{Dev_FINAL}:botkey') or "•"
    if not cb.message: return
    chat_id = cb.message.chat.id
    parts = cb.data.split(":")
    if len(parts) < 2 or not parts[1].isdigit():
        return await cb.answer(REPLIES['plugins_owners_399'], show_alert=True)
    action = parts[0]
    target_id = int(parts[1])
    owner_key = f"{cb.from_user.id}:promote_target:{chat_id}"
    expected_target = await r.get(owner_key)
    if not expected_target or int(expected_target) != target_id:
        return await cb.answer(REPLIES['plugins_supervision_1156'], show_alert=True)
    try:
        target_member = await cb.message.chat.get_member(target_id)
    except:
        return await cb.answer(REPLIES['plugins_supervision_1160'], show_alert=True)
    priv_key = f"{cb.from_user.id}:promote_privileges:{chat_id}"
    current_priv_str = await r.get(priv_key)
    
    if current_priv_str:
        current_privileges = json.loads(current_priv_str)
    else:
        current_privileges = {}
        if target_member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            current_privileges = {
                "can_change_info": target_member.can_change_info or False,
                "can_delete_messages": target_member.can_delete_messages or False,
                "can_restrict_members": target_member.can_restrict_members or False,
                "can_invite_users": target_member.can_invite_users or False,
                "can_promote_members": target_member.can_promote_members or False,
                "can_pin_messages": target_member.can_pin_messages or False,
                "can_edit_stories": target_member.can_edit_stories or False,
                "can_post_stories": target_member.can_post_stories or False,
                "can_delete_stories": target_member.can_delete_stories or False,
                "can_manage_topics": target_member.can_manage_topics or False,
                "can_manage_tags": target_member.can_manage_tags or False,
                "can_manage_video_chats": target_member.can_manage_video_chats or False
            }
            await r.set(priv_key, json.dumps(current_privileges), ex=600)

    perm_map = {
        "info": "can_change_info",
        "del": "can_delete_messages",
        "ban": "can_restrict_members",
        "calls": "can_manage_video_chats",
        "invite": "can_invite_users",
        "promote": "can_promote_members",
        "pin": "can_pin_messages",
        "edit_stories": "can_edit_stories",
        "post_stories": "can_post_stories",
        "delete_stories": "can_delete_stories",
        "manage_topics": "can_manage_topics",
        "manage_tags": "can_manage_tags"
    }

    if action.startswith("promote_toggle_"):
        perm = action.replace("promote_toggle_", "")
        if perm in perm_map:
            current_privileges[perm_map[perm]] = not current_privileges.get(perm_map[perm], False)
            await r.set(priv_key, json.dumps(current_privileges), ex=600)
        
        buttons = [
            [
                InlineKeyboardButton(f"{'✓' if current_privileges.get('can_change_info', False) else '✗'} تغيير المعلومات", callback_data=f"promote_toggle_info:{target_id}"),
                InlineKeyboardButton(f"{'✓' if current_privileges.get('can_delete_messages', False) else '✗'} حذف الرسائل", callback_data=f"promote_toggle_del:{target_id}")
            ],
            [
                InlineKeyboardButton(f"{'✓' if current_privileges.get('can_restrict_members', False) else '✗'} حظر المستخدمين", callback_data=f"promote_toggle_ban:{target_id}"),
                InlineKeyboardButton(f"{'✓' if current_privileges.get('can_manage_video_chats', False) else '✗'} ادارة المكالمات", callback_data=f"promote_toggle_calls:{target_id}")
            ],
            [
                InlineKeyboardButton(f"{'✓' if current_privileges.get('can_invite_users', False) else '✗'} دعوة المستخدمين", callback_data=f"promote_toggle_invite:{target_id}"),
                InlineKeyboardButton(f"{'✓' if current_privileges.get('can_promote_members', False) else '✗'} اضافة مشرفين", callback_data=f"promote_toggle_promote:{target_id}")
            ],
            [
                InlineKeyboardButton(f"{'✓' if current_privileges.get('can_pin_messages', False) else '✗'} تثبيت الرسائل", callback_data=f"promote_toggle_pin:{target_id}"),
                InlineKeyboardButton(f"{'✓' if current_privileges.get('can_edit_stories', False) else '✗'} تعديل القصص", callback_data=f"promote_toggle_edit_stories:{target_id}")
            ],
            [
                InlineKeyboardButton(f"{'✓' if current_privileges.get('can_post_stories', False) else '✗'} نشر القصص", callback_data=f"promote_toggle_post_stories:{target_id}"),
                InlineKeyboardButton(f"{'✓' if current_privileges.get('can_delete_stories', False) else '✗'} حذف القصص", callback_data=f"promote_toggle_delete_stories:{target_id}")
            ],
            [
                InlineKeyboardButton(f"{'✓' if current_privileges.get('can_manage_topics', False) else '✗'} ادارة المواضيع", callback_data=f"promote_toggle_manage_topics:{target_id}"),
                InlineKeyboardButton(f"{'✓' if current_privileges.get('can_manage_tags', False) else '✗'} ادارة الوسوم", callback_data=f"promote_toggle_manage_tags:{target_id}")
            ],
            [InlineKeyboardButton("جميع الصلاحيات", callback_data=f"promote_all:{target_id}")],
            [InlineKeyboardButton("رفع بالمحدد", callback_data=f"promote_apply:{target_id}")],
            [InlineKeyboardButton("اخفاء الرسالة", callback_data=f"promote_hide:{target_id}")]
        ]
        try:
            await cb.message.edit_reply_markup(InlineKeyboardMarkup(buttons))
        except Exception as e:
            if "MESSAGE_NOT_MODIFIED" not in str(e): raise e
        await cb.answer()
        return
    
    if action == "promote_all":
        all_privileges = {
            "can_change_info": True,
            "can_delete_messages": True,
            "can_restrict_members": True,
            "can_invite_users": True,
            "can_promote_members": True,
            "can_pin_messages": True,
            "can_edit_stories": True,
            "can_post_stories": True,
            "can_delete_stories": True,
            "can_manage_topics": True,
            "can_manage_tags": True,
            "can_manage_video_chats": True
        }
        await r.set(priv_key, json.dumps(all_privileges), ex=600)
        
        buttons = [
            [InlineKeyboardButton("✓ تغيير المعلومات", callback_data=f"promote_toggle_info:{target_id}"), InlineKeyboardButton("✓ حذف الرسائل", callback_data=f"promote_toggle_del:{target_id}")],
            [InlineKeyboardButton("✓ حظر المستخدمين", callback_data=f"promote_toggle_ban:{target_id}"), InlineKeyboardButton("✓ ادارة المكالمات", callback_data=f"promote_toggle_calls:{target_id}")],
            [InlineKeyboardButton("✓ دعوة المستخدمين", callback_data=f"promote_toggle_invite:{target_id}"), InlineKeyboardButton("✓ اضافة مشرفين", callback_data=f"promote_toggle_promote:{target_id}")],
            [InlineKeyboardButton("✓ تثبيت الرسائل", callback_data=f"promote_toggle_pin:{target_id}"), InlineKeyboardButton("✓ تعديل القصص", callback_data=f"promote_toggle_edit_stories:{target_id}")],
            [InlineKeyboardButton("✓ نشر القصص", callback_data=f"promote_toggle_post_stories:{target_id}"), InlineKeyboardButton("✓ حذف القصص", callback_data=f"promote_toggle_delete_stories:{target_id}")],
            [InlineKeyboardButton("✓ ادارة المواضيع", callback_data=f"promote_toggle_manage_topics:{target_id}"), InlineKeyboardButton("✓ ادارة الوسوم", callback_data=f"promote_toggle_manage_tags:{target_id}")],
            [InlineKeyboardButton("جميع الصلاحيات", callback_data=f"promote_all:{target_id}")],
            [InlineKeyboardButton("رفع بالمحدد", callback_data=f"promote_apply:{target_id}")],
            [InlineKeyboardButton("اخفاء الرسالة", callback_data=f"promote_hide:{target_id}")]
        ]
        try:
            await cb.message.edit_reply_markup(InlineKeyboardMarkup(buttons))
        except Exception as e:
            if "MESSAGE_NOT_MODIFIED" not in str(e): raise e
        await cb.answer(REPLIES['plugins_supervision_1274'])
        return
    
    if action == "promote_hide":
        await cb.message.delete()
        await r.delete(owner_key)
        await r.delete(priv_key)
        await cb.answer(REPLIES['plugins_supervision_1281'])
        return
    
    if action == "promote_apply":
        if not current_privileges or not any(current_privileges.values()):
            return await cb.answer(REPLIES['plugins_supervision_1286'], show_alert=True)
        
        try:
            is_already_admin = target_member.status == ChatMemberStatus.ADMINISTRATOR
            
            await c.promote_chat_member(
                chat_id=chat_id,
                user_id=target_id,
                privileges=ChatPrivileges(
                    can_manage_chat=True,
                    can_manage_video_chats=current_privileges.get('can_manage_video_chats', False),
                    can_delete_messages=current_privileges.get('can_delete_messages', False),
                    can_restrict_members=current_privileges.get('can_restrict_members', False),
                    can_promote_members=current_privileges.get('can_promote_members', False),
                    can_pin_messages=current_privileges.get('can_pin_messages', False),
                    can_change_info=current_privileges.get('can_change_info', False),
                    can_invite_users=current_privileges.get('can_invite_users', False),
                    can_post_stories=current_privileges.get('can_post_stories', False),
                    can_edit_stories=current_privileges.get('can_edit_stories', False),
                    can_delete_stories=current_privileges.get('can_delete_stories', False),
                    can_manage_topics=current_privileges.get('can_manage_topics', False),
                    can_manage_tags=current_privileges.get('can_manage_tags', False)
                )
            )
            
            await r.sadd(f"{chat_id}:listADMIN:{Dev_FINAL}", target_id)
            await r.delete(owner_key)
            await r.delete(priv_key)
            
            if is_already_admin:
                success_text = f"\n{k} المشرف ↤︎ {target_member.user.mention()}\n{k}تم تعديل صلاحياته\n_ "
                alert_text = "تم تعديل صلاحيات المشرف بنجاح ✓"
            else:
                success_text = f"\n{k} المستخدم ↤︎ {target_member.user.mention()} \n{k} تم رفعه مشرف\n_"
                alert_text = "تم رفع المشرف بنجاح ✓"
                
            await cb.answer(alert_text, show_alert=True)
            await cb.message.edit_text(success_text, reply_markup=None)
            
        except Exception as e:
            await cb.answer(plugins_supervision_1326(e), show_alert=True)
        return

@Client.on_message(filters.group & ~filters.bot, group=-1433)
async def main_message7_handler(c, m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    k = await r.get(f'{Dev_FINAL}:botkey')
    if await check_all_restrictions(c, m, k): return
    text = m.text or ""
    if text:
        await handle_moderation_commands(c, m, k, text)