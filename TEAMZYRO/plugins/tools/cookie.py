import os
from pyrogram import Client, filters
from TEAMZYRO import app as bot

# 🔹 Folder ensure
COOKIE_DIR = "cookies"
os.makedirs(COOKIE_DIR, exist_ok=True)

# 🔹 Function to delete old cookies and keep only the latest
def clean_cookies(latest_file):
    for file in os.listdir(COOKIE_DIR):
        file_path = os.path.join(COOKIE_DIR, file)
        if file_path != latest_file and file.endswith(".txt"):
            os.remove(file_path)

# 🔹 Upload command
@bot.on_message(filters.command("upload") & filters.private)
async def upload_cookie(client, message):
    if not message.reply_to_message or not message.reply_to_message.document:
        await message.reply("❌ Please reply to a TXT file with `/upload`.")
        return

    file_path = os.path.join(COOKIE_DIR, "cookie.txt")
    await message.reply_to_message.download(file_path)

    # Delete old cookies and keep only the latest
    clean_cookies(file_path)

    await message.reply(f"✅ Cookie uploaded successfully!\n🔹 File saved: `{file_path}`")
