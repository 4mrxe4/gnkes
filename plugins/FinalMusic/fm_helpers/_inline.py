# helpers/_inline.py — rebuilt for botm_unified (aiogram/compat only)
# The old standalone system had a custom "تعديل_الازرار" plugin (Plugins1)
# that is NOT part of botm_unified. The music module must not depend on it.
# These helpers produce aiogram-compatible inline keyboards directly.
from compat import InlineKeyboardMarkup as IKM, InlineKeyboardButton as IKB
from helpers.context import redis_proxy as r, dev_final_proxy as Dev_FINAL, k_proxy as k
from helpers.context import config_proxy as config

BUTTONS_DEFINITIONS = {
    "controls": {
        "name": "أزرار التحكم بالتشغيل",
        "buttons": [
            {"id": "status", "default": "الحالة"},
            {"id": "seek_back_30", "default": "I◂◂ 30"},
            {"id": "seek_back_10", "default": "◂◂ 10"},
            {"id": "seek_forward_10", "default": "10 ▸▸"},
            {"id": "seek_forward_30", "default": "30 ▸▸I"},
            {"id": "resume", "default": "▷"},
            {"id": "pause", "default": "II"},
            {"id": "replay", "default": "↻"},
            {"id": "skip", "default": "⋮⋮I"},
            {"id": "stop", "default": "□"},
            {"id": "close", "default": "✕"},
            {"id": "toggle", "default": "▷"},
        ]
    }
}


def register_buttons(_definitions) -> None:
    """No-op kept for compatibility (button-editing system is parent-owned)."""
    return None


async def create_button_raw(_group: str, _btn_id: str, text: str, callback_data: str = None) -> dict:
    """Build a raw inline keyboard button dict (compat-compatible)."""
    return {"text": text, "callback_data": callback_data or f"noop:{id(text)}"}


async def send_telegram_api(client, method: str, params: dict):
    """Send a raw Bot API call through the parent compat client (aiogram)."""
    import logging
    logger = logging.getLogger("FinalMusic")
    try:
        bot = getattr(client, "_bot", None)
        if bot is None:
            from helpers.context import get_bot_from_client
            bot = get_bot_from_client(client)
        if bot is None:
            logger.warning(f"send_telegram_api({method}): no aiogram Bot instance found")
            return None
        from aiogram import Bot
        if not isinstance(bot, Bot):
            logger.warning(f"send_telegram_api({method}): resolved object is not an aiogram Bot")
            return None
        # aiogram Bot exposes raw API methods via __getattr__; fall back to
        # our own send/edit implementations when the method is unavailable.
        if method == "sendMessage":
            return await bot.send_message(
                chat_id=params.get("chat_id"),
                text=params.get("text", ""),
                parse_mode=params.get("parse_mode"),
                reply_markup=params.get("reply_markup"),
            )
        if method == "editMessageReplyMarkup":
            return await bot.edit_message_reply_markup(
                chat_id=params.get("chat_id"),
                message_id=params.get("message_id"),
                reply_markup=params.get("reply_markup"),
            )
        if method == "editMessageText":
            return await bot.edit_message_text(
                text=params.get("text", ""),
                chat_id=params.get("chat_id"),
                message_id=params.get("message_id"),
                parse_mode=params.get("parse_mode"),
                reply_markup=params.get("reply_markup"),
            )
        return None
    except Exception as e:
        logger.warning(f"send_telegram_api({method}) failed: {e}")
        return None


