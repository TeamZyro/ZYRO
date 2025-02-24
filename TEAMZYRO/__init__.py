from TEAMZYRO.core.bot import ZYRO
from TEAMZYRO.core.dir import dirr
from TEAMZYRO.core.git import git
from TEAMZYRO.core.waifu_databese import *
from TEAMZYRO.core.userbot import Userbot
from TEAMZYRO.misc import dbb, heroku
from pyrogram import Client
from SafoneAPI import SafoneAPI
from .logging import LOGGER
from TEAMZYRO.core.application import application

dirr()
git()
dbb()
heroku()

app = ZYRO()
api = SafoneAPI()
userbot = Userbot()
application = application

from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()

#--------------------------- STRIN ---------------------------------------

locks = {}
message_counters = {}
spam_counters = {}
last_characters = {}
sent_characters = {}
first_correct_guesses = {}
message_counts = {}
last_user = {}
warned_users = {}
user_cooldowns = {}
user_nguess_progress = {}
user_guess_progress = {}

# -------------------------- POWER SETUP --------------------------------
from TEAMZYRO.plugins.waifu.unit.zyro_ban import *
from TEAMZYRO.plugins.waifu.unit.zyro_sudo import *
from TEAMZYRO.plugins.waifu.unit.zyro_react import *
from TEAMZYRO.plugins.waifu.unit.zyro_send_img import *
from TEAMZYRO.plugins.waifu.unit.zyro_guess import *
from TEAMZYRO.plugins.waifu.unit.zyro_rarity import *
