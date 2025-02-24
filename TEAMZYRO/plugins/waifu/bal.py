from TEAMZYRO import *

import urllib.request
import uuid
import requests
import random
import html
import logging
from pymongo import ReturnDocument
from typing import List
from bson import ObjectId
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import CommandHandler, CallbackContext, CallbackQueryHandler
from datetime import datetime, timedelta
import asyncio

import config

CHARA_CHANNEL_ID = config.CHARA_CHANNEL_ID
PHOTO_URL = config.START_IMG_URL
UPDATE_CHAT = config.SUPPORT_CHAT
OWNER_ID = config.OWNER_ID
SUPPORT_CHAT = config.SUPPORT_CHANNEL

shops_collection = db["shops"]

# Logging configuration
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)
LOGGER = logging.getLogger(__name__)


# Rewards for consecutive days
daily_rewards = {
    1: 40,
    2: 60,
    3: 80,
    4: 100,
}

# Logging configuration
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)
LOGGER = logging.getLogger(__name__)



async def check_balance(update: Update, context: CallbackContext) -> None:
    try:
        # Check if the command is a reply
        if update.message.reply_to_message:
            target_user_id = update.message.reply_to_message.from_user.id
        # Check if there are mentions
        elif update.message.entities and update.message.entities[0].type == "mention":
            target_user_id = int(update.message.text[update.message.entities[0].offset: update.message.entities[0].length].strip('@'))
        else:
            target_user_id = update.effective_user.id  # Default to the command sender

        user = await user_collection.find_one({"id": target_user_id})

        if user:
            coins = user.get("coins", 0)
            await update.message.reply_text(
                f"Bᴇʜᴏʟᴅ, Yᴏᴜʀ Cᴜʀʀᴇɴᴛ Bᴀʟᴀɴᴄᴇ Sʜɪɴᴇs ➻ 💸 {coins} Cᴏɪɴs."
            )
        else:
            await update.message.reply_text("Yᴏᴜ Dᴏɴ'ᴛ Hᴀᴠᴇ Aɴʏ Cᴏɪɴs Yᴇᴛ.")
    except Exception as e:
        # Log the error message here if you have a logging setup
        await update.message.reply_text("An error occurred while checking the balance. Please try again later.")


async def add_coins(user_id: int, amount: int) -> None:
    try:
        if amount <= 0:
            LOGGER.warning("Attempted to add non-positive amount of coins.")
            return
        
        user = await user_collection.find_one({"id": user_id})

        if user:
            current_coins = user.get("coins", 0)
            await user_collection.update_one(
                {"id": user_id},
                {"$set": {"coins": current_coins + amount}},
            )
        else:
            await user_collection.insert_one({"id": user_id, "coins": amount})
    except Exception as e:
        LOGGER.error(f"Error adding coins: {e}")


