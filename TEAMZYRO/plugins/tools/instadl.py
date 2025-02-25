from telegram import Update, Bot
import httpx

from TEAMZYRO import app
from pyrogram import filters

DOWNLOADING_STICKER_ID = (
    "CAACAgEAAx0CfD7LAgACO7xmZzb83lrLUVhxtmUaanKe0_ionAAC-gADUSkNORIJSVEUKRrhHgQ"
)
API_URL = "https://karma-api2.vercel.app/instadl"  # API URL

# इंस्टाग्राम लिंक का पता लगाने के लिए फ़िल्टर सेट करें
@app.on_message(filters.text & filters.regex(r"https?://(www\.)?instagram\.com/"))
async def instadl_auto_handler(client, message):
    link = message.text.strip()
    
    try:
        downloading_sticker = await message.reply_sticker(DOWNLOADING_STICKER_ID)

        # API से डेटा प्राप्त करें
        async with httpx.AsyncClient() as client:
            response = await client.get(API_URL, params={"url": link})
            response.raise_for_status()
            data = response.json()

        if "content_url" in data:
            content_url = data["content_url"]
            content_type = "video" if "video" in content_url else "photo"
            caption = f"Downloaded by {app.me.mention}"

            if content_type == "photo":
                await message.reply_photo(content_url, caption=caption)
            elif content_type == "video":
                await message.reply_video(content_url, caption=caption)
            else:
                await message.reply_text("Unsupported content type.")
        else:
            await message.reply_text("Unable to fetch content. Please check the Instagram URL.")

    except Exception as e:
        print(e)
        await message.reply_text("An error occurred while processing the request.")

    finally:
        await downloading_sticker.delete()
