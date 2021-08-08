from typing import List, Optional
from fastapi import Depends, Request, WebSocket, WebSocketDisconnect, APIRouter
from ..schemas import Card, RoomInfoBase
from ..schemas import Comment, CommentCreate
from coolname import generate_slug
from ..middleware import ConnectionManager
from .. import crud, models
from sqlalchemy.orm import Session
from ..deps import get_db

router = APIRouter()


@router.get("/cards", response_model=List[Card])
def get_cards(
    db: Session = Depends(get_db),
) -> List[models.Card]:
    return crud.get_cards(db)


@router.get("/cards/{name}", response_model=Card)
def get_card_by_name(
    name: str,
    db: Session = Depends(get_db),
) -> models.Card:
    return crud.get_card(db, name)


@router.get("/cards/{card_name}/comments", response_model=List[Comment])
def get_comments(
    card_name: str,
    db: Session = Depends(get_db),
) -> List[models.Card]:
    return crud.get_comments(db, card_name)


@router.post("/cards/{card_name}/comments", status_code=201, response_model=Comment)
def create_comment(card_name: str, comment: CommentCreate, db: Session = Depends(get_db)) -> models.Comment:
    return crud.create_comment(db, card_name, comment)


@router.post("/rooms", status_code=201, response_model=RoomInfoBase)
def create_room(request: Request, db: Session = Depends(get_db)) -> RoomInfoBase:
    connection_manager: Optional[ConnectionManager] = request.scope.get("connection_manager")
    available = None
    while available is None:
        name = generate_slug(4)
        available = not connection_manager.get_room(name)
    return connection_manager.create_room(name)


@router.get("/error")
def error() -> None:
    1 / 0


@router.websocket("/rooms/{room_name}/users/{user_name}.ws")
async def websocket_endpoint(room_name: str, user_name: str, websocket: WebSocket, db: Session = Depends(get_db)):
    print(f"Connecting new socket {id(websocket)}...")
    connection_manager: Optional[ConnectionManager] = websocket.scope.get("connection_manager")
    if connection_manager is None:
        raise RuntimeError("Global `connection_manager` instance unavailable!")
    room = connection_manager.get_room(room_name)
    if room is None:
        raise RuntimeError(f"Room instance '{room_name}' unavailable!")
    try:
        await websocket.accept()
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
        connection_manager.remove_user(room, user_name, websocket)
        await connection_manager.send_update(room)
