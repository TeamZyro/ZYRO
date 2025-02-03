from TEAMZYRO.core.bot import ZYRO
from TEAMZYRO.core.dir import dirr
from TEAMZYRO.core.git import git
from TEAMZYRO.core.userbot import Userbot
from TEAMZYRO.misc import dbb, heroku
from pyrogram import Client
from SafoneAPI import SafoneAPI
from .logging import LOGGER

dirr()
git()
dbb()
heroku()

app = ZYRO()
api = SafoneAPI()
userbot = Userbot()

from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()
