from __future__ import annotations

import asyncio
import datetime
import copy
import inspect
import re
import time
import html
from collections import defaultdict
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Union

from aiogram import Bot, F
from aiogram.enums import ChatType as AioChatType
from aiogram.enums import ParseMode as AioParseMode
from aiogram.enums import ChatAction as AioChatAction
from aiogram.exceptions import (
    AiogramError,
    TelegramAPIError,
    TelegramBadRequest,
    TelegramForbiddenError,
    TelegramNetworkError,
    TelegramRetryAfter,
    TelegramNotFound,
)
from aiogram.filters import Command, CommandObject, CommandStart, BaseFilter, and_f, or_f, invert_f
from aiogram.types import (
    CallbackQuery as AioCallbackQuery,
    Chat as AioChat,
    ChatJoinRequest as AioChatJoinRequest,
    ChatMemberUpdated as AioChatMemberUpdated,
    ChatPermissions as AioChatPermissions,
    InlineKeyboardButton as AioInlineKeyboardButton,
    InlineKeyboardMarkup as AioInlineKeyboardMarkup,
    InlineQuery as AioInlineQuery,
    InlineQueryResultArticle as AioInlineQueryResultArticle,
    InputMediaAudio as AioInputMediaAudio,
    InputMediaPhoto as AioInputMediaPhoto,
    InputMediaVideo as AioInputMediaVideo,
    InputTextMessageContent as AioInputTextMessageContent,
    Message as AioMessage,
    MessageEntity as AioMessageEntity,
    ReactionTypeEmoji as AioReactionTypeEmoji,
    User as AioUser,
)


class StopPropagation(Exception):
    """أوقف معالجة الـ update في باقي المجموعات (groups)."""


class ContinuePropagation(Exception):
    """تابع معالجة الـ update في المجموعات التالية."""


class ChatPrivileges:
    """حاوية صلاحيات رفع المشرف (pyrogram-style) مدعومة في aiogram 3.x."""

    def __init__(self, **kwargs):
        self._kwargs = dict(kwargs)

    def to_kwargs(self) -> dict:
        return dict(self._kwargs)

    def get(self, key, default=None):
        return self._kwargs.get(key, default)

    def __repr__(self):
        return f"ChatPrivileges({self._kwargs!r})"


