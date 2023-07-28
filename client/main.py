#sending and receiving through websocket
# Path: client/main.py

import asyncio
import json
import websockets

async def main():
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:
        while True:
            #send json
            await websocket.send(json.dumps({
                "message_json": input("Message: "),
                "run": True
            }))
            print(await websocket.recv())
        await websocket.close(code=1000, reason="Bye!")

asyncio.run(main())