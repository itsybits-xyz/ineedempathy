from backend.middleware import ConnectionManager


def test_add_room():
    room_token = 'meow.room'
    manager = ConnectionManager()
    assert manager.empty == True
    manager.create_room(room_token)
    assert manager.empty == False