def _html_escape(text: str) -> str:
    """يهرّب أحرف HTML في النص (fix F-5)."""
    if not isinstance(text, str):
        return text
    return (text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;"))


def _htmlize_backticks(text: str) -> str:
    """يحوّل أزواج backticks `...` إلى <code>...</code> (fix F-8).

    يُطبَّق فقط عند الإرسال بصيغة HTML حتى لا تظهر `` xx `` كنص خام.
    """
    if not isinstance(text, str) or "`" not in text:
        return text
    out = []
    in_code = False
    for chunk in text.split("`"):
        if in_code:
            out.append("<code>" + _html_escape(chunk) + "</code>")
        else:
            out.append(chunk)
        in_code = not in_code
    if in_code:
        out.append("")
    return "".join(out)



class ChatType(str, Enum):
    PRIVATE = "private"
    BOT = "bot"
    GROUP = "group"
    SUPERGROUP = "supergroup"
    CHANNEL = "channel"


class ChatMemberStatus(str, Enum):
    OWNER = "creator"
    ADMINISTRATOR = "administrator"
    MEMBER = "member"
    RESTRICTED = "restricted"
    LEFT = "left"
    BANNED = "kicked"


class ParseMode(str, Enum):
    DEFAULT = "default"
    MARKDOWN = "Markdown"
    HTML = "HTML"
    MARKDOWN_V2 = "MarkdownV2"


class ChatAction(str, Enum):
    TYPING = "typing"
    UPLOAD_PHOTO = "upload_photo"
    RECORD_VIDEO = "record_video"
    UPLOAD_VIDEO = "upload_video"
    RECORD_AUDIO = "record_audio"
    UPLOAD_AUDIO = "upload_audio"
    CHOOSE_STICKER = "choose_sticker"
    FIND_LOCATION = "find_location"
    RECORD_VOICE = "record_voice"
    UPLOAD_VOICE = "upload_voice"
    PLAY_GAME = "play_game"


class MessageEntityType(str, Enum):
    MENTION = "mention"
    HASHTAG = "hashtag"
    CASHTAG = "cashtag"
    BOT_COMMAND = "bot_command"
    URL = "url"
    EMAIL = "email"
    PHONE_NUMBER = "phone_number"
    BOLD = "bold"
    ITALIC = "italic"
    UNDERLINE = "underline"
    STRIKETHROUGH = "strikethrough"
    SPOILER = "spoiler"
    CODE = "code"
    PRE = "pre"
    TEXT_LINK = "text_link"
    TEXT_MENTION = "text_mention"
    CUSTOM_EMOJI = "custom_emoji"


class ChatMembersFilter(str, Enum):
    """فلاتر enumerate_chat_members في pyrogram (MTProto)."""

    SEARCH = "search"
    BANNED = "banned"
    RESTRICTED = "restricted"
    BOTS = "bots"
    RECENT = "recent"
    ADMINISTRATORS = "administrators"



class RPCError(Exception):
    """خطأ عام من Telegram API."""


class FloodWait(RPCError):
    def __init__(self, value, *args, **kwargs):
        if isinstance(value, TelegramRetryAfter):
            self.value = value.retry_after
            self.x = value.retry_after
            self.seconds = value.retry_after
        else:
            self.value = value
            self.x = value
            self.seconds = value
        super().__init__(f"Telegram is flooding. Wait {self.value} seconds")


class MessageNotModified(RPCError):
    pass


class MessageIdInvalid(RPCError):
    pass


class MessageDeleteForbidden(RPCError):
    pass


class UserNotParticipant(RPCError):
    pass


class ChannelInvalid(RPCError):
    pass


class UserIsBlocked(RPCError):
    pass


class InputUserDeactivated(RPCError):
    pass


class PeerIdInvalid(RPCError):
    pass


class ChatWriteForbidden(RPCError):
    pass


class MessageEmpty(RPCError):
    pass


class BadRequest(RPCError):
    pass


class Forbidden(RPCError):
    pass


class Unauthorized(RPCError):
    pass


class SlowmodeInterval(RPCError):
    pass


_HTML_TAG_RE = re.compile(r'<[^>]+>')


def _strip_html_tags(text):
    """يزيل كل وسوم HTML من النص — تراجع أخير آمن عند رفض تيليجرام لوسوم
    فاسدة (can't parse entities)، بدل تحطّم عملية الإرسال بالكامل."""
    if not isinstance(text, str):
        return text
    return _HTML_TAG_RE.sub('', text)


def _is_entity_parse_error(exc: Exception) -> bool:
    msg = str(exc).lower()
    return "can't parse entities" in msg or "cant parse entities" in msg


def _map_exception(exc: Exception) -> Exception:
    """يحول استثناءات aiogram إلى استثناءات pyrogram-style معروفة."""
    if isinstance(exc, TelegramRetryAfter):
        return FloodWait(exc)
    if isinstance(exc, TelegramNotFound):
        text = str(exc)
        low = text.lower()
        if "message to edit not found" in low or "message to delete not found" in low:
            return MessageIdInvalid(text)
        if "message is not modified" in low:
            return MessageNotModified(text)
        if "chat not found" in low:
            return PeerIdInvalid(text)
        if "user not found" in low:
            return PeerIdInvalid(text)
        if "bad request: user not found" in low:
            return PeerIdInvalid(text)
        return RPCError(text)
    if isinstance(exc, TelegramForbiddenError):
        text = str(exc)
        low = text.lower()
        if "bot was blocked by the user" in low:
            return UserIsBlocked(text)
        if "user is deactivated" in low:
            return InputUserDeactivated(text)
        if "bot can't initiate conversation" in low:
            return ChatWriteForbidden(text)
        if "forbidden: bot is not a member" in low:
            return ChannelInvalid(text)
        return Forbidden(text)
    if isinstance(exc, TelegramBadRequest):
        text = str(exc)
        low = text.lower()
        if "message is not modified" in low:
            return MessageNotModified(text)
        if "message to edit not found" in low or "message to delete not found" in low:
            return MessageIdInvalid(text)
        if "message can't be deleted" in low:
            return MessageDeleteForbidden(text)
        if "chat not found" in low:
            return PeerIdInvalid(text)
        if "user not found" in low:
            return PeerIdInvalid(text)
        if "chat_admin_required" in low or "need administrator rights" in low:
            return ChatWriteForbidden(text)
        if "have no rights to send" in low:
            return ChatWriteForbidden(text)
        if "slowmode" in low:
            return SlowmodeInterval(text)
        if "user is not a participant" in low:
            return UserNotParticipant(text)
        if "button_url_invalid" in low or "bad request" in low:
            return BadRequest(text)
        return BadRequest(text)
    if isinstance(exc, TelegramNetworkError):
        return RPCError(str(exc))
    if isinstance(exc, AiogramError):
        return RPCError(str(exc))
    return exc


async def _safe_call(coro, allow_peer_missing: bool = False):
    """ينفّذ استدعاء aiogram ويرفع استثناءات pyrogram-style.

    allow_peer_missing=True (fix F-1): لا يرفع PeerIdInvalid عند "chat not found"
    بل يعيد None حتى لا ينهار أمر "المطوّر" وغيره عند غياب المحادثة/المستخدم.
    """
    try:
        return await coro
    except Exception as e:
        mapped = _map_exception(e)
        if allow_peer_missing and isinstance(mapped, PeerIdInvalid):
            return None
        raise mapped from e


def _coerce_markup(markup):
    """يحوّل أي markup من طبقة compat إلى كائن aiogram 3.x أصلي.

    InlineKeyboardMarkup/InlineKeyboardButton يرثان من aiogram أصلاً، لكن
    ReplyKeyboardMarkup/KeyboardButton هما غلافان مخصصان لا يفهمهما aiogram
    عند الإرسال (ValidationError: Input should be a valid dictionary or
    instance of InlineKeyboardMarkup/ReplyKeyboardMarkup). هنا نستدعي to_python()
    لأي غلاف يملكها قبل تمريره إلى Bot API.

    fix NEW-1: كذلك نحوّل أي dict خام ({"inline_keyboard": [[{"text": ...}]]})
    إلى InlineKeyboardMarkup حقيقي، وأي زر dict بلا callback_data/url/user_id
    يحصل على callback_data افتراضية — حتى لا يصل Bot API زر نصي عارٍ
    (BadRequest: Text buttons are unallowed in the inline keyboard).
    """
    if markup is None:
        return None
    to_py = getattr(markup, "to_python", None)
    if callable(to_py):
        try:
            return to_py()
        except Exception:
            return markup
    if isinstance(markup, dict):
        rows = markup.get("inline_keyboard")
        if rows is None and "keyboard" in markup:
            return markup
        if rows is not None:
            from aiogram.types import InlineKeyboardMarkup as AioIKM
            try:
                norm_rows = []
                for row in rows:
                    norm_row = []
                    if not isinstance(row, (list, tuple)):
                        row = [row]
                    for b in row:
                        if isinstance(b, InlineKeyboardButton):
                            norm_row.append(b)
                        elif isinstance(b, dict):
                            norm_row.append(InlineKeyboardButton(**b))
                        else:
                            norm_row.append(InlineKeyboardButton(text=str(b)))
                    norm_rows.append(norm_row)
                return AioIKM(inline_keyboard=norm_rows)
            except Exception:
                return markup
    if isinstance(markup, (list, tuple)):
        from aiogram.types import InlineKeyboardMarkup as AioIKM
        try:
            norm_rows = []
            for row in markup:
                norm_row = []
                if not isinstance(row, (list, tuple)):
                    row = [row]
                for b in row:
                    if isinstance(b, InlineKeyboardButton):
                        norm_row.append(b)
                    elif isinstance(b, dict):
                        norm_row.append(InlineKeyboardButton(**b))
                    else:
                        norm_row.append(InlineKeyboardButton(text=str(b)))
                norm_rows.append(norm_row)
            return AioIKM(inline_keyboard=norm_rows)
        except Exception:
            return markup
    return markup


def _coerce_parse_mode(pm, text: str = None, caption: str = None):
    """يقيم parse_mode: يحول ParseMode compat إلى قيمته فقط.

    IMPORTANT (fix B-2): أُزيلت heuristic تخمين HTML من وجود `<`/`>` في النص.
    كانت تتسبب في BadRequest: Unsupported start tag لأي رسالة مستخدم عادية
    تحتوي رمز مقارنة (2<3) أو رابط بصيغة <url>. aiogram لا يخمن — parse_mode
    صريح فقط، والـ DefaultBotProperties(parse_mode=HTML) في cluster.py يعالج
    النصوص التي تُرسل مع parse_mode=None كـ HTML افتراضي بأمان (لا heuristic).

    IMPORTANT (fix M-1): عند تمرير parse_mode=None صراحةً من طبقة compat،
    نعيد "HTML" بدلاً من None. السبب: aiogram يمرر parse_mode=None حرفياً إلى
    Bot API فيلغي DefaultBotProperties(parse_mode=HTML)، فتُعرض وسوم HTML
    (مثل <a href="tg://user?id=...">) كنص خام. بجعل None → "HTML" نضمن أن
    كل المنشنات تُعرض كروابط قابلة للنقر. يمكن لأي متصل تجاوز ذلك بتمرير
    parse_mode="Markdown" أو ParseMode.MARKDOWN صراحةً.
    """
    if isinstance(pm, ParseMode):
        pm = pm.value
    if pm is None:
        pm = "HTML"
    return pm


def _coerce_file_input(value):
    """يحوّل أي مسار ملف محلي (str) إلى FSInputFile تلقائياً (fix B-4).

    aiogram يفرّق: str = file_id أو URL فقط، بينما الملفات المحلية تتطلب
    FSInputFile(path). هذه الدالة تتحقق:
      - إن كان value كائناً من aiogram (FSInputFile/URLInputFile/BufferedInputFile) → يمرر كما هو.
      - إن كان str يبدأ بـ http(s):// → يمرر كرابط (URLInputFile/str).
      - إن كان str يبدو file_id (نمط ملفات Telegram: alnum قصير بلا "/" أو ".") → يمرر كما هو.
      - وإلا (مسار محلي) → FSInputFile(value).
    """
    if value is None:
        return None
    if hasattr(value, "to_python") and not isinstance(value, str):
        return value
    if not isinstance(value, str):
        return value
    v = value.strip()
    if not v:
        return value
    if v.startswith(("http://", "https://")):
        return value
    if "/" not in v and "\\" not in v and "." not in v and " " not in v and len(v) < 200:
        return value
    from aiogram.types import FSInputFile
    return FSInputFile(value)


def _coerce_media(value):
    """يطبّق _coerce_file_input على وسيط أو قائمة وسائط (send_media_group).

    كما يحوّل أغلفة compat InputMediaPhoto/Video/Audio إلى dict مقبول من aiogram
    (لأن aiogram يتطلب list[InputMedia] وليس list[dict] — سنتركها ككائنات
    Pydantic إن كانت كذلك عبر to_python).
    """
    if isinstance(value, (list, tuple)):
        out = []
        for v in value:
            to_py = getattr(v, "to_python", None)
            if callable(to_py) and not isinstance(v, dict):
                try:
                    out.append(to_py())
                    continue
                except Exception:
                    pass
            out.append(_coerce_file_input(v))
        return out
    to_py = getattr(value, "to_python", None)
    if callable(to_py) and not isinstance(value, dict):
        try:
            return to_py()
        except Exception:
            pass
    return _coerce_file_input(value)



def _chat_type_to_pyro(chat_type: str) -> ChatType:
    mapping = {
        "private": ChatType.PRIVATE,
        "group": ChatType.GROUP,
        "supergroup": ChatType.SUPERGROUP,
        "channel": ChatType.CHANNEL,
    }
    return mapping.get(chat_type, ChatType.PRIVATE)


class _MentionStr(str):
    """نص المنشن نفسه، لكن قابل للاستدعاء أيضاً.

    pyrogram الأصلي يجعل `user.mention` خاصية (property) تُستخدم بدون أقواس،
    بينما بعض أكواد هذا المشروع تستدعيها كدالة `user.mention(name, style)`.
    قبل هذا الإصلاح كانت compat.py تطبّقها كدالة فقط، فأي استخدام بدون أقواس
    (17 موضعاً في plugins/FinalMusic) كان يمرر كائن الدالة نفسه (bound method)
    بدل النص، فيظهر كنص خام <bound method ...> ويكسر HTML عند الإرسال
    (خطأ Telegram: "Unsupported start tag"). هذا الكلاس يجعل القيمة تعمل
    بالطريقتين معاً بدون كسر أي استخدام قائم بالفعل.
    """
    def __new__(cls, value, owner):
        obj = str.__new__(cls, value)
        obj._owner = owner
        return obj

    def __call__(self, name: str = None, style: str = None):
        return self._owner._build_mention(name, style)


class CompatUser:
    """غلاف حول aiogram User يوفر واجهة pyrogram-like."""

    __slots__ = ("_u", "_client")

    def __init__(self, user: Optional[AioUser], client: "CompatClient" = None):
        self._u = user
        self._client = client

    @property
    def id(self) -> int:
        return self._u.id if self._u else 0

    @property
    def is_bot(self) -> bool:
        return bool(self._u and self._u.is_bot)

    @property
    def first_name(self) -> str:
        return (self._u.first_name or "") if self._u else ""

    @property
    def last_name(self) -> str:
        return (self._u.last_name or "") if self._u else ""

    @property
    def username(self) -> Optional[str]:
        return self._u.username if self._u else None

    @property
    def language_code(self) -> Optional[str]:
        return self._u.language_code if self._u else None

    @property
    def is_premium(self) -> bool:
        return bool(self._u and self._u.is_premium)

    @property
    def is_deleted(self) -> bool:
        return False

    @property
    def photo(self):
        return None

    def _build_mention(self, name: str = None, style: str = None) -> str:
        target = name or self.first_name or "user"
        target = html.escape(str(target))
        return f'<a href="tg://user?id={self.id}">{target}</a>'

    @property
    def mention(self):
        """يعمل بدون أقواس (property، مثل pyrogram) وبأقواس أيضاً `mention(name)`
        عبر _MentionStr — راجع تعليقها أعلاه لسبب هذا التصميم."""
        return _MentionStr(self._build_mention(), self)

    @property
    def full_name(self) -> str:
        if self._u:
            return self._u.full_name
        return ""

    def __str__(self):
        return self.full_name or str(self.id)

    def __int__(self):
        return self.id

    def __eq__(self, other):
        if isinstance(other, CompatUser):
            return self.id == other.id
        try:
            return self.id == int(other)
        except (TypeError, ValueError):
            return NotImplemented

    def __hash__(self):
        return hash(self.id)

    def __bool__(self):
        return self._u is not None


class CompatChatMember:
    """غلاف حول ChatMember من aiogram (أو كائن افتراضي للقنوات)."""

    __slots__ = ("_m", "_client", "_status", "_user", "_virtual_id")

    def __init__(self, member=None, client: "CompatClient" = None, status=None, user=None, virtual_id=None):
        self._m = member
        self._client = client
        self._status = status
        self._user = user
        self._virtual_id = virtual_id

    @property
    def status(self) -> ChatMemberStatus:
        if self._status is not None:
            return self._status
        if self._m is None:
            return ChatMemberStatus.LEFT
        s = self._m.status
        if s == "creator":
            return ChatMemberStatus.OWNER
        if s == "administrator":
            return ChatMemberStatus.ADMINISTRATOR
        if s == "member":
            return ChatMemberStatus.MEMBER
        if s == "restricted":
            return ChatMemberStatus.RESTRICTED
        if s == "left":
            return ChatMemberStatus.LEFT
        if s == "kicked":
            return ChatMemberStatus.BANNED
        return ChatMemberStatus.LEFT

    @property
    def user(self) -> CompatUser:
        if self._user is not None:
            if isinstance(self._user, CompatUser):
                return self._user
            return CompatUser(self._user, self._client)
        if self._m and getattr(self._m, "user", None):
            return CompatUser(self._m.user, self._client)
        uid = self._virtual_id if self._virtual_id is not None else 0
        return CompatUser(AioUser(id=uid, is_bot=False, first_name="ChannelOwner"), self._client)

    @property
    def id(self) -> int:
        return self.user.id

    @property
    def is_member(self) -> bool:
        return self.status in (ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER)

    @property
    def can_restrict_members(self) -> bool:
        return bool(self._m and getattr(self._m, "can_restrict_members", False))

    @property
    def can_promote_members(self) -> bool:
        return bool(self._m and getattr(self._m, "can_promote_members", False))

    @property
    def can_delete_messages(self) -> bool:
        return bool(self._m and getattr(self._m, "can_delete_messages", False))

    @property
    def can_manage_chat(self) -> bool:
        return bool(self._m and getattr(self._m, "can_manage_chat", False))

    @property
    def can_manage_video_chats(self) -> bool:
        return bool(self._m and getattr(self._m, "can_manage_video_chats", False))

    @property
    def can_change_info(self) -> bool:
        return bool(self._m and getattr(self._m, "can_change_info", False))

    @property
    def can_invite_users(self) -> bool:
        return bool(self._m and getattr(self._m, "can_invite_users", False))

    @property
    def can_pin_messages(self) -> bool:
        return bool(self._m and getattr(self._m, "can_pin_messages", False))

    @property
    def can_send_messages(self) -> bool:
        return bool(self._m and getattr(self._m, "can_send_messages", False))

    @property
    def can_send_media_messages(self) -> bool:
        return bool(self._m and getattr(self._m, "can_send_media_messages", False))

    @property
    def is_anonymous(self) -> bool:
        return bool(self._m and getattr(self._m, "is_anonymous", False))

    @property
    def custom_title(self) -> Optional[str]:
        return getattr(self._m, "custom_title", None) if self._m else None

    @property
    def until_date(self):
        return getattr(self._m, "until_date", None) if self._m else None

    def __int__(self):
        return self.id

    def __eq__(self, other):
        try:
            return self.id == int(other)
        except (TypeError, ValueError):
            return NotImplemented

    def __bool__(self):
        return self._m is not None or self._virtual_id is not None


class CompatChat:
    """غلاف حول aiogram Chat يوفر إدارة الأعضاء والرسائل."""

    __slots__ = ("_chat", "_client")

    def __init__(self, chat: Optional[AioChat], client: "CompatClient" = None):
        self._chat = chat
        self._client = client

    @property
    def id(self) -> int:
        return self._chat.id if self._chat else 0

    @property
    def type(self) -> ChatType:
        if self._chat is None:
            return ChatType.PRIVATE
        return _chat_type_to_pyro(self._chat.type)

    @property
    def title(self) -> Optional[str]:
        return self._chat.title if self._chat else None

    @property
    def username(self) -> Optional[str]:
        return self._chat.username if self._chat else None

    @property
    def first_name(self) -> Optional[str]:
        return self._chat.first_name if self._chat else None

    @property
    def last_name(self) -> Optional[str]:
        return self._chat.last_name if self._chat else None

    @property
    def description(self) -> Optional[str]:
        return self._chat.description if self._chat else None

    @property
    def bio(self) -> Optional[str]:
        return self._chat.bio if self._chat else None

    @property
    def invite_link(self) -> Optional[str]:
        return self._chat.invite_link if self._chat else None

    @property
    def linked_chat(self):
        return self._chat.linked_chat if self._chat else None

    @property
    def members_count(self) -> Optional[int]:
        return getattr(self._chat, "member_count", None) if self._chat else None

    @property
    def photo(self):
        return getattr(self._chat, "photo", None) if self._chat else None

    @property
    def permissions(self):
        return getattr(self._chat, "permissions", None) if self._chat else None

    # ===== الخواص الجديدة المضافة لدعم ميزات Telegram الحديثة =====
    @property
    def rating(self):
        """مستوى حساب المستخدم (خاصية جديدة في Bot API 10.1)."""
        return getattr(self._chat, 'rating', None) if self._chat else None
    
    @property
    def active_usernames(self):
        """قائمة بكل اليوزرات النشطة للمستخدم (خاصية جديدة في Bot API)."""
        return getattr(self._chat, 'active_usernames', None) if self._chat else None
    
    @property
    def member_count(self):
        """عدد أعضاء المجموعة."""
        return getattr(self._chat, 'member_count', None) if self._chat else None
    
    async def get_member(self, user_id: int) -> CompatChatMember:
        try:
            member = await self._client.bot.get_chat_member(self.id, int(user_id))
            return CompatChatMember(member, self._client)
        except Exception as e:
            mapped = _map_exception(e)
            if str(user_id).startswith("-") or user_id == self.id:
                return CompatChatMember(None, self._client, status=ChatMemberStatus.OWNER,
                                        user=AioUser(id=int(user_id), is_bot=False, first_name="ChannelOwner"),
                                        virtual_id=int(user_id))
            raise mapped

    async def get_members(self, *args, **kwargs):
        """إعادة تصميم aiogram-native لـ Pyrogram Chat.get_members.

        Bot API لا يوفر تعداد كل الأعضاء — يوفر getChatAdministrators فقط.
        المشروع يستخدم get_members(filter=ADMINISTRATORS) و get_members(limit=N)
        (للمنشن). الحالتان غير ممكنتين فعلياً عبر Bot API لكامل الأعضاء، لذا:
          - filter=ADMINISTRATORS → get_chat_administrators (متاح فعلياً)
          - filter=BOTS/BANNED/limit=N → استثناء واضح يوجّه لإعادة التصميم.
        نعيد async generator حقيقي (مطابق لنمط Pyrogram).
        """
        flt = kwargs.get("filter", None)
        limit = kwargs.get("limit", None)
        if flt is not None and flt != ChatMembersFilter.ADMINISTRATORS:
            raise NotImplementedError(
                f"chat.get_members(filter={flt!r}) غير متاحة عبر Bot API — "
                "يمكن جلب المشرفين فقط (get_chat_administrators) أو عضو واحد (get_chat_member)."
            )
        try:
            members = await _safe_call(self._client.bot.get_chat_administrators(self.id))
        except Exception as e:
            raise _map_exception(e) from e
        if not members:
            return
        count = 0
        for m in members:
            if limit is not None and count >= limit:
                break
            yield CompatChatMember(m, self._client)
            count += 1

    async def get_administrators(self):
        """يرجع async generator لقائمة المشرفين (get_chat_administrators)."""
        try:
            members = await _safe_call(self._client.bot.get_chat_administrators(self.id))
        except Exception as e:
            raise _map_exception(e) from e
        if not members:
            return
        for m in members:
            yield CompatChatMember(m, self._client)

    async def get_member_count(self) -> int:
        chat = await _safe_call(self._client.bot.get_chat(self.id))
        return getattr(chat, "member_count", 0) or 0

    async def ban_member(self, user_id: int, until_date=None, revoke_messages: bool = False) -> bool:
        await _safe_call(self._client.bot.ban_chat_member(self.id, int(user_id),
                                                          revoke_messages=revoke_messages))
        return True

    async def unban_member(self, user_id: int) -> bool:
        await _safe_call(self._client.bot.unban_chat_member(self.id, int(user_id)))
        return True

    async def restrict_member(self, user_id: int, permissions, until_date=None) -> bool:
        perms = permissions
        if isinstance(permissions, dict):
            perms = AioChatPermissions(**permissions)
        await _safe_call(self._client.bot.restrict_chat_member(self.id, int(user_id), perms,
                                                               until_date=until_date))
        return True

    async def promote_member(self, user_id: int, **privileges) -> bool:
        priv = privileges
        if isinstance(priv.get("privileges"), ChatPrivileges):
            priv = priv["privileges"].to_kwargs()
        await _safe_call(self._client.bot.promote_chat_member(self.id, int(user_id), **priv))
        return True

    async def set_administrator_title(self, user_id: int, title: str) -> bool:
        await _safe_call(self._client.bot.set_chat_administrator_custom_title(self.id, int(user_id), title))
        return True

    async def delete(self) -> bool:
        await _safe_call(self._client.bot.delete_chat(self.id))
        return True

    async def leave(self) -> bool:
        await _safe_call(self._client.bot.leave_chat(self.id))
        return True

    async def export_invite_link(self) -> str:
        return await _safe_call(self._client.bot.export_chat_invite_link(self.id))

    async def create_invite_link(self, **kwargs) -> str:
        link = await _safe_call(self._client.bot.create_chat_invite_link(self.id, **kwargs))
        return link.invite_link

    async def revoke_invite_link(self, link: str) -> bool:
        await _safe_call(self._client.bot.revoke_chat_invite_link(self.id, link))
        return True

    async def pin_message(self, message_id: int, disable_notification: bool = False) -> bool:
        await _safe_call(self._client.bot.pin_chat_message(self.id, int(message_id),
                                                           disable_notification=disable_notification))
        return True

    async def unpin_message(self, message_id: int = None) -> bool:
        await _safe_call(self._client.bot.unpin_chat_message(self.id, message_id=int(message_id) if message_id else None))
        return True

    async def unpin_all_messages(self) -> bool:
        await _safe_call(self._client.bot.unpin_all_chat_messages(self.id))
        return True

    async def set_title(self, title: str) -> bool:
        await _safe_call(self._client.bot.set_chat_title(self.id, title))
        return True

    async def set_description(self, description: str) -> bool:
        await _safe_call(self._client.bot.set_chat_description(self.id, description))
        return True

    async def set_photo(self, photo) -> bool:
        await _safe_call(self._client.bot.set_chat_photo(self.id, photo))
        return True

    async def send_message(self, text: str, *args, **kwargs) -> "CompatMessage":
        return await self._client.send_message(self.id, text, *args, **kwargs)

    def __int__(self):
        return self.id

    def __eq__(self, other):
        try:
            return self.id == int(other)
        except (TypeError, ValueError):
            return NotImplemented

    def __hash__(self):
        return hash(self.id)

    def __bool__(self):
        return self._chat is not None


class CompatEntity:
    """غلاف حول MessageEntity من aiogram."""

    __slots__ = ("_e", "_text")

    def __init__(self, entity: AioMessageEntity, text: Optional[str] = None):
        self._e = entity
        self._text = text

    @property
    def type(self) -> MessageEntityType:
        t = self._e.type
        mapping = {
            "mention": MessageEntityType.MENTION,
            "hashtag": MessageEntityType.HASHTAG,
            "cashtag": MessageEntityType.CASHTAG,
            "bot_command": MessageEntityType.BOT_COMMAND,
            "url": MessageEntityType.URL,
            "email": MessageEntityType.EMAIL,
            "phone_number": MessageEntityType.PHONE_NUMBER,
            "bold": MessageEntityType.BOLD,
            "italic": MessageEntityType.ITALIC,
            "underline": MessageEntityType.UNDERLINE,
            "strikethrough": MessageEntityType.STRIKETHROUGH,
            "spoiler": MessageEntityType.SPOILER,
            "code": MessageEntityType.CODE,
            "pre": MessageEntityType.PRE,
            "text_link": MessageEntityType.TEXT_LINK,
            "text_mention": MessageEntityType.TEXT_MENTION,
            "custom_emoji": MessageEntityType.CUSTOM_EMOJI,
        }
        return mapping.get(t, MessageEntityType.URL)

    @property
    def offset(self) -> int:
        return self._e.offset

    @property
    def length(self) -> int:
        return self._e.length

    @property
    def url(self) -> Optional[str]:
        return self._e.url

    @property
    def user(self):
        return CompatUser(self._e.user) if self._e.user else None

    @property
    def custom_emoji_id(self) -> Optional[str]:
        return self._e.custom_emoji_id

    def __getattr__(self, name):
        return getattr(self._e, name)


def _build_minimal_message(copied: Any, chat_id) -> AioMessage:
    """يبني AioMessage قياسي من نتيجة copy_message/copy_messages (MessageId).

    Bot API copyMessages لا يعيد محتوى الرسالة، فقط MessageId. لتدفق
    save_media_from_channel_by_message_link (devgames.py) نحتاج فقط:
    message_id + chat + media_group_id (للبحث عن الوسائط عبر iterate منفصل).
    """
    mid = int(getattr(copied, "message_id", 0) or 0)
    try:
        return AioMessage(
            message_id=mid,
            date=datetime.datetime.now(datetime.timezone.utc),
            chat=types.Chat(id=int(chat_id), type="private"),
        )
    except Exception:
        return AioMessage(message_id=mid, date=datetime.datetime.now(datetime.timezone.utc))


class CompatMessage:
    """الغلاف الأهم: يغلف aiogram Message ويوفر واجهة pyrogram-like (m.*)."""

    __slots__ = ("_m", "_client", "_props", "_grchk_cache", "_is_adding_mode")

    def __init__(self, message: Optional[AioMessage], client: "CompatClient" = None):
        self._m = message
        self._client = client
        self._props: Dict[str, Any] = {}
        self._grchk_cache: Optional[Dict[str, Any]] = None
        self._is_adding_mode: bool = False

    @property
    def id(self) -> int:
        return self._m.message_id if self._m else 0

    @property
    def message_id(self) -> int:
        return self.id

    @property
    def chat(self) -> CompatChat:
        if self._m is None:
            return CompatChat(None, self._client)
        return CompatChat(self._m.chat, self._client)

    @property
    def from_user(self) -> Optional[CompatUser]:
        if self._m is None:
            return None
        return CompatUser(self._m.from_user, self._client)

    @property
    def sender_chat(self) -> Optional[CompatChat]:
        if self._m is None or self._m.sender_chat is None:
            return None
        return CompatChat(self._m.sender_chat, self._client)

    @property
    def reply_to_message(self) -> Optional["CompatMessage"]:
        if self._m is None or self._m.reply_to_message is None:
            return None
        return CompatMessage(self._m.reply_to_message, self._client)

    @property
    def date(self):
        return self._m.date if self._m else None

    @property
    def edit_date(self):
        return self._m.edit_date if self._m else None

    @property
    def text(self) -> str:
        return self._m.text if (self._m and self._m.text is not None) else ""

    @property
    def caption(self) -> Optional[str]:
        return self._m.caption if self._m else None

    @property
    def html(self) -> Optional[str]:
        """نص الرسالة بصيغة HTML (مكافئ pyrogram Message.html).

        تُستخدم مباشرة كـ m.html أو عبر m.html — وفي الحالة الأخيرة
        نعيد نصاً آمناً: إن وُجدت entities حقيقية نستخدم html_text الأصلي،
        وإلا نعيد النص الخام (لا AttributeError أبداً — fix B-7).
        """
        if self._m is None:
            return None
        try:
            if getattr(self._m, "html_text", None):
                return self._m.html_text
        except Exception:
            pass
        return self._m.text if self._m.text is not None else ""

    @property
    def markdown(self) -> Optional[str]:
        if self._m is None:
            return None
        try:
            if getattr(self._m, "md_text", None):
                return self._m.md_text
        except Exception:
            pass
        return self._m.text if self._m.text is not None else ""

    @property
    def entities(self) -> Optional[List[CompatEntity]]:
        if self._m is None or not self._m.entities:
            return None
        return [CompatEntity(e, self._m.text) for e in self._m.entities]

    @property
    def caption_entities(self) -> Optional[List[CompatEntity]]:
        if self._m is None or not self._m.caption_entities:
            return None
        return [CompatEntity(e, self._m.caption) for e in self._m.caption_entities]

    @property
    def media_group_id(self) -> Optional[str]:
        return self._m.media_group_id if self._m else None

    @property
    def link(self) -> Optional[str]:
        return self._m.get_url() if self._m else None

    @property
    def photo(self):
        if self._m is None or not self._m.photo:
            return None
        return self._m.photo[-1]

    @property
    def video(self):
        if self._m is None or not self._m.video:
            return None
        return self._m.video[-1]

    @property
    def animation(self):
        if self._m is None or not self._m.animation:
            return None
        return self._m.animation[-1]

    @property
    def audio(self):
        return self._m.audio if self._m else None

    @property
    def voice(self):
        return self._m.voice if self._m else None

    @property
    def sticker(self):
        return self._m.sticker if self._m else None

    @property
    def document(self):
        return self._m.document if self._m else None

    @property
    def video_note(self):
        return self._m.video_note if self._m else None

    @property
    def dice(self):
        return self._m.dice if self._m else None

    @property
    def contact(self):
        return self._m.contact if self._m else None

    @property
    def location(self):
        return self._m.location if self._m else None

    @property
    def venue(self):
        return self._m.venue if self._m else None

    @property
    def poll(self):
        return self._m.poll if self._m else None

    @property
    def game(self):
        return self._m.game if self._m else None

    @property
    def service(self):
        return self._m is not None and self._m.content_type == "service"

    @property
    def media(self):
        return getattr(self._m, "content_type", None)

    @property
    def new_chat_members(self) -> Optional[List[CompatUser]]:
        if self._m is None or not self._m.new_chat_members:
            return None
        return [CompatUser(u, self._client) for u in self._m.new_chat_members]

    @property
    def left_chat_member(self) -> Optional[CompatUser]:
        if self._m is None or self._m.left_chat_member is None:
            return None
        return CompatUser(self._m.left_chat_member, self._client)

    @property
    def new_chat_title(self) -> Optional[str]:
        return self._m.new_chat_title if self._m else None

    @property
    def pinned_message(self):
        if self._m is None or self._m.pinned_message is None:
            return None
        return CompatMessage(self._m.pinned_message, self._client)

    @property
    def migrate_to_chat_id(self) -> Optional[int]:
        return self._m.migrate_to_chat_id if self._m else None

    @property
    def migrate_from_chat_id(self) -> Optional[int]:
        return self._m.migrate_from_chat_id if self._m else None

    @property
    def message_thread_id(self) -> Optional[int]:
        return self._m.message_thread_id if self._m else None

    def _get_cache(self) -> Dict[str, Any]:
        return self._grchk_cache

    def _set_cache(self, value: Dict[str, Any]) -> None:
        self._grchk_cache = value

    async def reply(self, text: str = None, *args, **kwargs):
        kwargs.pop("quote", None)
        kwargs.pop("reply_to_message_id", None)
        return await self._client.send_message(self.chat.id, text, *args,
                                               reply_to_message_id=self.id, **kwargs)

    async def reply_text(self, text: str = None, *args, **kwargs):
        kwargs.pop("quote", None)
        return await self._client.send_message(self.chat.id, text, *args,
                                               reply_to_message_id=self.id, **kwargs)

    async def reply_photo(self, photo, caption: str = None, *args, **kwargs):
        kwargs.pop("quote", None)
        return await self._client.send_photo(self.chat.id, photo, caption=caption, *args,
                                             reply_to_message_id=self.id, **kwargs)

    async def reply_video(self, video, caption: str = None, *args, **kwargs):
        kwargs.pop("quote", None)
        return await self._client.send_video(self.chat.id, video, caption=caption, *args,
                                             reply_to_message_id=self.id, **kwargs)

    async def reply_animation(self, animation, caption: str = None, *args, **kwargs):
        kwargs.pop("quote", None)
        return await self._client.send_animation(self.chat.id, animation, caption=caption, *args,
                                                 reply_to_message_id=self.id, **kwargs)

    async def reply_audio(self, audio, caption: str = None, *args, **kwargs):
        kwargs.pop("quote", None)
        return await self._client.send_audio(self.chat.id, audio, caption=caption, *args,
                                             reply_to_message_id=self.id, **kwargs)

    async def reply_voice(self, voice, caption: str = None, *args, **kwargs):
        kwargs.pop("quote", None)
        return await self._client.send_voice(self.chat.id, voice, caption=caption, *args,
                                             reply_to_message_id=self.id, **kwargs)

    async def reply_document(self, document, caption: str = None, *args, **kwargs):
        kwargs.pop("quote", None)
        return await self._client.send_document(self.chat.id, document, caption=caption, *args,
                                                reply_to_message_id=self.id, **kwargs)

    async def reply_sticker(self, sticker, *args, **kwargs):
        kwargs.pop("quote", None)
        return await self._client.send_sticker(self.chat.id, sticker, *args,
                                               reply_to_message_id=self.id, **kwargs)

    async def reply_video_note(self, video_note, *args, **kwargs):
        kwargs.pop("quote", None)
        return await self._client.send_video_note(self.chat.id, video_note, *args,
                                                  reply_to_message_id=self.id, **kwargs)

    async def reply_chat_action(self, action: ChatAction):
        return await self._client.send_chat_action(self.chat.id, action)

    async def react(self, emoji, big: bool = False):
        """يضيف/يحدّث رد فعل (reaction) على الرسالة (fix B-3).

        كان m.react() غير موجود في CompatMessage فيفشل بصمت داخل
        except Exception في riyaka.py. الآن نستدعي bot.set_message_reaction
        مع لفّ الـ emoji في [ReactionTypeEmoji(emoji=...)] — aiogram يتطلب
        قائمة وليس str.
        """
        try:
            await _safe_call(self._client.bot.set_message_reaction(
                self.chat.id,
                self.id,
                reaction=[ReactionTypeEmoji(emoji=emoji)],
                is_big=big,
            ))
            return True
        except Exception as e:
            raise _map_exception(e) from e

    async def reply_media_group(self, media, *args, **kwargs):
        return await self._client.send_media_group(self.chat.id, media, *args,
                                                   reply_to_message_id=self.id, **kwargs)

    async def edit_text(self, text: str, *args, **kwargs):
        return await self._client.edit_message_text(self.chat.id, self.id, text, *args, **kwargs)

    async def edit(self, text: str, *args, **kwargs):
        return await self._client.edit_message_text(self.chat.id, self.id, text, *args, **kwargs)

    async def edit_caption(self, caption: str = None, *args, **kwargs):
        return await self._client.edit_message_caption(self.chat.id, self.id, caption=caption, *args, **kwargs)

    async def edit_media(self, media, *args, **kwargs):
        return await self._client.edit_message_media(self.chat.id, self.id, media, *args, **kwargs)

    async def edit_reply_markup(self, reply_markup=None, *args, **kwargs):
        return await self._client.edit_message_reply_markup(self.chat.id, self.id,
                                                            reply_markup=reply_markup, *args, **kwargs)

    async def delete(self, revoke: bool = True) -> bool:
        try:
            await _safe_call(self._client.bot.delete_message(self.chat.id, self.id))
            return True
        except Exception:
            return False

    async def download_media(self, file_name: str = None, in_memory: bool = False, **kwargs):
        return await self._client.download_media(self, file_name=file_name, in_memory=in_memory, **kwargs)

    async def download(self, file_name: str = None, in_memory: bool = False, **kwargs):
        """pyrogram-style alias — fix F-7: convert_and_send يستدعي rep.download(...)."""
        return await self.download_media(file_name=file_name, in_memory=in_memory, **kwargs)

    def stop_propagation(self):
        raise StopPropagation()

    def continue_propagation(self):
        raise ContinuePropagation()

    async def forward(self, chat_id: int, *args, **kwargs):
        return await self._client.forward_message(chat_id, self.chat.id, self.id, *args, **kwargs)

    async def copy(self, chat_id: int, *args, **kwargs):
        return await self._client.copy_message(chat_id, self.chat.id, self.id, *args, **kwargs)

    async def pin(self, disable_notification: bool = False) -> bool:
        await _safe_call(self._client.bot.pin_chat_message(self.chat.id, self.id,
                                                           disable_notification=disable_notification))
        return True

    async def unpin(self) -> bool:
        await _safe_call(self._client.bot.unpin_chat_message(self.chat.id, self.id))
        return True

    async def click(self, *args, **kwargs):
        raise NotImplementedError("Message.click غير مدعومة عبر Bot API")

    async def get_media_group(self) -> List["CompatMessage"]:
        try:
            msgs = await self._client.bot.get_media_group(self.chat.id, self.id)
            return [CompatMessage(m, self._client) for m in msgs]
        except Exception:
            return [self]

    @property
    def command(self) -> List[str]:
        """يستخرج الأمر من نص الرسالة كقائمة مثل Pyrogram: ["/start", "arg1", "arg2"].
        (يصلح 'Message' object has no attribute 'command' في pydantic:1042 —
        والـ plugins تستخدم m.command[1] / len(m.command) كقائمة.)"""
        if self._m is None:
            return []
        text = (self._m.text or "").replace("\n", " ")
        if not text.startswith("/"):
            return []
        parts = text.split(" ")
        if parts and "@" in parts[0]:
            parts[0] = parts[0].split("@")[0]
        return parts

    def __getattr__(self, name):
        if self._m is not None:
            try:
                return getattr(self._m, name)
            except AttributeError:
                pass
        raise AttributeError(
            f"CompatMessage has no attribute {name!r} (not implemented in aiogram compat layer)"
        )

    def __str__(self):
        return self.text or self.caption or ""

    def __bool__(self):
        return self._m is not None


class CompatCallbackQuery:
    """غلاف حول aiogram CallbackQuery (يُمرَّر باسم callback_query في الـ handlers)."""

    __slots__ = ("_cq", "_client")

    def __init__(self, cq: AioCallbackQuery, client: "CompatClient" = None):
        self._cq = cq
        self._client = client

    @property
    def id(self) -> str:
        return self._cq.id if self._cq else ""

    @property
    def data(self) -> Optional[str]:
        return self._cq.data if self._cq else None

    @property
    def from_user(self) -> CompatUser:
        return CompatUser(self._cq.from_user, self._client)

    @property
    def message(self) -> Optional[CompatMessage]:
        if self._cq is None or self._cq.message is None:
            return None
        return CompatMessage(self._cq.message, self._client)

    @property
    def inline_message_id(self) -> Optional[str]:
        return self._cq.inline_message_id if self._cq else None

    @property
    def chat_instance(self) -> Optional[str]:
        return self._cq.chat_instance if self._cq else None

    @property
    def message_id(self):
        if self.message:
            return self.message.id
        return None

    async def edit_message_text(self, text: str, *args, **kwargs):
        """تعديل نص رسالة الـ callback (نمط pyrogram edit_message_text)."""
        return await self._client.edit_message_text(self.message.chat.id, self.message.id,
                                                    text, *args, **kwargs)

    async def edit_message_caption(self, caption: str = None, *args, **kwargs):
        return await self._client.edit_message_caption(self.message.chat.id, self.message.id,
                                                       caption=caption, *args, **kwargs)

    async def edit_message_reply_markup(self, reply_markup=None, *args, **kwargs):
        return await self._client.edit_message_reply_markup(self.message.chat.id, self.message.id,
                                                            reply_markup=reply_markup, *args, **kwargs)

    async def edit_message_media(self, media, *args, **kwargs):
        return await self._client.edit_message_media(self.message.chat.id, self.message.id,
                                                     media, *args, **kwargs)

    async def delete_message(self, *args, **kwargs):
        if self.message:
            return await self.message.delete(*args, **kwargs)
        return None

    async def answer_callback_query(self, text: str = None, show_alert: bool = False):
        return await self.answer(text=text, show_alert=show_alert)

    def __getattr__(self, name):
        if self._cq is not None:
            return getattr(self._cq, name)
        raise AttributeError(f"CompatCallbackQuery has no attribute {name!r}")

    def __bool__(self):
        return self._cq is not None


class CompatInlineQuery:
    """غلاف حول aiogram InlineQuery."""

    __slots__ = ("_q", "_client")

    def __init__(self, query: AioInlineQuery, client: "CompatClient" = None):
        self._q = query
        self._client = client

    @property
    def id(self) -> str:
        return self._q.id if self._q else ""

    @property
    def query(self) -> str:
        return self._q.query if self._q else ""

    @property
    def from_user(self) -> CompatUser:
        return CompatUser(self._q.from_user, self._client)

    @property
    def offset(self) -> str:
        return self._q.offset if self._q else ""

    @property
    def chat_type(self) -> Optional[str]:
        return self._q.chat_type if self._q else None

    async def answer(self, results, cache_time: int = 300, is_personal: bool = True,
                     next_offset: str = None, **kwargs) -> bool:
        converted = []
        for r in results or []:
            to_py = getattr(r, "to_python", None)
            if callable(to_py):
                try:
                    converted.append(to_py())
                except Exception:
                    converted.append(r)
            else:
                converted.append(r)
        await _safe_call(self._q.answer(results=converted, cache_time=cache_time,
                                        is_personal=is_personal, next_offset=next_offset))
        return True

    def __getattr__(self, name):
        if self._q is not None:
            return getattr(self._q, name)
        raise AttributeError(f"CompatInlineQuery has no attribute {name!r}")


class CompatChatMemberUpdated:
    """غلاف حول aiogram ChatMemberUpdated."""

    __slots__ = ("_e", "_client")

    def __init__(self, event: AioChatMemberUpdated, client: "CompatClient" = None):
        self._e = event
        self._client = client

    @property
    def chat(self) -> CompatChat:
        return CompatChat(self._e.chat, self._client)

    @property
    def from_user(self) -> Optional[CompatUser]:
        return CompatUser(self._e.from_user, self._client) if self._e.from_user else None

    @property
    def date(self):
        return self._e.date if self._e else None

    @property
    def old_chat_member(self) -> CompatChatMember:
        return CompatChatMember(self._e.old_chat_member, self._client)

    @property
    def new_chat_member(self) -> CompatChatMember:
        return CompatChatMember(self._e.new_chat_member, self._client)

    @property
    def invite_link(self):
        return self._e.invite_link if self._e else None

    def __getattr__(self, name):
        if self._e is not None:
            return getattr(self._e, name)
        raise AttributeError(f"CompatChatMemberUpdated has no attribute {name!r}")


class CompatChatJoinRequest:
    """غلاف حول aiogram ChatJoinRequest."""

    __slots__ = ("_r", "_client")

    def __init__(self, request: AioChatJoinRequest, client: "CompatClient" = None):
        self._r = request
        self._client = client

    @property
    def chat(self) -> CompatChat:
        return CompatChat(self._r.chat, self._client)

    @property
    def from_user(self) -> CompatUser:
        return CompatUser(self._r.from_user, self._client)

    @property
    def user_chat_id(self) -> int:
        return self._r.user_chat_id

    @property
    def date(self):
        return self._r.date if self._r else None

    @property
    def bio(self) -> Optional[str]:
        return self._r.bio if self._r else None

    @property
    def invite_link(self):
        return self._r.invite_link if self._r else None

    async def approve(self) -> bool:
        await _safe_call(self._r.approve())
        return True

    async def decline(self) -> bool:
        await _safe_call(self._r.decline())
        return True

    def __getattr__(self, name):
        if self._r is not None:
            return getattr(self._r, name)
        raise AttributeError(f"CompatChatJoinRequest has no attribute {name!r}")



class CompatClient:
    """يمثل عميل البوت أمام كود الـ plugins (c في handler(c, m))."""

    def __init__(self, bot: Bot, bot_id: str = None, bot_token: str = None,
                 owner_id: int = None, redis=None, config=None, is_parent: bool = False):
        self._bot = bot
        self.bot_id = bot_id or (bot_token.split(":")[0] if bot_token else None)
        self.dev_final = self.bot_id
        self.bot_token = bot_token or (getattr(bot, "token", None) or "")
        self.owner_id = owner_id
        self.redis = redis
        self.bot_config = config
        self.is_parent = is_parent
        self.sudoers = set()
        self.sudo_filter = None
        self.bl_users = set()
        self._me = None
        self._loop = None

    @property
    def bot(self) -> Bot:
        return self._bot

    @bot.setter
    def bot(self, value: Bot) -> None:
        """Allows `app.bot = aiogram_bot` (used by entry.py) — stores the
        aiogram Bot instance in `self._bot`. Read-only usages (`c.bot.get_me()`,
        `c.bot.send_message(...)`, ...) keep working unchanged."""
        self._bot = value
        if value is not None and not self.bot_token:
            self.bot_token = getattr(value, "token", None) or ""

    @property
    def me(self) -> Optional[CompatUser]:
        if self._me is not None:
            return self._me
        return None

    def set_me(self, me) -> None:
        """Stores the bot identity (from aiogram get_me / sync_client_identity)."""
        try:
            if me is None:
                self._me = None
                return
            if isinstance(me, CompatUser):
                self._me = me
            else:
                self._me = CompatUser(me, self)
        except Exception:
            self._me = None

    @property
    def id(self) -> Optional[int]:
        if self._bot is None:
            return None
        try:
            return self._bot.id
        except Exception:
            return None

    @property
    def loop(self):
        if self._loop is not None:
            return self._loop
        try:
            return asyncio.get_running_loop()
        except RuntimeError:
            return None

    @loop.setter
    def loop(self, value):
        self._loop = value

    async def get_me(self) -> CompatUser:
        me = await _safe_call(self._bot.get_me())
        self.set_me(me)
        return self._me

    async def get_chat(self, chat_id) -> CompatChat:
        chat = await _safe_call(self._bot.get_chat(chat_id), allow_peer_missing=True)
        if chat is None:
            raise PeerIdInvalid(f"chat {chat_id} not found")
        return CompatChat(chat, self)

    async def get_users(self, user_id) -> CompatUser:
        user = await _safe_call(self._bot.get_chat(int(user_id)))
        if user is None:
            raise PeerIdInvalid(f"user {user_id} not found")
        u = user
        aio_user = AioUser(id=u.id, is_bot=bool(getattr(u, "is_bot", False)),
                           first_name=getattr(u, "first_name", "") or "",
                           last_name=getattr(u, "last_name", "") or "",
                           username=getattr(u, "username", None),
                           language_code=getattr(u, "language_code", None),
                           is_premium=bool(getattr(u, "is_premium", False)))
        return CompatUser(aio_user, self)

    async def get_chat_member(self, chat_id, user_id) -> CompatChatMember:
        member = await _safe_call(self._bot.get_chat_member(chat_id, int(user_id)))
        return CompatChatMember(member, self)

    async def get_chat_members(self, chat_id, *args, **kwargs):
        """يعيد async generator لأعضاء المحادثة (فقط المشرفين متاحين عبر Bot API)."""
        flt = kwargs.get("filter", None)
        
        # فقط ADMINISTRATORS مدعوم عبر Bot API
        if flt == ChatMembersFilter.ADMINISTRATORS:
            try:
                members = await _safe_call(self._bot.get_chat_administrators(chat_id))
                for member in members:
                    yield CompatChatMember(member, self)
            except Exception as e:
                raise _map_exception(e) from e
        else:
            # للأنواع الأخرى غير المدعومة
            raise NotImplementedError(
                f"get_chat_members(filter={flt!r}) غير متاحة عبر Bot API — "
                "يمكن جلب المشرفين فقط (ADMINISTRATORS) أو استخدام get_chat_member للحصول على عضو واحد."
            )

    async def get_chat_members_count(self, chat_id, *args, **kwargs):
        """Pyrogram-style alias: عدد أعضاء المحادثة."""
        try:
            return await self._bot.get_chat_member_count(chat_id)
        except Exception as e:
            raise _map_exception(e) from e

    async def get_messages(self, chat_id, message_ids=None, *args, **kwargs):
        """يجلب رسالة واحدة أو عدة رسائل (نمط pyrogram get_messages).

        - message_ids يمكن أن يكون int أو قائمة int.
        - BLOCKER FIX v16.1: aiogram Bot لا يملك get_messages إطلاقًا (3.20-3.30).
          نستخدم copy_messages (متاح دائمًا) — ينسخ الرسائل إلى نفس المحادثة عبر
          Bot API copyMessages ويعيد list[MessageId]. كافٍ لتدفق devgames.py الذي
          يعرض msg.photo/video/audio/voice/animation/text وmedia_group_id فقط.
        """
        try:
            if message_ids is None:
                return None
            if isinstance(message_ids, (list, tuple)):
                if not message_ids:
                    return []
                ids = [int(x) for x in message_ids]
                copied = await self._bot.copy_messages(
                    chat_id=int(chat_id),
                    from_chat_id=int(chat_id),
                    message_ids=ids,
                )
                return [CompatMessage(_build_minimal_message(c, chat_id), self) for c in copied]
            single = await self._bot.copy_message(
                chat_id=int(chat_id),
                from_chat_id=int(chat_id),
                message_id=int(message_ids),
            )
            return CompatMessage(_build_minimal_message(single, chat_id), self)
        except Exception as e:
            raise _map_exception(e) from e

    async def get_chat_photos(self, user_id, limit: int = 1):
        """يرجع async generator حقيقي (مثل Pyrogram) لصور الملف الشخصي.

        Bot API يوفر get_user_profile_photos(user_id, limit) — نتيجة من نوع
        UserProfilePhotos تحتوي .photos (قائمة قوائم PhotoSize). نغذّي
        async generator يعيد أكبر حجم (PhotoSize له file_id) لكل صورة.
        """
        try:
            profile_photos = await _safe_call(self._bot.get_user_profile_photos(int(user_id), limit=limit))
        except Exception as e:
            raise _map_exception(e) from e
        if profile_photos is None or not getattr(profile_photos, "photos", None):
            return
        for sizes in profile_photos.photos:
            if sizes:
                yield sizes[-1]

    async def get_dialogs(self, *args, **kwargs):
        raise NotImplementedError("get_dialogs غير متوفرة عبر Bot API (تحتاج MTProto).")

    async def get_history(self, chat_id, limit: int = 100, *args, **kwargs):
        try:
            msgs = await self._bot.get_chat_history(chat_id, limit=limit)
            return [CompatMessage(m, self) for m in msgs]
        except Exception as e:
            raise _map_exception(e) from e

    async def search_messages(self, *args, **kwargs):
        raise NotImplementedError("search_messages غير متوفرة عبر Bot API.")

    async def get_callback_query(self, *args, **kwargs):
        raise NotImplementedError("get_callback_query غير متوفرة عبر Bot API.")

    async def get_common_chats(self, *args, **kwargs):
        raise NotImplementedError("get_common_chats غير متوفرة عبر Bot API (تحتاج MTProto).")

    async def get_sticker_set(self, name: str):
        """aiogram-native wrapper → bot.get_sticker_set (Bot API getStickerSet)."""
        try:
            return await _safe_call(self._bot.get_sticker_set(name))
        except Exception as e:
            raise _map_exception(e) from e

    async def create_sticker_set(self, user_id, name, title, stickers, sticker_format="static", **kwargs):
        """aiogram-native wrapper → bot.create_new_sticker_set (Bot API createNewStickerSet).

        stickers: list of dicts {sticker: file_id, emoji: str}.
        """
        try:
            from aiogram.types import InputSticker
            input_stickers = []
            for st in stickers:
                input_stickers.append(InputSticker(
                    sticker=st["sticker"],
                    emoji=st.get("emoji", "\u2022"),
                    format=sticker_format,
                ))
            return await _safe_call(self._bot.create_new_sticker_set(
                user_id=int(user_id), name=name, title=title, stickers=input_stickers, **kwargs
            ))
        except Exception as e:
            raise _map_exception(e) from e

    async def send_message(self, chat_id, text: str, *args, parse_mode=None, reply_markup=None,
                           reply_to_message_id=None, disable_web_page_preview=None,
                           disable_notification=None, **kwargs):
        pm = _coerce_parse_mode(parse_mode, text=text)
        if pm == "HTML" and isinstance(text, str) and "`" in text:
            text = _htmlize_backticks(text)
        rm = _coerce_markup(reply_markup)
        try:
            msg = await self._bot.send_message(
                chat_id, text,
                parse_mode=pm,
                reply_markup=rm,
                reply_to_message_id=reply_to_message_id,
                disable_web_page_preview=disable_web_page_preview,
                disable_notification=disable_notification,
                **kwargs,
            )
            return CompatMessage(msg, self)
        except (TelegramBadRequest, BadRequest) as e:
            err_str = str(e).lower()
            if "message to be replied not found" in err_str or "reply message not found" in err_str or "message_to_be_replied_not_found" in err_str:
                msg = await self._bot.send_message(
                    chat_id, text,
                    parse_mode=pm,
                    reply_markup=rm,
                    reply_to_message_id=None,
                    disable_web_page_preview=disable_web_page_preview,
                    disable_notification=disable_notification,
                    **kwargs,
                )
                return CompatMessage(msg, self)
            if _is_entity_parse_error(e) and pm:
                # وسوم HTML فاسدة (مثال: بيانات قديمة محفوظة قبل إصلاح
                # توليد <tg-emoji>) — إعادة المحاولة كنص عادي بدل تحطّم
                # الأمر بالكامل.
                try:
                    msg = await self._bot.send_message(
                        chat_id, _strip_html_tags(text),
                        parse_mode=None,
                        reply_markup=rm,
                        reply_to_message_id=reply_to_message_id,
                        disable_web_page_preview=disable_web_page_preview,
                        disable_notification=disable_notification,
                        **kwargs,
                    )
                    return CompatMessage(msg, self)
                except Exception:
                    pass
            raise _map_exception(e) if isinstance(e, TelegramBadRequest) else e
        except Exception as e:
            raise _map_exception(e) from e



    async def send_photo(self, chat_id, photo, caption: str = None, *args, parse_mode=None,
                         reply_markup=None, reply_to_message_id=None, **kwargs):
        pm = _coerce_parse_mode(parse_mode, caption=caption)
        rm = _coerce_markup(reply_markup)
        photo = _coerce_file_input(photo)
        try:
            msg = await self._bot.send_photo(chat_id, photo, caption=caption, parse_mode=pm,
                                             reply_markup=rm,
                                             reply_to_message_id=reply_to_message_id, **kwargs)
            return CompatMessage(msg, self)
        except TelegramBadRequest as e:
            if "message to be replied not found" in str(e).lower() or "reply message not found" in str(e).lower():
                msg = await self._bot.send_photo(chat_id, photo, caption=caption, parse_mode=pm,
                                                 reply_markup=rm,
                                                 reply_to_message_id=None, **kwargs)
                return CompatMessage(msg, self)
            if _is_entity_parse_error(e) and pm:
                try:
                    msg = await self._bot.send_photo(chat_id, photo, caption=_strip_html_tags(caption), parse_mode=None,
                                                     reply_markup=rm,
                                                     reply_to_message_id=reply_to_message_id, **kwargs)
                    return CompatMessage(msg, self)
                except Exception:
                    pass
            raise _map_exception(e) from e
        except Exception as e:
            raise _map_exception(e) from e

    async def send_video(self, chat_id, video, caption: str = None, *args, parse_mode=None,
                         reply_markup=None, reply_to_message_id=None, **kwargs):
        pm = _coerce_parse_mode(parse_mode, caption=caption)
        rm = _coerce_markup(reply_markup)
        video = _coerce_file_input(video)
        try:
            msg = await self._bot.send_video(chat_id, video, caption=caption, parse_mode=pm,
                                             reply_markup=rm,
                                             reply_to_message_id=reply_to_message_id, **kwargs)
            return CompatMessage(msg, self)
        except TelegramBadRequest as e:
            if "message to be replied not found" in str(e).lower() or "reply message not found" in str(e).lower():
                msg = await self._bot.send_video(chat_id, video, caption=caption, parse_mode=pm,
                                                 reply_markup=rm,
                                                 reply_to_message_id=None, **kwargs)
                return CompatMessage(msg, self)
            if _is_entity_parse_error(e) and pm:
                try:
                    msg = await self._bot.send_video(chat_id, video, caption=_strip_html_tags(caption), parse_mode=None,
                                                     reply_markup=rm,
                                                     reply_to_message_id=reply_to_message_id, **kwargs)
                    return CompatMessage(msg, self)
                except Exception:
                    pass
            raise _map_exception(e) from e
        except Exception as e:
            raise _map_exception(e) from e

    async def send_animation(self, chat_id, animation, caption: str = None, *args, parse_mode=None,
                             reply_markup=None, reply_to_message_id=None, **kwargs):
        pm = _coerce_parse_mode(parse_mode, caption=caption)
        rm = _coerce_markup(reply_markup)
        animation = _coerce_file_input(animation)
        try:
            msg = await self._bot.send_animation(chat_id, animation, caption=caption, parse_mode=pm,
                                                 reply_markup=rm,
                                                 reply_to_message_id=reply_to_message_id, **kwargs)
            return CompatMessage(msg, self)
        except TelegramBadRequest as e:
            if "message to be replied not found" in str(e).lower() or "reply message not found" in str(e).lower():
                msg = await self._bot.send_animation(chat_id, animation, caption=caption, parse_mode=pm,
                                                     reply_markup=rm,
                                                     reply_to_message_id=None, **kwargs)
                return CompatMessage(msg, self)
            if _is_entity_parse_error(e) and pm:
                try:
                    msg = await self._bot.send_animation(chat_id, animation, caption=_strip_html_tags(caption), parse_mode=None,
                                                     reply_markup=rm,
                                                     reply_to_message_id=reply_to_message_id, **kwargs)
                    return CompatMessage(msg, self)
                except Exception:
                    pass
            raise _map_exception(e) from e
        except Exception as e:
            raise _map_exception(e) from e

    async def send_audio(self, chat_id, audio, caption: str = None, *args, parse_mode=None,
                         reply_markup=None, reply_to_message_id=None, **kwargs):
        pm = _coerce_parse_mode(parse_mode, caption=caption)
        rm = _coerce_markup(reply_markup)
        audio = _coerce_file_input(audio)
        try:
            msg = await self._bot.send_audio(chat_id, audio, caption=caption, parse_mode=pm,
                                             reply_markup=rm,
                                             reply_to_message_id=reply_to_message_id, **kwargs)
            return CompatMessage(msg, self)
        except TelegramBadRequest as e:
            if "message to be replied not found" in str(e).lower() or "reply message not found" in str(e).lower():
                msg = await self._bot.send_audio(chat_id, audio, caption=caption, parse_mode=pm,
                                                 reply_markup=rm,
                                                 reply_to_message_id=None, **kwargs)
                return CompatMessage(msg, self)
            if _is_entity_parse_error(e) and pm:
                try:
                    msg = await self._bot.send_audio(chat_id, audio, caption=_strip_html_tags(caption), parse_mode=None,
                                                     reply_markup=rm,
                                                     reply_to_message_id=reply_to_message_id, **kwargs)
                    return CompatMessage(msg, self)
                except Exception:
                    pass
            raise _map_exception(e) from e
        except Exception as e:
            raise _map_exception(e) from e

    async def send_voice(self, chat_id, voice, caption: str = None, *args, parse_mode=None,
                         reply_markup=None, reply_to_message_id=None, **kwargs):
        pm = _coerce_parse_mode(parse_mode, caption=caption)
        rm = _coerce_markup(reply_markup)
        voice = _coerce_file_input(voice)
        try:
            msg = await self._bot.send_voice(chat_id, voice, caption=caption, parse_mode=pm,
                                             reply_markup=rm,
                                             reply_to_message_id=reply_to_message_id, **kwargs)
            return CompatMessage(msg, self)
        except TelegramBadRequest as e:
            if "message to be replied not found" in str(e).lower() or "reply message not found" in str(e).lower():
                msg = await self._bot.send_voice(chat_id, voice, caption=caption, parse_mode=pm,
                                                 reply_markup=rm,
                                                 reply_to_message_id=None, **kwargs)
                return CompatMessage(msg, self)
            if _is_entity_parse_error(e) and pm:
                try:
                    msg = await self._bot.send_voice(chat_id, voice, caption=_strip_html_tags(caption), parse_mode=None,
                                                     reply_markup=rm,
                                                     reply_to_message_id=reply_to_message_id, **kwargs)
                    return CompatMessage(msg, self)
                except Exception:
                    pass
            raise _map_exception(e) from e
        except Exception as e:
            raise _map_exception(e) from e

    async def send_document(self, chat_id, document, caption: str = None, *args, parse_mode=None,
                            reply_markup=None, reply_to_message_id=None, **kwargs):
        pm = _coerce_parse_mode(parse_mode, caption=caption)
        rm = _coerce_markup(reply_markup)
        document = _coerce_file_input(document)
        try:
            msg = await self._bot.send_document(chat_id, document, caption=caption, parse_mode=pm,
                                                reply_markup=rm,
                                                reply_to_message_id=reply_to_message_id, **kwargs)
            return CompatMessage(msg, self)
        except TelegramBadRequest as e:
            if "message to be replied not found" in str(e).lower() or "reply message not found" in str(e).lower():
                msg = await self._bot.send_document(chat_id, document, caption=caption, parse_mode=pm,
                                                    reply_markup=rm,
                                                    reply_to_message_id=None, **kwargs)
                return CompatMessage(msg, self)
            if _is_entity_parse_error(e) and pm:
                try:
                    msg = await self._bot.send_document(chat_id, document, caption=_strip_html_tags(caption), parse_mode=None,
                                                     reply_markup=rm,
                                                     reply_to_message_id=reply_to_message_id, **kwargs)
                    return CompatMessage(msg, self)
                except Exception:
                    pass
            raise _map_exception(e) from e
        except Exception as e:
            raise _map_exception(e) from e

    async def send_sticker(self, chat_id, sticker, *args, reply_markup=None,
                           reply_to_message_id=None, **kwargs):
        rm = _coerce_markup(reply_markup)
        sticker = _coerce_file_input(sticker)
        try:
            msg = await self._bot.send_sticker(chat_id, sticker, reply_markup=rm,
                                               reply_to_message_id=reply_to_message_id, **kwargs)
            return CompatMessage(msg, self)
        except TelegramBadRequest as e:
            if "message to be replied not found" in str(e).lower() or "reply message not found" in str(e).lower():
                msg = await self._bot.send_sticker(chat_id, sticker, reply_markup=rm,
                                                   reply_to_message_id=None, **kwargs)
                return CompatMessage(msg, self)
            raise _map_exception(e) from e
        except Exception as e:
            raise _map_exception(e) from e

    async def send_video_note(self, chat_id, video_note, *args, reply_markup=None,
                              reply_to_message_id=None, **kwargs):
        rm = _coerce_markup(reply_markup)
        video_note = _coerce_file_input(video_note)
        try:
            msg = await self._bot.send_video_note(chat_id, video_note, reply_markup=rm,
                                                  reply_to_message_id=reply_to_message_id, **kwargs)
            return CompatMessage(msg, self)
        except TelegramBadRequest as e:
            if "message to be replied not found" in str(e).lower() or "reply message not found" in str(e).lower():
                msg = await self._bot.send_video_note(chat_id, video_note, reply_markup=rm,
                                                      reply_to_message_id=None, **kwargs)
                return CompatMessage(msg, self)
            raise _map_exception(e) from e
        except Exception as e:
            raise _map_exception(e) from e

    async def send_media_group(self, chat_id, media, *args, reply_to_message_id=None, **kwargs):
        media = _coerce_media(media)
        try:
            msgs = await self._bot.send_media_group(chat_id, media, reply_to_message_id=reply_to_message_id,
                                                    **kwargs)
            return [CompatMessage(m, self) for m in msgs]
        except TelegramBadRequest as e:
            if "message to be replied not found" in str(e).lower() or "reply message not found" in str(e).lower():
                msgs = await self._bot.send_media_group(chat_id, media, reply_to_message_id=None,
                                                        **kwargs)
                return [CompatMessage(m, self) for m in msgs]
            raise _map_exception(e) from e
        except Exception as e:
            raise _map_exception(e) from e


    async def send_chat_action(self, chat_id, action) -> bool:
        if isinstance(action, ChatAction):
            action = action.value
        try:
            await self._bot.send_chat_action(chat_id, action)
            return True
        except Exception:
            return False

    async def send_copy(self, chat_id, message: CompatMessage, *args, **kwargs):
        try:
            msg = await self._bot.copy_message(chat_id, message.chat.id, message.id, **kwargs)
            return CompatMessage(msg, self)
        except Exception as e:
            raise _map_exception(e) from e

    async def copy_message(self, chat_id, from_chat_id, message_id, *args, **kwargs):
        try:
            msg = await self._bot.copy_message(chat_id, from_chat_id, message_id, **kwargs)
            return CompatMessage(msg, self)
        except Exception as e:
            raise _map_exception(e) from e

    async def forward_message(self, chat_id, from_chat_id, message_id, *args, **kwargs):
        try:
            msg = await self._bot.forward_message(chat_id, from_chat_id, message_id, **kwargs)
            return CompatMessage(msg, self)
        except Exception as e:
            raise _map_exception(e) from e

    async def edit_message_text(self, chat_id, message_id, text: str, *args, parse_mode=None,
                                reply_markup=None, **kwargs):
        pm = _coerce_parse_mode(parse_mode, text=text)
        rm = _coerce_markup(reply_markup)
        try:
            msg = await self._bot.edit_message_text(text, chat_id=chat_id, message_id=message_id,
                                                    parse_mode=pm, reply_markup=rm, **kwargs)
            return CompatMessage(msg, self)
        except (TelegramBadRequest, BadRequest, MessageNotModified) as e:
            err_str = str(e).lower()
            if "message is not modified" in err_str:
                return None
            if _is_entity_parse_error(e) and pm:
                try:
                    msg = await self._bot.edit_message_text(_strip_html_tags(text), chat_id=chat_id,
                                                            message_id=message_id,
                                                            parse_mode=None, reply_markup=rm, **kwargs)
                    return CompatMessage(msg, self)
                except Exception:
                    pass
            raise _map_exception(e) if isinstance(e, TelegramBadRequest) else e
        except Exception as e:
            raise _map_exception(e) from e


    async def edit_message_caption(self, chat_id, message_id, caption: str = None, *args,
                                   parse_mode=None, reply_markup=None, **kwargs):
        pm = _coerce_parse_mode(parse_mode, caption=caption)
        rm = _coerce_markup(reply_markup)
        try:
            msg = await self._bot.edit_message_caption(chat_id=chat_id, message_id=message_id,
                                                       caption=caption, parse_mode=pm,
                                                       reply_markup=rm, **kwargs)
            return CompatMessage(msg, self)
        except TelegramBadRequest as e:
            if _is_entity_parse_error(e) and pm:
                try:
                    msg = await self._bot.edit_message_caption(chat_id=chat_id, message_id=message_id,
                                                               caption=_strip_html_tags(caption), parse_mode=None,
                                                               reply_markup=rm, **kwargs)
                    return CompatMessage(msg, self)
                except Exception:
                    pass
            raise _map_exception(e) from e
        except Exception as e:
            raise _map_exception(e) from e

    async def edit_message_media(self, chat_id, message_id, media, *args, reply_markup=None, **kwargs):
        rm = _coerce_markup(reply_markup)
        media = _coerce_media(media)
        try:
            msg = await self._bot.edit_message_media(media, chat_id=chat_id, message_id=message_id,
                                                     reply_markup=rm, **kwargs)
            return CompatMessage(msg, self)
        except Exception as e:
            raise _map_exception(e) from e

    async def edit_message_reply_markup(self, chat_id, message_id, reply_markup=None, *args, **kwargs):
        rm = _coerce_markup(reply_markup)
        try:
            msg = await self._bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                                            reply_markup=rm, **kwargs)
            return CompatMessage(msg, self)
        except Exception as e:
            raise _map_exception(e) from e

    async def delete_messages(self, chat_id, message_ids, revoke: bool = True) -> bool:
        try:
            if isinstance(message_ids, (list, tuple)):
                ids = [int(i) for i in message_ids]
                await self._bot.delete_messages(chat_id, ids)
            else:
                await self._bot.delete_message(chat_id, int(message_ids))
            return True
        except Exception:
            return False

    async def ban_chat_member(self, chat_id, user_id, until_date=None, revoke_messages: bool = False) -> bool:
        await _safe_call(self._bot.ban_chat_member(chat_id, int(user_id), until_date=until_date,
                                                   revoke_messages=revoke_messages))
        return True

    async def unban_chat_member(self, chat_id, user_id) -> bool:
        await _safe_call(self._bot.unban_chat_member(chat_id, int(user_id)))
        return True

    async def restrict_chat_member(self, chat_id, user_id, permissions, until_date=None) -> bool:
        perms = permissions
        if isinstance(permissions, dict):
            perms = AioChatPermissions(**permissions)
        await _safe_call(self._bot.restrict_chat_member(chat_id, int(user_id), perms, until_date=until_date))
        return True

    async def promote_chat_member(self, chat_id, user_id, **privileges) -> bool:
        priv = privileges
        if isinstance(priv.get("privileges"), ChatPrivileges):
            priv = priv["privileges"].to_kwargs()
        await _safe_call(self._bot.promote_chat_member(chat_id, int(user_id), **priv))
        return True

    async def set_administrator_title(self, chat_id, user_id, title: str) -> bool:
        await _safe_call(self._bot.set_chat_administrator_custom_title(chat_id, int(user_id), title))
        return True

    async def pin_chat_message(self, chat_id, message_id, disable_notification: bool = False) -> bool:
        await _safe_call(self._bot.pin_chat_message(chat_id, int(message_id),
                                                    disable_notification=disable_notification))
        return True

    async def unpin_chat_message(self, chat_id, message_id=None) -> bool:
        await _safe_call(self._bot.unpin_chat_message(chat_id, message_id=int(message_id) if message_id else None))
        return True

    async def unpin_all_chat_messages(self, chat_id) -> bool:
        await _safe_call(self._bot.unpin_all_chat_messages(chat_id))
        return True

    async def leave_chat(self, chat_id) -> bool:
        await _safe_call(self._bot.leave_chat(chat_id))
        return True

    async def export_chat_invite_link(self, chat_id) -> str:
        return await _safe_call(self._bot.export_chat_invite_link(chat_id))

    async def create_chat_invite_link(self, chat_id, **kwargs) -> str:
        link = await _safe_call(self._bot.create_chat_invite_link(chat_id, **kwargs))
        return link.invite_link

    async def revoke_chat_invite_link(self, chat_id, link: str) -> bool:
        await _safe_call(self._bot.revoke_chat_invite_link(chat_id, link))
        return True

    async def set_chat_title(self, chat_id, title: str) -> bool:
        await _safe_call(self._bot.set_chat_title(chat_id, title))
        return True

    async def set_chat_description(self, chat_id, description: str) -> bool:
        await _safe_call(self._bot.set_chat_description(chat_id, description))
        return True

    async def set_chat_photo(self, chat_id, photo) -> bool:
        await _safe_call(self._bot.set_chat_photo(chat_id, photo))
        return True

    async def delete_chat_photo(self, chat_id) -> bool:
        await _safe_call(self._bot.delete_chat_photo(chat_id))
        return True

    async def set_chat_permissions(self, chat_id, permissions) -> bool:
        perms = permissions
        if isinstance(permissions, dict):
            perms = AioChatPermissions(**permissions)
        await _safe_call(self._bot.set_chat_permissions(chat_id, perms))
        return True

    async def decline_chat_join_request(self, chat_id, user_id) -> bool:
        await _safe_call(self._bot.decline_chat_join_request(chat_id, int(user_id)))
        return True

    async def approve_chat_join_request(self, chat_id, user_id) -> bool:
        await _safe_call(self._bot.approve_chat_join_request(chat_id, int(user_id)))
        return True

    async def download_media(self, message_or_file_id, file_name: str = None, in_memory: bool = False,
                             block: bool = True, **kwargs):
        try:
            if isinstance(message_or_file_id, CompatMessage):
                target = message_or_file_id._m
            else:
                target = message_or_file_id
            # الإصلاح: aiogram's bot.download() يحتاج file_id (نص) أو كائن
            # وسائط فيه .file_id (Audio/Voice/Video/Document/...) — وليس
            # كائن Message كامل. كان يتم تمرير الرسالة كاملة فيرمي aiogram
            # الخطأ: "file can only be of the string or Downloadable type".
            if not isinstance(target, str) and not hasattr(target, "file_id"):
                media = (
                    getattr(target, "audio", None)
                    or getattr(target, "voice", None)
                    or getattr(target, "video", None)
                    or getattr(target, "document", None)
                    or getattr(target, "video_note", None)
                    or getattr(target, "animation", None)
                    or getattr(target, "sticker", None)
                )
                if media is None:
                    photo = getattr(target, "photo", None)
                    if photo:
                        media = photo[-1]
                if media is not None:
                    target = media
            return await self._bot.download(target, destination=file_name, in_memory=in_memory)
        except Exception as e:
            raise _map_exception(e) from e

    async def invoke(self, *args, **kwargs):
        raise NotImplementedError(
            "c.invoke(...) (MTProto raw function) غير متوفرة عبر Bot API. "
            "راجع تقرير الترحيل لقائمة الوظائف المتأثرة."
        )

    async def resolve_peer(self, *args, **kwargs):
        raise NotImplementedError(
            "c.resolve_peer(...) (MTProto raw) غير متوفرة عبر Bot API. "
            "يمكن استخدام c.get_chat / c.get_users كبديل."
        )

    async def stream_media(self, *args, **kwargs):
        raise NotImplementedError(
            "c.stream_media(...) (MTProto) غير متوفرة عبر Bot API. "
            "استخدم m.download_media / bot.download بدلاً منها."
        )

    async def listen(self, *args, **kwargs):
        raise NotImplementedError("listen غير مدعومة في هذا النظام (لا FSM تلقائي).")

    async def ask(self, *args, **kwargs):
        raise NotImplementedError("ask غير مدعومة في هذا النظام (الـ FSM يتم عبر Redis).")

    async def get_users(self, user_id):
        """يعيد معلومات مستخدم واحد عبر Bot API (fix: كان يستدعي نفسه بلا نهاية)."""
        try:
            chat = await self.get_chat(user_id)
            return CompatUser(chat._chat if isinstance(chat, CompatChat) else chat, self)
        except Exception as e:
            raise _map_exception(e) from e

    def __getattr__(self, name):
        attr = getattr(self._bot, name, None)
        if attr is not None:
            return attr
        raise AttributeError(f"CompatClient has no attribute {name!r}")

    def __bool__(self):
        return True



