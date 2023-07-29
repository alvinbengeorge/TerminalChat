from fastapi import APIRouter, WebSocket
from json import loads
from dotenv import load_dotenv

app = APIRouter(prefix="/message")
load_dotenv()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    run = True
    await websocket.accept()
    while run:
        data = await websocket.receive_text()
        
    await websocket.close(code=1000)