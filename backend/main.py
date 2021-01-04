from typing import List, Dict, Optional

from fastapi.staticfiles import StaticFiles
from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
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
from .schemas import User, UserInfo
from .schemas import StoryCreate, Story
from .schemas import GuessCreate, Guess
from .middleware import EmpathyEventMiddleware, EmpathyMansion


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

app.add_middleware(EmpathyEventMiddleware)


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


@app.post("/rooms/{room_id}/story", status_code=201, response_model=Story)
def create_story(room_id: int, story: StoryCreate, db: Session = Depends(get_db)) -> models.Story:
    return crud.create_story(db, room_id, story)


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
    print("Connecting new user...")
    empathy_mansion: Optional[EmpathyMansion] = scope.get("empathy_mansion")
    if empathy_mansion is None:
        raise RuntimeError("Global `empathy_mansion` instance unavailable!")
    room = crud.get_room_by_name(db, room_name)
    if room is None:
        raise RuntimeError(f"Room instance '{room_name}' unavailable!")
    user = crud.get_user_by_name(db, user_name)
    if user is None or user.room_id != room.id:
        raise RuntimeError(f"User instance  '{user_name}' unavailable!")
    try:
        await websocket.accept()
        empathy_mansion.add_user(room, user, websocket)
        print("send_update1")
        await empathy_mansion.send_update(room)
        while True:
            await websocket.receive_json()
            print("send_update2")
            await empathy_mansion.send_update(room)
    except WebSocketDisconnect:
        empathy_mansion.remove_user(room, user)
        print("send_update3")
        await empathy_mansion.send_update(room)
