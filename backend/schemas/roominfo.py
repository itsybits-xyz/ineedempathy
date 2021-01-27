from typing import Dict, List
from pydantic import BaseModel
from fastapi import WebSocket
from . import Room, User, UserInfo, Story
from enum import Enum


class RoomStatus(str, Enum):
    WRITING = "WRITING"
    GUESSING = "GUESSING"
    RESULTS = "RESULTS"
    END_GAME = "END_GAME" 


class RoomInfo(BaseModel):
    status: RoomStatus = RoomStatus.WRITING
    room: Room
    users: Dict[int, UserInfo]
    stories: Dict[int, Story] = {}

    def end_game(self):
        self.status = RoomStatus.END_GAME

    def advance_status(self):
        if self.status == RoomStatus.WRITING:
            if len(self.stories) == len(self.users):
                self.status = RoomStatus.GUESSING
        elif self.status == RoomStatus.GUESSING:
            self.status = RoomStatus.RESULTS
        elif self.status == RoomStatus.RESULTS:
            self.status = RoomStatus.WRITING

    def empty(self):
        return len(self.users) == 0

    def get_user(self, user_id: int):
        if user_id in self.users:
            return self.users[user_id]
        return None

    def add_story(self, story: Story):
        if story.user_id not in self.stories:
            self.stories[story.user_id] = story
            self.advance_status()

    def add_user(self, user: User, socket: WebSocket):
        if user.id not in self.users:
            self.users[user.id] = UserInfo(
                user=user,
            )
        self.users[user.id].add_socket(socket)

    def remove_user(self, user: User, socket: WebSocket):
        if user.id in self.users:
            self.users[user.id].remove_socket(socket)
            if self.users[user.id].empty():
                del self.users[user.id]

    def progress_for(self, user_id: int):
        user = self.get_user(user_id)
        if self.status == RoomStatus.WRITING:
            return {
                "completed": 1 if user_id in self.stories else 0,
                "pending": 0 if user_id in self.stories else 1,
            }
        elif self.status == RoomStatus.GUESSING:
            return {
                "completed": -1,
                "pending": -1,
            }
        else:
            return user.progress()

    def progress(self):
        return {user_id: self.progress_for(user_id) for user_id, user_info in self.users.items()}

    async def send_update(self):
        await self.broadcast_message(
            {
                "status": self.status,
                "progress": self.progress(),
                "users": self.current_users(),
                "stories": [story for user_id, story in self.stories.items()],
            }
        )

    def current_users(self):
        return [userinfo.user.dict() for userinfo in self.users.values()]

    async def broadcast_message(self, msg: Dict):
        print("sending")
        print(msg)
        for user_id in self.users:
            await self.users[user_id].send_json(msg)
