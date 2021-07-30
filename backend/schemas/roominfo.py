from typing import Dict
from pydantic import BaseModel
from fastapi import WebSocket
from . import UserInfo, Card
from ..utils import after


class RoomInfoBase(BaseModel):
    name: str


class RoomInfo(RoomInfoBase):
    speaker: UserInfo = None
    users: Dict[str, UserInfo] = {}

    def get_speaker(self):
        if self.speaker is None:
            return UserInfo(name='')
        return self.speaker

    def set_speaker(self, speaker: UserInfo):
        self.speaker = speaker

    def empty(self):
        return len(self.users) == 0

    def get_user(self, name: str):
        if name in self.users:
            return self.users[name]

    def toggle_card(self, name: str, card_id: int):
        if name in self.users:
            self.users[name].toggle_card(card_id)

    @after("upsert_speaker")
    def add_user(self, name: str, socket: WebSocket):
        if name not in self.users:
            self.users[name] = UserInfo(
                name=name,
            )
        self.users[name].add_socket(socket)

    @after("upsert_speaker")
    def remove_user(self, name: str, socket: WebSocket):
        if name in self.users:
            self.users[name].remove_socket(socket)
            if self.users[name].empty():
                del self.users[name]

    def upsert_speaker(self):
        if self.get_speaker().name not in self.users:
            self.set_speaker(None)
        if self.get_speaker().name is None and len(self.users) > 1:
            self.set_speaker(self.users.values().first())

    async def send_update(self):
        await self.broadcast_message(
            {
                "users": self.current_users(),
            }
        )

    def current_users(self):
        speaker = self.get_speaker()
        return [userinfo.progress(speaker) for userinfo in self.users.values()]

    async def broadcast_message(self, msg: Dict):
        print("sending")
        print(msg)
        for user_id in self.users:
            await self.users[user_id].send_json(msg)
