from typing import List, Dict
from ..schemas import Room, RoomInfo, Card
from fastapi import WebSocket
from starlette.types import ASGIApp, Receive, Scope, Send


class ConnectionManagerMiddleware:
    def __init__(self, app: ASGIApp):
        self._app = app
        self._connection_manager = ConnectionManager()

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] in ("lifespan", "http", "websocket"):
            scope["connection_manager"] = self._connection_manager
        await self._app(scope, receive, send)


class ConnectionManager:
    """Room state, comprising connected users."""

    def __init__(self):
        print("Creating new empty room")
        self._rooms: Dict[int, RoomInfo] = {}

    def __len__(self) -> int:
        """Get the number of users in the room."""
        return len(self._rooms)

    @property
    def empty(self) -> bool:
        """Check if the room is empty."""
        return len(self._rooms) == 0

    @property
    def user_list(self) -> List[str]:
        """Return a list of IDs for connected users."""
        return list(self._rooms)

    def add_user(self, room: Room, user_token: str, socket: WebSocket):
        if room.id not in self._rooms:
            self._rooms[room.id] = RoomInfo(
                room=room,
                users={},
            )
        self._rooms[room.id].add_user(
            user_token=user_token,
            socket=socket
        )

    def remove_user(self, room: Room, user_token: str, socket: WebSocket):
        room_info = self._rooms.get(room.id)
        room_info.remove_user(user_token, socket)
        if room_info is None or room_info.empty():
            del self._rooms[room.id]

    def add_card(self, room: Room, user_token: str, card: Card, socket: WebSocket):
        room_info = self._rooms.get(room.id)
        room_info.add_card(user_token, card, socket)

    def remove_card(self, room: Room, user_token: str, card: Card, socket: WebSocket):
        room_info = self._rooms.get(room.id)
        room_info.remove_card(user_token, card, socket)

    async def send_update(self, room: Room):
        room_info = self._rooms.get(room.id)
        if room_info is not None:
            await room_info.send_update()