class _HandlerSpec:
    """وصف handler مسجّل عبر @Client.on_* في الـ plugins."""

    __slots__ = ("kind", "filter", "group", "callback")

    def __init__(self, kind: str, filter: Any, group: int, callback: Any = None):
        self.kind = kind
        self.filter = filter
        self.group = group
        self.callback = callback

    def __repr__(self):
        return f"<HandlerSpec {self.kind} group={self.group} filter={self.filter!r}>"


class Client:
    """فئة توافقية: تسجّل الـ decorators وتخزّن الـ handlers على الدوال
    (obj.handlers) بنفس الطريقة التي كان يتوقعها محمّل الـ plugins الأصلي."""

    _registry: Dict[str, List[Any]] = defaultdict(list)

    def __init__(self, *args, **kwargs):
        pass

    @classmethod
    def on_message(cls, *filters_args, **kwargs):
        def decorator(func):
            if not hasattr(func, "handlers") or not isinstance(func.handlers, list):
                func.handlers = []
            group = kwargs.get("group", 0)
            flt = _make_filter(*filters_args) if filters_args else None
            func.handlers.append(_HandlerSpec("message", flt, group, func))
            return func
        return decorator

    @classmethod
    def on_edited_message(cls, *filters_args, **kwargs):
        def decorator(func):
            if not hasattr(func, "handlers") or not isinstance(func.handlers, list):
                func.handlers = []
            group = kwargs.get("group", 0)
            flt = _make_filter(*filters_args) if filters_args else None
            func.handlers.append(_HandlerSpec("edited_message", flt, group, func))
            return func
        return decorator

    @classmethod
    def on_callback_query(cls, *filters_args, **kwargs):
        def decorator(func):
            if not hasattr(func, "handlers") or not isinstance(func.handlers, list):
                func.handlers = []
            group = kwargs.get("group", 0)
            flt = _make_filter(*filters_args) if filters_args else None
            func.handlers.append(_HandlerSpec("callback_query", flt, group, func))
            return func
        return decorator

    @classmethod
    def on_chat_member_updated(cls, *filters_args, **kwargs):
        def decorator(func):
            if not hasattr(func, "handlers") or not isinstance(func.handlers, list):
                func.handlers = []
            group = kwargs.get("group", 0)
            flt = _make_filter(*filters_args) if filters_args else None
            func.handlers.append(_HandlerSpec("chat_member_updated", flt, group, func))
            return func
        return decorator

    @classmethod
    def on_inline_query(cls, *filters_args, **kwargs):
        def decorator(func):
            if not hasattr(func, "handlers") or not isinstance(func.handlers, list):
                func.handlers = []
            group = kwargs.get("group", 0)
            flt = _make_filter(*filters_args) if filters_args else None
            func.handlers.append(_HandlerSpec("inline_query", flt, group, func))
            return func
        return decorator

    @classmethod
    def on_chat_join_request(cls, *filters_args, **kwargs):
        def decorator(func):
            if not hasattr(func, "handlers") or not isinstance(func.handlers, list):
                func.handlers = []
            group = kwargs.get("group", 0)
            flt = _make_filter(*filters_args) if filters_args else None
            func.handlers.append(_HandlerSpec("chat_join_request", flt, group, func))
            return func
        return decorator

    @classmethod
    def on_deleted_messages(cls, *filters_args, **kwargs):
        def decorator(func):
            if not hasattr(func, "handlers") or not isinstance(func.handlers, list):
                func.handlers = []
            group = kwargs.get("group", 0)
            flt = _make_filter(*filters_args) if filters_args else None
            func.handlers.append(_HandlerSpec("deleted_messages", flt, group, func))
            return func
        return decorator

    @classmethod
    def on_message_reaction(cls, *filters_args, **kwargs):
        def decorator(func):
            if not hasattr(func, "handlers") or not isinstance(func.handlers, list):
                func.handlers = []
            group = kwargs.get("group", 0)
            flt = _make_filter(*filters_args) if filters_args else None
            func.handlers.append(_HandlerSpec("message_reaction", flt, group, func))
            return func
        return decorator



