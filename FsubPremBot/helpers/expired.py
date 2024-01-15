import asyncio
from datetime import datetime

from pytz import timezone

from FsubPremBot import bot
from FsubPremBot.config import LOGS_MAKER_BOT
from FsubPremBot.helpers.database import *
from FsubPremBot.helpers.tools import MSG, Button


async def exp_bot(X):
    try:
        time = datetime.now(timezone("Asia/Jakarta")).strftime("%d-%m-%Y")
        exp = (await get_expired_date(X.me.id)).strftime("%d-%m-%Y")
        if time == exp:
            await remove_bot(X.me.id)
            await remove_all_vars(X.me.id)
            await remove_all_user(X.me.id)
            await rem_expired_date(X.me.id)
            bot._bot.remove(X)
            await bot.send_message(
                LOGS_MAKER_BOT,
                MSG.EXPIRED_MSG_BOT(X),
                reply_markup=InlineKeyboardMarkup(Button.expired_button_bot(bot)),
            )
            await X.stop()
    except Exception as e:
        print(f"Error: - {X.me.id} - {str(e)}")


async def expiredBot():
    while True:
        tasks = [exp_bot(X) for X in bot._bot]
        await asyncio.gather(*tasks)
        await asyncio.sleep(3600)
