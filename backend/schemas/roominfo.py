from typing import List, Dict
from pydantic import BaseModel
from fastapi import WebSocket
from backend.schemas import Story, Guess, Room, User, UserInfo
from backend.utils import after
from enum import Enum


class RoomStatus(str, Enum):
    WRITING = "WRITING"
    GUESSING = "GUESSING"
    END_GAME = "END_GAME"


class RoomInfo(BaseModel):
    status: RoomStatus = RoomStatus.WRITING
    room: Room
    users: Dict[int, UserInfo]
    stories: List[Story] = []
    guesses: List[Guess] = []

    @property
    def completed(self) -> List[int]:
        complete: List[int] = []
        if self.status == RoomStatus.WRITING:
            for story in self.stories:
                complete.append(story.user_id)
        elif self.status == RoomStatus.GUESSING:
            users.filter((user) => {
                return user.hasGuessFor(self.stories)
            })
        return complete

    async def add_guess(self, story: Story, guess: Guess):
        self.guesses.append(story)
        await self.send_update()
        return True

    async def add_story(self, story: Story):
        if story.room_id == self.room.id and story.user_id in self.users:
            self.stories.append(story)
            await self.send_update()
            return True
        return False

    def collected_all(self) -> bool:
        if len(self.users) <= 1:
            return False
        if self.status in [RoomStatus.WRITING, RoomStatus.GUESSING]:
            return len(self.completed) == len(self.users)

    def clear_cache(self):
        self.stories.clear()
        self.guesses.clear()

    @after("clear_cache")
    def end_game(self):
        self.status = RoomStatus.END_GAME

    def advance_status(self):
        if not self.collected_all():
            return
        if self.status == RoomStatus.WRITING:
            self.status = RoomStatus.GUESSING
        elif self.status == RoomStatus.GUESSING:
            self.status = RoomStatus.WRITING
            self.clear_cache()

    def empty(self):
        return len(self.users) == 0

    def get_user(self, user_id: int):
        if user_id in self.users:
            return self.users[user_id]
        return None

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

    async def send_update(self):
        self.advance_status()
        await self.broadcast_message(
            {
                "status": self.status,
                "completed": self.completed,
                "currentUsers": self.current_users(),
            }
        )

    def current_users(self):
        return [userinfo.user.dict() for userinfo in self.users.values()]

    async def broadcast_message(self, msg: Dict):
        print("sending")
        print(msg)
        for user_id in self.users:
            await self.users[user_id].send_json(msg)
