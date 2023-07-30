from fastapi import APIRouter, Response, Request
from utilities.database import Database, User
from utilities.schemas import AddUser, ResetPassword
from dotenv import load_dotenv

router = APIRouter(prefix="/user")
load_dotenv()
db = Database()


@router.post("/add")
async def add_user(user: AddUser):
    return db.insert_user(User(user.username, user.password))

@router.get("/get")
async def get_user(req: Request):
    user = db.get_user(req.headers["username"])
    if not req.headers.get("username") or not req.headers.get("password"):
        return {
            "error": "Please provide a username and password in the headers of the request"
        }
    if (
        user
        and user.username == req.headers["username"]
        and user.password == req.headers["username"]
    ):
        return user

    return {"error": "Invalid username or password"}
