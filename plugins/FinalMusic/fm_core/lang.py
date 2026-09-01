# Plugins1/FinalMusic/fm_core/lang.py
from helpers.context import redis_proxy as r, dev_final_proxy as Dev_FINAL, k_proxy as k
import json
from functools import wraps
from pathlib import Path
import logging
logger = logging.getLogger("FinalMusic")
lang_codes = {"en": "English"}
class Language:
    def __init__(self):
        self.lang_codes = lang_codes
        self.lang_dir = Path("plugins/FinalMusic/locales")
        self.languages = self.load_files()
    def load_files(self):
        languages = {}
        for lang_code in self.lang_codes.keys():
            lang_file = self.lang_dir / f"{lang_code}.json"
            if lang_file.exists():
                with open(lang_file, "r", encoding="utf-8") as file:
                    languages[lang_code] = json.load(file)
        logger.info(f"🌐 Loaded languages: {', '.join(languages.keys())}")
        return languages
    async def get_lang(self, chat_id: int) -> dict:
        return self.languages["en"]
    def language(self):
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                fallen = next((arg for arg in args if hasattr(arg, "chat") or hasattr(arg, "message")), None)
                if hasattr(fallen, "chat"):
                    chat = fallen.chat
                elif hasattr(fallen, "message"):
                    chat = fallen.message.chat
                blacklisted = await r.smembers(f"blacklist_chats:{Dev_FINAL}")
                if chat.id in [int(b) for b in blacklisted] if blacklisted else []:
                    return await chat.leave()
                lang_code = "en"
                lang_dict = self.languages[lang_code]
                setattr(fallen, "lang", lang_dict)
                return await func(*args, **kwargs)
            return wrapper
        return decorator
lang = Language()        