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
    stories: List[Story] = []

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
        self.stories.append(story)
        if story.user_id in self.users:
            self.users[story.user_id].story = story
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

    def progress(self):
        return {user_id: user_info.progress() for user_id, user_info in self.users.items()}

    async def send_update(self):
        if self.status == RoomStatus.GUESSING:
            await self.broadcast_message(
                {
                    "status": self.status,
                    "progress": self.progress(),
                    "users": self.current_users(),
                    "stories": [{"user_id": story.user_id, "story_id": story.id} for story in self.stories],
                }
            )
        else:
            await self.broadcast_message(
                {
                    "status": self.status,
                    "progress": self.progress(),
                    "users": self.current_users(),
                    "stories": [],
                }
            )

    def current_users(self):
        return [userinfo.user.dict() for userinfo in self.users.values()]

    async def broadcast_message(self, msg: Dict):
        print("sending")
        print(msg)
        for user_id in self.users:
            await self.users[user_id].send_json(msg)
