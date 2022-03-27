from typing import Generator

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from backend.main import app
from backend import crud
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
        ),
    )
    response = test_client.get("/api/cards/compersion")
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


def upsert_story(db, display_name, scenes):
    story = crud.upsert_story(
        db=db,
        display_name=display_name,
        scenes=scenes
    )

    db_scenes = []
    db_guesses = []

    i = 0
    for scene in scenes:
        i += 1
        db_scene = crud.upsert_scene(
            db=db,
            story_id=story.id,
            noun=scene.get('noun'),
            position=i,
            description=scene.get('description')
        )

        db_scenes.append(db_scene)

        db_guesses.append(crud.upsert_guess(
            db=db,
            story_id=story.id,
            scene_id=db_scene.id,
            card_id=scene.get('feeling_id')
        ))
        db_guesses.append(crud.upsert_guess(
            db=db,
            story_id=story.id,
            scene_id=db_scene.id,
            card_id=scene.get('need_id')
        ))
    return story


def test_full_story():
    db = TestingSessionLocal()
    scared = crud.upsert_card(
        db=db,
        card=CardCreate(
            display_name="Scared",
            name="scared",
            type="feeling",
            level=4,
            definition=":,(",
            definition_source="",
        ),
    )
    hopeful = crud.upsert_card(
        db=db,
        card=CardCreate(
            display_name="Hopeful",
            name="hopeful",
            type="feeling",
            level=4,
            definition=":o !",
            definition_source="",
        ),
    )
    harmony = crud.upsert_card(
        db=db,
        card=CardCreate(
            display_name="Harmony",
            name="harmony",
            type="need",
            level=4,
            definition=":<3",
            definition_source="",
        ),
    )
    ease = crud.upsert_card(
        db=db,
        card=CardCreate(
            display_name="Ease",
            name="ease",
            type="need",
            level=4,
            definition="<3",
            definition_source="",
        ),
    )
    story = upsert_story(
        db=db,
        display_name='The Itsy Bitsy Spider',
        scenes=[
            {
                'description': ' '.join([
                    'The Itsy Bisty Spider went up the water spout.',
                    'Down came the ran and washed the spider out.',
                ]),
                'noun': 'the spider',
                'feeling_id': scared.id,
                'need_id': harmony.id
            },
            {
                'description': ' '.join([
                    'Up came the sun and dried up all the rain.',
                    'So the Itsy Bitsy Spider went up the spout again.',
                ]),
                'noun': 'the spider',
                'feeling_id': hopeful.id,
                'need_id': harmony.id
            }
        ]
    )
    scenes = crud.get_scenes(db=db, story_id=story.id)
    # New Guess
    response = test_client.post(f"/api/stories/{story.id}/scenes/{scenes[0].id}/guesses/{ease.id}")
    assert response.status_code == 201

    # Test Story
    response = test_client.get(f"/api/stories/{story.id}")
    assert response.status_code == 200
    res_story = response.json()
    assert res_story["displayName"] == "The Itsy Bitsy Spider"

    # Test Scene
    response = test_client.get(f"/api/stories/{story.id}/scenes/{scenes[0].id}")
    res_scene = response.json()
    assert len(res_scene["cardGuesses"]) == 3
    response = test_client.get(f"/api/stories/{story.id}/scenes/{scenes[1].id}")
    res_scene = response.json()
    assert len(res_scene["cardGuesses"]) == 2


def test_upsert_new_card():
    db = TestingSessionLocal()
    crud.upsert_card(
        db=db,
        card=CardCreate(
            display_name="Compersion!",
            name="compersion-2",
            type="feeling",
            level=2,
            definition="<33",
            definition_source="<33.com",
        ),
    );
    card = crud.get_card(db, 'compersion-2');
    assert card.display_name == 'Compersion!';
    assert card.type == 'feeling';
    assert card.level == 2;
    assert card.definition == '<33';
    assert card.definition_source == '<33.com';


def test_upsert_existing_card():
    db = TestingSessionLocal()
    card = crud.create_card(
        db=db,
        card=CardCreate(
            display_name="Compersion",
            name="compersion",
            type="need",
            level=1,
            definition="<3",
            definition_source="<3.com",
        ),
    );
    crud.upsert_card(
        db=db,
        card=CardCreate(
            display_name="Compersion!",
            name="compersion",
            type="feeling",
            level=2,
            definition="<33",
            definition_source="<33.com",
        ),
    );
    card = crud.get_card(db, 'compersion');
    assert card.display_name == 'Compersion!';
    assert card.type == 'feeling';
    assert card.level == 2;
    assert card.definition == '<33';
    assert card.definition_source == '<33.com';


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
        ),
    )
    post_response = test_client.post(
        f"/api/cards/{card.name}/comments", json={
            "cardId": card.id,
            "type": "NEED_MET",
            "data": "princess.wiggles"
        }
    )
    assert post_response.status_code == 201
    comment_response = test_client.get(
        f"/api/cards/{card.name}/comments",
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


def test_invalid_comment():
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
        ),
    )
    with pytest.raises(ValueError):
        post_response = test_client.post(
            f"/api/cards/{card.name}/comments", json={
                "cardId": card.id,
                "type": "NEED_MET",
                "data": "",
            }
        )


def socket_url(room_token, user_token):
    return f"/api/rooms/{room_token}.ws"


def test_websocket_add_cards():
    user_token = "user.princess.wiggles"
    room_name = 'empatymeplease.1'
    client = TestClient(app)
    with client.websocket_connect(socket_url(room_name, user_token)) as websocket:
        websocket.send_text('{"setName": "' + user_token + '"}')
        websocket.receive_json()  # join "status" not asserted
        websocket.send_text('{"toggleCard": 1}')
        data = websocket.receive_json()
        assert data == {
            "users": [{"name": user_token, "speaker": True, "cards": [1]}],
        }
        websocket.send_text('{"toggleCard": 4}')
        data = websocket.receive_json()
        assert data == {
            "users": [{"name": user_token, "speaker": True, "cards": [1, 4]}],
        }
        websocket.send_text('{"toggleCard": 4}')
        data = websocket.receive_json()
        assert data == {
            "users": [{"name": user_token, "speaker": True, "cards": [1]}],
        }


def test_websocket_connect():
    room_name = 'empatymeplease.2'
    user_token = "user.princess.wiggles"
    user_token_2 = "user.princess.wiggles.2"
    client = TestClient(app)
    with client.websocket_connect(socket_url(room_name, user_token)) as websocket:
        websocket.send_text('{"setName": "' + user_token + '"}')
        data = websocket.receive_json()
        assert data == {
            "users": [{"name": user_token, "speaker": True, "cards": []}],
        }
        with client.websocket_connect(socket_url(room_name, user_token_2)) as websocket_2:
            websocket_2.send_text('{"setName": "' + user_token_2 + '"}')
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
            "users": [{"name": user_token, "speaker": True, "cards": []}],
        }
