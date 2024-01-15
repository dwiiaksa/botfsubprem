import asyncio
import importlib
import os

from pykeyboard import InlineKeyboard
from pyrogram.types import *

from FsubPremBot import *


@SUB.DATA("^add_bot")
async def _(client, callback_query):
    user = callback_query.from_user
    if not client.me.id == bot.me.id:
        return await callback_query.edit_message_text(
            f"""
<b>🙋🏻‍♂️ ʜᴀʟᴏ <a href=tg://user?id={user.id}>{user.first_name} {user.last_name or ''}</a></b>

<b>🗣️ ᴊɪᴋᴀ ᴀɴᴅᴀ ɪɴɢɪɴ ᴍᴇᴍʙᴜᴀᴛ ʙᴏᴛ ғɪʟᴇ sʜᴀʀɪɴɢ sᴇᴘᴇʀᴛɪ ɪɴɪ,
sɪʟᴀʜᴋᴀɴ ᴋᴜɴᴊᴜɴɢɪ ʙᴏᴛ ʀᴇsᴍɪ ᴋᴀᴍɪ @{bot.me.username}</b>
""",
            reply_markup=InlineKeyboardMarkup(Button.back()),
        )
    elif user.id not in await get_premium():
        buttons = InlineKeyboard(row_width=2)
        keyboard = []
        for i in await get_seller():
            try:
                get = await client.get_users(int(i))
                name_admin = f"{get.first_name} {get.last_name or ''}"
                id_admin = get.id
            except Exception:
                pass
            keyboard.append(
                InlineKeyboardButton(
                    name_admin,
                    user_id=id_admin,
                )
            )
        buttons.add(*keyboard)
        buttons.row(InlineKeyboardButton("ᴋᴇᴍʙᴀʟɪ", callback_data="back_start"))
        return await callback_query.edit_message_text(
            f"""
<b>🙋🏻‍♂️ ʜᴀʟᴏ <a href=tg://user?id={callback_query.from_user.id}>{callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}</a>!</b>

<b>🗣️ sɪʟᴀʜᴋᴀɴ ʜᴜʙᴜɴɢɪ sᴀʟᴀʜ sᴀᴛᴜ ᴘᴇɴᴊᴜᴀʟ ᴋᴀᴍɪ ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴜᴀᴛ ʙᴏᴛ ғɪʟᴇ-sʜᴀʀɪɴɢ</b>

<b>🔻 ᴋʟɪᴋ ᴛᴏᴍʙᴏʟ ᴅɪʙᴀᴡᴀʜ ᴜɴᴛᴜᴋ ᴍᴇɴɢʜᴜʙᴜɴɢɪ sᴀʟᴀʜ sᴀᴛᴜ ᴘᴇɴᴊᴜᴀʟ</b>
""",
            disable_web_page_preview=True,
            reply_markup=buttons,
        )
    else:
        await callback_query.message.delete()
        try:
            api = await client.ask(
                user.id,
                "<b>ᴍᴀsᴜᴋᴀɴ API_ID ᴀɴᴅᴀ, ᴅᴀᴘᴀᴛᴋᴀɴ API_ID ᴅᴀʀɪ my.telegram.org,\n\nɢᴜɴᴀᴋᴀɴ /cancel ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴀᴛᴀʟᴋᴀɴ ᴘʀᴏsᴇs</b>",
                timeout=300,
            )
        except asyncio.TimeoutError:
            return await client.send_message(
                user.id,
                "<b>ᴅɪʙᴀᴛᴀʟᴋᴀɴ sᴇᴄᴀʀᴀ ᴏᴛᴏᴍᴀᴛɪs ᴋᴀʀᴇɴᴀ ᴡᴀᴋᴛᴜ ᴛᴜɴɢɢᴜ sᴇʟᴀᴍᴀ 𝟻 ᴍᴇɴɪᴛ ᴛᴇʟᴀʜ ʙᴇʀʟᴀʟᴜ</b>",
            )
        if await is_cancel(callback_query, api.text):
            return
        try:
            api_id = int(api.text)
        except Exception as error:
            return await client.send_message(user.id, f"<b>❌ ERROR: {error}</b>")
        try:
            hash = await client.ask(
                user.id,
                "<b>ᴍᴀsᴜᴋᴀɴ API_HASH ᴀɴᴅᴀ, ᴅᴀᴘᴀᴛᴋᴀɴ API_HASH ᴅᴀʀɪ my.telegram.org,\n\nɢᴜɴᴀᴋᴀɴ /cancel ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴀᴛᴀʟᴋᴀɴ ᴘʀᴏsᴇs</b>",
                timeout=300,
            )
        except asyncio.TimeoutError:
            return await client.send_message(
                user.id,
                "<b>ᴅɪʙᴀᴛᴀʟᴋᴀɴ sᴇᴄᴀʀᴀ ᴏᴛᴏᴍᴀᴛɪs ᴋᴀʀᴇɴᴀ ᴡᴀᴋᴛᴜ ᴛᴜɴɢɢᴜ sᴇʟᴀᴍᴀ 𝟻 ᴍᴇɴɪᴛ ᴛᴇʟᴀʜ ʙᴇʀʟᴀʟᴜ</b>",
            )
        if await is_cancel(callback_query, api.text):
            return
        api_hash = hash.text
        try:
            token = await client.ask(
                user.id,
                "<b>ᴍᴀsᴜᴋᴀɴ BOT_TOKEN ᴀɴᴅᴀ, ᴅᴀᴘᴀᴛᴋᴀɴ BOT_TOKEN ᴅᴀʀɪ @BotFather,\n\nɢᴜɴᴀᴋᴀɴ /cancel ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴀᴛᴀʟᴋᴀɴ ᴘʀᴏsᴇs</b>",
                timeout=300,
            )
        except asyncio.TimeoutError:
            return await client.send_message(
                user.id,
                "<b>ᴅɪʙᴀᴛᴀʟᴋᴀɴ sᴇᴄᴀʀᴀ ᴏᴛᴏᴍᴀᴛɪs ᴋᴀʀᴇɴᴀ ᴡᴀᴋᴛᴜ ᴛᴜɴɢɢᴜ sᴇʟᴀᴍᴀ 𝟻 ᴍᴇɴɪᴛ ᴛᴇʟᴀʜ ʙᴇʀʟᴀʟᴜ</b>",
            )
        if await is_cancel(callback_query, api.text):
            return
        bot_token = token.text
        try:
            fsub = await client.ask(
                user.id,
                "<b>ᴍᴀsᴜᴋᴀɴ CHANNEL_FSUB_ID ᴀɴᴅᴀ, ɪɴɪ ᴅɪɢᴜɴᴀᴋᴀɴ sᴇʙᴀɢᴀɪ ᴄʜᴀɴɴᴇʟ sᴜʙsᴄʀɪʙᴇ ʙᴇʀᴛᴜɢᴀs ᴜɴᴛᴜᴋ ᴍᴇᴍᴀᴋsᴀ ᴘᴜɴɢɢᴜɴɢ ᴜɴᴛᴜᴋ ᴊᴏɪɴ ᴊɪᴋᴀ ᴍᴀᴜ ᴍᴇɴɢᴀᴋsᴇs ʙᴏᴛ,\n\nᴄᴀᴛᴀᴛᴀɴ: ʙᴏᴛ ʜᴀʀᴜs ʙᴇʀᴀᴅᴀ ᴅᴀʟᴀᴍ ᴄʜᴀɴɴᴇʟ Jɪᴋᴀ ᴛɪᴅᴀᴋ ᴀᴅᴀ ᴅᴀʟᴀᴍ ᴄʜᴀɴɴᴇʟ ʙᴏᴛ ᴛɪᴅᴀᴋ ᴀᴋᴀɴ ʙɪsᴀ ᴅɪ ᴀᴋᴛɪғᴋᴀɴ,\n\nɢᴜɴᴀᴋᴀɴ /cancel ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴀᴛᴀʟᴋᴀɴ ᴘʀᴏsᴇs</b>",
                timeout=300,
            )
        except asyncio.TimeoutError:
            return await client.send_message(
                user.id,
                f"<b>ᴅɪʙᴀᴛᴀʟᴋᴀɴ sᴇᴄᴀʀᴀ ᴏᴛᴏᴍᴀᴛɪs ᴋᴀʀᴇɴᴀ ᴡᴀᴋᴛᴜ ᴛᴜɴɢɢᴜ sᴇʟᴀᴍᴀ 𝟻 ᴍᴇɴɪᴛ ᴛᴇʟᴀʜ ʙᴇʀʟᴀʟᴜ</b>",
            )
        if await is_cancel(callback_query, api.text):
            return
        fsub_id = fsub.text
        try:
            post = await client.ask(
                user.id,
                "<b>ᴍᴀsᴜᴋᴀɴ CHANNEL_POST_ID ᴀɴᴅᴀ, ɪɴɪ ᴅɪɢᴜɴᴀᴋᴀɴ sᴇʙᴀɢᴀɪ ᴄʜᴀɴɴᴇʟ ᴘᴏsᴛɪɴɢᴀɴ ᴀɴᴅᴀ ʙᴇʀᴛᴜɢᴀs ᴜɴᴛᴜᴋ ᴍᴇɴʏɪᴍᴘᴀɴ ᴋᴏɴᴛᴇɴ ʏᴀɴɢ ɪɴɢɪɴ ᴅɪ sʜᴀʀᴇ ᴋᴇ ᴘᴇɴɢɢᴜɴᴀ,\n\nᴄᴀᴛᴀᴛᴀɴ: ʙᴏᴛ ʜᴀʀᴜs ʙᴇʀᴀᴅᴀ ᴅᴀʟᴀᴍ ᴄʜᴀɴɴᴇʟ ᴊɪᴋᴀ ᴛɪᴅᴀᴋ ᴀᴅᴀ ᴅᴀʟᴀᴍ ᴄʜᴀɴɴᴇʟ ʙᴏᴛ ᴛɪᴅᴀᴋ ᴀᴋᴀɴ ʙɪsᴀ ᴅɪ ᴀᴋᴛɪғᴋᴀɴ,\n\nɢᴜɴᴀᴋᴀɴ /cancel ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴀᴛᴀʟᴋᴀɴ ᴘʀᴏsᴇs</b>",
                timeout=300,
            )
        except asyncio.TimeoutError:
            return await client.send_message(
                user.id,
                f"<b>ᴅɪʙᴀᴛᴀʟᴋᴀɴ sᴇᴄᴀʀᴀ ᴏᴛᴏᴍᴀᴛɪs ᴋᴀʀᴇɴᴀ ᴡᴀᴋᴛᴜ ᴛᴜɴɢɢᴜ sᴇʟᴀᴍᴀ 𝟻 ᴍᴇɴɪᴛ ᴛᴇʟᴀʜ ʙᴇʀʟᴀʟᴜ</b>",
            )
        if await is_cancel(callback_query, api.text):
            return
        try:
            post_id = int(post.text)
        except Exception as error:
            return await client.send_message(user.id, f"<b>❌ ERROR: {error}</b>")
        try:
            owner = await client.ask(
                user.id,
                "<b>ᴍᴀsᴜᴋᴀɴ OWNER_ID ᴀɴᴅᴀ, ɪɴɪ ᴀᴋᴀɴ ᴅɪɢᴜɴᴀᴋᴀɴ sᴇʙᴀɢᴀɪ ᴀᴅᴍɪɴ ᴅɪ ʙᴏᴛ,\n\nᴜɴᴀᴋᴀɴ /cancel ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴀᴛᴀʟᴋᴀɴ ᴘʀᴏsᴇs</b>",
                timeout=300,
            )
        except asyncio.TimeoutError:
            return await client.send_message(
                user.id,
                "<b>ᴅɪʙᴀᴛᴀʟᴋᴀɴ sᴇᴄᴀʀᴀ ᴏᴛᴏᴍᴀᴛɪs ᴋᴀʀᴇɴᴀ ᴡᴀᴋᴛᴜ ᴛᴜɴɢɢᴜ sᴇʟᴀᴍᴀ 𝟻 ᴍᴇɴɪᴛ ᴛᴇʟᴀʜ ʙᴇʀʟᴀʟᴜ</b>",
            )
        if await is_cancel(callback_query, api.text):
            return
        try:
            owner_id = int(owner.text)
        except Exception as error:
            return await client.send_message(user.id, f"<b>❌ ERROR: {error}</b>")
        txt = await client.send_message(
            user.id, "<b>🔁 sɪʟᴀʜᴋᴀɴ ᴛᴜɴɢɢᴜ sᴇᴅᴀɴɢ ᴍᴇᴍᴘʀᴏsᴇs</b>"
        )
        fsub_bot = Bot(
            name=str(bot_token.split(":")[0]),
            api_id=api_id,
            api_hash=api_hash,
            bot_token=bot_token,
        )
        await fsub_bot.start()
        await add_bot(
            bot_id=fsub_bot.me.id,
            api_id=api_id,
            api_hash=api_hash,
            bot_token=bot_token,
        )
        await add_exp_bot(fsub_bot.me.id)
        await add_vars_bot(fsub_bot.me.id, fsub_id, post_id, owner_id)
        await add_bot_command(fsub_bot)
        await remove_premium(user.id)
        for mod in loadModule():
            importlib.reload(importlib.import_module(f"FsubPremBot.modules.{mod}"))
        await txt.edit(f"<b>✅ {fsub_bot.me.mention} ʙᴇʀʜᴀsɪʟ ᴅɪᴀᴋᴛɪғᴋᴀɴ")
        return await client.send_message(
            LOGS_MAKER_BOT,
            f"""
<b>❏ ғɪʟᴇ-sʜᴀʀɪɴɢ ᴅɪᴀᴋᴛɪғᴋᴀɴ</b>
<b> ├ ᴀᴋᴜɴ:</b> <a href=tg://user?id={fsub_bot.me.id}>{fsub_bot.me.first_name}</a> 
<b> ├ ɪᴅ:</b> <code>{fsub_bot.me.id}</code>
<b> ╰ ᴜsᴇʀɴᴀᴍᴇ: </b> {fsub_bot.me.username}
""",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "📁 ᴄᴇᴋ ᴍᴀsᴀ ᴀᴋᴛɪғ 📁",
                            callback_data=f"cek_masa_aktif {new_client.me.id}",
                        )
                    ],
                ]
            ),
            disable_web_page_preview=True,
        )
        os.system("rm *.session*")


