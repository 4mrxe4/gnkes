# plugins/events/iquery.py — rebuilt for botm_unified (aiogram inline query)
# The old standalone project used py_yt + Pyrogram inline query; here we use
# the music module's own search (yt.search) and aiogram InlineQueryResult.
from helpers.context import redis_proxy as r, dev_final_proxy as Dev_FINAL, k_proxy as k
from compat import Client, filters, types
from compat import InlineQueryResultArticle, InputTextMessageContent
from plugins.FinalMusic import app, yt
from plugins.FinalMusic.fm_helpers import buttons


def _format_duration(sec) -> str:
    try:
        sec = int(sec)
        if sec <= 0:
            return "N/A"
        h, rem = divmod(sec, 3600)
        m, s = divmod(rem, 60)
        if h:
            return f"{h}:{m:02d}:{s:02d}"
        return f"{m}:{s:02d}"
    except Exception:
        return "N/A"


@Client.on_inline_query(filters.user(list(app.bl_users)) if app.bl_users else filters.incoming, group=-50)
async def inline_query_handler(_, query: types.InlineQuery):
    text = query.query.strip()
    if not text:
        return
    try:
        tracks = await yt.search(text, query.id)
        if not tracks:
            tracks = []
        answers = []
        for idx, track in enumerate(tracks[:15]):
            title = track.title
            duration = _format_duration(getattr(track, "duration_sec", 0))
            link = f"https://www.youtube.com/watch?v={track.id}"
            caption = (
                f"<b>العنوان:</b> <a href='{link}'>{title[:250]}</a>\n\n"
                f"<b>المدة:</b> {duration}\n\n"
                f"<u><i>بواسطة {app.name if hasattr(app, 'name') else 'البوت'}</i></u>"
            )
            answers.append(InlineQueryResultArticle(
                id=f"yt_{idx}_{track.id}",
                title=title,
                description=f"{duration}",
                input_message_content=InputTextMessageContent(
                    message_text=f"/play {link}\n\n{title}",
                    parse_mode="HTML",
                ),
                reply_markup=buttons.yt_key(link).model_dump(exclude_none=True) if hasattr(buttons.yt_key(link), "model_dump") else None,
            ))
        if answers:
            await query.answer(answers, cache_time=5)
    except Exception:
        pass
