
import base64
import struct
from typing import Optional, Tuple

from helpers.redis import RedisFake


def _get_api_credentials():
    """Fetch API_ID / API_HASH from the parent config (single source of truth).

    Order: current bot config (helpers.context.get_config) -> bare settings.
    Mirrors the credential source used by fm_core/userbot.py.
    """
    try:
        from helpers.context import get_config
        cfg = get_config()
        if cfg is not None:
            api_id = getattr(cfg, "API_ID", None)
            api_hash = getattr(cfg, "API_HASH", None)
            if api_id and api_hash:
                return api_id, api_hash
    except Exception:
        pass

    try:
        import settings as _bare_config
        api_id = getattr(_bare_config, "API_ID", None)
        api_hash = getattr(_bare_config, "API_HASH", None)
        if api_id and api_hash:
            return api_id, api_hash
    except Exception:
        pass

    return None, None


def _is_bot_token(session: str) -> bool:
    """A real MTProto user session string never matches the bot-token shape.

    Bot tokens look like '123456789:AAH...' (digits, colon, alnum).
    Pyrogram string sessions are base64-like (no colon + digit prefix shape),
    so this heuristic tells us whether the user pasted a bot token by mistake.
    """
    if not session:
        return False
    if ":" in session:
        parts = session.split(":")
        if parts and parts[0].isdigit():
            return True
    return False


def _diagnose_session_string(session: str) -> Optional[str]:
    """فحص أولي سريع (بدون شبكة) لشكل جلسة Pyrogram قبل تمريرها لـ Client.

    يلتقط حالة الخطأ الشائعة `struct.error: unpack requires a buffer of N bytes`
    التي تحدث داخل Pyrogram عندما تكون الجلسة منسوخة ناقصة، أو تالفة، أو
    مولّدة بمكتبة/نسخة مختلفة (مثل Telethon أو Pyrogram v1)، ويرجع رسالة
    عربية واضحة بدل ترك الاستثناء الخام يخرج كما هو.
    يرجع None إذا كان الشكل سليماً ظاهرياً (لا يضمن صحة الجلسة فعلياً — ذلك
    يُتحقق لاحقاً عبر Client.start()).
    """
    try:
        padded = session + "=" * (-len(session) % 4)
        raw = base64.urlsafe_b64decode(padded)
    except Exception:
        return (
            "الجلسة المرسلة ليست Base64 صالحاً — تأكد من نسخها كاملة دون حذف أو "
            "إضافة أي حرف (بعض التطبيقات تقص الرسائل الطويلة عند النسخ)."
        )

    if len(raw) < 32:
        return (
            "الجلسة قصيرة جداً وناقصة على الأرجح — الرجاء نسخ جلسة Pyrogram "
            "(STRING_SESSION) كاملة كما تم توليدها، وليس جزءاً منها."
        )

    return None