class _Filter:
    """تمثيل داخلي لمركّب filters (يُبنى بـ & | ~)."""

    __slots__ = ("kind", "args", "op", "left", "right")

    def __init__(self, kind: str = "true", args: tuple = (), op: str = None,
                 left: "_Filter" = None, right: "_Filter" = None):
        self.kind = kind
        self.args = args
        self.op = op
        self.left = left
        self.right = right

    def __and__(self, other):
        other = other if isinstance(other, _Filter) else _Filter("true")
        return _Filter(op="and", left=self, right=other)

    def __rand__(self, other):
        other = other if isinstance(other, _Filter) else _Filter("true")
        return _Filter(op="and", left=other, right=self)

    def __or__(self, other):
        other = other if isinstance(other, _Filter) else _Filter("true")
        return _Filter(op="or", left=self, right=other)

    def __ror__(self, other):
        other = other if isinstance(other, _Filter) else _Filter("true")
        return _Filter(op="or", left=other, right=self)

    def __invert__(self):
        return _Filter(op="not", left=self)

    def __call__(self, *args, **kwargs):
        """يسمح بـ filters.text('كلمة') بينما filters.text كائن _Filter.

        في pyrogram: filters.text فلتر مباشر، و filters.text(pattern) يعيد
        فلتر نص بشرط. نجعل _Filter قابلاً للاستدعاء لتحقيق السلوكين معاً.
        """
        if self.kind == "text" and args:
            return _Filter("text_multi", (list(args) if len(args) > 1 else [args[0]],))
        if self.kind == "caption" and args:
            return _Filter("caption_multi", (list(args) if len(args) > 1 else [args[0]],))
        if self.kind == "command":
            return self
        if self.kind == "user":
            uids = []
            for a in args:
                if isinstance(a, (list, tuple, set)):
                    uids.extend(a)
                else:
                    uids.append(a)
            return _Filter("user", (uids,))
        if self.kind == "chat":
            cids = []
            for a in args:
                if isinstance(a, (list, tuple, set)):
                    cids.extend(a)
                else:
                    cids.append(a)
            return _Filter("chat", (cids,))
        return self

    def __repr__(self):
        if self.op:
            return f"Filter({self.op} {self.left!r} {self.right!r})"
        return f"Filter({self.kind}{self.args!r})"