async def daily_reward(update: Update, context: CallbackContext) -> None:
    user_id = int(update.effective_user.id)
    try:
        user = await user_collection.find_one({"id": user_id})
        today = datetime.now()

        if user:
            last_claimed = user.get("last_daily_claimed")
            streak = user.get("daily_streak", 0)

            if last_claimed:
                last_claimed_date = last_claimed

                # Check if the user already claimed today
                if last_claimed_date.date() == today.date():
                    # Calculate the time remaining until the next claim
                    time_remaining = last_claimed_date + timedelta(days=1) - today
                    hours, remainder = divmod(time_remaining.total_seconds(), 3600)
                    minutes, seconds = divmod(remainder, 60)

                    await update.message.reply_text(
                        f"Yᴏᴜ Hᴀᴠᴇ Aʟʀᴇᴀᴅʏ Cʟᴀɪᴍᴇᴅ Yᴏᴜʀ Dᴀɪʟʏ Rᴇᴡᴀʀᴅ.\n"
                        f"Nᴇxᴛ Cʟᴀɪᴍ Aʀᴏᴜɴᴅ: {int(hours)}h {int(minutes)}m {int(seconds)}s"
                    )
                    return
                elif (today - last_claimed_date).days > 1:
                    streak = 1  # Reset streak if a day was skipped
                    await update.message.reply_text("Yᴏᴜʀ Dᴀɪʟʏ Sᴛʀᴇᴀᴋ Hᴀs Bᴇᴇɴ Rᴇsᴇᴛ.")
                else:
                    streak += 1

                # Cap the streak at 4
                streak = min(streak, 4)
            else:
                streak = 1  # First-time claim

            # Get the reward based on the streak
            coins_earned = daily_rewards[streak]
            await add_coins(user_id, coins_earned)

            # Update user's streak and last claimed time
            await user_collection.update_one(
                {"id": user_id},
                {"$set": {"daily_streak": streak, "last_daily_claimed": today}}
            )

            await update.message.reply_text(
                f"Yᴏᴜ Hᴀᴠᴇ Cʟᴀɪᴍᴇᴅ Yᴏᴜʀ Dᴀɪʟʏ ʀᴇᴡᴀʀᴅ. Yᴏᴜ Eᴀʀɴᴇᴅ {coins_earned} Cᴏɪɴs. (Leval {streak}🆙)"
            )
        else:
            # First-time claim
            await user_collection.insert_one({"id": user_id, "coins": 40, "daily_streak": 1, "last_daily_claimed": today})
            await update.message.reply_text("Yᴏᴜ Hᴀᴠᴇ Cʟᴀɪᴍᴇᴅ Yᴏᴜʀ Dᴀɪʟʏ ʀᴇᴡᴀʀᴅ. Yᴏᴜ Eᴀʀɴᴇᴅ 40 Cᴏɪɴs. (Leval 1)")
    except Exception as e:
        LOGGER.error(f"Error in daily_reward for user {user_id}: {e}")
        await update.message.reply_text("An error occurred while processing your daily reward. Please try again later.")


async def weekly_reward(update: Update, context: CallbackContext) -> None:
    try:
        user_id = int(update.effective_user.id)
        user = await user_collection.find_one({"id": user_id})

        current_time = datetime.utcnow()
        start_of_week = current_time.date() - timedelta(days=current_time.weekday())

        if user:
            last_claimed = user.get("last_weekly_claimed")
            if last_claimed and last_claimed.date() >= start_of_week:
                # Calculate the next claim time
                next_claim_time = last_claimed + timedelta(days=7)
                remaining_time = next_claim_time - current_time

                # Ensure remaining time is not negative
                if remaining_time.total_seconds() < 0:
                    remaining_time = timedelta(seconds=0)

                days = remaining_time.days
                hours, remainder = divmod(remaining_time.seconds, 3600)
                minutes, _ = divmod(remainder, 60)

                await update.message.reply_text(
                    f"Yᴏᴜ Hᴀᴠᴇ Aʟʀᴇᴀᴅʏ Cʟᴀɪᴍᴇᴅ Yᴏᴜʀ Wᴇᴇᴋʟʏ Rᴇᴡᴀʀᴅ.\n"
                    f"Nᴇxᴛ Cʟᴀɪᴍ Iɴ: {days} Dᴀʏs, {hours} Hᴏᴜʀs, {minutes} Mɪɴᴜᴛᴇs."
                )
                return

            # If the user can claim
            await add_coins(user_id, 250)
            await user_collection.update_one(
                {"id": user_id},
                {"$set": {"last_weekly_claimed": current_time}},
            )
            await update.message.reply_text("Yᴏᴜ Hᴀᴠᴇ Cʟᴀɪᴍᴇᴅ Yᴏᴜʀ Wᴇᴇᴋʟʏ Rᴇᴡᴀʀᴅ. Yᴏᴜ Eᴀʀɴᴇᴅ 𝟸𝟻𝟶 Cᴏɪɴs.")
        else:
            await user_collection.insert_one({"id": user_id, "coins": 500, "last_weekly_claimed": current_time})
            await update.message.reply_text("Yᴏᴜ Hᴀᴠᴇ Cʟᴀɪᴍᴇᴅ Yᴏᴜʀ Wᴇᴇᴋʟʏ Rᴇᴡᴀʀᴅ. Yᴏᴜ Eᴀʀɴᴇᴅ 500 Cᴏɪɴs.")
    except Exception as e:
        LOGGER.error(f"Error occurred: {e}")
        await update.message.reply_text("Aɴ ᴇʀʀᴏʀ ᴏᴄcᴜʀʀᴇᴅ, pʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ.")

