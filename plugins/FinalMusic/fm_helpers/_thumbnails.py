# _thumbnails.py
from helpers.context import redis_proxy as r, dev_final_proxy as Dev_FINAL, k_proxy as k
import os
import re
import asyncio
import aiohttp
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from helpers.context import config_proxy as config
from ._dataclass import Track
FALLBACK_THUMB = "https://files.catbox.moe/8czm1s.png"
BOT_CARD_DIR = "cache/bot_cards"
PANEL_W, PANEL_H = 763, 545
PANEL_X = (1280 - PANEL_W) // 2
PANEL_Y = 88
TRANSPARENCY = 170
THUMB_W, THUMB_H = 542, 273
THUMB_X = PANEL_X + (PANEL_W - THUMB_W) // 2
THUMB_Y = PANEL_Y + 36
TITLE_X = 377
TITLE_Y = THUMB_Y + THUMB_H + 10
META_Y = TITLE_Y + 45
BAR_X, BAR_Y = 388, META_Y + 45
BAR_RED_LEN = 280
BAR_TOTAL_LEN = 480
ICONS_W, ICONS_H = 415, 45
ICONS_X = PANEL_X + (PANEL_W - ICONS_W) // 2
ICONS_Y = BAR_Y + 48
MAX_TITLE_WIDTH = 580
def trim_to_width(text: str, font: ImageFont.FreeTypeFont, max_w: int) -> str:
    ellipsis = "…"
    if font.getlength(text) <= max_w:
        return text
    for i in range(len(text) - 1, 0, -1):
        if font.getlength(text[:i] + ellipsis) <= max_w:
            return text[:i] + ellipsis
    return ellipsis