@SUB.DATA("^back_start")
async def _(client, callback_query):
    return await callback_query.edit_message_text(
        await MSG.START(callback_query),
        reply_markup=InlineKeyboardMarkup(Button.start()),
    )


@SUB.DATA("^back_vars")
async def _(client, callback_query):
    return await callback_query.edit_message_text(
        "<b>⤵️ sɪʟᴀʜᴋᴀɴ ᴋʟɪᴋ sᴀʟᴀʜ sᴀᴛᴜ ᴅɪʙᴀᴡᴀʜ ɪɴɪ</b>",
        reply_markup=InlineKeyboardMarkup(Button.list_vars(client.me.id)),
    )


@SUB.DATA("^cek_status")
async def _(client, callback_query):
    return await callback_query.edit_message_text(
        await MSG.STATUS(callback_query),
        reply_markup=InlineKeyboardMarkup(Button.back()),
    )


@SUB.DATA("del_bot")
@SUB.OWNER_CB
async def _(client, callback_query):
    data = callback_query.data.split()
    for X in client._bot:
        if X.me.id == int(data[1]):
            await remove_bot(X.me.id)
            await remove_all_vars(X.me.id)
            await remove_all_user(X.me.id)
            await rem_expired_date(X.me.id)
            client._bot.remove(X)
            await client.send_message(
                LOGS_MAKER_BOT,
                MSG.EXPIRED_MSG_BOT(X),
                reply_markup=InlineKeyboardMarkup(Button.expired_button_bot(client)),
            )
            await X.stop()
            return await callback_query.edit_message_text(
                await MSG.BOT(0),
                reply_markup=InlineKeyboardMarkup(Button.bot(bot._bot[0].me.id, 0)),
            )


