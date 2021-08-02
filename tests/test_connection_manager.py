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
    manager.prune_rooms()
    assert len(manager) == 0

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
    user_socket = 'user.socket.1'
    card_token = 'card.1'
    manager = ConnectionManager()
    assert len(manager) == 0
    room = manager.create_room(room_token)
    manager.add_user(room, user_token, user_socket)
    manager.toggle_card(room, user_token, card_token)
    assert len(manager) == 1
    manager.remove_user(room, user_token, user_socket)
    assert len(manager) == 1
    manager.toggle_card(room, user_token, card_token)
    assert len(manager) == 0
