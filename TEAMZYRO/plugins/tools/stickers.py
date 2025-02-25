from TEAMZYRO import app
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
from bs4 import BeautifulSoup
import cloudscraper
import asyncio  # Required for async sleep

scraper = cloudscraper.create_scraper()
MAX_LENGTH = 4000  # Safe limit under 4096

@app.on_message(filters.command("sticker"))
async def find_sticker(_, message):
    if len(message.command) < 2:
        await message.reply_text("❌ **Usage:** /sticker <sticker name>")
        return

    query = "+".join(message.command[1:])
    await send_sticker_results(message, query, page=1)

async def send_sticker_results(message, query, page):
    search_url = f"https://combot.org/stickers?page={page}&q={query}"

    try:
        response = scraper.get(search_url)
        response.raise_for_status()
    except Exception as e:
        await message.reply_text(f"🚫 **Error:** {str(e)}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a", href=True)

    sticker_links = set()
    for link in links:
        href = link["href"]
        if href.startswith("/stickers/"):
            sticker_links.add(f"https://t.me/addstickers/{href.split('/')[-1]}")

    if not sticker_links:
        await message.reply_text("❌ **No sticker packs found on this page!**")
        return

    reply_text = f"🎨 **Sticker Packs for:** `{query}` (Page {page})\n\n"
    message_parts = []
    
    for link in sticker_links:
        if len(reply_text) + len(link) + 2 > MAX_LENGTH:
            message_parts.append(reply_text)
            reply_text = ""
        reply_text += link + "\n"

    if reply_text:
        message_parts.append(reply_text)

    # Pagination buttons
    buttons = []
    if page > 1:
        buttons.append(InlineKeyboardButton("⬅️ Previous", callback_data=f"sticker_{query}_{page-1}"))
    buttons.append(InlineKeyboardButton("➡️ Next", callback_data=f"sticker_{query}_{page+1}"))

    keyboard = InlineKeyboardMarkup([buttons])

    await message.reply_text(message_parts[0], disable_web_page_preview=True, reply_markup=keyboard)

@app.on_callback_query(filters.regex(r"sticker_(.*)_(\d+)"))
async def pagination_callback(_, query):
    query_data = query.data.split("_")
    sticker_name = query_data[1]
    page_number = int(query_data[2])

    # Send "Fetching new stickers..." message
    fetching_msg = await query.message.edit_text("🔄 Fetching new stickers...")
    
    await asyncio.sleep(1)  # 1-second delay before updating message to prevent flood error
    
    await send_sticker_results(query.message, sticker_name, page_number)
    
    # Delete the "Fetching new stickers..." message
    await fetching_msg.delete()
