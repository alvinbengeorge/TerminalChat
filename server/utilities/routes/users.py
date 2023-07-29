from fastapi import APIRouter, Response, Request
from utilities.database import Database, User
from utilities.schema import AddUser

router = APIRouter(prefix="/user")
db = Database()

@router.post("/add")
async def add_user(user: AddUser):
    return db.insert_user(
        User(user.username, user.password, []
    ))

@router.get("/get")
async def get_user(req: Request):
    user = db.get_user(req.headers["username"])
    if user and user.username == req.headers["username"] and user.password == req.headers["username"]:
        return user
