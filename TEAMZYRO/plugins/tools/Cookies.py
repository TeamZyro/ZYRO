import os
import shutil
import httpx
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Bot credentials
from TEAMZYRO import app

COOKIE_FOLDER = "cookies"  # Folder to store cookies

# Ensure cookie folder exists
os.makedirs(COOKIE_FOLDER, exist_ok=True)

async def check_cookie(file_path):
    """Check if the cookie is live or dead."""
    with open(file_path, "r") as file:
        cookies = file.read().strip()

    headers = {
        "Cookie": cookies,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("https://www.youtube.com/", headers=headers)
            if "Sign in" in response.text or response.status_code == 401:
                return False  # Dead cookie
            return True  # Live cookie
    except:
        return False

@app.on_message(filters.command("cookieck") & filters.reply)
async def cookie_checker(bot, message):
    """Check the replied cookie file."""
    if not message.reply_to_message or not message.reply_to_message.document:
        return await message.reply("Reply to a .txt file containing the cookie.")

    file = message.reply_to_message.document
    if not file.file_name.endswith(".txt"):
        return await message.reply("Please reply with a valid .txt file.")

    # Download file
    file_path = os.path.join(COOKIE_FOLDER, file.file_name)
    await message.reply_to_message.download(file_path)

    # Check cookie
    is_live = await check_cookie(file_path)

    if is_live:
        buttons = [
            [InlineKeyboardButton("✅ Upload Cookie", callback_data=f"upload:{file.file_name}")]
        ]
        await message.reply("✅ Cookie is **LIVE**!", reply_markup=InlineKeyboardMarkup(buttons))
    else:
        buttons = [
            [InlineKeyboardButton("🗑 Delete", callback_data=f"delete:{message.message_id}")]
        ]
        await message.reply("❌ Cookie is **DEAD**!", reply_markup=InlineKeyboardMarkup(buttons))

@app.on_callback_query()
async def handle_callback(bot, query):
    """Handle button clicks."""
    action, value = query.data.split(":")

    if action == "upload":
        # Delete old cookies
        for file in os.listdir(COOKIE_FOLDER):
            os.remove(os.path.join(COOKIE_FOLDER, file))
        
        # Move new cookie
        old_path = os.path.join(COOKIE_FOLDER, value)
        new_path = os.path.join(COOKIE_FOLDER, "active_cookie.txt")
        shutil.move(old_path, new_path)

        await query.message.edit_text("✅ Cookie uploaded successfully!")
    
    elif action == "delete":
        await bot.delete_messages(query.message.chat.id, int(value))


