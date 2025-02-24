import asyncio
import importlib

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from TEAMZYRO import LOGGER, app, userbot
from TEAMZYRO.core.call import ZYRO
from TEAMZYRO.core.application import application
from TEAMZYRO.misc import sudo
from TEAMZYRO.plugins import ALL_MODULES
from TEAMZYRO.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS

async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("String session not filled, please fill a Pyrogram session")
        exit()

    await sudo()
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass

    # Start Pyrogram bot
    await app.start()
    
    # Start Pyrogram userbot
    await userbot.start()
    
    # Start PyTgCalls
    await ZYRO.start()

    # Start Telegram bot using python-telegram-bot
    # async def run_application():
    #     await application.initialize()
    #     await application.start()
    #     await application.updater.start_polling()
    
    # asyncio.create_task(run_application())

    try:
        await ZYRO.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("DAXXMUSIC").error(
            "Please start your log group voice chat/channel\n\nDAXX BOT STOPPING..."
        )
        exit()
    except:
        pass

    await ZYRO.decorators()
    LOGGER("DAXXMUSIC").info(
        "╔═════ஜ۩۞۩ஜ════╗\n  ☠︎︎ MADE BY MR DAXX ☠︎︎\n╚═════ஜ۩۞۩ஜ════╝"
    )
    
    await idle()

    # Stop all services before exit
    await app.stop()
    await userbot.stop()
    await application.stop()
    LOGGER("DAXXMUSIC").info("Stopped DAXX Music Bot..")



if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
