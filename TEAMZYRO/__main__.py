import asyncio
import importlib
from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall
import config
from TEAMZYRO import LOGGER, app, userbot
from TEAMZYRO.core.call import ZYRO
from TEAMZYRO.misc import sudo
from TEAMZYRO.plugins import ALL_MODULES
from TEAMZYRO.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS
from TEAMZYRO.core.application import application

async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("𝐒𝐭𝐫𝐢𝐧𝐠 𝐒𝐞𝐬𝐬𝐢𝐨𝐧 𝐍𝐨𝐭 𝐅𝐢𝐥𝐥𝐞𝐝, 𝐏𝐥𝐞𝐚𝐬𝐞 𝐅𝐢𝐥𝐥 𝐀 𝐏𝐲𝐫𝐨𝐠𝐫𝐚𝐦 𝐒𝐞𝐬𝐬𝐢𝐨𝐧")
        exit()
    await sudo()
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except Exception as e:
        LOGGER(__name__).error(f"Error loading banned users: {e}")
    
    await app.start()
    for all_module in ALL_MODULES:
        importlib.import_module("TEAMZYRO.plugins" + all_module)
    LOGGER("TEAMZYRO.plugins").info("𝐀𝐥𝐥 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬 𝐋𝐨𝐚𝐝𝐞𝐝 𝐁𝐚𝐛𝐲🥳...")
    await userbot.start()
    await ZYRO.start()
    
    try:
        await ZYRO.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("TEAMZYRO").error("𝗣𝗹𝗭 𝗦𝗧𝗔𝗥𝗧 𝗬𝗢𝗨𝗥 𝗟𝗢𝗚 𝗚𝗥𝗢𝗨𝗣 𝗩𝗢𝗜𝗖𝗘𝗖𝗛𝗔𝗧\𝗖𝗛𝗔𝗡𝗡𝗘𝗟")
        exit()
    except Exception as e:
        LOGGER("TEAMZYRO").error(f"Error starting stream call: {e}")
    
    await ZYRO.decorators()
    await application.run_polling(drop_pending_updates=True)
    await idle()
    
    await app.stop()
    await userbot.stop()
    LOGGER("TEAMZYRO").info("𝗦𝗧𝗢𝗣 𝗧𝗘𝗔𝗠𝗭𝗬𝗥𝗢 𝗕𝗢𝗧..")

async def main():
    await init()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except Exception as e:
        LOGGER(__name__).error(f"Error in main loop: {e}")
    finally:
        loop.close()
