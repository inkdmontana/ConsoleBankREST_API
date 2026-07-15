from datetime import datetime

from bson import ObjectId
from bson.errors import InvalidId
from pymongo.errors import PyMongoError

from db import get_database
from Models.User import User


class UserRepository:
    

    def __init__(self):
        database = get_database()

        if database is None:
            raise ConnectionError("Could not connect to MongoDB Atlas.")

        self.users_collection = database["users"]

    def find_by_id(self, user_id):
        
        try:
            document = self.users_collection.find_one({"_id": ObjectId(user_id)})

            if document is None:
                return None

            return User(
                user_id=str(document.get("_id")),
                name=document.get("name"),
                email=document.get("email"),
                password_hash=document.get("password_hash"),
                created_at=document.get("created_at")
            )
                
        except (PyMongoError, InvalidId) as error:
            print(f"Error finding user: {error}")
            return None

    def create_user(self, user):
        try:
            document = {
                "name": user.name.strip(),
                "email": user.email.strip().lower(),
                "password_hash": user.password_hash,
                "created_at": user.created_at or datetime.now()
            }

            result = self.users_collection.insert_one(document)

            return str(result.inserted_id)

        except PyMongoError as error:
            print(f"Error creating user: {error}")
            return None

    def find_by_email(self, email):

        try:
            normalized_email = email.strip().lower()

            document = self.users_collection.find_one({
                "email": normalized_email
            })

            if document is None:
                return None

            return User(
                user_id=str(document.get("_id")),
                name=document.get("name"),
                email=document.get("email"),
                password_hash=document.get("password_hash"),
                created_at=document.get("created_at")
            )

        except PyMongoError as error:
            print(f"Error finding user: {error}")
            return None