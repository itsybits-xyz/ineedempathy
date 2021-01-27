from pydantic import BaseModel
from fastapi import WebSocket
from . import User, Story
from typing import Dict, Optional
from fastapi.encoders import jsonable_encoder


class UserInfo(BaseModel):
    user: User
    sockets: Dict[int, WebSocket] = {}
    story: Optional[Story] = None

    def empty(self):
        return len(self.sockets) == 0

    def add_socket(self, socket: WebSocket):
        self.sockets[id(socket)] = socket

    def remove_socket(self, socket: WebSocket):
        del self.sockets[id(socket)]

    def progress(self):
        return {
            "completed": 0,
            "pending": 1,
        }

    async def send_json(self, msg: Dict):
        for socket in self.sockets.values():
            await socket.send_json(jsonable_encoder(msg))

    class Config:
        arbitrary_types_allowed = True
