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