@SUB.DATA("^help_bot")
async def _(client, callback_query):
    vars = await get_vars(client.me.id, "OWNER_ID")
    mention = ""
    for x in str(vars).split():
        user = await client.get_users(int(x))
        mention += f"    •> <a href='tg://user?id={user.id}'>{user.first_name} {user.last_name or ''}</a>\n"
    return await callback_query.edit_message_text(
        f"""
<b>❏ ᴍᴇɴᴜ ʙᴀɴᴛᴜᴀɴ: {client.me.mention}</b>

<b>•> /start: ᴜɴᴛᴜᴋ sᴛᴀʀᴛ ʙᴏᴛ</b>
<b>•> /ping: ᴜɴᴛᴜᴋ ᴍᴇɴɢᴇᴄᴋ ᴋᴇᴄᴇᴘᴀᴛᴀɴ ʀᴇsᴘᴏɴ</b>
<b>•> /genlink (ʙᴀʟᴀs ᴋᴇ ᴘᴇsᴀɴ): ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴜᴀᴛ ʟɪɴᴋ sʜᴀʀɪɴɢ</b>
<b>•> /broadcast (ʙᴀʟᴀs ᴋᴇ ᴘᴇsᴀɴ): ᴜɴᴛᴜᴋ ᴍᴇɴɢɪʀɪᴍ ᴘᴇsᴀɴ ᴋᴇ ᴘᴇɴɢɢᴜɴᴀ ʏᴀɴɢ ᴘᴇʀɴᴀʜ sᴛᴀʀᴛ ʙᴏᴛ</b>
<b>•> /setvars (ǫᴜᴇʀʏ) (ᴠᴀʟᴜᴇ): ᴜɴᴛᴜᴋ ᴍᴇʀᴜʙᴀʜ ᴠᴀʀɪᴀʙᴇʟ</b>
<b>•> /delvars (ǫᴜᴇʀʏ) (ᴠᴀʟᴜᴇ): ᴜɴᴛᴜᴋ ᴍᴇɴɢʜᴀᴘᴜs ᴠᴀʀɪᴀʙᴇʟ</b>
<b>•> /getvars: ᴜɴᴛᴜᴋ ᴍᴇɴᴅᴀᴘᴛᴋᴀɴ ᴅᴀғᴛᴀʀ ᴠᴀʀɪᴀʙᴇʟ</b>

<b>•> ǫᴜᴇʀʏ:</b>
    <b>•> <code>FSUB</code></b>
    <b>•> <code>POST</code></b>
    <b>•> <code>OWNER</code></b>
    
<b>❏ ʙʏ ᴀᴅᴍɪɴ:</b>
{mention}

""",
        reply_markup=InlineKeyboardMarkup(Button.back()),
    )


