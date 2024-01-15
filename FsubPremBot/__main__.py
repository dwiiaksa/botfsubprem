import asyncio

from pyrogram import idle
from pyrogram.errors import RPCError

from FsubPremBot import *


async def start_bot(_bot):
    bot_ = Bot(**_bot)
    try:
        await asyncio.wait_for(bot_.start(), timeout=30)
    except asyncio.TimeoutError:
        print(f"[𝗜𝗡𝗙𝗢] - ({int(_bot['bot_id'])}) 𝗧𝗜𝗗𝗔𝗞 𝗗𝗔𝗣𝗔𝗧 𝗠𝗘𝗥𝗘𝗦𝗣𝗢𝗡")
    except RPCError:
        await remove_bot(int(_bot["bot_id"]))
        await remove_all_vars(int(_bot["bot_id"]))
        await rem_expired_date(int(_bot["bot_id"]))
        await remove_all_user(int(_bot["bot_id"]))
        print(f"✅ {user_id} 𝗕𝗘𝗥𝗛𝗔𝗦𝗜𝗟 𝗗𝗜𝗛𝗔𝗣𝗨𝗦")


async def main():
    tasks = [start_bot(_bot) for _bot in await get_bots()]
    await asyncio.gather(*tasks, bot.start())
    vars = await get_vars(bot.me.id, "OWNER_ID")
    if vars:
        owner_id = [int(x) for x in str(vars).split()]
        if OWNER_ID not in owner_id:
            await set_vars(bot.me.id, "OWNER_ID", OWNER_ID)
    await asyncio.gather(loadPlugins(), expiredBot(), idle())


if __name__ == "__main__":
    loop = asyncio.get_event_loop_policy().get_event_loop()
    loop.run_until_complete(main())
