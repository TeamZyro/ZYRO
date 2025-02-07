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

def get_current_cookie():
    cookie_dir = "cookies"
    if not os.path.exists(cookie_dir):
        os.makedirs(cookie_dir)

    cookies_files = [f for f in os.listdir(cookie_dir) if f.endswith(".txt")]
    if not cookies_files:
        return None

    return os.path.join(cookie_dir, max(cookies_files, key=extract_version))

# 🔹 Function to extract version from filename
def extract_version(filename):
    match = re.search(r"V(\d+)", filename)
    return int(match.group(1)) if match else 0

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

# 🔹 /upload Command
@bot.on_message(filters.command("upload_cookie"))
async def upload_cookie(client, message):
    if len(message.command) < 2:
        await message.reply("❌ Please specify a version. Example: `/upload V1`")
        return

    version = message.command[1]
    cookie_file = f"cookies/{version}.txt"

    if not os.path.exists(cookie_file):
        await message.reply(f"❌ Cookie file `{version}.txt` not found!")
        return

    success, result = upload_to_catbox(cookie_file)

    if success:
        collection.update_one({"version": version}, {"$set": {"url": result}}, upsert=True)
        await message.reply(f"✅ Cookie uploaded successfully!\n🔹 Version: `{version}`\n🔹 URL: {result}")
    else:
        await message.reply(f"❌ Upload failed: {result}")

# 🔹 /updatecookie Command
@bot.on_message(filters.command("update_cookie"))
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
            # Download new cookie file
            new_cookie_file = f"cookies/V{latest_version}.txt"
            response = requests.get(latest_url)
            with open(new_cookie_file, "wb") as f:
                f.write(response.content)

            await message.reply(f"✅ Cookie updated to V{latest_version}!")
            return

        await message.reply(f"🔹 Current Cookie: V{current_version}\n🔹 Latest: V{latest_version}\n❌ No update required!")
        return

    await message.reply("⚠️ No valid version found in database!")