@SUB.DATA("^(prev_b|next_b)")
async def _(client, callback_query):
    query = callback_query.data.split()
    count = int(query[1])
    if query[0] == "next_b":
        if count == len(bot._bot) - 1:
            count = 0
        else:
            count += 1
    elif query[0] == "prev_b":
        if count == 0:
            count = len(bot._bot) - 1
        else:
            count -= 1
    await callback_query.edit_message_text(
        await MSG.BOT(count),
        reply_markup=InlineKeyboardMarkup(Button.bot(bot._bot[count].me.id, count)),
    )


@SUB.DATA("^(db_post|db_fsub|db_owner)")
async def _(client, callback_query):
    query = callback_query.data.split()
    try:
        if query[0] == "db_fsub":
            text = await MSG.DB_FSUB(client)
        elif query[0] == "db_post":
            text = await MSG.DB_POST(client)
        elif query[0] == "db_owner":
            text = await MSG.DB_OWNER(client)
    except Exception as error:
        text = error
    await callback_query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "• ᴋᴇᴍʙᴀʟɪ •",
                        callback_data="back_vars",
                    )
                ],
            ]
        ),
        disable_web_page_preview=True,
    )


@SUB.DATA("^cek_masa_aktif")
async def _(client, callback_query):
    user_id = int(callback_query.data.split()[1])
    expired = await get_expired_date(user_id)
    try:
        xxxx = (expired - datetime.now()).days
        return await callback_query.answer(f"⏳ ᴛɪɴɢɢᴀʟ {xxxx} ʜᴀʀɪ ʟᴀɢɪ", True)
    except:
        return await callback_query.answer("✅ sᴜᴅᴀʜ ᴛɪᴅᴀᴋ ᴀᴋᴛɪғ", True)


