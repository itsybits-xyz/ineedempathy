from pydantic import BaseModel
from fastapi import WebSocket
from typing import List, Dict
from fastapi.encoders import jsonable_encoder


class UserInfo(BaseModel):
    name: str = "Princess"
    sockets: Dict[int, WebSocket] = {}
    cards: List[int] = []

    def empty(self):
        return len(self.sockets) == 0

    def add_socket(self, socket: WebSocket):
        self.sockets[id(socket)] = socket

    def remove_socket(self, socket: WebSocket):
        del self.sockets[id(socket)]

    def toggle_card(self, card_id: int):
        if card_id in self.cards:
            self.cards.remove(card_id)
        else:
            self.cards.append(card_id)

    def progress(self, speaker):
        return {
            "name": self.name,
            "speaker": self.name == speaker.name,
            "cards": self.cards,
        }

    async def send_json(self, msg: Dict):
        for socket in self.sockets.values():
            await socket.send_json(jsonable_encoder(msg))

    class Config:
        arbitrary_types_allowed = True
