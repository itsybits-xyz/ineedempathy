from backend.schemas import User, Room, RoomInfo, RoomType
from datetime import datetime


room_count = 0
user_count = 0


def mock_room(name="princess.mansion"):
    global room_count
    room_count += 1
    return Room(
        id=room_count,
        name=name,
        type=RoomType.Singleplayer,
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


def test_empty():
    room = mock_room()
    user = mock_user()
    roominfo = RoomInfo(
        room=room,
        users={},
    )
    assert roominfo.empty() == True
    roominfo.add_user(user, None)
    assert roominfo.empty() == False
    roominfo.remove_user(user.id)
    assert roominfo.empty() == True