class Thumbnail:
    def __init__(self):
        try:
            self.title_font = ImageFont.truetype("plugins/FinalMusic/fm_helpers/Raleway-Bold.ttf", 32)
            self.regular_font = ImageFont.truetype("plugins/FinalMusic/fm_helpers/Inter-Light.ttf", 18)
        except OSError:
            self.title_font = self.regular_font = ImageFont.load_default()
    async def save_thumb(self, output_path: str, url: str) -> str:
        if not url:
            return FALLBACK_THUMB
        try:
            os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status != 200:
                        return FALLBACK_THUMB
                    with open(output_path, "wb") as f:
                        f.write(await resp.read())
                    return output_path
        except Exception:
            return FALLBACK_THUMB
    async def generate(self, song: Track, size=(1280, 720)) -> str:
        try:
            if not song or not getattr(song, 'thumbnail', None):
                return getattr(config, 'DEFAULT_THUMB', None) or FALLBACK_THUMB
            temp = f"cache/temp_{song.id}.jpg"
            output = f"cache/{song.id}_modern.png"
            if os.path.exists(output):
                return output
            await self.save_thumb(temp, song.thumbnail)
            if not os.path.exists(temp):
                return getattr(config, 'DEFAULT_THUMB', None) or FALLBACK_THUMB
            result = await asyncio.get_event_loop().run_in_executor(None, self._generate_sync, temp, output, song, size)
            return result or getattr(config, 'DEFAULT_THUMB', None) or FALLBACK_THUMB
        except Exception:
            return getattr(config, 'DEFAULT_THUMB', None) or FALLBACK_THUMB
    def _generate_sync(self, temp: str, output: str, song: Track, size=(1280, 720)) -> str:
        try:
            with Image.open(temp) as temp_img:
                base = temp_img.resize(size).convert("RGBA")
            bg = ImageEnhance.Brightness(base.filter(ImageFilter.BoxBlur(10))).enhance(0.6)
            panel_area = bg.crop((PANEL_X, PANEL_Y, PANEL_X + PANEL_W, PANEL_Y + PANEL_H))
            overlay = Image.new("RGBA", (PANEL_W, PANEL_H), (255, 255, 255, TRANSPARENCY))
            frosted = Image.alpha_composite(panel_area, overlay)
            mask = Image.new("L", (PANEL_W, PANEL_H), 0)
            ImageDraw.Draw(mask).rounded_rectangle((0, 0, PANEL_W, PANEL_H), 50, fill=255)
            bg.paste(frosted, (PANEL_X, PANEL_Y), mask)
            thumb = base.resize((THUMB_W, THUMB_H))
            tmask = Image.new("L", thumb.size, 0)
            ImageDraw.Draw(tmask).rounded_rectangle((0, 0, THUMB_W, THUMB_H), 20, fill=255)
            bg.paste(thumb, (THUMB_X, THUMB_Y), tmask)
            draw = ImageDraw.Draw(bg)
            clean_title = re.sub(r"\W+", " ", song.title).title()
            draw.text((TITLE_X, TITLE_Y), trim_to_width(clean_title, self.title_font, MAX_TITLE_WIDTH), fill="black", font=self.title_font)
            draw.text((TITLE_X, META_Y), f"YouTube | {song.view_count or 'Unknown Views'}", fill="black", font=self.regular_font)
            draw.line([(BAR_X, BAR_Y), (BAR_X + BAR_RED_LEN, BAR_Y)], fill="red", width=6)
            draw.line([(BAR_X + BAR_RED_LEN, BAR_Y), (BAR_X + BAR_TOTAL_LEN, BAR_Y)], fill="gray", width=5)
            draw.ellipse([(BAR_X + BAR_RED_LEN - 7, BAR_Y - 7), (BAR_X + BAR_RED_LEN + 7, BAR_Y + 7)], fill="red")
            draw.text((BAR_X, BAR_Y + 15), "00:00", fill="black", font=self.regular_font)
            is_live = getattr(song, 'is_live', False)
            end_text = "Live" if is_live else song.duration
            draw.text((BAR_X + BAR_TOTAL_LEN - (90 if is_live else 60), BAR_Y + 15), end_text, fill="red" if is_live else "black", font=self.regular_font)
            icons_path = "plugins/FinalMusic/fm_helpers/play_icons.png"
            if os.path.isfile(icons_path):
                with Image.open(icons_path) as icons_img:
                    ic = icons_img.resize((ICONS_W, ICONS_H)).convert("RGBA")
                    r, g, b, a = ic.split()
                    black_ic = Image.merge("RGBA", (r.point(lambda _: 0), g.point(lambda _: 0), b.point(lambda _: 0), a))
                    bg.paste(black_ic, (ICONS_X, ICONS_Y), black_ic)
            bg.save(output)
            try:
                os.remove(temp)
            except OSError:
                pass
            return output
        except Exception:
            return getattr(config, 'DEFAULT_THUMB', None) or FALLBACK_THUMB

    # ------------------------------------------------------------------
    # "تشغيل" بالرد على مقطع موجود بالمحادثة: لا يوجد لدينا بيانات يوتيوب
    # (عنوان/مشاهدات) لهذا الملف، فنعرض بنفس تصميم اللوحة لكن ببيانات
    # البوت نفسه (صورته + يوزره + اسمه). بما أن بيانات البوت ثابتة، تُبنى
    # اللوحة الأساسية مرة واحدة فقط وتُخزَّن على القرص، وبعدها فقط نطبع
    # مدة المقطع الحالي فوق النسخة المخزّنة (سريع، بدون إعادة تحميل الصورة
    # أو إعادة عمل الـ blur في كل مرة).
    # ------------------------------------------------------------------
    async def _get_bot_avatar_path(self, bot_id: str, bot_user, app) -> str | None:
        os.makedirs(BOT_CARD_DIR, exist_ok=True)
        avatar_path = f"{BOT_CARD_DIR}/avatar_{bot_id}.jpg"
        if os.path.exists(avatar_path):
            return avatar_path
        try:
            photo_file_id = None
            async for p in app.get_chat_photos(bot_user.id, limit=1):
                photo_file_id = getattr(p, "file_id", None)
                break
            if not photo_file_id:
                return None
            downloaded = await app.download_media(photo_file_id, file_name=avatar_path)
            return downloaded if downloaded and os.path.exists(avatar_path) else None
        except Exception:
            return None

    def _build_bot_base_sync(self, avatar_path: str, bot_name: str, bot_username: str | None, output: str, size=(1280, 720)) -> str | None:
        try:
            with Image.open(avatar_path) as av_img:
                base = av_img.resize(size).convert("RGBA")
            bg = ImageEnhance.Brightness(base.filter(ImageFilter.BoxBlur(10))).enhance(0.6)
            panel_area = bg.crop((PANEL_X, PANEL_Y, PANEL_X + PANEL_W, PANEL_Y + PANEL_H))
            overlay = Image.new("RGBA", (PANEL_W, PANEL_H), (255, 255, 255, TRANSPARENCY))
            frosted = Image.alpha_composite(panel_area, overlay)
            mask = Image.new("L", (PANEL_W, PANEL_H), 0)
            ImageDraw.Draw(mask).rounded_rectangle((0, 0, PANEL_W, PANEL_H), 50, fill=255)
            bg.paste(frosted, (PANEL_X, PANEL_Y), mask)
            thumb_img = base.resize((THUMB_W, THUMB_H))
            tmask = Image.new("L", thumb_img.size, 0)
            ImageDraw.Draw(tmask).rounded_rectangle((0, 0, THUMB_W, THUMB_H), 20, fill=255)
            bg.paste(thumb_img, (THUMB_X, THUMB_Y), tmask)
            draw = ImageDraw.Draw(bg)
            clean_title = re.sub(r"\W+", " ", bot_name or "").strip().title() or "Music Bot"
            draw.text((TITLE_X, TITLE_Y), trim_to_width(clean_title, self.title_font, MAX_TITLE_WIDTH), fill="black", font=self.title_font)
            handle = f"@{bot_username}" if bot_username else "Telegram"
            draw.text((TITLE_X, META_Y), trim_to_width(handle, self.regular_font, MAX_TITLE_WIDTH), fill="black", font=self.regular_font)
            draw.line([(BAR_X, BAR_Y), (BAR_X + BAR_RED_LEN, BAR_Y)], fill="red", width=6)
            draw.line([(BAR_X + BAR_RED_LEN, BAR_Y), (BAR_X + BAR_TOTAL_LEN, BAR_Y)], fill="gray", width=5)
            draw.ellipse([(BAR_X + BAR_RED_LEN - 7, BAR_Y - 7), (BAR_X + BAR_RED_LEN + 7, BAR_Y + 7)], fill="red")
            draw.text((BAR_X, BAR_Y + 15), "00:00", fill="black", font=self.regular_font)
            icons_path = "plugins/FinalMusic/fm_helpers/play_icons.png"
            if os.path.isfile(icons_path):
                with Image.open(icons_path) as icons_img:
                    ic = icons_img.resize((ICONS_W, ICONS_H)).convert("RGBA")
                    ir, ig, ib, ia = ic.split()
                    black_ic = Image.merge("RGBA", (ir.point(lambda _: 0), ig.point(lambda _: 0), ib.point(lambda _: 0), ia))
                    bg.paste(black_ic, (ICONS_X, ICONS_Y), black_ic)
            bg.save(output)
            return output
        except Exception:
            return None

    def _stamp_duration_sync(self, base_path: str, output: str, end_text: str, is_live: bool) -> str | None:
        try:
            with Image.open(base_path) as base_img:
                img = base_img.copy()
            draw = ImageDraw.Draw(img)
            x = BAR_X + BAR_TOTAL_LEN - (90 if is_live else 60)
            draw.text((x, BAR_Y + 15), end_text, fill="red" if is_live else "black", font=self.regular_font)
            img.save(output)
            return output
        except Exception:
            return None

    async def generate_bot_card(self, bot_id: str, bot_name: str, bot_username: str | None, media, app) -> str:
        try:
            os.makedirs(BOT_CARD_DIR, exist_ok=True)
            base_path = f"{BOT_CARD_DIR}/base_{bot_id}.png"
            if not os.path.exists(base_path):
                bot_user = getattr(app, "me", None) or await app.get_me()
                avatar_path = await self._get_bot_avatar_path(bot_id, bot_user, app)
                if not avatar_path:
                    return FALLBACK_THUMB
                built = await asyncio.get_event_loop().run_in_executor(
                    None, self._build_bot_base_sync, avatar_path, bot_name, bot_username, base_path
                )
                if not built:
                    return FALLBACK_THUMB
            is_live = bool(getattr(media, 'is_live', False))
            end_text = "Live" if is_live else (getattr(media, 'duration', None) or "00:00")
            media_id = getattr(media, 'id', None) or "x"
            output = f"{BOT_CARD_DIR}/card_{bot_id}_{media_id}.png"
            result = await asyncio.get_event_loop().run_in_executor(
                None, self._stamp_duration_sync, base_path, output, end_text, is_live
            )
            return result or base_path
        except Exception:
            return FALLBACK_THUMB