SUPPORT = {}


@SUB.DATA("^support")
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    full_name = f"{callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}"
    get = await client.get_users(user_id)
    await callback_query.message.delete()
    SUPPORT.setdefault(client.me.id, []).append(get.id)
    try:
        button = [
            [InlineKeyboardButton("❌ ʙᴀᴛᴀʟᴋᴀɴ", callback_data=f"batal {user_id}")]
        ]
        pesan = await client.ask(
            user_id,
            f"<b>✍️ sɪʟᴀʜᴋᴀɴ ᴋɪʀɪᴍ ᴘᴇʀᴛᴀɴʏᴀᴀɴ ᴀɴᴅᴀ: {full_name}</b>",
            reply_markup=InlineKeyboardMarkup(button),
            timeout=90,
        )
    except asyncio.TimeoutError as out:
        if get.id in SUPPORT.get(client.me.id, []):
            SUPPORT[client.me.id].remove(get.id)
            buttons = Button.start(callback_query)
            return await callback_query.edit_message_text(
                await MSG.START(callback_query),
                reply_markup=InlineKeyboardMarkup(buttons),
            )
    text = f"<b>💬 ᴘᴇʀᴛᴀɴʏᴀᴀɴ ᴀɴᴅᴀ sᴜᴅᴀʜ ᴛᴇʀᴋɪʀɪᴍ: {full_name}</b>"
    buttons = [
        [
            InlineKeyboardButton("👤 ᴘʀᴏꜰɪʟ", callback_data=f"profil {user_id}"),
            InlineKeyboardButton("ᴊᴀᴡᴀʙ 💬", callback_data=f"jawab_pesan {user_id}"),
        ]
    ]
    if get.id in SUPPORT.get(client.me.id, []):
        try:
            await pesan.copy(
                OWNER_ID,
                reply_markup=InlineKeyboardMarkup(buttons),
            )
            SUPPORT[client.me.id].remove(get.id)
            await pesan.request.edit(
                f"<b>✍️ sɪʟᴀʜᴋᴀɴ ᴋɪʀɪᴍ ᴘᴇʀᴛᴀɴʏᴀɴ ᴀɴᴅᴀ: {full_name}</b>"
            )
            return await client.send_message(user_id, text)
        except Exception as error:
            return await client.send_message(user_id, error)


