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
        sg = "SaveMedia_bot"  # No need for random choice as only one bot is used

        try:
            # Ensure the chat exists before sending
            bot_chat = await us.one.get_chat(sg)
            
            # Send the link to the SaveMedia bot
            sent_message = await us.one.send_message(bot_chat.id, link)
        except Exception as e:
            return await lol.edit(f"<code>Error: {e}</code>")

        await asyncio.sleep(10)  # Wait for bot response (increase if needed)

        # Fetch messages sent by SaveMedia_bot
        async for response in us.one.search_messages(bot_chat.id, limit=5):
            if response.from_user and response.from_user.username == sg:
                if response.media:
                    await message.reply_document(response.document) if response.document else await message.reply_media(response.media)
                    await lol.delete()
                    return

        # If no media was found
        await lol.edit("Sorry, I couldn't retrieve the media from the link.")
