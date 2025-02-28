from pyrogram.types import InlineKeyboardButton

import config
from TEAMZYRO import app
from config import OWNER_USERNAME, SUPPORT_CHAT, SUPPORT_CHANNEL

bot_user = app.get_me()

def start_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_1"], url=f"https://t.me/{app.username}?startgroup=true"
            ),
            InlineKeyboardButton(text=_["S_B_2"], url=config.SUPPORT_CHAT),
        ],
    ]
    return buttons


def private_panel(_):
    buttons = [
        [InlineKeyboardButton("sᴜᴍᴍᴏɴ ᴍᴇ", url=f"https://t.me/{app.username}?startgroup=true")],
        [InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url=f"{SUPPORT_CHAT}"),  
         InlineKeyboardButton("ᴄʜᴀɴɴᴇʟ", url=f"{SUPPORT_CHANNEL}")],
        [InlineKeyboardButton("Pᴀɪᴅ Hᴏsᴛɪɴɢ", callback_data="host"),  
         InlineKeyboardButton("Dᴇᴠᴇʟᴏᴘᴇʀ", url=f"https://t.me/{OWNER_USERNAME}")],  # ✅ Added comma here
        [InlineKeyboardButton("ᴄᴏᴍᴍᴀɴᴅs", callback_data="open_help")]
    ]
    return buttons
