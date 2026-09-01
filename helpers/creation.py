
import httpx


async def get_creation_date(id: int, r=None) -> str:
    """يحسب تاريخ إنشاء الحساب.

    الأصل كان يعتمد على `from settings import r` — هنا نستقبل r صراحةً
    أو نقرأه من السياق الحالي للحفاظ على العزل بين البوتات.
    """
    if r is None:
        from helpers.context import get_redis
        r = get_redis()

    if r is not None:
        cached = await r.get(f'{id}:CreateDate')
        if cached:
            return cached

    url = "https://restore-access.indream.app/regdate"
    headers = {
        "accept": "*/*",
        "content-type": "application/x-www-form-urlencoded",
        "user-agent": "Nicegram/92 CFNetwork/1390 Darwin/22.0.0",
        "x-api-key": "e758fb28-79be-4d1c-af6b-066633ded128",
        "accept-language": "en-US,en;q=0.9"
    }
    data = {"telegramId": id}
    try:
        async with httpx.AsyncClient(timeout=15) as http:
            res = await http.post(url, headers=headers, json=data)
        res_json = res.json()
        date_str = res_json['data']['date'].replace('-', '/')
        if r is not None:
            await r.set(f'{id}:CreateDate', date_str)
        return date_str
    except Exception:
        return "غير معروف"


async def get_creation_date_legacy(id: int) -> str:
    """نسخة متوافقة مع الاستدعاءات التي كانت تستدعي (id) فقط."""
    return await get_creation_date(id)
