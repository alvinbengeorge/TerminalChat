from fastapi import FastAPI, WebSocket
from json import loads
from dotenv import load_dotenv
from routes import message, users

app = FastAPI()
load_dotenv()
app.include_router(message.router)
app.include_router(users.router)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    run = True
    await websocket.accept()
    while run:
        data = await websocket.receive_text()
        run = loads(data)["run"]
        await websocket.send_json({"message_json": loads(data)["message_json"]})
    await websocket.close(code=1000)


@app.get("/")
async def root():
    return {"message": "Hello World"}
