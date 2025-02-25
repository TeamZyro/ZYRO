from TEAMZYRO import *
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, filters, ContextTypes
import asyncio
import time

async def message_counter(update: Update, context: CallbackContext) -> None:
    chat_id = str(update.effective_chat.id)
    user_id = update.effective_user.id
    current_time = time.time()

    existing_group = await group_user_totals_collection.find_one({"group_id": chat_id})
    if not existing_group:
        await group_user_totals_collection.update_one(
            {"group_id": chat_id}, 
            {"$set": {"group_id": chat_id}}, 
            upsert=True
        )


    if chat_id not in locks:
        locks[chat_id] = asyncio.Lock()
    lock = locks[chat_id]

    async with lock:
        # Check if user is in cooldown
        if user_id in user_cooldowns:
            cooldown_end = user_cooldowns[user_id]
            if current_time < cooldown_end:
                remaining_time = int(cooldown_end - current_time)              
                return
            else:
                del user_cooldowns[user_id]

        if chat_id in last_user and last_user[chat_id]['user_id'] == user_id:
            last_user[chat_id]['count'] += 1
            if last_user[chat_id]['count'] >= 10:
                if user_id not in warned_users or current_time - warned_users[user_id] >= 600:
                    cooldown_end = current_time + 600  # 10 minutes from now
                    user_cooldowns[user_id] = cooldown_end
                    warned_users[user_id] = current_time
                    await update.message.reply_text(
                        f"⚠️ Don't Spam {update.effective_user.first_name}...\n"
                        "Your Messages Will be ignored for 10 Minutes..."
                    )
                return
        else:
            last_user[chat_id] = {'user_id': user_id, 'count': 1}

        if chat_id in message_counts:
            message_counts[chat_id] += 1
        else:
            message_counts[chat_id] = 1

        # Fixed threshold for triggering at 80 messages
        if message_counts[chat_id] % 100 == 0:
            await send_image(update, context)
            message_counts[chat_id] = 0

        # Now handle the guess in the message
        await guessz(update, context)

application.add_handler(MessageHandler(filters.ALL, message_counter, block=False))