from helpers.context import get_global_r, get_global_dev, get_global_k
r = get_global_r()
Dev_FINAL = get_global_dev()
k = get_global_k()
from threading import Thread
from compat import *
from compat import *
from helpers.ranks import *
from .protect import *
from helpers.replies_store import (
    plugins_locks_1000,
    plugins_locks_1003,
    plugins_locks_1006,
    plugins_locks_1010,
    plugins_locks_1013,
    plugins_locks_1016,
    plugins_locks_1020,
    plugins_locks_1023,
    plugins_locks_1026,
    plugins_locks_1030,
    plugins_locks_1033,
    plugins_locks_1036,
    plugins_locks_1040,
    plugins_locks_1043,
    plugins_locks_1046,
    plugins_locks_1051,
    plugins_locks_1054,
    plugins_locks_1056,
    plugins_locks_1061,
    plugins_locks_1064,
    plugins_locks_1066,
    plugins_locks_1071,
    plugins_locks_1075,
    plugins_locks_1077,
    plugins_locks_1082,
    plugins_locks_1086,
    plugins_locks_1088,
    plugins_locks_1093,
    plugins_locks_1097,
    plugins_locks_1099,
    plugins_locks_1104,
    plugins_locks_1108,
    plugins_locks_1110,
    plugins_locks_1115,
    plugins_locks_1119,
    plugins_locks_1121,
    plugins_locks_1126,
    plugins_locks_1130,
    plugins_locks_1132,
    plugins_locks_1137,
    plugins_locks_1141,
    plugins_locks_1143,
    plugins_locks_1148,
    plugins_locks_1152,
    plugins_locks_1154,
    plugins_locks_1159,
    plugins_locks_1163,
    plugins_locks_1165,
    plugins_locks_1170,
    plugins_locks_1174,
    plugins_locks_1176,
    plugins_locks_1180,
    plugins_locks_1182,
    plugins_locks_1185,
    plugins_locks_1189,
    plugins_locks_1191,
    plugins_locks_1194,
    plugins_locks_150,
    plugins_locks_186,
    plugins_locks_190,
    plugins_locks_227,
    plugins_locks_263,
    plugins_locks_267,
    plugins_locks_305,
    plugins_locks_326,
    plugins_locks_330,
    plugins_locks_353,
    plugins_locks_374,
    plugins_locks_378,
    plugins_locks_400,
    plugins_locks_403,
    plugins_locks_406,
    plugins_locks_410,
    plugins_locks_413,
    plugins_locks_416,
    plugins_locks_420,
    plugins_locks_423,
    plugins_locks_426,
    plugins_locks_430,
    plugins_locks_433,
    plugins_locks_436,
    plugins_locks_440,
    plugins_locks_443,
    plugins_locks_446,
    plugins_locks_450,
    plugins_locks_453,
    plugins_locks_456,
    plugins_locks_460,
    plugins_locks_463,
    plugins_locks_466,
    plugins_locks_470,
    plugins_locks_473,
    plugins_locks_476,
    plugins_locks_480,
    plugins_locks_483,
    plugins_locks_486,
    plugins_locks_490,
    plugins_locks_493,
    plugins_locks_496,
    plugins_locks_500,
    plugins_locks_503,
    plugins_locks_506,
    plugins_locks_51,
    plugins_locks_510,
    plugins_locks_513,
    plugins_locks_516,
    plugins_locks_520,
    plugins_locks_523,
    plugins_locks_527,
    plugins_locks_531,
    plugins_locks_534,
    plugins_locks_538,
    plugins_locks_542,
    plugins_locks_545,
    plugins_locks_548,
    plugins_locks_552,
    plugins_locks_555,
    plugins_locks_558,
    plugins_locks_562,
    plugins_locks_565,
    plugins_locks_568,
    plugins_locks_572,
    plugins_locks_575,
    plugins_locks_578,
    plugins_locks_582,
    plugins_locks_585,
    plugins_locks_588,
    plugins_locks_592,
    plugins_locks_595,
    plugins_locks_598,
    plugins_locks_602,
    plugins_locks_605,
    plugins_locks_609,
    plugins_locks_613,
    plugins_locks_616,
    plugins_locks_620,
    plugins_locks_624,
    plugins_locks_627,
    plugins_locks_631,
    plugins_locks_635,
    plugins_locks_638,
    plugins_locks_642,
    plugins_locks_646,
    plugins_locks_649,
    plugins_locks_652,
    plugins_locks_656,
    plugins_locks_659,
    plugins_locks_662,
    plugins_locks_666,
    plugins_locks_669,
    plugins_locks_672,
    plugins_locks_676,
    plugins_locks_679,
    plugins_locks_682,
    plugins_locks_686,
    plugins_locks_689,
    plugins_locks_692,
    plugins_locks_696,
    plugins_locks_699,
    plugins_locks_702,
    plugins_locks_706,
    plugins_locks_709,
    plugins_locks_712,
    plugins_locks_716,
    plugins_locks_719,
    plugins_locks_722,
    plugins_locks_726,
    plugins_locks_729,
    plugins_locks_732,
    plugins_locks_736,
    plugins_locks_739,
    plugins_locks_742,
    plugins_locks_746,
    plugins_locks_749,
    plugins_locks_752,
    plugins_locks_756,
    plugins_locks_759,
    plugins_locks_762,
    plugins_locks_766,
    plugins_locks_769,
    plugins_locks_773,
    plugins_locks_777,
    plugins_locks_780,
    plugins_locks_784,
    plugins_locks_788,
    plugins_locks_791,
    plugins_locks_794,
    plugins_locks_798,
    plugins_locks_801,
    plugins_locks_804,
    plugins_locks_808,
    plugins_locks_811,
    plugins_locks_814,
    plugins_locks_818,
    plugins_locks_821,
    plugins_locks_824,
    plugins_locks_828,
    plugins_locks_831,
    plugins_locks_834,
    plugins_locks_838,
    plugins_locks_841,
    plugins_locks_844,
    plugins_locks_848,
    plugins_locks_851,
    plugins_locks_854,
    plugins_locks_858,
    plugins_locks_861,
    plugins_locks_864,
    plugins_locks_868,
    plugins_locks_871,
    plugins_locks_874,
    plugins_locks_878,
    plugins_locks_881,
    plugins_locks_884,
    plugins_locks_888,
    plugins_locks_891,
    plugins_locks_894,
    plugins_locks_898,
    plugins_locks_901,
    plugins_locks_904,
    plugins_locks_908,
    plugins_locks_911,
    plugins_locks_914,
    plugins_locks_918,
    plugins_locks_921,
    plugins_locks_924,
    plugins_locks_928,
    plugins_locks_931,
    plugins_locks_935,
    plugins_locks_939,
    plugins_locks_942,
    plugins_locks_946,
    plugins_locks_95,
    plugins_locks_950,
    plugins_locks_953,
    plugins_locks_956,
    plugins_locks_960,
    plugins_locks_963,
    plugins_locks_966,
    plugins_locks_970,
    plugins_locks_973,
    plugins_locks_976,
    plugins_locks_980,
    plugins_locks_983,
    plugins_locks_986,
    plugins_locks_990,
    plugins_locks_993,
    plugins_locks_996,
)


