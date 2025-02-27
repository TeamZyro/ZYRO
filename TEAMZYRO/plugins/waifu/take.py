from TEAMZYRO import app
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

def is_admin(user_id: int) -> bool:
    """Check if the user is an admin."""
    return user_id in OWNER_ID

async def give_command(update: Update, context: CallbackContext) -> None:

    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ You are not authorized to use this command.")
        return

    # Check if the command has at least one argument (character_id)
    if len(context.args) < 1:
        await update.message.reply_text("❌ Usage: /givec {character_id} {reason (optional)}")
        return

    character_id = context.args[0]
    reason = " ".join(context.args[1:]) if len(context.args) > 1 else "No reason provided."

    # Fetch the character from the database
    character = await collection.find_one({'id': character_id})
    if not character:
        await update.message.reply_text(f"❌ Character with ID {character_id} not found.")
        return

    # Check if the user is mentioned in the command
    if not update.message.reply_to_message:
        await update.message.reply_text("❌ Please reply to a user's message to give them the character.")
        return

    user_id = update.message.reply_to_message.from_user.id
    user_name = update.message.reply_to_message.from_user.first_name

    # Add the character to the user's collection
    user = await user_collection.find_one({'id': user_id})
    if user:
        await user_collection.update_one(
            {'id': user_id},
            {'$push': {'characters': character}}
        )
    else:
        await user_collection.insert_one({
            'id': user_id,
            'username': update.message.reply_to_message.from_user.username,
            'first_name': user_name,
            'characters': [character],
        })

    # Check if the character has a video URL
    media_message = "🎥 This character has a video! Check it out below." if 'vid_url' in character else "🖼️ This character has an image."

    # Send confirmation to the owner
    await update.message.reply_text(
        f"✅ Character {character['name']} (ID: {character['id']}) has been given to {user_name}.\n"
        f"📜 Reason: {reason}\n{media_message}"
    )

    # Send confirmation to the user
    user_message = (
        f"{reason}\n\n"
        f"Name : <b>{character['name']}</b>\n"
        f"Rarity : <b>{character['rarity']}</b>\n"
        f"ID : <b>{character['id']}</b>\n"
    )

    if 'vid_url' in character:
        await context.bot.send_video(
            chat_id=user_id,
            video=character['vid_url'],
            caption=user_message,
            parse_mode='HTML'
        )
    else:
        await context.bot.send_photo(
            chat_id=user_id,
            photo=character['img_url'],
            caption=user_message,
            parse_mode='HTML'
        )

async def giveb(update: Update, context: CallbackContext) -> None:
    sender_id = update.effective_user.id

    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ You are not authorized to use this command.")
        return

    # Ensure the command is a reply to a user's message
    if not update.message.reply_to_message:
        await update.message.reply_text("Please reply to a user to use /giveb.")
        return

    recipient = update.message.reply_to_message.from_user
    recipient_id = recipient.id
    recipient_first_name = recipient.first_name
    recipient_username = recipient.username

    # Extract arguments
    try:
        amount = int(context.args[0])
    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /giveb <amount> [optional reason]")
        return

    reason = " ".join(context.args[1:]) if len(context.args) > 1 else "No reason provided."

    if amount <= 0:
        await update.message.reply_text("Amount must be a positive number!")
        return

    # Fetch recipient's balance
    recipient_data = await user_collection.find_one({'id': recipient_id})
    recipient_balance = int(recipient_data.get('balance', 0)) if recipient_data else 0

    # Update recipient balance (balance system se directly add hoga)
    await user_collection.update_one({'id': recipient_id}, {'$set': {'balance': recipient_balance + amount}})

    # DM the recipient with reward details
    reward_message = f"{reason}\n\nYour Reward: ₿{amount}"
    try:
        await context.bot.send_message(chat_id=recipient_id, text=reward_message)
    except Exception as e:
        await update.message.reply_text(f"Could not send DM: {e}")

    # Notify sender
    recipient_link = f"https://t.me/{recipient_username}" if recipient_username else f"https://t.me/user{recipient_id}"
    success_message = f"Success! You gave ₿{amount} Berries to [{recipient_first_name}]({recipient_link})!"
    
    await update.message.reply_text(success_message, parse_mode="Markdown")


application.add_handler(CommandHandler("giveb", giveb, block=False))
application.add_handler(CommandHandler("givec", give_command, block=False))