async def pay_coins(update: Update, context: CallbackContext) -> None:
    try:
        # Parse the amount from the command arguments
        args = context.args
        if len(args) != 1:
            await update.message.reply_text("Invalid format. Use: /pay <amount>")
            return

        try:
            amount = int(args[0])
            if amount <= 0:
                await update.message.reply_text("Amount must be a positive number.")
                return
        except ValueError:
            await update.message.reply_text("Invalid amount. Please provide a valid number.")
            return

        # Check if the command is a reply to a message
        if not update.message.reply_to_message:
            await update.message.reply_text("Please reply to the message of the user you want to pay.")
            return

        # Extract the recipient's user ID from the replied message
        recipient_id = int(update.message.reply_to_message.from_user.id)

        # Get the sender's user ID
        sender_id = int(update.effective_user.id)

        # Check if sender is trying to pay themselves
        if sender_id == recipient_id:
            await update.message.reply_text("You cannot pay yourself.")
            return

        # Retrieve sender's wallet
        sender_wallet = await user_collection.find_one({"id": sender_id})
        if not sender_wallet:
            await update.message.reply_text("Sender's wallet not found.")
            return

        # Check sender's balance
        sender_balance = sender_wallet.get("coins", 0)
        if sender_balance < amount:
            await update.message.reply_text("Insufficient balance to make the payment.")
            return

        # Retrieve recipient's wallet
        recipient_wallet = await user_collection.find_one({"id": recipient_id})
        if not recipient_wallet:
            await update.message.reply_text("Recipient's wallet not found.")
            return

        # Update sender's balance
        new_sender_balance = sender_balance - amount
        await user_collection.update_one({"id": sender_id}, {"$set": {"coins": new_sender_balance}})

        # Update recipient's balance
        recipient_balance = recipient_wallet.get("coins", 0)
        new_recipient_balance = recipient_balance + amount
        await user_collection.update_one({"id": recipient_id}, {"$set": {"coins": new_recipient_balance}})

        await update.message.reply_text(f"Successfully transferred {amount} coins to user {recipient_id}.")

    except Exception as e:
        LOGGER.error(f"Error occurred: {e}")
        await update.message.reply_text("An error occurred while processing the payment. Please try again later.")




# owner coin play
OWNER_ID = 7078181502

async def give_coins(update: Update, context: CallbackContext) -> None:
    try:
        # Verify if the user is the owner
        if update.effective_user.id != OWNER_ID:
            await update.message.reply_text("You are not authorized to use this command.")
            return

        # Parse the amount and recipient ID
        args = context.args
        if len(args) != 2:
            await update.message.reply_text("Invalid format. Use: /givecoins <user_id> <amount>")
            return

        try:
            recipient_id = int(args[0])
            amount = int(args[1])
            if amount <= 0:
                await update.message.reply_text("Amount must be a positive number.")
                return
        except ValueError:
            await update.message.reply_text("Invalid input. Please provide a valid user ID and amount.")
            return

        # Retrieve recipient's wallet
        recipient_wallet = await user_collection.find_one({"id": recipient_id})
        if not recipient_wallet:
            await update.message.reply_text("Recipient's wallet not found. Make sure the user is registered.")
            return

        # Update recipient's balance
        recipient_balance = recipient_wallet.get("coins", 0)
        new_recipient_balance = recipient_balance + amount
        await user_collection.update_one({"id": recipient_id}, {"$set": {"coins": new_recipient_balance}})

        # Notify the user of successful operation
        await update.message.reply_text(f"Successfully added {amount} coins to user {recipient_id}.")

    except Exception as e:
        LOGGER.error(f"Error occurred while giving coins to user {update.effective_user.id}: {e}")
        await update.message.reply_text("An error occurred while processing the transaction. Please try again later.")


