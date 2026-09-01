from helpers.context import get_global_r, get_global_dev, get_global_k
r = get_global_r()
Dev_FINAL = get_global_dev()
k = get_global_k()
import os
import glob
import json
import uuid
import asyncio
import requests
import logging
from compat import Client, filters
from compat import ChatAction
from compat import Message
try:
    # NOTE: compat.py does NOT re-export "InputSticker" at module level (it only
    # imports it locally inside its own create_sticker_set() method), so
    # "from compat import InputSticker" always raised ImportError and silently
    # left _InputSticker = None below. That meant to_input_sticker() below never
    # actually built a real InputSticker and always fell back to returning the
    # plain dict — which is what caused the
    # "1 validation error for InputSticker / emoji_list Field required" crash
    # downstream. Import the real aiogram type directly instead.
    from aiogram.types import InputSticker as _InputSticker
except Exception:
    _InputSticker = None
try:
    from aiogram.types import FSInputFile as _FSInputFile
except Exception:
    _FSInputFile = None
from helpers.ranks import *

logger = logging.getLogger('convert_sigha')


def _patch_aiogram_download_in_memory():
    """
    compat.py's download chain always calls Bot.download(..., in_memory=in_memory)
    (see compat.py ~line 2066), but this install's aiogram.Bot.download() doesn't
    accept that kwarg at all -> TypeError on every single download, for every
    caller, not just ours. Patching it once here at import time fixes it
    globally instead of working around it only inside this file.
    """
    try:
        from aiogram import Bot as _AiogramBot
    except Exception as e:
        logger.warning('could not import aiogram.Bot to patch download(): %s', e)
        return
    if getattr(_AiogramBot.download, '_in_memory_patched', False):
        return
    _orig_download = _AiogramBot.download

    async def _patched_download(self, *args, in_memory=None, **kwargs):
        return await _orig_download(self, *args, **kwargs)

    _patched_download._in_memory_patched = True
    _AiogramBot.download = _patched_download
    logger.info('patched aiogram.Bot.download to accept/ignore unsupported in_memory kwarg')


_patch_aiogram_download_in_memory()


def _patch_compat_message_media_props():
    """
    compat.py's CompatMessage.video and .animation properties do
    `self._m.video[-1]` / `self._m.animation[-1]` (mirroring how .photo
    correctly unwraps aiogram's list of PhotoSize). But aiogram's
    Message.video and Message.animation are each a single Video / Animation
    object, not a list — only Message.photo is a list. That mismatch crashed
    every handler that touched a video or animation message with
    "'Animation' object is not subscriptable" (and would do the same for
    video). Patch both properties once here, the same way the download()
    signature is patched above, so every caller across the bot is fixed too.
    """
    try:
        from compat import CompatMessage as _CompatMessage
    except Exception as e:
        logger.warning('could not import CompatMessage to patch video/animation: %s', e)
        return
    if getattr(_CompatMessage, '_media_props_patched', False):
        return

    def _video(self):
        return self._m.video if self._m else None

    def _animation(self):
        return self._m.animation if self._m else None

    _CompatMessage.video = property(_video)
    _CompatMessage.animation = property(_animation)
    _CompatMessage._media_props_patched = True
    logger.info('patched CompatMessage.video/.animation (were incorrectly subscripting single objects)')


_patch_compat_message_media_props()

TMP_DIR = '/tmp/convert_sigha'
os.makedirs(TMP_DIR, exist_ok=True)
for stale in glob.glob(os.path.join(TMP_DIR, '*')):
    try: os.remove(stale)
    except Exception: pass

MAX_INPUT_SIZE = 60 * 1024 * 1024
MAX_VIDEO_DURATION = 120
STICKER_DURATION = 3
STICKER_MAX_BYTES = 256 * 1024
STATIC_STICKER_MAX_BYTES = 500 * 1024
FFMPEG_TIMEOUT = 90

CONV_WORKERS = max(2, min(4, (os.cpu_count() or 2)))
_conv_queue: asyncio.Queue = asyncio.Queue()
_workers_started = False


def _ensure_workers():
    global _workers_started
    if _workers_started:
        return
    _workers_started = True
    for _ in range(CONV_WORKERS):
        asyncio.create_task(_worker_loop())


async def _worker_loop():
    while True:
        job = await _conv_queue.get()
        try:
            await job()
        except Exception:
            logger.exception('convert job crashed')
        finally:
            _conv_queue.task_done()


async def submit_job(coro_factory):
    _ensure_workers()
    loop = asyncio.get_running_loop()
    fut = loop.create_future()

    async def _run():
        try:
            res = await coro_factory()
            if not fut.done():
                fut.set_result(res)
        except Exception as e:
            if not fut.done():
                fut.set_exception(e)

    await _conv_queue.put(_run)
    return await fut


