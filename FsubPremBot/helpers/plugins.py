from importlib import import_module

from FsubPremBot import OWNER_ID, bot
from FsubPremBot.modules import loadModule


async def loadPlugins():
    modules = loadModule()
    for mod in modules:
        import_module(f"FsubPremBot.modules.{mod}")
    print(f"[🤖 @{bot.me.username} 🤖] [🔥 TELAH BERHASIL DIAKTIFKAN! 🔥]")
    await bot.send_message(
        OWNER_ID, f"<b>[🤖 @{bot.me.username} 🤖] [🔥 TELAH BERHASIL DIAKTIFKAN! 🔥]</b>"
    )
