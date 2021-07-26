from pydantic import BaseModel
from fastapi import WebSocket
from . import Card
from typing import Dict, Optional
from fastapi.encoders import jsonable_encoder


class UserInfo(BaseModel):
    user_token: str = None
    name: str = "Princess"
    sockets: Dict[int, WebSocket] = {}
    cards: Optional[Card] = []

    def empty(self):
        return len(self.sockets) == 0

    def add_socket(self, socket: WebSocket):
        self.sockets[id(socket)] = socket

    def remove_socket(self, socket: WebSocket):
        del self.sockets[id(socket)]

    def add_card(self, card: Card):
        self.cards[id(card)] = card

    def remove_card(self, card: Card):
        del self.card[id(card)]

    def progress(self, speaker):
        return {
            "name": self.name,
            "speaker": self.user_token == speaker.user_token,
            "cards": [card.id for card in self.cards.values()],
        }

    async def send_json(self, msg: Dict):
        for socket in self.sockets.values():
            await socket.send_json(jsonable_encoder(msg))

    class Config:
        arbitrary_types_allowed = True
