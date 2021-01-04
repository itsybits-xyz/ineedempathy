from typing import Dict
from pydantic import BaseModel
from . import Room, UserInfo


class RoomInfo(BaseModel):
    room: Room
    users: Dict[int, UserInfo]

    def empty(self):
        return len(self.users) == 0

    def get_user(self, user_id: int):
        if user_id in self.users:
            return self.users[user_id]
        return None

    def add_user(self, userInfo: UserInfo):
        self.users[userInfo.user.id] = userInfo

    def remove_user(self, user_id: int):
        if user_id in self.users:
            del self.users[user_id]

    async def send_update(self):
        await self.broadcast_message(
            {
                "status": 0,
                "waitingOn": [user_id for user_id in self.users.keys()],
                "currentUsers": self.current_users(),
            }
        )

    def current_users(self):
        return [userinfo.user.dict() for userinfo in self.users.values()]

    async def broadcast_message(self, msg: Dict):
        print("sending")
        print(msg)
        for user_id in self.users:
            await self.users[user_id].socket.send_json(msg)
