import sys
import traceback
from io import StringIO

from FsubPremBot import *


@SUB.BOT("getbot", SUB.OWNER)
async def _(client, message):
    try:
        await client.send_message(
            message.chat.id,
            await MSG.BOT(0),
            reply_markup=InlineKeyboardMarkup(Button.bot(bot._bot[0].me.id, 0)),
        )
    except Exception as error:
        await message.reply(str(error))


@SUB.BOT("prem")
@SUB.SELLER
async def _(client, message):
    prem = await get_premium()
    msg = await message.reply("<b>ᴛᴜɴɢɢᴜ sᴇʙᴇɴᴛᴀʀ</b>", quote=True)

    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(f"<b>{message.text} ᴜsᴇʀ_ɪᴅ/ᴜsᴇʀɴᴀᴍᴇ</b>")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(str(error))

    if user.id in prem:
        return await msg.edit(f"<b>{user.id} sᴜᴅᴀʜ ʙᴇʀᴀᴅᴀ ᴅᴀʟᴀᴍ ᴅᴀғᴛᴀʀ ᴘᴇᴍʙᴜᴀᴛ</b>")

    try:
        await add_premium(user.id)
        return await msg.edit(
            f"<b>✅ {user.id} sɪʟᴀʜᴋᴀɴ ʙᴜᴀᴛ ғɪʟᴇ-sʜᴀʀɪɴɢ ᴘᴀᴅᴀ ʙᴏᴛ: @{client.me.username}</b>"
        )
    except Exception as error:
        return await msg.edit(str(error))


@SUB.BOT("seller", SUB.OWNER)
async def _(client, message):
    seller = await get_seller()
    msg = await message.reply("<b>ᴛᴜɴɢɢᴜ sᴇʙᴇɴᴛᴀʀ</b>", quote=True)

    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(f"<b>{message.text} ᴜsᴇʀ_ɪᴅ/ᴜsᴇʀɴᴀᴍᴇ</b>")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(str(error))

    if user.id in seller:
        return await msg.edit(f"<b>{user.id} sᴜᴅᴀʜ ʙᴇʀᴀᴅᴀ ᴅᴀʟᴀᴍ ᴅᴀғᴛᴀʀ ʀᴇsᴇʟʟᴇʀ</b>")

    try:
        await add_seller(user.id)
        return await msg.edit(
            f"<b>✅ {user.id} ʙᴇʀʜᴀsɪʟ ᴅɪᴍᴀsᴜᴋᴋᴀɴ ᴋᴇ ᴅᴀғᴛᴀʀ ʀᴇsᴇʟʟᴇʀ</b>"
        )
        await client.send_message(
            OWNER_ID,
            f"• {message.from_user.id} | {user.id} •",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "👤 ᴘʀᴏғɪʟ",
                            callback_data=f"profil {message.from_user.id}",
                        ),
                        InlineKeyboardButton(
                            "ᴘʀᴏғɪʟ 👤", callback_data=f"profil {get_id}"
                        ),
                    ],
                ]
            ),
        )
    except Exception as error:
        return await msg.edit(str(error))


@SUB.BOT("unprem")
@SUB.SELLER
async def _(client, message):
    prem = await get_premium()
    msg = await message.reply("<b>ᴛᴜɴɢɢᴜ sᴇʙᴇɴᴛᴀʀ</b>", quote=True)

    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(f"<b>{message.text} ᴜsᴇʀ_ɪᴅ/ᴜsᴇʀɴᴀᴍᴇ</b>")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(str(error))

    if user.id not in prem:
        return await msg.edit(f"<b>{user.id} ʙᴇʟᴜᴍ ᴛᴇʀᴅᴀғᴛᴀʀ ᴅᴀʟᴀᴍ ᴅᴀғᴛᴀʀ ᴘᴇᴍʙᴜᴀᴛ</b>")

    try:
        await remove_premium(user.id)
        return await msg.edit(f"<b>❌ {user.id} ᴛᴇʟᴀʜ ᴅɪᴄᴀʙᴜᴛ ᴅᴀʀɪ ᴅᴀғᴛᴀʀ ᴘᴇᴍʙᴜᴀᴛ</b>")
    except Exception as error:
        return await msg.edit(str(error))


