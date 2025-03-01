from pyrogram import Client, filters
import httpx
from TEAMZYRO import app

API_URL = "https://karma-api2.vercel.app/instadl"

@app.on_message(filters.regex(r"https?://(www\.)?instagram\.com/\S+"))
async def insta_link_handler(client, message):
    link = message.text
    try:
        downloading_message = await message.reply_text("Pʀᴏᴄᴇssɪɴɢ...")

        async with httpx.AsyncClient() as http_client:  # Renamed to http_client
            response = await http_client.get(API_URL, params={"url": link})
            data = response.json()

        if "content_url" in data:
            content_url = data["content_url"]
            
            bot_info = await app.get_me()  # ✅ Correct way to get bot username
            bot_username = bot_info.username
            
            caption = f"Downloaded by @{bot_username}"  # ✅ Proper caption

            if "video" in content_url:
                await message.reply_video(content_url, caption=caption)
            else:
                await message.reply_photo(content_url, caption=caption)
        else:
            await message.reply_text("Unable to fetch content. Please check the Instagram URL.")

    except Exception as e:
        print(e)
        await message.reply_text("An error occurred while processing the request.")

    finally:
        await downloading_message.delete()

