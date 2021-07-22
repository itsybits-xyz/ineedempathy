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
from .schemas import User, Room, RoomCreate
from .schemas import StoryCreate, Story
from .schemas import GuessCreate, Guess
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

@app.get("/cards/{name}", response_model=Card)
def get_card_by_name(
    name: str,
    db: Session = Depends(get_db),
) -> List[models.Card]:
    return crud.get_card(name, db)


@app.post("/cards", status_code=201, response_model=Card)
def create_card(card: CardCreate, db: Session = Depends(get_db)) -> models.Room:
    return crud.create_card(db, card)


@app.get("/rooms/{room_id}", response_model=Room)
def get_room(
    room_id: int,
    db: Session = Depends(get_db),
) -> models.Room:
    return crud.get_room(db, room_id)


@app.post("/rooms", status_code=201, response_model=Room)
def create_room(room: RoomCreate, db: Session = Depends(get_db)) -> models.Room:
    return crud.create_room(db, room)


@app.post("/rooms/{room_id}/story/{story_id}/guess", status_code=201, response_model=Guess)
def create_guess(room_id: int, story_id: int, guess: GuessCreate, db: Session = Depends(get_db)) -> models.Guess:
    return crud.create_guess(db, room_id, story_id, guess)


# @app.post("/rooms/{room_name}/user/{user_name}/transition", status_code=201)
# async def transition_status(room_name: str, request: Request, db: Session = Depends(get_db)):
#     connection_manager: Optional[ConnectionManager] = request.scope.get("connection_manager")
#     if connection_manager is None:
#         raise RuntimeError("Global `connection_manager` instance unavailable!")
#     room = crud.get_room_by_name(db, room_name)
#     if room is None:
#         raise HTTPException(status_code=404, detail="Room not found")
#     await connection_manager.transition(room)
#     # await connection_manager.send_update(room)
#     return


@app.post("/rooms/{room_name}/story", status_code=201, response_model=Story)
async def create_story(
    room_name: str, story_create: StoryCreate, request: Request, db: Session = Depends(get_db)
) -> models.Story:
    connection_manager: Optional[ConnectionManager] = request.scope.get("connection_manager")
    if connection_manager is None:
        raise RuntimeError("Global `connection_manager` instance unavailable!")
    room = crud.get_room_by_name(db, room_name)
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    story = crud.create_story(db, room, story_create)
    schema_story = Story.from_orm(story)
    await connection_manager.add_story(room, schema_story)
    return story


@app.post("/rooms/{room_name}/user", status_code=201, response_model=User)
def create_user(room_name: str, db: Session = Depends(get_db)) -> models.Room:
    room = crud.get_room_by_name(db, room_name)
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return crud.create_user(db, room.id)


@app.get("/")
def root() -> Dict:
    return {"msg": "Check /docs"}


@app.websocket("/rooms/{room_name}/users/{user_name}.ws")
async def websocket_endpoint(room_name: str, user_name: str, websocket: WebSocket, db: Session = Depends(get_db)):
    scope = websocket.scope
    print(f"Connecting new socket {id(websocket)}...")
    connection_manager: Optional[ConnectionManager] = scope.get("connection_manager")
    if connection_manager is None:
        raise RuntimeError("Global `connection_manager` instance unavailable!")
    room = crud.get_room_by_name(db, room_name)
    if room is None:
        raise RuntimeError(f"Room instance '{room_name}' unavailable!")
    user = crud.get_user_by_name(db, user_name)
    if user is None:
        raise RuntimeError(f"User instance '{user_name}' unavailable!")
    if user not in room.users:
        raise RuntimeError(f"User '{user_name}' does not belong to '{room_name}'!")
    try:
        await websocket.accept()
        connection_manager.add_user(room, user, websocket)
        await connection_manager.send_update(room)
        while True:
            await websocket.receive_json()
            await connection_manager.send_update(room)
    except WebSocketDisconnect:
        connection_manager.remove_user(room, user, websocket)
        await connection_manager.send_update(room)
