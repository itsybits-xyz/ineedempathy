import datetime
from typing import Dict
from pydantic import BaseModel
from fastapi import WebSocket
from . import UserInfo
from ..utils import after


class RoomInfoBase(BaseModel):
    name: str = ''


class RoomInfo(RoomInfoBase):
    speaker: UserInfo = None
    users: Dict[str, UserInfo] = {}

    def __init__(self, *args, **kwargs):
        super(RoomInfo, self).__init__(*args, **kwargs)

    def total_connections(self) -> int:
        total = 0
        for userinfo in self.users.values():
            total += len(userinfo)
        return total

    def get_speaker(self):
        if self.speaker is None:
            return UserInfo(name='')
        return self.speaker

    def set_speaker(self, speaker: UserInfo):
        self.speaker = speaker

    def empty(self):
        if len(self.users) == 0:
            return True
        for idx in self.users:
            if not self.users[idx].empty():
                return False
        return True

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

    def active_users(self):
        speaker = self.get_speaker()
        return [userinfo for userinfo in self.users.values()
                if not userinfo.empty()]

    def upsert_speaker(self):
        no_speaker = self.get_speaker().empty()
        active_players = self.active_users()
        has_players = len(active_players) > 0
        if no_speaker and has_players:
            print(active_players[0].name)
            return self.set_speaker(active_players[0])
        elif not has_players:
            return self.set_speaker(None)

    async def send_update(self):
        await self.broadcast_message(
            {
                "users": self.current_users(),
            }
        )

    def current_users(self):
        speaker = self.get_speaker()
        return [userinfo.progress(speaker) for userinfo in self.users.values()
                if not userinfo.empty()]

    async def broadcast_message(self, msg: Dict):
        for user_id in self.users:
            await self.users[user_id].send_json(msg)