async def run_ffmpeg(cmd, timeout=FFMPEG_TIMEOUT):
    proc = await asyncio.create_subprocess_exec(
        *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    try:
        _, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
    except asyncio.TimeoutError:
        proc.kill()
        await proc.wait()
        logger.error('ffmpeg timeout after %ss: %s', timeout, ' '.join(cmd))
        raise RuntimeError(f'انتهت المهلة ({timeout}s) قبل اكتمال ffmpeg')
    if proc.returncode != 0:
        err = stderr.decode(errors='ignore').strip()
        logger.error('ffmpeg failed (rc=%s): %s\ncmd: %s', proc.returncode, err[-1500:], ' '.join(cmd))
        raise RuntimeError(err[-800:] or f'ffmpeg exited with code {proc.returncode}')


async def run_tool(cmd, timeout=FFMPEG_TIMEOUT):
    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
    except FileNotFoundError:
        logger.error('tool not found: %s', cmd[0])
        raise
    try:
        _, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
    except asyncio.TimeoutError:
        proc.kill()
        await proc.wait()
        logger.error('tool timeout after %ss: %s', timeout, ' '.join(cmd))
        raise RuntimeError(f'انتهت المهلة ({timeout}s) قبل اكتمال الأداة')
    if proc.returncode != 0:
        err = stderr.decode(errors='ignore').strip()
        logger.error('tool failed (rc=%s): %s\ncmd: %s', proc.returncode, err[-1500:], ' '.join(cmd))
        raise RuntimeError(err[-800:] or f'{cmd[0]} exited with code {proc.returncode}')


async def ffprobe_duration(path, default=0.0):
    cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
           '-of', 'json', path]
    proc = await asyncio.create_subprocess_exec(
        *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    out, _ = await proc.communicate()
    try:
        data = json.loads(out.decode(errors='ignore'))
        return float(data.get('format', {}).get('duration', default))
    except Exception:
        return default


def new_path(ext):
    return os.path.join(TMP_DIR, f'{uuid.uuid4().hex}.{ext}')


def _extract_file_id(media_msg):
    """
    aiogram's Bot.download() only accepts a file_id string or an object that
    has a .file_id attribute ("Downloadable") — never a full Message. Every
    attempt in safe_download() used to hand the whole message straight
    through (media_msg.download(...) / client.download_media(media_msg, ...)),
    which compat.py forwards as-is into Bot.download(target=<Message>, ...).
    A Message itself has no .file_id, so aiogram raised:
    "file can only be of the string or Downloadable type" on every call shape.
    Pull the actual media object's file_id out here instead.
    """
    obj = get_media_obj(media_msg)
    if isinstance(obj, (list, tuple)):
        obj = obj[-1] if obj else None
    if obj is None:
        return None
    return getattr(obj, 'file_id', None)


async def safe_download(media_msg, dest_path):
    """
    Download resilient to library-signature drift. Some installs of the
    underlying client changed download()'s kwargs (observed error:
    "Bot.download() got an unexpected keyword argument 'in_memory'"), which
    made every conversion fail at the download step. Instead of failing hard
    on the first shape, try a few call shapes and only move on when the
    failure is specifically a TypeError (signature mismatch) — any other
    error (network, permissions, etc.) is raised immediately as-is.

    The first (and normally only) attempt now downloads by file_id, since
    that's the one shape aiogram's Bot.download() actually accepts (see
    _extract_file_id). The old message-based attempts are kept as a last
    resort in case file_id extraction ever fails for an unexpected media
    type.
    """
    client = getattr(media_msg, '_client', None) or getattr(media_msg, 'client', None)
    file_id = _extract_file_id(media_msg)

    attempts = []
    if file_id and client is not None:
        attempts.append(lambda: client.download_media(file_id, file_name=dest_path))
    attempts.append(lambda: media_msg.download(file_name=dest_path))
    if client is not None:
        attempts.append(lambda: client.download_media(media_msg, file_name=dest_path))
        attempts.append(lambda: client.download_media(media_msg))
    attempts.append(lambda: media_msg.download())

    last_err = None
    for attempt in attempts:
        try:
            result = await attempt()
        except TypeError as e:
            last_err = e
            logger.warning('download attempt failed with TypeError, trying next shape: %s', e)
            continue
        if result and result != dest_path and os.path.exists(result):
            try:
                os.replace(result, dest_path)
                return dest_path
            except Exception:
                return result
        return result or dest_path
    raise last_err or RuntimeError('تعذر تحميل الملف بكل الطرق المتاحة')


def sticker_item(file_id, emoji, fmt='static'):
    """Plain, JSON-serializable representation of one pack item (safe to
    store in redis across the multi-turn merge/replace flows)."""
    return {"sticker": file_id, "format": fmt, "emoji_list": [emoji or '\u2022']}


def to_input_sticker(item):
    """
    Convert a plain dict item into a real InputSticker right before the
    create_sticker_set call. A plain dict with an 'emoji_list' key isn't
    reliably honored by every client version (observed error: InputSticker
    'emoji_list' Field required even though it was present in our dict) —
    building the real object avoids that dict-to-model conversion entirely.
    """
    if _InputSticker is not None:
        try:
            return _InputSticker(sticker=item['sticker'], format=item.get('format', 'static'),
                                  emoji_list=item.get('emoji_list') or ['\u2022'])
        except Exception as e:
            logger.warning('InputSticker construction failed, using dict as-is: %s', e)
    return item


async def create_sticker_set_safe(c, user_id, name, title, items, is_emoji_pack=False):
    """
    compat.py's Client.create_sticker_set(...) rebuilds InputSticker itself
    from each item using `emoji=st.get("emoji", ...)` and never sets
    `emoji_list` — aiogram's InputSticker requires emoji_list, so that call
    always raised "1 validation error for InputSticker / emoji_list Field
    required", no matter what we passed it. It also returns whatever
    Bot API's createNewStickerSet returns (plain `True` on success, not an
    object with a `.name` attribute), so `new_pack.name` would have crashed
    right after even once the validation error was fixed.

    It also never passed `sticker_type` at all, so Telegram always validated
    dimensions against the "regular" (512x512) rule. When rebuilding an emoji
    pack (custom-emoji stickers, which are 100x100) that mismatch is exactly
    what produced "Bad Request: STICKER_PNG_DIMENSIONS" — the files were
    valid custom-emoji stickers, just checked against the wrong size rule.

    Call the underlying aiogram Bot directly instead, with real InputSticker
    objects built via to_input_sticker(), the correct sticker_type for the
    pack kind, and return the short name we asked for (createNewStickerSet
    doesn't hand back a richer object to read it from).
    """
    bot = getattr(c, 'bot', None) or getattr(c, '_bot', None)
    if bot is None:
        raise RuntimeError('تعذر الوصول لعميل تيليجرام الأساسي لإنشاء الحزمة')
    input_stickers = [to_input_sticker(it) for it in items]
    await bot.create_new_sticker_set(
        user_id=int(user_id), name=name, title=title, stickers=input_stickers,
        sticker_type='custom_emoji' if is_emoji_pack else 'regular',
    )
    return name


def get_media_obj(rep):
    """
    NOTE: rep here is a compat.CompatMessage, not a raw aiogram Message.
    CompatMessage.photo already resolves aiogram's list of PhotoSize down to
    the single largest one (see compat.py), so rep.photo is already one
    object here — indexing it again with [-1] (an earlier fix) crashed with
    "'PhotoSize' object is not subscriptable". Use it as-is.
    """
    if not rep:
        return None
    return (rep.voice or rep.audio or rep.video or rep.animation or
            rep.sticker or rep.photo)


def is_too_large(rep):
    obj = get_media_obj(rep)
    size = getattr(obj, 'file_size', 0) or 0
    return size > MAX_INPUT_SIZE


def is_too_long(rep, limit):
    obj = rep.video or rep.animation
    dur = getattr(obj, 'duration', 0) or 0
    return dur > limit


async def encode_video_sticker(src, out):
    duration = await ffprobe_duration(src, default=STICKER_DURATION)
    duration = min(duration, STICKER_DURATION) if duration > 0 else STICKER_DURATION
    vf = 'fps=30,scale=512:512:force_original_aspect_ratio=decrease:flags=lanczos'
    target_bitrate = max(int((STICKER_MAX_BYTES * 0.85 * 8) / duration), 80_000)
    threads = str(max(1, os.cpu_count() or 2))

    async def _encode(bitrate):
        await run_ffmpeg(['ffmpeg', '-y', '-i', src, '-t', str(duration), '-an', '-vf', vf,
                           '-c:v', 'libvpx-vp9', '-b:v', str(bitrate),
                           '-deadline', 'realtime', '-cpu-used', '8',
                           '-threads', threads, '-row-mt', '1',
                           '-f', 'webm', out])

    await _encode(target_bitrate)

    if not os.path.exists(out) or os.path.getsize(out) > STICKER_MAX_BYTES:
        await _encode(int(target_bitrate * 0.55))
    if not os.path.exists(out) or os.path.getsize(out) > STICKER_MAX_BYTES:
        raise RuntimeError('تجاوز حجم الملصق المتحرك الحد المسموح حتى بعد ضغطه')


async def encode_static_sticker(src, out):
    vf = 'scale=512:512:force_original_aspect_ratio=decrease'
    for quality in (80, 55, 35, 20):
        await run_ffmpeg(['ffmpeg', '-y', '-i', src, '-vf', vf,
                           '-c:v', 'libwebp', '-quality', str(quality), '-method', '4', out])
        if os.path.exists(out) and os.path.getsize(out) <= STATIC_STICKER_MAX_BYTES:
            return
    raise RuntimeError('تجاوز حجم الملصق الحد المسموح حتى بعد ضغطه')


async def convert_and_send(rep, m, k, dl_ext, out_ext, encoder, send_func, fail_msg):
    async def job():
        if is_too_large(rep):
            return await m.reply(plugins_attachments_391(k))
        src = out = None
        try:
            src = await safe_download(rep, new_path(dl_ext))
            if not src or not os.path.exists(src):
                return await m.reply(plugins_attachments_396(k))
            out = new_path(out_ext)
            await encoder(src, out)
            if not os.path.exists(out) or os.path.getsize(out) == 0:
                raise RuntimeError('لم يتم انشاء ملف الخروج (خرج فارغ من ffmpeg)')
            await send_func(out)
        except FileNotFoundError as e:
            logger.exception('missing conversion tool: %s', e)
            await m.reply(plugins_attachments_404(k, e))
        except asyncio.TimeoutError as e:
            logger.exception('conversion timeout')
            await m.reply(plugins_attachments_407(k, fail_msg))
        except Exception as e:
            logger.exception('convert_and_send failed (%s -> %s)', dl_ext, out_ext)
            reason = str(e).strip().splitlines()[-1][:300] if str(e).strip() else e.__class__.__name__
            await m.reply(plugins_attachments_411(k, fail_msg, reason))
        finally:
            for f in (src, out):
                if f and os.path.exists(f):
                    try: os.remove(f)
                    except Exception: pass
    await submit_job(job)


@Client.on_message(filters.text & filters.group, group=31)
async def addPluginHandler(c, m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    k = await r.get(f'{Dev_FINAL}:botkey')
    await plugin_func(c, m, k)

async def plugin_func(c, m, k):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if not await check_global_restrictions(c, m, k):
        return
    text = m.text

    if text == 'التحويلات':
        convert_list = (
            '• قائمة تحويلات الصيغ •\n\n'
            '1. فويس ↤︎ بالرد على ملف mp3\n'
            '2. اوديو ↤︎ بالرد على فويس\n'
            '3. ملصق ↤︎ بالرد على صورة\n'
            '4. صورة ↤︎ بالرد على ملصق\n'
            '5. ملصق متحرك ↤︎ بالرد على فيديو\n'
            '6. متحركة ↤︎ بالرد على فيديو او ملصق متحرك\n'
            '7. وش مكتوب ↤︎ بالرد على صوره\n'
            '8. صوت ↤︎ بالرد على فيديو\n\n'

        )
        return await m.reply(plugins_attachments_449(k, convert_list))

    if text == 'تفعيل تحويل الصيغ':
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_attachments_453(k))
        if not await r.get(f'convertSigha:customPluginD:{Dev_FINAL}{m.chat.id}'):
            return await m.reply(plugins_attachments_455(k))
        await r.delete(f'convertSigha:customPluginD:{Dev_FINAL}{m.chat.id}')
        return await m.reply(plugins_attachments_457(m.from_user.mention(), k))

    if text == 'تعطيل تحويل الصيغ':
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_attachments_461(k))
        if await r.get(f'convertSigha:customPluginD:{Dev_FINAL}{m.chat.id}'):
            return await m.reply(plugins_attachments_463(k))
        await r.set(f'convertSigha:customPluginD:{Dev_FINAL}{m.chat.id}', 1)
        return await m.reply(plugins_attachments_465(m.from_user.mention(), k))

    if text == 'تفعيل استبدال الحزم':
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_attachments_469(k))
        if not await r.get(f'replacePack:disabled:{Dev_FINAL}{m.chat.id}'):
            return await m.reply(plugins_attachments_471(k))
        await r.delete(f'replacePack:disabled:{Dev_FINAL}{m.chat.id}')
        return await m.reply(plugins_attachments_473(m.from_user.mention(), k))

    if text == 'تعطيل استبدال الحزم':
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_attachments_477(k))
        if await r.get(f'replacePack:disabled:{Dev_FINAL}{m.chat.id}'):
            return await m.reply(plugins_attachments_479(k))
        await r.set(f'replacePack:disabled:{Dev_FINAL}{m.chat.id}', 1)
        return await m.reply(plugins_attachments_481(m.from_user.mention(), k))
    if await r.get(f'replacePack:disabled:{Dev_FINAL}{m.chat.id}'):
        return

    rep = m.reply_to_message
    vid = None
    if rep:
        vid = rep.video or rep.animation

    if text and text.startswith('اوديو') and rep and rep.voice:
        custom_name = text[len('اوديو'):].strip()
        safe_name = None
        if custom_name:
            safe_name = re.sub(r'[\\/:*?"<>|\n\r\t]', '', custom_name)[:64].strip() or 'مقطع صوتي'

        def _send_audio(out, _title=safe_name):
            # aiogram's Bot.send_audio() has no "file_name" parameter at all —
            # the displayed filename comes from the uploaded file object
            # itself. Passing file_name as a kwarg (the previous code) always
            # raised "Bot.send_audio() got an unexpected keyword argument
            # 'file_name'". Wrap the local path in FSInputFile with the
            # desired filename instead, and only pass the real "title" param.
            audio = out
            if _title and _FSInputFile is not None:
                audio = _FSInputFile(out, filename=f'{_title}.mp3')
            return m.reply_audio(audio, **({'title': _title} if _title else {}))

        await c.send_chat_action(m.chat.id, ChatAction.UPLOAD_AUDIO)
        await convert_and_send(
            rep, m, k, 'ogg', 'mp3',
            lambda src, out: run_ffmpeg(['ffmpeg', '-y', '-i', src, '-acodec', 'libmp3lame', '-q:a', '2', out]),
            _send_audio,
            'تعذر تحويل البصمة الى mp3'
        )
    elif text and text.startswith('اوديو') and rep and not rep.voice:
        await m.reply(plugins_attachments_516(k, k))

    if text == 'فويس' and rep and rep.audio:
        await c.send_chat_action(m.chat.id, ChatAction.RECORD_AUDIO)
        await convert_and_send(
            rep, m, k, 'mp3', 'ogg',
            lambda src, out: run_ffmpeg(['ffmpeg', '-y', '-i', src, '-c:a', 'libopus', '-b:a', '64k', '-vbr', 'on', out]),
            lambda out: m.reply_voice(out),
            'تعذر تحويل الصوت الى فويس'
        )
    elif text == 'فويس' and rep and not rep.audio:
        await m.reply(plugins_attachments_527(k))

    if text == 'ملصق' and rep and rep.photo:
        await c.send_chat_action(m.chat.id, ChatAction.CHOOSE_STICKER)
        await convert_and_send(
            rep, m, k, 'jpg', 'webp',
            encode_static_sticker,
            lambda out: m.reply_sticker(out),
            'تعذر تحويل الصورة الى ملصق'
        )
    elif text == 'ملصق' and rep and not rep.photo:
        await m.reply(plugins_attachments_538(k))

    if text == 'صورة' and rep and rep.sticker:
        await c.send_chat_action(m.chat.id, ChatAction.UPLOAD_PHOTO)
        if rep.sticker.is_animated:
            async def _tgs_frame(src, out):
                r = get_global_r()
                Dev_FINAL = get_global_dev()
                k = get_global_k()
                gif_tmp = out + '.gif'
                await run_tool(['lottie_convert.py', src, gif_tmp])
                await run_ffmpeg(['ffmpeg', '-y', '-i', gif_tmp, '-frames:v', '1', out])
                if os.path.exists(gif_tmp): os.remove(gif_tmp)
            await convert_and_send(rep, m, k, 'tgs', 'jpg', _tgs_frame,
                                     lambda out: m.reply_photo(out),
                                     'تعذر تحويل الملصق (Lottie) الى صورة، تأكد من تثبيت مكتبة lottie')
        elif rep.sticker.is_video:
            await convert_and_send(
                rep, m, k, 'webm', 'jpg',
                lambda src, out: run_ffmpeg(['ffmpeg', '-y', '-i', src, '-frames:v', '1', out]),
                lambda out: m.reply_photo(out),
                'تعذر تحويل الملصق الى صورة'
            )
        else:
            await convert_and_send(
                rep, m, k, 'webp', 'jpg',
                lambda src, out: run_ffmpeg(['ffmpeg', '-y', '-i', src, out]),
                lambda out: m.reply_photo(out),
                'تعذر تحويل الملصق الى صورة'
            )
    elif text == 'صورة' and rep and not rep.sticker:
        await m.reply(plugins_attachments_569(k))

    if text == 'ملصق متحرك' or text == 'ملصق متحركة':
        if not vid:
            return await m.reply(plugins_attachments_573(k, text))
        await c.send_chat_action(m.chat.id, ChatAction.CHOOSE_STICKER)
        await convert_and_send(
            rep, m, k, 'mp4', 'webm',
            encode_video_sticker,
            lambda out: m.reply_sticker(out),
            'تعذر تحويل الفيديو الى ملصق متحرك (تأكد ان الفيديو غير طويل جداً)'
        )

    if text == 'متحركة' and vid:
        if is_too_long(rep, MAX_VIDEO_DURATION):
            await m.reply(plugins_attachments_584(k, MAX_VIDEO_DURATION))
        else:
            await c.send_chat_action(m.chat.id, ChatAction.UPLOAD_VIDEO)
            await convert_and_send(
                rep, m, k, 'mp4', 'gif',
                lambda src, out: run_ffmpeg(['ffmpeg', '-y', '-i', src, '-vf',
                                 'fps=15,scale=480:-1:flags=lanczos,split[s0][s1];'
                                 '[s0]palettegen[p];[s1][p]paletteuse', out]),
                lambda out: m.reply_animation(out),
                'تعذر تحويل الفيديو الى متحركة'
            )
    elif text == 'متحركة' and rep and rep.sticker:
        if rep.sticker.is_video:
            await c.send_chat_action(m.chat.id, ChatAction.UPLOAD_VIDEO)
            await convert_and_send(
                rep, m, k, 'webm', 'gif',
                lambda src, out: run_ffmpeg(['ffmpeg', '-y', '-i', src, '-vf',
                                'fps=15,scale=480:-1:flags=lanczos,split[s0][s1];'
                                '[s0]palettegen[p];[s1][p]paletteuse', out]),
                lambda out: m.reply_animation(out),
                'تعذر تحويل الملصق المتحرك الى متحركة'
            )
        elif rep.sticker.is_animated:
            await c.send_chat_action(m.chat.id, ChatAction.UPLOAD_VIDEO)
            await convert_and_send(
                rep, m, k, 'tgs', 'gif',
                lambda src, out: run_tool(['lottie_convert.py', src, out]),
                lambda out: m.reply_animation(out),
                'تعذر تحويل الملصق (Lottie) الى متحركة، تأكد من تثبيت مكتبة lottie'
            )
        else:
            await m.reply(plugins_attachments_615(k))

    if text == 'صوت' and vid:
        if is_too_long(rep, MAX_VIDEO_DURATION):
            await m.reply(plugins_attachments_619(k, MAX_VIDEO_DURATION))
        else:
            await c.send_chat_action(m.chat.id, ChatAction.UPLOAD_AUDIO)
            await convert_and_send(
                rep, m, k, 'mp4', 'mp3',
                lambda src, out: run_ffmpeg(['ffmpeg', '-y', '-i', src, '-vn', '-acodec', 'libmp3lame', '-q:a', '2', out]),
                lambda out: m.reply_audio(out),
                'تعذر استخراج الصوت من الفيديو'
            )
    elif text == 'صوت' and rep and (rep.audio or rep.voice):
        await m.reply(plugins_attachments_629(k))

    elif text == 'وش مكتوب' and rep and rep.photo:
        await c.send_chat_action(m.chat.id, ChatAction.TYPING)
        photo_path = None
    
        def _call_ocr(path):
            # runs in a worker thread so the bot's event loop never blocks/freezes on this
            with open(path, 'rb') as f:
                return requests.post(
                    "https://api.ocr.space/parse/image",
                    files={"image": f},
                    data={
                        "apikey": "K87903001988957", 
                        "language": "ara",
                        "OCREngine": "3"
                    },
                    timeout=25,
                )
    
        try:
            photo_path = await safe_download(rep, new_path('jpg'))
            if not photo_path or not os.path.exists(photo_path):
                return await m.reply("اسف طفشت مابستخرج الحين تعال بعدين ")
    
            response = await asyncio.wait_for(asyncio.to_thread(_call_ocr, photo_path), timeout=30)
    
            if response.status_code != 200:
                logger.error('ocr.space returned status %s: %s', response.status_code, response.text[:500])
                return await m.reply("اسف طفشت مابستخرج الحين تعال بعدين ")
    
            data = response.json()
            if data.get('IsErroredOnProcessing', False):
                err = data.get('ErrorMessage', 'خطأ غير معروف')
                if isinstance(err, list):
                    err = '، '.join(str(x) for x in err)
                logger.error('ocr.space processing error: %s', err)
                return await m.reply("اسف طفشت مابستخرج الحين تعال بعدين ")
    
            parsed_text = data.get('ParsedResults', [{}])[0].get('ParsedText', '').strip()
    
            if not parsed_text or 'no text detected' in parsed_text.lower():
                return await m.reply(f"{k} شكله مكتوب بخط يدك \nمحتاج مترجم اثار عشان نفهم ذا.")
    
            reply_text = f'{k} المكتوب في الصورة هو :\n\n{parsed_text}'
    
            if len(reply_text) > 4000:
                parts = [reply_text[i:i+4000] for i in range(0, len(reply_text), 4000)]
                for part in parts:
                    await m.reply(part)
            else:
                await m.reply(reply_text)
    
        except asyncio.TimeoutError:
            logger.error('ocr.space request timed out')
            await m.reply("اسف طفشت مابستخرج الحين تعال بعدين ")
        except requests.exceptions.RequestException as e:
            logger.exception('ocr request failed')
            await m.reply("اسف طفشت مابستخرج الحين تعال بعدين ")
        except Exception as e:
            logger.exception('ocr handler failed')
            await m.reply("اسف طفشت مابستخرج الحين تعال بعدين ")
        finally:
            if photo_path and os.path.exists(photo_path):
                try:
                    os.remove(photo_path)
                except Exception:
                    pass



