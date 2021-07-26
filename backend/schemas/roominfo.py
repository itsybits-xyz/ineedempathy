from typing import Dict
from pydantic import BaseModel
from fastapi import WebSocket
from . import Room, UserInfo, Card
from ..utils import after


class RoomInfo(BaseModel):
    room: Room
    speaker: UserInfo = None
    users: Dict[int, UserInfo]

    def get_speaker(self):
        if self.speaker is None:
            return UserInfo(user_token=None)
        return self.speaker

    def set_speaker(self, speaker: UserInfo):
        self.speaker = speaker

    def empty(self):
        return len(self.users) == 0

    def get_user(self, user_token: int):
        if user_token in self.users:
            return self.users[user_token]

    def add_card(self, user_token: str, card: Card):
        if user_token in self.users:
            self.users[user_token].add_card(card)

    def remove_card(self, user_token: str, card: Card):
        if user_token in self.users:
            self.users[user_token].remove_card(card)

    @after("upsert_speaker")
    def add_user(self, user_token: str, socket: WebSocket):
        if user_token not in self.users:
            self.users[user_token] = UserInfo(
                user_token=user_token,
            )
        self.users[user_token].add_socket(socket)

    @after("upsert_speaker")
    def remove_user(self, user_token: str, socket: WebSocket):
        if user_token in self.users:
            self.users[user_token].remove_socket(socket)
            if self.users[user_token].empty():
                del self.users[user_token]

    def upsert_speaker(self):
        if self.get_speaker().user_token not in self.users:
            self.set_speaker(None)
        if self.get_speaker().user_token is None and len(self.users) > 1:
            self.set_speaker(self.users.values().first())

    async def send_update(self):
        await self.broadcast_message(
            {
                "users": self.current_users(),
            }
        )

    def current_users(self):
        return [userinfo.status(self.speaker) for userinfo in self.users.values()]

    async def broadcast_message(self, msg: Dict):
        print("sending")
        print(msg)
        for user_id in self.users:
            await self.users[user_id].send_json(msg)
