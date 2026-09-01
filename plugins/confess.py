import html
from helpers.context import get_global_r, get_global_dev, get_global_k
r = get_global_r()
Dev_FINAL = get_global_dev()
k = get_global_k()
import random, re, time, os, sys, pytz, string
from helpers.http import telegram_api_post
from threading import Thread
from compat import *
from compat import *
from compat import *
from datetime import datetime 
from helpers.ranks import *
from .buttons import register_buttons, get_button_custom, get_button_color, create_button_raw
import settings
from helpers.replies_store import (
    REPLIES,
    plugins_confess_128,
    plugins_confess_199,
    plugins_confess_255,
    plugins_confess_283,
)

BUTTONS_DEFINITIONS = {
    "sarhni": {
        "name": "أزرار صارحني",
        "buttons": [
            {"id": "send_btn", "default": "📩"},
            {"id": "cancel_btn", "default": "الغاء"},
            {"id": "channel_btn", "default": "🧚‍♀️"},
            {"id": "reply_btn", "default": "رد"},
            {"id": "reply_confirm", "default": "رد"},
        ]
    }
}

register_buttons(BUTTONS_DEFINITIONS)

def get_sarhni_id():
   rndm = ''.join([random.choice(string.ascii_letters
            + string.digits) for n in range(10)])
   return rndm
   
