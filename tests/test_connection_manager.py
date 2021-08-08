from backend.middleware import ConnectionManager


def test_add_room():
    room_token = 'meow.room'
    manager = ConnectionManager()
    assert manager.empty == True
    manager.create_room(room_token)
    assert manager.empty == False

def test_room_count():
    room_token = 'meow.room'
    manager = ConnectionManager()
    assert len(manager) == 0
    manager.create_room(room_token)
    assert len(manager) == 1

def test_room_count_with_users():
    room_token = 'meow.room'
    user_token = 'user.token'
    user_socket = 'user.socket.1'
    manager = ConnectionManager()
    assert len(manager) == 0
    room = manager.create_room(room_token)
    manager.add_user(room, user_token, user_socket)
    assert len(manager) == 1
    manager.prune_rooms()
    assert len(manager) == 1

def test_auto_prune():
    room_token = 'meow.room'
    user_token = 'user.token'
    user_socket = 'user.socket'
    card_token = 'card.1'
    manager = ConnectionManager()
    assert len(manager) == 0

    # Insert first
    first_room = manager.create_room(room_token + "-first")

    # Insert middle
    for x in range(0, 999):
        room = manager.create_room(room_token + str(x))
        assert room.empty()
        assert len(manager) > 0
    assert len(manager) == 1000

    # Insert last, should push one out
    last_room = manager.create_room(room_token + "-max")
    assert last_room.empty()

    # asserts last room pushed one out
    assert len(manager) == 1000

    # assert newest room is there
    assert last_room.name in manager._rooms

    # assert first room is not there
    assert first_room.name not in manager._rooms
