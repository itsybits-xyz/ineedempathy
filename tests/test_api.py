from typing import Generator

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


def create_room(type):
    room = test_client.post(
        "/rooms",
        json={"type": "singleplayer"},
    )
    assert room.status_code == 201
    return room.json()


def test_create_room():
    room = create_room("singleplayer")
    assert len(list(room.keys())) == 4
    assert type(room['id']) == int
    assert type(room['name']) == str
    assert room['type'] == 'singleplayer'
    assert type(room['createdAt']) == str


def test_create_user():
    room = create_room("singleplayer")
    response = test_client.post(
        f"/rooms/{room['name']}/user",
        json={},
    )
    assert response.status_code == 201
    json = response.json()
    assert len(list(json.keys())) == 3
    assert json['room_id'] == room['id']
    assert type(json['id']) == int
    assert type(json['name']) == str


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
    assert json['room_id'] == 1
    assert json['user_id'] == 1
    assert json['card_id'] == 10
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


def test_incorrect_websocket_connect():
    client = TestClient(app)
    with client.websocket_connect("/ws") as websocket:
        websocket.send_json({"msg": "Hello WebSocket"})
        data = websocket.receive_json()
        assert data == {"type": "ERROR", "msg": "Responds to ROOM_JOIN message only"}


def test_websocket_connect():
    client = TestClient(app)
    with client.websocket_connect("/ws") as websocket:
        websocket.send_json({
            "type": "ROOM_JOIN",
            "data": {
                "room_id": 10,
                "room_name": "princess.tower",
                "user_id": 15,
                "user_name": "princess.wiggles",
            },
        })
        data = websocket.receive_json()
        assert data == {
            "type": "USER_JOIN",
            "data": {
                "user_id": 15,
                "user_name": "princess.wiggles",
            },
        }
