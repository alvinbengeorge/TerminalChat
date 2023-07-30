from fastapi import APIRouter, Response, Request
from utilities.database import Database, User
from utilities.schemas import AddUser, ResetPassword

router = APIRouter(prefix="/user")
db = Database()


@router.post("/add")
async def add_user(user: AddUser):
    return db.insert_user(User(user.username, user.password, []))

@router.post("/reset")
async def reset_password(req: Request, reset_password: ResetPassword):
    return db.edit_user(User(reset_password.username, reset_password.new_password, []), reset_password.new_password)


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