@SUB.DATA("^jawab_pesan")
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    full_name = f"{callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}"
    get = await client.get_users(user_id)
    user_ids = int(callback_query.data.split()[1])
    SUPPORT.setdefault(client.me.id, []).append(get.id)
    try:
        button = [
            [InlineKeyboardButton("❌ ʙᴀᴛᴀʟᴋᴀɴ", callback_data=f"batal {user_id}")]
        ]
        pesan = await client.ask(
            user_id,
            f"<b>✉️ sɪʟᴀʜᴋᴀɴ ᴋɪʀɪᴍ ʙᴀʟᴀsᴀɴ ᴀɴᴅᴀ: {full_name}</b>",
            reply_markup=InlineKeyboardMarkup(button),
            timeout=300,
        )
    except asyncio.TimeoutError:
        if get.id in SUPPORT.get(client.me.id, []):
            SUPPORT[client.me.id].remove(get.id)
            buttons = Button.start(callback_query)
            return await callback_query.edit_message_text(
                await MSG.START(callback_query),
                reply_markup=InlineKeyboardMarkup(buttons),
            )
    text = f"<b>✅ ᴘᴇsᴀɴ ʙᴀʟᴀsᴀɴ ᴀɴᴅᴀ ᴛᴇʟᴀʜ ᴛᴇʀᴋɪʀɪᴍ: {full_name}</b>"
    if not user_ids == OWNER_ID:
        buttons = [[InlineKeyboardButton("💬 ᴊᴀᴡᴀʙ ᴘᴇsᴀɴ 💬", f"jawab_pesan {user_id}")]]
    else:
        buttons = [
            [
                InlineKeyboardButton("👤 ᴘʀᴏꜰɪʟ", callback_data=f"profil {user_id}"),
                InlineKeyboardButton("ᴊᴀᴡᴀʙ 💬", callback_data=f"jawab_pesan {user_id}"),
            ]
        ]
    if get.id in SUPPORT.get(client.me.id, []):
        try:
            await pesan.copy(
                user_ids,
                reply_markup=InlineKeyboardMarkup(buttons),
            )
            SUPPORT[client.me.id].remove(get.id)
            await pesan.request.edit(
                f"<b>✉️ sɪʟᴀʜᴋᴀɴ ᴋɪʀɪᴍ ʙᴀʟᴀsᴀɴ ᴀɴᴅᴀ: {full_name}</b>",
            )
            await client.send_message(user_id, text)
        except Exception as error:
            return await callback_query.edit_message_text(error)