class Inline:
    def __init__(self):
        self.ikm = IKM
        self.ikb = IKB

    def controls(self, chat_id: int, status: str = None, timer: str = None, remove: bool = False, user_id: int = 0):
        keyboard = []
        if status:
            keyboard.append([self.ikb(text=status, callback_data=f"controls status {chat_id} {user_id}")])
        elif timer:
            keyboard.append([self.ikb(text=timer, callback_data=f"controls status {chat_id} {user_id}")])
        if not remove:
            keyboard.append([
                self.ikb(text="I◂◂ 30", callback_data=f"controls seek_back_30 {chat_id} {user_id}"),
                self.ikb(text="◂◂ 10", callback_data=f"controls seek_back_10 {chat_id} {user_id}"),
                self.ikb(text="10 ▸▸", callback_data=f"controls seek_forward_10 {chat_id} {user_id}"),
                self.ikb(text="30 ▸▸I", callback_data=f"controls seek_forward_30 {chat_id} {user_id}"),
            ])
            keyboard.append([
                self.ikb(text="▷", callback_data=f"controls resume {chat_id} {user_id}"),
                self.ikb(text="II", callback_data=f"controls pause {chat_id} {user_id}"),
                self.ikb(text="↻", callback_data=f"controls replay {chat_id} {user_id}"),
                self.ikb(text="⋮⋮I", callback_data=f"controls skip {chat_id} {user_id}"),
                self.ikb(text="□", callback_data=f"controls stop {chat_id} {user_id}"),
            ])
            keyboard.append([self.ikb(text="✕", callback_data=f"controls close {chat_id} {user_id}")])
        return self.ikm(keyboard)

    def play_queued(self, chat_id: int, item_id: str, _text: str, user_id: int = 0):
        return self.ikm([
            [
                self.ikb(text="▷", callback_data=f"controls resume {chat_id} {user_id}"),
                self.ikb(text="∣ ∣", callback_data=f"controls pause {chat_id} {user_id}"),
                self.ikb(text="I⋮⋮", callback_data=f"controls skip {chat_id} {user_id}"),
                self.ikb(text="□", callback_data=f"controls stop {chat_id} {user_id}"),
            ],
            [self.ikb(text="حذف", callback_data=f"controls close {chat_id} {user_id}")],
        ])

    def queue_markup(self, chat_id: int, _text: str, playing: bool, user_id: int = 0):
        _action = "pause" if playing else "resume"
        return self.ikm([[self.ikb(text=_text, callback_data=f"controls {_action} {chat_id} q {user_id}")]])

    async def controls_raw(self, chat_id: int, status: str = None, timer: str = None, remove: bool = False, user_id: int = 0) -> dict:
        return (await self._controls_markup(chat_id, status, timer, remove, user_id)).model_dump(exclude_none=True)

    async def _controls_markup(self, chat_id: int, status: str = None, timer: str = None, remove: bool = False, user_id: int = 0):
        return self.controls(chat_id, status, timer, remove, user_id)

    async def play_queued_raw(self, chat_id: int, item_id: str, _text: str, user_id: int = 0) -> dict:
        return self.play_queued(chat_id, item_id, _text, user_id).model_dump(exclude_none=True)

    async def queue_markup_raw(self, chat_id: int, _text: str, playing: bool, user_id: int = 0) -> dict:
        return self.queue_markup(chat_id, _text, playing, user_id).model_dump(exclude_none=True)

    async def send_controls(self, client, chat_id: int, text: str, status: str = None, timer: str = None, remove: bool = False, user_id: int = 0, parse_mode: str = "HTML"):
        markup = self.controls(chat_id, status, timer, remove, user_id)
        return await send_telegram_api(client, "sendMessage", {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode,
            "reply_markup": markup,  # نمرر كائن InlineKeyboardMarkup كما هو -- aiogram يحتاج الكائن نفسه لا dict
        })

    async def edit_controls_markup(self, client, chat_id: int, message_id: int, status: str = None, timer: str = None, remove: bool = False, user_id: int = 0):
        markup = self.controls(chat_id, status, timer, remove, user_id)
        return await send_telegram_api(client, "editMessageReplyMarkup", {
            "chat_id": chat_id,
            "message_id": message_id,
            "reply_markup": markup,  # نمرر كائن InlineKeyboardMarkup كما هو -- aiogram يحتاج الكائن نفسه لا dict
        })

    async def send_play_queued(self, client, chat_id: int, text: str, item_id: str, _text: str, user_id: int = 0, parse_mode: str = "HTML"):
        markup = self.play_queued(chat_id, item_id, _text, user_id)
        return await send_telegram_api(client, "sendMessage", {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode,
            "reply_markup": markup,  # نمرر كائن InlineKeyboardMarkup كما هو -- aiogram يحتاج الكائن نفسه لا dict
        })

    async def edit_play_queued_markup(self, client, chat_id: int, message_id: int, item_id: str, _text: str, user_id: int = 0):
        markup = self.play_queued(chat_id, item_id, _text, user_id)
        return await send_telegram_api(client, "editMessageReplyMarkup", {
            "chat_id": chat_id,
            "message_id": message_id,
            "reply_markup": markup,  # نمرر كائن InlineKeyboardMarkup كما هو -- aiogram يحتاج الكائن نفسه لا dict
        })

    async def edit_queue_markup(self, client, chat_id: int, message_id: int, _text: str, playing: bool, user_id: int = 0):
        markup = self.queue_markup(chat_id, _text, playing, user_id)
        return await send_telegram_api(client, "editMessageReplyMarkup", {
            "chat_id": chat_id,
            "message_id": message_id,
            "reply_markup": markup,  # نمرر كائن InlineKeyboardMarkup كما هو -- aiogram يحتاج الكائن نفسه لا dict
        })

    def yt_key(self, url: str):
        """Inline keyboard with a single 'open on YouTube' button (aiogram)."""
        return self.ikm([
            [self.ikb(text="▶️ فتح على يوتيوب", url=url)],
        ])

    def cancel_dl(self, text: str = "إلغاء"):
        """Cancel-download button (aiogram)."""
        return self.ikm([
            [self.ikb(text=text, callback_data="cancel_dl")],
        ])
