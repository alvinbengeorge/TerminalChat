from textual import widgets
from textual.app import App
from json import dumps

import requests
import asyncio
import setup
import os
import time
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
        self.to = ""

    def compose(self):
        yield widgets.Header("Hello, world!")
        yield widgets.DataTable()
        yield Input(app=self, placeholder="Type something...", id="input")
        yield widgets.Footer()

    def on_mount(self):
        table = self.query_one(widgets.DataTable)
        table.add_columns("User", "Text")
        table.add_rows([])

    def addValue(self, user, text):
        table = self.query_one(widgets.DataTable)
        table.add_rows([[user, text]])

    def sendToServer(self, user, to, text):
        requests.post(
            "http://localhost:8000/message/add",            
            headers={"username": self.username, "password": self.password},
            json={
                "user": user,
                "to": to,
                "text": text,
                "timestamp": int(time.time()),
            }
        )
        self.addValue(user, text)


app = TerminalApp()
app.run()
