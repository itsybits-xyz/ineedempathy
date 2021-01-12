from typing import Dict, List
from pydantic import BaseModel
from fastapi import WebSocket
from . import Story, Guess, Room, User, UserInfo
from ..utils import after
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
        for item in (self.stories if self.status == RoomStatus.WRITING else self.guesses):
            complete.append(item.user_id)
        return complete

    async def add_guess(self, story: Story, guess: Guess):
        self.guesses.append(story)
        await self.send_update()

    async def add_story(self, story: Story):
        self.stories.append(story)
        await self.send_update()

    def collected_all(self) -> bool:
        if self.status == RoomStatus.WRITING:
            has_stories: bool = len(self.stories) > 0
            stories_complete: bool = len(self.completed) == len(self.stories)
            return has_stories and stories_complete
        elif self.status == RoomStatus.GUESSING:
            has_guesses: bool = len(self.guesses) > 0
            guesses_complete: bool = len(self.completed) == len(self.guesses)
            return has_guesses and guesses_complete

    def calculate_status(self):
        if self.collected_all():
            self.advance_status()

    def clear_cache(self):
        self.stories.clear()
        self.guesses.clear()

    @after("clear_cache")
    def end_game(self):
        self.status = RoomStatus.END_GAME

    @after("clear_cache")
    def advance_status(self):
        if self.status == RoomStatus.WRITING:
            self.status = RoomStatus.GUESSING
        elif self.status == RoomStatus.GUESSING:
            self.status = RoomStatus.WRITING

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
        self.calculate_status()
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