class _CustomFilter(_Filter):
    """فلتر مخصص يُنفَّذ دالة (من filters.create)."""

    __slots__ = ("func", "name")

    def __init__(self, func, name: str = "CustomFilter"):
        super().__init__(kind="custom")
        self.func = func
        self.name = name

    def __repr__(self):
        return f"<CustomFilter {self.name}>"


class _FilterFactory:
    """يوفر نفس واجهة pyrogram.filters (filters.group, filters.command(...) ...)."""

    @staticmethod
    def create(func, name=None):
        """ينشئ فلتر مخصص من دالة (أسلوب pyrogram)."""
        return _CustomFilter(func, name or "CustomFilter")

    media = _Filter("media")
    outgoing = _Filter("outgoing")
    incoming = _Filter("incoming")

    @staticmethod
    def regex(pattern, flags: int = 0):
        return _Filter("regex", (pattern, flags))

    group = _Filter("group")
    private = _Filter("private")
    channel = _Filter("channel")
    text = _Filter("text")
    photo = _Filter("photo")
    video = _Filter("video")
    animation = _Filter("animation")
    audio = _Filter("audio")
    voice = _Filter("voice")
    sticker = _Filter("sticker")
    document = _Filter("document")
    reply = _Filter("reply")
    media_group = _Filter("media_group")
    dice = _Filter("dice")
    new_chat_members = _Filter("new_chat_members")
    left_chat_member = _Filter("left_chat_member")
    video_chat_started = _Filter("video_chat_started")
    video_chat_ended = _Filter("video_chat_ended")
    bot = _Filter("bot")
    me = _Filter("me")
    service = _Filter("service")
    forwarded = _Filter("forwarded")
    video_note = _Filter("video_note")
    contact = _Filter("contact")
    location = _Filter("location")
    venue = _Filter("venue")
    poll = _Filter("poll")
    game = _Filter("game")
    giveaway = _Filter("giveaway")

    @staticmethod
    def command(commands, prefixes: str = "/", case_sensitive: bool = False):
        cmds = commands if isinstance(commands, (list, tuple, set)) else [commands]
        return _Filter("command", (list(cmds), prefixes, case_sensitive))

    @staticmethod
    def regex(pattern, flags: int = 0):
        return _Filter("regex", (pattern, flags))

    @staticmethod
    def user(user_ids):
        uids = user_ids if isinstance(user_ids, (list, tuple, set)) else [user_ids]
        return _Filter("user", (list(uids),))

    @staticmethod
    def chat(chat_ids):
        cids = chat_ids if isinstance(chat_ids, (list, tuple, set)) else [chat_ids]
        return _Filter("chat", (list(cids),))

    @staticmethod
    def text_equals(text):
        return _Filter("text_equals", (text,))

    @staticmethod
    def text_startswith(prefix):
        return _Filter("text_startswith", (prefix,))

    @staticmethod
    def text_contains(text):
        return _Filter("text_contains", (text,))

    @staticmethod
    def text_endswith(suffix):
        return _Filter("text_endswith", (suffix,))