@SUB.BOT("unseller", SUB.OWNER)
async def _(client, message):
    seller = await get_seller()
    msg = await message.reply("<b>ᴛᴜɴɢɢᴜ sᴇʙᴇɴᴛᴀʀ</b>", quote=True)

    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(f"<b>{message.text} ᴜsᴇʀ_ɪᴅ/ᴜsᴇʀɴᴀᴍᴇ</b>")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(str(error))

    if user.id not in seller:
        return await msg.edit(f"<b>{user.id} ʙᴇʟᴜᴍ ᴛᴇʀᴅᴀғᴛᴀʀ ᴅᴀʟᴀᴍ ᴅᴀғᴛᴀʀ ʀᴇsᴇʟʟᴇʀ</b>")

    try:
        await remove_seller(user.id)
        return await msg.edit(f"<b>❌ {user.id} ᴛᴇʟᴀʜ ᴅɪᴄᴀʙᴜᴛ ᴅᴀʀɪ ᴅᴀғᴛᴀʀ ʀᴇsᴇʟʟᴇʀ</b>")
    except Exception as error:
        return await msg.edit(str(error))


@SUB.BOT("time")
@SUB.SELLER
async def _(client, message):
    msg = await message.reply("<b>ᴛᴜɴɢɢᴜ sᴇʙᴇɴᴛᴀʀ</b>", quote=True)

    user_id, exp_day = await extract_user_and_reason(message)
    if not user_id:
        return await msg.edit(f"<b>{message.text} ᴜsᴇʀ_ɪᴅ/ᴜsᴇʀɴᴀᴍᴇ</b>")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(str(error))

    exp_day = exp_day or 30
    await add_exp_bot(user.id, int(exp_day))
    exp_time = (await get_expired_date(user.id)).strftime("%d-%m-%Y")

    await msg.edit(
        f"<b>✅ {user.id} ᴛᴇʟᴀʜ ᴅɪᴛᴀᴍʙᴀʜᴋᴀɴ {exp_day} ʜᴀʀɪ\n\nᴍᴀsᴀ ᴀᴋᴛɪғ ᴍᴇɴᴊᴀᴅɪ: {exp_time}</b>"
    )


@SUB.BOT("sh", SUB.OWNER)
async def _(client, message):
    command = get_arg(message)
    msg = await message.reply("memproses...", quote=True)
    if not command:
        return await msg.edit("noob")
    try:
        if command == "shutdown":
            await msg.delete()
            await handle_shutdown(message)
        elif command == "restart":
            await msg.delete()
            await handle_restart(message)
        elif command == "update":
            await msg.delete()
            await handle_update(message)
        elif command == "clean":
            await handle_clean(message)
            await msg.delete()
        elif command == "host":
            await handle_host(message)
            await msg.delete()
        else:
            await process_command(message, command)
            await msg.delete()
    except Exception as error:
        await msg.edit(error)


@SUB.BOT("eval", SUB.OWNER)
async def _(client, message):
    msg = await message.reply_text("Processing ...")
    cmd = get_arg(message)
    if not cmd:
        return await msg.edit("Berikan kode yang akan dievaluasi")

    reply_to_ = message.reply_to_message or message
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc = None, None, None

    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()

    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    evaluation = exc or stderr or stdout or "Success"
    final_output = f"<b>OUTPUT</b>:\n<b>{evaluation.strip()}</b>"

    if len(final_output) > 4096:
        await send_large_output(message, final_output)
    else:
        await reply_to_.reply_text(final_output, quote=True)

    await msg.delete()
