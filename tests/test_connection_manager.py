from backend.middleware import ConnectionManager
from backend.schemas import User, Room
from datetime import datetime


room_count = 0
user_count = 0


def mock_room(name="princess.mansion"):
    global room_count
    room_count += 1
    return Room(
        id=room_count,
        name=name,
        createdAt=datetime.now(),
    )


def mock_user(roomId=1, name="princess.wiggles"):
    global user_count
    user_count += 1
    return User(
        name=name,
        roomId=roomId,
        id=user_count
    )


def test_add_remove_user():
    room = mock_room()
    user = mock_user()
    manager = ConnectionManager()
    assert manager.empty == True
    manager.add_user(room, user, None)
    assert manager.empty == False
    manager.remove_user(room, user, None)
    assert manager.empty == True
