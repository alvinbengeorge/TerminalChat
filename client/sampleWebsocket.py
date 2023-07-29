#sending and receiving through websocket
# Path: client/main.py

import asyncio
import json
import websockets

async def main():
    uri = "ws://localhost:8000/ws"
    i = ""
    async with websockets.connect(uri) as websocket:
        while i != "X":
            i = input("Message: ")
            await websocket.send(json.dumps({
                "message_json": i,
                "run": True
            }))
            print(await websocket.recv())
        await websocket.close(code=1000, reason="Bye!")

asyncio.run(main())