async def remove_coins(update: Update, context: CallbackContext) -> None:
    try:
        # Verify if the user is the owner
        if update.effective_user.id != OWNER_ID:
            await update.message.reply_text("You are not authorized to use this command.")
            return

        # Parse the amount and recipient ID
        args = context.args
        if len(args) != 2:
            await update.message.reply_text("Invalid format. Use: /removecoins <user_id> <amount>")
            return

        try:
            recipient_id = int(args[0])
            amount = int(args[1])
            if amount <= 0:
                await update.message.reply_text("Amount must be a positive number.")
                return
        except ValueError:
            await update.message.reply_text("Invalid input. Please provide a valid user ID and amount.")
            return

        # Retrieve recipient's wallet
        recipient_wallet = await user_collection.find_one({"id": recipient_id})
        if not recipient_wallet:
            await update.message.reply_text("Recipient's wallet not found. Make sure the user is registered.")
            return

        # Check recipient's balance
        recipient_balance = recipient_wallet.get("coins", 0)
        if recipient_balance < amount:
            await update.message.reply_text(f"User {recipient_id} has insufficient coins. Current balance: {recipient_balance}.")
            return

        # Update recipient's balance
        new_recipient_balance = recipient_balance - amount
        await user_collection.update_one({"id": recipient_id}, {"$set": {"coins": new_recipient_balance}})

        # Notify the user of successful operation
        await update.message.reply_text(f"Successfully removed {amount} coins from user {recipient_id}.")

    except Exception as e:
        LOGGER.error(f"Error occurred while removing coins from user {update.effective_user.id}: {e}")
        await update.message.reply_text("An error occurred while processing the transaction. Please try again later.")


# Add command handlers for give and remove coins
application.add_handler(CommandHandler("givecoins", give_coins))
application.add_handler(CommandHandler("removecoins", remove_coins))

# bouns play

SPECIAL_GROUP_ID = -1002289810575
# Define the bot's join link
BOT_JOIN_LINK = "https://t.me/PiratesMainchat"

