from typing import Any, Dict, List, Union
from pymongo import MongoClient
from config import MONGO_DB_URI

# MongoDB Connection
my_client = MongoClient(MONGO_DB_URI)
my_db = my_client["aki-db"]
karma_collection = my_db["karma"]
users_collection = my_db["users"]
settings_collection = my_db["settings"]

# ID Conversion Functions
async def int_to_alpha(user_id: int) -> str:
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    return "".join(alphabet[int(i)] for i in str(user_id))

async def alpha_to_int(user_id_alphabet: str) -> int:
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    return int("".join(str(alphabet.index(i)) for i in user_id_alphabet))

# Karma Functions
async def get_karmas_count() -> dict:
    chats = karma_collection.find({"chat_id": {"$lt": 0}})
    chats_count = 0
    karmas_count = 0
    async for chat in chats:
        for i in chat.get("karma", {}):
            karma_ = chat["karma"][i]["karma"]
            if karma_ > 0:
                karmas_count += karma_
        chats_count += 1
    return {"chats_count": chats_count, "karmas_count": karmas_count}

async def user_global_karma(user_id: int) -> int:
    chats = karma_collection.find({"chat_id": {"$lt": 0}})
    total_karma = 0
    async for chat in chats:
        karma = await get_karma(chat["chat_id"], await int_to_alpha(user_id))
        if karma and karma.get("karma", 0) > 0:
            total_karma += karma["karma"]
    return total_karma

async def get_karmas(chat_id: int) -> Dict[str, int]:
    karma_data = karma_collection.find_one({"chat_id": chat_id})
    return karma_data.get("karma", {}) if karma_data else {}

async def get_karma(chat_id: int, name: str) -> Union[bool, dict]:
    name = name.lower().strip()
    karmas = await get_karmas(chat_id)
    return karmas.get(name, False)

async def update_karma(chat_id: int, name: str, karma: dict):
    name = name.lower().strip()
    karmas = await get_karmas(chat_id)
    karmas[name] = karma
    karma_collection.update_one({"chat_id": chat_id}, {"$set": {"karma": karmas}}, upsert=True)

async def is_karma_on(chat_id: int) -> bool:
    chat = settings_collection.find_one({"chat_id_toggle": chat_id})
    return not chat  # If not found, default to True (karma is on)

async def karma_on(chat_id: int):
    if not await is_karma_on(chat_id):
        settings_collection.delete_one({"chat_id_toggle": chat_id})

async def karma_off(chat_id: int):
    if await is_karma_on(chat_id):
        settings_collection.insert_one({"chat_id_toggle": chat_id})

# User Management Functions
def addUser(user_id: int, first_name: str, last_name: str, user_name: str) -> None:
    user = users_collection.find_one({"user_id": user_id})
    if user is None:
        users_collection.insert_one({
            "user_id": user_id,
            "first_name": first_name,
            "last_name": last_name,
            "user_name": user_name,
            "aki_lang": "en",
            "child_mode": 1,
            "total_guess": 0,
            "correct_guess": 0,
            "wrong_guess": 0,
            "unfinished_guess": 0,
            "total_questions": 0,
        })
    else:
        updateUser(user_id, first_name, last_name, user_name)

def totalUsers() -> int:
    return users_collection.count_documents({})

def updateUser(user_id: int, first_name: str, last_name: str, user_name: str) -> None:
    users_collection.update_one(
        {"user_id": user_id},
        {"$set": {"user_name": user_name, "first_name": first_name, "last_name": last_name}}
    )

def getUser(user_id: int) -> Any:
    return users_collection.find_one({"user_id": user_id})

def getChildMode(user_id: int) -> int:
    user = users_collection.find_one({"user_id": user_id})
    return user.get("child_mode", 1) if user else 1

def getTotalGuess(user_id: int) -> int:
    user = users_collection.find_one({"user_id": user_id})
    return user.get("total_guess", 0) if user else 0

def getCorrectGuess(user_id: int) -> int:
    user = users_collection.find_one({"user_id": user_id})
    return user.get("correct_guess", 0) if user else 0

def getWrongGuess(user_id: int) -> int:
    user = users_collection.find_one({"user_id": user_id})
    return user.get("wrong_guess", 0) if user else 0

def getUnfinishedGuess(user_id: int) -> int:
    correct_wrong_guess = getCorrectGuess(user_id) + getWrongGuess(user_id)
    unfinished_guess = getTotalGuess(user_id) - correct_wrong_guess
    users_collection.update_one({"user_id": user_id}, {"$set": {"unfinished_guess": unfinished_guess}})
    return unfinished_guess

def getTotalQuestions(user_id: int) -> int:
    user = users_collection.find_one({"user_id": user_id})
    return user.get("total_questions", 0) if user else 0

def updateChildMode(user_id: int, mode: int) -> None:
    users_collection.update_one({"user_id": user_id}, {"$set": {"child_mode": mode}})

def updateTotalGuess(user_id: int, total_guess: int) -> None:
    total_guess += getTotalGuess(user_id)
    users_collection.update_one({"user_id": user_id}, {"$set": {"total_guess": total_guess}})

def updateCorrectGuess(user_id: int, correct_guess: int) -> None:
    correct_guess += getCorrectGuess(user_id)
    users_collection.update_one({"user_id": user_id}, {"$set": {"correct_guess": correct_guess}})

def updateWrongGuess(user_id: int, wrong_guess: int) -> None:
    wrong_guess += getWrongGuess(user_id)
    users_collection.update_one({"user_id": user_id}, {"$set": {"wrong_guess": wrong_guess}})

def updateTotalQuestions(user_id: int, total_questions: int) -> None:
    total_questions += getTotalQuestions(user_id)
    users_collection.update_one({"user_id": user_id}, {"$set": {"total_questions": total_questions}})

# Leaderboard Functions
def getLead(field: str) -> list:
    leaderboard = {}
    for user in users_collection.find({}):
        leaderboard[user["first_name"]] = user.get(field, 0)
    sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)
    return sorted_leaderboard[:10]
