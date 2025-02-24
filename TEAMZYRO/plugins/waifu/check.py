# made by team zyro 
from TEAMZYRO import collection, user_collection, app
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

import asyncio  # Add this for sleep function

@app.on_message(filters.command("check"))
async def check_character(client, message):
    try:
        args = message.command
        if len(args) != 2:
            sent_message = await message.reply_text("❌ Incorrect format. Please use: `/check character_id`", parse_mode=enums.ParseMode.MARKDOWN)
            await asyncio.sleep(180)  # Wait for 3 minutes
            await sent_message.delete()
            return

        character_id = args[1]
        character = await collection.find_one({'id': character_id})

        if character:
            response_message = (
                f"✨ **Character Details** ✨\n\n"
                f"🆔 **Character ID:** `{character['id']}`\n"
                f"👤 **Name:** {character['name']}\n"
                f"📺 **Anime:** {character['anime']}\n"
                f"🌟 **Rarity:** {character['rarity']}\n"
            )

            sent_message = None

            if 'vid_url' in character:
                sent_message = await client.send_video(
                    chat_id=message.chat.id,
                    video=character['vid_url'],
                    caption=response_message,
                    parse_mode=enums.ParseMode.MARKDOWN,
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("🔍 Who Has It?", callback_data=f"who_has_{character_id}")]]
                    )
                )
            elif 'img_url' in character:
                sent_message = await client.send_photo(
                    chat_id=message.chat.id,
                    photo=character['img_url'],
                    caption=response_message,
                    parse_mode=enums.ParseMode.MARKDOWN,
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("🔍 Who Has It?", callback_data=f"who_has_{character_id}")]]
                    )
                )
            else:
                sent_message = await message.reply_text("⚠️ Character has no media (image or video) associated with it.")

            if sent_message:
                await asyncio.sleep(180)  # Wait for 3 minutes
                await sent_message.delete()

        else:
            sent_message = await message.reply_text("⚠️ Character not found.")
            await asyncio.sleep(180)  # Wait for 3 minutes
            await sent_message.delete()

    except Exception as e:
        sent_message = await message.reply_text(f"⚠️ **Error:** {str(e)}")
        await asyncio.sleep(45)  # Wait for 3 minutes
        await sent_message.delete()

@app.on_callback_query(filters.regex(r"who_has_(.+)"))
async def who_has_character(client: Client, query: CallbackQuery):
    try:
        character_id = query.data.split("_")[2]

        # Find users who have this character
        users_with_character = await user_collection.find({'characters.id': character_id}).to_list(100)

        if not users_with_character:
            # Check if "No users have this character." is already in caption
            if query.message.caption and "⚠️ **No users have this character.**" in query.message.caption:
                await query.answer("Already checked!", show_alert=True)
                return

            new_caption = query.message.caption + "\n\n⚠️ **No users have this character.**"

            await query.message.edit_caption(
                caption=new_caption,
                parse_mode=enums.ParseMode.MARKDOWN,
                reply_markup=None  # Disable buttons
            )
            return

        # Generate the list of users and counts
        user_list = []
        for user in users_with_character:
            first_name = user.get('first_name', 'Unknown')
            user_id = user['id']
            count = sum(1 for c in user['characters'] if c['id'] == character_id)

            mention = f"[{first_name}](tg://user?id={user_id})"
            user_list.append(f"👤 {mention} (x{count})")

        # Limit to top 10 and format the message
        response = "📝 **Users Who Have This Character:**\n\n" + "\n".join(user_list[:10]) + "\n\n📊 **Top 10 Results Displayed!**"

        # Check if the new response is already in the caption
        if query.message.caption and response in query.message.caption:
            await query.answer("Already checked!", show_alert=True)
            return

        new_caption = query.message.caption + "\n\n" + response

        await query.message.edit_caption(
            caption=new_caption,
            parse_mode=enums.ParseMode.MARKDOWN,
            reply_markup=None  # Disable buttons
        )

    except Exception as e:
        # Prevent duplicate error message
        if query.message.caption and f"⚠️ **Error:** {str(e)}" in query.message.caption:
            return

        await query.message.edit_caption(
            caption=query.message.caption + f"\n\n⚠️ **Error:** {str(e)}",
            reply_markup=None
        )