@Client.on_message(filters.text & filters.group, group=37)
async def sarhniHandler(c,m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    k = await r.get(f'{Dev_FINAL}:botkey')
    await sarhniFunc(c,m,k)
    
async def sarhniFunc(c, m, k):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if not await check_global_restrictions(c, m, k):
        return
    text = m.text
    name = await r.get(f'{Dev_FINAL}:BotName') if await r.get(f'{Dev_FINAL}:BotName') else 'فاينل'
    if text.startswith(f'{name} '):
        text = text.replace(f'{name} ', '')
    if await r.get(f'{m.chat.id}:Custom:{m.chat.id}{Dev_FINAL}&text={text}'):
        text = await r.get(f'{m.chat.id}:Custom:{m.chat.id}{Dev_FINAL}&text={text}')
    if await r.get(f'Custom:{Dev_FINAL}&text={text}'):
        text = await r.get(f'Custom:{Dev_FINAL}&text={text}')
    if await check_and_guard_locked_command(c, m, k, text):
        return

    if text == 'صارحني':
        if not await r.get(f'{m.from_user.id}:sar7ni:{Dev_FINAL}'):
            id = get_sarhni_id()
            await r.set(f'{m.from_user.id}:sar7ni:{Dev_FINAL}', id)
            await r.set(f'{id}:sarhni:{Dev_FINAL}', m.from_user.id)
        else:
            id = await r.get(f'{m.from_user.id}:sar7ni:{Dev_FINAL}')
        await r.set(f'{m.from_user.id}:sarhniname', m.from_user.first_name)
        
        me = await c.get_me()
        bot_username = me.username
        
        send_btn = await create_button_raw("sarhni", "send_btn", "📩", url=f't.me/{bot_username}?start=sarhni{id}')
        
        bot_token = c.bot_token if hasattr(c, "bot_token") else settings.TOKEN
        chat_id = m.chat.id
        reply_to_message_id = m.id
        
        mention_html = f'<a href="tg://user?id={m.from_user.id}">{html.escape(str(m.from_user.first_name))}</a>'
        text_msg = f'{k} أهلين عيني「 {mention_html} 」\n{k} هذا رابط صارحني الخاص فيك'
        
        await telegram_api_post(bot_token, "sendMessage", {
                "chat_id": chat_id,
                "text": text_msg,
                "parse_mode": "HTML",
                "reply_to_message_id": reply_to_message_id,
                "reply_markup": {"inline_keyboard": [[send_btn]]}
            })

@Client.on_message(filters.private, group=2)
async def sarhniHandlerP(c,m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    k = await r.get(f'{Dev_FINAL}:botkey')
    channel = await r.get(f'{Dev_FINAL}:BotChannel') if await r.get(f'{Dev_FINAL}:BotChannel') else ''
    await sarhniFuncP(c,m,k,channel)


async def _has_whisper_pending(r, Dev_FINAL, user_id):
    """fix NEW-5: هل لدى المستخدم همسة قيد الكتابة الآن؟"""
    try:
        keys = await r.keys(f"{Dev_FINAL}:whisper_pending:*")
        for key in keys:
            key_str = key if isinstance(key, str) else key.decode("utf-8")
            data = await r.hgetall(key_str)
            if data and str(data.get(b"writer", data.get("writer", b""))).strip("b'\'") == str(user_id):
                return True
    except Exception:
        return False
    return False

async def sarhniFuncP(c,m,k,channel):
   r = get_global_r()
   Dev_FINAL = get_global_dev()
   k = get_global_k()
   bot_token = c.bot_token if hasattr(c, "bot_token") else settings.TOKEN
   chat_id = m.chat.id
   
   if m.text:
      text = m.text
      if text.startswith('/start sarhni'):
        id = text.split('sarhni')[1]
        if not await r.get(f'{id}:sarhni:{Dev_FINAL}'):
          return await m.reply(plugins_confess_128(k))
        else:
          user_id = int((await r.get(f'{id}:sarhni:{Dev_FINAL}')) or 0)
          if m.from_user.id == user_id:
            return await m.reply(REPLIES['plugins_confess_132'])
          get = await c.get_chat(user_id)
          await r.set(f'{m.from_user.id}:sarhni',get.id,ex=300)
          
          cancel_btn = await create_button_raw("sarhni", "cancel_btn", "الغاء", callback_data='sarhni:bye')
          channel_btn = await create_button_raw("sarhni", "channel_btn", "🧚‍♀️", url=f't.me/{channel}')
          
          mention_html = f'<a href="tg://user?id={get.id}">{html.escape(str(get.first_name))}</a>'
          text_msg = f'{k} دخلت الحين رابط صارحني مع「 {mention_html} 」\n{k} اي رسالة ترسلها لي راح احولها له بسرية تامة بدون مايعرفك\n༄'
          
          response = await telegram_api_post(bot_token, "sendMessage", {
                  "chat_id": chat_id,
                  "text": text_msg,
                  "parse_mode": "HTML",
                  "reply_markup": {
                      "inline_keyboard": [
                          [cancel_btn],
                          [channel_btn]
                      ]
                  }
              })
          
          if response.get('ok'):
              msg_id = response['result']['message_id']
              await telegram_api_post(bot_token, "pinChatMessage", {
                      "chat_id": chat_id,
                      "message_id": msg_id
                  })
          return
      
      if await r.get(f'{m.from_user.id}:sarhni') and len(text) < 1000:
        if await r.exists(f'{Dev_FINAL}:whisper_pending:') or await _has_whisper_pending(r, Dev_FINAL, m.from_user.id):
            return
        user_id = int((await r.get(f'{m.from_user.id}:sarhni')) or 0)
        name = await r.get(f'{user_id}:sarhniname')
        TIME_ZONE = "Asia/Riyadh"
        ZONE = pytz.timezone(TIME_ZONE)
        TIME = datetime.now(ZONE)
        clock = TIME.strftime("%I:%M %p")
        date = TIME.strftime("%d/%m/%Y")
        txt = f'{k} وصلتك رسالة مصارحة جديدة\n{k} التاريخ : {date}\n{k} الساعة : {clock}\n\n{k} الرسالة :\n\n{text}\n'
        
        reply_btn = await create_button_raw("sarhni", "reply_btn", "رد", callback_data=f'sarhni+rep{m.from_user.id}')
        channel_btn = await create_button_raw("sarhni", "channel_btn", "🧚‍♀️", url=f't.me/{channel}')
        
        try:
          await telegram_api_post(bot_token, "sendMessage", {
                  "chat_id": user_id,
                  "text": txt,
                  "parse_mode": "HTML",
                  "disable_web_page_preview": True,
                  "reply_markup": {
                      "inline_keyboard": [
                          [reply_btn],
                          [channel_btn]
                      ]
                  }
              })
          return await m.reply(plugins_confess_199(k, name),quote=True)
        except Exception as e:  
          print(e)
          return await m.reply(REPLIES['plugins_confess_258'],quote=True)
   
   if await r.get(f'{m.from_user.id}:sarhni'):
     if await _has_whisper_pending(r, Dev_FINAL, m.from_user.id):
       return
     user_id = int((await r.get(f'{m.from_user.id}:sarhni')) or 0)
     name = await r.get(f'{user_id}:sarhniname')
     TIME_ZONE = "Asia/Riyadh"
     ZONE = pytz.timezone(TIME_ZONE)
     TIME = datetime.now(ZONE)
     clock = TIME.strftime("%I:%M %p")
     date = TIME.strftime("%d/%m/%Y")
     txt = f'{k} وصلتك رسالة مصارحة جديدة\n{k} التاريخ : {date}\n{k} الساعة : {clock}\n\n{k} الرسالة :'
     
     reply_btn = await create_button_raw("sarhni", "reply_btn", "رد", callback_data=f'sarhni+rep{m.from_user.id}')
     channel_btn = await create_button_raw("sarhni", "channel_btn", "🧚‍♀️", url=f't.me/{channel}')
     
     try:
       await telegram_api_post(bot_token, "sendMessage", {
               "chat_id": user_id,
               "text": txt,
               "parse_mode": "HTML",
               "disable_web_page_preview": True
           })
       
       if m.media:
           await telegram_api_post(bot_token, "forwardMessage", {
                   "chat_id": user_id,
                   "from_chat_id": chat_id,
                   "message_id": m.id
               })
       else:
           await telegram_api_post(bot_token, "sendMessage", {
                   "chat_id": user_id,
                   "text": m.text,
                   "parse_mode": "HTML",
                   "reply_markup": {
                       "inline_keyboard": [
                           [reply_btn],
                           [channel_btn]
                       ]
                   }
               })
       
       return await m.reply(plugins_confess_255(k, name),quote=True)
     except Exception as e:
       print(e)
       return await m.reply(REPLIES['plugins_confess_258'],quote=True)
   
   if await r.get(f'{m.from_user.id}:sarhnirep'):
     user_id = int((await r.get(f'{m.from_user.id}:sarhnirep')) or 0)
     await r.delete(f'{m.from_user.id}:sarhnirep')
     
     if m.text:
         await telegram_api_post(bot_token, "sendMessage", {
                 "chat_id": user_id,
                 "text": m.text,
                 "parse_mode": "HTML"
             })
     elif m.media:
         await telegram_api_post(bot_token, "forwardMessage", {
                 "chat_id": user_id,
                 "from_chat_id": chat_id,
                 "message_id": m.id
             })
     
     await m.reply(plugins_confess_283(k),quote=True)
     return

@Client.on_callback_query(filters.regex(r"^sarhni"), group=7)
async def sarhni_callback(c,m):
   r = get_global_r()
   Dev_FINAL = get_global_dev()
   k = get_global_k()
   bot_token = c.bot_token if hasattr(c, "bot_token") else settings.TOKEN
   
   if m.data == 'sarhni:bye':
     await r.delete(f'{m.from_user.id}:sarhni')
     await telegram_api_post(bot_token, "deleteMessage", {
             "chat_id": m.message.chat.id,
             "message_id": m.message.id
         })
     return await m.answer(REPLIES['plugins_confess_302'], show_alert=True)
   
   if m.data.startswith('sarhni+rep'):
     user_id = int(m.data.split('rep')[1])
     if not await r.get(f'{user_id}:sarhni'):
       return await m.answer(REPLIES['plugins_confess_307'], show_alert=True)
     if not int((await r.get(f'{user_id}:sarhni')) or 0) == m.from_user.id:
       return await m.answer(REPLIES['plugins_confess_307'], show_alert=True)
     else:
       await r.set(f'{m.from_user.id}:sarhnirep', user_id, ex=300)
       await telegram_api_post(bot_token, "sendMessage", {
               "chat_id": m.from_user.id,
               "text": "ارسل الرد الحين",
               "parse_mode": "HTML"
           })
       await m.answer()