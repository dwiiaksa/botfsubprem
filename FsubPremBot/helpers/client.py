from pykeyboard import InlineKeyboard
from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from FsubPremBot import bot
from FsubPremBot.config import OWNER_ID
from FsubPremBot.helpers.database import *


class SUB:
    OWNER = filters.user(OWNER_ID)
    PRIVATE = filters.private

    @staticmethod
    def BOT(command, filter=False):
        def wrapper(func):
            message_filters = (
                filters.command(command) & filter
                if filter
                else filters.command(command)
            )

            @bot.on_message(message_filters)
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper

    @staticmethod
    def UP_CONTENT(filter=PRIVATE):
        def wrapper(func):
            @bot.on_message(
                filter
                & ~filters.command(
                    [
                        "start",
                        "ping",
                        "broadcast",
                        "setvars",
                        "getvars",
                        "delvars",
                        "id",
                        "eval",
                        "sh",
                        "getbot",
                        "prem",
                        "seller",
                        "unprem",
                        "unseller",
                        "time",
                    ]
                )
            )
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper

    @staticmethod
    def DATA(command):
        def wrapper(func):
            @bot.on_callback_query(filters.regex(command))
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper

    @staticmethod
    def OWNER_CB(func):
        async def function(client, callback_query):
            user = callback_query.from_user
            rpk = f"{user.first_name} {user.last_name or ''}"
            if user.id != OWNER_ID:
                return await callback_query.answer(
                    f"""
❌ ᴍᴀᴀғ {rpk}, ᴀɴᴅᴀ ᴛɪᴅᴀᴋ ᴅɪɪᴢɪɴᴋᴀɴ ᴜɴᴛᴜᴋ ᴍᴇɴᴇᴋᴀɴ ᴛᴏᴍʙᴏʟ ɪɴɪ,
ᴄᴜᴍᴀɴ ᴏᴡɴᴇʀ ʙᴏᴛ ʏᴀɴɢ ᴅɪɪᴢɪɴᴋᴀɴ ᴜɴᴛᴜᴋ ᴍᴇɴᴇᴋᴀɴ ᴛᴏᴍʙᴏʟ ɪɴɪ.
""",
                    True,
                )
            return await func(client, callback_query)

        return function

    @staticmethod
    def ADMIN(func):
        async def function(client, message):
            user = message.from_user
            rpk = f"<a href='tg://user?id={user.id}'>{user.first_name} {user.last_name or ''}</a>"
            vars = [
                int(x)
                for x in str(await get_vars(client.me.id, "OWNER_ID")).split()
                + [OWNER_ID]
            ]
            if user.id not in vars:
                return await message.reply(
                    f"""
<b>❌ ᴍᴀᴀғ {rpk}, ᴀɴᴅᴀ ᴛɪᴅᴀᴋ ᴅɪɪᴢɪɴᴋᴀɴ ᴍᴇɴɢɢᴜɴᴀᴋᴀɴ ᴘᴇʀɪɴᴛᴀʜ ɪɴɪ.
ᴘᴇʀɪɴᴛᴀʜ ɪɴɪ ʜᴀɴʏᴀ ʙɪsᴀ ᴅɪɢᴜɴᴀᴋᴀɴ ᴏʟᴇʜ ᴀᴅᴍɪɴ.</b>
""",
                    quote=True,
                )
            return await func(client, message)

        return function

    @staticmethod
    def SELLER(func):
        async def function(client, message):
            user = message.from_user
            rpk = f"<a href='tg://user?id={user.id}'>{user.first_name} {user.last_name or ''}</a>"
            seller_id = await get_seller()
            if user.id not in seller_id:
                return await message.reply(
                    f"""
<b>❌ ᴍᴀᴀғ {rpk}, ᴀɴᴅᴀ ᴛɪᴅᴀᴋ ᴅɪɪᴢɪɴᴋᴀɴ ᴍᴇɴɢɢᴜɴᴀᴋᴀɴ ᴘᴇʀɪɴᴛᴀʜ ɪɴɪ.
ᴜɴᴛᴜᴋ ᴍᴇɴɢɢᴜɴᴀᴋᴀɴ ᴘᴇʀɪɴᴛᴀʜ ɪɴɪ ᴀɴᴅᴀ ʜᴀʀᴜs ᴍᴇɴᴊᴀᴅɪ ʀᴇsᴇʟʟᴇʀ ᴛᴇʀʟᴇʙɪʜ ᴅᴀʜᴜʟᴜ</b>
""",
                    quote=True,
                )
            return await func(client, message)

        return function

    @staticmethod
    def SUBSCRIBE(func):
        async def function(client, message):
            user = message.from_user
            rpk = f"<a href='tg://user?id={user.id}'>{user.first_name} {user.last_name or ''}</a>"
            vars = await get_vars(client.me.id, "CHANNEL_FSUB_ID")
            if not vars:
                return await func(client, message)
            try:
                for x in str(vars).split():
                    await client.get_chat_member(int(x), user.id)
            except UserNotParticipant:
                buttons = InlineKeyboard(row_width=2)
                keyboard = []
                for x in str(vars).split():
                    chat = await client.get_chat(int(x))
                    invite_link = chat.invite_link
                    chat_type = chat.type
                    if chat_type in (ChatType.GROUP, ChatType.SUPERGROUP):
                        button_text = "ɢʀᴏᴜᴘ"
                    elif chat_type == ChatType.CHANNEL:
                        button_text = "ᴄʜᴀɴɴᴇʟ"
                    keyboard.append(
                        InlineKeyboardButton(
                            text=f"• ᴊᴏɪɴ {button_text} •",
                            url=invite_link,
                        )
                    )
                start_bot = (
                    f"https://t.me/{client.me.username}?start={message.command[1]}"
                    if len(message.command) >= 2
                    else f"https://t.me/{client.me.username}?start"
                )
                buttons.add(*keyboard)
                buttons.row(InlineKeyboardButton("• ᴄᴏʙᴀ ʟᴀɢɪ •", url=start_bot))
                return await message.reply(
                    f"""
<b>🙋🏻‍♂️ Hᴀʟᴏ {rpk} !

💡 ᴜɴᴛᴜᴋ ᴍᴇɴᴅᴀᴘᴀᴛᴋᴀɴ ᴛᴀᴜᴛᴀɴ ʏᴀɴɢ ɪɴɢɪɴ ᴋᴀᴍᴜ ᴀᴋsᴇs,
ᴋᴀᴍᴜ ʜᴀʀᴜs ʙᴇʀɢᴀʙᴜɴɢ ᴅɪ ɢʀᴏᴜᴘ/ᴄʜᴀɴɴᴇʟ ᴛᴇʀʟᴇʙɪʜ ᴅᴀʜᴜʟᴜ.

✅ sᴇᴛᴇʟᴀʜ ʙᴇʀɢᴀʙᴜɴɢ, sɪʟᴀᴋᴀɴ ᴛᴇᴋᴀɴ "ᴄᴏʙᴀ ʟᴀɢɪ".

💻 JIKA BOT EROR LAPORAN KE @MafiaYakuza.</b>
""",
                    disable_web_page_preview=True,
                    reply_markup=buttons,
                )
            return await func(client, message)

        return function

    @staticmethod
    def NOTIFICATION(func):
        async def function(client, message):
            try:
                vars = [
                    int(x)
                    for x in str(await get_vars(client.me.id, "OWNER_ID")).split()
                    + [OWNER_ID]
                ]
                saved_users = await get_served_user(client.me.id)
            except Exception as error:
                return await message.reply(str(error))
            if message.from_user.id not in vars:
                if message.from_user.id not in saved_users:
                    await add_served_user(client.me.id, message.from_user.id)
                for owner_id in vars:
                    try:
                        user_link = f"<a href=tg://user?id={message.from_user.id}>{message.from_user.first_name} {message.from_user.last_name or ''}</a>"
                        formatted_text = f""
                        buttons = [
                            [
                                InlineKeyboardButton(
                                    "",
                                    callback_data=f"profil {message.from_user.id}",
                                ),
                            ]
                        ]
                        
                      
                    except Exception:
                        pass
            return await func(client, message)

        return function
