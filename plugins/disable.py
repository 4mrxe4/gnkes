from helpers.context import get_global_r, get_global_dev, get_global_k
r = get_global_r()
Dev_FINAL = get_global_dev()
k = get_global_k()
"""
[ = This plugin is a part from Rfinal Source code = ]
{"Developer":"https://t.me/i0i0ii"}
"""

from threading import Thread
from compat import *
from compat import *
from helpers.ranks import *
from .protect import *
from helpers.replies_store import (
    plugins_disable_103,
    plugins_disable_109,
    plugins_disable_112,
    plugins_disable_117,
    plugins_disable_123,
    plugins_disable_126,
    plugins_disable_131,
    plugins_disable_137,
    plugins_disable_140,
    plugins_disable_145,
    plugins_disable_151,
    plugins_disable_154,
    plugins_disable_159,
    plugins_disable_165,
    plugins_disable_168,
    plugins_disable_173,
    plugins_disable_179,
    plugins_disable_182,
    plugins_disable_187,
    plugins_disable_193,
    plugins_disable_196,
    plugins_disable_201,
    plugins_disable_207,
    plugins_disable_210,
    plugins_disable_215,
    plugins_disable_221,
    plugins_disable_224,
    plugins_disable_227,
    plugins_disable_231,
    plugins_disable_234,
    plugins_disable_237,
    plugins_disable_241,
    plugins_disable_244,
    plugins_disable_249,
    plugins_disable_25,
    plugins_disable_255,
    plugins_disable_258,
    plugins_disable_263,
    plugins_disable_269,
    plugins_disable_272,
    plugins_disable_277,
    plugins_disable_28,
    plugins_disable_283,
    plugins_disable_286,
    plugins_disable_291,
    plugins_disable_297,
    plugins_disable_300,
    plugins_disable_305,
    plugins_disable_311,
    plugins_disable_314,
    plugins_disable_319,
    plugins_disable_325,
    plugins_disable_328,
    plugins_disable_33,
    plugins_disable_333,
    plugins_disable_339,
    plugins_disable_342,
    plugins_disable_347,
    plugins_disable_356,
    plugins_disable_359,
    plugins_disable_364,
    plugins_disable_370,
    plugins_disable_373,
    plugins_disable_378,
    plugins_disable_384,
    plugins_disable_387,
    plugins_disable_39,
    plugins_disable_392,
    plugins_disable_398,
    plugins_disable_401,
    plugins_disable_406,
    plugins_disable_412,
    plugins_disable_415,
    plugins_disable_42,
    plugins_disable_420,
    plugins_disable_426,
    plugins_disable_429,
    plugins_disable_434,
    plugins_disable_440,
    plugins_disable_443,
    plugins_disable_448,
    plugins_disable_454,
    plugins_disable_457,
    plugins_disable_462,
    plugins_disable_468,
    plugins_disable_47,
    plugins_disable_471,
    plugins_disable_476,
    plugins_disable_482,
    plugins_disable_485,
    plugins_disable_490,
    plugins_disable_497,
    plugins_disable_500,
    plugins_disable_505,
    plugins_disable_511,
    plugins_disable_514,
    plugins_disable_519,
    plugins_disable_525,
    plugins_disable_528,
    plugins_disable_53,
    plugins_disable_533,
    plugins_disable_539,
    plugins_disable_542,
    plugins_disable_547,
    plugins_disable_56,
    plugins_disable_61,
    plugins_disable_67,
    plugins_disable_70,
    plugins_disable_75,
    plugins_disable_81,
    plugins_disable_84,
    plugins_disable_89,
    plugins_disable_95,
    plugins_disable_98,
)


