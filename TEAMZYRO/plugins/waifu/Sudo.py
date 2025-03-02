from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pymongo import MongoClient

from config import OWNER_ID

from TEAMZYRO import app, db
from functools import wraps

sudo_users = db['sudo_users']

# Predefined powers
ALL_POWERS = [
    "add_character",  # Adds a new character
    "delete_character",  # Deletes a character
    "update_character",  # Updates an existing character
    "approve_request",  # Approves a request
    "approve_inventory_request",  # Approves an inventory request
    "VIP"
]

# Command: /addsudo
@app.on_message(filters.command("saddsudo") & filters.reply)
async def add_sudo(client, message):
    if message.from_user.id != OWNER_ID:
        await message.reply_text("You do not have permission to use this command.")
        return

    replied_user_id = message.reply_to_message.from_user.id

    # Check if the user is already a sudo
    existing_user = await sudo_users.find_one({"_id": replied_user_id})
    if existing_user:
        await message.reply_text(f"User `{replied_user_id}` is already a sudo.")
        return

    # Add the user as a sudo
    sudo_users.update_one(
        {"_id": replied_user_id},
        {"$set": {"powers": {"add_character": True}}},  # Only giving the 'add_character' power
        upsert=True
    )
    await message.reply_text(f"User `{replied_user_id}` has been added as a sudo with 'add_character' power.")

@app.on_message(filters.command("srmsudo") & filters.reply)
async def remove_sudo(client, message):
    if message.from_user.id != OWNER_ID:
        await message.reply_text("You do not have permission to use this command.")
        return

    replied_user_id = message.reply_to_message.from_user.id

    # Check if the user is a sudo
    existing_user = await sudo_users.find_one({"_id": replied_user_id})
    if not existing_user:
        await message.reply_text(f"User `{replied_user_id}` is not a sudo.")
        return

    # Remove the user from sudo
    sudo_users.delete_one({"_id": replied_user_id})
    await message.reply_text(f"User `{replied_user_id}` has been removed from sudo.")

# Command: /editsudo
@app.on_message(filters.command("editsudo") & filters.reply)
async def edit_sudo(client, message):
    if message.from_user.id != OWNER_ID:
        await message.reply_text("You do not have permission to use this command.")
        return

    replied_user_id = message.reply_to_message.from_user.id
    user_data = await sudo_users.find_one({"_id": replied_user_id})

    if not user_data:
        await message.reply_text("This user is not a sudo.")
        return

    # Generate inline keyboard with "Closed" button
    buttons = []
    powers = user_data.get("powers", {})
    for i, power in enumerate(ALL_POWERS):
        current_status = "Yes" if powers.get(power, False) else "No"
        buttons.append([
            InlineKeyboardButton(f"{power}", callback_data=f"noop"),
            InlineKeyboardButton(f"{current_status}", callback_data=f"toggle_{replied_user_id}_{power}")
        ])
    
    # Add the "Closed" button to close the keyboard
    buttons.append([InlineKeyboardButton("Closed", callback_data="close_keyboard")])

    keyboard = InlineKeyboardMarkup(buttons)

    await message.reply_text(f"Edit powers for `{replied_user_id}`:", reply_markup=keyboard)

# Callback handler for toggling powers
@app.on_callback_query(filters.regex(r"^toggle_(\d+)_(\w+)$"))
async def toggle_power(client, callback_query):
    if callback_query.from_user.id != OWNER_ID:
        await callback_query.answer("You do not have permission to edit powers.", show_alert=True)
        return

    user_id = int(callback_query.matches[0].group(1))
    power = callback_query.matches[0].group(2)

    user_data = await sudo_users.find_one({"_id": user_id})
    if not user_data:
        await callback_query.answer("User not found.", show_alert=True)
        return

    # Toggle the power
    current_status = user_data.get("powers", {}).get(power, False)
    new_status = not current_status
    await sudo_users.update_one(
        {"_id": user_id},
        {"$set": {f"powers.{power}": new_status}}
    )

    # Notify the user and update the keyboard
    await callback_query.answer(f"Power '{power}' updated to {'Yes' if new_status else 'No'}.", show_alert=True)

    user_data = await sudo_users.find_one({"_id": user_id})  # Fetch updated user data
    powers = user_data.get("powers", {})
    buttons = []
    for p in ALL_POWERS:
        status = "Yes" if powers.get(p, False) else "No"
        buttons.append([
            InlineKeyboardButton(f"{p}", callback_data=f"noop"),
            InlineKeyboardButton(f"{status}", callback_data=f"toggle_{user_id}_{p}")
        ])
    
    # Add the "Closed" button again after toggling
    buttons.append([InlineKeyboardButton("Closed", callback_data="close_keyboard")])

    keyboard = InlineKeyboardMarkup(buttons)
    await callback_query.message.edit_reply_markup(reply_markup=keyboard)