def _make_filter(*filters_args):
    """يبني _Filter من وسائط filters.args (قد تكون _Filter أو شيء آخر)."""
    if not filters_args:
        return _Filter("true")
    result = None
    for arg in filters_args:
        if isinstance(arg, _Filter):
            f = arg
        else:
            f = _Filter("true")
        result = f if result is None else (result & f)
    return result or _Filter("true")



_GROUP_CHAT_TYPES = {AioChatType.GROUP, AioChatType.SUPERGROUP}


def _as_aiogram_filter(value: Any) -> Any:
    """يحوّل أي قيمة (قد تكون bool أو None أو فلتر) إلى فلتر aiogram صالح.

    السبب: في بعض إصدارات aiogram، دمج قيمة منطقية (True/False) مع فلتر
    (خاصة ~F.x الذي يولّد _InvertFilter) عبر & يرمي:
        TypeError: unsupported operand type(s) for &: 'bool' and '_InvertFilter'
    هنا نضمن أن كل طرف من أطراف الدمج هو فلتر حقيقي وليس bool.
    """
    if value is None:
        return None
    if value is True:
        return _AlwaysTrueFilter()
    if value is False:
        return _NeverFilter()
    return value


def _compile_filter(flt: Optional[_Filter], kind: str = "message") -> Any:
    """يحول شجرة _Filter إلى filter جاهز لـ aiogram."""
    if flt is None:
        return None
    if not isinstance(flt, _Filter):
        return _as_aiogram_filter(flt)
    if flt.op == "and":
        left = _as_aiogram_filter(_compile_filter(flt.left, kind))
        right = _as_aiogram_filter(_compile_filter(flt.right, kind))
        if left is None:
            return right
        if right is None:
            return left
        if isinstance(left, bool) and isinstance(right, bool):
            return left and right
        if isinstance(left, bool):
            return and_f(_AlwaysTrueFilter() if left else _NeverFilter(), right)
        if isinstance(right, bool):
            return and_f(left, _AlwaysTrueFilter() if right else _NeverFilter())
        return and_f(left, right)
    if flt.op == "or":
        left = _as_aiogram_filter(_compile_filter(flt.left, kind))
        right = _as_aiogram_filter(_compile_filter(flt.right, kind))
        if left is None:
            return right
        if right is None:
            return left
        if isinstance(left, bool) and isinstance(right, bool):
            return left or right
        if isinstance(left, bool):
            return or_f(_AlwaysTrueFilter() if left else _NeverFilter(), right)
        if isinstance(right, bool):
            return or_f(left, _AlwaysTrueFilter() if right else _NeverFilter())
        return or_f(left, right)
    if flt.op == "not":
        inner = _as_aiogram_filter(_compile_filter(flt.left, kind))
        if inner is None:
            return None
        if isinstance(inner, bool):
            return _AlwaysTrueFilter() if not inner else _NeverFilter()
        return invert_f(inner)

    k = flt.kind
    args = flt.args

    if k == "true":
        return None
    if k == "false":
        return F.text == "__never_match__"

    if k == "custom":
        func = flt.func
        async def custom_filter(event):
            try:
                from aiogram import Bot as AioBot
                from compat import CompatMessage
                bot = getattr(event, "_bot", None)
                client = CompatClient(bot, bot_id="__filter__") if bot else None
                cm = CompatMessage(event, client)
                try:
                    sig = inspect.signature(func)
                    n_params = len([p for p in sig.parameters.values()
                                    if p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)])
                except Exception:
                    n_params = 3
                if n_params >= 3:
                    res = func(None, cm, cm)
                elif n_params == 2:
                    res = func(cm, cm)
                else:
                    res = func(cm)
                if hasattr(res, "__await__"):
                    return await res
                return res
            except Exception:
                return False
        return custom_filter

    if kind == "callback_query":
        if k == "regex":
            pattern = args[0]
            return F.data.regexp(pattern)
        if k == "user":
            uids = args[0]
            return F.from_user.id.in_(uids)
        if k == "chat":
            cids = args[0]
            return F.message.chat.id.in_(cids)
        if k == "group":
            return F.message.chat.type.in_(_GROUP_CHAT_TYPES)
        if k == "private":
            return F.message.chat.type == AioChatType.PRIVATE
        if k == "channel":
            return F.message.chat.type == AioChatType.CHANNEL
        if k == "data_startswith":
            prefix = args[0]
            return F.data.startswith(prefix)
        return None

    if kind in ("inline_query", "chat_member_updated", "chat_join_request", "deleted_messages", "message_reaction"):
        if k == "group":
            return F.chat.type.in_(_GROUP_CHAT_TYPES)
        if k == "private":
            return F.chat.type == AioChatType.PRIVATE
        if k == "channel":
            return F.chat.type == AioChatType.CHANNEL
        if k == "regex":
            if kind == "inline_query":
                pattern = args[0]
                return F.query.regexp(pattern)
            return None
        return None

    if k == "group":
        return F.chat.type.in_(_GROUP_CHAT_TYPES)
    if k == "private":
        return F.chat.type == AioChatType.PRIVATE
    if k == "channel":
        return F.chat.type == AioChatType.CHANNEL
    if k == "supergroup":
        return F.chat.type == AioChatType.SUPERGROUP
    if k == "text":
        return F.text
    if k == "text_multi":
        pats = args[0]
        return F.text.in_(pats)
    if k == "text_equals":
        return F.text == args[0]
    if k == "text_startswith":
        return F.text.startswith(args[0])
    if k == "text_contains":
        return F.text.contains(args[0])
    if k == "text_endswith":
        return F.text.endswith(args[0])
    if k == "caption":
        return F.caption
    if k == "caption_multi":
        pats = args[0]
        return F.caption.in_(pats)
    if k == "photo":
        return F.photo
    if k == "video":
        return F.video
    if k == "animation":
        return F.animation
    if k == "audio":
        return F.audio
    if k == "voice":
        return F.voice
    if k == "sticker":
        return F.sticker
    if k == "document":
        return F.document
    if k == "video_note":
        return F.video_note
    if k == "contact":
        return F.contact
    if k == "location":
        return F.location
    if k == "venue":
        return F.venue
    if k == "poll":
        return F.poll
    if k == "game":
        return F.game
    if k == "dice":
        return F.dice
    if k == "media":
        return (F.photo | F.video | F.document | F.animation | F.audio | F.voice | F.sticker | F.video_note).as_(bool)
    if k == "media_group":
        return F.media_group_id.as_(bool)
    if k == "new_chat_members":
        return F.new_chat_members.as_(bool)
    if k == "left_chat_member":
        return F.left_chat_member.as_(bool)
    if k == "video_chat_started":
        return F.video_chat_started.as_(bool)
    if k == "video_chat_ended":
        return F.video_chat_ended.as_(bool)
    if k == "outgoing" or k == "incoming":
        return _NeverFilter()
    if k == "reply":
        return F.reply_to_message
    if k == "media_group":
        return F.media_group_id
    if k == "new_chat_members":
        return F.new_chat_members
    if k == "left_chat_member":
        return F.left_chat_member
    if k == "bot":
        return F.from_user.is_bot
    if k == "me":
        return (F.from_user.id == F._bot.id) if hasattr(F, "_bot") else F.from_user.id == 0
    if k == "command":
        cmds, prefixes, case_sensitive = args
        if cmds == ["start"]:
            return CommandStart(ignore_case=not case_sensitive)
        if len(cmds) == 1:
            return Command(cmds[0], prefixes=prefixes, ignore_case=not case_sensitive)
        return Command(*cmds, prefixes=prefixes, ignore_case=not case_sensitive)
    if k == "regex":
        pattern, flags = args
        return F.text.regexp(pattern)
    if k == "user":
        uids = args[0]
        return F.from_user.id.in_(uids)
    if k == "chat":
        cids = args[0]
        return F.chat.id.in_(cids)
    if k == "via_bot":
        bots = args[0]
        return F.via_bot.id.in_(bots)
    if k == "forwarded":
        return F.forward_origin
    if k == "service":
        return F.content_type == "service"
    if k == "scheduled":
        return F.message_thread_id.is_not(None)
    if k == "pinned":
        return F.pinned_message
    if k == "from_scheduled":
        return F.is_from_offline
    return None



