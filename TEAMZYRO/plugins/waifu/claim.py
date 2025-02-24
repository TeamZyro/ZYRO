import asyncio
from pyrogram import Client, filters, types as t
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta
from TEAMZYRO import app as bot
from TEAMZYRO import user_collection, collection
import time

chat = "-1002289810575"
CHARACTERS_PER_PAGE = 10

# Helper function to format time
async def format_time_delta(delta):
    try:
        seconds = delta.total_seconds()
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
    except Exception as e:
        print(f"Error formatting time delta: {e}")
        return "unknown time"

# Fetch unique characters function
async def get_unique_characters(user_id, target_rarities=['💫 Rare', '🌿 Medium', '🦄 Legendary', '💮 Special Edition']):
    try:
        # Get the already claimed character ids
        user_data = await user_collection.find_one({'id': user_id}, {'characters.id': 1})
        claimed_ids = [char['id'] for char in user_data.get('characters', [])] if user_data else []

        pipeline = [
            {'$match': {'rarity': {'$in': target_rarities}, 'id': {'$nin': claimed_ids}}},
            {'$sample': {'size': 1}}  # Randomly sample one character
        ]
        cursor = collection.aggregate(pipeline)
        characters = await cursor.to_list(length=None)
        return characters if characters else []
    except Exception as e:
        print(f"Error retrieving unique characters: {e}")
        return []

# Command handler for daily claim (hclaim)
@bot.on_message(filters.command(["hclaim"]))
async def hclaim(_, message: t.Message):
    try:
        user_id = message.from_user.id
        mention = message.from_user.mention

        if str(message.chat.id) != chat:
            join_button = InlineKeyboardMarkup([
                [InlineKeyboardButton("Join Here", url="https://t.me/PiratesMainchat")]
            ])
            return await message.reply_text(
                "🥀 ᴊᴏɪɴ ᴛʜᴇ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴄʟᴀɪᴍ ʏᴏᴜʀ ᴅᴀɪʟʏ ᴄʜᴀʀᴀᴄᴛᴇʀ 😉",
                reply_markup=join_button
            )

        try:
            # Fetch user data from database
            user_data = await user_collection.find_one({'id': user_id})
            if not user_data:
                user_data = {
                    'id': user_id,
                    'username': message.from_user.username,
                    'characters': [],
                    'last_daily_reward': None
                }
                await user_collection.insert_one(user_data)

            last_claimed_date = user_data.get('last_daily_reward')
            if last_claimed_date:
                last_claimed_date = last_claimed_date.replace(tzinfo=None)
                if last_claimed_date.date() == datetime.utcnow().date():
                    remaining_time = timedelta(days=1) - (datetime.utcnow() - last_claimed_date)
                    formatted_time = await format_time_delta(remaining_time)
                    return await message.reply_text(f"⏳ *You've already claimed today! Next reward in:* {formatted_time}")

            # Fetch a unique character for the user
            unique_characters = await get_unique_characters(user_id)
            if not unique_characters:
                return await message.reply_text("🚫 *No unique characters found.*")

            # Update the user with the new character and claim time
            await user_collection.update_one(
                {'id': user_id},
                {
                    '$push': {'characters': {'$each': unique_characters}},
                    '$set': {'last_daily_reward': datetime.utcnow()}
                }
            )

            # Send character images and info
            for character in unique_characters:
                await message.reply_photo(
                    photo=character['img_url'],
                    caption=(
                        f"🎉🇨 🇴 🇳 🇬 🇷 🇦 🇹 🇺 🇱 🇦 🇹 🇮 🇴 🇳 🇸 {mention}! 😉\n"
                        f"❣️ 𝐍𝐚𝐦𝐞 : {character['name']}\n"
                        f"⚡ 𝐑𝐚𝐫𝐢𝐭𝐲 : {character['rarity']}\n"
                        f"🏝️ 𝐀𝐧𝐢𝐦𝐞 : {character['anime']}\n"
                        f"😉 Come back tomorrow for another claim!"
                    )
                )

        except Exception as e:
            print(f"Error in daily claim database logic: {e}")
            return await message.reply_text("❌ *Something went wrong, please try again later.*")

    except Exception as e:
        print(f"Error in hclaim command: {e}")
        await message.reply_text("❌ *An unexpected error occurred.*")