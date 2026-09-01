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
from helpers.context import get_redis, get_dev_final
from helpers.replies_store import (
    plugins_features_100,
    plugins_features_105,
    plugins_features_111,
    plugins_features_114,
    plugins_features_119,
    plugins_features_125,
    plugins_features_128,
    plugins_features_133,
    plugins_features_139,
    plugins_features_142,
    plugins_features_147,
    plugins_features_153,
    plugins_features_156,
    plugins_features_161,
    plugins_features_167,
    plugins_features_170,
    plugins_features_175,
    plugins_features_181,
    plugins_features_184,
    plugins_features_189,
    plugins_features_195,
    plugins_features_198,
    plugins_features_203,
    plugins_features_209,
    plugins_features_212,
    plugins_features_217,
    plugins_features_223,
    plugins_features_226,
    plugins_features_229,
    plugins_features_233,
    plugins_features_236,
    plugins_features_239,
    plugins_features_243,
    plugins_features_246,
    plugins_features_251,
    plugins_features_257,
    plugins_features_260,
    plugins_features_265,
    plugins_features_27,
    plugins_features_271,
    plugins_features_274,
    plugins_features_279,
    plugins_features_285,
    plugins_features_288,
    plugins_features_293,
    plugins_features_299,
    plugins_features_30,
    plugins_features_302,
    plugins_features_307,
    plugins_features_313,
    plugins_features_316,
    plugins_features_321,
    plugins_features_327,
    plugins_features_330,
    plugins_features_335,
    plugins_features_341,
    plugins_features_344,
    plugins_features_349,
    plugins_features_35,
    plugins_features_358,
    plugins_features_361,
    plugins_features_366,
    plugins_features_372,
    plugins_features_375,
    plugins_features_380,
    plugins_features_386,
    plugins_features_389,
    plugins_features_394,
    plugins_features_400,
    plugins_features_403,
    plugins_features_408,
    plugins_features_41,
    plugins_features_414,
    plugins_features_417,
    plugins_features_422,
    plugins_features_428,
    plugins_features_431,
    plugins_features_436,
    plugins_features_44,
    plugins_features_442,
    plugins_features_445,
    plugins_features_450,
    plugins_features_456,
    plugins_features_459,
    plugins_features_464,
    plugins_features_470,
    plugins_features_473,
    plugins_features_478,
    plugins_features_484,
    plugins_features_487,
    plugins_features_49,
    plugins_features_492,
    plugins_features_499,
    plugins_features_502,
    plugins_features_507,
    plugins_features_513,
    plugins_features_516,
    plugins_features_521,
    plugins_features_527,
    plugins_features_530,
    plugins_features_535,
    plugins_features_541,
    plugins_features_544,
    plugins_features_549,
    plugins_features_55,
    plugins_features_58,
    plugins_features_63,
    plugins_features_69,
    plugins_features_72,
    plugins_features_77,
    plugins_features_83,
    plugins_features_86,
    plugins_features_91,
    plugins_features_97,
)

