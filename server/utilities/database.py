from pymongo import MongoClient
import os

class Message:
    def __init__(self, user: str, text: str, to: str, timestamp: int):
        self.user = user
        self.text = text
        self.to = to
        self.timestamp = timestamp

    def __dict__(self):
        return {
            "user": self.user,
            "text": self.text,
            "to": self.to,
            "timestamp": self.timestamp
        }

class User:
    def __init__(self, username: str, friends: list):
        self.username = username
        self.friends = friends
        self.password = password

    def __dict__(self):
        return {
            "username": self.username,
            "friends": self.friends
        }

class Database:
    def __init__(self):
        self.URI = os.environ.get("MONGODB_URI")
        self.CLIENT = MongoClient(URI)
        self.DATABASE = self.CLIENT.get_database("terminalChat")
        self.messages = self.DATABASE.get_collection("messages")
        self.users = self.DATABASE.get_collection("users")

    def insert_message(self, message: Message):
        return self.messages.insert_one(message)       

    def insert_user(self, user: User):
        if not self.get_user(user.username):
            return {"error": "User already exists"}
        return self.users.insert_one(user)

    def get_messages(self, user: str, to: str):
        return self.messages.find({
            "to": to,
            "user": user
        })

    def get_users(self):
        return self.users.find()

    def get_user(self, username: str):
        return self.users.find_one({
            "username": username
        })
     

    