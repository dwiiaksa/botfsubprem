import asyncio
import base64
import os
import platform
import subprocess
import sys
from datetime import datetime
from io import BytesIO
from time import time as waktunya

import psutil
from pyrogram import enums
from pyrogram.types import *

from FsubPremBot import bot
from FsubPremBot.helpers.database import *

start_time = waktunya()


async def get_time(seconds):
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "ᴍ", "ʜ", "ᴅ", "ᴡ", "ᴍᴏ"]

    while count < 6:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        elif count < 4:
            remainder, result = divmod(seconds, 24)
        elif count < 5:
            remainder, result = divmod(seconds, 7)
        else:
            remainder, result = divmod(seconds, 30 * 24 * 60 * 60)

        if seconds == 0 and remainder == 0:
            break

        time_list.append(int(result))
        seconds = int(remainder)

    for i in range(len(time_list)):
        time_list[i] = str(time_list[i]) + time_suffix_list[i]

    if len(time_list) >= 4:
        up_time += time_list.pop() + ":"

    time_list.reverse()
    up_time += ":".join(time_list)

    return up_time


def get_file_id(msg):
    if msg.media:
        for message_type in (
            "photo",
            "animation",
            "audio",
            "document",
            "video",
            "video_note",
            "voice",
            "contact",
            "dice",
            "poll",
            "location",
            "venue",
            "sticker",
        ):
            obj = getattr(msg, message_type)
            if obj:
                setattr(obj, "message_type", message_type)
                return obj


async def extract_userid(message, text):
    def is_int(text):
        try:
            int(text)
        except ValueError:
            return False
        return True

    text = text.strip()

    if is_int(text):
        return int(text)

    entities = message.entities
    app = message._client
    entity = entities[1 if message.text.startswith("/") else 0]
    if entity.type == enums.MessageEntityType.MENTION:
        return (await app.get_users(text)).id
    if entity.type == enums.MessageEntityType.TEXT_MENTION:
        return entity.user.id
    return None


async def extract_user_and_reason(message, sender_chat=False):
    args = message.text.strip().split()
    text = message.text
    user = None
    reason = None
    if message.reply_to_message:
        reply = message.reply_to_message
        if not reply.from_user:
            if (
                reply.sender_chat
                and reply.sender_chat != message.chat.id
                and sender_chat
            ):
                id_ = reply.sender_chat.id
            else:
                return None, None
        else:
            id_ = reply.from_user.id

        if len(args) < 2:
            reason = None
        else:
            reason = text.split(None, 1)[1]
        return id_, reason

    if len(args) == 2:
        user = text.split(None, 1)[1]
        return await extract_userid(message, user), None

    if len(args) > 2:
        user, reason = text.split(None, 2)[1:]
        return await extract_userid(message, user), reason

    return user, reason


async def extract_user(message):
    return (await extract_user_and_reason(message))[0]


async def add_bot_command(client):
    await client.set_bot_commands(
        [
            BotCommand("start", "Start bot"),
            BotCommand("genlink", "untuk membuat link sharing"),
            BotCommand("setvars", "untuk mengatur variabel"),
            BotCommand("delvars", "untuk menghapus variabel"),
            BotCommand("getvars", "untuk mendapatkan daftar variabel"),
            BotCommand("broadcast", "untuk mengirimkan pesan yang pernah start bot"),
            BotCommand("ping", "untuk mengecek kecepatan respon"),
        ]
    )


def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


def get_arg(message):
    if message.reply_to_message and len(message.command) < 2:
        msg = message.reply_to_message.text or message.reply_to_message.caption
        if not msg:
            return ""
        msg = msg.encode().decode("UTF-8")
        msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
        return msg
    elif len(message.command) > 1:
        return message.text.split(None, 1)[1]
    else:
        return ""


async def encode(string):
    string_bytes = string.encode("ascii")
    base64_bytes = base64.urlsafe_b64encode(string_bytes)
    return (base64_bytes.decode("ascii")).strip("=")


async def decode(base64_string):
    base64_string = base64_string.strip("=")
    base64_bytes = (base64_string + "=" * (-len(base64_string) % 4)).encode("ascii")
    string_bytes = base64.urlsafe_b64decode(base64_bytes)
    return string_bytes.decode("ascii")


