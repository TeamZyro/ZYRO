import re
from os import getenv
# ------------------------------------
# ------------------------------------
from dotenv import load_dotenv
from pyrogram import filters
# ------------------------------------
# ------------------------------------
load_dotenv()
# ------------------------------------
# -----------------------------------------------------
API_ID = getenv("API_ID", "25981592")
API_HASH = getenv("API_HASH", "709f3c9d34d83873d3c7e76cdd75b866")

EVAL = list(map(int, getenv("EVAL", "7638720582 7638720582").split()))
# ------------------------------------------------------
BOT_TOKEN = getenv("BOT_TOKEN", "7726309603:AAHB-pi4qBg7Gj57kivENYPILQWNVCURvn4")
# -------------------------------------------------------
OWNER_USERNAME = getenv("OWNER_USERNAME","xeno_kakarot")
# --------------------------------------------------------
BOT_USERNAME = getenv("BOT_USERNAME" , "Oneforall_rebot")
# --------------------------------------------------------
BOT_NAME = getenv("BOT_NAME" , "TeamZyro")
# ---------------------------------------------------------
ASSUSERNAME = getenv("ASSUSERNAME" , "TeamZyro")
# ---------------------------------------------------------


#---------------------------------------------------------------
#---------------------------------------------------------------
MONGO_DB_URI = getenv("MONGO_DB_URI", "mongodb+srv://bikash:bikash@bikash.3jkvhp7.mongodb.net/?retryWrites=true&w=majority")
DB_NAME = getenv("DB_NAME", "Zyro")
#---------------------------------------------------------------
#---------------------------------------------------------------

# ----------------------------------------------------------------
DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 17000))
# ----------------------------------------------------------------

# ----------------------------------------------------------------
LOGGER_ID = int(getenv("LOGGER_ID", -1002009280180))
CHARA_CHANNEL_ID = getenv("CHARA_CHANNEL_ID", "-1002051009747")
# ----------------------------------------------------------------
# ----------------------------------------------------------------
OWNER_ID = int(getenv("OWNER_ID", 7078181502))
# -----------------------------------------------------------------
# -----------------------------------------------------------------
# ----------------------------------------------------------------
# ----------------------------------------------------------------
# ----------------------------------------------------------------
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
# ----------------------------------------------------------------
HEROKU_API_KEY = getenv("HEROKU_API_KEY")
# ----------------------------------------------------------------
# ----------------------------------------------------------------
# ----------------------------------------------------------------
UPSTREAM_REPO = getenv(
    "UPSTREAM_REPO",
    "https://github.com/ZYROTEAM/TEAMZYRO",
)
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "Master")
GIT_TOKEN = getenv(
    "GIT_TOKEN", None
)  # ----------------------------------------------------------------
# -------------------------------------------------------------------
# --------------------------------------------------------------------
# --------------------------------------------------------------------



# ------------------------------------------------------------------------
# -------------------------------------------------------------------------
SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/Gaming_World_Update")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/ZyropiratesMainchat")
# ------------------------------------------------------------------------------
# -------------------------------------------------------------------------------







# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------
AUTO_LEAVING_ASSISTANT = getenv("AUTO_LEAVING_ASSISTANT", "True")
AUTO_LEAVE_ASSISTANT_TIME = int(getenv("ASSISTANT_LEAVE_TIME", "9000"))
SONG_DOWNLOAD_DURATION = int(getenv("SONG_DOWNLOAD_DURATION", "9999999"))
SONG_DOWNLOAD_DURATION_LIMIT = int(getenv("SONG_DOWNLOAD_DURATION_LIMIT", "9999999"))
# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", "1c21247d714244ddbb09925dac565aed")
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", "709e1a2969664491b58200860623ef19")
# ----------------------------------------------------------------------------------




# -----------------------------------------------------------------------------------
PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", 25))
# ------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------
TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", "5242880000"))
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", "5242880000"))
# --------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------



# ------------------------------------
# ------------------------------------
# ------------------------------------
# ------------------------------------
STRING1 = getenv("STRING_SESSION", "BQFa2kUAll-nw73HVWcVQhzVqNURFzbDCKSMzkqtGUxIGVonds-cbnolPt84RmV9HnGzMbuvTCo0020l1YF_UTR7B4LNfzXs_dNWAx1AM772nn_ntFGCF24WFl91YoX5TsIjJXhmna65Od5sn8YvUkeA6wZS8ljefhZzyyVnLzHCUTjSy8PM8XR0aIpWqRA1vtZwF3YcuHpGH-rvMVNzCQWKE5Bu3fL_f-fdttVWzkjxGar29FZlLiESAaVFNlYNERq_nSuOwq10QeX90rKDeMpV71R984VZu9SbQ9wgwAOsre5Bgm4CSlDXG4bdn5XVU2nP7YNCsYaLWsrEZ_E2jA3AMze_uwAAAAHYrNprAA")
STRING2 = getenv("STRING_SESSION2", None)
STRING3 = getenv("STRING_SESSION3", None)
STRING4 = getenv("STRING_SESSION4", None)
STRING5 = getenv("STRING_SESSION5", None)
STRING6 = getenv("STRING_SESSION6", None)
STRING7 = getenv("STRING_SESSION7", None)
BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}

# ------------------------------------
# ------------------------------------
# ------------------------------------
# ------------------------------------

# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
START_IMG_URL = getenv(
    "START_IMG_URL", "https://files.catbox.moe/bct8lb.jpg"
)
PING_IMG_URL = getenv(
    "PING_IMG_URL", "https://files.catbox.moe/bct8lb.jpg"
)
PLAYLIST_IMG_URL = "https://files.catbox.moe/bct8lb.jpg"
STATS_IMG_URL = "https://files.catbox.moe/bct8lb.jpg"
TELEGRAM_AUDIO_URL = "https://files.catbox.moe/bct8lb.jpg"
TELEGRAM_VIDEO_URL = "https://files.catbox.moe/bct8lb.jpg"
STREAM_IMG_URL = "https://files.catbox.moe/bct8lb.jpg"
SOUNCLOUD_IMG_URL = "https://files.catbox.moe/bct8lb.jpg"
YOUTUBE_IMG_URL = "https://files.catbox.moe/bct8lb.jpg"
SPOTIFY_ARTIST_IMG_URL = "https://files.catbox.moe/bct8lb.jpg"
SPOTIFY_ALBUM_IMG_URL = "https://files.catbox.moe/bct8lb.jpg"
SPOTIFY_PLAYLIST_IMG_URL = "https://files.catbox.moe/bct8lb.jpg"

# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))


DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# ------------------------------------------------------------------------------
if SUPPORT_CHANNEL:
    if not re.match("(?:http|https)://", SUPPORT_CHANNEL):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHANNEL url is wrong. Please ensure that it starts with https://"
        )

if SUPPORT_CHAT:
    if not re.match("(?:http|https)://", SUPPORT_CHAT):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHAT url is wrong. Please ensure that it starts with https://"
        )
# ---------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------
