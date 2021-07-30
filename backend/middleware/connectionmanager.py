from typing import List, Dict
from ..schemas import RoomInfo, Card
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
        self._rooms: Dict[str, RoomInfo] = {}

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

    def get_room(self, name: str):
        return self._rooms.get(name)

    def create_room(self, name: str):
        room_info = RoomInfo(name=name)
        self._rooms[name] = room_info
        return room_info

    def add_user(self, room: RoomInfo, name: str, socket: WebSocket):
        if room.name not in self._rooms:
            # TODO
            self._rooms[room.name] = RoomInfo(
                room=room,
                users={},
            )
        self._rooms[room.name].add_user(
            name=name,
            socket=socket
        )

    def remove_user(self, room: RoomInfo, name: str, socket: WebSocket):
        room_info = self._rooms.get(room.name)
        room_info.remove_user(name, socket)
        if room_info is None or room_info.empty():
            del self._rooms[room.name]

    def add_card(self, room: RoomInfo, name: str, card: Card, socket: WebSocket):
        room_info = self._rooms.get(room.name)
        room_info.add_card(name, card, socket)

    def remove_card(self, room: RoomInfo, name: str, card: Card, socket: WebSocket):
        room_info = self._rooms.get(room.name)
        room_info.remove_card(name, card, socket)

    async def send_update(self, room: RoomInfo):
        room_info = self._rooms.get(room.name)
        if room_info is not None:
            await room_info.send_update()
