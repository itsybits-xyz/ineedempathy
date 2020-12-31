from pydantic import BaseModel
from fastapi import WebSocket
from . import User


class UserInfo(BaseModel):
    user: User
    socket: WebSocket

    class Config:
        arbitrary_types_allowed = True
