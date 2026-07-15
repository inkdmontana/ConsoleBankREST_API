import os

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("MONGODB_DATABASE")

client = None
database = None


def get_database():
    global client, database

    if database is not None:
        return database

    try:
        client = MongoClient(MONGODB_URI)
        client.admin.command("ping")

        database = client[DATABASE_NAME]

        print("Connected to MongoDB Atlas successfully!")

        return database

    except PyMongoError as e:
        print(f"MongoDB connection failed: {e}")
        return None