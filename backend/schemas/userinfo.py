from pydantic import BaseModel
from fastapi import WebSocket
from . import User
from typing import Set, Dict


class UserInfo(BaseModel):
    user: User
    sockets: Dict[int, WebSocket] = {}

    def empty(self):
        return len(self.sockets) == 0

    def add_socket(self, socket: WebSocket):
        self.sockets[id(socket)] = socket

    def remove_socket(self, socket: WebSocket):
        del self.sockets[id(socket)]

    async def send_json(self, msg: Dict):
        for socket in self.sockets.values():
            await socket.send_json(msg)

    class Config:
        arbitrary_types_allowed = True
