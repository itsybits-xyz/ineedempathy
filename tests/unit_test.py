from typing import Generator, Dict

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.main import app
from backend.deps import get_db
from backend.database import Base
from backend.schemas import (RoomInfo, RoomStatus, RoomType, UserInfo, Story,
                             Guess, Room, User)
from datetime import datetime
from fastapi import WebSocket
import pytest
from unittest.mock import MagicMock, AsyncMock


# Setup a testing db
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db() -> Generator:
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Apply the test db as database dependency.
app.dependency_overrides[get_db] = override_get_db


def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


class MockWebSocket(WebSocket):
    def __init__(self):
        pass


room_id = 0
story_id = 0
user_id = 0
guess_id = 0


def create_guess(story, user):
    global guess_id
    guess_id += 1
    return Guess(id=guess_id, user_id=user.id, room_id=story.room_id,
                 story_id=story.id, card_id=1)


def create_user(room):
    global user_id
    user_id += 1
    return User(id=user_id, name="princess", room_id=room.id)


def create_story(room, user):
    global story_id
    story_id += 1
    return Story(id=story_id, user_id=user.id, card_id=1, room_id=room.id, description="")


def create_room():
    global room_id
    room_id += 1
    return Room(id=room_id, name="meow", type=RoomType.Multiplayer, created_at=datetime.now())


def test_add_user():
    mock_room = create_room()
    room_info = RoomInfo(
        status=RoomStatus.WRITING,
        room=mock_room,
        users={}
    )
    assert room_info.empty()
    room_info.add_user(
        user=User(id=1, name="princess", room_id=mock_room.id),
        socket=MockWebSocket()
    )
    assert not room_info.empty()


@pytest.mark.asyncio
async def test_add_story_with_no_users():
    mock_room = create_room()
    room_info = RoomInfo(
        status=RoomStatus.WRITING,
        room=mock_room,
        users={}
    )
    assert len(room_info.stories) == 0
    assert await room_info.add_story(story=Story(id=1, user_id=1, card_id=1,
        room_id=mock_room.id, description="")) is False
    assert len(room_info.stories) == 0


@pytest.mark.asyncio
async def test_add_story_with_users():
    mock_room = create_room()
    user_1 = UserInfo(user=create_user(mock_room))
    user_2 = UserInfo(user=create_user(mock_room))
    story_1 = create_story(mock_room, user_1.user)
    story_2 = create_story(mock_room, user_2.user)
    room_info = RoomInfo(
        status=RoomStatus.WRITING,
        room=mock_room,
        users={user_1.user.id: user_1, user_2.user.id: user_2},
        stories=[story_1]
    )
    assert room_info.status == RoomStatus.WRITING
    await room_info.add_story(story_2)
    assert room_info.status == RoomStatus.GUESSING


@pytest.mark.asyncio
async def test_add_guesses_to_story_with_users():
    mock_room = create_room()
    user_1 = UserInfo(user=create_user(mock_room))
    user_2 = UserInfo(user=create_user(mock_room))
    story_1 = create_story(mock_room, user_1.user)
    story_2 = create_story(mock_room, user_2.user)
    guess_1 = create_guess(story_1, user_2.user)
    guess_2 = create_guess(story_2, user_1.user)
    room_info = RoomInfo(
        status=RoomStatus.WRITING,
        room=mock_room,
        users={user_1.user.id: user_1, user_2.user.id: user_2},
        stories=[story_1, story_2]
    )
    room_info.advance_status()
    assert room_info.status == RoomStatus.GUESSING
    await room_info.add_guess(story_1, guess_1)
    assert room_info.status == RoomStatus.GUESSING
    await room_info.add_guess(story_2, guess_2)
    assert room_info.status == RoomStatus.WRITING