async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {l_}" for l_ in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)


async def bash(cmd):
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    err = stderr.decode().strip()
    out = stdout.decode().strip()
    return out, err


class MSG:
    async def DB_POST(client):
        vars = await all_vars(client.me.id)
        text = ""
        for key, value in vars.items():
            if key == "CHANNEL_POST_ID":
                get = await client.get_chat(int(value))
                text += f"<b>📣 ᴄʜᴀɴɴᴇʟ_ᴅᴀᴛᴀʙᴀsᴇ:</b>\n    • [{get.title}]({get.invite_link}) - <code>{get.id}</code>\n"
        return text

    async def DB_FSUB(client):
        vars = await all_vars(client.me.id)
        text = ""
        for key, value in vars.items():
            if key == "CHANNEL_FSUB_ID":
                text += "<b>💡 ᴄʜᴀɴɴᴇʟ_ғsᴜʙ:</b>"
                for x in str(value).split():
                    get = await client.get_chat(int(x))
                    text += f"\n   • [{get.title}]({get.invite_link}) - <code>{get.id}</code>"
        return text

    async def DB_OWNER(client):
        vars = await all_vars(client.me.id)
        text = ""
        for key, value in vars.items():
            if key == "OWNER_ID":
                text += "<b>✨ ᴏᴡɴᴇʀ_ʙᴏᴛ:</b>"
                for x in str(value).split():
                    get = await client.get_users(int(x))
                    text += f"\n    • [{get.first_name} {get.last_name or ''}](tg://user?id={get.id}) - <code>{get.id}</code>"
        return text

    async def BOT(count):
        expired_date = await get_expired_date(bot._bot[int(count)].me.id)
        return f"""
<b>❏ ʙᴏᴛ ᴋᴇ</b> <code>{int(count) + 1}/{len(bot._bot)}</code>
<b> ├ ɴᴀᴍᴇ:</b> <a href=tg://user?id={bot._bot[int(count)].me.id}>{bot._bot[int(count)].me.first_name}</a>
<b> ├ ɪᴅ:</b> <code>{bot._bot[int(count)].me.id}</code> 
<b> ├ ᴜsᴇʀɴᴀᴍᴇ:</b> @{bot._bot[int(count)].me.username}
<b> ╰ ᴇxᴘɪʀᴇᴅ</b> <code>{expired_date.strftime('%d-%m-%Y')}</code>
"""

    def EXPIRED_MSG_BOT(X):
        return f"""
<b>❏ ᴘᴇᴍʙᴇʀɪᴛᴀʜᴜᴀɴ</b>
<b> ├ ʙᴏᴛ:</b> <a href=tg://user?id={X.me.id}>{X.me.first_name}</a>
<b> ├ ᴜsᴇʀɴᴀᴍᴇ:</b> @{X.me.username}
<b> ├ ɪᴅ:</b> <code>{X.me.id}</code>
<b> ╰ ᴍᴀsᴀ ᴀᴋᴛɪꜰ ᴛᴇʟᴀʜ ʜᴀʙɪs</b>
"""

    async def START(message):
        user = message.from_user
        client = message._client
        text = f"""
<b>👋🏻 ʜᴀʟᴏ <a href=tg://user?id={user.id}>{user.first_name} {user.last_name or ''}</a> !

💬 @{client.me.username} ᴀᴅᴀʟᴀʜ ʙᴏᴛ ғɪʟᴇ-sʜᴀʀɪɴɢ ᴘʀᴇᴍɪᴜᴍ.

✨ ᴋᴀᴍᴜ ᴅᴀᴘᴀᴛ ᴍᴇᴍʙᴜᴀᴛ ʙᴏᴛ Fɪʟᴇ-Sʜᴀʀᴇ ᴅᴇɴɢᴀɴ ᴍᴜᴅᴀʜ ᴍᴇɴɢɢᴜɴᴀᴋᴀɴ ʙᴏᴛ ɪɴɪ</b>
"""
        return text

    async def STATUS(message):
        mention = ""
        client = message._client
        saved = await get_served_user(client.me.id)
        expired = (await get_expired_date(client.me.id)).strftime("%d-%m-%Y")
        uptime = await get_time((waktunya() - start_time))
        vars = await get_vars(client.me.id, "OWNER_ID")
        for x in str(vars).split():
            owner = await client.get_users(int(x))
            mention += f"    •> <a href=tg://user?id={owner.id}>{owner.first_name} {owner.last_name or ''}</a>\n"
        text = f"""
<b>•> ʙᴏᴛ: {client.me.mention}</b>

<b>•> ᴇxᴘɪʀᴇᴅ_ᴏɴ: <code>{expired}</code></b>

<b>•> sᴀᴠᴇᴅ_ᴜsᴇʀ: <code>{len(saved)}</code></b>

<b>•> sᴛᴀʀᴛ_ᴜᴘᴛɪᴍᴇ: {uptime}</b>

<b>•> ᴏᴡɴᴇʀ_ɴᴀᴍᴇ:</b>
{mention}
"""
        return text


