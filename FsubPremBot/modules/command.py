from time import time

from pyrogram.enums import ChatType
from pyrogram.raw.functions import Ping

from FsubPremBot import *

query_mapping = {
    "fsub": "CHANNEL_FSUB_ID",
    "post": "CHANNEL_POST_ID",
    "owner": "OWNER_ID",
}


@SUB.BOT("start")
@SUB.SUBSCRIBE
@SUB.NOTIFICATION
async def _(client, message):
    if len(message.command) < 2:
        buttons = Button.start()
        msg = await MSG.START(message)
        await message.reply(msg, reply_markup=InlineKeyboardMarkup(buttons))
    else:
        ctrl = message.text.split(None, 1)[1]
        if "get" in ctrl:
            send = await message.reply("<b>ᴛᴜɴɢɢᴜ sᴇʙᴇɴᴛᴀʀ...</b>")
            try:
                decoded_str = await decode(ctrl.split("_")[1])
                chat_id, msg_id = decoded_str.split("_")
                get_msg = await client.get_messages(int(chat_id), int(msg_id))
                await get_msg.copy(message.chat.id, protect_content=True)
                await send.delete()
            except Exception as error:
                await send.edit(str(error))


@SUB.BOT("broadcast")
@SUB.ADMIN
async def _(client, message):
    msg = await message.reply("<b>sᴇᴅᴀɴɢ ᴅɪᴘʀᴏsᴇs ᴛᴜɴɢɢᴜ sᴇʙᴇɴᴛᴀʀ</b>", quote=True)
    done = 0
    if not message.reply_to_message:
        return await msg.edit("<b>ᴍᴏʜᴏɴ ʙᴀʟᴀs ᴘᴇsᴀɴ</b>")
    for x in await get_served_user(client.me.id):
        try:
            await message.reply_to_message.copy(int(x))
            done += 1
        except Exception:
            await remove_served_user(client.me.id, int(x))
    return await msg.edit(f"✅ ʙᴇʀʜᴀsɪʟ ᴍᴇɴɢɪʀɪᴍ ᴘᴇsᴀɴ ᴋᴇ {done} sᴀᴠᴇᴅ ᴄʜᴀᴛ")


@SUB.UP_CONTENT()
@SUB.ADMIN
async def _(client, message):
    try:
        msg = await message.reply("<b>sᴇᴅᴀɴɢ ᴅɪᴘʀᴏsᴇs ᴛᴜɴɢɢᴜ sᴇʙᴇɴᴛᴀʀ</b>")
        vars = await get_vars(client.me.id, "CHANNEL_POST_ID")
        copy_str = await message.copy(int(vars))
        encode_str = await encode(f"{vars}_{copy_str.id}")
        link = f"https://t.me/{client.me.username}?start=get_{encode_str}"
        button = Button.share(link)
        await msg.edit(
            f"<b>ʟɪɴᴋ sʜᴀʀɪɴɢ ғɪʟᴇ ʙᴇʀʜᴀsɪʟ ᴅɪ ʙᴜᴀᴛ:</b>\n\n{link}",
            reply_markup=InlineKeyboardMarkup(button),
            disable_web_page_preview=True,
        )
    except Exception as error:
        await msg.edit(str(error))


@SUB.BOT("setvars")
@SUB.ADMIN
async def _(client, message):
    try:
        msg = await message.reply("<b>sɪʟᴀʜᴋᴀɴ ᴛᴜɴɢɢᴜ...</b>")
        if len(message.command) < 3:
            return await msg.edit("<b>ᴛᴏʟᴏɴɢ ᴍᴀsᴜᴋᴋᴀɴ ǫᴜᴇʀʏ ᴅᴀɴ ᴠᴀʟᴇᴜ ɴʏᴀ</b>")
        command, mapping, valeu = message.command[:3]
        if mapping.lower() in query_mapping:
            query_var = query_mapping[mapping.lower()]
            vars = await get_vars(client.me.id, query_var)
            if vars:
                valeu = f"{vars} {valeu}"
            await set_vars(client.me.id, query_var, valeu)
            return await msg.edit(
                f"<b>✅ <code>{query_var}</code> ʙᴇʀʜᴀsɪʟ ᴅɪ sᴇᴛᴛɪɴɢ ᴋᴇ: <code>{valeu}</code></b>"
            )
        else:
            return await msg.edit("<b>ǫᴜᴇʀʏ ʏᴀɴɢ ᴅɪ ᴍᴀsᴜᴋᴋᴀɴ sᴀʟᴀʜ</b>")
    except Exception as error:
        await msg.edit(str(error))