async def handle_lock_commands(c, m, k, text):
    r = get_global_r()
    Dev_FINAL = get_global_dev()
    k = get_global_k()
    
    
    

    

    
    

    if text == "الاعدادات":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_51(k))
        else:
            x1 = "مقفول" if await r.get(f"{m.chat.id}:lockAudios:{Dev_FINAL}") else "مفتوح"
            x2 = "مقفول" if await r.get(f"{m.chat.id}:lockVideo:{Dev_FINAL}") else "مفتوح"
            x3 = "مقفول" if await r.get(f"{m.chat.id}:lockVoice:{Dev_FINAL}") else "مفتوح"
            x4 = "مقفول" if await r.get(f"{m.chat.id}:lockPhoto:{Dev_FINAL}") else "مفتوح"
            x5 = "مقفول" if await r.get(f"{m.chat.id}:mute:{Dev_FINAL}") else "مفتوح"
            x6 = "مقفول" if await r.get(f"{m.chat.id}:lockInline:{Dev_FINAL}") else "مفتوح"
            x7 = "مقفول" if await r.get(f"{m.chat.id}:lockForward:{Dev_FINAL}") else "مفتوح"
            x8 = "مقفول" if await r.get(f"{m.chat.id}:lockHashtags:{Dev_FINAL}") else "مفتوح"
            x9 = "مقفول" if await r.get(f"{m.chat.id}:lockEdit:{Dev_FINAL}") else "مفتوح"
            x10 = "مقفول" if await r.get(f"{m.chat.id}:lockStickers:{Dev_FINAL}") else "مفتوح"
            x11 = "مقفول" if await r.get(f"{m.chat.id}:lockFiles:{Dev_FINAL}") else "مفتوح"
            x12 = "مقفول" if await r.get(f"{m.chat.id}:lockAnimations:{Dev_FINAL}") else "مفتوح"
            x13 = "مقفول" if await r.get(f"{m.chat.id}:lockUrls:{Dev_FINAL}") else "مفتوح"
            x14 = "مقفول" if await r.get(f"{m.chat.id}:lockBots:{Dev_FINAL}") else "مفتوح"
            x15 = "مقفول" if await r.get(f"{m.chat.id}:lockTags:{Dev_FINAL}") else "مفتوح"
            x16 = "مقفول" if await r.get(f"{m.chat.id}:lockNot:{Dev_FINAL}") else "مفتوح"
            x17 = "مقفول" if await r.get(f"{m.chat.id}:lockaddContacts:{Dev_FINAL}") else "مفتوح"
            x18 = "مقفول" if await r.get(f"{m.chat.id}:lockMessages:{Dev_FINAL}") else "مفتوح"
            x19 = "مقفول" if await r.get(f"{m.chat.id}:lockSHTM:{Dev_FINAL}") else "مفتوح"
            x20 = "مقفول" if await r.get(f"{m.chat.id}:lockSpam:{Dev_FINAL}") else "مفتوح"
            x21 = "مقفول" if await r.get(f"{m.chat.id}:lockChannels:{Dev_FINAL}") else "مفتوح"
            x22 = "مقفول" if await r.get(f"{m.chat.id}:lockEditM:{Dev_FINAL}") else "مفتوح"
            x23 = "مقفول" if await r.get(f"{m.chat.id}:lockJoin:{Dev_FINAL}") else "مفتوح"
            x24 = "مقفول" if await r.get(f"{m.chat.id}:lockPersian:{Dev_FINAL}") else "مفتوح"
            x25 = "مقفول" if await r.get(f"{m.chat.id}:lockJoinPersian:{Dev_FINAL}") else "مفتوح"
            x26 = "مقفول" if await r.get(f"{m.chat.id}:lockNSFW:{Dev_FINAL}") else "مفتوح"
            x27 = "مقفول" if await r.get(f"{m.chat.id}:lockFakeName:{Dev_FINAL}") else "مفتوح"
            x28 = "مقفول" if await r.get(f"{m.chat.id}:lockQuote:{Dev_FINAL}") else "مفتوح"
            x29 = "مقفول" if await r.get(f"{m.chat.id}:lockDash:{Dev_FINAL}") else "مفتوح"
            x30 = "مقفول" if await r.get(f"{m.chat.id}:lockPremiumEmoji:{Dev_FINAL}") else "مفتوح"
            x31 = "مقفول" if await r.get(f"{m.chat.id}:lockText:{Dev_FINAL}") else "مفتوح"
            x32 = "مقفول" if await r.get(f"{m.chat.id}:lockGamthon:{Dev_FINAL}") else "مفتوح"
            x33 = "مقفول" if await r.get(f"{m.chat.id}:BotNotifications:{Dev_FINAL}") else "مفتوح"
            
            x34 = "مقفول" if await r.get(f"{m.chat.id}:lockPhotoRestrict:{Dev_FINAL}") else "مفتوح"
            x35 = "مقفول" if await r.get(f"{m.chat.id}:lockVideoRestrict:{Dev_FINAL}") else "مفتوح"
            x36 = "مقفول" if await r.get(f"{m.chat.id}:lockAnimationsRestrict:{Dev_FINAL}") else "مفتوح"
            x37 = "مقفول" if await r.get(f"{m.chat.id}:lockUrlsRestrict:{Dev_FINAL}") else "مفتوح"
            x38 = "مقفول" if await r.get(f"{m.chat.id}:lockForwardRestrict:{Dev_FINAL}") else "مفتوح"
            x39 = "مقفول" if await r.get(f"{m.chat.id}:lockJoinRestrict:{Dev_FINAL}") else "مفتوح"

            channel = await r.get(f"{Dev_FINAL}:BotChannel") if await r.get(f"{Dev_FINAL}:BotChannel") else ''
            return await m.reply(plugins_locks_95(k, x1, k, x2, k, x3, k, x4, k, x5, k, x6, k, x7, k, x8, k, x9, k, x10, k, x11, k, x12, k, x13, k, x14, k, x15, k, x16, k, x17, k, x18, k, x19, k, x20, k, x21, k, x22, k, x23, k, x24, k, x25, k, x26, k, x27, k, x28, k, x29, k, x30, k, x31, k, x32, k, x33, k, x34, k, x35, k, x36, k, x37, k, x38, k, x39, channel))

    if text == "قفل الكل":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_150(k))
        else:
            if (
                await r.get(f"{m.chat.id}:mute:{Dev_FINAL}")
                and await r.get(f"{m.chat.id}:lockEdit:{Dev_FINAL}")
                and await r.get(f"{m.chat.id}:lockEditM:{Dev_FINAL}")
                and await r.get(f"{m.chat.id}:lockVoice:{Dev_FINAL}")
                and await r.get(f"{m.chat.id}:lockVideo:{Dev_FINAL}")
                and await r.get(f"{m.chat.id}:lockNot:{Dev_FINAL}")
                and await r.get(f"{m.chat.id}:lockPhoto:{Dev_FINAL}")
                and await r.get(f"{m.chat.id}:lockPersian:{Dev_FINAL}")
                and await r.get(f"{m.chat.id}:lockStickers:{Dev_FINAL}")
                and await r.get(f"{m.chat.id}:lockFiles:{Dev_FINAL}")
                and await r.get(f"{m.chat.id}:lockAnimations:{Dev_FINAL}")
                and await r.get(f"{m.chat.id}:lockUrls:{Dev_FINAL}")
                and await r.get(f"{m.chat.id}:lockHashtags:{Dev_FINAL}")
                and await r.get(f"{m.chat.id}:lockBots:{Dev_FINAL}")
                and await r.get(f"{m.chat.id}:lockTags:{Dev_FINAL}")
                and await r.get(f"{m.chat.id}:lockMessages:{Dev_FINAL}")
                and await r.get(f"{m.chat.id}:lockSpam:{Dev_FINAL}")
                and await r.get(f"{m.chat.id}:lockForward:{Dev_FINAL}")
                and await r.get(f"{m.chat.id}:lockSHTM:{Dev_FINAL}")
                and await r.get(f"{m.chat.id}:lockaddContacts:{Dev_FINAL}")
                and await r.get(f"{m.chat.id}:lockAudios:{Dev_FINAL}")
                and await r.get(f"{m.chat.id}:lockChannels:{Dev_FINAL}")
                and await r.get(f"{m.chat.id}:lockJoin:{Dev_FINAL}")
                and await r.get(f"{m.chat.id}:lockInline:{Dev_FINAL}")
                and await r.get(f"{m.chat.id}:lockNSFW:{Dev_FINAL}")
                and await r.get(f"{m.chat.id}:lockFakeName:{Dev_FINAL}")
                and await r.get(f"{m.chat.id}:lockQuote:{Dev_FINAL}")
                and await r.get(f"{m.chat.id}:lockDash:{Dev_FINAL}")
                and await r.get(f"{m.chat.id}:lockPremiumEmoji:{Dev_FINAL}")
                and await r.get(f"{m.chat.id}:lockText:{Dev_FINAL}")
                and await r.get(f"{m.chat.id}:lockGamthon:{Dev_FINAL}")
                and await r.get(f"{m.chat.id}:lockJoinRestrict:{Dev_FINAL}")
            ):
                return await m.reply(
                    plugins_locks_186(k, m.from_user.mention(), k)
                )
            else:
                await m.reply(plugins_locks_190(k, m.from_user.mention(), k))
                await r.set(f"{m.chat.id}:mute:{Dev_FINAL}", 1)
                await r.set(f"{m.chat.id}:lockJoin:{Dev_FINAL}", 1)
                await r.set(f"{m.chat.id}:lockChannels:{Dev_FINAL}", 1)
                await r.set(f"{m.chat.id}:lockEdit:{Dev_FINAL}", 1)
                await r.set(f"{m.chat.id}:lockEditM:{Dev_FINAL}", 1)
                await r.set(f"{m.chat.id}:lockVoice:{Dev_FINAL}", 1)
                await r.set(f"{m.chat.id}:lockVideo:{Dev_FINAL}", 1)
                await r.set(f"{m.chat.id}:lockNot:{Dev_FINAL}", 1)
                await r.set(f"{m.chat.id}:lockPhoto:{Dev_FINAL}", 1)
                await r.set(f"{m.chat.id}:lockStickers:{Dev_FINAL}", 1)
                await r.set(f"{m.chat.id}:lockAnimations:{Dev_FINAL}", 1)
                await r.set(f"{m.chat.id}:lockFiles:{Dev_FINAL}", 1)
                await r.set(f"{m.chat.id}:lockPersian:{Dev_FINAL}", 1)
                await r.set(f"{m.chat.id}:lockUrls:{Dev_FINAL}", 1)
                await r.set(f"{m.chat.id}:lockHashtags:{Dev_FINAL}", 1)
                await r.set(f"{m.chat.id}:lockMessages:{Dev_FINAL}", 1)
                await r.set(f"{m.chat.id}:lockTags:{Dev_FINAL}", 1)
                await r.set(f"{m.chat.id}:lockBots:{Dev_FINAL}", 1)
                await r.set(f"{m.chat.id}:lockSpam:{Dev_FINAL}", 1)
                await r.set(f"{m.chat.id}:lockInline:{Dev_FINAL}", 1)
                await r.set(f"{m.chat.id}:lockForward:{Dev_FINAL}", 1)
                await r.set(f"{m.chat.id}:lockAudios:{Dev_FINAL}", 1)
                await r.set(f"{m.chat.id}:lockaddContacts:{Dev_FINAL}", 1)
                await r.set(f"{m.chat.id}:lockSHTM:{Dev_FINAL}", 1)
                await r.set(f"{m.chat.id}:lockNSFW:{Dev_FINAL}", 1)
                await r.set(f"{m.chat.id}:lockFakeName:{Dev_FINAL}", 1)
                await r.set(f"{m.chat.id}:lockQuote:{Dev_FINAL}", 1)
                await r.set(f"{m.chat.id}:lockDash:{Dev_FINAL}", 1)
                await r.set(f"{m.chat.id}:lockPremiumEmoji:{Dev_FINAL}", 1)
                await r.set(f"{m.chat.id}:lockText:{Dev_FINAL}", 1)
                await r.set(f"{m.chat.id}:lockGamthon:{Dev_FINAL}", 1)
                await r.set(f"{m.chat.id}:lockJoinRestrict:{Dev_FINAL}", 1)
                return False

    if text == "فتح الكل":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_227(k))
        else:
            if (
                not await r.get(f"{m.chat.id}:mute:{Dev_FINAL}")
                and not await r.get(f"{m.chat.id}:lockEdit:{Dev_FINAL}")
                and not await r.get(f"{m.chat.id}:lockEditM:{Dev_FINAL}")
                and not await r.get(f"{m.chat.id}:lockVoice:{Dev_FINAL}")
                and not await r.get(f"{m.chat.id}:lockVideo:{Dev_FINAL}")
                and not await r.get(f"{m.chat.id}:lockNot:{Dev_FINAL}")
                and not await r.get(f"{m.chat.id}:lockPhoto:{Dev_FINAL}")
                and not await r.get(f"{m.chat.id}:lockPersian:{Dev_FINAL}")
                and not await r.get(f"{m.chat.id}:lockStickers:{Dev_FINAL}")
                and not await r.get(f"{m.chat.id}:lockFiles:{Dev_FINAL}")
                and not await r.get(f"{m.chat.id}:lockAnimations:{Dev_FINAL}")
                and not await r.get(f"{m.chat.id}:lockUrls:{Dev_FINAL}")
                and not await r.get(f"{m.chat.id}:lockHashtags:{Dev_FINAL}")
                and not await r.get(f"{m.chat.id}:lockBots:{Dev_FINAL}")
                and not await r.get(f"{m.chat.id}:lockTags:{Dev_FINAL}")
                and not await r.get(f"{m.chat.id}:lockMessages:{Dev_FINAL}")
                and not await r.get(f"{m.chat.id}:lockSpam:{Dev_FINAL}")
                and not await r.get(f"{m.chat.id}:lockForward:{Dev_FINAL}")
                and not await r.get(f"{m.chat.id}:lockSHTM:{Dev_FINAL}")
                and not await r.get(f"{m.chat.id}:lockaddContacts:{Dev_FINAL}")
                and not await r.get(f"{m.chat.id}:lockAudios:{Dev_FINAL}")
                and not await r.get(f"{m.chat.id}:lockChannels:{Dev_FINAL}")
                and not await r.get(f"{m.chat.id}:lockJoin:{Dev_FINAL}")
                and not await r.get(f"{m.chat.id}:lockInline:{Dev_FINAL}")
                and not await r.get(f"{m.chat.id}:lockNSFW:{Dev_FINAL}")
                and not await r.get(f"{m.chat.id}:lockFakeName:{Dev_FINAL}")
                and not await r.get(f"{m.chat.id}:lockQuote:{Dev_FINAL}")
                and not await r.get(f"{m.chat.id}:lockDash:{Dev_FINAL}")
                and not await r.get(f"{m.chat.id}:lockPremiumEmoji:{Dev_FINAL}")
                and not await r.get(f"{m.chat.id}:lockText:{Dev_FINAL}")
                and not await r.get(f"{m.chat.id}:lockGamthon:{Dev_FINAL}")
                and not await r.get(f"{m.chat.id}:lockJoinRestrict:{Dev_FINAL}")
            ):
                return await m.reply(
                    plugins_locks_263(k, m.from_user.mention(), k)
                )
            else:
                await m.reply(plugins_locks_267(k, m.from_user.mention(), k))
                await r.delete(f"{m.chat.id}:mute:{Dev_FINAL}")
                await r.delete(f"{m.chat.id}:lockJoin:{Dev_FINAL}")
                await r.delete(f"{m.chat.id}:lockChannels:{Dev_FINAL}")
                await r.delete(f"{m.chat.id}:lockEdit:{Dev_FINAL}")
                await r.delete(f"{m.chat.id}:lockEditM:{Dev_FINAL}")
                await r.delete(f"{m.chat.id}:lockVoice:{Dev_FINAL}")
                await r.delete(f"{m.chat.id}:lockVideo:{Dev_FINAL}")
                await r.delete(f"{m.chat.id}:lockNot:{Dev_FINAL}")
                await r.delete(f"{m.chat.id}:lockPhoto:{Dev_FINAL}")
                await r.delete(f"{m.chat.id}:lockStickers:{Dev_FINAL}")
                await r.delete(f"{m.chat.id}:lockAnimations:{Dev_FINAL}")
                await r.delete(f"{m.chat.id}:lockFiles:{Dev_FINAL}")
                await r.delete(f"{m.chat.id}:lockPersian:{Dev_FINAL}")
                await r.delete(f"{m.chat.id}:lockUrls:{Dev_FINAL}")
                await r.delete(f"{m.chat.id}:lockHashtags:{Dev_FINAL}")
                await r.delete(f"{m.chat.id}:lockMessages:{Dev_FINAL}")
                await r.delete(f"{m.chat.id}:lockTags:{Dev_FINAL}")
                await r.delete(f"{m.chat.id}:lockBots:{Dev_FINAL}")
                await r.delete(f"{m.chat.id}:lockSpam:{Dev_FINAL}")
                await r.delete(f"{m.chat.id}:lockInline:{Dev_FINAL}")
                await r.delete(f"{m.chat.id}:lockForward:{Dev_FINAL}")
                await r.delete(f"{m.chat.id}:lockAudios:{Dev_FINAL}")
                await r.delete(f"{m.chat.id}:lockaddContacts:{Dev_FINAL}")
                await r.delete(f"{m.chat.id}:lockSHTM:{Dev_FINAL}")
                await r.delete(f"{m.chat.id}:lockKFR:{Dev_FINAL}")
                await r.delete(f"{m.chat.id}:lockNSFW:{Dev_FINAL}")
                await r.delete(f"{m.chat.id}:lockFakeName:{Dev_FINAL}")
                await r.delete(f"{m.chat.id}:lockQuote:{Dev_FINAL}")
                await r.delete(f"{m.chat.id}:lockDash:{Dev_FINAL}")
                await r.delete(f"{m.chat.id}:lockPremiumEmoji:{Dev_FINAL}")
                await r.delete(f"{m.chat.id}:lockText:{Dev_FINAL}")
                await r.delete(f"{m.chat.id}:lockGamthon:{Dev_FINAL}")
                await r.delete(f"{m.chat.id}:lockJoinRestrict:{Dev_FINAL}")
                return False

    if text == "تفعيل الحماية" or text == "تفعيل الحمايه":
        if not await owner_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_305(k))
        else:
            if (
                await r.get(f"{m.chat.id}:lockEditM:{Dev_FINAL}")
                and await r.get(f"{m.chat.id}:lockVoice:{Dev_FINAL}")
                and await r.get(f"{m.chat.id}:lockVideo:{Dev_FINAL}")
                and await r.get(f"{m.chat.id}:lockPhoto:{Dev_FINAL}")
                and await r.get(f"{m.chat.id}:lockPersian:{Dev_FINAL}")
                and await r.get(f"{m.chat.id}:lockStickers:{Dev_FINAL}")
                and await r.get(f"{m.chat.id}:lockFiles:{Dev_FINAL}")
                and await r.get(f"{m.chat.id}:lockAnimations:{Dev_FINAL}")
                and await r.get(f"{m.chat.id}:lockUrls:{Dev_FINAL}")
                and await r.get(f"{m.chat.id}:lockTags:{Dev_FINAL}")
                and await r.get(f"{m.chat.id}:lockMessages:{Dev_FINAL}")
                and await r.get(f"{m.chat.id}:lockSpam:{Dev_FINAL}")
                and await r.get(f"{m.chat.id}:lockForward:{Dev_FINAL}")
                and await r.get(f"{m.chat.id}:lockSHTM:{Dev_FINAL}")
                and await r.get(f"{m.chat.id}:lockAudios:{Dev_FINAL}")
                and await r.get(f"{m.chat.id}:lockChannels:{Dev_FINAL}")
                and await r.get(f"{m.chat.id}:lockNSFW:{Dev_FINAL}")
            ):
                return await m.reply(
                    plugins_locks_326(k, m.from_user.mention(), k)
                )
            else:
                await m.reply(
                    plugins_locks_330(k, m.from_user.mention(), k)
                )
                await r.set(f"{m.chat.id}:lockChannels:{Dev_FINAL}", 1)
                await r.delete(f"{m.chat.id}:disableWarn:{Dev_FINAL}")
                await r.set(f"{m.chat.id}:lockVoice:{Dev_FINAL}", 1)
                await r.set(f"{m.chat.id}:lockVideo:{Dev_FINAL}", 1)
                await r.set(f"{m.chat.id}:lockPhoto:{Dev_FINAL}", 1)
                await r.set(f"{m.chat.id}:lockStickers:{Dev_FINAL}", 1)
                await r.set(f"{m.chat.id}:lockAnimations:{Dev_FINAL}", 1)
                await r.set(f"{m.chat.id}:lockFiles:{Dev_FINAL}", 1)
                await r.set(f"{m.chat.id}:lockPersian:{Dev_FINAL}", 1)
                await r.set(f"{m.chat.id}:lockUrls:{Dev_FINAL}", 1)
                await r.set(f"{m.chat.id}:lockTags:{Dev_FINAL}", 1)
                await r.set(f"{m.chat.id}:lockSpam:{Dev_FINAL}", 1)
                await r.set(f"{m.chat.id}:lockForward:{Dev_FINAL}", 1)
                await r.set(f"{m.chat.id}:lockAudios:{Dev_FINAL}", 1)
                await r.set(f"{m.chat.id}:lockSHTM:{Dev_FINAL}", 1)
                await r.set(f"{m.chat.id}:lockNSFW:{Dev_FINAL}", 1)
                return False

    if text == "تعطيل الحماية" or text == "تعطيل الحمايه":
        if not await owner_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_353(k))
        else:
            if (
                await r.get(f"{m.chat.id}:lockEditM:{Dev_FINAL}")
                and not await r.get(f"{m.chat.id}:lockVoice:{Dev_FINAL}")
                and not await r.get(f"{m.chat.id}:lockVideo:{Dev_FINAL}")
                and not await r.get(f"{m.chat.id}:lockPhoto:{Dev_FINAL}")
                and not await r.get(f"{m.chat.id}:lockPersian:{Dev_FINAL}")
                and not await r.get(f"{m.chat.id}:lockStickers:{Dev_FINAL}")
                and not await r.get(f"{m.chat.id}:lockFiles:{Dev_FINAL}")
                and not await r.get(f"{m.chat.id}:lockAnimations:{Dev_FINAL}")
                and not await r.get(f"{m.chat.id}:lockUrls:{Dev_FINAL}")
                and not await r.get(f"{m.chat.id}:lockTags:{Dev_FINAL}")
                and not await r.get(f"{m.chat.id}:lockMessages:{Dev_FINAL}")
                and not await r.get(f"{m.chat.id}:lockSpam:{Dev_FINAL}")
                and not await r.get(f"{m.chat.id}:lockForward:{Dev_FINAL}")
                and not await r.get(f"{m.chat.id}:lockSHTM:{Dev_FINAL}")
                and not await r.get(f"{m.chat.id}:lockAudios:{Dev_FINAL}")
                and not await r.get(f"{m.chat.id}:lockChannels:{Dev_FINAL}")
                and not await r.get(f"{m.chat.id}:lockNSFW:{Dev_FINAL}")
            ):
                return await m.reply(
                    plugins_locks_374(k, m.from_user.mention(), k)
                )
            else:
                await m.reply(
                    plugins_locks_378(k, m.from_user.mention(), k)
                )
                await r.delete(f"{m.chat.id}:lockChannels:{Dev_FINAL}")
                await r.delete(f"{m.chat.id}:lockVoice:{Dev_FINAL}")
                await r.delete(f"{m.chat.id}:lockVideo:{Dev_FINAL}")
                await r.delete(f"{m.chat.id}:lockPhoto:{Dev_FINAL}")
                await r.delete(f"{m.chat.id}:lockStickers:{Dev_FINAL}")
                await r.delete(f"{m.chat.id}:lockAnimations:{Dev_FINAL}")
                await r.delete(f"{m.chat.id}:lockFiles:{Dev_FINAL}")
                await r.delete(f"{m.chat.id}:lockPersian:{Dev_FINAL}")
                await r.delete(f"{m.chat.id}:lockUrls:{Dev_FINAL}")
                await r.delete(f"{m.chat.id}:lockTags:{Dev_FINAL}")
                await r.delete(f"{m.chat.id}:lockSpam:{Dev_FINAL}")
                await r.delete(f"{m.chat.id}:lockForward:{Dev_FINAL}")
                await r.delete(f"{m.chat.id}:lockAudios:{Dev_FINAL}")
                await r.delete(f"{m.chat.id}:lockSHTM:{Dev_FINAL}")
                await r.delete(f"{m.chat.id}:lockNSFW:{Dev_FINAL}")
                return False

    if text == "قفل الدردشة" or text == "قفل الدردشه" or text == "قفل الشات":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_400(k))
        else:
            if await r.get(f"{m.chat.id}:mute:{Dev_FINAL}"):
                return await m.reply(plugins_locks_403(k, m.from_user.mention(), k, "الشات"))
            else:
                await r.set(f"{m.chat.id}:mute:{Dev_FINAL}", 1)
                return await m.reply(plugins_locks_406(k, m.from_user.mention(), k, "الشات"))

    if text == "فتح الدردشة" or text == "فتح الدردشه" or text == "فتح الشات":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_410(k))
        else:
            if not await r.get(f"{m.chat.id}:mute:{Dev_FINAL}"):
                return await m.reply(plugins_locks_413(k, m.from_user.mention(), k, "الشات"))
            else:
                await r.delete(f"{m.chat.id}:mute:{Dev_FINAL}")
                return await m.reply(plugins_locks_416(k, m.from_user.mention(), k, "الشات"))

    if text == "قفل التعديل":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_420(k))
        else:
            if await r.get(f"{m.chat.id}:lockEdit:{Dev_FINAL}"):
                return await m.reply(plugins_locks_423(k, m.from_user.mention(), k, "التعديل"))
            else:
                await r.set(f"{m.chat.id}:lockEdit:{Dev_FINAL}", 1)
                return await m.reply(plugins_locks_426(k, m.from_user.mention(), k, "التعديل"))

    if text == "فتح التعديل":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_430(k))
        else:
            if not await r.get(f"{m.chat.id}:lockEdit:{Dev_FINAL}"):
                return await m.reply(plugins_locks_433(k, m.from_user.mention(), k, "التعديل"))
            else:
                await r.delete(f"{m.chat.id}:lockEdit:{Dev_FINAL}")
                return await m.reply(plugins_locks_436(k, m.from_user.mention(), k, "التعديل"))

    if text == "قفل تعديل الميديا":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_440(k))
        else:
            if await r.get(f"{m.chat.id}:lockEditM:{Dev_FINAL}"):
                return await m.reply(plugins_locks_443(k, m.from_user.mention(), k, "تعديل الميديا"))
            else:
                await r.set(f"{m.chat.id}:lockEditM:{Dev_FINAL}", 1)
                return await m.reply(plugins_locks_446(k, m.from_user.mention(), k, "تعديل الميديا"))

    if text == "فتح تعديل الميديا":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_450(k))
        else:
            if not await r.get(f"{m.chat.id}:lockEditM:{Dev_FINAL}"):
                return await m.reply(plugins_locks_453(k, m.from_user.mention(), k, "تعديل الميديا"))
            else:
                await r.delete(f"{m.chat.id}:lockEditM:{Dev_FINAL}")
                return await m.reply(plugins_locks_456(k, m.from_user.mention(), k, "تعديل الميديا"))

    if text == "قفل الفويسات" or text == "قفل البصمات":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_460(k))
        else:
            if await r.get(f"{m.chat.id}:lockVoice:{Dev_FINAL}"):
                return await m.reply(plugins_locks_463(k, m.from_user.mention(), k, "الفويس"))
            else:
                await r.set(f"{m.chat.id}:lockVoice:{Dev_FINAL}", 1)
                return await m.reply(plugins_locks_466(k, m.from_user.mention(), k, "الفويس"))

    if text == "فتح الفويسات" or text == "فتح البصمات":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_470(k))
        else:
            if not await r.get(f"{m.chat.id}:lockVoice:{Dev_FINAL}"):
                return await m.reply(plugins_locks_473(k, m.from_user.mention(), k, "الفويس"))
            else:
                await r.delete(f"{m.chat.id}:lockVoice:{Dev_FINAL}")
                return await m.reply(plugins_locks_476(k, m.from_user.mention(), k, "الفويس"))

    if text == "قفل الفيديو" or text == "قفل الفيديوهات":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_480(k))
        else:
            if await r.get(f"{m.chat.id}:lockVideo:{Dev_FINAL}"):
                return await m.reply(plugins_locks_483(k, m.from_user.mention(), k, "الفيديو"))
            else:
                await r.set(f"{m.chat.id}:lockVideo:{Dev_FINAL}", 1)
                return await m.reply(plugins_locks_486(k, m.from_user.mention(), k, "الفيديو"))

    if text == "فتح الفيديو" or text == "فتح الفيديوهات":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_490(k))
        else:
            if not await r.get(f"{m.chat.id}:lockVideo:{Dev_FINAL}"):
                return await m.reply(plugins_locks_493(k, m.from_user.mention(), k, "الفيديو"))
            else:
                await r.delete(f"{m.chat.id}:lockVideo:{Dev_FINAL}")
                return await m.reply(plugins_locks_496(k, m.from_user.mention(), k, "الفيديو"))

    if text == "قفل الاشعارات":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_500(k))
        else:
            if await r.get(f"{m.chat.id}:lockNot:{Dev_FINAL}"):
                return await m.reply(plugins_locks_503(k, m.from_user.mention(), k, "الاشعارات"))
            else:
                await r.set(f"{m.chat.id}:lockNot:{Dev_FINAL}", 1)
                return await m.reply(plugins_locks_506(k, m.from_user.mention(), k, "الاشعارات"))

    if text == "فتح الاشعارات":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_510(k))
        else:
            if not await r.get(f"{m.chat.id}:lockNot:{Dev_FINAL}"):
                return await m.reply(plugins_locks_513(k, m.from_user.mention(), k, "الاشعارات"))
            else:
                await r.delete(f"{m.chat.id}:lockNot:{Dev_FINAL}")
                return await m.reply(plugins_locks_516(k, m.from_user.mention(), k, "الاشعارات"))

    if text == "قفل الصور":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_520(k))
        else:
            if await r.get(f"{m.chat.id}:lockPhoto:{Dev_FINAL}"):
                return await m.reply(plugins_locks_523(k, m.from_user.mention(), k, "الصور"))
            else:
                await r.set(f"{m.chat.id}:lockPhoto:{Dev_FINAL}", 1)
                await r.delete(f"{m.chat.id}:lockPhotoRestrict:{Dev_FINAL}")
                return await m.reply(plugins_locks_527(k, m.from_user.mention(), k, "الصور"))

    if text == "فتح الصور":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_531(k))
        else:
            if not await r.get(f"{m.chat.id}:lockPhoto:{Dev_FINAL}"):
                return await m.reply(plugins_locks_534(k, m.from_user.mention(), k, "الصور"))
            else:
                await r.delete(f"{m.chat.id}:lockPhoto:{Dev_FINAL}")
                await r.delete(f"{m.chat.id}:lockPhotoRestrict:{Dev_FINAL}")
                return await m.reply(plugins_locks_538(k, m.from_user.mention(), k, "الصور"))

    if text == "قفل الملصقات":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_542(k))
        else:
            if await r.get(f"{m.chat.id}:lockStickers:{Dev_FINAL}"):
                return await m.reply(plugins_locks_545(k, m.from_user.mention(), k, "الملصقات"))
            else:
                await r.set(f"{m.chat.id}:lockStickers:{Dev_FINAL}", 1)
                return await m.reply(plugins_locks_548(k, m.from_user.mention(), k, "الملصقات"))

    if text == "فتح الملصقات":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_552(k))
        else:
            if not await r.get(f"{m.chat.id}:lockStickers:{Dev_FINAL}"):
                return await m.reply(plugins_locks_555(k, m.from_user.mention(), k, "الملصقات"))
            else:
                await r.delete(f"{m.chat.id}:lockStickers:{Dev_FINAL}")
                return await m.reply(plugins_locks_558(k, m.from_user.mention(), k, "الملصقات"))

    if text == "قفل الفارسيه":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_562(k))
        else:
            if await r.get(f"{m.chat.id}:lockPersian:{Dev_FINAL}"):
                return await m.reply(plugins_locks_565(k, m.from_user.mention(), k, "الفارسيه"))
            else:
                await r.set(f"{m.chat.id}:lockPersian:{Dev_FINAL}", 1)
                return await m.reply(plugins_locks_568(k, m.from_user.mention(), k, "الفارسيه"))

    if text == "فتح الفارسيه":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_572(k))
        else:
            if not await r.get(f"{m.chat.id}:lockPersian:{Dev_FINAL}"):
                return await m.reply(plugins_locks_575(k, m.from_user.mention(), k, "الفارسيه"))
            else:
                await r.delete(f"{m.chat.id}:lockPersian:{Dev_FINAL}")
                return await m.reply(plugins_locks_578(k, m.from_user.mention(), k, "الفارسيه"))

    if text == "قفل الملفات":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_582(k))
        else:
            if await r.get(f"{m.chat.id}:lockFiles:{Dev_FINAL}"):
                return await m.reply(plugins_locks_585(k, m.from_user.mention(), k, "الملفات"))
            else:
                await r.set(f"{m.chat.id}:lockFiles:{Dev_FINAL}", 1)
                return await m.reply(plugins_locks_588(k, m.from_user.mention(), k, "الملفات"))

    if text == "فتح الملفات":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_592(k))
        else:
            if not await r.get(f"{m.chat.id}:lockFiles:{Dev_FINAL}"):
                return await m.reply(plugins_locks_595(k, m.from_user.mention(), k, "الملفات"))
            else:
                await r.delete(f"{m.chat.id}:lockFiles:{Dev_FINAL}")
                return await m.reply(plugins_locks_598(k, m.from_user.mention(), k, "الملفات"))

    if text == "قفل المتحركات" or text == "قفل المتحركه":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_602(k))
        else:
            if await r.get(f"{m.chat.id}:lockAnimations:{Dev_FINAL}"):
                return await m.reply(plugins_locks_605(k, m.from_user.mention(), k, "المتحركات"))
            else:
                await r.set(f"{m.chat.id}:lockAnimations:{Dev_FINAL}", 1)
                await r.delete(f"{m.chat.id}:lockAnimationsRestrict:{Dev_FINAL}")
                return await m.reply(plugins_locks_609(k, m.from_user.mention(), k, "المتحركات"))

    if text == "فتح المتحركات" or text == "فتح المتحركه":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_613(k))
        else:
            if not await r.get(f"{m.chat.id}:lockAnimations:{Dev_FINAL}"):
                return await m.reply(plugins_locks_616(k, m.from_user.mention(), k, "المتحركات"))
            else:
                await r.delete(f"{m.chat.id}:lockAnimations:{Dev_FINAL}")
                await r.delete(f"{m.chat.id}:lockAnimationsRestrict:{Dev_FINAL}")
                return await m.reply(plugins_locks_620(k, m.from_user.mention(), k, "المتحركات"))

    if text == "قفل الروابط":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_624(k))
        else:
            if await r.get(f"{m.chat.id}:lockUrls:{Dev_FINAL}"):
                return await m.reply(plugins_locks_627(k, m.from_user.mention(), k, "الروابط"))
            else:
                await r.set(f"{m.chat.id}:lockUrls:{Dev_FINAL}", 1)
                await r.delete(f"{m.chat.id}:lockUrlsRestrict:{Dev_FINAL}")
                return await m.reply(plugins_locks_631(k, m.from_user.mention(), k, "الروابط"))

    if text == "فتح الروابط":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_635(k))
        else:
            if not await r.get(f"{m.chat.id}:lockUrls:{Dev_FINAL}"):
                return await m.reply(plugins_locks_638(k, m.from_user.mention(), k, "الروابط"))
            else:
                await r.delete(f"{m.chat.id}:lockUrls:{Dev_FINAL}")
                await r.delete(f"{m.chat.id}:lockUrlsRestrict:{Dev_FINAL}")
                return await m.reply(plugins_locks_642(k, m.from_user.mention(), k, "الروابط"))

    if text == "قفل الهشتاق" or text == "قفل الهاشتاق":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_646(k))
        else:
            if await r.get(f"{m.chat.id}:lockHashtags:{Dev_FINAL}"):
                return await m.reply(plugins_locks_649(k, m.from_user.mention(), k, "الهاشتاق"))
            else:
                await r.set(f"{m.chat.id}:lockHashtags:{Dev_FINAL}", 1)
                return await m.reply(plugins_locks_652(k, m.from_user.mention(), k, "الهاشتاق"))

    if text == "فتح الهشتاق" or text == "فتح الهاشتاق":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_656(k))
        else:
            if not await r.get(f"{m.chat.id}:lockHashtags:{Dev_FINAL}"):
                return await m.reply(plugins_locks_659(k, m.from_user.mention(), k, "الهاشتاق"))
            else:
                await r.delete(f"{m.chat.id}:lockHashtags:{Dev_FINAL}")
                return await m.reply(plugins_locks_662(k, m.from_user.mention(), k, "الهاشتاق"))

    if text == "قفل البوتات":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_666(k))
        else:
            if await r.get(f"{m.chat.id}:lockBots:{Dev_FINAL}"):
                return await m.reply(plugins_locks_669(k, m.from_user.mention(), k, "البوتات"))
            else:
                await r.set(f"{m.chat.id}:lockBots:{Dev_FINAL}", 1)
                return await m.reply(plugins_locks_672(k, m.from_user.mention(), k, "البوتات"))

    if text == "فتح البوتات":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_676(k))
        else:
            if not await r.get(f"{m.chat.id}:lockBots:{Dev_FINAL}"):
                return await m.reply(plugins_locks_679(k, m.from_user.mention(), k, "البوتات"))
            else:
                await r.delete(f"{m.chat.id}:lockBots:{Dev_FINAL}")
                return await m.reply(plugins_locks_682(k, m.from_user.mention(), k, "البوتات"))

    if text == "قفل اليوزرات" or text == "قفل المنشن":
        if not (await mod_pls(m.from_user.id, m.chat.id) or await fake_rank_pls(m.from_user.id, m.chat.id, 'mention')):
            return await m.reply(plugins_locks_686(k))
        else:
            if await r.get(f"{m.chat.id}:lockTags:{Dev_FINAL}"):
                return await m.reply(plugins_locks_689(k, m.from_user.mention(), k, "اليوزرات"))
            else:
                await r.set(f"{m.chat.id}:lockTags:{Dev_FINAL}", 1)
                return await m.reply(plugins_locks_692(k, m.from_user.mention(), k, "اليوزرات"))

    if text == "فتح اليوزرات" or text == "فتح المنشن":
        if not (await mod_pls(m.from_user.id, m.chat.id) or await fake_rank_pls(m.from_user.id, m.chat.id, 'mention')):
            return await m.reply(plugins_locks_696(k))
        else:
            if not await r.get(f"{m.chat.id}:lockTags:{Dev_FINAL}"):
                return await m.reply(plugins_locks_699(k, m.from_user.mention(), k, "اليوزرات"))
            else:
                await r.delete(f"{m.chat.id}:lockTags:{Dev_FINAL}")
                return await m.reply(plugins_locks_702(k, m.from_user.mention(), k, "اليوزرات"))

    if text == "قفل الإباحي" or text == "قفل الاباحي":
        if not await owner_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_706(k))
        else:
            if await r.get(f"{m.chat.id}:lockNSFW:{Dev_FINAL}"):
                return await m.reply(plugins_locks_709(k, m.from_user.mention(), k, "الإباحي"))
            else:
                await r.set(f"{m.chat.id}:lockNSFW:{Dev_FINAL}", 1)
                return await m.reply(plugins_locks_712(k, m.from_user.mention(), k, "الإباحي"))

    if text == "فتح الإباحي" or text == "فتح الاباحي":
        if not await owner_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_716(k))
        else:
            if not await r.get(f"{m.chat.id}:lockNSFW:{Dev_FINAL}"):
                return await m.reply(plugins_locks_719(k, m.from_user.mention(), k, "االإباحي"))
            else:
                await r.delete(f"{m.chat.id}:lockNSFW:{Dev_FINAL}")
                return await m.reply(plugins_locks_722(k, m.from_user.mention(), k, "الإباحي"))

    if text == "قفل الكلام الكثير" or text == "قفل الكلايش":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_726(k))
        else:
            if await r.get(f"{m.chat.id}:lockMessages:{Dev_FINAL}"):
                return await m.reply(plugins_locks_729(k, m.from_user.mention(), k, "الكلام الكثير"))
            else:
                await r.set(f"{m.chat.id}:lockMessages:{Dev_FINAL}", 1)
                return await m.reply(plugins_locks_732(k, m.from_user.mention(), k, "الكلام الكثير"))

    if text == "فتح الكلام الكثير" or text == "فتح الكلايش":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_736(k))
        else:
            if not await r.get(f"{m.chat.id}:lockMessages:{Dev_FINAL}"):
                return await m.reply(plugins_locks_739(k, m.from_user.mention(), k, "الكلام الكثير"))
            else:
                await r.delete(f"{m.chat.id}:lockMessages:{Dev_FINAL}")
                return await m.reply(plugins_locks_742(k, m.from_user.mention(), k, "الكلام الكثير"))

    if text == "قفل التكرار":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_746(k))
        else:
            if await r.get(f"{m.chat.id}:lockSpam:{Dev_FINAL}"):
                return await m.reply(plugins_locks_749(k, m.from_user.mention(), k, "التكرار"))
            else:
                await r.set(f"{m.chat.id}:lockSpam:{Dev_FINAL}", 1)
                return await m.reply(plugins_locks_752(k, m.from_user.mention(), k, "التكرار"))

    if text == "فتح التكرار":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_756(k))
        else:
            if not await r.get(f"{m.chat.id}:lockSpam:{Dev_FINAL}"):
                return await m.reply(plugins_locks_759(k, m.from_user.mention(), k, "التكرار"))
            else:
                await r.delete(f"{m.chat.id}:lockSpam:{Dev_FINAL}")
                return await m.reply(plugins_locks_762(k, m.from_user.mention(), k, "التكرار"))

    if text == "قفل التوجيه":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_766(k))
        else:
            if await r.get(f"{m.chat.id}:lockForward:{Dev_FINAL}"):
                return await m.reply(plugins_locks_769(k, m.from_user.mention(), k, "التوجيه"))
            else:
                await r.set(f"{m.chat.id}:lockForward:{Dev_FINAL}", 1)
                await r.delete(f"{m.chat.id}:lockForwardRestrict:{Dev_FINAL}")
                return await m.reply(plugins_locks_773(k, m.from_user.mention(), k, "التوجيه"))

    if text == "فتح التوجيه":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_777(k))
        else:
            if not await r.get(f"{m.chat.id}:lockForward:{Dev_FINAL}"):
                return await m.reply(plugins_locks_780(k, m.from_user.mention(), k, "التوجيه"))
            else:
                await r.delete(f"{m.chat.id}:lockForward:{Dev_FINAL}")
                await r.delete(f"{m.chat.id}:lockForwardRestrict:{Dev_FINAL}")
                return await m.reply(plugins_locks_784(k, m.from_user.mention(), k, "التوجيه"))

    if text == "قفل الانلاين":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_788(k))
        else:
            if await r.get(f"{m.chat.id}:lockInline:{Dev_FINAL}"):
                return await m.reply(plugins_locks_791(k, m.from_user.mention(), k, "الانلاين"))
            else:
                await r.set(f"{m.chat.id}:lockInline:{Dev_FINAL}", 1)
                return await m.reply(plugins_locks_794(k, m.from_user.mention(), k, "الانلاين"))

    if text == "فتح الانلاين":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_798(k))
        else:
            if not await r.get(f"{m.chat.id}:lockInline:{Dev_FINAL}"):
                return await m.reply(plugins_locks_801(k, m.from_user.mention(), k, "الانلاين"))
            else:
                await r.delete(f"{m.chat.id}:lockInline:{Dev_FINAL}")
                return await m.reply(plugins_locks_804(k, m.from_user.mention(), k, "الانلاين"))

    if text == "قفل السب":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_808(k))
        else:
            if await r.get(f"{m.chat.id}:lockSHTM:{Dev_FINAL}"):
                return await m.reply(plugins_locks_811(k, m.from_user.mention(), k, "السب"))
            else:
                await r.set(f"{m.chat.id}:lockSHTM:{Dev_FINAL}", 1)
                return await m.reply(plugins_locks_814(k, m.from_user.mention(), k, "السب"))

    if text == "فتح السب":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_818(k))
        else:
            if not await r.get(f"{m.chat.id}:lockSHTM:{Dev_FINAL}"):
                return await m.reply(plugins_locks_821(k, m.from_user.mention(), k, "السب"))
            else:
                await r.delete(f"{m.chat.id}:lockSHTM:{Dev_FINAL}")
                return await m.reply(plugins_locks_824(k, m.from_user.mention(), k, "السب"))

    if text == "قفل الاضافه" or text == "قفل الاضافة" or text == "قفل الجهات":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_828(k))
        else:
            if await r.get(f"{m.chat.id}:lockaddContacts:{Dev_FINAL}"):
                return await m.reply(plugins_locks_831(k, m.from_user.mention(), k, "الاضافه"))
            else:
                await r.set(f"{m.chat.id}:lockaddContacts:{Dev_FINAL}", 1)
                return await m.reply(plugins_locks_834(k, m.from_user.mention(), k, "الاضافه"))

    if text == "فتح الاضافه" or text == "فتح الاضافة" or text == "فتح الجهات":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_838(k))
        else:
            if not await r.get(f"{m.chat.id}:lockaddContacts:{Dev_FINAL}"):
                return await m.reply(plugins_locks_841(k, m.from_user.mention(), k, "الاضافه"))
            else:
                await r.delete(f"{m.chat.id}:lockaddContacts:{Dev_FINAL}")
                return await m.reply(plugins_locks_844(k, m.from_user.mention(), k, "الاضافه"))

    if text == "قفل دخول البوتات" or text == "قفل الوهمي" or text == "قفل الايراني":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_848(k))
        else:
            if await r.get(f"{m.chat.id}:lockJoinPersian:{Dev_FINAL}"):
                return await m.reply(plugins_locks_851(k, m.from_user.mention(), k, "دخول البوتات"))
            else:
                await r.set(f"{m.chat.id}:lockJoinPersian:{Dev_FINAL}", 1)
                return await m.reply(plugins_locks_854(k, m.from_user.mention(), k, "دخول البوتات"))

    if text == "فتح دخول البوتات" or text == "فتح الوهمي" or text == "فتح الايراني":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_858(k))
        else:
            if not await r.get(f"{m.chat.id}:lockJoinPersian:{Dev_FINAL}"):
                return await m.reply(plugins_locks_861(k, m.from_user.mention(), k, "دخول البوتات"))
            else:
                await r.delete(f"{m.chat.id}:lockJoinPersian:{Dev_FINAL}")
                return await m.reply(plugins_locks_864(k, m.from_user.mention(), k, "دخول البوتات"))

    if text == "قفل الصوت":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_868(k))
        else:
            if await r.get(f"{m.chat.id}:lockAudios:{Dev_FINAL}"):
                return await m.reply(plugins_locks_871(k, m.from_user.mention(), k, "الصوت"))
            else:
                await r.set(f"{m.chat.id}:lockAudios:{Dev_FINAL}", 1)
                return await m.reply(plugins_locks_874(k, m.from_user.mention(), k, "الصوت"))

    if text == "فتح الصوت":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_878(k))
        else:
            if not await r.get(f"{m.chat.id}:lockAudios:{Dev_FINAL}"):
                return await m.reply(plugins_locks_881(k, m.from_user.mention(), k, "الصوت"))
            else:
                await r.delete(f"{m.chat.id}:lockAudios:{Dev_FINAL}")
                return await m.reply(plugins_locks_884(k, m.from_user.mention(), k, "الصوت"))

    if text == "قفل القنوات":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_888(k))
        else:
            if await r.get(f"{m.chat.id}:lockChannels:{Dev_FINAL}"):
                return await m.reply(plugins_locks_891(k, m.from_user.mention(), k, "القنوات"))
            else:
                await r.set(f"{m.chat.id}:lockChannels:{Dev_FINAL}", 1)
                return await m.reply(plugins_locks_894(k, m.from_user.mention(), k, "القنوات"))

    if text == "فتح القنوات":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_898(k))
        else:
            if not await r.get(f"{m.chat.id}:lockChannels:{Dev_FINAL}"):
                return await m.reply(plugins_locks_901(k, m.from_user.mention(), k, "القنوات"))
            else:
                await r.delete(f"{m.chat.id}:lockChannels:{Dev_FINAL}")
                return await m.reply(plugins_locks_904(k, m.from_user.mention(), k, "القنوات"))

    if text == "قفل الدخول":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_908(k))
        else:
            if await r.get(f"{m.chat.id}:lockJoin:{Dev_FINAL}"):
                return await m.reply(plugins_locks_911(k, m.from_user.mention(), k, "الدخول"))
            else:
                await r.set(f"{m.chat.id}:lockJoin:{Dev_FINAL}", 1)
                return await m.reply(plugins_locks_914(k, m.from_user.mention(), k, "الدخول"))

    if text == "فتح الدخول":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_918(k))
        else:
            if not await r.get(f"{m.chat.id}:lockJoin:{Dev_FINAL}"):
                return await m.reply(plugins_locks_921(k, m.from_user.mention(), k, "الدخول"))
            else:
                await r.delete(f"{m.chat.id}:lockJoin:{Dev_FINAL}")
                return await m.reply(plugins_locks_924(k, m.from_user.mention(), k, "الدخول"))

    if text == "قفل الدخول بالتقييد" or text == "قفل الدخول بالتقيد":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_928(k))
        else:
            if await r.get(f"{m.chat.id}:lockJoinRestrict:{Dev_FINAL}"):
                return await m.reply(plugins_locks_931(k, m.from_user.mention(), k, "الدخول بالتقييد"))
            else:
                await r.set(f"{m.chat.id}:lockJoin:{Dev_FINAL}", 1)
                await r.set(f"{m.chat.id}:lockJoinRestrict:{Dev_FINAL}", 1)
                return await m.reply(plugins_locks_935(k, m.from_user.mention(), k, "الدخول بالتقييد"))

    if text == "فتح الدخول بالتقييد" or text == "فتح الدخول بالتقيد":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_939(k))
        else:
            if not await r.get(f"{m.chat.id}:lockJoinRestrict:{Dev_FINAL}"):
                return await m.reply(plugins_locks_942(k, m.from_user.mention(), k, "الدخول بالتقييد"))
            else:
                await r.delete(f"{m.chat.id}:lockJoinRestrict:{Dev_FINAL}")
                await r.delete(f"{m.chat.id}:lockJoin:{Dev_FINAL}")
                return await m.reply(plugins_locks_946(k, m.from_user.mention(), k, "الدخول بالتقييد"))

    if text == "قفل الانتحال":
        if m.from_user.id != 5434703779:
            return await m.reply(plugins_locks_950(k))
        else:
            if await r.get(f"lockFakeName:Global:{Dev_FINAL}"):
                return await m.reply(plugins_locks_953(k, m.from_user.mention(), k))
            else:
                await r.set(f"lockFakeName:Global:{Dev_FINAL}", 1)
                return await m.reply(plugins_locks_956(k, m.from_user.mention(), k))

    if text == "فتح الانتحال":
        if m.from_user.id != 5434703779:
            return await m.reply(plugins_locks_960(k))
        else:
            if not await r.get(f"lockFakeName:Global:{Dev_FINAL}"):
                return await m.reply(plugins_locks_963(k, m.from_user.mention(), k))
            else:
                await r.delete(f"lockFakeName:Global:{Dev_FINAL}")
                return await m.reply(plugins_locks_966(k, m.from_user.mention(), k))

    if text == "قفل الاقتباس":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_970(k))
        else:
            if await r.get(f"{m.chat.id}:lockQuote:{Dev_FINAL}"):
                return await m.reply(plugins_locks_973(k, m.from_user.mention(), k, "الاقتباس"))
            else:
                await r.set(f"{m.chat.id}:lockQuote:{Dev_FINAL}", 1)
                return await m.reply(plugins_locks_976(k, m.from_user.mention(), k, "الاقتباس"))

    if text == "فتح الاقتباس":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_980(k))
        else:
            if not await r.get(f"{m.chat.id}:lockQuote:{Dev_FINAL}"):
                return await m.reply(plugins_locks_983(k, m.from_user.mention(), k, "الاقتباس"))
            else:
                await r.delete(f"{m.chat.id}:lockQuote:{Dev_FINAL}")
                return await m.reply(plugins_locks_986(k, m.from_user.mention(), k, "الاقتباس"))

    if text == "قفل الشارحه" or text == "قفل الشارحة":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_990(k))
        else:
            if await r.get(f"{m.chat.id}:lockDash:{Dev_FINAL}"):
                return await m.reply(plugins_locks_993(k, m.from_user.mention(), k, "الشارحة"))
            else:
                await r.set(f"{m.chat.id}:lockDash:{Dev_FINAL}", 1)
                return await m.reply(plugins_locks_996(k, m.from_user.mention(), k, "الشارحة"))

    if text == "فتح الشارحه" or text == "فتح الشارحة":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_1000(k))
        else:
            if not await r.get(f"{m.chat.id}:lockDash:{Dev_FINAL}"):
                return await m.reply(plugins_locks_1003(k, m.from_user.mention(), k, "الشارحة"))
            else:
                await r.delete(f"{m.chat.id}:lockDash:{Dev_FINAL}")
                return await m.reply(plugins_locks_1006(k, m.from_user.mention(), k, "الشارحة"))

    if text == "قفل الايموجيات المميزه" or text == "قفل الايموجيات المميزة":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_1010(k))
        else:
            if await r.get(f"{m.chat.id}:lockPremiumEmoji:{Dev_FINAL}"):
                return await m.reply(plugins_locks_1013(k, m.from_user.mention(), k, "الايموجيات المميزة"))
            else:
                await r.set(f"{m.chat.id}:lockPremiumEmoji:{Dev_FINAL}", 1)
                return await m.reply(plugins_locks_1016(k, m.from_user.mention(), k, "الايموجيات المميزة"))

    if text == "فتح الايموجيات المميزه" or text == "فتح الايموجيات المميزة":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_1020(k))
        else:
            if not await r.get(f"{m.chat.id}:lockPremiumEmoji:{Dev_FINAL}"):
                return await m.reply(plugins_locks_1023(k, m.from_user.mention(), k, "الايموجيات المميزة"))
            else:
                await r.delete(f"{m.chat.id}:lockPremiumEmoji:{Dev_FINAL}")
                return await m.reply(plugins_locks_1026(k, m.from_user.mention(), k, "الايموجيات المميزة"))

    if text == "قفل الكتابه" or text == "قفل الكتابة":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_1030(k))
        else:
            if await r.get(f"{m.chat.id}:lockText:{Dev_FINAL}"):
                return await m.reply(plugins_locks_1033(k, m.from_user.mention(), k, "الكتابة"))
            else:
                await r.set(f"{m.chat.id}:lockText:{Dev_FINAL}", 1)
                return await m.reply(plugins_locks_1036(k, m.from_user.mention(), k, "الكتابة"))

    if text == "فتح الكتابه" or text == "فتح الكتابة":
        if not await mod_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_1040(k))
        else:
            if not await r.get(f"{m.chat.id}:lockText:{Dev_FINAL}"):
                return await m.reply(plugins_locks_1043(k, m.from_user.mention(), k, "الكتابة"))
            else:
                await r.delete(f"{m.chat.id}:lockText:{Dev_FINAL}")
                return await m.reply(plugins_locks_1046(k, m.from_user.mention(), k, "الكتابة"))

    if text in ["قفل جمثون", "قفل الجمثون"]:
        if await mod_pls(m.from_user.id, m.chat.id):
            if await r.get(f"{m.chat.id}:lockGamthon:{Dev_FINAL}"):
                return await m.reply(plugins_locks_1051(k, m.from_user.mention(), k, "الجمثون"))
            else:
                await r.set(f"{m.chat.id}:lockGamthon:{Dev_FINAL}", 1)
                return await m.reply(plugins_locks_1054(k, m.from_user.mention(), k, "الجمثون"))
        else:
            return await m.reply(plugins_locks_1056(k))

    if text in ["فتح جمثون", "فتح الجمثون"]:
        if await mod_pls(m.from_user.id, m.chat.id):
            if not await r.get(f"{m.chat.id}:lockGamthon:{Dev_FINAL}"):
                return await m.reply(plugins_locks_1061(k, m.from_user.mention(), k, "الجمثون"))
            else:
                await r.delete(f"{m.chat.id}:lockGamthon:{Dev_FINAL}")
                return await m.reply(plugins_locks_1064(k, m.from_user.mention(), k, "الجمثون"))
        else:
            return await m.reply(plugins_locks_1066(k))

    if text in ["قفل الصور بالتقييد", "قفل الصور بالتقيد"]:
        if await mod_pls(m.from_user.id, m.chat.id):
            if await r.get(f"{m.chat.id}:lockPhotoRestrict:{Dev_FINAL}"):
                return await m.reply(plugins_locks_1071(k, m.from_user.mention(), k, "الصور بالتقييد"))
            else:
                await r.set(f"{m.chat.id}:lockPhoto:{Dev_FINAL}", 1)
                await r.set(f"{m.chat.id}:lockPhotoRestrict:{Dev_FINAL}", 1)
                return await m.reply(plugins_locks_1075(k, m.from_user.mention(), k, "الصور بالتقييد"))
        else:
            return await m.reply(plugins_locks_1077(k))

    if text in ["فتح الصور بالتقييد", "فتح الصور بالتقيد"]:
        if await mod_pls(m.from_user.id, m.chat.id):
            if not await r.get(f"{m.chat.id}:lockPhotoRestrict:{Dev_FINAL}"):
                return await m.reply(plugins_locks_1082(k, m.from_user.mention(), k, "الصور بالتقييد"))
            else:
                await r.delete(f"{m.chat.id}:lockPhotoRestrict:{Dev_FINAL}")
                await r.delete(f"{m.chat.id}:lockPhoto:{Dev_FINAL}")
                return await m.reply(plugins_locks_1086(k, m.from_user.mention(), k, "الصور بالتقييد"))
        else:
            return await m.reply(plugins_locks_1088(k))

    if text in ["قفل الفيديو بالتقييد", "قفل الفيديوهات بالتقييد"]:
        if await mod_pls(m.from_user.id, m.chat.id):
            if await r.get(f"{m.chat.id}:lockVideoRestrict:{Dev_FINAL}"):
                return await m.reply(plugins_locks_1093(k, m.from_user.mention(), k, "الفيديو بالتقييد"))
            else:
                await r.set(f"{m.chat.id}:lockVideo:{Dev_FINAL}", 1)
                await r.set(f"{m.chat.id}:lockVideoRestrict:{Dev_FINAL}", 1)
                return await m.reply(plugins_locks_1097(k, m.from_user.mention(), k, "الفيديو بالتقييد"))
        else:
            return await m.reply(plugins_locks_1099(k))

    if text in ["فتح الفيديو بالتقييد", "فتح الفيديوهات بالتقييد"]:
        if await mod_pls(m.from_user.id, m.chat.id):
            if not await r.get(f"{m.chat.id}:lockVideoRestrict:{Dev_FINAL}"):
                return await m.reply(plugins_locks_1104(k, m.from_user.mention(), k, "الفيديو بالتقييد"))
            else:
                await r.delete(f"{m.chat.id}:lockVideoRestrict:{Dev_FINAL}")
                await r.delete(f"{m.chat.id}:lockVideo:{Dev_FINAL}")
                return await m.reply(plugins_locks_1108(k, m.from_user.mention(), k, "الفيديو بالتقييد"))
        else:
            return await m.reply(plugins_locks_1110(k))

    if text in ["قفل المتحركه بالتقييد", "قفل المتحركات بالتقييد"]:
        if await mod_pls(m.from_user.id, m.chat.id):
            if await r.get(f"{m.chat.id}:lockAnimationsRestrict:{Dev_FINAL}"):
                return await m.reply(plugins_locks_1115(k, m.from_user.mention(), k, "المتحركات بالتقييد"))
            else:
                await r.set(f"{m.chat.id}:lockAnimations:{Dev_FINAL}", 1)
                await r.set(f"{m.chat.id}:lockAnimationsRestrict:{Dev_FINAL}", 1)
                return await m.reply(plugins_locks_1119(k, m.from_user.mention(), k, "المتحركات بالتقييد"))
        else:
            return await m.reply(plugins_locks_1121(k))

    if text in ["فتح المتحركه بالتقييد", "فتح المتحركات بالتقييد"]:
        if await mod_pls(m.from_user.id, m.chat.id):
            if not await r.get(f"{m.chat.id}:lockAnimationsRestrict:{Dev_FINAL}"):
                return await m.reply(plugins_locks_1126(k, m.from_user.mention(), k, "المتحركات بالتقييد"))
            else:
                await r.delete(f"{m.chat.id}:lockAnimationsRestrict:{Dev_FINAL}")
                await r.delete(f"{m.chat.id}:lockAnimations:{Dev_FINAL}")
                return await m.reply(plugins_locks_1130(k, m.from_user.mention(), k, "المتحركات بالتقييد"))
        else:
            return await m.reply(plugins_locks_1132(k))

    if text in ["قفل الروابط بالتقييد", "قفل الروابط بالتقيد"]:
        if await mod_pls(m.from_user.id, m.chat.id):
            if await r.get(f"{m.chat.id}:lockUrlsRestrict:{Dev_FINAL}"):
                return await m.reply(plugins_locks_1137(k, m.from_user.mention(), k, "الروابط بالتقييد"))
            else:
                await r.set(f"{m.chat.id}:lockUrls:{Dev_FINAL}", 1)
                await r.set(f"{m.chat.id}:lockUrlsRestrict:{Dev_FINAL}", 1)
                return await m.reply(plugins_locks_1141(k, m.from_user.mention(), k, "الروابط بالتقييد"))
        else:
            return await m.reply(plugins_locks_1143(k))

    if text in ["فتح الروابط بالتقييد", "فتح الروابط بالتقيد"]:
        if await mod_pls(m.from_user.id, m.chat.id):
            if not await r.get(f"{m.chat.id}:lockUrlsRestrict:{Dev_FINAL}"):
                return await m.reply(plugins_locks_1148(k, m.from_user.mention(), k, "الروابط بالتقييد"))
            else:
                await r.delete(f"{m.chat.id}:lockUrlsRestrict:{Dev_FINAL}")
                await r.delete(f"{m.chat.id}:lockUrls:{Dev_FINAL}")
                return await m.reply(plugins_locks_1152(k, m.from_user.mention(), k, "الروابط بالتقييد"))
        else:
            return await m.reply(plugins_locks_1154(k))

    if text in ["قفل التوجيه بالتقييد", "قفل التوجية بالتقيد"]:
        if await mod_pls(m.from_user.id, m.chat.id):
            if await r.get(f"{m.chat.id}:lockForwardRestrict:{Dev_FINAL}"):
                return await m.reply(plugins_locks_1159(k, m.from_user.mention(), k, "التوجيه بالتقييد"))
            else:
                await r.set(f"{m.chat.id}:lockForward:{Dev_FINAL}", 1)
                await r.set(f"{m.chat.id}:lockForwardRestrict:{Dev_FINAL}", 1)
                return await m.reply(plugins_locks_1163(k, m.from_user.mention(), k, "التوجيه بالتقييد"))
        else:
            return await m.reply(plugins_locks_1165(k))

    if text in ["فتح التوجيه بالتقييد", "فتح التوجية بالتقيد"]:
        if await mod_pls(m.from_user.id, m.chat.id):
            if not await r.get(f"{m.chat.id}:lockForwardRestrict:{Dev_FINAL}"):
                return await m.reply(plugins_locks_1170(k, m.from_user.mention(), k, "التوجيه بالتقييد"))
            else:
                await r.delete(f"{m.chat.id}:lockForwardRestrict:{Dev_FINAL}")
                await r.delete(f"{m.chat.id}:lockForward:{Dev_FINAL}")
                return await m.reply(plugins_locks_1174(k, m.from_user.mention(), k, "التوجيه بالتقييد"))
        else:
            return await m.reply(plugins_locks_1176(k))

    if text == "فتح اشعارات البوت":
        if not await owner_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_1180(k))
        if await r.get(f"{m.chat.id}:BotNotifications:{Dev_FINAL}"):
            return await m.reply(plugins_locks_1182(k, m.from_user.mention(), k))
        else:
            await r.set(f"{m.chat.id}:BotNotifications:{Dev_FINAL}", 1)
            return await m.reply(plugins_locks_1185(k, m.from_user.mention(), k))

    if text == "قفل اشعارات البوت":
        if not await owner_pls(m.from_user.id, m.chat.id):
            return await m.reply(plugins_locks_1189(k))
        if not await r.get(f"{m.chat.id}:BotNotifications:{Dev_FINAL}"):
            return await m.reply(plugins_locks_1191(k, m.from_user.mention(), k))
        else:
            await r.delete(f"{m.chat.id}:BotNotifications:{Dev_FINAL}")
            return await m.reply(plugins_locks_1194(k, m.from_user.mention(), k))

    return None