from pyrogram import Client, filters
from pyrogram.types import Message
from TEAMZYRO import app

# Track promote and demote actions
@app.on_message(filters.group & (filters.promote_member | filters.demote_member))
async def track_promote_demote(client: Client, message: Message):
    # Get the user who performed the action (admin)
    admin = message.from_user

    # Get the user who was promoted/demoted
    if message.new_chat_members:
        user = message.new_chat_members[0]
    elif message.left_chat_member:
        user = message.left_chat_member
    else:
        user = None

    if user:
        action = "promoted" if filters.promote_member else "demoted"
        await message.reply_text(
            f"@{admin.username} has {action} @{user.username}."
        )

