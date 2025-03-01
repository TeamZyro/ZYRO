from pyrogram import Client, filters
from pyrogram.types import ChatPrivileges

from TEAMZYRO import app

@app.on_chat_member_updated()
async def admin_change_handler(client, message):
    old_status = message.old_chat_member
    new_status = message.new_chat_member
    chat_id = message.chat.id

    if old_status is None or new_status is None:
        return

    admin_user = message.from_user  # The admin making the change
    target_user = new_status.user  # The affected user
    new_title = new_status.custom_title if new_status.custom_title else "No Title"

    # 🔹 Admin Promotion / Demotion
    if old_status.status != new_status.status or old_status.privileges != new_status.privileges:
        if isinstance(new_status.privileges, ChatPrivileges):  # Promoted
            text = (
                "╭─────────────────\n"
                f"├─➩ {admin_user.mention}\n"
                f"├──── Promoted ────\n"
                f"├─➩ {target_user.mention}\n"
                f"├─ Title: {new_title}\n"
                "╰─────────────────"
            )
        else:  # Demoted
            text = (
                "╭─────────────────\n"
                f"├─➩ {admin_user.mention}\n"
                f"├──── Demoted ────\n"
                f"├─➩ {target_user.mention}\n"
                "╰─────────────────"
            )
        await client.send_message(chat_id, text)
    
    # 🔹 Title Change
    elif old_status.custom_title != new_status.custom_title:
        text = (
            "╭─────────────────\n"
            f"├─➩ {admin_user.mention}\n"
            f"├──── Changed Title ────\n"
            f"├─➩ {target_user.mention}\n"
            f"├─ New Title: {new_title}\n"
            "╰─────────────────"
        )
        await client.send_message(chat_id, text)


