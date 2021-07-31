from typing import List, Dict, Optional

from fastapi.staticfiles import StaticFiles
from fastapi import (
    Depends,
    FastAPI,
    Request,
    WebSocket,
    WebSocketDisconnect,
)
from coolname import generate_slug
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import crud, models
from .config import settings
from .deps import get_db
from .schemas import CardCreate, Card, RoomInfoBase
from .schemas import Comment, CommentCreate
from .middleware import ConnectionManagerMiddleware, ConnectionManager


app = FastAPI()
app.mount("/static", StaticFiles(directory="backend/static"), name="static")

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

app.add_middleware(ConnectionManagerMiddleware)


@app.get("/")
def root() -> Dict:
    return {"msg": "Check /docs"}


@app.get("/cards", response_model=List[Card])
def get_cards(
    db: Session = Depends(get_db),
) -> List[models.Card]:
    return crud.get_cards(db)


@app.get("/cards/{name}", response_model=Card)
def get_card_by_name(
    name: str,
    db: Session = Depends(get_db),
) -> models.Card:
    return crud.get_card(db, name)


@app.get("/cards/{card_name}/comments", response_model=List[Comment])
def get_comments(
    card_name: str,
    db: Session = Depends(get_db),
) -> List[models.Card]:
    return crud.get_comments(db, card_name)


@app.post("/cards/{card_name}/comments", status_code=201, response_model=Comment)
def create_comment(
    card_name: str,
    comment: CommentCreate,
    db: Session = Depends(get_db)
) -> models.Comment:
    return crud.create_comment(db, card_name, comment)


@app.post("/rooms", status_code=201, response_model=RoomInfoBase)
def create_room(request: Request, db: Session = Depends(get_db)) -> RoomInfoBase:
    connection_manager: Optional[ConnectionManager] = request.scope.get("connection_manager")
    available = None
    while available is None:
        name = generate_slug(4)
        available = not connection_manager.get_room(name)
    return connection_manager.create_room(name)


@app.websocket("/rooms/{room_name}/users/{user_name}.ws")
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
            card_id = await websocket.receive_json()
            connection_manager.toggle_card(room, user_name, card_id)
            await connection_manager.send_update(room)
    except WebSocketDisconnect:
        connection_manager.remove_user(room, user_name, websocket)
        await connection_manager.send_update(room)