@SUB.DATA("^profil")
async def _(client, callback_query):
    user_id = int(callback_query.data.split()[1])
    try:
        get = await client.get_users(user_id)
        first_name = f"{get.first_name}"
        last_name = f"{get.last_name}"
        full_name = f"{get.first_name} {get.last_name or ''}"
        username = f"{get.username}"
        msg = (
            f"<b>👤 <a href=tg://user?id={get.id}>{full_name}</a></b>\n"
            f"<b> ┣ ɪᴅ ᴘᴇɴɢɢᴜɴᴀ:</b> <code>{get.id}</code>\n"
            f"<b> ┣ ɴᴀᴍᴀ ᴅᴇᴘᴀɴ:</b> {first_name}\n"
        )
        if last_name != "None":
            msg += f"<b> ┣ ɴᴀᴍᴀ ʙᴇʟᴀᴋᴀɴɢɴʏᴀ:</b> {last_name}\n"
        if username != "None":
            msg += f"<b> ┣ ᴜsᴇʀɴᴀᴍᴇ:</b> @{username}\n"
        msg += f"<b> ┗ ʙᴏᴛ: {client.me.mention}\n"
        buttons = [
            [
                InlineKeyboardButton(
                    f"{full_name}",
                    url=f"tg://openmessage?user_id={get.id}",
                )
            ]
        ]
        await callback_query.message.reply_text(
            msg, reply_markup=InlineKeyboardMarkup(buttons)
        )
    except Exception as why:
        await callback_query.message.reply_text(why)


@SUB.DATA("^batal")
async def _(client, callback_query):
    user_id = int(callback_query.data.split()[1])
    if user_id in SUPPORT.get(client.me.id, []):
        try:
            SUPPORT[client.me.id].remove(user_id)
            buttons = Button.start()
            await callback_query.edit_message_text(
                await MSG.START(callback_query),
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        except Exception as why:
            await callback_query.message.reply_text(f"<b>❌ ɢᴀɢᴀʟ ᴅɪʙᴀᴛᴀʟᴋᴀɴ! {why}</b>")


async def is_cancel(callback_query, text):
    if text.startswith("/cancel"):
        await callback_query._client.send_message(
            callback_query.from_user.id, "<b>pembatalan dilakukan!</b>"
        )
        return True
    return False
