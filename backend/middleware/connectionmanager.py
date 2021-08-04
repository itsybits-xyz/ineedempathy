from typing import List, Dict, Optional
from ..schemas import RoomInfo
from fastapi import WebSocket
from starlette.types import ASGIApp, Receive, Scope, Send
from ..utils import after


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

    @after("prune_rooms")
    def add_user(self, room: RoomInfo, name: str, socket: WebSocket):
        if room.name not in self._rooms:
            raise Exception("room_does_not_exist_meowww")
        self._rooms[room.name].add_user(name=name, socket=socket)

    @after("prune_rooms")
    def remove_user(self, room: RoomInfo, name: str, socket: WebSocket):
        room_info = self._rooms.get(room.name)
        if room_info is None:
            return
        room_info.remove_user(name, socket)

    @after("prune_rooms")
    def toggle_card(self, room: RoomInfo, name: str, card_id: Optional[int]):
        if card_id is None:
            return
        room_info = self._rooms.get(room.name)
        room_info.toggle_card(name, card_id)

    @after("prune_rooms")
    def change_speaker(self, room: RoomInfo, name: str):
        if name is None:
            return
        room_info = self._rooms.get(room.name)
        user_info = room_info.get_user(name)
        room_info.set_speaker(user_info)

    def prune_rooms(self):
        for room_name in list(self._rooms):
            if self._rooms[room_name].empty():
                del self._rooms[room_name]

    async def send_update(self, room: RoomInfo):
        room_info = self._rooms.get(room.name)
        if room_info is not None:
            await room_info.send_update()
