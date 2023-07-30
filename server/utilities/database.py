from pymongo import MongoClient
import os


class Message:
    def __init__(self, user: str, text: str, to: str, timestamp: int):
        self.user = user
        self.text = text
        self.to = to
        self.timestamp = timestamp

    def toDict(self):
        return {
            "user": self.user,
            "text": self.text,
            "to": self.to,
            "timestamp": self.timestamp,
        }


class User:
    def __init__(self, username: str, password: str = ""):
        self.username = username
        self.password = password

    def toDict(self):
        return {
            "username": self.username,
            "password": self.password,
        }


class Database:
    def __init__(self):
        self.URI = os.environ.get("MONGODB_URI")
        self.CLIENT = MongoClient(self.URI)
        self.DATABASE = self.CLIENT.get_database("terminalChat")
        self.messages = self.DATABASE.get_collection("messages")
        self.users = self.DATABASE.get_collection("users")

    def insert_message(self, message: Message):
        return self.messages.insert_one(message.toDict())

    def insert_user(self, user: User):
        if self.get_user(user.username):
            return {"error": "User already exists"}
        result = self.users.insert_one(user.toDict())
        print(result)

    def get_messages(self, user: str, to: str):
        return self.messages.find({"to": to, "user": user})

    def get_users(self):
        return self.users.find()

    def get_user(self, username: str):
        result = self.users.find_one({"username": username})
        return result