class Button:
    def list_vars(user_id):
        button = [
            [
                InlineKeyboardButton(
                    "📣 ᴅᴀᴛᴀʙᴀsᴇ",
                    callback_data=f"db_post {int(user_id)}",
                ),
                InlineKeyboardButton(
                    "sᴜʙsᴄʀɪʙᴇ 💡",
                    callback_data=f"db_fsub {int(user_id)}",
                ),
            ],
            [
                InlineKeyboardButton(
                    "✨ ᴏᴡɴᴇʀ ʙᴏᴛ ✨", callback_data=f"db_owner {int(user_id)}"
                ),
            ],
        ]
        return button

    def bot(user_id, count):
        button = [
            [
                InlineKeyboardButton(
                    "📁 ʜᴀᴘᴜs ᴅᴀʀɪ ᴅᴀᴛᴀʙᴀsᴇ 📁",
                    callback_data=f"del_bot {int(user_id)}",
                )
            ],
            [
                InlineKeyboardButton(
                    "⏳ ᴄᴇᴋ ᴍᴀsᴀ ᴀᴋᴛɪғ ⏳",
                    callback_data=f"cek_masa_aktif {int(user_id)}",
                )
            ],
            [
                InlineKeyboardButton("⬅️", callback_data=f"prev_b {int(count)}"),
                InlineKeyboardButton("➡️", callback_data=f"next_b {int(count)}"),
            ],
        ]
        return button

    def expired_button_bot(x):
        button = [
            [
                InlineKeyboardButton(
                    text=f"{x.me.first_name}",
                    url=f"https://t.me/{x.me.username}",
                )
            ]
        ]
        return button

    def back():
        button = [[InlineKeyboardButton("• ᴋᴇᴍʙᴀʟɪ •", callback_data="back_start")]]
        return button

    def share(link):
        button = [
            [
                InlineKeyboardButton(
                    "sʜᴀʀᴇ ʟɪɴᴋ", url=f"https://telegram.me/share/url?url={link}"
                )
            ]
        ]
        return button

    def start():
        button = [
            [
                InlineKeyboardButton(
                    "🔥 ʙᴜᴀᴛ ғɪʟᴇ-sʜᴀʀɪɴɢ ʙᴏᴛ 🔥", callback_data="add_bot"
                )
            ],
            [
                InlineKeyboardButton("📝 sᴛᴀᴛᴜs", callback_data="cek_status"),
            ],
            [
                InlineKeyboardButton("✨ ʙᴀɴᴛᴜᴀɴ", callback_data="help_bot"),
                InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ 🧑‍💻", callback_data="support"),
            ],
        ]
        return button


async def handle_shutdown(message):
    await message.reply("✅ System berhasil dimatikan", quote=True)
    os.system(f"kill -9 {os.getpid()}")


async def handle_restart(message):
    await message.reply("✅ System berhasil direstart", quote=True)
    os.execl(sys.executable, sys.executable, "-m", "FsubPremBot")


async def handle_update(message):
    out = subprocess.check_output(["git", "pull"]).decode("UTF-8")
    if "Already up to date." in str(out):
        return await message.reply(out, quote=True)
    elif int(len(str(out))) > 4096:
        await send_large_output(message, out)
    else:
        await message.reply(f"```{out}```", quote=True)
    os.execl(sys.executable, sys.executable, "-m", "FsubPremBot")


