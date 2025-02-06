import os
import random
import re
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from TEAMZYRO import app as bot, userbot

CHANNEL_ID = "@update_cookie"

# Bot client setup


# Function to get current cookie file
def cookies():
    cookie_dir = "cookies"
    cookies_files = [f for f in os.listdir(cookie_dir) if f.endswith(".txt")]

    if not cookies_files:
        return None

    cookie_file = os.path.join(cookie_dir, random.choice(cookies_files))
    return cookie_file

# Function to extract version from file name
def extract_version(filename):
    match = re.search(r"(\d+\.\d+)V\.txt", filename)
    return float(match.group(1)) if match else 0

# Command to check and update cookie
@bot.on_message(filters.command("update_cookie") & filters.private)
async def update_cookie(client, message):
    current_cookie = cookies()
    
    if not current_cookie:
        await message.reply("⚠️ No cookie files found!")
        return
    
    current_version = extract_version(os.path.basename(current_cookie))

    # Fetch last message from channel
    async for msg in userbot.get_chat_history(CHANNEL_ID, limit=1):
        if msg.text:
            match = re.search(r"(\d+\.\d+)V\.txt", msg.text)
            if match:
                latest_version = float(match.group(1))
                latest_file = f"{latest_version}V.txt"

                # Compare versions
                if latest_version > current_version:
                    # Download new cookie file (Assuming it's a document)
                    async for doc in bot.get_chat_history(CHANNEL_ID, limit=5):
                        if doc.document and latest_file in doc.document.file_name:
                            await userbot.download_media(doc.document, file_name=os.path.join("cookies", latest_file))
                            await message.reply(f"✅ Cookie updated to {latest_version}V!")
                            return
                
                await message.reply(f"🔹 Current Cookie: {current_version}V\n🔹 Latest: {latest_version}V\n❌ No update required!")
                return

    # If no version found in messages
    await message.reply("⚠️ No valid version found in channel!")