class InlineKeyboardMarkup(AioInlineKeyboardMarkup):
    """Pyrogram-style InlineKeyboardMarkup: يقبل inline_keyboard موضعياً (مثل Pyrogram) ويمرره كـ kwargs لـ aiogram 3.x."""

    def __init__(self, inline_keyboard=None, *args, **kwargs):
        if args and inline_keyboard is None:
            inline_keyboard = args[0]
        if inline_keyboard is None:
            inline_keyboard = []
        super().__init__(inline_keyboard=inline_keyboard, **kwargs)


import itertools as _itertools
_NOOP_BTN_COUNTER = _itertools.count(1)



class InlineKeyboardButton(AioInlineKeyboardButton):
    """Pyrogram-style InlineKeyboardButton: يقبل text/callback_data موضعياً (مثل Pyrogram) ويمررهم كـ kwargs لـ aiogram 3.x.

    fix NEW-1: أي زر inline بلا callback_data/url/user_id/web_app/login_url/switch_* يُعامل كزر نصي عارٍ
    ويرفضه Bot API (BadRequest: Text buttons are unallowed in the inline keyboard) — يظهر هذا
    تحديداً في send_photo/send_message التي تمرر reply_markup. الحل: إعطاء زر افتراضي
    callback_data="noop:<id>" بدلاً من إرسال زر نصي، فيبقى الزر تفاعلياً ولا ينهار الإرسال.
    """

    def __init__(self, text=None, *args, callback_data=None, url=None, **kwargs):
        if args:
            if text is None:
                text = args[0]
                args = args[1:]
            if args and callback_data is None:
                callback_data = args[0]
                args = args[1:]
            if args and url is None:
                url = args[0]
                args = args[1:]
        if text is None:
            raise TypeError("InlineKeyboardButton requires a text argument")

        _user_id = kwargs.pop("user_id", None)
        if _user_id is not None and url is None:
            url = f"tg://user?id={_user_id}"

        has_action = any((
            callback_data is not None,
            url is not None,
            kwargs.get("web_app") is not None,
            kwargs.get("login_url") is not None,
            kwargs.get("switch_inline_query") is not None,
            kwargs.get("switch_inline_query_current_chat") is not None,
            kwargs.get("switch_inline_query_chosen_chat") is not None,
            kwargs.get("copy_text") is not None,
            kwargs.get("callback_game") is not None,
            kwargs.get("pay") is not None,
        ))
        if not has_action:
            callback_data = f"noop:{next(_NOOP_BTN_COUNTER)}"

        super().__init__(text=text, callback_data=callback_data, url=url, **kwargs)


class ReplyKeyboardMarkup:
    """Pyrogram-style ReplyKeyboardMarkup: يقبل keyboard موضعياً (قائمة صفوف أزرار)
    ويبني AioReplyKeyboardMarkup صحيحاً لـ aiogram 3.x (كانت الفئة مذكورة في types.__all__
    لكنها غير معرّفة — يصلح NameError في devs.py:1328)."""

    def __init__(self, keyboard=None, *args, resize_keyboard=None, one_time_keyboard=None,
                 selective=None, input_field_placeholder=None, **kwargs):
        if args and keyboard is None:
            keyboard = args[0]
        if keyboard is None:
            keyboard = []
        super().__init__()
        self._kb = keyboard
        self._resize = resize_keyboard
        self._one_time = one_time_keyboard
        self._selective = selective
        self._placeholder = input_field_placeholder

    def to_python(self):
        from aiogram.types import ReplyKeyboardMarkup as AioReplyKeyboardMarkup
        from aiogram.types import KeyboardButton as AioKeyboardButton

        rows = []
        for row in self._kb:
            if isinstance(row, (list, tuple)):
                rows.append([AioKeyboardButton(text=b.text if isinstance(b, KeyboardButton) else str(b))
                             for b in row])
            else:
                b = row
                rows.append([AioKeyboardButton(text=b.text if isinstance(b, KeyboardButton) else str(b))])
        return AioReplyKeyboardMarkup(
            keyboard=rows,
            resize_keyboard=self._resize,
            one_time_keyboard=self._one_time,
            selective=self._selective,
            input_field_placeholder=self._placeholder,
        )

    def __repr__(self):
        return f"ReplyKeyboardMarkup(rows={len(self._kb)})"

    def to_python(self):
        from aiogram.types import ReplyKeyboardMarkup as AioReplyKeyboardMarkup
        from aiogram.types import KeyboardButton as AioKeyboardButton

        rows = []
        for row in self._kb:
            if isinstance(row, (list, tuple)):
                rows.append([AioKeyboardButton(text=b.text if isinstance(b, KeyboardButton) else str(b))
                             for b in row])
            else:
                b = row
                rows.append([AioKeyboardButton(text=b.text if isinstance(b, KeyboardButton) else str(b))])
        return AioReplyKeyboardMarkup(
            keyboard=rows,
            resize_keyboard=self._resize,
            one_time_keyboard=self._one_time,
            selective=self._selective,
            input_field_placeholder=self._placeholder,
        )


class KeyboardButton:
    """Pyrogram-style KeyboardButton: يقبل text موضعياً."""

    def __init__(self, text: str = None, *args, **kwargs):
        if text is None and args:
            text = args[0]
        if text is None:
            raise TypeError("KeyboardButton requires a text argument")
        self.text = text

    def __repr__(self):
        return f"KeyboardButton({self.text!r})"
ChatPermissions = AioChatPermissions
InputMediaPhoto = AioInputMediaPhoto
InputMediaVideo = AioInputMediaVideo
InputMediaAudio = AioInputMediaAudio


class InputTextMessageContent:
    """غلاف متوافق: يقبل نص الرسالة كوسيط أول (نمط Pyrogram القديم).

    aiogram يتطلب message_text= صراحةً — هذا الغلاف يحوّل
    InputTextMessageContent('text', disable_web_page_preview=True)
    إلى AioInputTextMessageContent(message_text='text', ...).
    """

    def __init__(self, message_text: str = None, *args, **kwargs):
        if isinstance(message_text, dict):
            self._content = AioInputTextMessageContent(**message_text)
        else:
            self._content = AioInputTextMessageContent(message_text=message_text, **kwargs)

    def to_python(self):
        return self._content.model_dump(exclude_none=True)

    def model_dump(self, **kw):
        return self._content.model_dump(**kw)


class InlineQueryResultArticle:
    """غلاف متوافق: يترجم توقيع Pyrogram القديم إلى aiogram.

    - يُولّد id تلقائياً عند غيابه (fix B-5).
    - يترجم thumb_url= إلى thumbnail_url=.
    - يقبل input_message_content ككائن أو dict.
    """

    def __init__(self, *args, **kwargs):
        import uuid as _uuid
        data = dict(kwargs)
        if "thumb_url" in data and "thumbnail_url" not in data:
            data["thumbnail_url"] = data.pop("thumb_url")
        if not data.get("id"):
            data["id"] = f"art_{_uuid.uuid4().hex[:16]}"
        imc = data.get("input_message_content")
        if isinstance(imc, dict):
            data["input_message_content"] = AioInputTextMessageContent(**imc)
        elif imc is not None:
            to_py = getattr(imc, "to_python", None)
            if callable(to_py):
                try:
                    data["input_message_content"] = to_py()
                except Exception:
                    data["input_message_content"] = imc
            else:
                data["input_message_content"] = imc
        self._result = AioInlineQueryResultArticle(**data)

    def to_python(self):
        return self._result.model_dump(exclude_none=True)

    def model_dump(self, **kw):
        return self._result.model_dump(**kw)

Message = AioMessage
CallbackQuery = AioCallbackQuery
User = AioUser
Chat = AioChat
ChatMember = AioChatMemberUpdated
InlineQuery = AioInlineQuery
MessageEntity = AioMessageEntity
ReactionTypeEmoji = AioReactionTypeEmoji

ChatMemberUpdated = AioChatMemberUpdated
ChatJoinRequest = AioChatJoinRequest



def _coerce_inline_imc(imc):
    """يحوّل غلاف compat InputTextMessageContent إلى dict مقبول من aiogram."""
    if imc is None:
        return None
    if isinstance(imc, dict):
        return imc
    to_py = getattr(imc, "to_python", None)
    if callable(to_py):
        try:
            return to_py()
        except Exception:
            return imc
    return imc