# Callback handler for closing the keyboard
@app.on_callback_query(filters.regex(r"^close_keyboard$"))
async def close_keyboard(client, callback_query):
    await callback_query.message.edit_reply_markup(reply_markup=None)
    await callback_query.answer("Keyboard closed.", show_alert=True)

# Command: Power check mechanism
@app.on_message(filters.command("checkpower") & filters.reply)
async def check_power(client, message):
    if user_id != OWNER_ID:
        await message.reply_text("You do not have permission to use this command.")
        return

    replied_user_id = message.reply_to_message.from_user.id
    user_data = sudo_users.find_one({"_id": replied_user_id})
    if not user_data:
        await message.reply_text(f"User `{replied_user_id}` has no powers.")
        return

    powers = user_data.get("powers", {})
    powers_list = "\n".join([f"{p}: {'Yes' if v else 'No'}" for p, v in powers.items()])
    await message.reply_text(f"User `{replied_user_id}` powers:\n{powers_list}")



def require_power(required_power):
    def decorator(func):
        @wraps(func)
        async def wrapper(client, message, *args, **kwargs):
            # Check if the message is a callback query or a regular message
            if isinstance(message, CallbackQuery):
                # This is a callback query, not a regular message
                user_id = message.from_user.id
                # If the user is the owner, bypass the power check
                if user_id == OWNER_ID:
                    return await func(client, message, *args, **kwargs)

                # Otherwise, check if the user has the required power
                user_data = await sudo_users.find_one({"_id": user_id})
                if not user_data or not user_data.get("powers", {}).get(required_power, False):
                    # Use callback_query.answer for callback queries
                    await message.answer(f"You do not have the `{required_power}` power required to use this button.", show_alert=True)
                    return
                return await func(client, message, *args, **kwargs)

            # Regular message handling
            user_id = message.from_user.id
            # If the user is the owner, bypass the power check
            if user_id == OWNER_ID:
                return await func(client, message, *args, **kwargs)

            # Otherwise, check if the user has the required power
            user_data = await sudo_users.find_one({"_id": user_id})
            if not user_data or not user_data.get("powers", {}).get(required_power, False):
                # Use message.reply_text for regular messages
                await message.reply_text(f"You do not have the `{required_power}` power required to use this command.")
                return
            return await func(client, message, *args, **kwargs)
        return wrapper
    return decorator


# Command: /sudolist
@app.on_message(filters.command("csudolist"))
async def sudo_list(client, message):
    if message.from_user.id != OWNER_ID:
        await message.reply_text("You do not have permission to use this command.")
        return

    # Fetch all sudo users from the database and convert the cursor to a list
    users = await sudo_users.find().to_list(length=None)

    # Check if there are any sudo users
    if not users:
        await message.reply_text("There are no sudo users.")
        return

    # Prepare a list of users and their powers
    sudo_list_text = "Sudo Users List:\n\n"
    for user in users:
        user_id = user.get("_id")
        powers = user.get("powers", {})
        # Map full power names to abbreviations
        power_abbreviations = {
            "add_character": "AC",
            "delete_character": "DC",
            "update_character": "UC",
            "approve_request": "AR",
            "approve_inventory_request": "AIR",
            "VIP": "VIP",
            # Add other powers here
        }
        powers_list = ", ".join([f"{power_abbreviations.get(power, power)}: {'✅' if powers.get(power, False) else '❎'}"
                                 for power in ALL_POWERS])
        # Mention user instead of showing their ID
        sudo_list_text += f"User: [{user_id}](tg://user?id={user_id})\nPowers: {powers_list}\n\n"

    # Send the list of sudo users
    await message.reply_text(sudo_list_text, disable_web_page_preview=True)
