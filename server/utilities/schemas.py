from pydantic import BaseModel

class AddUser(BaseModel):
    username: str
    password: str

class AddMessage(BaseModel):
    user: str
    text: str
    to: str
    timestamp: int
