import asyncio
import random
from pyrogram import Client, filters, types as t
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from datetime import datetime, timedelta
from TEAMZYRO import app as bot
from TEAMZYRO import user_collection, collection, user_nguess_progress, user_guess_progress, rarity_map2, RARITY_R, db



from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

redeem_collection = db['redeem']

async def get_balance(user_id):
    user_data = await user_collection.find_one({'id': user_id}, {'balance': 1, 'black_stars': 1, 'white_stars': 1, 'golden_stars': 1})
    return user_data.get('balance', 0), user_data.get('black_stars', 0), user_data.get('white_stars', 0), user_data.get('golden_stars', 0) if user_data else (0, 0, 0, 0)

async def update_balance(user_id, amount):
    # Fetch the user's current balance
    user_data = await user_collection.find_one({'id': user_id}, {'balance': 1})
    current_balance = user_data.get('balance', 0) if user_data else 0
    
    # Calculate the new balance
    new_balance = current_balance + amount
    
    # Update the user's balance in the database
    await user_collection.update_one(
        {'id': user_id},
        {'$set': {'balance': new_balance}},
        upsert=True
    )

def get_rarity_buttons():
    buttons = []
    row = []  # Temporary list to hold buttons for the current row
    
    for rarity, emoji in rarity_map2.items():
        # Add the button to the current row
        row.append(InlineKeyboardButton(f"{emoji}", callback_data=f"rarity_{rarity}"))
        
        # If the row has 3 buttons, add it to the buttons list and reset the row
        if len(row) == 3:
            buttons.append(row)
            row = []
    
    # If there are any remaining buttons (less than 3), add them as the last row
    if row:
        buttons.append(row)
    
    return InlineKeyboardMarkup(buttons)

@bot.on_message(filters.command(["shop"]))
async def shop(_, message: t.Message):
    await message.reply_text(
        "🌟 **Welcome to the Rarity Shop!** 🌟\n\n"
        "Here, you can spin for characters of different rarities. Each rarity has its own unique characters and spin cost.\n\n"
        "**Please choose the rarity you want to spin for:**",
        reply_markup=get_rarity_buttons()
    )


async def generate_random_code():
    return str(random.randint(10000, 99999))

@bot.on_callback_query(filters.regex(r"^spin_"))
async def handle_spin_click(_, query: CallbackQuery):
    user_id = query.from_user.id
    rarity = query.data.split("_")[1]  # Rarity from button

    cost = next((cost for r, cost in RARITY_R if r == rarity), 0)
    user_balance, _, _, _ = await get_balance(user_id)

    if user_balance >= cost:
        await update_balance(user_id, -cost)

        await query.edit_message_text("🎰")
        await asyncio.sleep(4)  # Wait for 4 seconds

        # Generate a unique redeem code
        random_code = await generate_random_code()

        # Store the redeem code with rarity
        await redeem_collection.insert_one({
            'user_id': user_id,
            'code': random_code,
            'rarity': rarity,  # Store the rarity
            'redeemed': False
        })

        # Send "See Code" button
        await query.edit_message_text(
            "🎟 **You got a Redeem Code!**\n\n"
            "Use `/redeem <code>` to claim your reward!",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔑 See Code", callback_data=f"see_code_{random_code}")]
            ])
        )
    else:
        await query.answer("❌ You don't have enough coins to spin.", show_alert=True)

@bot.on_callback_query(filters.regex(r"^see_code_"))
async def see_code(_, query: CallbackQuery):
    user_id = query.from_user.id
    code = query.data.split("_")[2]

    # Check if the user owns this code
    code_data = await redeem_collection.find_one({'code': code, 'user_id': user_id, 'redeemed': False})

    if code_data:
        await query.answer(f"Your redeem code: {code}", show_alert=True)
    else:
        await query.answer("❌ You cannot view this code.", show_alert=True)

@bot.on_message(filters.command(["redeem"]))
async def redeem_code(_, message):
    user_id = message.from_user.id
    args = message.text.split(" ")

    if len(args) < 2:
        return await message.reply_text("❌ Please provide a code: `/redeem 12345`")

    code = args[1]
    code_data = await redeem_collection.find_one({'code': code, 'user_id': user_id, 'redeemed': False})

    if not code_data:
        return await message.reply_text("❌ Invalid or already redeemed code!")

    rarity = code_data["rarity"]  # Get the rarity from the redeem code

    # Fetch a random character of the same rarity
    character = await collection.aggregate([
        {'$match': {'rarity': rarity}},  # Filter by rarity
        {'$sample': {'size': 1}}  # Get a random character
    ]).to_list(length=1)

    if character:
        character = character[0]  # Get first (only) character
        await user_collection.update_one(
            {'id': user_id},
            {'$push': {'characters': character}}
        )

        # Mark code as redeemed
        await redeem_collection.update_one({'code': code}, {'$set': {'redeemed': True}})

        await message.reply_photo(
            character["img_url"],  # Send character image
            caption=(
                f"🎉 **You redeemed a character!**\n\n"
                f"🌸 **Name:** {character['name']}\n"
                f"🌈 **Rarity:** {character['rarity']}\n"
                f"⛩️ **Anime:** {character['anime']}"
            )
        )
    else:
        await message.reply_text("❌ No characters found to redeem!")

@bot.on_callback_query(filters.regex(r"^back_to_rarity$"))
async def handle_back_click(_, query: t.CallbackQuery):
    await query.edit_message_text(
        "🌟 **Welcome to the Rarity Shop!** 🌟\n\n"
        "Here, you can spin for characters of different rarities. Each rarity has its own unique characters and spin cost.\n\n"
        "**Please choose the rarity you want to spin for:**",
        reply_markup=get_rarity_buttons()
    )


@bot.on_callback_query(filters.regex(r"^rarity_"))
async def handle_rarity_click(_, query: t.CallbackQuery):
    user_id = query.from_user.id
    rarity = query.data.split("_")[1]
    
    # Fetch the total number of characters of the selected rarity
    total_characters = await collection.count_documents({'rarity': rarity})
    
    # Fetch the spin cost for the selected rarity
    spin_cost = next((cost for r, cost in RARITY_R if r == rarity), 0)
    
    # Create buttons for spin and back
    spin_button = InlineKeyboardButton(f"🎰 Spin", callback_data=f"spin_{rarity}")
    back_button = InlineKeyboardButton("🔙 Back", callback_data="back_to_rarity")
    buttons = InlineKeyboardMarkup([[spin_button, back_button]])
    
    # Send the response
    await query.edit_message_text(
        f"**{rarity}**\n\n"
        f"Total characters: {total_characters}\n"
        f"Spin cost: {spin_cost} coins\n\n"
        "Do you want to spin?",
        reply_markup=buttons
    )