import re
import uuid
import json
from compat import RPCError
from helpers.replies_store import (
    plugins_attachments_1002,
    plugins_attachments_1009,
    plugins_attachments_1014,
    plugins_attachments_1022,
    plugins_attachments_1024,
    plugins_attachments_391,
    plugins_attachments_396,
    plugins_attachments_404,
    plugins_attachments_407,
    plugins_attachments_411,
    plugins_attachments_449,
    plugins_attachments_453,
    plugins_attachments_455,
    plugins_attachments_457,
    plugins_attachments_461,
    plugins_attachments_463,
    plugins_attachments_465,
    plugins_attachments_469,
    plugins_attachments_471,
    plugins_attachments_473,
    plugins_attachments_477,
    plugins_attachments_479,
    plugins_attachments_481,
    plugins_attachments_516,
    plugins_attachments_527,
    plugins_attachments_538,
    plugins_attachments_569,
    plugins_attachments_573,
    plugins_attachments_584,
    plugins_attachments_615,
    plugins_attachments_619,
    plugins_attachments_629,
    plugins_attachments_648,
    plugins_attachments_654,
    plugins_attachments_662,
    plugins_attachments_667,
    plugins_attachments_680,
    plugins_attachments_683,
    plugins_attachments_686,
    plugins_attachments_737,
    plugins_attachments_740,
    plugins_attachments_749,
    plugins_attachments_784,
    plugins_attachments_794,
    plugins_attachments_798,
    plugins_attachments_804,
    plugins_attachments_812,
    plugins_attachments_919,
    plugins_attachments_932,
    plugins_attachments_937,
    plugins_attachments_943,
    plugins_attachments_946,
    plugins_attachments_949,
    plugins_attachments_958,
    plugins_attachments_967,
    plugins_attachments_974,
    plugins_attachments_977,
    plugins_attachments_983,
    plugins_attachments_986,
    plugins_attachments_990,
)

