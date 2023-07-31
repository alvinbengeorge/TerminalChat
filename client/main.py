from textual import widgets
from textual.app import App
from json import dumps

import requests
import threading
import asyncio
import setup
import os
import time
import websockets
import sys


class Input(widgets.Input):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.TerminalApp = app
        self.value = ""

    async def action_submit(self):
        if not self.value:
            return
        self.TerminalApp.sendToServer(
            self.TerminalApp.username, self.TerminalApp.to, self.value
        )
        self.value = ""


class TerminalApp(App):
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode"), ("q", "quit", "Quit")]
    CSS = """
    #input {
        dock: bottom;
        offset: 0 -1;
    }
    """

    def __init__(self):
        super().__init__()
        self.username = os.environ.get("USERNAME")
        self.password = os.environ.get("PASSWORD")
        self.to = sys.argv[1]
        self.lastUpdated = int(time.time())
        self.process = threading.Thread(target=asyncio.run, args=(self.websocket_run(),))
        self.process.start()
        self.exitApplication = False

    def compose(self):
        yield widgets.Header("Hello, world!")
        yield widgets.DataTable()
        yield Input(app=self, placeholder="Type something...", id="input")
        yield widgets.Footer()

    def on_mount(self):
        table = self.query_one(widgets.DataTable)
        table.add_columns("User", "Text")
        table.add_rows(
            [
                [
                    "System",
                    "Welcome to the chat! You're now texting with {}".format(self.to),
                ]
            ]
        )

    def addValue(self, user, text):
        table = self.query_one(widgets.DataTable)
        table.add_rows([[user, text]])

    def sendToServer(self, user, to, text):
        requests.post(
            "http://localhost:8000/message/add",
            headers={
                "username": self.username, 
                "password": self.password
            },
            json={
                "user": user,
                "to": to,
                "text": text,
                "timestamp": int(time.time()),
            },
        )
        self.addValue(user, text)

    async def websocket_run(self):
        uri = "ws://localhost:8000/message/ws"
        i = ""
        async with websockets.connect(uri) as websocket:
            try:
                while not self.exitApplication:
                    print("Sending message")
                    await websocket.send(
                        dumps(
                            {
                                "message_json": {
                                    "user": self.username,
                                    "to": self.to,
                                    "lastUpdated": self.lastUpdated,
                                },
                                "run": self.exitApplication,
                            }
                        )
                    )
                    data = (await websocket.recv())["messages"]
                    self.lastUpdated = int(time.time())
                    for message in data:
                        self.addValue(message["user"], message["text"])
                await websocket.close(code=1000, reason="Bye!")
            except Exception as e:
                print(e)


app = TerminalApp()
app.run()
