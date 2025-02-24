import urllib.request
import os
from pymongo import ReturnDocument
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
import math
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from TEAMZYRO import application, collection, db, app, user_collection


from pyrogram import enums

rarity_map = {
     "💫 Rare": "💫",
     "🌿 Medium": "🌿",
     "🦄 Legendary": "🦄",
     "💮 Special Edition": "💮",
     "🔮 Limited Edition": "🔮",
     "🎉 Festival": "🎉",
     "🍂 Seasonal": "🍂",
     "🎐 Celestial": "🎐",
     "❄️ Winter": "❄️",
     "💝 Valentine": "💝",
     "🔞 Erotic": "🔞",
}

async def handle_search(client, message, query=None, page=1, is_callback=False):
    try:
        if not query:
            args = message.command
            if len(args) < 2:
                await message.reply_text("Please provide a character name. Usage: /sips {character name}")
                return
            query = " ".join(args[1:]).strip()

        per_page = 10
        skip = (page - 1) * per_page

        # Count the total characters
        total_characters = await collection.count_documents({"name": {"$regex": query, "$options": "i"}})

        if total_characters == 0:
            await message.reply_text(f"No characters found matching: {query}")
            return

        # Fetch the characters for the current page
        characters = await collection.find({"name": {"$regex": query, "$options": "i"}}).skip(skip).limit(per_page).to_list(length=per_page)

        # Create response message
        response = f"**Total Characters Found:** {total_characters}\n\n"
        for index, character in enumerate(characters, start=1 + skip):
            rarity_emoji = rarity_map.get(character['rarity'], "❓")  # Default to ❓ if rarity is not found
            response += (
                f"◈⌠{rarity_emoji}⌡ **{index}** {character['name']}\n"
                f"Anime: {character['anime']}\n"
                f"ID: {character['id']}\n\n"
            )

        # Create pagination buttons
        buttons = []
        if page > 1:
            buttons.append(InlineKeyboardButton("⬅️ Back", callback_data=f"sips:{query}:{page - 1}"))
        if skip + per_page < total_characters:
            buttons.append(InlineKeyboardButton("➡️ Next", callback_data=f"sips:{query}:{page + 1}"))

        # Edit the message if it's a callback query, otherwise send a new one
        if is_callback:
            await message.edit_text(
                response,
                reply_markup=InlineKeyboardMarkup([buttons]) if buttons else None,
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await message.reply_text(
                response,
                reply_markup=InlineKeyboardMarkup([buttons]) if buttons else None,
                parse_mode=ParseMode.MARKDOWN
            )

    except Exception as e:
        error_message = f"Error: {str(e)}"
        if is_callback:
            await message.edit_text(error_message)
        else:
            await message.reply_text(error_message)


@app.on_callback_query(filters.regex(r"^sips:(.+):(\d+)$"))
async def handle_pagination(client, callback_query):
    try:
        data = callback_query.data.split(":")
        query = data[1]
        page = int(data[2])

        # Edit the current message with new results
        await handle_search(client, callback_query.message, query=query, page=page, is_callback=True)

    except Exception as e:
        await callback_query.answer(f"Error: {str(e)}", show_alert=True)


import datetime
from pymongo import ReturnDocument

@app.on_message(filters.command("jackpot"))
async def basket(bot, message):
    user_id = message.from_user.id
    today = datetime.date.today()

    # Check if user exists in the database
    user_data = await user_collection.find_one({"id": user_id})
    if not user_data:
        # Initialize user data
        user_data = {
            "user_id": user_id,
            "balance": 0,
            "last_played": None,
            "plays_today": 0
        }
        await collection.insert_one(user_data)

    # Check play limits
    last_played = user_data.get("last_played")
    plays_today = user_data.get("plays_today", 0)

    if last_played == str(today):
        if plays_today >= 2:
            await message.reply_text("You can only play the jackpot twice per day. Try again tomorrow!")
            return
    else:
        # Reset the play count for a new day
        plays_today = 0

    # Send dice and calculate score
    dice_message = await bot.send_dice(message.chat.id, "🎰")
    dice_score = dice_message.dice.value

    # Calculate rewards
    if dice_score == 64:
        coins_earned = 2000
    else:
        coins_earned = 5 * dice_score

    # Update user's balance and play count
    updated_user = await user_collection.find_one_and_update(
        {"id": user_id},
        {
            "$set": {"last_played": str(today)},
            "$inc": {"balance": coins_earned, "plays_today": 1}
        },
        return_document=ReturnDocument.AFTER
    )

    # Send response
    await message.reply_text(
        f"Hey {message.from_user.mention}, your score is: {dice_score}.\n"
        f"You earned **{coins_earned} coins**! 🎉\n"
        f"Your new balance is **{updated_user['balance']} coins**.",
        quote=True
    )


@app.on_message(filters.command("sips"))
async def search_characters(client, message):
    await handle_search(client, message)


async def handle_search(client, message, query=None, page=1, is_callback=False):
    try:
        if not query:
            args = message.command
            if len(args) < 2:
                await message.reply_text("Please provide a character name. Usage: /sips {character name}")
                return
            query = " ".join(args[1:]).strip()

        per_page = 10
        skip = (page - 1) * per_page

        # Count the total characters
        total_characters = await collection.count_documents({"name": {"$regex": query, "$options": "i"}})

        if total_characters == 0:
            await message.reply_text(f"No characters found matching: {query}")
            return

        # Fetch the characters for the current page
        characters = await collection.find({"name": {"$regex": query, "$options": "i"}}).skip(skip).limit(per_page).to_list(length=per_page)

        # Create response message
        response = f"**Total Characters Found:** {total_characters}\n\n"
        for index, character in enumerate(characters, start=1 + skip):
            rarity_emoji = rarity_map.get(character['rarity'], "❓")  # Default to ❓ if rarity is not found
            response += (
                f"◈⌠{rarity_emoji}⌡ **{index}** {character['name']}\n"
                f"Anime: {character['anime']}\n"
                f"ID: {character['id']}\n\n"
            )

        # Create pagination buttons
        buttons = []
        if page > 1:
            buttons.append(InlineKeyboardButton("⬅️ Back", callback_data=f"sips:{query}:{page - 1}"))
        if skip + per_page < total_characters:
            buttons.append(InlineKeyboardButton("➡️ Next", callback_data=f"sips:{query}:{page + 1}"))

        # Edit the message if it's a callback query, otherwise send a new one
        if is_callback:
            await message.edit_text(
                response,
                reply_markup=InlineKeyboardMarkup([buttons]) if buttons else None,
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await message.reply_text(
                response,
                reply_markup=InlineKeyboardMarkup([buttons]) if buttons else None,
                parse_mode=ParseMode.MARKDOWN
            )

    except Exception as e:
        error_message = f"Error: {str(e)}"
        if is_callback:
            await message.edit_text(error_message)
        else:
            await message.reply_text(error_message)


@app.on_callback_query(filters.regex(r"^sips:(.+):(\d+)$"))
async def handle_pagination(client, callback_query):
    try:
        data = callback_query.data.split(":")
        query = data[1]
        page = int(data[2])

        # Edit the current message with new results
        await handle_search(client, callback_query.message, query=query, page=page, is_callback=True)

    except Exception as e:
        await callback_query.answer(f"Error: {str(e)}", show_alert=True)

from pyrogram.enums import ParseMode

@app.on_message(filters.command("oc"))
async def rarity_count(client, message):
    try:
        # Fetch distinct rarities from the characters collection
        distinct_rarities = await collection.distinct('rarity')
        
        if not distinct_rarities:
            await message.reply_text("⚠️ No rarities found in the database.")
            return
        
        response_message = "✨ Character Count by Rarity ✨\n\n"
        
        # Loop through each rarity and count the number of characters
        for rarity in distinct_rarities:
            # Count the number of characters with the current rarity
            count = await collection.count_documents({'rarity': rarity})
            
            response_message += f"◈ {rarity} {count} character(s)\n"
        
        await message.reply_text(response_message)
    
    except Exception as e:
        await message.reply_text(f"⚠️ Error: {str(e)}")