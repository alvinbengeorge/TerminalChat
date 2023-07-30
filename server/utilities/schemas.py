from pydantic import BaseModel


class AddUser(BaseModel):
    username: str
    password: str

class ResetPassword(BaseModel):
    username: str
    password: str
    new_password: str


class AddMessage(BaseModel):
    user: str
    text: str
    to: str
    timestamp: int


class GetMessages(BaseModel):
    user: str
    to: str