async def handle_clean(message):
    count = 0
    for file_name in os.popen("ls").read().split():
        try:
            os.remove(file_name)
            count += 1
        except:
            pass
    await message.reply(f"✅ {count} sampah berhasil di bersihkan")


async def handle_host(message):
    system_info = get_system_info()
    formatted_info = format_system_info(system_info)
    await message.reply(formatted_info, quote=True)


async def process_command(message, command):
    result = (await bash(command))[0]
    if int(len(str(result))) > 4096:
        await send_large_output(message, result)
    else:
        await message.reply(result)


async def send_large_output(message, output):
    with BytesIO(str.encode(str(output))) as out_file:
        out_file.name = "result.txt"
        await message.reply_document(document=out_file)


def get_system_info():
    uname = platform.uname()
    cpufreq = psutil.cpu_freq()
    svmem = psutil.virtual_memory()
    return {
        "system": uname.system,
        "release": uname.release,
        "version": uname.version,
        "machine": uname.machine,
        "boot_time": psutil.boot_time(),
        "cpu_physical_cores": psutil.cpu_count(logical=False),
        "cpu_total_cores": psutil.cpu_count(logical=True),
        "cpu_max_frequency": cpufreq.max,
        "cpu_min_frequency": cpufreq.min,
        "cpu_current_frequency": cpufreq.current,
        "cpu_percent_per_core": [
            percentage for percentage in psutil.cpu_percent(percpu=True)
        ],
        "cpu_total_usage": psutil.cpu_percent(),
        "network_upload": get_size(psutil.net_io_counters().bytes_sent),
        "network_download": get_size(psutil.net_io_counters().bytes_recv),
        "memory_total": get_size(svmem.total),
        "memory_available": get_size(svmem.available),
        "memory_used": get_size(svmem.used),
        "memory_percentage": svmem.percent,
    }


def format_system_info(system_info):
    formatted_info = "Informasi Sistem\n"
    formatted_info += f"Sistem   : {system_info['system']}\n"
    formatted_info += f"Rilis    : {system_info['release']}\n"
    formatted_info += f"Versi    : {system_info['version']}\n"
    formatted_info += f"Mesin    : {system_info['machine']}\n"

    boot_time = datetime.fromtimestamp(system_info["boot_time"])
    formatted_info += f"Waktu Hidup: {boot_time.day}/{boot_time.month}/{boot_time.year}  {boot_time.hour}:{boot_time.minute}:{boot_time.second}\n"

    formatted_info += "\nInformasi CPU\n"
    formatted_info += (
        "Physical cores   : " + str(system_info["cpu_physical_cores"]) + "\n"
    )
    formatted_info += "Total cores      : " + str(system_info["cpu_total_cores"]) + "\n"
    formatted_info += f"Max Frequency    : {system_info['cpu_max_frequency']:.2f}Mhz\n"
    formatted_info += f"Min Frequency    : {system_info['cpu_min_frequency']:.2f}Mhz\n"
    formatted_info += (
        f"Current Frequency: {system_info['cpu_current_frequency']:.2f}Mhz\n\n"
    )
    formatted_info += "CPU Usage Per Core\n"

    for i, percentage in enumerate(system_info["cpu_percent_per_core"]):
        formatted_info += f"Core {i}  : {percentage}%\n"
    formatted_info += "Total CPU Usage\n"
    formatted_info += f"Semua Core: {system_info['cpu_total_usage']}%\n"

    formatted_info += "\nBandwith Digunakan\n"
    formatted_info += f"Unggah  : {system_info['network_upload']}\n"
    formatted_info += f"Download: {system_info['network_download']}\n"

    formatted_info += "\nMemori Digunakan\n"
    formatted_info += f"Total     : {system_info['memory_total']}\n"
    formatted_info += f"Available : {system_info['memory_available']}\n"
    formatted_info += f"Used      : {system_info['memory_used']}\n"
    formatted_info += f"Percentage: {system_info['memory_percentage']}%\n"
    return f"<b>{formatted_info}</b>"
