from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ParseMode
import asyncio
from TEAMZYRO import user_collection, app as shivuu

pending_trades = {}


@shivuu.on_message(filters.command("trade"))
async def trade(client, message):
    sender_id = message.from_user.id

    if not message.reply_to_message:
        await message.reply_text("You need to reply to a user's message to trade a character!")
        return

    receiver_id = message.reply_to_message.from_user.id

    if sender_id == receiver_id:
        await message.reply_text("You can't trade a character with yourself!")
        return

    if len(message.command) != 3:
        await message.reply_text("You need to provide two character IDs!")
        return

    sender_character_id, receiver_character_id = message.command[1], message.command[2]

    sender = await user_collection.find_one({'id': sender_id})
    receiver = await user_collection.find_one({'id': receiver_id})

    sender_character = next((character for character in sender['characters'] if character['id'] == sender_character_id), None)
    receiver_character = next((character for character in receiver['characters'] if character['id'] == receiver_character_id), None)

    if not sender_character:
        await message.reply_text("You don't have the character you're trying to trade!")
        return

    if not receiver_character:
        await message.reply_text("The other user doesn't have the character they're trying to trade!")
        return






    if len(message.command) != 3:
        await message.reply_text("/trade [Your Character ID] [Other User Character ID]!")
        return

    sender_character_id, receiver_character_id = message.command[1], message.command[2]

    
    pending_trades[(sender_id, receiver_id)] = (sender_character_id, receiver_character_id)

    
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Confirm Trade", callback_data="confirm_trade")],
            [InlineKeyboardButton("Cancel Trade", callback_data="cancel_trade")]
        ]
    )

    await message.reply_text(f"{message.reply_to_message.from_user.mention}, do you accept this trade?", reply_markup=keyboard)


@shivuu.on_callback_query(filters.create(lambda _, __, query: query.data in ["confirm_trade", "cancel_trade"]))
async def on_callback_query(client, callback_query):
    receiver_id = callback_query.from_user.id

    
    for (sender_id, _receiver_id), (sender_character_id, receiver_character_id) in pending_trades.items():
        if _receiver_id == receiver_id:
            break
    else:
        await callback_query.answer("This is not for you!", show_alert=True)
        return

    if callback_query.data == "confirm_trade":
        
        sender = await user_collection.find_one({'id': sender_id})
        receiver = await user_collection.find_one({'id': receiver_id})

        sender_character = next((character for character in sender['characters'] if character['id'] == sender_character_id), None)
        receiver_character = next((character for character in receiver['characters'] if character['id'] == receiver_character_id), None)

        
        
        sender['characters'].remove(sender_character)
        receiver['characters'].remove(receiver_character)

        
        await user_collection.update_one({'id': sender_id}, {'$set': {'characters': sender['characters']}})
        await user_collection.update_one({'id': receiver_id}, {'$set': {'characters': receiver['characters']}})

        
        sender['characters'].append(receiver_character)
        receiver['characters'].append(sender_character)

        
        await user_collection.update_one({'id': sender_id}, {'$set': {'characters': sender['characters']}})
        await user_collection.update_one({'id': receiver_id}, {'$set': {'characters': receiver['characters']}})

        
        del pending_trades[(sender_id, receiver_id)]

        await callback_query.message.edit_text(f"You have successfully traded your character with {callback_query.message.reply_to_message.from_user.mention}!")

    elif callback_query.data == "cancel_trade":
        
        del pending_trades[(sender_id, receiver_id)]

        await callback_query.message.edit_text("❌️ Sad Cancelled....")




pending_gifts = {}

# Function to auto-cancel gift after 1 hour
async def auto_cancel_gift(sender_id, receiver_id):
    await asyncio.sleep(3600)  # Wait for 1 hour (3600 seconds)

    # Check if the gift is still pending and not processed
    if (sender_id, receiver_id) in pending_gifts and not pending_gifts[(sender_id, receiver_id)]['processed']:
        del pending_gifts[(sender_id, receiver_id)]
        print(f"Gift from {sender_id} to {receiver_id} auto-cancelled after 1 hour.")  # Debugging

@shivuu.on_message(filters.command("gift"))
async def gift(client, message):
    sender_id = message.from_user.id

    # Check if the user already has a pending gift
    for _sender_id, _ in pending_gifts.keys():
        if _sender_id == sender_id:
            await message.reply_text(
                "You already have a gift processing. Please confirm or cancel it before sending another gift.",
                parse_mode=ParseMode.MARKDOWN
            )
            return

    if not message.reply_to_message:
        await message.reply_text(
            "You need to reply to a user's message to gift a character!",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    receiver_id = message.reply_to_message.from_user.id
    receiver_username = message.reply_to_message.from_user.username
    receiver_first_name = message.reply_to_message.from_user.first_name

    if sender_id == receiver_id:
        await message.reply_text(
            "You can't gift a character to yourself!",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    if len(message.command) != 2:
        await message.reply_text(
            "You need to provide a character ID!",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    character_id = message.command[1]

    sender = await user_collection.find_one({'id': sender_id})

    # Check if the sender has the character
    character = next((char for char in sender['characters'] if char['id'] == character_id), None)

    if not character:
        await message.reply_text(
            "You don't have this character in your collection!",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    # Add gift to pending gifts with a processed flag
    pending_gifts[(sender_id, receiver_id)] = {
        'character': character,
        'receiver_username': receiver_username,
        'receiver_first_name': receiver_first_name,
        'processed': False  # Initialize processed flag
    }

    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("✔️", callback_data="confirm_gift")],
            [InlineKeyboardButton("❌", callback_data="cancel_gift")]
        ]
    )

    await message.reply_text(
        f"Do you really want to gift {message.reply_to_message.from_user.mention}?",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=keyboard
    )

    # Start the auto-cancel task for this gift
    asyncio.create_task(auto_cancel_gift(sender_id, receiver_id))


@shivuu.on_callback_query(filters.create(lambda _, __, query: query.data in ["confirm_gift", "cancel_gift"]))
async def on_callback_query(client, callback_query):
    sender_id = callback_query.from_user.id

    # Check if there's a pending gift for the sender
    for (_sender_id, receiver_id), gift in pending_gifts.items():
        if _sender_id == sender_id:
            break
    else:
        await callback_query.answer("This is not for you!", show_alert=True)
        return

    if callback_query.data == "confirm_gift":
        # Check if the gift has already been processed
        if gift['processed']:
            await callback_query.answer("This gift has already been processed.", show_alert=True)
            return

        # Mark the gift as processed
        gift['processed'] = True
        
        sender = await user_collection.find_one({'id': sender_id})
        receiver = await user_collection.find_one({'id': receiver_id})

        # Transfer the character
        sender['characters'].remove(gift['character'])
        await user_collection.update_one({'id': sender_id}, {'$set': {'characters': sender['characters']}})

        if receiver:
            await user_collection.update_one({'id': receiver_id}, {'$push': {'characters': gift['character']}})
        else:
            await user_collection.insert_one({
                'id': receiver_id,
                'username': gift['receiver_username'],
                'first_name': gift['receiver_first_name'],
                'characters': [gift['character']],
            })

        del pending_gifts[(sender_id, receiver_id)]

        # Edit the message to disable the buttons
        await callback_query.message.edit_text(
            f"You have successfully gifted your character to [{gift['receiver_first_name']}](tg://user?id={receiver_id})!",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=None
        )

    elif callback_query.data == "cancel_gift":
        del pending_gifts[(sender_id, receiver_id)]
        
        # Edit the message to disable the buttons
        await callback_query.message.edit_text(
            "❌️ Gift cancelled.",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=None
      )
      
