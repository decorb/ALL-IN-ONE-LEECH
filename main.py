# main.py — PW Token-Based + All-In-One Leech Bot

import os
import time
import subprocess
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatAction
from vars import API_ID, API_HASH, BOT_TOKEN, CHANNEL_ID
from utils import get_file_extension, clean_up
from utils_progress import progress_bar

bot = Client("pw_token_leech_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

user_data = {}

@bot.on_message(filters.command("leech") & filters.private)
async def start_leech(client, message: Message):
    user_data[message.chat.id] = {}
    await message.reply_text("🔢 Enter VID ID:")

@bot.on_message(filters.private & filters.text)
async def get_meta_inputs(client, message: Message):
    user_id = message.chat.id
    if user_id not in user_data:
        return

    u = user_data[user_id]

    if "vid_id" not in u:
        u["vid_id"] = message.text.strip()
        await message.reply_text("📚 Enter Batch Name:")
        return

    if "batch" not in u:
        u["batch"] = message.text.strip()
        await message.reply_text("📝 Enter Downloaded By (your tag):")
        return

    if "by" not in u:
        u["by"] = message.text.strip()
        await message.reply_text("📺 Enter Quality (e.g., 360p, 720p):")
        return

    if "quality" not in u:
        u["quality"] = message.text.strip()
        await message.reply_text("🔑 Enter PW Token (Authorization Header):")
        return

    if "token" not in u:
        u["token"] = message.text.strip()
        await message.reply_text("🔗 Send the video link (.m3u8 or .mpd):")
        return

    if "url" not in u:
        u["url"] = message.text.strip()
        await message.reply_text("📥 Downloading... Please wait...")

        file_name = f"PW_{int(time.time())}.mp4"
        ytdlp_cmd = [
            "yt-dlp",
            u["url"],
            "-o", file_name,
            "--add-header", f"authorization: {u['token']}"
        ]

        try:
            subprocess.run(ytdlp_cmd, check=True)
        except subprocess.CalledProcessError as e:
            await message.reply_text(f"❌ yt-dlp error: {e}")
            return

        await send_to_channel(client, message, file_name)
        clean_up(file_name)

async def send_to_channel(client, message, file_path):
    u = user_data[message.chat.id]
    file_name = os.path.basename(file_path)
    ext = get_file_extension(file_name)

    caption = (
        f"**➖➖➖➖➖➖➖**\n"
        f"**◆➤ VID_ID:** {u['vid_id']}\n"
        f"**📜 Title:** {file_name}\n"
        f"**🗂️ Batch:** {u['batch']}\n"
        f"**📁 Ext:** {ext}\n"
        f"**📺 Quality:** {u['quality']}\n\n"
        f"📥 **Downloaded By:** @{u['by'].strip('@')}\n"
        f"✯ ━━━━━━ ✿ SAMEER BHYYA ✿ ━━━━━━ ✯"
    )

    await client.send_document(
        chat_id=CHANNEL_ID,
        document=file_path,
        caption=caption
    )
    await message.reply_text("✅ Uploaded successfully!")
    user_data.pop(message.chat.id)

bot.run()
