
import os
import random
import re
import requests
from pymongo import MongoClient
from pyrogram import Client, filters

from TEAMZYRO import app as bot


# 🔹 Function to extract version from filename
def extract_version(filename):
    match = re.search(r"V(\d+)", filename)
    return int(match.group(1)) if match else 0

# 🔹 Function to get current cookie file
def get_current_cookie():
    cookie_dir = "cookies"
    if not os.path.exists(cookie_dir):
        os.makedirs(cookie_dir)

    cookies_files = [f for f in os.listdir(cookie_dir) if f.endswith(".txt")]
    if not cookies_files:
        return None

    return os.path.join(cookie_dir, max(cookies_files, key=extract_version))

# 🔹 Upload function to Catbox
@bot.on_message(filters.command("upload") & filters.private)
async def upload_cookie(client, message):
    if len(message.command) < 2:
        await message.reply("❌ Please specify a version. Example: `/upload V1`")
        return

    version = message.command[1]

    # Check if user replied with a file
    if message.reply_to_message and message.reply_to_message.document:
        file_name = f"cookies/{version}.txt"
        await message.reply_to_message.download(file_name)
    else:
        await message.reply("❌ Please reply to a TXT file with `/upload V1` format.")
        return

    # Here we no longer call upload_to_catbox, just store the file name
    # You can adjust the logic to simply store the file locally or handle it differently
    collection.update_one({"version": version}, {"$set": {"file_name": file_name}}, upsert=True)

    await message.reply(f"✅ Cookie uploaded successfully!\n🔹 Version: `{version}`\n🔹 File saved: {file_name}")
