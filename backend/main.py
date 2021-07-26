from typing import List, Dict, Optional

from fastapi.staticfiles import StaticFiles
from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    Request,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud, models
from .config import settings
from .deps import get_db
from .schemas import CardCreate, Card
from .schemas import Room, RoomCreate
from .middleware import ConnectionManagerMiddleware, ConnectionManager


app = FastAPI()
app.mount("/static", StaticFiles(directory="backend/static"), name="static")

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

app.add_middleware(ConnectionManagerMiddleware)


@app.get("/")
def root() -> Dict:
    return {"msg": "Check /docs"}


@app.get("/rooms", response_model=List[Room])
def get_rooms(
    skip: int = 0,
    limit: int = 1000,
    db: Session = Depends(get_db),
) -> List[models.Room]:
    return crud.get_rooms(db, skip, limit)


@app.get("/cards", response_model=List[Card])
def get_cards(
    db: Session = Depends(get_db),
) -> List[models.Card]:
    return crud.get_cards(db)


@app.post("/cards", status_code=201, response_model=Card)
def create_card(card: CardCreate, db: Session = Depends(get_db)) -> models.Room:
    return crud.create_card(db, card)


@app.get("/cards/{name}", response_model=Card)
def get_card_by_name(
    name: str,
    db: Session = Depends(get_db),
) -> List[models.Card]:
    return crud.get_card(name, db)


@app.get("/rooms/{room_id}", response_model=Room)
def get_room(
    room_id: int,
    db: Session = Depends(get_db),
) -> models.Room:
    return crud.get_room(db, room_id)


@app.post("/rooms", status_code=201, response_model=Room)
def create_room(room: RoomCreate, db: Session = Depends(get_db)) -> models.Room:
    room = crud.create_room(db, room)
    print(room.name)
    return room


@app.post("/rooms/{room_name}/users/{user_token}/card/{card_name}", status_code=201, response_model=Card)
def add_card(room_name: str, user_token: str, card_name: str, websocket: WebSocket, db: Session = Depends(get_db)) -> models.Card:
    scope = websocket.scope
    connection_manager: Optional[ConnectionManager] = scope.get("connection_manager")
    card = crud.get_card(card_name, db)
    room = crud.get_room_by_name(db, room_name)
    connection_manager.add_card(room, user_token, card)


@app.delete("/rooms/{room_name}/users/{user_token}/card/{card_name}", status_code=204)
def remove_card(room_name: str, user_token: str, card_name: str, websocket: WebSocket, db: Session = Depends(get_db)) -> models.Card:
    scope = websocket.scope
    connection_manager: Optional[ConnectionManager] = scope.get("connection_manager")
    card = crud.get_card(card_name, db)
    room = crud.get_room_by_name(db, room_name)
    connection_manager.remove_card(room, user_token, card)


@app.websocket("/rooms/{room_name}/users/{user_token}.ws")
async def websocket_endpoint(room_name: str, user_token: str, websocket: WebSocket, db: Session = Depends(get_db)):
    scope = websocket.scope
    print(f"Connecting new socket {id(websocket)}...")
    connection_manager: Optional[ConnectionManager] = scope.get("connection_manager")
    if connection_manager is None:
        raise RuntimeError("Global `connection_manager` instance unavailable!")
    room = crud.get_room_by_name(db, room_name)
    if room is None:
        raise RuntimeError(f"Room instance '{room_name}' unavailable!")
    try:
        await websocket.accept()
        connection_manager.add_user(room, user_token, websocket)
        await connection_manager.send_update(room)
        while True:
            await websocket.receive_json()
            await connection_manager.send_update(room)
    except WebSocketDisconnect:
        connection_manager.remove_user(room, user_token, websocket)
        await connection_manager.send_update(room)
