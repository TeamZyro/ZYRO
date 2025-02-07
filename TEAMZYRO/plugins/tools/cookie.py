import os
import random
import re
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import os
import random
import re
import requests
from pymongo import MongoClient
from pyrogram import Client, filters

from TEAMZYRO import app as bot

MONGO_URI = "mongodb+srv://test12:test12@cluster0.z1pajuv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["cookie_db"]
collection = db["cookies"]


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
def upload_to_catbox(file_path):
    url = "https://catbox.moe/user/api.php"
    files = {'fileToUpload': open(file_path, 'rb')}
    data = {"reqtype": "fileupload"}

    response = requests.post(url, files=files, data=data)
    files['fileToUpload'].close()

    if response.status_code == 200:
        return True, response.text.strip()
    else:
        return False, f"Error: {response.status_code} - {response.text}"

# 🔹 /upload Command (With Reply File Support)
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

    success, result = upload_to_catbox(file_name)

    if success:
        collection.update_one({"version": version}, {"$set": {"url": result}}, upsert=True)
        await message.reply(f"✅ Cookie uploaded successfully!\n🔹 Version: `{version}`\n🔹 URL: {result}")
    else:
        await message.reply(f"❌ Upload failed: {result}")

# 🔹 /updatecookie Command (Auto-Delete Old File)
@bot.on_message(filters.command("updatecookie") & filters.private)
async def update_cookie(client, message):
    current_cookie = get_current_cookie()

    if not current_cookie:
        await message.reply("⚠️ No cookie files found!")
        return

    current_version = extract_version(os.path.basename(current_cookie))

    # Fetch latest version from MongoDB
    latest_cookie = collection.find_one({}, sort=[("version", -1)])

    if latest_cookie:
        latest_version = int(latest_cookie["version"][1:])
        latest_url = latest_cookie["url"]

        if latest_version > current_version:
            # Delete old cookie
            os.remove(current_cookie)

            # Download new cookie file
            new_cookie_file = f"cookies/V{latest_version}.txt"
            response = requests.get(latest_url)
            with open(new_cookie_file, "wb") as f:
                f.write(response.content)

            await message.reply(f"✅ Cookie updated to V{latest_version}!\n🔹 Old version deleted!")
            return

        await message.reply(f"🔹 Current Cookie: V{current_version}\n🔹 Latest: V{latest_version}\n❌ No update required!")
        return

    await message.reply("⚠️ No valid version found in database!")

