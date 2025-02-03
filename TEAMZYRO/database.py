from motor.motor_asyncio import AsyncIOMotorClient
import config
#----------------------------------------#
#----------------------------------------#
zyro = AsyncIOMotorClient(config.MONGO_DB_URI)
#----------------------------------------#
#----------------------------------------#
db = zyro['gaming_create']
user_totals_collection = db['gaming_totals']
group_user_totals_collection = db['gaming_group_total']
top_global_groups_collection = db['gaming_global_groups']
pm_users = db['gaming_pm_users']
user_collection = db['gamimg_user_collection']
collection = db['gaming_anime_characters']
#----------------------------------------#
