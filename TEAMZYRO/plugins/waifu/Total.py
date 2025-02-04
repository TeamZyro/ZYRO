import urllib.request
from pymongo import ReturnDocument
import os
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from TEAMZYRO import application
from TEAMZYRO.database import collection, user_collection
from gridfs import GridFS 
from io import BytesIO


async def check_total_characters(update: Update, context: CallbackContext) -> None:
    try:
        total_characters = await collection.count_documents({})
        
        await update.message.reply_text(f"Total number of characters: {total_characters}")
    except Exception as e:
        await update.message.reply_text(f"Error occurred: {e}")


application.add_handler(CommandHandler("total", check_total_characters))
