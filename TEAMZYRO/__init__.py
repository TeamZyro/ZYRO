from TEAMZYRO.core.bot import ZYRO
from TEAMZYRO.core.dir import dirr
from TEAMZYRO.core.git import git
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

from motor.motor_asyncio import AsyncIOMotorClient

MONGO_DB_URI = "mongodb+srv://bikash:bikash@bikash.3jkvhp7.mongodb.net/?retryWrites=true&w=majority"

zyro = AsyncIOMotorClient(MONGO_DB_URI)
db = zyro['waifu_collector_bot']
collection = db['anime_characters_lol']
user_totals_collection = db['user_totals_lmaoooo']
user_collection = db["user_collection_lmaoooo"]
group_user_totals_collection = db['group_user_totalsssssss']
top_global_groups_collection = db['top_global_groups']
pm_users = db['total_pm_users']
