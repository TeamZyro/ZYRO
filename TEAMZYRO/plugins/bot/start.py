import os
import random
import time
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from TEAMZYRO import app
from config import OWNER_USERNAME, LOGGER_ID, SUPPORT_CHANNEL, SUPPORT_CHAT 
from TEAMZYRO.utils.formatters import get_readable_time
from TEAMZYRO.utils.inline import help_pannel, private_panel, start_panel

NEXI_VID = [
    "https://envs.sh/QjY.mp4",
    "https://envs.sh/QjY.mp4"
]

START_TIME = time.time()

def get_uptime():
    uptime_seconds = int(time.time() - START_TIME)
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}h {minutes}m {seconds}s"

async def generate_start_message(client, message):
    bot_user = await client.get_me()
    bot_name = bot_user.first_name

    caption = f"""
๏ 𝑻𝑯𝑰𝑺 𝑰𝑺 𝑨𝑫𝑽𝑨𝑵𝑪𝑬 𝑴𝑼𝑺𝑰𝑪 𝑷𝑳𝑨𝒀𝑬𝑹 , 𝑴𝑨𝑵𝑨𝑮𝑬𝑴𝑬𝑵𝑻 𝑨𝑵𝑫 𝑾𝑨𝑰𝑭𝑼 𝑩𝑶𝑻 𝑭𝑶𝑹 𝑻𝑬𝑳𝑬𝑮𝑹𝑨𝑴 𝑮𝑹𝑶𝑼𝑷𝑺 + 𝑪𝑯𝑨𝑵𝑵𝑬𝑳𝑺 𝑽𝑪.\n\n🔐ᴜꜱᴇ » /help ᴛᴏ ᴄʜᴇᴄᴋ ғᴇᴀᴛᴜʀᴇs.\n\n👷 ᴍᴀᴅᴇ ʙʏ ➪ [TEAM ✯ ZYRO](https://t.me/TEAMZYRO) 💞"""

    buttons = [
        [InlineKeyboardButton("sᴜᴍᴍᴏɴ ᴍᴇ", url=f"https://t.me/{bot_user.username}?startgroup=true")],
        [InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url=f"{SUPPORT_CHAT}"),  
         InlineKeyboardButton("ᴄʜᴀɴɴᴇʟ", url=f"{SUPPORT_CHANNEL}")],
        [InlineKeyboardButton("Pᴀɪᴅ Hᴏsᴛɪɴɢ", callback_data="host"),  
         InlineKeyboardButton("Dᴇᴠᴇʟᴏᴘᴇʀ", url=f"https://t.me/{OWNER_USERNAME}")],  # ✅ Added comma here
        [InlineKeyboardButton("ᴄᴏᴍᴍᴀɴᴅs", callback_data="open_help")]
    ]

    return caption, InlineKeyboardMarkup(buttons)

@app.on_message(filters.command(["start"]) & filters.private)
async def start_command(client, message):
    caption, buttons = await generate_start_message(client, message)
    video = random.choice(NEXI_VID)  # Random video select
    await app.send_message(
        chat_id=LOGGER_ID,
        text=f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>sᴜᴅᴏʟɪsᴛ</b>.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
    )
    await message.reply_video(
        video=video,
        caption=caption,
        reply_markup=buttons
    )


@app.on_message(filters.command(["start"]) & filters.group)
async def start_gp(client, message: Message, _):
    out = start_panel(_)
    uptime = int(time.time() - _boot_)
    await message.reply_video(
        random.choice(NEXI_VID),
        caption=_["start_1"].format(app.mention, get_readable_time(uptime)),
        reply_markup=InlineKeyboardMarkup(out),
    )
    return await add_served_chat(message.chat.id)

# Mɪɴɪ Gᴀᴍᴇs
# Mᴜɪsᴄ Mᴀɴᴀɢᴇᴍᴇɴᴛ Wᴀɪғᴜ Aɴᴅ Hᴜsʙᴀɴᴅᴏs Exᴛʀᴀ

