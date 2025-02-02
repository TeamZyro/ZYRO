from ZYROTEAM.core.bot import ZYRO
from ZYROTEAM.core.dir import dirr
from ZYROTEAM.core.git import git
from ZYROTEAM.core.userbot import Userbot
from ZYROTEAM.misc import dbb, heroku
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
