from backend.schemas import User, Room, RoomInfo
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
    return User(name=name, roomId=roomId, id=user_count)


def test_empty():
    room = mock_room()
    user = mock_user()
    roominfo = RoomInfo(
        room=room,
        users={},
    )
    assert roominfo.empty() == True
    roominfo.add_user(user, 1)
    roominfo.add_user(user, 2)
    assert roominfo.empty() == False
    roominfo.remove_user(user, 1)
    assert roominfo.empty() == False
    roominfo.remove_user(user, 2)
    assert roominfo.empty() == True


# def test_advance_room_state():
#     room = mock_room()
#     user = mock_user()
#     roominfo = RoomInfo(
#         room=room,
#         users={},
#     )
#     for x in range(6):
#         assert roominfo.status == RoomStatus.WRITING
#         roominfo.advance_status()
#         assert roominfo.status == RoomStatus.GUESSING
#         roominfo.advance_status()
#     roominfo.end_game()
#     assert roominfo.status == RoomStatus.END_GAME
#     roominfo.advance_status()
#     assert roominfo.status == RoomStatus.END_GAME
