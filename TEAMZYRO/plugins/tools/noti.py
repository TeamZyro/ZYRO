from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Replace these with your own values
from TEAMZYRO import application

# Function to handle promote, demote, ban, and unban actions
async def track_actions(update: Update, context: CallbackContext):
    message = update.message

    # Get the user who performed the action (admin)
    admin = message.from_user

    # Get the user who was affected (promoted/demoted/banned/unbanned)
    user = None
    if message.new_chat_members:
        user = message.new_chat_members[0]
        action = "promoted"
    elif message.left_chat_member:
        user = message.left_chat_member
        action = "banned or removed"
    else:
        return

    if user:
        await message.reply_text(
            f"@{admin.username} has {action} @{user.username}."
        )


    # Adding a message handler to track actions

application.add_handler(MessageHandler(filters.ChatType.GROUPS, track_actions))

  
