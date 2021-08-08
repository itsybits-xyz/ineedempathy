from backend.schemas import RoomInfo


def test_upsert_speaker_to_first_player():
    socket = 1
    room_token = 'princess.wiggles.room'
    user_token = 'princess.wiggles.user'
    roominfo = RoomInfo(
        name=room_token,
        users={},
    )
    assert len(roominfo.get_speaker().name) == 0
    roominfo.add_user(user_token, socket)
    assert roominfo.get_speaker().name == user_token


def test_upsert_speaker_to_second_player_if_first_resigns():
    socket = 1
    room_token = 'princess.wiggles.room'
    user_token_1 = 'princess.wiggles.user.1'
    user_token_2 = 'princess.wiggles.user.2'
    roominfo = RoomInfo(
        name=room_token,
        users={},
    )

    # first user joins
    roominfo.add_user(user_token_1, socket)
    assert roominfo.get_speaker().name == user_token_1

    # second user joins
    roominfo.add_user(user_token_2, socket)
    assert roominfo.get_speaker().name == user_token_1

    # speaker leaves
    roominfo.remove_user(user_token_1, socket)
    assert roominfo.get_speaker().name == user_token_2


def test_empty():
    socket_1 = 1
    socket_2 = 2
    room_token = 'princess.wiggles.room'
    user_token = 'princess.wiggles.user'
    roominfo = RoomInfo(
        name=room_token,
        users={},
    )
    assert roominfo.empty() == True
    roominfo.add_user(user_token, socket_1)
    roominfo.add_user(user_token, socket_2)
    assert roominfo.empty() == False
    roominfo.remove_user(user_token, socket_1)
    assert roominfo.empty() == False
    roominfo.remove_user(user_token, socket_2)
    assert roominfo.empty() == True
