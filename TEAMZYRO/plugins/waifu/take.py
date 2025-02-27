from TEAMZYRO import *
from TEAMZYRO import app
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram import enums

# Initialize the Pyrogram client
OWNER_ID = [7638720582, 7638720582]

# Admin check function
def is_admin(user_id: int) -> bool:
    """Check if the user is an admin."""
    return user_id in OWNER_ID

# /givec command
@app.on_message(filters.command("givec"))
async def give_command(client: Client, message: Message):
    # Check if the user is an admin
    if not is_admin(message.from_user.id):
        await message.reply_text("❌ You are not authorized to use this command.")
        return

    # Check if the command has at least one argument (character_id)
    if len(message.command) < 2:
        await message.reply_text("❌ Usage: /givec {character_id} {reason (optional)}")
        return

    character_id = message.command[1]
    reason = " ".join(message.command[2:]) if len(message.command) > 2 else "No reason provided."

    # Fetch the character from the database
    character = await collection.find_one({'id': character_id})
    if not character:
        await message.reply_text(f"❌ Character with ID {character_id} not found.")
        return

    # Check if the user is mentioned in the command
    if not message.reply_to_message:
        await message.reply_text("❌ Please reply to a user's message to give them the character.")
        return

    user_id = message.reply_to_message.from_user.id
    user_name = message.reply_to_message.from_user.first_name

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
            'username': message.reply_to_message.from_user.username,
            'first_name': user_name,
            'characters': [character],
        })

    # Check if the character has a video URL
    media_message = "🎥 This character has a video! Check it out below." if 'vid_url' in character else "🖼️ This character has an image."

    # Send confirmation to the owner
    await message.reply_text(
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
        await client.send_video(
            chat_id=user_id,
            video=character['vid_url'],
            caption=user_message,
            parse_mode=enums.ParseMode.HTML
        )
    else:
        await client.send_photo(
            chat_id=user_id,
            photo=character['img_url'],
            caption=user_message,
            parse_mode=enums.ParseMode.HTML
        )

# /giveb command
@app.on_message(filters.command("giveb"))
async def giveb_command(client: Client, message: Message):
    # Check if the user is an admin
    if not is_admin(message.from_user.id):
        await message.reply_text("❌ You are not authorized to use this command.")
        return

    # Ensure the command is a reply to a user's message
    if not message.reply_to_message:
        await message.reply_text("Please reply to a user to use /giveb.")
        return

    recipient = message.reply_to_message.from_user
    recipient_id = recipient.id
    recipient_first_name = recipient.first_name
    recipient_username = recipient.username

    # Extract arguments
    try:
        amount = int(message.command[1])
    except (IndexError, ValueError):
        await message.reply_text("Usage: /giveb <amount> [optional reason]")
        return

    reason = " ".join(message.command[2:]) if len(message.command) > 2 else "No reason provided."

    if amount <= 0:
        await message.reply_text("Amount must be a positive number!")
        return

    # Fetch recipient's balance
    recipient_data = await user_collection.find_one({'id': recipient_id})
    recipient_balance = int(recipient_data.get('coins', 0)) if recipient_data else 0

    # Update recipient balance
    await user_collection.update_one({'id': recipient_id}, {'$set': {'coins': recipient_balance + amount}})

    # DM the recipient with reward details
    reward_message = f"{reason}\n\nYour Reward: ₿{amount}"
    try:
        await client.send_message(chat_id=recipient_id, text=reward_message)
    except Exception as e:
        await message.reply_text(f"Could not send DM: {e}")

    # Notify sender
    recipient_link = f"https://t.me/{recipient_username}" if recipient_username else f"https://t.me/user{recipient_id}"
    success_message = f"Success! You gave ₿{amount} Berries to [{recipient_first_name}]({recipient_link})!"
    await message.reply_text(success_message, parse_mode=enums.ParseMode.HTML)

# /takec command
@app.on_message(filters.command("takec"))
async def takec_command(client: Client, message: Message):
    # Check if the user is an admin
    if not is_admin(message.from_user.id):
        await message.reply_text("❌ You are not authorized to use this command.")
        return

    # Rest of the /takec command logic
    if len(message.command) < 2:
        await message.reply_text("❌ Usage: /takec {character_id} {reason (optional)}")
        return

    character_id = message.command[1]
    reason = " ".join(message.command[2:]) if len(message.command) > 2 else "No reason provided."

    if not message.reply_to_message:
        await message.reply_text("❌ Please reply to a user's message to take the character from them.")
        return

    user_id = message.reply_to_message.from_user.id
    user_name = message.reply_to_message.from_user.first_name

    user = await user_collection.find_one({'id': user_id})
    if not user:
        await message.reply_text(f"❌ User {user_name} has no characters.")
        return

    character = None
    for char in user.get('characters', []):
        if char.get('id') == character_id:
            character = char
            break

    if not character:
        await message.reply_text(f"❌ Character with ID {character_id} not found in {user_name}'s collection.")
        return

    await user_collection.update_one(
        {'id': user_id},
        {'$pull': {'characters': {'id': character_id}}}
    )

    await message.reply_text(
        f"✅ Character {character['name']} (ID: {character['id']}) has been taken from {user_name}.\n"
        f"📜 Reason: {reason}"
    )

    await client.send_message(
        chat_id=user_id,
        text=f"Character {character['name']} (ID: {character['id']}) has been taken from you.\nReason: {reason}"
    )

# /takeb command
@app.on_message(filters.command("takeb"))
async def takeb_command(client: Client, message: Message):
    # Check if the user is an admin
    if not is_admin(message.from_user.id):
        await message.reply_text("❌ You are not authorized to use this command.")
        return

    # Rest of the /takeb command logic
    if not message.reply_to_message:
        await message.reply_text("Please reply to a user to use /takeb.")
        return

    recipient = message.reply_to_message.from_user
    recipient_id = recipient.id
    recipient_first_name = recipient.first_name
    recipient_username = recipient.username

    try:
        amount = int(message.command[1])
    except (IndexError, ValueError):
        await message.reply_text("Usage: /takeb <amount> [optional reason]")
        return

    reason = " ".join(message.command[2:]) if len(message.command) > 2 else "No reason provided."

    if amount <= 0:
        await message.reply_text("Amount must be a positive number!")
        return

    recipient_data = await user_collection.find_one({'id': recipient_id})
    if not recipient_data:
        await message.reply_text(f"❌ User {recipient_first_name} has no balance.")
        return

    recipient_balance = int(recipient_data.get('coins', 0))

    if recipient_balance < amount:
        await message.reply_text(f"❌ User {recipient_first_name} only has ₿{recipient_balance} berries.")
        return

    await user_collection.update_one({'id': recipient_id}, {'$set': {'coins': recipient_balance - amount}})

    recipient_link = f"https://t.me/{recipient_username}" if recipient_username else f"https://t.me/user{recipient_id}"
    success_message = f"Success! You took ₿{amount} Berries from [{recipient_first_name}]({recipient_link})!"
    await message.reply_text(success_message, parse_mode=enums.ParseMode.HTML)

    await client.send_message(
        chat_id=recipient_id,
        text=f"₿{amount} Berries have been taken from you.\nReason: {reason}"
    )
