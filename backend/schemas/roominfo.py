from typing import Dict, List
from pydantic import BaseModel
from fastapi import WebSocket
from . import Room, User, UserInfo
from ..utils import after
from enum import Enum


class RoomStatus(str, Enum):
    WRITING = "WRITING"
    GUESSING = "GUESSING"
    END_GAME = "END_GAME"


class RoomInfo(BaseModel):
    status: RoomStatus = RoomStatus.WRITING
    room: Room
    users: Dict[int, UserInfo]
    completed: List[int] = []

    def add_to_done_list(self, user_id: int):
        self.completed.append(user_id)
        left_over = set(self.users.keys()) - set(self.completed)
        if len(left_over) == 0:
            self.advance_status()

    def end_game(self):
        self.completed.clear()
        self.status = RoomStatus.END_GAME

    def advance_status(self):
        if self.status == RoomStatus.WRITING:
            self.completed.clear()
            self.status = RoomStatus.GUESSING
        elif self.status == RoomStatus.GUESSING:
            self.completed.clear()
            self.status = RoomStatus.WRITING

    def empty(self):
        return len(self.users) == 0

    def get_user(self, user_id: int):
        if user_id in self.users:
            return self.users[user_id]
        return None

    def add_user(self, user: User, socket: WebSocket):
        if user.id not in self.users:
            self.users[user.id] = UserInfo(
                user=user,
            )
        self.users[user.id].add_socket(socket)

    def remove_user(self, user: User, socket: WebSocket):
        if user.id in self.users:
            self.users[user.id].remove_socket(socket)
            if self.users[user.id].empty():
                del self.users[user.id]

    async def send_update(self):
        await self.broadcast_message(
            {
                "status": self.status,
                "completed": self.completed,
                "currentUsers": self.current_users(),
            }
        )

    def current_users(self):
        return [userinfo.user.dict() for userinfo in self.users.values()]

    async def broadcast_message(self, msg: Dict):
        print("sending")
        print(msg)
        for user_id in self.users:
            await self.users[user_id].send_json(msg)
