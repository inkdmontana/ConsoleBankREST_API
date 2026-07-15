from datetime import datetime
from decimal import Decimal

from bson import ObjectId
from bson.errors import InvalidId
from pymongo.errors import PyMongoError

from db import get_database
from Models.Account import Account


class AccountRepository:

    def __init__(self):
        database = get_database()

        if database is None:
            raise ConnectionError("Could not connect to MongoDB Atlas.")

        self.accounts_collection = database["accounts"]

    def find_by_id(self, account_id):
        try:
            document = self.accounts_collection.find_one({
                "_id": ObjectId(account_id)
            })

            if document is None:
                return None

            return Account(
                account_id=str(document["_id"]),
                user_id=str(document["user_id"]),
                balance=Decimal(str(document["balance"])),
                account_type=document["account_type"],
                created_at=document.get("created_at")
            )

        except InvalidId:
            print("Invalid account ID.")
            return None

        except PyMongoError as error:
            print(f"Error finding account: {error}")
            return None

    def find_by_user_and_type(self, user_id, account_type):
        try:
            normalized_type = account_type.strip().title()

            document = self.accounts_collection.find_one({
                "user_id": ObjectId(user_id),
                "account_type": normalized_type
            })

            if document is None:
                return None

            return Account(
                account_id=str(document["_id"]),
                user_id=str(document["user_id"]),
                balance=Decimal(str(document["balance"])),
                account_type=document["account_type"],
                created_at=document.get("created_at")
            )

        except InvalidId:
            print("Invalid user ID.")
            return None

        except PyMongoError as error:
            print(f"Error finding account by user and type: {error}")
            return None

    def find_by_user_id(self, user_id):
        try:
            documents = self.accounts_collection.find({
                "user_id": ObjectId(user_id)
            })

            accounts = []

            for document in documents:
                accounts.append(
                    Account(
                        account_id=str(document["_id"]),
                        user_id=str(document["user_id"]),
                        balance=Decimal(str(document["balance"])),
                        account_type=document["account_type"],
                        created_at=document.get("created_at")
                    )
                )

            return accounts

        except InvalidId:
            print("Invalid user ID.")
            return []

        except PyMongoError as error:
            print(f"Error finding user accounts: {error}")
            return []

    def create_account(self, account):
        try:
            normalized_type = account.account_type.strip().title()

            document = {
                "user_id": ObjectId(account.user_id),
                "balance": float(account.balance),
                "account_type": normalized_type,
                "created_at": account.created_at or datetime.now()
            }

            result = self.accounts_collection.insert_one(document)

            return result.inserted_id is not None

        except InvalidId:
            print("Invalid user ID.")
            return False

        except PyMongoError as error:
            print(f"Error creating account: {error}")
            return False

    def update_balance(self, account_id, new_balance):
        try:
            result = self.accounts_collection.update_one(
                {"_id": ObjectId(account_id)},
                {
                    "$set": {
                        "balance": float(new_balance)
                    }
                }
            )

            return result.matched_count > 0

        except InvalidId:
            print("Invalid account ID.")
            return False

        except PyMongoError as error:
            print(f"Error updating account balance: {error}")
            return False