async def generate_short_name(client, display_name, user_id):
    try:
        me = await client.get_me()
        bot_username = me.username if me and me.username else "bot"
    except Exception:
        bot_username = "bot"

    clean = re.sub(r'[^a-zA-Z0-9]', '', display_name)
    if not clean:
        clean = "pack"
    if not clean[0].isalpha():
        clean = f"p{clean}"

    short = f"{clean}_{user_id}_{uuid.uuid4().hex[:4]}_by_{bot_username}"
    return short.lower()[:64]

@Client.on_message((filters.text | filters.sticker | filters.document) & filters.group, group=1232)
async def replace_pack_handler(c, m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()

    if await r.get(f'replacePack:disabled:{Dev_FINAL}{m.chat.id}'):
        return

    if not await check_global_restrictions(c, m, k):
        return

    if not m.from_user:
        return

    user_id = m.from_user.id
    chat_id = m.chat.id
    text = m.text.strip() if m.text else (m.caption.strip() if m.caption else "")

    state_key = f"replace_pack_state:{chat_id}:{user_id}"
    data_key = f"replace_pack_data:{chat_id}:{user_id}"

    if text == 'استبدال حزمه':
        if await r.get(f'replacePack:disabled:{Dev_FINAL}{m.chat.id}'):
            return await m.reply(plugins_attachments_737(k))
        
        await r.set(state_key, 'waiting_for_pack', ex=300)
        return await m.reply(plugins_attachments_740(k, k))

    current_state = await r.get(state_key)
    if not current_state:
        return

    if text == 'الغاء':
        await r.delete(state_key)
        await r.delete(data_key)
        return await m.reply(plugins_attachments_749(k))

    if current_state == 'waiting_for_pack':
        rep = m.reply_to_message
        pack_short_name = None
        pack_id = None
        pack_hash = None
        is_emoji_pack = False

        check_text = text or (rep.text if rep and rep.text else "") or (rep.caption if rep and rep.caption else "")
        if 'addemoji/' in check_text:
            match = re.search(r't\.me/addemoji/([a-zA-Z0-9_]+)', check_text)
            if match:
                pack_short_name = match.group(1)
                is_emoji_pack = True
        elif 'addstickers/' in check_text:
            match = re.search(r't\.me/addstickers/([a-zA-Z0-9_]+)', check_text)
            if match:
                pack_short_name = match.group(1)
                is_emoji_pack = False

        target_media = m.sticker or m.document or (rep.sticker if rep else None) or (rep.document if rep else None)
        if not pack_short_name and target_media:
            if hasattr(target_media, 'set_name') and target_media.set_name:
                pack_short_name = target_media.set_name
            elif hasattr(target_media, 'attributes') and target_media.attributes:
                for attr in target_media.attributes:
                    if hasattr(attr, 'stickerset') and attr.stickerset:
                        pack_id = attr.stickerset.id
                        pack_hash = attr.stickerset.access_hash
                        break
                if any(isinstance(a, DocumentAttributeCustomEmoji) for a in target_media.attributes):
                    is_emoji_pack = True

        if not pack_short_name and not pack_id:
            return await m.reply(plugins_attachments_784(k))

        pack_info = {
            'pack_short_name': pack_short_name,
            'pack_id': pack_id,
            'pack_hash': pack_hash,
            'is_emoji_pack': is_emoji_pack
        }
        await r.set(data_key, json.dumps(pack_info), ex=300)
        await r.set(state_key, 'waiting_for_name', ex=300)
        return await m.reply(plugins_attachments_794(k))

    elif current_state == 'waiting_for_name':
        if not text:
            return await m.reply(plugins_attachments_798(k))

        new_display_name = text
        stored_data = await r.get(data_key)
        if not stored_data:
            await r.delete(state_key)
            return await m.reply(plugins_attachments_804(k))

        pack_info = json.loads(stored_data)
        pack_short_name = pack_info.get('pack_short_name')
        pack_id = pack_info.get('pack_id')
        pack_hash = pack_info.get('pack_hash')
        is_emoji_pack = pack_info.get('is_emoji_pack', False)

        msg = await m.reply(plugins_attachments_812(k))

        try:
            old_link = None
            if pack_short_name:
                try:
                    pack_data = await c.get_sticker_set(pack_short_name)
                    documents = pack_data.stickers or []
                    old_link = f"https://t.me/{'addemoji' if is_emoji_pack else 'addstickers'}/{pack_short_name}"
                except Exception:
                    documents = []
            else:
                documents = []
                old_link = f"https://t.me/addstickers/pack"

            items = []
            for st in documents:
                emoji = st.emoji or "\u2022"
                items.append(sticker_item(st.file_id, emoji))

            if not items:
                await r.delete(state_key)
                await r.delete(data_key)
                return await msg.edit(f'{k} \u0645\u0639\u0637\u064a\u0646\u064a \u062d\u0632\u0645\u0647 \u0641\u0627\u0631\u063a\u0647 \u0634\u0648\u0636\u0639\u0643 \u062a\u062e\u0628\u0631 \u0635\u0628\u0631\u064a \u061f.')

            new_short_name = await generate_short_name(c, new_display_name, user_id)

            try:
                new_pack_name = await create_sticker_set_safe(
                    c,
                    user_id=user_id,
                    name=new_short_name,
                    title=new_display_name,
                    items=items,
                    is_emoji_pack=is_emoji_pack,
                )
                new_link = f"https://t.me/{'addemoji' if is_emoji_pack else 'addstickers'}/{new_pack_name}"
            except Exception as e:
                logger.exception('create_sticker_set failed (replace pack)')
                await r.delete(state_key)
                await r.delete(data_key)
                return await msg.edit(f'{k} \u0635\u0627\u0631 \u062e\u0637\u0623 \u0623\u062b\u0646\u0627\u0621 \u0625\u0646\u0634\u0627\u0621 \u0627\u0644\u062d\u0632\u0645\u0629: {str(e)[:200]}')

            await r.delete(state_key)
            await r.delete(data_key)

            completion_text = (
                f"{k} اكتمل الاستبدال\n"
                f"{k} رابط الحزمه القديم  ↤ <a href=\"{old_link}\">اضغط هنا</a>\n\n"
                f"{k} رابط الحزمه الجديد ↤ <a href=\"{new_link}\">اضغط هنا</a>"
            )
            return await msg.edit(completion_text, disable_web_page_preview=True)

        except RPCError as e:
            logger.exception('replace pack RPCError')
            await r.delete(state_key)
            await r.delete(data_key)
            return await msg.edit(f'{k} صار خطأ أثناء إنشاء الحزمة: {str(e)[:200]}')
        except Exception as e:
            logger.exception('replace pack unexpected error')
            await r.delete(state_key)
            await r.delete(data_key)
            return await msg.edit(f'{k} صار خطأ غير متوقع: {str(e)[:200]}')

# ============================================================
# دمج حزمتين ملصقات/ايموجي في حزمة واحدة جديدة
# ============================================================

MERGE_MAX_ITEMS = 120


def parse_pack_link(text_val):
    text_val = text_val or ""
    match = re.search(r't\.me/addemoji/([a-zA-Z0-9_]+)', text_val)
    if match:
        return match.group(1), True
    match = re.search(r't\.me/addstickers/([a-zA-Z0-9_]+)', text_val)
    if match:
        return match.group(1), False
    return None, None


async def fetch_pack_items(c, short_name):
    pack_data = await c.get_sticker_set(short_name)
    documents = pack_data.stickers or []
    return [sticker_item(st.file_id, st.emoji) for st in documents]


@Client.on_message(filters.text & filters.group, group=1234)
async def merge_pack_handler(c, m):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()

    if not await check_global_restrictions(c, m, k):
        return

    if not m.from_user:
        return

    user_id = m.from_user.id
    chat_id = m.chat.id
    text = m.text.strip() if m.text else ""

    state_key = f"merge_pack_state:{chat_id}:{user_id}"
    data_key = f"merge_pack_data:{chat_id}:{user_id}"

    if text == 'دمج حزمه':
        await r.set(state_key, 'waiting_first', ex=300)
        await r.delete(data_key)
        return await m.reply(
            plugins_attachments_919(k, k, MERGE_MAX_ITEMS, k)
        )

    current_state = await r.get(state_key)
    if not current_state:
        return

    if text == 'الغاء':
        await r.delete(state_key)
        await r.delete(data_key)
        return await m.reply(plugins_attachments_932(k))

    if current_state == 'waiting_first':
        short_name, is_emoji = parse_pack_link(text)
        if not short_name:
            return await m.reply(plugins_attachments_937(k))

        try:
            items = await fetch_pack_items(c, short_name)
        except Exception as e:
            logger.exception('merge pack: failed to fetch first pack')
            return await m.reply(plugins_attachments_943(k, str(e)[:200]))

        if not items:
            return await m.reply(plugins_attachments_946(k))

        if len(items) > MERGE_MAX_ITEMS:
            return await m.reply(plugins_attachments_949(k, len(items), MERGE_MAX_ITEMS))

        kind = 'ايموجي' if is_emoji else 'ملصق'
        await r.set(data_key, json.dumps({
            'first_items': items,
            'is_emoji_pack': is_emoji,
            'first_short': short_name,
        }), ex=300)
        await r.set(state_key, 'waiting_second', ex=300)
        return await m.reply(
            plugins_attachments_958(k, len(items), kind, k)
        )

    if current_state == 'waiting_second':
        stored = await r.get(data_key)
        if not stored:
            await r.delete(state_key)
            return await m.reply(plugins_attachments_967(k))
        data = json.loads(stored)
        first_items = data.get('first_items', [])
        is_emoji_pack = data.get('is_emoji_pack', False)

        short_name, is_emoji = parse_pack_link(text)
        if not short_name:
            return await m.reply(plugins_attachments_974(k))

        if is_emoji != is_emoji_pack:
            return await m.reply(plugins_attachments_977(k))

        try:
            second_items = await fetch_pack_items(c, short_name)
        except Exception as e:
            logger.exception('merge pack: failed to fetch second pack')
            return await m.reply(plugins_attachments_983(k, str(e)[:200]))

        if not second_items:
            return await m.reply(plugins_attachments_986(k))

        total = len(first_items) + len(second_items)
        if total > MERGE_MAX_ITEMS:
            return await m.reply(
                plugins_attachments_990(k, total, MERGE_MAX_ITEMS, k)
            )

        kind = 'ايموجي' if is_emoji_pack else 'ملصق'
        merged_items = first_items + second_items
        await r.set(data_key, json.dumps({
            'merged_items': merged_items,
            'is_emoji_pack': is_emoji_pack,
        }), ex=300)
        await r.set(state_key, 'waiting_name', ex=300)
        return await m.reply(
            plugins_attachments_1002(k, len(second_items), kind, k)
        )

    if current_state == 'waiting_name':
        if not text:
            return await m.reply(plugins_attachments_1009(k))

        stored = await r.get(data_key)
        if not stored:
            await r.delete(state_key)
            return await m.reply(plugins_attachments_1014(k))
        data = json.loads(stored)
        merged_items = data.get('merged_items', [])
        is_emoji_pack = data.get('is_emoji_pack', False)

        if not merged_items:
            await r.delete(state_key)
            await r.delete(data_key)
            return await m.reply(plugins_attachments_1022(k))

        msg = await m.reply(plugins_attachments_1024(k))
        new_display_name = text
        new_short_name = await generate_short_name(c, new_display_name, user_id)

        try:
            new_pack_name = await create_sticker_set_safe(
                c,
                user_id=user_id,
                name=new_short_name,
                title=new_display_name,
                items=merged_items,
                is_emoji_pack=is_emoji_pack,
            )
            new_link = f"https://t.me/{'addemoji' if is_emoji_pack else 'addstickers'}/{new_pack_name}"
        except Exception as e:
            logger.exception('merge pack: create_sticker_set failed')
            await r.delete(state_key)
            await r.delete(data_key)
            return await msg.edit(f'{k} صار خطأ أثناء إنشاء الحزمة: {str(e)[:200]}')

        await r.delete(state_key)
        await r.delete(data_key)

        completion_text = (
            f"{k} تم اكتمال دمج الحزمتين\n"
            f"{k} رابط الحزمة ↤ <a href=\"{new_link}\">اضغط هنا</a>"
        )
        return await msg.edit(completion_text, disable_web_page_preview=True)