async def handle_feature_toggles(c, m, k, text, channel):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    r = get_redis()
    Dev_FINAL = get_dev_final()
    if not await check_global_restrictions(c, m, k):
        return    
    if text == "تعطيل الترحيب":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_features_27(k))
        else:
            if await r.get(f"{m.chat.id}:disableWelcome:{Dev_FINAL}"):
                return await m.reply(
                    plugins_features_30(k, m.from_user.mention(), k)
                )
            else:
                await r.set(f"{m.chat.id}:disableWelcome:{Dev_FINAL}", 1)
                return await m.reply(
                    plugins_features_35(k, m.from_user.mention(), k)
                )

    if text == "تفعيل الترحيب":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_features_41(k))
        else:
            if not await r.get(f"{m.chat.id}:disableWelcome:{Dev_FINAL}"):
                return await m.reply(
                    plugins_features_44(k, m.from_user.mention(), k)
                )
            else:
                await r.delete(f"{m.chat.id}:disableWelcome:{Dev_FINAL}")
                return await m.reply(
                    plugins_features_49(k, m.from_user.mention(), k)
                )

    if text == "تعطيل الترحيب بالصورة" or text == "تعطيل الترحيب بالصوره":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_features_55(k))
        else:
            if await r.get(f"{m.chat.id}:disableWelcomep:{Dev_FINAL}"):
                return await m.reply(
                    plugins_features_58(k, m.from_user.mention(), k)
                )
            else:
                await r.set(f"{m.chat.id}:disableWelcomep:{Dev_FINAL}", 1)
                return await m.reply(
                    plugins_features_63(k, m.from_user.mention(), k)
                )

    if text == "تفعيل الترحيب بالصورة" or text == "تفعيل الترحيب بالصوره":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_features_69(k))
        else:
            if not await r.get(f"{m.chat.id}:disableWelcomep:{Dev_FINAL}"):
                return await m.reply(
                    plugins_features_72(k, m.from_user.mention(), k)
                )
            else:
                await r.delete(f"{m.chat.id}:disableWelcomep:{Dev_FINAL}")
                return await m.reply(
                    plugins_features_77(k, m.from_user.mention(), k)
                )

    if text == "تعطيل الرابط":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_features_83(k))
        else:
            if await r.get(f"{m.chat.id}:disableLINK:{Dev_FINAL}"):
                return await m.reply(
                    plugins_features_86(k, m.from_user.mention(), k)
                )
            else:
                await r.set(f"{m.chat.id}:disableLINK:{Dev_FINAL}", 1)
                return await m.reply(
                    plugins_features_91(k, m.from_user.mention(), k)
                )

    if text == "تفعيل الرابط":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_features_97(k))
        else:
            if not await r.get(f"{m.chat.id}:disableLINK:{Dev_FINAL}"):
                return await m.reply(
                    plugins_features_100(k, m.from_user.mention(), k)
                )
            else:
                await r.delete(f"{m.chat.id}:disableLINK:{Dev_FINAL}")
                return await m.reply(
                    plugins_features_105(k, m.from_user.mention(), k)
                )

    if text == "تعطيل البايو":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_features_111(k))
        else:
            if await r.get(f"{m.chat.id}:disableBio:{Dev_FINAL}"):
                return await m.reply(
                    plugins_features_114(k, m.from_user.mention(), k)
                )
            else:
                await r.set(f"{m.chat.id}:disableBio:{Dev_FINAL}", 1)
                return await m.reply(
                    plugins_features_119(k, m.from_user.mention(), k)
                )

    if text == "تفعيل البايو":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_features_125(k))
        else:
            if not await r.get(f"{m.chat.id}:disableBio:{Dev_FINAL}"):
                return await m.reply(
                    plugins_features_128(k, m.from_user.mention(), k)
                )
            else:
                await r.delete(f"{m.chat.id}:disableBio:{Dev_FINAL}")
                return await m.reply(
                    plugins_features_133(k, m.from_user.mention(), k)
                )

    if text == "تعطيل اطردني":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_features_139(k))
        else:
            if not await r.get(f"{m.chat.id}:enableKickMe:{Dev_FINAL}"):
                return await m.reply(
                    plugins_features_142(k, m.from_user.mention(), k)
                )
            else:
                await r.delete(f"{m.chat.id}:enableKickMe:{Dev_FINAL}")
                return await m.reply(
                    plugins_features_147(k, m.from_user.mention(), k)
                )

    if text == "تفعيل اطردني":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_features_153(k))
        else:
            if await r.get(f"{m.chat.id}:enableKickMe:{Dev_FINAL}"):
                return await m.reply(
                    plugins_features_156(k, m.from_user.mention(), k)
                )
            else:
                await r.set(f"{m.chat.id}:enableKickMe:{Dev_FINAL}", 1)
                return await m.reply(
                    plugins_features_161(k, m.from_user.mention(), k)
                )

    if text == "تعطيل التحقق":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_features_167(k))
        else:
            if not await r.get(f"{m.chat.id}:enableVerify:{Dev_FINAL}"):
                return await m.reply(
                    plugins_features_170(k, m.from_user.mention(), k)
                )
            else:
                await r.delete(f"{m.chat.id}:enableVerify:{Dev_FINAL}")
                return await m.reply(
                    plugins_features_175(k, m.from_user.mention(), k)
                )

    if text == "تفعيل التحقق":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_features_181(k))
        else:
            if await r.get(f"{m.chat.id}:enableVerify:{Dev_FINAL}"):
                return await m.reply(
                    plugins_features_184(k, m.from_user.mention(), k)
                )
            else:
                await r.set(f"{m.chat.id}:enableVerify:{Dev_FINAL}", 1)
                return await m.reply(
                    plugins_features_189(k, m.from_user.mention(), k)
                )

    if text == "تعطيل انطقي" or text == "تعطيل انطق":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_features_195(k))
        else:
            if await r.get(f"{m.chat.id}:disableSay:{Dev_FINAL}"):
                return await m.reply(
                    plugins_features_198(k, m.from_user.mention(), k)
                )
            else:
                await r.set(f"{m.chat.id}:disableSay:{Dev_FINAL}", 1)
                return await m.reply(
                    plugins_features_203(k, m.from_user.mention(), k)
                )

    if text == "تفعيل انطقي" or text == "تفعيل انطق":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_features_209(k))
        else:
            if not await r.get(f"{m.chat.id}:disableSay:{Dev_FINAL}"):
                return await m.reply(
                    plugins_features_212(k, m.from_user.mention(), k)
                )
            else:
                await r.delete(f"{m.chat.id}:disableSay:{Dev_FINAL}")
                return await m.reply(
                    plugins_features_217(k, m.from_user.mention(), k)
                )

    if text == "تعطيل المنشن":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_features_223(k))
        else:
            if await r.get(f"{m.chat.id}:disableALL:{Dev_FINAL}"):
                return await m.reply(plugins_features_226(k, m.from_user.mention(), k))
            else:
                await r.set(f"{m.chat.id}:disableALL:{Dev_FINAL}", 1)
                return await m.reply(plugins_features_229(k, m.from_user.mention(), k))

    if text == "تفعيل المنشن":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_features_233(k))
        else:
            if not await r.get(f"{m.chat.id}:disableALL:{Dev_FINAL}"):
                return await m.reply(plugins_features_236(k, m.from_user.mention(), k))
            else:
                await r.delete(f"{m.chat.id}:disableALL:{Dev_FINAL}")
                return await m.reply(plugins_features_239(k, m.from_user.mention(), k))

    if text == "تعطيل التحذير":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_features_243(k))
        else:
            if await r.get(f"{m.chat.id}:disableWarn:{Dev_FINAL}"):
                return await m.reply(
                    plugins_features_246(k, m.from_user.mention(), k)
                )
            else:
                await r.set(f"{m.chat.id}:disableWarn:{Dev_FINAL}", 1)
                return await m.reply(
                    plugins_features_251(k, m.from_user.mention(), k)
                )

    if text == "تفعيل التحذير":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_features_257(k))
        else:
            if not await r.get(f"{m.chat.id}:disableWarn:{Dev_FINAL}"):
                return await m.reply(
                    plugins_features_260(k, m.from_user.mention(), k)
                )
            else:
                await r.delete(f"{m.chat.id}:disableWarn:{Dev_FINAL}")
                return await m.reply(
                    plugins_features_265(k, m.from_user.mention(), k)
                )

    if text == "تعطيل ال8888يوتيوب":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_features_271(k))
        else:
            if await r.get(f"{m.chat.id}:disableYT:{Dev_FINAL}"):
                return await m.reply(
                    plugins_features_274(k, m.from_user.mention(), k)
                )
            else:
                await r.set(f"{m.chat.id}:disableYT:{Dev_FINAL}", 1)
                return await m.reply(
                    plugins_features_279(k, m.from_user.mention(), k)
                )

    if text == "تفعيل8888 اليوتيوب":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_features_285(k))
        else:
            if not await r.get(f"{m.chat.id}:disableYT:{Dev_FINAL}"):
                return await m.reply(
                    plugins_features_288(k, m.from_user.mention(), k)
                )
            else:
                await r.delete(f"{m.chat.id}:disableYT:{Dev_FINAL}")
                return await m.reply(
                    plugins_features_293(k, m.from_user.mention(), k)
                )

    if text == "تعطيل الساوند":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_features_299(k))
        else:
            if await r.get(f"{m.chat.id}:disableSound:{Dev_FINAL}"):
                return await m.reply(
                    plugins_features_302(k, m.from_user.mention(), k)
                )
            else:
                await r.set(f"{m.chat.id}:disableSound:{Dev_FINAL}", 1)
                return await m.reply(
                    plugins_features_307(k, m.from_user.mention(), k)
                )

    if text == "تفعيل الساوند":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_features_313(k))
        else:
            if not await r.get(f"{m.chat.id}:disableSound:{Dev_FINAL}"):
                return await m.reply(
                    plugins_features_316(k, m.from_user.mention(), k)
                )
            else:
                await r.delete(f"{m.chat.id}:disableSound:{Dev_FINAL}")
                return await m.reply(
                    plugins_features_321(k, m.from_user.mention(), k)
                )

    if text == "تعطيل الانستا":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_features_327(k))
        else:
            if await r.get(f"{m.chat.id}:disableINSTA:{Dev_FINAL}"):
                return await m.reply(
                    plugins_features_330(k, m.from_user.mention(), k)
                )
            else:
                await r.set(f"{m.chat.id}:disableINSTA:{Dev_FINAL}", 1)
                return await m.reply(
                    plugins_features_335(k, m.from_user.mention(), k)
                )

    if text == "تفعيل الانستا":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_features_341(k))
        else:
            if not await r.get(f"{m.chat.id}:disableINSTA:{Dev_FINAL}"):
                return await m.reply(
                    plugins_features_344(k, m.from_user.mention(), k)
                )
            else:
                await r.delete(f"{m.chat.id}:disableINSTA:{Dev_FINAL}")
                return await m.reply(
                    plugins_features_349(k, m.from_user.mention(), k)
                )




    if text == "تعطيل التيك":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_features_358(k))
        else:
            if await r.get(f"{m.chat.id}:disableTik:{Dev_FINAL}"):
                return await m.reply(
                    plugins_features_361(k, m.from_user.mention(), k)
                )
            else:
                await r.set(f"{m.chat.id}:disableTik:{Dev_FINAL}", 1)
                return await m.reply(
                    plugins_features_366(k, m.from_user.mention(), k)
                )

    if text == "تفعيل التيك":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_features_372(k))
        else:
            if not await r.get(f"{m.chat.id}:disableTik:{Dev_FINAL}"):
                return await m.reply(
                    plugins_features_375(k, m.from_user.mention(), k)
                )
            else:
                await r.delete(f"{m.chat.id}:disableTik:{Dev_FINAL}")
                return await m.reply(
                    plugins_features_380(k, m.from_user.mention(), k)
                )

    if text == "تعطيل شازام":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_features_386(k))
        else:
            if await r.get(f"{m.chat.id}:disableShazam:{Dev_FINAL}"):
                return await m.reply(
                    plugins_features_389(k, m.from_user.mention(), k)
                )
            else:
                await r.set(f"{m.chat.id}:disableShazam:{Dev_FINAL}", 1)
                return await m.reply(
                    plugins_features_394(k, m.from_user.mention(), k)
                )

    if text == "تفعيل شازام":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_features_400(k))
        else:
            if not await r.get(f"{m.chat.id}:disableShazam:{Dev_FINAL}"):
                return await m.reply(
                    plugins_features_403(k, m.from_user.mention(), k)
                )
            else:
                await r.delete(f"{m.chat.id}:disableShazam:{Dev_FINAL}")
                return await m.reply(
                    plugins_features_408(k, m.from_user.mention(), k)
                )

    if text == "تعطيل الالعاب":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_features_414(k))
        else:
            if await r.get(f"{m.chat.id}:disableGames:{Dev_FINAL}"):
                return await m.reply(
                    plugins_features_417(k, m.from_user.mention(), k)
                )
            else:
                await r.set(f"{m.chat.id}:disableGames:{Dev_FINAL}", 1)
                return await m.reply(
                    plugins_features_422(k, m.from_user.mention(), k)
                )

    if text == "تفعيل الالعاب":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_features_428(k))
        else:
            if not await r.get(f"{m.chat.id}:disableGames:{Dev_FINAL}"):
                return await m.reply(
                    plugins_features_431(k, m.from_user.mention(), k)
                )
            else:
                await r.delete(f"{m.chat.id}:disableGames:{Dev_FINAL}")
                return await m.reply(
                    plugins_features_436(k, m.from_user.mention(), k)
                )

    if text == "تعطيل الترجمة" or text == "تعطيل الترجمه":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_features_442(k))
        else:
            if await r.get(f"{m.chat.id}:disableTrans:{Dev_FINAL}"):
                return await m.reply(
                    plugins_features_445(k, m.from_user.mention(), k)
                )
            else:
                await r.set(f"{m.chat.id}:disableTrans:{Dev_FINAL}", 1)
                return await m.reply(
                    plugins_features_450(k, m.from_user.mention(), k)
                )

    if text == "تفعيل الترجمة" or text == "تفعيل الترجمه":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_features_456(k))
        else:
            if not await r.get(f"{m.chat.id}:disableTrans:{Dev_FINAL}"):
                return await m.reply(
                    plugins_features_459(k, m.from_user.mention(), k)
                )
            else:
                await r.delete(f"{m.chat.id}:disableTrans:{Dev_FINAL}")
                return await m.reply(
                    plugins_features_464(k, m.from_user.mention(), k)
                )

    if text == "تعطيل التسلية" or text == "تعطيل التسليه":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_features_470(k))
        else:
            if await r.get(f"{m.chat.id}:disableFun:{Dev_FINAL}"):
                return await m.reply(
                    plugins_features_473(k, m.from_user.mention(), k)
                )
            else:
                await r.set(f"{m.chat.id}:disableFun:{Dev_FINAL}", 1)
                return await m.reply(
                    plugins_features_478(k, m.from_user.mention(), k)
                )

    if text == "تفعيل التسلية" or text == "تفعيل التسليه":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_features_484(k))
        else:
            if not await r.get(f"{m.chat.id}:disableFun:{Dev_FINAL}"):
                return await m.reply(
                    plugins_features_487(k, m.from_user.mention(), k)
                )
            else:
                await r.delete(f"{m.chat.id}:disableFun:{Dev_FINAL}")
                return await m.reply(
                    plugins_features_492(k, m.from_user.mention(), k)
                )


    if text == "تعطيل اهمس":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_features_499(k))
        else:
            if await r.get(f"{Dev_FINAL}:whisper_{m.chat.id}") == "off":
                return await m.reply(
                    plugins_features_502(k, m.from_user.mention(), k)
                )
            else:
                await r.set(f"{Dev_FINAL}:whisper_{m.chat.id}", "off")
                return await m.reply(
                    plugins_features_507(k, m.from_user.mention(), k)
                )

    if text == "تفعيل اهمس":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_features_513(k))
        else:
            if await r.get(f"{Dev_FINAL}:whisper_{m.chat.id}") != "off":
                return await m.reply(
                    plugins_features_516(k, m.from_user.mention(), k)
                )
            else:
                await r.delete(f"{Dev_FINAL}:whisper_{m.chat.id}")
                return await m.reply(
                    plugins_features_521(k, m.from_user.mention(), k)
                )

    # أوامر "تعطيل/تفعيل الاشتراك" القديمة (عالمية) أُزيلت — الاشتراك الاجباري
    # الآن لكل قروب عبر "اضف اشتراك @..." / "حذف الاشتراك الاجباري"
    # (plugins/force_subscribe.py)

    return None