async def handle_feature_toggles(c, m, k, text, channel):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    if not await check_global_restrictions(c, m, k):
        return
    if text == "تعطيل الترحيب":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_disable_25(k))
        else:
            if await r.get(f"{m.chat.id}:disableWelcome:{Dev_FINAL}"):
                return await m.reply(
                    plugins_disable_28(k, m.from_user.mention(), k)
                )
            else:
                await r.set(f"{m.chat.id}:disableWelcome:{Dev_FINAL}", 1)
                return await m.reply(
                    plugins_disable_33(k, m.from_user.mention(), k)
                )

    if text == "تفعيل الترحيب":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_disable_39(k))
        else:
            if not await r.get(f"{m.chat.id}:disableWelcome:{Dev_FINAL}"):
                return await m.reply(
                    plugins_disable_42(k, m.from_user.mention(), k)
                )
            else:
                await r.delete(f"{m.chat.id}:disableWelcome:{Dev_FINAL}")
                return await m.reply(
                    plugins_disable_47(k, m.from_user.mention(), k)
                )

    if text == "تعطيل الترحيب بالصورة" or text == "تعطيل الترحيب بالصوره":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_disable_53(k))
        else:
            if await r.get(f"{m.chat.id}:disableWelcomep:{Dev_FINAL}"):
                return await m.reply(
                    plugins_disable_56(k, m.from_user.mention(), k)
                )
            else:
                await r.set(f"{m.chat.id}:disableWelcomep:{Dev_FINAL}", 1)
                return await m.reply(
                    plugins_disable_61(k, m.from_user.mention(), k)
                )

    if text == "تفعيل الترحيب بالصورة" or text == "تفعيل الترحيب بالصوره":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_disable_67(k))
        else:
            if not await r.get(f"{m.chat.id}:disableWelcomep:{Dev_FINAL}"):
                return await m.reply(
                    plugins_disable_70(k, m.from_user.mention(), k)
                )
            else:
                await r.delete(f"{m.chat.id}:disableWelcomep:{Dev_FINAL}")
                return await m.reply(
                    plugins_disable_75(k, m.from_user.mention(), k)
                )

    if text == "تعطيل الرابط":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_disable_81(k))
        else:
            if await r.get(f"{m.chat.id}:disableLINK:{Dev_FINAL}"):
                return await m.reply(
                    plugins_disable_84(k, m.from_user.mention(), k)
                )
            else:
                await r.set(f"{m.chat.id}:disableLINK:{Dev_FINAL}", 1)
                return await m.reply(
                    plugins_disable_89(k, m.from_user.mention(), k)
                )

    if text == "تفعيل الرابط":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_disable_95(k))
        else:
            if not await r.get(f"{m.chat.id}:disableLINK:{Dev_FINAL}"):
                return await m.reply(
                    plugins_disable_98(k, m.from_user.mention(), k)
                )
            else:
                await r.delete(f"{m.chat.id}:disableLINK:{Dev_FINAL}")
                return await m.reply(
                    plugins_disable_103(k, m.from_user.mention(), k)
                )

    if text == "تعطيل البايو":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_disable_109(k))
        else:
            if await r.get(f"{m.chat.id}:disableBio:{Dev_FINAL}"):
                return await m.reply(
                    plugins_disable_112(k, m.from_user.mention(), k)
                )
            else:
                await r.set(f"{m.chat.id}:disableBio:{Dev_FINAL}", 1)
                return await m.reply(
                    plugins_disable_117(k, m.from_user.mention(), k)
                )

    if text == "تفعيل البايو":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_disable_123(k))
        else:
            if not await r.get(f"{m.chat.id}:disableBio:{Dev_FINAL}"):
                return await m.reply(
                    plugins_disable_126(k, m.from_user.mention(), k)
                )
            else:
                await r.delete(f"{m.chat.id}:disableBio:{Dev_FINAL}")
                return await m.reply(
                    plugins_disable_131(k, m.from_user.mention(), k)
                )

    if text == "تعطيل اطردني":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_disable_137(k))
        else:
            if not await r.get(f"{m.chat.id}:enableKickMe:{Dev_FINAL}"):
                return await m.reply(
                    plugins_disable_140(k, m.from_user.mention(), k)
                )
            else:
                await r.delete(f"{m.chat.id}:enableKickMe:{Dev_FINAL}")
                return await m.reply(
                    plugins_disable_145(k, m.from_user.mention(), k)
                )

    if text == "تفعيل اطردني":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_disable_151(k))
        else:
            if await r.get(f"{m.chat.id}:enableKickMe:{Dev_FINAL}"):
                return await m.reply(
                    plugins_disable_154(k, m.from_user.mention(), k)
                )
            else:
                await r.set(f"{m.chat.id}:enableKickMe:{Dev_FINAL}", 1)
                return await m.reply(
                    plugins_disable_159(k, m.from_user.mention(), k)
                )

    if text == "تعطيل التحقق":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_disable_165(k))
        else:
            if not await r.get(f"{m.chat.id}:enableVerify:{Dev_FINAL}"):
                return await m.reply(
                    plugins_disable_168(k, m.from_user.mention(), k)
                )
            else:
                await r.delete(f"{m.chat.id}:enableVerify:{Dev_FINAL}")
                return await m.reply(
                    plugins_disable_173(k, m.from_user.mention(), k)
                )

    if text == "تفعيل التحقق":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_disable_179(k))
        else:
            if await r.get(f"{m.chat.id}:enableVerify:{Dev_FINAL}"):
                return await m.reply(
                    plugins_disable_182(k, m.from_user.mention(), k)
                )
            else:
                await r.set(f"{m.chat.id}:enableVerify:{Dev_FINAL}", 1)
                return await m.reply(
                    plugins_disable_187(k, m.from_user.mention(), k)
                )

    if text == "تعطيل انطقي" or text == "تعطيل انطق":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_disable_193(k))
        else:
            if await r.get(f"{m.chat.id}:disableSay:{Dev_FINAL}"):
                return await m.reply(
                    plugins_disable_196(k, m.from_user.mention(), k)
                )
            else:
                await r.set(f"{m.chat.id}:disableSay:{Dev_FINAL}", 1)
                return await m.reply(
                    plugins_disable_201(k, m.from_user.mention(), k)
                )

    if text == "تفعيل انطقي" or text == "تفعيل انطق":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_disable_207(k))
        else:
            if not await r.get(f"{m.chat.id}:disableSay:{Dev_FINAL}"):
                return await m.reply(
                    plugins_disable_210(k, m.from_user.mention(), k)
                )
            else:
                await r.delete(f"{m.chat.id}:disableSay:{Dev_FINAL}")
                return await m.reply(
                    plugins_disable_215(k, m.from_user.mention(), k)
                )

    if text == "تعطيل المنشن":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_disable_221(k))
        else:
            if await r.get(f"{m.chat.id}:disableALL:{Dev_FINAL}"):
                return await m.reply(plugins_disable_224(k, m.from_user.mention(), k))
            else:
                await r.set(f"{m.chat.id}:disableALL:{Dev_FINAL}", 1)
                return await m.reply(plugins_disable_227(k, m.from_user.mention(), k))

    if text == "تفعيل المنشن":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_disable_231(k))
        else:
            if not await r.get(f"{m.chat.id}:disableALL:{Dev_FINAL}"):
                return await m.reply(plugins_disable_234(k, m.from_user.mention(), k))
            else:
                await r.delete(f"{m.chat.id}:disableALL:{Dev_FINAL}")
                return await m.reply(plugins_disable_237(k, m.from_user.mention(), k))

    if text == "تعطيل التحذير":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_disable_241(k))
        else:
            if await r.get(f"{m.chat.id}:disableWarn:{Dev_FINAL}"):
                return await m.reply(
                    plugins_disable_244(k, m.from_user.mention(), k)
                )
            else:
                await r.set(f"{m.chat.id}:disableWarn:{Dev_FINAL}", 1)
                return await m.reply(
                    plugins_disable_249(k, m.from_user.mention(), k)
                )

    if text == "تفعيل التحذير":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_disable_255(k))
        else:
            if not await r.get(f"{m.chat.id}:disableWarn:{Dev_FINAL}"):
                return await m.reply(
                    plugins_disable_258(k, m.from_user.mention(), k)
                )
            else:
                await r.delete(f"{m.chat.id}:disableWarn:{Dev_FINAL}")
                return await m.reply(
                    plugins_disable_263(k, m.from_user.mention(), k)
                )

    if text == "تعطيل ال8888يوتيوب":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_disable_269(k))
        else:
            if await r.get(f"{m.chat.id}:disableYT:{Dev_FINAL}"):
                return await m.reply(
                    plugins_disable_272(k, m.from_user.mention(), k)
                )
            else:
                await r.set(f"{m.chat.id}:disableYT:{Dev_FINAL}", 1)
                return await m.reply(
                    plugins_disable_277(k, m.from_user.mention(), k)
                )

    if text == "تفعيل8888 اليوتيوب":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_disable_283(k))
        else:
            if not await r.get(f"{m.chat.id}:disableYT:{Dev_FINAL}"):
                return await m.reply(
                    plugins_disable_286(k, m.from_user.mention(), k)
                )
            else:
                await r.delete(f"{m.chat.id}:disableYT:{Dev_FINAL}")
                return await m.reply(
                    plugins_disable_291(k, m.from_user.mention(), k)
                )

    if text == "تعطيل الساوند":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_disable_297(k))
        else:
            if await r.get(f"{m.chat.id}:disableSound:{Dev_FINAL}"):
                return await m.reply(
                    plugins_disable_300(k, m.from_user.mention(), k)
                )
            else:
                await r.set(f"{m.chat.id}:disableSound:{Dev_FINAL}", 1)
                return await m.reply(
                    plugins_disable_305(k, m.from_user.mention(), k)
                )

    if text == "تفعيل الساوند":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_disable_311(k))
        else:
            if not await r.get(f"{m.chat.id}:disableSound:{Dev_FINAL}"):
                return await m.reply(
                    plugins_disable_314(k, m.from_user.mention(), k)
                )
            else:
                await r.delete(f"{m.chat.id}:disableSound:{Dev_FINAL}")
                return await m.reply(
                    plugins_disable_319(k, m.from_user.mention(), k)
                )

    if text == "تعطيل الانستا":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_disable_325(k))
        else:
            if await r.get(f"{m.chat.id}:disableINSTA:{Dev_FINAL}"):
                return await m.reply(
                    plugins_disable_328(k, m.from_user.mention(), k)
                )
            else:
                await r.set(f"{m.chat.id}:disableINSTA:{Dev_FINAL}", 1)
                return await m.reply(
                    plugins_disable_333(k, m.from_user.mention(), k)
                )

    if text == "تفعيل الانستا":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_disable_339(k))
        else:
            if not await r.get(f"{m.chat.id}:disableINSTA:{Dev_FINAL}"):
                return await m.reply(
                    plugins_disable_342(k, m.from_user.mention(), k)
                )
            else:
                await r.delete(f"{m.chat.id}:disableINSTA:{Dev_FINAL}")
                return await m.reply(
                    plugins_disable_347(k, m.from_user.mention(), k)
                )




    if text == "تعطيل التيك":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_disable_356(k))
        else:
            if await r.get(f"{m.chat.id}:disableTik:{Dev_FINAL}"):
                return await m.reply(
                    plugins_disable_359(k, m.from_user.mention(), k)
                )
            else:
                await r.set(f"{m.chat.id}:disableTik:{Dev_FINAL}", 1)
                return await m.reply(
                    plugins_disable_364(k, m.from_user.mention(), k)
                )

    if text == "تفعيل التيك":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_disable_370(k))
        else:
            if not await r.get(f"{m.chat.id}:disableTik:{Dev_FINAL}"):
                return await m.reply(
                    plugins_disable_373(k, m.from_user.mention(), k)
                )
            else:
                await r.delete(f"{m.chat.id}:disableTik:{Dev_FINAL}")
                return await m.reply(
                    plugins_disable_378(k, m.from_user.mention(), k)
                )

    if text == "تعطيل شازام":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_disable_384(k))
        else:
            if await r.get(f"{m.chat.id}:disableShazam:{Dev_FINAL}"):
                return await m.reply(
                    plugins_disable_387(k, m.from_user.mention(), k)
                )
            else:
                await r.set(f"{m.chat.id}:disableShazam:{Dev_FINAL}", 1)
                return await m.reply(
                    plugins_disable_392(k, m.from_user.mention(), k)
                )

    if text == "تفعيل شازام":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_disable_398(k))
        else:
            if not await r.get(f"{m.chat.id}:disableShazam:{Dev_FINAL}"):
                return await m.reply(
                    plugins_disable_401(k, m.from_user.mention(), k)
                )
            else:
                await r.delete(f"{m.chat.id}:disableShazam:{Dev_FINAL}")
                return await m.reply(
                    plugins_disable_406(k, m.from_user.mention(), k)
                )

    if text == "تعطيل الالعاب":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_disable_412(k))
        else:
            if await r.get(f"{m.chat.id}:disableGames:{Dev_FINAL}"):
                return await m.reply(
                    plugins_disable_415(k, m.from_user.mention(), k)
                )
            else:
                await r.set(f"{m.chat.id}:disableGames:{Dev_FINAL}", 1)
                return await m.reply(
                    plugins_disable_420(k, m.from_user.mention(), k)
                )

    if text == "تفعيل الالعاب":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_disable_426(k))
        else:
            if not await r.get(f"{m.chat.id}:disableGames:{Dev_FINAL}"):
                return await m.reply(
                    plugins_disable_429(k, m.from_user.mention(), k)
                )
            else:
                await r.delete(f"{m.chat.id}:disableGames:{Dev_FINAL}")
                return await m.reply(
                    plugins_disable_434(k, m.from_user.mention(), k)
                )

    if text == "تعطيل الترجمة" or text == "تعطيل الترجمه":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_disable_440(k))
        else:
            if await r.get(f"{m.chat.id}:disableTrans:{Dev_FINAL}"):
                return await m.reply(
                    plugins_disable_443(k, m.from_user.mention(), k)
                )
            else:
                await r.set(f"{m.chat.id}:disableTrans:{Dev_FINAL}", 1)
                return await m.reply(
                    plugins_disable_448(k, m.from_user.mention(), k)
                )

    if text == "تفعيل الترجمة" or text == "تفعيل الترجمه":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_disable_454(k))
        else:
            if not await r.get(f"{m.chat.id}:disableTrans:{Dev_FINAL}"):
                return await m.reply(
                    plugins_disable_457(k, m.from_user.mention(), k)
                )
            else:
                await r.delete(f"{m.chat.id}:disableTrans:{Dev_FINAL}")
                return await m.reply(
                    plugins_disable_462(k, m.from_user.mention(), k)
                )

    if text == "تعطيل التسلية" or text == "تعطيل التسليه":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_disable_468(k))
        else:
            if await r.get(f"{m.chat.id}:disableFun:{Dev_FINAL}"):
                return await m.reply(
                    plugins_disable_471(k, m.from_user.mention(), k)
                )
            else:
                await r.set(f"{m.chat.id}:disableFun:{Dev_FINAL}", 1)
                return await m.reply(
                    plugins_disable_476(k, m.from_user.mention(), k)
                )

    if text == "تفعيل التسلية" or text == "تفعيل التسليه":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_disable_482(k))
        else:
            if not await r.get(f"{m.chat.id}:disableFun:{Dev_FINAL}"):
                return await m.reply(
                    plugins_disable_485(k, m.from_user.mention(), k)
                )
            else:
                await r.delete(f"{m.chat.id}:disableFun:{Dev_FINAL}")
                return await m.reply(
                    plugins_disable_490(k, m.from_user.mention(), k)
                )


    if text == "تعطيل اهمس":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_disable_497(k))
        else:
            if await r.get(f"{Dev_FINAL}:whisper_{m.chat.id}") == "off":
                return await m.reply(
                    plugins_disable_500(k, m.from_user.mention(), k)
                )
            else:
                await r.set(f"{Dev_FINAL}:whisper_{m.chat.id}", "off")
                return await m.reply(
                    plugins_disable_505(k, m.from_user.mention(), k)
                )

    if text == "تفعيل اهمس":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_disable_511(k))
        else:
            if await r.get(f"{Dev_FINAL}:whisper_{m.chat.id}") != "off":
                return await m.reply(
                    plugins_disable_514(k, m.from_user.mention(), k)
                )
            else:
                await r.delete(f"{Dev_FINAL}:whisper_{m.chat.id}")
                return await m.reply(
                    plugins_disable_519(k, m.from_user.mention(), k)
                )

    # أوامر "تعطيل/تفعيل الاشتراك" القديمة (عالمية) أُزيلت — الاشتراك الاجباري
    # الآن لكل قروب عبر "اضف اشتراك @..." / "حذف الاشتراك الاجباري"
    # (plugins/force_subscribe.py)

    return None
