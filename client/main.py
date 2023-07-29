from textual import widgets
from textual.app import App

class TerminalApp(App):

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("q", "quit", "Quit")
    ]
    
    def __init__(self, sendToServer):
        super().__init__()
        self.sendToServer = sendToServer
        
    def compose(self):
        yield widgets.Header("Hello, world!")
        yield widgets.DataTable()
        yield widgets.Input(placeholder="Type something...")
        yield widgets.Button("Submit", name="submit")
        yield widgets.Footer()

    def on_mount(self):
        table = self.query_one(widgets.DataTable)
        table.add_columns("User", "Text")
        table.add_rows([
            ["@mdelacruz", "Miguel de la Cruz"],
            ["@johndoe", "John Doe"],
            ["@janedoe", "Jane Doe"],
        ])
    
    def on_button_pressed(self, event: widgets.Button.Pressed):
        input_bar = self.query_one(widgets.Input)
        if not input_bar.value:
            return
        self.addValue("@me", input_bar.value)
        self.sendToServer(input_bar.value)
        input_bar.value = ""

    def addValue(self, user, text):
        table = self.query_one(widgets.DataTable)
        table.add_rows([[user, text]]

app = TerminalApp()
app.run()
