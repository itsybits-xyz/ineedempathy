from typing import Generator, Dict

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.main import app
from backend.deps import get_db
from backend.database import Base


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
test_client = TestClient(app)


def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_root():
    rv = test_client.get("/")
    assert rv.status_code == 200
    assert rv.headers["content-type"] == "application/json"
    assert rv.json()['msg'] == "Check /docs"


def create_room(type: str):
    room = test_client.post(
        "/rooms",
        json={"type": type},
    )
    assert room.status_code == 201
    return room.json()


def create_user(room: Dict):
    user = test_client.post(
        f"/rooms/{room['name']}/user",
        json={},
    )
    assert user.status_code == 201
    return user.json()


def test_create_room():
    room = create_room("singleplayer")
    assert len(list(room.keys())) == 4
    assert type(room['id']) == int
    assert type(room['name']) == str
    assert room['type'] == 'singleplayer'
    assert type(room['createdAt']) == str


def test_create_user():
    room = create_room("singleplayer")
    user = create_user(room)
    assert len(list(user.keys())) == 3
    assert user['roomId'] == room['id']
    assert type(user['id']) == int
    assert type(user['name']) == str


def test_create_story():
    response = test_client.post(
        "/rooms/1/story",
        json={
            "user_id": 1,
            "card_id": 10,
            "description": 'meow'
        },
    )
    assert response.status_code == 201
    json = response.json()
    assert len(list(json.keys())) == 5
    assert json['roomId'] == 1
    assert json['userId'] == 1
    assert json['cardId'] == 10
    assert json['description'] == 'meow'


def test_create_guess():
    response = test_client.post(
        "/rooms/1/story/1/guess",
        json={
            "user_id": 1,
            "card_id": 10
        },
    )
    assert response.status_code == 201
    json = response.json()
    assert len(list(json.keys())) == 5
    assert json['room_id'] == 1
    assert json['user_id'] == 1
    assert json['card_id'] == 10
    assert json['story_id'] == 1


def test_create_card():
    response = test_client.post(
        "/cards",
        json={
            "name": 'angry',
            "type": 'feeling'
        },
    )
    assert response.status_code == 201
    json = response.json()
    assert len(list(json.keys())) == 5
    assert json['id'] == 1
    assert json['name'] == 'angry'
    assert json['type'] == 'feeling'
    assert json['textUrl'] == '/static/angry.jpg'
    assert json['blankUrl'] == '/static/angry_blank.jpg'


def socket_url(room, user):
    return f"/rooms/{room['name']}/users/{user['name']}.ws"


def test_invalid_websocket_connect():
    try:
        client = TestClient(app)
        room = {"name" : "fake-room"}
        user = {"name" : "fake-user"}
        client.websocket_connect(socket_url(room, user))
        assert False
    except RuntimeError:
        assert True


def test_websocket_connect():
    client = TestClient(app)
    room = create_room("singleplayer")
    user = create_user(room)
    with client.websocket_connect(socket_url(room, user)) as websocket:
        data = websocket.receive_json()
        assert data == {
            "status": "WRITING",
            "waitingOn": [user.get("id")],
            "currentUsers": [
                {
                    "id": user.get("id"),
                    "name": user.get("name"),
                    "room_id": room.get("id")
                }
            ],
        }


def test_websocket_with_multiple_connections():
    client = TestClient(app)
    room = create_room("singleplayer")
    user_1 = create_user(room)
    user_2 = create_user(room)
    # connect user_1
    with client.websocket_connect(socket_url(room, user_1)) as websocket_1:
        data_1 = websocket_1.receive_json()
        assert data_1 == {
            "status": "WRITING",
            "waitingOn": [user_1.get("id")],
            "currentUsers": [
                {
                    "id": user_1.get("id"),
                    "name": user_1.get("name"),
                    "room_id": room.get("id")
                }
            ],
        }
        # connect user_2 - first client
        with client.websocket_connect(socket_url(room, user_2)) as websocket_2:
            data_1 = websocket_1.receive_json()
            data_2 = websocket_2.receive_json()
            assert data_1 == data_2
            assert data_2 == {
                "status": "WRITING",
                "waitingOn": [user_1.get("id"), user_2.get("id")],
                "currentUsers": [
                    {
                        "id": user_1.get("id"),
                        "name": user_1.get("name"),
                        "room_id": room.get("id")
                    }, {
                        "id": user_2.get("id"),
                        "name": user_2.get("name"),
                        "room_id": room.get("id")
                    }
                ],
            }
            # connect user_2 - second client
            with client.websocket_connect(socket_url(room, user_2)) as websocket_3:
                data_1 = websocket_1.receive_json()
                data_2 = websocket_2.receive_json()
                data_3 = websocket_3.receive_json()
                assert data_1 == data_2
                assert data_2 == data_3
                assert data_3 == {
                    "status": "WRITING",
                    "waitingOn": [user_1.get("id"), user_2.get("id")],
                    "currentUsers": [
                        {
                            "id": user_1.get("id"),
                            "name": user_1.get("name"),
                            "room_id": room.get("id")
                        }, {
                            "id": user_2.get("id"),
                            "name": user_2.get("name"),
                            "room_id": room.get("id")
                        }
                    ],
                }
                # disconnect user_2 - first client
                websocket_3.close()
            data_1 = websocket_1.receive_json()
            data_2 = websocket_2.receive_json()
            assert data_1 == data_2
            assert data_2 == {
                "status": "WRITING",
                "waitingOn": [user_1.get("id"), user_2.get("id")],
                "currentUsers": [
                    {
                        "id": user_1.get("id"),
                        "name": user_1.get("name"),
                        "room_id": room.get("id")
                    }, {
                        "id": user_2.get("id"),
                        "name": user_2.get("name"),
                        "room_id": room.get("id")
                    }
                ],
            }
            # disconnect user_2 - first client
            websocket_2.close()
        # client_1 gets update
        data_1 = websocket_1.receive_json()
        assert data_1 == {
            "status": "WRITING",
            "waitingOn": [user_1.get("id")],
            "currentUsers": [
                {
                    "id": user_1.get("id"),
                    "name": user_1.get("name"),
                    "room_id": room.get("id")
                }
            ],
        }
        websocket_1.close()
