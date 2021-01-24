from typing import List, Dict
from ..schemas import User, Room, RoomInfo, Story
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

    async def add_story(self, room: Room, story: Story):
        room_info = self._rooms.get(room.id)
        if room_info is None:
            raise RuntimeError(f"Room '{room.name}' does not exist!")
        if story.user_id not in room_info.users:
            raise RuntimeError("Please join the room")
        room_info.add_story(story)
        await room_info.send_update()

    def add_user(self, room: Room, user: User, socket: WebSocket):
        if room.id not in self._rooms:
            self._rooms[room.id] = RoomInfo(
                room=room,
                users={},
            )
        self._rooms[room.id].add_user(
            user=user,
            socket=socket
        )

    def remove_user(self, room: Room, user: User, socket: WebSocket):
        room_info = self._rooms.get(room.id)
        room_info.remove_user(user, socket)
        if room_info is None or room_info.empty():
            del self._rooms[room.id]

    async def send_update(self, room: Room):
        room_info = self._rooms.get(room.id)
        if room_info is not None:
            await room_info.send_update()
