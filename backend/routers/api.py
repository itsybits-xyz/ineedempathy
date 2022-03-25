from typing import List, Optional
from fastapi import Depends, WebSocket, WebSocketDisconnect, APIRouter
from ..schemas import Card, SmallStory, Story, Guess, LargeScene
from ..schemas import Comment, CommentCreate
from ..middleware import ConnectionManager
from .. import crud, models
from sqlalchemy.orm import Session
from ..deps import get_db


router = APIRouter()


@router.get("/stories", response_model=List[SmallStory])
def get_stories(
    db: Session = Depends(get_db),
) -> List[models.Story]:
    return crud.get_stories(db)


@router.get("/stories/{story_id}", response_model=Story)
def get_story(
    story_id: int,
    db: Session = Depends(get_db),
) -> Optional[models.Story]:
    return crud.get_story(db, story_id)


@router.get("/stories/{story_id}/scenes/{scene_id}", response_model=LargeScene)
def get_scene(
    story_id: int,
    scene_id: int,
    db: Session = Depends(get_db),
) -> Optional[models.Scene]:
    return crud.get_scene(db, story_id, scene_id)


@router.post("/stories/{story_id}/scenes/{scene_id}/guesses/{card_id}", status_code=201, response_model=Guess)
def create_guess(
    story_id: int,
    scene_id: int,
    card_id: int,
    db: Session = Depends(get_db),
) -> models.Guess:
    return crud.create_guess(db, story_id, scene_id, card_id)


@router.get("/cards", response_model=List[Card])
def get_cards(
    db: Session = Depends(get_db),
) -> List[models.Card]:
    return crud.get_cards(db)


@router.get("/cards/{name}", response_model=Card)
def get_card_by_name(
    name: str,
    db: Session = Depends(get_db),
) -> Optional[models.Card]:
    return crud.get_card(db, name)


@router.get("/cards/{card_name}/comments", response_model=List[Comment])
def get_comments(
    card_name: str,
    db: Session = Depends(get_db),
) -> List[models.Comment]:
    if comments := crud.get_comments(db, card_name):
        return comments
    return []


@router.post("/cards/{card_name}/comments", status_code=201, response_model=Comment)
def create_comment(card_name: str, comment: CommentCreate, db: Session = Depends(get_db)) -> Optional[models.Comment]:
    return crud.create_comment(db, card_name, comment)


@router.get("/error")
def error() -> None:
    1 / 0


@router.websocket("/rooms/{room_name}.ws")
async def websocket_endpoint(room_name: str, websocket: WebSocket):
    print(f"Connecting new socket {id(websocket)}...")
    connection_manager: Optional[ConnectionManager] = websocket.scope.get("connection_manager")
    if connection_manager is None:
        raise RuntimeError("Global `connection_manager` instance unavailable!")
    room = connection_manager.get_room(room_name)
    user_name = None
    if room is None:
        room = connection_manager.create_room(room_name)
    try:
        await websocket.accept()
        data = await websocket.receive_json()
        user_name = data["setName"]
        connection_manager.add_user(room, user_name, websocket)
        await connection_manager.send_update(room)
        while True:
            data = await websocket.receive_json()
            if "toggleCard" in data:
                connection_manager.toggle_card(room, user_name, data["toggleCard"])
            elif "changeSpeaker" in data:
                connection_manager.change_speaker(room, data["changeSpeaker"])
            await connection_manager.send_update(room)
    except WebSocketDisconnect:
        if user_name:
            connection_manager.remove_user(room, user_name, websocket)
            await connection_manager.send_update(room)
