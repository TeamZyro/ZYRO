from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message
from TEAMZYRO import app, user_collection

@app.on_message(filters.command("bet"))
async def roll(client, message: Message):
    user_id = message.from_user.id
    args = message.command[1:]  # Extract arguments from command

    if len(args) < 2:
        await message.reply_text(
            "Invalid usage! Use: `/roll <amount> <E/O>`",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    try:
        amount = int(args[0])
        choice = args[1].upper()  # Expecting "E" or "O"
    except ValueError:
        await message.reply_text(
            "Invalid amount! Please enter a number.",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    if choice not in ["E", "O"]:
        await message.reply_text(
            "Invalid choice! Use 'E' for Even or 'O' for Odd.",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    if amount <= 0:
        await message.reply_text(
            "Amount must be a positive number.",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    # Fetch user data from MongoDB
    user_data = await user_collection.find_one({'id': user_id})
    if not user_data:
        await message.reply_text(
            "User data not found in database.",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    # Ensure balance is a number
    try:
        balance_amount = float(user_data.get('coins', 0))  # Convert to float
    except ValueError:
        await message.reply_text(
            "Invalid balance data in database. Please contact support.",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    # Ensure balance is stored as a number
    await user_collection.update_one({'id': user_id}, {'$set': {'coins': balance_amount}})

    # Ensure the user is betting at least 7% of their balance
    min_bet = max(1, int(balance_amount * 0.07))  # Ensure min bet is at least 1
    if amount < min_bet:
        await message.reply_text(
            f"You must bet at least `{min_bet}` Berries (7% of your balance).",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    if balance_amount < amount:
        await message.reply_text(
            "Insufficient balance to place the bet.",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    # Send a dice emoji and get the dice value
    dice_message = await client.send_dice(message.chat.id, emoji="🎲")  # Send a dice emoji
    dice_value = dice_message.dice.value  # Extract the dice value (1-6)

    # Determine if the dice result is EVEN or ODD
    dice_result = "E" if dice_value % 2 == 0 else "O"

    # Initialize XP change
    xp_change = 0

    if choice == dice_result:
 
        win_amount = amount * 2
        await user_collection.update_one(
            {'id': user_id},
            {'$inc': {'coins': win_amount}}  # Ensured balance is numeric
        )
        await message.reply_text(
            f"🎲 Dice roll: `{dice_value}`\n✅ You won! `+{win_amount}` Berries!",
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        # User loses
        xp_change = -2
        await user_collection.update_one(
            {'id': user_id},
            {'$inc': {'coins': -amount}}  # Ensured balance is numeric
        )
        await message.reply_text(
            f"🎲 Dice roll: `{dice_value}`\n❌ You lost! `-{amount}` Berries!",
            parse_mode=ParseMode.MARKDOWN
        )
