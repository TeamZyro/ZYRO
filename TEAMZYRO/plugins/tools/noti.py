from pyrogram import Client, filters
from pyrogram.types import ChatMemberUpdated
from TEAMZYRO import app

@app.on_chat_member_updated(filters.group)
async def track_promote_demote(client: Client, chat_member: ChatMemberUpdated):
    old = chat_member.old_chat_member
    new = chat_member.new_chat_member

    admin = chat_member.from_user  # The admin who performed the action
    user = new.user  # The user who was promoted or demoted

    if old.status != new.status:  # Check if the status changed
        if new.status in ["administrator", "owner"] and old.status not in ["administrator", "owner"]:
            action = "promoted"
        elif new.status not in ["administrator", "owner"] and old.status in ["administrator", "owner"]:
            action = "demoted"
        else:
            return  # No promotion or demotion happened

        await client.send_message(
            chat_member.chat.id,
            f"@{admin.username} has {action} @{user.username}."
        )
