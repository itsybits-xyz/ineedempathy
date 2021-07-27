from typing import Generator, Dict

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.main import app
from backend.deps import get_db
from backend.database import Base
import pytest


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
    assert rv.json()["msg"] == "Check /docs"


def test_create_room():
    response = test_client.post("/rooms", json={})
    assert response.status_code == 201
    json = response.json()
    assert len(list(json.keys())) == 3
    assert json["id"] == 1
    assert len(json["name"]) >= 1
    assert len(json["createdAt"]) >= 1


def test_create_card():
    response = test_client.post(
        "/cards",
        json={"name": "angry", "type": "feeling"},
    )
    assert response.status_code == 201
    json = response.json()
    assert len(list(json.keys())) == 5
    assert json["id"] == 1
    assert json["name"] == "angry"
    assert json["type"] == "feeling"
    assert json["textUrl"] == "/static/angry.jpg"
    assert json["blankUrl"] == "/static/angry_blank.jpg"


def test_get_card():
    response = test_client.post(
        "/cards",
        json={"name": "compersion", "type": "feeling"},
    )
    assert response.status_code == 201
    response = test_client.get("/cards/compersion")
    assert response.status_code == 200
    json = response.json()
    assert len(list(json.keys())) == 5
    assert json["id"] == 1
    assert json["name"] == "compersion"
    assert json["type"] == "feeling"
    assert json["textUrl"] == "/static/compersion.jpg"
    assert json["blankUrl"] == "/static/compersion_blank.jpg"


def test_create_and_get_comment():
    card_resp = test_client.post(
        "/cards",
        json={"name": "compersion", "type": "feeling"},
    )
    assert card_resp.status_code == 201
    card_json = card_resp.json()
    print(card_json)
    post_response = test_client.post(
        "/cards/compersion/comments",
        json={
            "cardId": card_json["id"],
            "type": "NEED_MET",
            "data": "princess.wiggles"
        }
    )
    assert post_response.status_code == 201
    comment_response = test_client.get(
        "/cards/compersion/comments",
    )
    assert comment_response.status_code == 200
    json = comment_response.json()
    assert len(json) == 1
    comment = json[0]
    assert len(list(comment.keys())) == 5
    assert comment["id"]
    assert comment["cardId"] == card_json["id"]
    assert comment["type"] == "NEED_MET"
    assert comment["data"] == "princess.wiggles"
    assert comment["createdAt"]


def __socket_url(room, user):
    return f"/rooms/{room['name']}/users/{user['name']}.ws"


def __test_invalid_websocket_connect():
    try:
        client = TestClient(app)
        room = {"name": "fake-room"}
        user = {"name": "fake-user"}
        client.websocket_connect(socket_url(room, user))
        assert False
    except RuntimeError:
        assert True


def __test_websocket_connect():
    client = TestClient(app)
    room = create_room("singleplayer")
    user = create_user(room)
    with client.websocket_connect(socket_url(room, user)) as websocket:
        data = websocket.receive_json()
        assert data == {
            "status": "WRITING",
            "progress": {
                f"{user.get('id')}": {"completed": 0, "pending": 1},
            },
            "stories": [],
            "users": [{"id": user.get("id"), "name": user.get("name"), "room_id": room.get("id")}],
        }
