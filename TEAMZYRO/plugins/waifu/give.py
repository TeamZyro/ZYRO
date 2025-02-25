from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from TEAMZYRO import *

@require_power("approve_request")
async def give_command(update: Update, context: CallbackContext) -> None:

    # Check if the command has the correct format
    if len(context.args) != 1:
        await update.message.reply_text("❌ Usage: /give {character_id}")
        return

    character_id = context.args[0]

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
        # If the user already exists, update their collection
        await user_collection.update_one(
            {'id': user_id},
            {'$push': {'characters': character}}
        )
    else:
        # If the user doesn't exist, create a new entry
        await user_collection.insert_one({
            'id': user_id,
            'username': update.message.reply_to_message.from_user.username,
            'first_name': user_name,
            'characters': [character],
        })

    # Check if the character has a video URL
    if 'vid_url' in character:
        video_message = "🎥 This character has a video! Check it out below."
    else:
        video_message = "🖼️ This character has an image."

    # Send confirmation to the owner
    await update.message.reply_text(
        f"✅ Character {character['name']} (ID: {character['id']}) has been given to {user_name}.\n"
        f"{video_message}"
    )

    # Send confirmation to the user
    user_message = (
        f"🎉 You have received a new character!\n\n"
        f"📛 𝗡𝗔𝗠𝗘: <b>{character['name']}</b>\n"
        f"🌈 𝗔𝗡𝗜𝗠𝗘: <b>{character['anime']}</b>\n"
        f"✨ 𝗥𝗔𝗥𝗜𝗧𝗬: <b>{character['rarity']}</b>\n"
        f"🆔 𝗜𝗗: <b>{character['id']}</b>\n\n"
        f"{video_message}"
    )

    if 'vid_url' in character:
        # Send the video to the user
        await context.bot.send_video(
            chat_id=user_id,
            video=character['vid_url'],
            caption=user_message,
            parse_mode='HTML'
        )
    else:
        # Send the image to the user
        await context.bot.send_photo(
            chat_id=user_id,
            photo=character['img_url'],
            caption=user_message,
            parse_mode='HTML'
        )

# Add the command handler to your bot's application
application.add_handler(CommandHandler("give", give_command, block=False))