class InputMediaPhoto:
    """غلاف متوافق: يقبل media كوسيط أول (نمط Pyrogram) ويحوّل المسارات المحلية."""

    def __init__(self, media=None, *args, **kwargs):
        if isinstance(media, dict):
            self._media = AioInputMediaPhoto(**media)
        else:
            self._media = AioInputMediaPhoto(media=_coerce_file_input(media), **kwargs)

    def to_python(self):
        return self._media.model_dump(exclude_none=True)

    def model_dump(self, **kw):
        return self._media.model_dump(**kw)


class InputMediaVideo:
    """غلاف متوافق: يقبل media كوسيط أول (نمط Pyrogram) ويحوّل المسارات المحلية."""

    def __init__(self, media=None, *args, **kwargs):
        if isinstance(media, dict):
            self._media = AioInputMediaVideo(**media)
        else:
            self._media = AioInputMediaVideo(media=_coerce_file_input(media), **kwargs)

    def to_python(self):
        return self._media.model_dump(exclude_none=True)

    def model_dump(self, **kw):
        return self._media.model_dump(**kw)


class InputMediaAudio:
    """غلاف متوافق: يقبل media كوسيط أول (نمط Pyrogram) ويحوّل المسارات المحلية."""

    def __init__(self, media=None, *args, **kwargs):
        if isinstance(media, dict):
            self._media = AioInputMediaAudio(**media)
        else:
            self._media = AioInputMediaAudio(media=_coerce_file_input(media), **kwargs)

    def to_python(self):
        return self._media.model_dump(exclude_none=True)

    def model_dump(self, **kw):
        return self._media.model_dump(**kw)


class InlineQueryResultCachedPhoto:

    def __init__(self, photo_file_id: str, *args, **kwargs):
        self.type = "photo"
        self.photo_file_id = photo_file_id
        self.kwargs = kwargs

    def to_python(self):
        from aiogram.types import InlineQueryResultCachedPhoto as AioCachedPhoto
        return AioCachedPhoto(
            photo_file_id=self.photo_file_id,
            caption=self.kwargs.get("caption"),
            parse_mode=self.kwargs.get("parse_mode"),
            reply_markup=self.kwargs.get("reply_markup"),
            input_message_content=_coerce_inline_imc(self.kwargs.get("input_message_content")),
            id=self.kwargs.get("id"),
        ).model_dump(exclude_none=True)


class InlineQueryResultCachedVideo:
    def __init__(self, video_file_id: str, title: str = "", *args, **kwargs):
        self.type = "video"
        self.video_file_id = video_file_id
        self.title = title
        self.kwargs = kwargs

    def to_python(self):
        from aiogram.types import InlineQueryResultCachedVideo as AioCachedVideo
        return AioCachedVideo(
            video_file_id=self.video_file_id,
            title=self.title,
            caption=self.kwargs.get("caption"),
            parse_mode=self.kwargs.get("parse_mode"),
            reply_markup=self.kwargs.get("reply_markup"),
            input_message_content=_coerce_inline_imc(self.kwargs.get("input_message_content")),
            id=self.kwargs.get("id"),
        ).model_dump(exclude_none=True)


class InlineQueryResultCachedAudio:
    def __init__(self, audio_file_id: str, caption: str = None, *args, **kwargs):
        self.type = "audio"
        self.audio_file_id = audio_file_id
        self.caption = caption
        self.kwargs = kwargs

    def to_python(self):
        from aiogram.types import InlineQueryResultCachedAudio as AioCachedAudio
        return AioCachedAudio(
            audio_file_id=self.audio_file_id,
            caption=self.caption,
            parse_mode=self.kwargs.get("parse_mode"),
            reply_markup=self.kwargs.get("reply_markup"),
            input_message_content=_coerce_inline_imc(self.kwargs.get("input_message_content")),
            id=self.kwargs.get("id"),
        ).model_dump(exclude_none=True)


class InlineQueryResultCachedVoice:
    def __init__(self, voice_file_id: str, title: str = "", *args, **kwargs):
        self.type = "voice"
        self.voice_file_id = voice_file_id
        self.title = title
        self.kwargs = kwargs

    def to_python(self):
        from aiogram.types import InlineQueryResultCachedVoice as AioCachedVoice
        return AioCachedVoice(
            voice_file_id=self.voice_file_id,
            title=self.title,
            caption=self.kwargs.get("caption"),
            parse_mode=self.kwargs.get("parse_mode"),
            reply_markup=self.kwargs.get("reply_markup"),
            input_message_content=_coerce_inline_imc(self.kwargs.get("input_message_content")),
            id=self.kwargs.get("id"),
        ).model_dump(exclude_none=True)


class InlineQueryResultCachedSticker:
    def __init__(self, sticker_file_id: str, *args, **kwargs):
        self.type = "sticker"
        self.sticker_file_id = sticker_file_id
        self.kwargs = kwargs

    def to_python(self):
        from aiogram.types import InlineQueryResultCachedSticker as AioCachedSticker
        return AioCachedSticker(
            sticker_file_id=self.sticker_file_id,
            reply_markup=self.kwargs.get("reply_markup"),
            input_message_content=_coerce_inline_imc(self.kwargs.get("input_message_content")),
            id=self.kwargs.get("id"),
        ).model_dump(exclude_none=True)


class InlineQueryResultCachedAnimation:
    def __init__(self, animation_file_id: str, caption: str = None, *args, **kwargs):
        self.type = "gif"
        self.animation_file_id = animation_file_id
        self.caption = caption
        self.kwargs = kwargs

    def to_python(self):
        from aiogram.types import InlineQueryResultCachedGif as AioCachedGif
        return AioCachedGif(
            gif_file_id=self.animation_file_id,
            caption=self.caption,
            parse_mode=self.kwargs.get("parse_mode"),
            reply_markup=self.kwargs.get("reply_markup"),
            input_message_content=_coerce_inline_imc(self.kwargs.get("input_message_content")),
            id=self.kwargs.get("id"),
        ).model_dump(exclude_none=True)


InlineQueryResultCachedGif = InlineQueryResultCachedAnimation



class raw:
    """مساحة أسماء تحاكي pyrogram.raw — كل شيء هنا يرفع NotImplementedError عند الاستخدام."""

    class functions:
        class users:
            class GetFullUser:
                def __init__(self, *args, **kwargs):
                    raise NotImplementedError(
                        "GetFullUser (MTProto) غير متوفرة عبر Bot API. "
                        "تُستخدم فقط في ميزة مستوى/هدايا Telegram Stars — لا يمكن تنفيذها عبر Bot API."
                    )

        class channels:
            class GetFullChannel:
                def __init__(self, *args, **kwargs):
                    raise NotImplementedError(
                        "GetFullChannel (MTProto) غير متوفرة عبر Bot API. "
                        "استخدم bot.get_chat بدلاً منها."
                    )

        class messages:
            class GetStickerSet:
                def __init__(self, *args, **kwargs):
                    raise NotImplementedError(
                        "GetStickerSet (MTProto) غير متوفرة عبر Bot API. "
                        "استخدم bot.get_sticker_set (Bot API 8.3+) بدلاً منها."
                    )

            class CreateStickerSet:
                def __init__(self, *args, **kwargs):
                    raise NotImplementedError(
                        "CreateStickerSet (MTProto) غير متوفرة عبر Bot API. "
                        "استخدم bot.create_new_sticker_set (Bot API 8.3+) بدلاً منها."
                    )

    class types:
        class InputPeerUser:
            def __init__(self, *args, **kwargs):
                raise NotImplementedError("InputPeerUser (MTProto) غير متوفرة عبر Bot API.")


class FileType:
    PHOTO = "photo"
    VIDEO = "video"
    DOCUMENT = "document"


class ThumbnailSource:
    THUMBNAIL = 0
    CHAT_PHOTO_SMALL = 1
    CHAT_PHOTO_BIG = 2
    STICKER_SET_THUMBNAIL = 3


class FileId:
    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs

    def encode(self):
        raise NotImplementedError(
            "FileId.encode (MTProto file reference) غير متوفرة عبر Bot API. "
            "تستخدم فقط لسحب الفيديو المتحرك لصورة البروفايل — استخدم get_user_profile_photos "
            "للحصول على file_id جاهز بدلاً من بناء FileId يدوياً."
        )

    def decode(self, *args, **kwargs):
        raise NotImplementedError("FileId.decode (MTProto) غير متوفرة عبر Bot API.")


class InputStickerSetShortName:
    def __init__(self, short_name: str = None, *args, **kwargs):
        self.short_name = short_name


class InputStickerSetID:
    def __init__(self, id=None, access_hash=None, *args, **kwargs):
        self.id = id
        self.access_hash = access_hash


class InputDocument:
    def __init__(self, id=None, access_hash=None, file_reference=None, *args, **kwargs):
        self.id = id
        self.access_hash = access_hash
        self.file_reference = file_reference


class InputUser:
    def __init__(self, user_id=None, access_hash=None, *args, **kwargs):
        self.user_id = user_id
        self.access_hash = access_hash


class DocumentAttributeCustomEmoji:
    def __init__(self, *args, **kwargs):
        pass


class InputStickerSetItem:
    def __init__(self, document=None, emoji=None, *args, **kwargs):
        self.document = document
        self.emoji = emoji


class StickerSet:
    def __init__(self, short_name: str = None, title: str = None, *args, **kwargs):
        self.short_name = short_name
        self.title = title
        self.count = kwargs.get("count", 0)
        self.documents = kwargs.get("documents", [])


class GetFullUser:
    def __init__(self, id=None, *args, **kwargs):
        self.id = id


class GetFullChannel:
    def __init__(self, channel=None, *args, **kwargs):
        self.channel = channel


class GetStickerSet:
    def __init__(self, stickerset=None, hash=0, *args, **kwargs):
        self.stickerset = stickerset
        self.hash = hash


class CreateStickerSet:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs



class MessageHandler:
    """فئة توافقية — لا تُستخدم مباشرة في التسجيل (التسجيل يتم عبر router)."""

    def __init__(self, callback, filters=None):
        self.callback = callback
        self.filters = filters



async def idle():
    """يبقي العملية حية إلى أجل غير مسمى."""
    stop_event = asyncio.Event()
    await stop_event.wait()



class _NeverFilter(BaseFilter):
    """فلتر يرجع دائماً False — يُستخدم للفلاتر المستحيلة عبر Bot API (outgoing/incoming)."""
    async def __call__(self, *args, **kwargs) -> bool:
        return False


class _AlwaysTrueFilter(BaseFilter):
    """فلتر يرجع دائماً True — بديل آمن لأي قيمة True في شجرة الفلاتر."""
    async def __call__(self, *args, **kwargs) -> bool:
        return True


def build_aiogram_filter(handler_spec: _HandlerSpec) -> Any:
    """يبني filter aiogram من HandlerSpec."""
    return _compile_filter(handler_spec.filter, handler_spec.kind)


def collect_handlers(obj) -> List[_HandlerSpec]:
    """يجمع كل الـ handlers من كائن module/class (obj.handlers)."""
    handlers = []
    for attr_name in dir(obj):
        if attr_name.startswith("__") and attr_name.endswith("__"):
            continue
        try:
            attr_value = getattr(obj, attr_name)
        except Exception:
            continue
        if hasattr(attr_value, "handlers") and isinstance(attr_value.handlers, list):
            for spec in attr_value.handlers:
                if isinstance(spec, _HandlerSpec):
                    handlers.append((attr_value, spec))
    return handlers


Client = Client
filters = _FilterFactory()

idle_fn = idle


import types as _types
enums = _types.ModuleType("types")
for _enum_name in ("ChatType", "ChatMemberStatus", "ParseMode", "ChatAction",
                   "MessageEntityType", "ChatMembersFilter"):
    setattr(enums, _enum_name, globals()[_enum_name])


import types as _types
types = _types.ModuleType("types")
for _t_name in ("Message", "CallbackQuery", "User", "Chat", "ChatMember", "ChatMemberUpdated",
                "InlineQuery", "MessageEntity", "InlineKeyboardMarkup", "InlineKeyboardButton",
                "InlineQueryResultArticle", "InlineQueryResultPhoto", "InlineQueryResultVideo",
                "InlineQueryResultGif", "InlineQueryResultAudio", "InlineQueryResultCachedPhoto",
                "InlineQueryResultCachedVideo", "InlineQueryResultCachedGif", "InlineQueryResultCachedAudio",
                "InlineQueryResultCachedDocument", "InlineQueryResultCachedSticker", "InlineQueryResultCachedVoice",
                "InlineQueryResultCachedVideoNote", "InputTextMessageContent", "InputMediaPhoto",
                "InputMediaVideo", "InputMediaAudio", "InputMediaDocument", "InputMediaAnimation",
                "InputMedia", "ReplyKeyboardMarkup", "ReplyKeyboardRemove", "ForceReply",
                "KeyboardButton", "BotCommand", "Sticker", "StickerSet", "FileId", "FileType",
                "ThumbnailSource", "InputStickerSetShortName", "InputDocument", "InputUser",
                "DocumentAttributeCustomEmoji", "InlineKeyboardMarkup"):
    try:
        setattr(types, _t_name, globals()[_t_name])
    except KeyError:
        pass
types.Message = AioMessage
types.CallbackQuery = AioCallbackQuery
types.User = AioUser
types.Chat = AioChat
types.ChatMember = AioChatMemberUpdated
types.MessageEntity = AioMessageEntity


errors = _types.ModuleType("errors")
for _err_name in ("RPCError", "FloodWait", "MessageNotModified", "MessageIdInvalid",
                  "MessageDeleteForbidden", "UserNotParticipant", "ChannelInvalid",
                  "UserIsBlocked", "InputUserDeactivated", "PeerIdInvalid",
                  "ChatWriteForbidden", "MessageEmpty", "BadRequest", "Forbidden",
                  "Unauthorized", "SlowmodeInterval"):
    setattr(errors, _err_name, globals()[_err_name])
class ChatAdminRequired(Forbidden):
    pass
class ChatSendPlainForbidden(Forbidden):
    pass
class InviteRequestSent(Forbidden):
    pass
class UserAlreadyParticipant(Forbidden):
    pass
class UsernameNotOccupied(BadRequest):
    pass
class UsernameInvalid(BadRequest):
    pass
class ChatNotModified(BadRequest):
    pass
class ChatForbidden(Forbidden):
    pass
class MessageTooLong(BadRequest):
    pass
class ReplyMarkupInvalid(BadRequest):
    pass
class ButtonUrlInvalid(BadRequest):
    pass
class QueryIdInvalid(BadRequest):
    pass
class MessageAuthorRequired(BadRequest):
    pass
class MessageNotModifiedError(MessageNotModified):
    pass
for _err_name2 in ("ChatAdminRequired", "ChatSendPlainForbidden", "InviteRequestSent", "UserAlreadyParticipant", "UsernameNotOccupied",
                   "UsernameInvalid", "ChatNotModified", "ChatForbidden", "MessageTooLong",
                   "ReplyMarkupInvalid", "ButtonUrlInvalid", "QueryIdInvalid",
                   "MessageAuthorRequired", "MessageNotModifiedError"):
    setattr(errors, _err_name2, globals()[_err_name2])


__all__ = [n for n in dir() if not n.startswith("_") and n not in ("F", "AioMessage", "AioCallbackQuery", "AioUser", "AioChat", "AioChatMemberUpdated", "AioInlineQuery", "AioMessageEntity", "AioChatJoinRequest")]