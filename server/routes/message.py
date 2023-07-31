from fastapi import APIRouter, WebSocket, Response, Request
from json import loads
from dotenv import load_dotenv
from utilities.database import Database, User, Message
from utilities.schemas import GetMessages, AddMessage

router = APIRouter(prefix="/message")
load_dotenv()
db = Database()



@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    run = True
    await websocket.accept()
    while run:
        data = await websocket.receive_text()
        data = loads(data)
        print(data)
        if data.get("run"):
            messages = db.get_messages(
                data["message_json"]["to"],
                data["message_json"]["user"]
            )
            print(messages)
            messages = [
                message for message in messages if message["timestamp"] > data["message_json"]["lastUpdated"]
            ]
            if messages:
                await websocket.send_json({"messages": messages})

    await websocket.close(code=1000)


@router.post("/getAllMessages")
async def get_all_messages(req: Request, get_messages: GetMessages):
    if not req.headers.get("username") or not req.headers.get("password"):
        return {
            "error": "Please provide a username and password in the headers of the request"
        }
    user = db.get_user(req.headers["username"])
    if (
        user
        and user.get("username") == req.headers["username"]
        and user.get("password") == req.headers["password"]
    ):
        return db.get_messages(get_messages.user, get_messages.to)
    if not get_messages.user != req.headers["username"]:
        return {"error": "Cannot fetch messages from other users"}

    return {"error": "Invalid username or password"}


@router.post("/add")
async def add_message(req: Request, message: AddMessage):
    if req.headers.get("username") and req.headers.get("password"):
        user = db.get_user(req.headers["username"])
        conditions = user and user.get("username", "") == req.headers["username"] and user.get("password", "") == req.headers["password"]
        if (conditions):
            db.insert_message(
                Message(
                    user=message.user,
                    text=message.text,
                    to=message.to,
                    timestamp=message.timestamp,
                )
            )
            return {"message": "Message added"}
        return {"error": "Invalid username or password"}
    else :
        return {"error": "Please provide a username and password in the headers of the request"}