class AssistantManager:

    def __init__(self):
        self._assistants = {}

    async def add_assistant(self, bot_id: str, session_string: str) -> Tuple[bool, str, Optional[int]]:
        """Add an assistant user account for a bot.

        The assistant is ALWAYS a MTProto user session (STRING_SESSION) managed
        through Pyrogram — never a bot token, never aiogram Bot API. The session
        is validated by actually starting a Pyrogram client and calling get_me(),
        then stored per bot_id in the parent Redis registry.
        """
        r = RedisFake(bot_id=bot_id)

        if not session_string or not session_string.strip():
            return False, "لم يتم إرسال الجلسة", None

        session_string = session_string.strip()

        if _is_bot_token(session_string):
            return False, (
                "هذا الشكل يبدو كـ bot token وليس جلسة حساب مستخدم. "
                "الحساب المساعد يجب أن يكون حساب مستخدم عبر MTProto — أرسل STRING_SESSION (Pyrogram) وليس توكن بوت."
            ), None

        api_id, api_hash = _get_api_credentials()
        if not api_id or not api_hash:
            return False, "API_ID / API_HASH غير متوفرين في إعدادات البوت — لا يمكن تشغيل حساب مساعد MTProto", None

        diagnosis = _diagnose_session_string(session_string)
        if diagnosis:
            return False, diagnosis, None

        try:
            from pyrogram import Client

            probe = Client(
                name=f"assistant_probe_{bot_id}",
                api_id=api_id,
                api_hash=api_hash,
                session_string=session_string,
                in_memory=True,
            )
            try:
                await probe.start()
                me = probe.me
            finally:
                try:
                    await probe.stop()
                except Exception:
                    pass

            if me is None:
                return False, "تعذر الحصول على معلومات الحساب — جلسة غير صالحة", None

            await r.set(f"{bot_id}:assistant_session", session_string)
            await r.set(f"{bot_id}:assistant_id", str(me.id))
            await r.set(f"{bot_id}:assistant_username", me.username or "")
            await r.set(f"{bot_id}:has_assistant", "true")
            self._assistants[bot_id] = {
                'session': session_string,
                'user_id': me.id,
                'username': me.username
            }
            return True, f"{me.first_name} (@{me.username})", me.id

        except struct.error:
            return False, (
                "تعذر قراءة الجلسة (unpack error) — الجلسة تالفة أو ناقصة أو مولّدة "
                "بمكتبة/نسخة مختلفة عن Pyrogram (مثل Telethon أو Pyrogram v1). "
                "الرجاء توليد جلسة جديدة عبر Pyrogram (STRING_SESSION) وإرسالها كاملة."
            ), None
        except Exception as e:
            return False, str(e), None

    async def remove_assistant(self, bot_id: str) -> Tuple[bool, str]:
        r = RedisFake(bot_id=bot_id)

        await r.delete(f"{bot_id}:assistant_session")
        await r.delete(f"{bot_id}:assistant_id")
        await r.delete(f"{bot_id}:assistant_username")
        await r.delete(f"{bot_id}:has_assistant")

        if bot_id in self._assistants:
            del self._assistants[bot_id]

        return True, "تم إزالة الحساب المساعد"

    async def get_assistant(self, bot_id: str) -> Optional[dict]:
        if bot_id in self._assistants:
            return self._assistants[bot_id]

        r = RedisFake(bot_id=bot_id)
        session = await r.get(f"{bot_id}:assistant_session")
        if session:
            user_id = await r.get(f"{bot_id}:assistant_id")
            username = await r.get(f"{bot_id}:assistant_username")
            data = {
                'session': session,
                'user_id': int(user_id) if user_id else None,
                'username': username or ""
            }
            self._assistants[bot_id] = data
            return data

        return None

    async def create_assistant_client(self, bot_id: str):
        """Create and start the assistant Pyrogram client for a bot.

        The assistant is a MTProto user session — built with pyrogram.Client
        (api_id / api_hash / session_string / in_memory=True), exactly like the
        music module's fm_core/userbot.py. Returns the started client, or None
        if no assistant session is stored for this bot.
        """
        data = await self.get_assistant(bot_id)
        if not data or not data.get('session'):
            return None

        session = data['session']

        if _is_bot_token(session):
            print(f"[assistant_manager] bot_id={bot_id}: تم تخزين bot token كجلسة مساعد — يجب أن تكون جلسة مستخدم MTProto")
            return None

        api_id, api_hash = _get_api_credentials()
        if not api_id or not api_hash:
            print(f"[assistant_manager] bot_id={bot_id}: API_ID / API_HASH غير متوفرين — لا يمكن إنشاء حساب مساعد")
            return None

        try:
            from pyrogram import Client

            client = Client(
                name=f"assistant_{bot_id}",
                api_id=api_id,
                api_hash=api_hash,
                session_string=session,
                in_memory=True,
            )
            await client.start()
            return client
        except Exception as e:
            print(f"Failed to create assistant client for {bot_id}: {e}")
            return None

    async def stop_assistant(self, bot_id: str):
        if bot_id in self._assistants:
            del self._assistants[bot_id]


assistant_manager = AssistantManager()
