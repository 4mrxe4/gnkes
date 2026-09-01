from helpers.context import get_global_r, get_global_dev, get_global_k
r = get_global_r()
Dev_FINAL = get_global_dev()
k = get_global_k()
k = get_global_k()
Dev_FINAL = get_global_dev()
r = get_global_r()
from helpers.context import get_global_r, get_global_dev, get_global_k
"""
[ = This plugin is a part from Rfinal Source code = ]
{"Developer":"https://t.me/i0i0ii"}
"""
from compat import Client
import random
from compat import *
from compat import *
from helpers.ranks import *
from helpers.games import *
from compat import Client
from helpers.replies_store import (
    plugins_games_questions_29,
)
async def handle_quiz_games(c, m, k, text):
   r = get_global_r()
   Dev_FINAL = get_global_dev()
   k = get_global_k()
   if text == 'عواصم':
     country=random.choice(countries)
     name = country['name']
     capital=country['capital']
     await r.set(f'{m.chat.id}:game:{Dev_FINAL}', capital,ex=600)
     await m.reply(plugins_games_questions_29(k, name))
     return True
   
   if text == 'دين':
     dee = random.choice(deen)
     question = dee['question']
     answer = dee['answer']
     await r.set(f'{m.chat.id}:game:{Dev_FINAL}', answer ,ex=600)
     await m.reply(question)
     return True
   
   if text == 'اعلام':
     country=random.choice(countries_)
     name = country['name']
     flag=country['flag']
     await r.set(f'{m.chat.id}:game:{Dev_FINAL}', name,ex=600)
     await m.reply_photo(flag, caption='ايش اسم الدولة ؟')
     return True

   return None