async def bonus_command(update: Update, context: CallbackContext) -> None:
    try:
        chat_id = update.effective_chat.id
        user_id = int(update.effective_user.id)
        user = await user_collection.find_one({"id": user_id})
        
        if chat_id == SPECIAL_GROUP_ID:
            if user:
                now = datetime.now()
                last_claimed = user.get("last_bonus_claimed")

                # Check if the user has claimed today
                if last_claimed and last_claimed.date() == now.date():
                    await update.message.reply_text("Yᴏᴜ Hᴀᴠᴇ Aʟʀᴇᴀᴅʏ Cʟᴀɪᴍᴇᴅ Yᴏᴜʀ Bᴏɴᴜs Tᴏᴅᴀʏ.")
                    return

                # Add bonus and update claim date
                await add_coins(user_id, 500)
                await user_collection.update_one(
                    {"id": user_id},
                    {"$set": {"last_bonus_claimed": now}},
                )
                
                # Create an inline button with a simple "Join" label
                keyboard = [[InlineKeyboardButton("Join", url=BOT_JOIN_LINK)]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await update.message.reply_text(
                    "🎊Cᴏɴɢʀᴀᴛᴜʟᴀᴛɪᴏɴs🎉    Yᴏᴜ Cʟᴀɪᴍᴇᴅ Yᴏᴜʀ Dᴀɪʟʏ Bᴏɴᴜs ᴏғ 500 Cᴏɪɴs! Eɴᴊᴏʏ",
                    reply_markup=reply_markup
                )
            else:
                await user_collection.insert_one({"id": user_id, "coins": 500, "last_bonus_claimed": datetime.now()})
                
                # Create an inline button with a simple "Join" label
                keyboard = [[InlineKeyboardButton("Join", url=BOT_JOIN_LINK)]]
                reply_markup = InlineKeyboardMarkup(keyboard)

                await update.message.reply_text(
                    "🎊Cᴏɴɢʀᴀᴛᴜʟᴀᴛɪᴏɴs🎉    Yᴏᴜ Cʟᴀɪᴍᴇᴅ Yᴏᴜʀ Dᴀɪʟʏ Bᴏɴᴜs ᴏғ 500 Cᴏɪɴs! Eɴᴊᴏʏ",
                    reply_markup=reply_markup
                )
        else:
            # Inform the user to claim their bonus in the special group
            keyboard = [[InlineKeyboardButton("Join", url=BOT_JOIN_LINK)]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(
                f"THIS COMMMAND IS ONLY WORK IN @PiratesMainchat .🎁TO CLAIM YOUR DAILY BONUS",
                reply_markup=reply_markup
            )

    except Exception as e:
        LOGGER.error(f"Error occurred: {e}")
        await update.message.reply_text(f"Error occurred: {e}")



          # coin top


# Use a cache to store top users temporarily
top_users_cache = None
cache_timestamp = None

async def fetch_top_users():
    global top_users_cache, cache_timestamp
    current_time = asyncio.get_event_loop().time()

    # Refresh the cache every 60 seconds
    if top_users_cache is None or (current_time - cache_timestamp > 60):
        top_users_cache = await user_collection.find({}, {"id": 1, "coins": 1, "username": 1, "first_name": 1}).sort("coins", -1).limit(10).to_list(length=10)
        cache_timestamp = current_time

    return top_users_cache

async def top_users(update: Update, context: CallbackContext) -> None:
    try:
        top_users = await fetch_top_users()
        
        if not top_users:
            await update.message.reply_text("No users found.")
            return
        
        caption = "🏆 Tᴏᴘ 10 Uꜱᴇʀs ʙʏ Cᴏɪɴs:\n\n"
        
        for rank, user in enumerate(top_users, start=1):
            user_id = user.get("id")
            coins = user.get("coins", 0)
            username = user.get("username", "NoUsername")
            first_name = user.get("first_name", "No Name")
            profile_link = f"https://t.me/{username}" if username else "#"
            caption += f"{rank}. <a href='{profile_link}'><b>{first_name}</b></a>: 💸 {coins} Coins\n\n"
        
        image_url = 'https://files.catbox.moe/3liel3.jpg'  # Replace with your image URL
        await update.message.reply_photo(photo=image_url, caption=caption, parse_mode='HTML')
        
    except Exception as e:
        LOGGER.error(f"Error occurred while fetching top users: {e}")
        await update.message.reply_text("An error occurred while fetching the top users. Please try again later.")



      ############################





async def buy_character(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    
    # Check if the user is the one who initiated the shop command
    if user_id != context.user_data.get("shop_user_id"):
        await query.answer("You are not authorized to perform this action.")
        return

    try:
        # Extract character index from callback query
        character_index = int(query.data.split("_")[1])

        # Retrieve character data from the database
        characters_cursor = shops_collection.find()
        characters = await characters_cursor.to_list(length=None)

        if character_index >= len(characters):
            await query.answer("Character not found.")
            return

        character = characters[character_index]

        # Retrieve user data including wallet balance
        user = await user_collection.find_one({"id": user_id})
        if not user:
            await query.answer("User not found.")
            return

        # Check affordability
        price = character["price"]
        current_balance = user.get("coins", 0)
        if current_balance < price:
            await query.answer(f"Insufficient funds. You need {price - current_balance} more coins to buy this character.", show_alert=True)
            return

        # Deduct coins from user's wallet
        new_coins = current_balance - price

        # Add character to user's collection
        character_id = str(character["_id"])
        character_data = {
            "_id": ObjectId(),  # Generate a new ObjectId for the character entry
            "img_url": character["img_url"],
            "name": character["name"],
            "anime": character["anime"],
            "rarity": character["rarity"],
            "id": character["id"],
            "message_id": character.get("message_id")  # Optional, if message_id is available
        }

        if "characters" not in user:
            user["characters"] = []

        user["characters"].append(character_data)

        # Update user data in the database
        await user_collection.update_one(
            {"id": user_id},
            {"$set": {"coins": new_coins, "characters": user["characters"]}}
        )

        # Confirmation message
        await query.answer("Character purchased successfully.")

    except Exception as e:
        LOGGER.error(f"Error buying character: {e}")
        await query.answer("An error occurred while processing the purchase. Please try again later.", show_alert=True)



async def next_item(update: Update, context: CallbackContext) -> None:
    try:
        # Check if the user is the one who initiated the shop command
        if update.callback_query.from_user.id != context.user_data.get("shop_user_id"):
            await update.callback_query.answer("You are not authorized to perform this action.")
            return
        
        # Retrieve characters/items from the database
        characters_cursor = shops_collection.find()
        characters = await characters_cursor.to_list(length=None)

        if not characters:
            await update.callback_query.answer("No characters found in the shop.")
            return

        # Get the current character index from context.user_data
        current_index = context.user_data.get("current_index", 0)

        # Calculate the index of the next character
        next_index = (current_index + 1) % len(characters)

        # Display the next character
        character = characters[next_index]
        caption_message = f"🛍 Welcome to the Luxury Shop! 🛍\n\n" \
                         f"🔹 Character: {character['name']}\n" \
                         f"🔺 Anime: {character['anime']}\n" \
                         f"💡 Rarity: {character['rarity']}\n" \
                         f"💸 Price: {character['price']} coin\n" \
                         f"🔢 ID: {character['id']}\n" \
                         f"Unleash Your Inner Otaku and Buy Now! 🎊"
        keyboard = [
            [InlineKeyboardButton("Buy", callback_data=f"buy_{str(next_index)}")],
            [InlineKeyboardButton("Next", callback_data="next")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Update the user's data to store the current index
        context.user_data["current_index"] = next_index

        await update.callback_query.message.edit_media(
            media=InputMediaPhoto(media=character['img_url'], caption=caption_message),
            reply_markup=reply_markup
        )

        await update.callback_query.answer()  # Acknowledge the callback

        LOGGER.info("Next item displayed in the shop.")

    except Exception as e:
        LOGGER.error(f"Error occurred: {e}")
        await update.callback_query.answer("An error occurred while displaying the next item. Please try again later.")
    
async def show_top_users(update: Update, context: CallbackContext) -> None:
    try:
        # Retrieve the top 10 users sorted by coins in descending order
        top_users = await user_collection.find().sort("coins", DESCENDING).limit(10).to_list(length=10)

        if not top_users:
            await update.message.reply_text("No users found.")
            return

        # Create a message to display the top 10 users
        message = "🌟 Dɪsᴄᴏᴠᴇʀ Tʜᴇ Eʟɪᴛᴇ Tᴏᴘ 𝟷𝟶 Usᴇʀs Rᴇᴡᴀʀᴅᴇᴅ Wɪᴛʜ Tʜᴇ Mᴏsᴛ Cᴏɪɴs:-\n\n"
        
        for i, user in enumerate(top_users, 1):
            username = user.get("username", "Unknown User")  # Get username or default to "Unknown User"
            coins = user.get("coins", 0)
            message += f"{i}. ◾ {username},\nBᴀʟᴀɴᴄᴇ➻💵{coins} coins.\n\n"

        # Debugging: Log the user data to check field values
        LOGGER.info(f"Top users data: {top_users}")

        await update.message.reply_text(message)
    
    except Exception as e:
        LOGGER.error(f"Error occurred: {e}")
        await update.message.reply_text("An error occurred while retrieving the top users. Please try again later.")


application.add_handler(CommandHandler("bonus", bonus_command))
application.add_handler(CommandHandler('cointop', top_users))
application.add_handler(CallbackQueryHandler(next_item, pattern="^next$"))
application.add_handler(CallbackQueryHandler(buy_character, pattern=r'^buy_\d+$'))
application.add_handler(CommandHandler('paycoin', pay_coins))

CHECK_BALANCE_HANDLER = CommandHandler(['balance','bal'],check_balance)
DAILY_REWARD_HANDLER = CommandHandler('daily', daily_reward)
WEEKLY_REWARD_HANDLER = CommandHandler('weekly', weekly_reward)

application.add_handler(CHECK_BALANCE_HANDLER)
application.add_handler(DAILY_REWARD_HANDLER)
application.add_handler(WEEKLY_REWARD_HANDLER)