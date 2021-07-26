from backend.schemas import Room, RoomInfo
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


def test_empty():
    room = mock_room()
    user_token = 'princess.wiggles'
    roominfo = RoomInfo(
        room=room,
        users={},
    )
    assert roominfo.empty() == True
    roominfo.add_user(user_token, 1)
    roominfo.add_user(user_token, 2)
    assert roominfo.empty() == False
    roominfo.remove_user(user_token, 1)
    assert roominfo.empty() == False
    roominfo.remove_user(user_token, 2)
    assert roominfo.empty() == True