@SUB.BOT("delvars")
@SUB.ADMIN
async def _(client, message):
    try:
        msg = await message.reply("<b>sɪʟᴀʜᴋᴀɴ ᴛᴜɴɢɢᴜ...</b>")
        if len(message.command) < 3:
            return await msg.edit("<b>ᴛᴏʟᴏɴɢ ᴍᴀsᴜᴋᴋᴀɴ ǫᴜᴇʀʏ ᴅᴀɴ ᴠᴀʟᴇᴜ ɴʏᴀ</b>")
        command, mapping, valeu = message.command[:3]
        if mapping.lower() in query_mapping:
            query_var = query_mapping[mapping.lower()]
            vars = await get_vars(client.me.id, query_var)
            list_vars = str(vars).split()
            if valeu in list_vars:
                list_vars.remove(valeu)
                await set_vars(client.me.id, query_var, " ".join(list_vars))
                return await msg.edit(
                    f"<b>✅ <code>{valeu}</code> ʙᴇʀʜᴀsɪʟ ᴅɪʜᴀᴘᴜs ᴅᴀʀɪ ᴠᴀʀɪᴀʙᴇʟ: <code>{query_var}</code></b>"
                )
            else:
                return await msg.edit(
                    f"<b>❌ <code>{valeu}</code> ᴛɪᴅᴀᴋ ᴅɪᴛᴇᴍᴜᴋᴀɴ ᴅᴀʟᴀᴍ ᴠᴀʀɪᴀʙᴇʟ</b>"
                )
        else:
            return await msg.edit("<b>ǫᴜᴇʀʏ ʏᴀɴɢ ᴅɪ ᴍᴀsᴜᴋᴋᴀɴ sᴀʟᴀʜ</b>")
    except Exception as error:
        await msg.edit(str(error))


@SUB.BOT("getvars")
@SUB.ADMIN
async def _(client, message):
    try:
        await client.send_message(
            message.chat.id,
            "<b>⤵️ sɪʟᴀʜᴋᴀɴ ᴋʟɪᴋ sᴀʟᴀʜ sᴀᴛᴜ ᴅɪʙᴀᴡᴀʜ ɪɴɪ</b>",
            reply_markup=InlineKeyboardMarkup(Button.list_vars(client.me.id)),
        )
    except Exception as error:
        await message.reply(str(error))


@SUB.BOT("ping")
async def _(client, message):
    uptime = await get_time((time() - start_time))
    start = datetime.now()
    await client.invoke(Ping(ping_id=0))
    end = datetime.now()
    delta_ping = (end - start).microseconds / 1000
    _ping = f"""
<b>❏ ᴘᴏɴɢ:</b> <code>{delta_ping} ms</code>
<b>└ ᴜᴘᴛɪᴍᴇ:</b> <code>{uptime}</code>
"""
    await message.reply(_ping)


@SUB.BOT("id")
async def _(client, message):
    text = f"<b><a href={message.link}>ᴍᴇssᴀɢᴇ ɪᴅ:</a></b> <code>{message.id}</code>\n"

    if message.chat.type == ChatType.CHANNEL:
        text += f"<b><a href=https://t.me/{message.chat.username}>ᴄʜᴀᴛ ɪᴅ:</a></b> <code>{message.sender_chat.id}</code>\n"
    else:
        text += f"<b><a href=tg://user?id={message.from_user.id}>ʏᴏᴜʀ ɪᴅ:</a></b> <code>{message.from_user.id}</code>\n\n"

        if len(message.command) > 1:
            try:
                user = await client.get_chat(message.text.split()[1])
                text += f"<b><a href=tg://user?id={user.id}>ᴜsᴇʀ ɪᴅ:</a></b> <code>{user.id}</code>\n\n"
            except:
                return await message.reply("Pengguna tidak ditemukan.")

        text += f"<b><a href=https://t.me/{message.chat.username}>ᴄʜᴀᴛ ɪᴅ:</a></b> <code>{message.chat.id}</code>\n\n"

    if message.reply_to_message:
        id_ = (
            message.reply_to_message.from_user.id
            if message.reply_to_message.from_user
            else message.reply_to_message.sender_chat.id
        )
        file_info = get_file_id(message.reply_to_message)
        if file_info:
            text += f"<b><a href={message.reply_to_message.link}>ᴍᴇᴅɪᴀ ɪᴅ:</a> <code>{file_info.file_id}</code>\n\n"
        text += (
            f"<b><a href={message.reply_to_message.link}>ʀᴇᴘʟɪᴇᴅ ᴍᴇssᴀɢᴇ ɪᴅ:</a></b> <code>{message.reply_to_message.id}</code>\n"
            f"<b><a href=tg://user?id={id_}>ʀᴇᴘʟɪᴇᴅ ᴜsᴇʀ ɪᴅ:</a></b> <code>{id_}</code>"
        )

    return await message.reply(text, disable_web_page_preview=True)
