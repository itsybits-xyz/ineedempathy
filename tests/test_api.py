from typing import Generator

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.main import app, crud
from backend.deps import get_db
from backend.database import Base
from backend.schemas import CardCreate


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
    response = test_client.post("/rooms")
    assert response.status_code == 201
    json = response.json()
    assert len(list(json.keys())) == 1
    assert len(json["name"]) >= 1


def test_get_card():
    db = TestingSessionLocal()
    crud.create_card(
        db=db,
        card=CardCreate(
            display_name="Compersion",
            name="compersion",
            type="feeling",
            level=1,
            definition="<3",
            definition_source="<3.com",
        )
    )
    response = test_client.get("/cards/compersion")
    assert response.status_code == 200
    json = response.json()
    assert len(list(json.keys())) == 8
    assert json["id"] == 1
    assert json["displayName"] == "Compersion"
    assert json["name"] == "compersion"
    assert json["type"] == "feeling"
    assert json["level"] == 1
    assert json["image"] == {
        "og": "/static/og/compersion.jpg",
        "md": "/static/md/compersion.jpg",
        "lg": "/static/lg/compersion.jpg",
    }


def test_create_and_get_comment():
    db = TestingSessionLocal()
    card = crud.create_card(
        db=db,
        card=CardCreate(
            display_name="Compersion",
            name="compersion",
            type="feeling",
            level=1,
            definition="<3",
            definition_source="<3.com",
        )
    )
    post_response = test_client.post(
        f"/cards/{card.name}/comments",
        json={
            "cardId": card.id,
            "type": "NEED_MET",
            "data": "princess.wiggles"
        }
    )
    assert post_response.status_code == 201
    comment_response = test_client.get(
        f"/cards/{card.name}/comments",
    )
    assert comment_response.status_code == 200
    json = comment_response.json()
    assert len(json) == 1
    comment = json[0]
    assert len(list(comment.keys())) == 5
    assert comment["id"]
    assert comment["type"] == "NEED_MET"
    assert comment["data"] == "princess.wiggles"
    assert comment["createdAt"]


def socket_url(room_token, user_token):
    return f"/rooms/{room_token}/users/{user_token}.ws"


def test_invalid_websocket_connect():
    try:
        client = TestClient(app)
        room = {"name": "fake-room"}
        user = {"name": "fake-user"}
        client.websocket_connect(socket_url(room, user))
        assert False
    except RuntimeError:
        assert True


def test_websocket_add_cards():
    user_token = 'user.princess.wiggles'
    room = test_client.post("/rooms", json={}).json()
    client = TestClient(app)
    with client.websocket_connect(socket_url(room["name"], user_token)) as websocket:
        websocket.receive_json()  # join "status" not asserted
        websocket.send_text('1')
        data = websocket.receive_json()
        assert data == {
            "users": [
                {"name": user_token, "speaker": True, "cards": [1]}
            ],
        }
        websocket.send_text('4')
        data = websocket.receive_json()
        assert data == {
            "users": [
                {"name": user_token, "speaker": True, "cards": [1, 4]}
            ],
        }
        websocket.send_text('4')
        data = websocket.receive_json()
        assert data == {
            "users": [
                {"name": user_token, "speaker": True, "cards": [1]}
            ],
        }


def test_websocket_connect():
    user_token = 'user.princess.wiggles'
    user_token_2 = 'user.princess.wiggles.2'
    room = test_client.post("/rooms", json={}).json()
    client = TestClient(app)
    with client.websocket_connect(socket_url(room["name"], user_token)) as websocket:
        data = websocket.receive_json()
        assert data == {
            "users": [
                {"name": user_token, "speaker": True, "cards": []}
            ],
        }
        with client.websocket_connect(socket_url(room["name"], user_token_2)) as websocket_2:
            data = websocket_2.receive_json()
            assert data == {
                "users": [
                    {"name": user_token, "speaker": True, "cards": []},
                    {"name": user_token_2, "speaker": False, "cards": []},
                ],
            }
            data_2 = websocket.receive_json()
            assert data == data_2
        data = websocket.receive_json()
        assert data == {
            "users": [
                {"name": user_token, "speaker": True, "cards": []}
            ],
        }
