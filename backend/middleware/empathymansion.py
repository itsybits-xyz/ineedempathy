from typing import List, Dict
from ..schemas import User, UserInfo, RoomInfo
from ..schemas import Room
from fastapi import WebSocket


class EmpathyMansion:
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

    def add_user(self, room: Room, user: User, socket: WebSocket):
        if room.id not in self._rooms:
            self._rooms[room.id] = RoomInfo(
                room=room,
                users={},
            )
        self._rooms[room.id].add_user(UserInfo(
            user=user,
            socket=socket
        ))

    def remove_user(self, room: Room, user: User):
        roomInfo = self._rooms.get(room.id)
        roomInfo.remove_user(user.id)
        if roomInfo is None or roomInfo.empty():
            del self._rooms[room.id]

    async def send_update(self, room: Room):
        roomInfo = self._rooms.get(room.id)
        if roomInfo is not None:
            await roomInfo.send_update()
