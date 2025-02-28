import random

import asyncio
import re
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.raw.functions.messages import DeleteHistory

from TEAMZYRO import userbot as us, app
from TEAMZYRO.core.userbot import assistants

# Updated regex pattern to match any Instagram link
INSTAGRAM_LINK_PATTERN = r"(https?://(www\.)?instagram\.com/[^ ]+)"

@app.on_message(filters.text)
async def handle_instagram_links(client: Client, message: Message):
    if message.reply_to_message:
        return  # Ignore replies for this handler

    # Check if the message contains an Instagram link
    if re.search(INSTAGRAM_LINK_PATTERN, message.text):
        lol = await message.reply("<code>Processing...</code>")
        link = message.text.strip()

        # Choose the bot to send the message to
        bo = ["SaveMedia_bot"]
        sg = random.choice(bo)

        try:
            # Send the link to the SaveMedia bot
            a = await us.one.send_message(sg, link)
            await a.delete()
        except Exception as e:
            return await lol.edit(f"<code>Error: {e}</code>")

        await asyncio.sleep(1)

        # Check for the response from SaveMedia bot
        async for stalk in us.one.search_messages(a.chat.id):
            if stalk.text is None:
                continue
            if stalk.media:  # If the response contains media
                await message.reply_media(stalk.media)
                break  # Exit the loop after sending the media
        else:
            # If no media was found in the response
            await message.reply("Sorry, I couldn't retrieve the media from the link.")

        await lol.delete()
