from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
# MongoDB connection
client = MongoClient(os.getenv("MONGO_URI"))
db = client["ubakahub"]
def get_user_collection():
    return db["users"]
def get_interest_collection():
    return db["interest_signups"]