# 🔹 Help Button Click Handler
@app.on_callback_query(filters.regex("^open_help$"))
async def show_help_menu(client, query: CallbackQuery):
    time.sleep(0.5)
    buttons = [
        [InlineKeyboardButton("Mᴜɪsᴄ", callback_data="help_music"),
        InlineKeyboardButton("Mᴀɴᴀɢᴇᴍᴇɴᴛ", callback_data="help_management")],
        [InlineKeyboardButton("Wᴀɪғᴜ Aɴᴅ Hᴜsʙᴀɴᴅᴏs", callback_data="help_waifu")],
        [InlineKeyboardButton("Exᴛʀᴀ", callback_data="help_extra"),
        InlineKeyboardButton("Mɪɴɪ Gᴀᴍᴇs", callback_data="help_minigame")],
        [InlineKeyboardButton("⬅ Back", callback_data="back_to_home")]
    ]

    await query.message.edit_text(
        "Choose a category for which you want to get help.",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# 🔹 Music Help Menu
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import time

@app.on_callback_query(filters.regex("^help_music$"))
async def show_music_help_menu(client, query: CallbackQuery):
    time.sleep(0.5)
    buttons = [
        [
            InlineKeyboardButton("ᴀᴅᴍɪɴ", callback_data="help_admin"),
            InlineKeyboardButton("ᴀᴜᴛʜ", callback_data="help_auth"),
            InlineKeyboardButton("ɢ-ᴄᴀsᴛ", callback_data="help_broadcast")
        ],
        [
            InlineKeyboardButton("ʙʟ-ᴄʜᴀᴛ", callback_data="help_blacklist"),
            InlineKeyboardButton("ʙʟ-ᴜsᴇʀ", callback_data="help_block"),
            InlineKeyboardButton("ᴄ-ᴘʟᴀʏ", callback_data="help_channelplay")
        ],
        [
            InlineKeyboardButton("ᴄ-ᴘʟᴀʏ", callback_data="help_gban"),
            InlineKeyboardButton("ʟᴏᴏᴘ", callback_data="help_loop"),
            InlineKeyboardButton("ʟᴏɢ", callback_data="help_maintenance")
        ],
        [
            InlineKeyboardButton("ᴘɪɴɢ", callback_data="help_ping"),
            InlineKeyboardButton("ᴘʟᴀʏ", callback_data="help_play"),
            InlineKeyboardButton("sʜᴜғғʟᴇ", callback_data="help_shuffle")
        ],
        [
            InlineKeyboardButton("sᴇᴇᴋ", callback_data="help_seek"),
            InlineKeyboardButton("sᴏɴɢ", callback_data="help_song"),
            InlineKeyboardButton("sᴘᴇᴇᴅ", callback_data="help_speed")
        ],
        [
            InlineKeyboardButton("⬅ Back", callback_data="open_help")
        ]
    ]

    await query.message.edit_text(
        "Select a music command to get help.",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# 🔹 Individual Music Command Help Handlers
MUSIC_HELP_TEXTS = {
    "help_admin": """<b><u>ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅs :</b></u>

ᴊᴜsᴛ ᴀᴅᴅ <b>ᴄ</b> ɪɴ ᴛʜᴇ sᴛᴀʀᴛɪɴɢ ᴏғ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅs ᴛᴏ ᴜsᴇ ᴛʜᴇᴍ ғᴏʀ ᴄʜᴀɴɴᴇʟ.

- /pause : ᴩᴀᴜsᴇ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴩʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ.
- /resume : ʀᴇsᴜᴍᴇ ᴛʜᴇ ᴩᴀᴜsᴇᴅ sᴛʀᴇᴀᴍ.
- /skip : sᴋɪᴩ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴩʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ ᴀɴᴅ sᴛᴀʀᴛ sᴛʀᴇᴀᴍɪɴɢ ᴛʜᴇ ɴᴇxᴛ ᴛʀᴀᴄᴋ ɪɴ ǫᴜᴇᴜᴇ.
- /end ᴏʀ /stop : ᴄʟᴇᴀʀs ᴛʜᴇ ǫᴜᴇᴜᴇ ᴀɴᴅ ᴇɴᴅ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴩʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ.
- /player : ɢᴇᴛ ᴀ ɪɴᴛᴇʀᴀᴄᴛɪᴠᴇ ᴩʟᴀʏᴇʀ ᴩᴀɴᴇʟ.
- /queue : sʜᴏᴡs ᴛʜᴇ ǫᴜᴇᴜᴇᴅ ᴛʀᴀᴄᴋs ʟɪsᴛ.
""",
    "help_auth": """<b><u>ᴀᴜᴛʜ ᴜsᴇʀs :</b></u>

ᴀᴜᴛʜ ᴜsᴇʀs ᴄᴀɴ ᴜsᴇ ᴀᴅᴍɪɴ ʀɪɢʜᴛs ɪɴ ᴛʜᴇ ʙᴏᴛ ᴡɪᴛʜᴏᴜᴛ ᴀᴅᴍɪɴ ʀɪɢʜᴛs ɪɴ ᴛʜᴇ ᴄʜᴀᴛ.

/auth [ᴜsᴇʀɴᴀᴍᴇ/ᴜsᴇʀ_ɪᴅ] : ᴀᴅᴅ ᴀ ᴜsᴇʀ ᴛᴏ ᴀᴜᴛʜ ʟɪsᴛ ᴏғ ᴛʜᴇ ʙᴏᴛ.
/unauth [ᴜsᴇʀɴᴀᴍᴇ/ᴜsᴇʀ_ɪᴅ] : ʀᴇᴍᴏᴠᴇ ᴀ ᴀᴜᴛʜ ᴜsᴇʀs ғʀᴏᴍ ᴛʜᴇ ᴀᴜᴛʜ ᴜsᴇʀs ʟɪsᴛ.
/authusers : sʜᴏᴡs ᴛʜᴇ ʟɪsᴛ ᴏғ ᴀᴜᴛʜ ᴜsᴇʀs ᴏғ ᴛʜᴇ ɢʀᴏᴜᴩ.
""",
    "help_broadcast": """<u><b>ʙʀᴏᴀᴅᴄᴀsᴛ ғᴇᴀᴛᴜʀᴇ</b></u> [ᴏɴʟʏ ғᴏʀ sᴜᴅᴏᴇʀs] :

/broadcast [ᴍᴇssᴀɢᴇ ᴏʀ ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ] : ʙʀᴏᴀᴅᴄᴀst ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ sᴇʀᴠᴇᴅ ᴄʜᴀᴛs ᴏғ ᴛʜᴇ ʙᴏᴛ.

<u>ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ ᴍᴏᴅᴇs :</u>
<b>-pin</b> : ᴩɪɴs ʏᴏᴜʀ ʙʀᴏᴀᴅᴄᴀsᴛᴇᴅ ᴍᴇssᴀɢᴇs ɪɴ sᴇʀᴠᴇᴅ ᴄʜᴀᴛs.
<b>-pinloud</b> : ᴩɪɴs ʏᴏᴜʀ ʙʀᴏᴀᴅᴄᴀsᴛᴇᴅ ᴍᴇssᴀɢᴇ ɪɴ sᴇʀᴠᴇᴅ ᴄʜᴀᴛs ᴀɴᴅ sᴇɴᴅ ɴᴏᴛɪғɪᴄᴀᴛɪᴏɴ ᴛᴏ ᴛʜᴇ ᴍᴇᴍʙᴇʀs.
<b>-user</b> : ʙʀᴏᴀᴅᴄᴀsᴛs ᴛʜᴇ ᴍᴇssᴀɢᴇ ᴛᴏ ᴛʜᴇ ᴜsᴇʀs ᴡʜᴏ ʜᴀᴠᴇ sᴛᴀʀᴛᴇᴅ ʏᴏᴜʀ ʙᴏᴛ.
<b>-assistant</b> : ʙʀᴏᴀᴅᴄᴀsᴛ ʏᴏᴜʀ ᴍᴇssᴀɢᴇ ғʀᴏᴍ ᴛʜᴇ ᴀssɪᴛᴀɴᴛ ᴀᴄᴄᴏᴜɴᴛ ᴏғ ᴛʜᴇ ʙᴏᴛ.
<b>-nobot</b> : ғᴏʀᴄᴇs ᴛʜᴇ ʙᴏᴛ ᴛᴏ ɴᴏᴛ ʙʀᴏᴀᴅᴄᴀsᴛ ᴛʜᴇ ᴍᴇssᴀɢᴇ..

<b>ᴇxᴀᴍᴩʟᴇ:</b> <code>/broadcast -user -assistant -pin ᴛᴇsᴛɪɴɢ ʙʀᴏᴀᴅᴄᴀsᴛ</code>
""",
    "help_blacklist": """<u><b>ᴄʜᴀᴛ ʙʟᴀᴄᴋʟɪsᴛ ғᴇᴀᴛᴜʀᴇ :</b></u> [ᴏɴʟʏ ғᴏʀ sᴜᴅᴏᴇʀs]

ʀᴇsᴛʀɪᴄᴛ sʜɪᴛ ᴄʜᴀᴛs ᴛᴏ ᴜsᴇ ᴏᴜʀ ᴘʀᴇᴄɪᴏᴜs ʙᴏᴛ.

/blacklistchat [ᴄʜᴀᴛ ɪᴅ] : ʙʟᴀᴄᴋʟɪsᴛ ᴀ ᴄʜᴀᴛ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜᴇ ʙᴏᴛ.
/whitelistchat [ᴄʜᴀᴛ ɪᴅ] : ᴡʜɪᴛᴇʟɪsᴛ ᴛʜᴇ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ᴄʜᴀᴛ.
/blacklistedchat : sʜᴏᴡs ᴛʜᴇ ʟɪsᴛ ᴏғ ʙʟᴏᴄᴋᴇᴅ ᴄʜᴀᴛs.
""",
    "help_block": """<u><b>ʙʟᴏᴄᴋ ᴜsᴇʀs:</b></u> [ᴏɴʟʏ ғᴏʀ sᴜᴅᴏᴇʀs]

sᴛᴀʀᴛs ɪɢɴᴏʀɪɴɢ ᴛʜᴇ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ᴜsᴇʀ, sᴏ ᴛʜᴀᴛ ʜᴇ ᴄᴀɴ'ᴛ ᴜsᴇ ʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅs.

/block [ᴜsᴇʀɴᴀᴍᴇ ᴏʀ ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴜsᴇʀ] : ʙʟᴏᴄᴋ ᴛʜᴇ ᴜsᴇʀ ғʀᴏᴍ ᴏᴜʀ ʙᴏᴛ.
/unblock [ᴜsᴇʀɴᴀᴍᴇ ᴏʀ ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴜsᴇʀ] : ᴜɴʙʟᴏᴄᴋs ᴛʜᴇ ʙʟᴏᴄᴋᴇᴅ ᴜsᴇʀ.
/blockedusers : sʜᴏᴡs ᴛʜᴇ ʟɪsᴛ ᴏғ ʙʟᴏᴄᴋᴇᴅ ᴜsᴇʀs.
""",
    "help_channelplay": """<u><b>ᴄʜᴀɴɴᴇʟ ᴩʟᴀʏ ᴄᴏᴍᴍᴀɴᴅs:</b></u>

ʏᴏᴜ ᴄᴀɴ sᴛʀᴇᴀᴍ ᴀᴜᴅɪᴏ/ᴠɪᴅᴇᴏ ɪɴ ᴄʜᴀɴɴᴇʟ.

/cplay : sᴛᴀʀᴛs sᴛʀᴇᴀᴍɪɴɢ ᴛʜᴇ ʀᴇǫᴜᴇsᴛᴇᴅ ᴀᴜᴅɪᴏ ᴛʀᴀᴄᴋ ᴏɴ ᴄʜᴀɴɴᴇʟ's ᴠɪᴅᴇᴏᴄʜᴀᴛ.
/cvplay : sᴛᴀʀᴛs sᴛʀᴇᴀᴍɪɴɢ ᴛʜᴇ ʀᴇǫᴜᴇsᴛᴇᴅ ᴠɪᴅᴇᴏ ᴛʀᴀᴄᴋ ᴏɴ ᴄʜᴀɴɴᴇʟ's ᴠɪᴅᴇᴏᴄʜᴀᴛ.
/cplayforce or /cvplayforce : sᴛᴏᴩs ᴛʜᴇ ᴏɴɢᴏɪɴɢ sᴛʀᴇᴀᴍ ᴀɴᴅ sᴛᴀʀᴛs sᴛʀᴇᴀᴍɪɴɢ ᴛʜᴇ ʀᴇǫᴜᴇsᴛᴇᴅ ᴛʀᴀᴄᴋ.

/channelplay [ᴄʜᴀᴛ ᴜsᴇʀɴᴀᴍᴇ ᴏʀ ɪᴅ] ᴏʀ [ᴅɪsᴀʙʟᴇ] : ᴄᴏɴɴᴇᴄᴛ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴀ ɢʀᴏᴜᴩ ᴀɴᴅ sᴛᴀʀᴛs sᴛʀᴇᴀᴍɪɴɢ ᴛʀᴀᴄᴋs ʙʏ ᴛʜᴇ ʜᴇʟᴩ ᴏғ ᴄᴏᴍᴍᴀɴᴅs sᴇɴᴛ ɪɴ ɢʀᴏᴜᴩ.
""",
    "help_gban": """<u><b>ɢʟᴏʙᴀʟ ʙᴀɴ ғᴇᴀᴛᴜʀᴇ</b></u> [ᴏɴʟʏ ғᴏʀ sᴜᴅᴏᴇʀs] :

/gban [ᴜsᴇʀɴᴀᴍᴇ ᴏʀ ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴜsᴇʀ] : ɢʟᴏʙᴀʟʟʏ ʙᴀɴs ᴛʜᴇ ᴄʜᴜᴛɪʏᴀ ғʀᴏᴍ ᴀʟʟ ᴛʜᴇ sᴇʀᴠᴇᴅ ᴄʜᴀᴛs ᴀɴᴅ ʙʟᴀᴄᴋʟɪsᴛ ʜɪᴍ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜᴇ ʙᴏᴛ.
/ungban [ᴜsᴇʀɴᴀᴍᴇ ᴏʀ ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴜsᴇʀ] : ɢʟᴏʙᴀʟʟʏ ᴜɴʙᴀɴs ᴛʜᴇ ɢʟᴏʙᴀʟʟʏ ʙᴀɴɴᴇᴅ ᴜsᴇʀ.
/gbannedusers : sʜᴏᴡs ᴛʜᴇ ʟɪsᴛ ᴏғ ɢʟᴏʙᴀʟʟʏ ʙᴀɴɴᴇᴅ ᴜsᴇʀs.
""",
    "help_loop": """<b><u>ʟᴏᴏᴘ sᴛʀᴇᴀᴍ :</b></u>

<b>sᴛᴀʀᴛs sᴛʀᴇᴀᴍɪɴɢ ᴛʜᴇ ᴏɴɢᴏɪɴɢ sᴛʀᴇᴀᴍ ɪɴ ʟᴏᴏᴘ</b>

/loop [enable/disable] : ᴇɴᴀʙʟᴇs/ᴅɪsᴀʙʟᴇs ʟᴏᴏᴘ ғᴏʀ ᴛʜᴇ ᴏɴɢᴏɪɴɢ sᴛʀᴇᴀᴍ
/loop [1, 2, 3, ...] : ᴇɴᴀʙʟᴇs ᴛʜᴇ ʟᴏᴏᴘ ғᴏʀ ᴛʜᴇ ɢɪᴠᴇɴ ᴠᴀʟᴜᴇ.
""",
    "help_maintenance": """<u><b>ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ ᴍᴏᴅᴇ</b></u> [ᴏɴʟʏ ғᴏʀ sᴜᴅᴏᴇʀs] :

/logs : ɢᴇᴛ ʟᴏɢs ᴏғ ᴛʜᴇ ʙᴏᴛ.

/logger [ᴇɴᴀʙʟᴇ/ᴅɪsᴀʙʟᴇ] : ʙᴏᴛ ᴡɪʟʟ sᴛᴀʀᴛ ʟᴏɢɢɪɴɢ ᴛʜᴇ ᴀᴄᴛɪᴠɪᴛɪᴇs ʜᴀᴩᴩᴇɴ ᴏɴ ʙᴏᴛ.

/maintenance [ᴇɴᴀʙʟᴇ/ᴅɪsᴀʙʟᴇ] : ᴇɴᴀʙʟᴇ ᴏʀ ᴅɪsᴀʙʟᴇ ᴛʜᴇ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ ᴍᴏᴅᴇ ᴏғ ʏᴏᴜʀ ʙᴏᴛ.
""",
    "help_ping": """<b><u>ᴘɪɴɢ & sᴛᴀᴛs :</b></u>

/start : sᴛᴀʀᴛs ᴛʜᴇ ᴍᴜsɪᴄ ʙᴏᴛ.
/help : ɢᴇᴛ ʜᴇʟᴩ ᴍᴇɴᴜ ᴡɪᴛʜ ᴇxᴩʟᴀɴᴀᴛɪᴏɴ ᴏғ ᴄᴏᴍᴍᴀɴᴅs.

/ping : sʜᴏᴡs ᴛʜᴇ ᴩɪɴɢ ᴀɴᴅ sʏsᴛᴇᴍ sᴛᴀᴛs ᴏғ ᴛʜᴇ ʙᴏᴛ.

/stats : sʜᴏᴡs ᴛʜᴇ ᴏᴠᴇʀᴀʟʟ sᴛᴀᴛs ᴏғ ᴛʜᴇ ʙᴏᴛ.
""",
    "help_play": """<u><b>ᴩʟᴀʏ ᴄᴏᴍᴍᴀɴᴅs :</b></u>

<b>v :</b> sᴛᴀɴᴅs ғᴏʀ ᴠɪᴅᴇᴏ ᴩʟᴀʏ.
<b>force :</b> sᴛᴀɴᴅs ғᴏʀ ғᴏʀᴄᴇ ᴩʟᴀʏ.

/play ᴏʀ /vplay : sᴛᴀʀᴛs sᴛʀᴇᴀᴍɪɴɢ ᴛʜᴇ ʀᴇǫᴜᴇsᴛᴇᴅ ᴛʀᴀᴄᴋ ᴏɴ ᴠɪᴅᴇᴏᴄʜᴀᴛ.

/playforce ᴏʀ /vplayforce : sᴛᴏᴩs ᴛʜᴇ ᴏɴɢᴏɪɴɢ sᴛʀᴇᴀᴍ ᴀɴᴅ sᴛᴀʀᴛs sᴛʀᴇᴀᴍɪɴɢ ᴛʜᴇ ʀᴇǫᴜᴇsᴛᴇᴅ ᴛʀᴀᴄᴋ.
""",
    "help_shuffle": """<b><u>sʜᴜғғʟᴇ ᴏ̨ᴜᴇᴜᴇ :</b></u>

/shuffle : sʜᴜғғʟᴇ's ᴛʜᴇ ᴏ̨ᴜᴇᴜᴇ.
/queue : sʜᴏᴡs ᴛʜᴇ sʜᴜғғʟᴇᴅ ᴏ̨ᴜᴇᴜᴇ.
""",
    "help_seek": """<b><u>sᴇᴇᴋ sᴛʀᴇᴀᴍ :</b></u>

/seek [ᴅᴜʀᴀᴛɪᴏɴ ɪɴ sᴇᴄᴏɴᴅs] : sᴇᴇᴋ ᴛʜᴇ sᴛʀᴇᴀᴍ ᴛᴏ ᴛʜᴇ ɢɪᴠᴇɴ ᴅᴜʀᴀᴛɪᴏɴ.
/seekback [ᴅᴜʀᴀᴛɪᴏɴ ɪɴ sᴇᴄᴏɴᴅs] : ʙᴀᴄᴋᴡᴀʀᴅ sᴇᴇᴋ ᴛʜᴇ sᴛʀᴇᴀᴍ ᴛᴏ ᴛʜᴇ ᴛʜᴇ ɢɪᴠᴇɴ ᴅᴜʀᴀᴛɪᴏɴ.
""",
    "help_song": """<b><u>sᴏɴɢ ᴅᴏᴡɴʟᴏᴀᴅ</b></u>

/song [sᴏɴɢ ɴᴀᴍᴇ/ʏᴛ ᴜʀʟ] : ᴅᴏᴡɴʟᴏᴀᴅ ᴀɴʏ ᴛʀᴀᴄᴋ ғʀᴏᴍ ʏᴏᴜᴛᴜʙᴇ ɪɴ ᴍᴘ3 ᴏʀ ᴍᴘ4 ғᴏʀᴍᴀᴛs.
""",
    "help_speed": """<b><u>sᴘᴇᴇᴅ ᴄᴏᴍᴍᴀɴᴅs :</b></u>

ʏᴏᴜ ᴄᴀɴ ᴄᴏɴᴛʀᴏʟ ᴛʜᴇ ᴘʟᴀʏʙᴀᴄᴋ sᴘᴇᴇᴅ ᴏғ ᴛʜᴇ ᴏɴɢᴏɪɴɢ sᴛʀᴇᴀᴍ. [ᴀᴅᴍɪɴs ᴏɴʟʏ]

/speed or /playback : ғᴏʀ ᴀᴅᴊᴜsᴛɪɴɢ ᴛʜᴇ ᴀᴜᴅɪᴏ ᴘʟᴀʏʙᴀᴄᴋ sᴘᴇᴇᴅ ɪɴ ɢʀᴏᴜᴘ.
/cspeed or /cplayback : ғᴏʀ ᴀᴅᴊᴜsᴛɪɴɢ ᴛʜᴇ ᴀᴜᴅɪᴏ ᴘʟᴀʏʙᴀᴄᴋ sᴘᴇᴇᴅ ɪɴ ᴄʜᴀɴɴᴇʟ.
"""
}

# 🔹 Waifu Help Menu
@app.on_callback_query(filters.regex("^help_waifu$"))
async def show_waifu_help_menu(client, query: CallbackQuery):
    time.sleep(1)
    buttons = [
        [InlineKeyboardButton("Balance", callback_data="help_balance"),
         InlineKeyboardButton("Check", callback_data="help_check"),
         InlineKeyboardButton("Guess", callback_data="help_guess")],
        [InlineKeyboardButton("Harem", callback_data="help_harem"),
         InlineKeyboardButton("Inline", callback_data="help_inline"),
         InlineKeyboardButton("Favorites", callback_data="help_favorites")],
        [InlineKeyboardButton("Claim", callback_data="help_claim"),
         InlineKeyboardButton("Requests", callback_data="help_requests"),
         InlineKeyboardButton("Gift", callback_data="help_gift")],
        [InlineKeyboardButton("Rankings", callback_data="help_rankings"),
         InlineKeyboardButton("Sips", callback_data="help_sips"),
         InlineKeyboardButton("Shop", callback_data="help_shop")],
        [InlineKeyboardButton("⬅ Back", callback_data="open_help")]
    ]

    await query.message.edit_text(
        "Select a waifu command to get help.",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


# 🔹 Individual Waifu Command Help Handlers
WAIFU_HELP_TEXTS = {
    "help_balance": """💰 **Balance Commands**:
- `/balance` → Check your balance.
- `/balance @username` → Check another user's balance.
- `/balance user_id` → Check balance using user ID.

💳 **Payment Commands**:
- `/pay amount @username` → Send coins to a user.
- `/pay amount user_id` → Send coins using user ID.
- `/pay amount` (reply to a user) → Send coins to the replied user.

⚠ **Note**:
- You must have enough balance to send coins.
- Payments are final and cannot be reversed.
""",
    "help_check": """Use `/check <character_id>` to view details of a character.

- Displays character ID, name, anime, and rarity.
- Shows an image or video if available.
- Use the 'Who Have It' button to see the top 10 owners.
""",
    "help_guess": """Use `/guess <character_name>` to guess the mystery character.

- Earn 40 coins for a correct guess.
- The first correct guess captures the character.
- If incorrect, you can try again.
- A 'See Harem' button lets you view your collected characters.
""",
    "help_harem": """Use `/harem` or `/collection` to view your collected characters.

- Navigate pages using the buttons.
- Filter by rarity using the filter button.
- Use "Collection" button for detailed inline view.
- "💌 AMV" button shows a video-only collection.

Characters are grouped by anime and show the count you own.
""",
    "help_inline": """Use inline queries to search for characters or view collections.

- `@Gaming_X_World_Bot query` → Search for characters.
- `@Gaming_X_World_Bot collection.<user_id>` → View a user's character collection.
- `@Gaming_X_World_Bot collection.<user_id> <name>` → Search within a user's collection.
- `@Gaming_X_World_Bot <query>.AMV` → Show characters with video clips.

Results include character name, anime, rarity, and image/video.
""",
    "help_favorites": """Add your favorite characters to your collection.

- `/fav <character_id>` → Add a character to your favorites.
- Click "✅ Yes" to confirm or "❎ No" to cancel.
- Your favorite characters will be saved for quick access.

Note: You can only favorite characters that are in your collection.
""",
    "help_claim": """Claim a free character every day! 🌟

- `/hclaim` or `/claim` → Claim your daily character.
- You must be in the required channel to claim.
- If you've already claimed today, you'll see the time remaining for the next claim.
- Characters are unique and not repeated from your collection.
- Return tomorrow for another claim! 🌸
""",
    "help_requests": """Use the following command to request a character:

Request a Character  
`/reqchar <character_id>` - Request a specific character by ID.

Once requested, the owner will review and approve or deny your request.
""",
    "help_gift": """🎁 **Gift System**  
Send characters to other users using the `/gift` command.

**Commands:**
- `/gift <character_id>` (Reply to a user's message)  
  ┗ Gift a character to another user.

**How it works:**
1. Reply to a user's message.
2. Use `/gift <character_id>` to send a character.
3. The receiver gets a confirmation message.
4. The gift is auto-canceled if not confirmed within 1 hour.
""",
    "help_rankings": """🏆 **Rankings & Leaderboards**  
Check out the top users and groups in different categories!

**Commands:**
- `/rank`  
  ┗ View the Top 10 Users with the most characters.

**Categories:**
1. **Top Users** → Users with the highest number of characters.
2. **Top Groups** → Groups that have guessed the most characters.
3. **MTOP** → Users ranked by the highest coin balance.

**How it works:**
- `/rank` will display the top 10 users based on character count.
- You can switch between Top Users, Top Groups, and MTOP using the buttons.
- Rankings update dynamically as users collect characters or earn coins.
""",
    "help_sips": """Use this command to search for characters by name.

Commands:
- /sips <character_name> → Search for a character by name.
- Pagination buttons will appear if multiple results are found.

Each result includes:
- Character name
- Anime name
- Character ID
- Rarity indicator
""",
    "help_shop": """🛒 Shop Commands:
- /shop - Open the shop menu.
- /hshopmenu - Alternative command to open the shop.
- /hshop - Another way to access the shop.
- /addshop <id> <price> - Add a character to the shop (Admin only).

🛍 How It Works:
1. Use /shop to browse characters.
2. Click "Buy" to purchase a character.
3. Click "Next" to view more characters.
4. Make sure you have enough balance!

🔹 Enjoy shopping!
"""
}

@app.on_callback_query(filters.regex(r"^help_(balance|check|guess|harem|inline|favorites|claim|requests|gift|rankings|sips|shop)$"))
async def show_waifu_command_help(client, query: CallbackQuery):
    time.sleep(0.5)
    command = query.data
    help_text = WAIFU_HELP_TEXTS.get(command, "No help available for this command.")
    
    buttons = [[InlineKeyboardButton("⬅ Back", callback_data="help_waifu")]]
    
    await query.message.edit_text(f"**{command.capitalize()} Help:**\n\n{help_text}", reply_markup=InlineKeyboardMarkup(buttons))


@app.on_callback_query(filters.regex(r"^help_(admin|auth|broadcast|blacklist|block|channelplay|gban|loop|maintenance|ping|play|shuffle|seek|song|speed)$"))
async def show_music_command_help(client, query: CallbackQuery):
    time.sleep(0.5)
    command = query.data
    help_text = MUSIC_HELP_TEXTS.get(command, "No help available for this command.")
    
    buttons = [[InlineKeyboardButton("⬅ Back", callback_data="help_music")]]
    
    await query.message.edit_text(f"**{command.capitalize()} Help:**\n\n{help_text}", reply_markup=InlineKeyboardMarkup(buttons))

# 🔹 Back to Home (Edit Message Instead of Sending New)
@app.on_callback_query(filters.regex("^back_to_home$"))
async def back_to_home(client, query: CallbackQuery):
    time.sleep(0.5)
    caption, buttons = await generate_start_message(client, query.message)
    await query.message.edit_text(caption, reply_markup=buttons)

@app.on_callback_query(filters.regex("^help_extra$"))
async def show_extra_help_menu(client, query: CallbackQuery):
    time.sleep(0.5)
    buttons = [
        [InlineKeyboardButton("ɢᴘᴛ", callback_data="help_chatgpt"),
         InlineKeyboardButton("sᴛɪᴄᴋᴇʀ", callback_data="help_sticker"),
         InlineKeyboardButton("ᴛᴀɢ-ᴀʟʟ", callback_data="help_tagall")],
        [InlineKeyboardButton("ɪɴғᴏ", callback_data="help_info"),
         InlineKeyboardButton("ɢʀᴏᴜᴘ", callback_data="help_group"),
         InlineKeyboardButton("ᴀᴄᴛɪᴏɴ", callback_data="help_action")],
        [InlineKeyboardButton("sᴇᴀʀᴄʜ", callback_data="help_search"),
         InlineKeyboardButton("Font", callback_data="help_font"),
         InlineKeyboardButton("Game", callback_data="help_game")],
        [InlineKeyboardButton("T-Grap", callback_data="help_tg"),
         InlineKeyboardButton("Imposter", callback_data="help_imposter"),
         InlineKeyboardButton("Truth-Dare", callback_data="help_td")],
        [InlineKeyboardButton("Quote", callback_data="help_q"),
         InlineKeyboardButton("TTS", callback_data="help_tts"),
         InlineKeyboardButton("Fun", callback_data="help_fun")],
        [
            InlineKeyboardButton("⬅ Back", callback_data="open_help")
        ]
    ]

    await query.message.edit_text(
        "Select an extra command to get help.",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


# 🔹 Individual Extra Command Help Handlers
EXTRA_HELP_TEXTS = {
    "help_chatgpt": """CʜᴀᴛGPT

CʜᴀᴛGPT ᴄᴏᴍᴍᴀɴᴅꜱ:

/ask ➠ ǫᴜᴇʀɪᴇs ᴛʜᴇ ᴀɪ ᴍᴏᴅᴇʟ ᴛᴏ ɢᴇᴛ ᴀ ʀᴇsᴘᴏɴsᴇ ᴛᴏ ʏᴏᴜʀ ǫᴜᴇsᴛɪᴏɴ.
""",
    "help_sticker": """sᴛɪᴄᴋᴇʀs

sᴛɪᴄᴋᴇʀs ᴄᴏᴍᴍᴀɴᴅꜱ:

/packkang ➠ ᴄʀᴇᴀᴛᴇs ᴀ ᴘᴀᴄᴋ ᴏғ sᴛɪᴄᴋᴇʀs ғʀᴏᴍ ᴀ ᴏᴛʜᴇʀ ᴘᴀᴄᴋ.
/stickerid ➠ ɢᴇᴛs ᴛʜᴇ sᴛɪᴄᴋᴇʀ ɪᴅ ᴏғ ᴀ sᴛɪᴄᴋᴇʀ.
""",
    "help_tagall": """Tᴀɡ

Tᴀɡ ᴄᴏᴍᴍᴀɴᴅꜱ:

✿ ᴄʜᴏᴏsᴇ ᴛᴀɢ ɪɴ ʏᴏᴜʀ ᴄʜᴀᴛ ✿

๏ /gmtag ➛ ɢᴏᴏᴅ ᴍᴏʀɴɪɴɢ 
ᴛᴀɢ sᴛᴏᴘ ⇴ /gmstop

๏ /gntag ➛ ɢᴏᴏᴅ ɴɪɢʜᴛ ᴛᴀɢ sᴛᴏᴘ ⇴ /gnstop

๏ /tagall ➛ ʀᴀɴᴅᴏᴍ ᴍᴇssᴀɢᴇ ᴛᴀɢ sᴛᴏᴘ ⇴ /tagoff /tagstop

๏ /hitag ➛ ʀᴀɴᴅᴏᴍ ʜɪɴᴅɪ ᴍᴇssᴀɢᴇ ᴛᴀɢ sᴛᴏᴘ ⇴/histop

๏ /shayari ➛ ʀᴀɴᴅᴏᴍ sʜᴀʏᴀʀɪ ᴛᴀɢ sᴛᴏᴘ ⇴ /shstop

๏ /utag ➛ ᴀɴʏ ᴡʀɪᴛᴛᴇɴ ᴛᴇxᴛ ᴛᴀɢ sᴛᴏᴘ ⇴ /cancel 

๏ /vctag ➛ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ɪɴᴠɪᴛᴇ ᴛᴀɢ sᴛᴏᴘ ⇴ /vcstop
""",
    "help_info": """Iɴꜰᴏ

Iɴꜰᴏ ᴄᴏᴍᴍᴀɴᴅꜱ:

/id : ɢᴇᴛ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ɢʀᴏᴜᴘ ɪᴅ. ɪғ ᴜsᴇᴅ ʙʏ ʀᴇᴘʟʏɪɴɢ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ, ɢᴇᴛs ᴛʜᴀᴛ ᴜsᴇʀ's ɪᴅ.
/info : ɢᴇᴛ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ᴀ ᴜsᴇʀ.
/github <ᴜsᴇʀɴᴀᴍᴇ> : ɢᴇᴛ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ᴀ ɢɪᴛʜᴜʙ ᴜsᴇʀ.
""",
    "help_group": """Gʀᴏᴜᴘ

Gʀᴏᴜᴘ ᴄᴏᴍᴍᴀɴᴅꜱ:

ᴛʜᴇsᴇ ᴀʀᴇ ᴛʜᴇ ᴀᴠᴀɪʟᴀʙʟᴇ ɢʀᴏᴜᴘ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ᴄᴏᴍᴍᴀɴᴅs:

⦿ /pin ➠ ᴘɪɴs ᴀ ᴍᴇssᴀɢᴇ ɪɴ ᴛʜᴇ ɢʀᴏᴜᴘ.
⦿ /pinned ➠ ᴅɪsᴘʟᴀʏs ᴛʜᴇ ᴘɪɴɴᴇᴅ ᴍᴇssᴀɢᴇ ɪɴ ᴛʜᴇ ɢʀᴏᴜᴘ.
⦿ /unpin ➠ ᴜɴᴘɪɴs ᴛʜᴇ ᴄᴜʀʀᴇɴᴛʟʏ ᴘɪɴɴᴇᴅ ᴍᴇssᴀɢᴇ.
⦿ /staff ➠ ᴅɪsᴘʟᴀʏs ᴛʜᴇ ʟɪsᴛ ᴏғ sᴛᴀғғ ᴍᴇᴍʙᴇʀs.
⦿ /bots ➠ ᴅɪsᴘʟᴀʏs ᴛʜᴇ ʟɪsᴛ ᴏғ ʙᴏᴛs ɪɴ ᴛʜᴇ ɢʀᴏᴜᴘ.
⦿ /settitle ➠ sᴇᴛs ᴛʜᴇ ᴛɪᴛʟᴇ ᴏғ ᴛʜᴇ ɢʀᴏᴜᴘ.
⦿ /setdiscription ➠ sᴇᴛs ᴛʜᴇ ᴅᴇsᴄʀɪᴘᴛɪᴏɴ ᴏғ ᴛʜᴇ ɢʀᴏᴜᴘ.
⦿ /setphoto ➠ sᴇᴛs ᴛʜᴇ ɢʀᴏᴜᴘ ᴘʜᴏᴛᴏ.
⦿ /removephoto ➠ ʀᴇᴍᴏᴠᴇs ᴛʜᴇ ɢʀᴏᴜᴘ ᴘʜᴏᴛᴏ.
⦿ /zombies ➠ ʀᴇᴍᴏᴠᴇs ᴀᴄᴄ ᴅᴇʟᴇᴛᴇᴅ ᴍᴇᴍʙᴇʀs ғʀᴏᴍ ᴛʜᴇ ɢʀᴏᴜᴘ.
""",
    "help_action": """Aᴄᴛɪᴏɴ

Aᴄᴛɪᴏɴ ᴄᴏᴍᴍᴀɴᴅꜱ:

» ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅs ꜰᴏʀ Bᴀɴs & Mᴜᴛᴇ :

 ❍ /kickme: kicks the user who issued the command

Admins only:
 ❍ /ban <userhandle>: bans a user. (via handle, or reply)
 ❍ /sban <userhandle>: Silently ban a user. Deletes command, Replied message and doesn't reply. (via handle, or reply)
 ❍ /tban <userhandle> x(m/h/d): bans a user for x time. (via handle, or reply). m = minutes, h = hours, d = days.
 ❍ /unban <userhandle>: unbans a user. (via handle, or reply)
 ❍ /kick <userhandle>: kicks a user out of the group, (via handle, or reply)
 ❍ /mute <userhandle>: silences a user. Can also be used as a reply, muting the replied to user.
 ❍ /tmute <userhandle> x(m/h/d): mutes a user for x time. (via handle, or reply). m = minutes, h = hours, d = days.
 ❍ /unmute <userhandle>: unmutes a user. Can also be used as a reply, muting the replied to user.
__
𝐒ᴘᴇᴄɪᴀʟ 𝐂ᴏᴍᴍᴀɴᴅs 𝐒ᴜᴘᴘᴏʀᴛ 𝐀ʟʟ 𝐄xᴀᴍᴘʟᴇ  - 𝚈𝚞𝚖𝚒 𝚋𝚊𝚗 𝚈𝚞𝚖𝚒 𝚖𝚞𝚝𝚎 𝚈𝚞𝚖𝚒 𝚙𝚛𝚘𝚖𝚘𝚝𝚎 ..... 𝚎𝚝𝚌
""",
    "help_search": """Sᴇᴀʀᴄʜ

Sᴇᴀʀᴄʜ ᴄᴏᴍᴍᴀɴᴅꜱ:

• /google <query> : Search the google for the given query.
• /anime <query>  : Search myanimelist for the given query.
• /stack <query>  : Search stackoverflow for the given query.
• /image (/imgs) <query> : Get the images regarding to your query

Example:
/google pyrogram: return top 5 reuslts.
""",
    "help_font": """ғᴏɴᴛ

ʜᴇʀᴇ ɪs ᴛʜᴇ ʜᴇʟᴘ ғᴏʀ ᴛʜᴇ ғᴏɴᴛ ᴍᴏᴅᴜʟᴇ:

ғᴏɴᴛ ᴍᴏᴅᴜʟᴇ:

ʙʏ ᴜsɪɴɢ ᴛʜɪs ᴍᴏᴅᴜʟᴇ ʏᴏᴜ ᴄᴀɴ ᴄʜᴀɴɢᴇ ғᴏɴᴛs ᴏғ ᴀɴʏ ᴛᴇxᴛ!

◌ /font [ᴛᴇxᴛ]
""",
    "help_game": """ɢᴀᴍᴇs

ʜᴇʀᴇ ɪs ᴛʜᴇ ʜᴇʟᴘ ғᴏʀ ᴛʜᴇ ɢᴀᴍᴇs ᴍᴏᴅᴜʟᴇ:
ɢᴀᴍᴇs ᴍᴏᴅᴜʟᴇ:

ʜᴇʀᴇ ᴀʀᴇ sᴏᴍᴇ ᴍɪɴɪ ɢᴀᴍᴇs ғᴏʀ ʏᴏᴜ ᴛᴏ ᴘʟᴀʏ!

◌ /toss [ᴛᴏss ᴀ ᴄᴏɪɴ]

◌ /roll [ʀᴏʟʟ ᴀ ᴅɪᴄᴇ]

◌ /dart [ᴛʜʀᴏᴡ ᴀ ᴅᴀʀᴛ]

◌ /slot [Jᴀᴄᴋᴘᴏᴛ ᴍᴀᴄʜɪɴᴇ]

◌ /bowling [ʙᴏᴡʟɪɴɢ ɢᴀᴍᴇ]

◌ /basket [ʙᴀsᴋᴇᴛʙᴀʟʟ ɢᴀᴍᴇ]

◌ /football [ғᴏᴏᴛʙᴀʟʟ ɢᴀᴍᴇ]
""",
    "help_tg": """Ⓣ-ɢʀᴀᴘʜ

Ⓣ-ɢʀᴀᴘʜ ᴄᴏᴍᴍᴀɴᴅꜱ:

ᴄʀᴇᴀᴛᴇ ᴀ ᴛᴇʟᴇɢʀᴀᴘʜ ʟɪɴᴋ ᴀɴʏ ᴍᴇᴅɪᴀ!

◌ /tgm [ʀᴇᴘʟʏ ᴛᴏ ᴀɴʏ ᴍᴇᴅɪᴀ]
◌ /tgt [ʀᴇᴘʟʏ ᴛᴏ ᴀɴʏ ᴍᴇᴅɪᴀ]
""",
    "help_imposter": """ɪᴍᴘᴏsᴛᴇʀ

ʜᴇʀᴇ ɪs ᴛʜᴇ ʜᴇʟᴘ ғᴏʀ ᴛʜᴇ ɪᴍᴘᴏsᴛᴇʀ ᴍᴏᴅᴜʟᴇ:

ɪᴍᴘᴏsᴛᴇʀ ᴍᴏᴅᴜʟᴇ:

◌ /imposter on
◌ /imposter off
""",
    "help_td": """Tʀᴜᴛʜ-ᗪᴀʀᴇ

ʜᴇʀᴇ ɪs ᴛʜᴇ ʜᴇʟᴘ ғᴏʀ ᴛʜᴇ Tʀᴜᴛʜ-ᗪᴀʀᴇ ᴍᴏᴅᴜʟᴇ:

ᴛʀᴜᴛʜ ᴀɴᴅ ᴅᴀʀᴇ
◌ /truth : sᴇɴᴅs ᴀ ʀᴀɴᴅᴏᴍ ᴛʀᴜᴛʜ sᴛʀɪɴɢ.
◌ /dare : sᴇɴᴅs ᴀ ʀᴀɴᴅᴏᴍ ᴅᴀʀᴇ sᴛʀɪɴɢ.
""",
    "help_q": """ǫᴜᴏᴛʏ

ʜᴇʀᴇ ɪs ᴛʜᴇ ʜᴇʟᴘ ғᴏʀ ᴛʜᴇ ǫᴜᴏᴛʟʏ ᴍᴏᴅᴜʟᴇ:

◌ /q : ᴄʀᴇᴀᴛᴇs ᴀ ǫᴜᴏᴛᴇ ғʀᴏᴍ ᴛʜᴇ ᴍᴇssᴀɢᴇ

◌ /q r : ᴄʀᴇᴀᴛᴇs ᴀ ǫᴜᴏᴛᴇ ғʀᴏᴍ ᴛʜᴇ ᴍᴇssᴀɢᴇ ᴡɪᴛʜ ʀᴇᴘʟʏ
""",
    "help_tts": """ᴛᴛs

ʜᴇʀᴇ ɪs ᴛʜᴇ ʜᴇʟᴘ ғᴏʀ ᴛʜᴇ ᴛᴛs ᴍᴏᴅᴜʟᴇ:

❀ ᴛᴛs
◌ /tts : [ᴛᴇxᴛ]

◌ ᴜsᴀɢᴇ ➛ ᴛᴇxᴛ ᴛᴏ ᴀᴜᴅɪᴏ
""",
    "help_fun": """ғᴜɴ

ʜᴇʀᴇ ɪs ᴛʜᴇ ʜᴇʟᴘ ғᴏʀ ᴛʜᴇ ғᴜɴ ᴍᴏᴅᴜʟᴇ:
ᴡɪsʜ ᴍᴏᴅᴜʟᴇ:

◌ /wish : ᴀᴅᴅ ʏᴏᴜʀ ᴡɪsʜ ᴀɴᴅ sᴇᴇ ɪᴛs ᴘᴏssɪʙɪʟɪᴛʏ!

ᴍᴏʀᴇ sᴛᴜғғ:
◌ /sigma [ᴄʜᴇᴄᴋ ʏᴏᴜʀ sɪɢᴍᴀɴᴇss]
◌ /cute [ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴄᴜᴛᴇɴᴇss]
◌ /horny [ᴄʜᴇᴄᴋ ʏᴏᴜʀ ʜᴏʀɴʏɴᴇss]
◌ /lesbo [ᴄʜᴇᴄᴋ ʜᴏᴡ ᴍᴜᴄʜ ʟᴇᴢʙɪᴀɴ ʏᴏᴜ ᴀʀᴇ]
◌ /depressed [ᴄʜᴇᴄᴋ ʜᴏᴡ ᴍᴜᴄʜ ᴅᴇᴘʀᴇssᴇᴅ ʏᴏᴜ ᴀʀᴇ]
◌ /gay [ᴄʜᴇᴄᴋ ʜᴏᴡ ᴍᴜᴄʜ ɢᴀʏ ʏᴏᴜ ᴀʀᴇ]
◌ /rand [ᴄʜᴇᴄᴋ ʜᴏᴡ ᴍᴜᴄʜ ʀᴀɴᴅ ʏᴏᴜ ᴀʀᴇ]
◌ /bkl [ᴄʜᴇᴄᴋ ʜᴏᴡ ᴍᴜᴄʜ ʙᴋʟ ʏᴏᴜ ᴀʀᴇ]
◌ /boobs [ᴄʜᴇᴄᴋ ʏᴏᴜʀ ʙᴏᴏʙɪᴇs sɪᴢᴇ]
◌ /dick [ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴅɪᴄᴋ sɪᴢᴇ]
"""
}

@app.on_callback_query(filters.regex(r"^help_(chatgpt|sticker|tagall|info|group|action|search|font|game|tg|imposter|td|q|tts|fun)$"))
async def show_extra_command_help(client, query: CallbackQuery):
    time.sleep(0.5)
    command = query.data
    help_text = EXTRA_HELP_TEXTS.get(command, "No help available for this command.")
    
    buttons = [[InlineKeyboardButton("⬅ Back", callback_data="help_extra")]]
    
    await query.message.edit_text(f"**{command.capitalize()} Help:**\n\n{help_text}", reply_markup=InlineKeyboardMarkup(buttons))


@app.on_callback_query(filters.regex("^host$"))
async def show_management_help_menu(client, query: CallbackQuery):
    time.sleep(0.5)
    
    buttons = [
        [InlineKeyboardButton("⬅ Back", callback_data="back_to_home")]
    ]

    await query.message.edit_text(
        """✨ Bᴏᴛ Hᴏsᴛɪɴɢ Aᴠᴀɪʟᴀʙʟᴇ!

➡️Wᴀɪғᴜ – ₹𝟻𝟶𝟶/ᴍᴏɴᴛʜ 
➡️Mᴜsɪᴄ – ₹𝟸𝟶𝟶/ᴍᴏɴᴛʜ 
➡️Fɪʟᴇ Sʜᴀʀᴇ – ₹𝟷𝟶𝟶/ᴍᴏɴᴛʜ 
➡️Fɪʟᴇ Rᴇɴᴀᴍᴇ – ₹𝟷𝟶𝟶/ᴍᴏɴᴛʜ 
➡️Mᴀɴᴀɢᴇᴍᴇɴᴛ – ₹𝟽𝟻𝟶/ᴍᴏɴᴛʜ
➡️Mᴜsɪᴄ + 𝟹𝟻% Mᴀɴᴀɢᴇᴍᴇɴᴛ – ₹𝟹𝟻𝟶/ᴍᴏɴᴛʜ

➡️Sᴘᴀᴍ Bᴏᴛ – ₹𝟷𝟶𝟶/ᴍᴏɴᴛʜ
➡️Cʜᴀᴛ Bᴏᴛ – ₹𝟷𝟶𝟶/ᴍᴏɴᴛʜ

➡️AI Bᴏᴛ – (Cᴏᴍɪɴɢ Sᴏᴏɴ)

➡️Usᴇʀʙᴏᴛ - (Cᴏᴍɪɴɢ Sᴏᴏɴ)
➡️Usᴇʀ Cʜᴀᴛ Bᴏᴛ - (Cᴏᴍɪɴɢ Sᴏᴏɴ)

🌐 𝟸𝟺/𝟽 Sᴜᴘᴘᴏʀᴛ
❤️DM - @Sukuna_dev
❤️DM - @xeno_kakarot""",
       reply_markup=InlineKeyboardMarkup(buttons)
    )


@app.on_callback_query(filters.regex("^help_management$"))
async def show_management_help_menu(client, query: CallbackQuery):
    time.sleep(0.5)
    buttons = [
        [InlineKeyboardButton("Ban", callback_data="mhelp_ban"),
         InlineKeyboardButton("Approve", callback_data="mhelp_approve"),
         InlineKeyboardButton("Admin", callback_data="mhelp_admin")],
        [InlineKeyboardButton("Warn", callback_data="mhelp_warn"),
         InlineKeyboardButton("Filters", callback_data="mhelp_filters"),
         InlineKeyboardButton("Report", callback_data="mhelp_report")],
        [InlineKeyboardButton("Rules", callback_data="mhelp_rules"),
         InlineKeyboardButton("⬅ Back", callback_data="open_help")]
    ]

    await query.message.edit_text(
        "Select a management command to get help.",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# 🔹 Individual Management Command Help Handlers
MANAGEMENT_HELP_TEXTS = {
    "mhelp_ban": """» ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅs ꜰᴏʀ 𝗕𝗔𝗡 :

⚠️ Bans

Admin only:
➥ /kick: Kick the user replied or tagged.
➥ /skick: Kick the user replied or tagged and delete your message.
➥ /dkick: Kick the user replied and delete their message.
➥ /ban: Bans the user replied to or tagged.
➥ /sban: Bans the user replied or tagged and delete your message.
➥ /dban: Bans the user replied and delete their message.
➥ /tban x(m/h/d): Bans a user for x time. (via handle, or reply). m = minutes, h = hours, d = days.
➥ /stban x(m/h/d): Silently bans a user for x time. (via handle, or reply). m = minutes, h = hours, d = days.
➥ /dtban x(m/h/d): Silently bans a user for x time and delete the replied message. (via reply). m = minutes, h = hours, d = days.
➥ /unban: Unbans the user replied to or tagged.

Disable kickme by this command:
➥ /kickme off

Example:
/ban @username: this bans a user in the chat.
""",
    "mhelp_approve": """» ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅs ꜰᴏʀ 𝗔𝗣𝗣𝗥𝗢𝗩𝗘 :

✅ Approve

Admin commands:
➥ /approval: Check a user's approval status in this chat.
➥ /approve: Approve of a user. Locks, blacklists, and antiflood won't apply to them anymore.
➥ /unapprove: Unapprove of a user. They will now be subject to blocklists.
➥ /approved: List all approved users.
➥ /unapproveall: Unapprove *ALL* users in a chat. This cannot be undone!

Example:
/approve @username: this approves a user in the chat.
""",
    "mhelp_admin": """» ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅs ꜰᴏʀ 𝗔𝗗𝗠𝗜𝗡 :

👮 Admin

User Commands:
➥ /adminlist: List all the admins in the Group.

Admin only:
➥ /invitelink: Gets chat invitelink.
➥ /promote: Promotes the user replied to or tagged (supports with title).
➥ /fullpromote: Fully Promotes the user replied to or tagged (supports with title).
➥ /demote: Demotes the user replied to or tagged.
➥ /setgpic: Set group picture.
➥ /admincache: Reloads the List of all the admins in the Group.
➥ /zombies: Bans all the deleted accounts. (owner only)
➥ /title: sets a custom title for an admin that the bot promoted.
➥ /enable: Allow users from using "commandname" in this group.
➥ /disabledel: Delete disabled commands when used by non-admins.
➥ /enableall: enable all disabled commands.

Example:
/promote @username: this promotes a user to admin.
""",
    "mhelp_warn": """**🚫 Warns**

**Admin commands:**
➥ /warn `<reason>`: Warn a user.
➥ /dwarn `<reason>`: Warn a user by reply, and delete their message.
➥ /swarn `<reason>`: Silently warn a user, and delete your message.
➥ /warns: See a user's warnings.
➥ /rmwarn: Remove a user's latest warning.
➥ /resetwarn: Reset all of a user's warnings to 0.
➥ /warnings: Get the chat's warning settings.
➥ /warnmode `<ban/kick/mute>`: Set the chat's warn mode.
➥ /warnlimit `<number>`: Set the number of warnings before users are punished.

**Examples:**
`/warn @user`: this warns a user in the chat.
""",
    "mhelp_filters": """**💠 Filters**

➥ /filters: List all active filters saved in the chat.

**Admin only:**
➥ /filter "`<keyword>`" `<reply message>`: Add a filter to this chat. The bot will now reply that message whenever 'keyword'
is mentioned. If you reply to a sticker with a keyword, the bot will reply with that sticker.
If you want your keyword to be a sentence, use quotes. eg: /filter "hey there" How are you doin?
**Example:**
`/filter "filtername" Reply Text`
Aliases for filters can be too set, just put '|' between the filternames you want.
**Example:**
`/filter "filtername1|filtername2" Reply Text`
Using the you can make a single filter work on 2 filternames without manually adding another one.
➥ /stop `<filter keyword>`: Stop that filter.
**Note:**
For filters with aliases, if you stop one alias, the filter will stop working on other aliases too.
**For Example:**
If you stop the "filtername1" from above example, the bot will not respond to "filtername2".
**Chat creator only:**
➥ /removeallfilters: Remove all chat filters at once.
**Note:**
Currently there is a limit of 50 filters and 120 aliases per chat.
All filter keywords are in lowercase.
""",
    "mhelp_report": """**🚸 Report**

➥ /report `<reason>`: reply to a message to report it to admins.
× @admin: reply to a message to report it to admins.

**NOTE:** Neither of these will get triggered if used by admins.

**Admins Only:**
➥ /reports `<on/off/yes/no>`: change report setting, or view current status.
    ‣ If done in PM, toggles your status.
    ‣ If in group, toggles that group's status.
""",
    "mhelp_rules": """**📕 Rules**

**Set rules for your chat so that members know what to do and what not to do in your group!**

➥ /rules: get the rules for current chat.

**Admin only:**
➥ /setrules `<rules message>`: Set the rules for this chat, also works as a reply to a message.
➥ /clearrules: Clear the rules for this chat.
➥ /privaterules , /pmrules `<on/yes/no/off>`: Turns on/off the option to send the rules to PM of user or group.

**Note Format**
    Check /markdownhelp for help related to formatting!
"""
}


HELP_GAME = {

    "Ghelp_bet": """🎲 **Bet Command Help** 🎲

Use this command to place a bet on a dice roll!  

📝 **Usage:**  
`/bet <amount> <E/O>`  

📌 **Parameters:**  
- `<amount>`: The number of Berries you want to bet.  
- `<E/O>`: Choose `E` for Even or `O` for Odd.  

📢 **Rules:**  
✅ Minimum bet must be **7% of your balance** (or at least 1 Berry).  
✅ If you win, you **double** your bet amount!  
❌ If you lose, you lose the amount you bet.  

🎲 **Example:**  
`/bet 50 E` → Bets 50 Berries that the dice roll will be Even.  

Good luck! 🍀
""",
    "Ghelp_jackpot": """🎰 **Jackpot Command Help** 🎰  

Try your luck in the jackpot game and win coins! 💰  

📝 **Usage:**  
`/jackpot`  

📌 **Rules:**  
- 🎰 Roll the slot machine to get a random score.  
- 🎯 Your reward is **5x your dice score** in coins!  
- 🎲 **Jackpot!** If you roll **64**, you win **2000 coins**! 🎉  
- ⏳ **Play Limit:** You can play only **once per day**.  

🎲 **Example:**  
User types `/jackpot` → Rolls 🎰 → Wins **5 × dice score** coins!  

Give it a spin and test your luck! 🍀🔥  
""",
    "Ghelp_guess": """📝 **Guess The Character Game - Help Guide** 🎮  

📌 **How to Play?**  
1️⃣ Use `/nguess` in the group to start a new game.  
2️⃣ A character image will be sent, and you have **5 minutes** to guess their name.  
3️⃣ Send your guess in the chat. If correct, you earn **20 coins**! 💰  

🏆 **Streak Rewards**  
🔥 Keep guessing correctly to build a streak!  
- **50 Streak:** +1000 Coins  
- **100 Streak:** +2000 Coins  

🕒 **Cooldown & Limits**  
- You can guess up to **100 times** before a **4-hour cooldown** starts.  
- If you don't guess in **48 hours**, a new character will be sent.  

⚠️ **Important**  
- This game is only available in our official group: [Join Here](https://t.me/TEAMZYRO).  
- Commands won't work in other groups.  

✨ **Enjoy the game and keep guessing!** 🎉  
"""
}

# 🔹 Mini Game Help Menu
@app.on_callback_query(filters.regex("^help_minigame$"))
async def show_minigame_help_menu(client, query: CallbackQuery):
    time.sleep(1)
    buttons = [
        [InlineKeyboardButton("Bᴇᴛ", callback_data="Ghelp_bet"),
         InlineKeyboardButton("Jᴀᴄᴋᴘᴏᴛ", callback_data="Ghelp_jackpot"),
         InlineKeyboardButton("Nɢᴜᴇss", callback_data="Ghelp_guess")],
        [InlineKeyboardButton("⬅ Back", callback_data="open_help")]
    ]

    await query.message.edit_text(
        "Select a mini-game command to get help.",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@app.on_callback_query(filters.regex(r"^Ghelp_(bet|jackpot|guess)$"))
async def show_minigame_command_help(client, query: CallbackQuery):
    time.sleep(0.5)
    command = query.data
    help_text = HELP_GAME.get(command, "No help available for this command.")
    
    buttons = [[InlineKeyboardButton("⬅ Back", callback_data="help_minigame")]]
    
    await query.message.edit_text(f"**{command.capitalize()} Help:**\n\n{help_text}", reply_markup=InlineKeyboardMarkup(buttons))


@app.on_callback_query(filters.regex(r"^mhelp_(ban|approve|admin|warn|filters|report|rules)$"))
async def show_management_command_help(client, query: CallbackQuery):
    time.sleep(0.5)
    command = query.data
    help_text = MANAGEMENT_HELP_TEXTS.get(command, "No help available for this command.")
    
    buttons = [[InlineKeyboardButton("⬅ Back", callback_data="help_management")]]
    
    await query.message.edit_text(f"**{command.capitalize()} Help:**\n\n{help_text}", reply_markup=InlineKeyboardMarkup(buttons))
