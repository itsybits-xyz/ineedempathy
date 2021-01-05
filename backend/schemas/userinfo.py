from pydantic import BaseModel
from fastapi import WebSocket
from . import User
from typing import Optional


class UserInfo(BaseModel):
    user: User
    socket: Optional[WebSocket]

    class Config:
        arbitrary_types_allowed = True
