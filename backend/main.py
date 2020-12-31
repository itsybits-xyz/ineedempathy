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
from starlette.types import ASGIApp, Receive, Scope, Send

from . import crud, models
from .config import settings
from .deps import get_db
from .schemas import CardCreate, Card
from .schemas import Room, RoomCreate
from .schemas import User
from .schemas import StoryCreate, Story
from .schemas import GuessCreate, Guess
from pydantic import BaseModel


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


class UserInfo(BaseModel):
    user: User
    socket: WebSocket

    class Config:
        arbitrary_types_allowed = True


class RoomInfo(BaseModel):
    room_name: str
    room_id: int
    users: Dict[int, UserInfo]

    def get_user(self, user_id: int) -> Optional[UserInfo]:
        if user_id in self.users:
            return self.users[user_id]
        return None

    def add_user(self, userInfo: UserInfo):
        self.users[userInfo.user.id] = userInfo

    async def remove_user(self, user_id: int) -> None:
        if user_id in self.users:
            del self.users[user_id]

    async def broadcast_message(self, msg: Dict) -> None:
        print("sending")
        print(msg)
        for user_id in self.users:
            await self.users[user_id].socket.send_json(msg)


class EmpathyMansion:
    """Room state, comprising connected users."""

    def __init__(self):
        print("Creating new empty room")
        self._rooms: Dict[int, RoomInfo] = {}

    def __len__(self) -> int:
        """Get the number of users in the room."""
        return len(self._rooms)

    @property
    def empty(self) -> bool:
        """Check if the room is empty."""
        return len(self._rooms) == 0

    @property
    def user_list(self) -> List[str]:
        """Return a list of IDs for connected users."""
        return list(self._rooms)

    def add_user(self, room: Room, user: UserInfo) -> None:
        if room.id not in self._rooms:
            self._rooms[room.id] = RoomInfo(
                room_name=room.name,
                room_id=room.id,
                users={},
            )
        self._rooms[room.id].add_user(user)

    def remove_user(self, room_id: int, user_id: int) -> None:
        room = self._rooms.get(room_id)
        if room is None:
            raise ValueError("Room not found")
        room.remove_user(user_id)

    async def broadcast_user_joined(self, room_id: int, user_id: int) -> None:
        room = self._rooms.get(room_id)
        if room is None:
            raise ValueError("Room not found")
        user = room.get_user(user_id)
        if user is None:
            raise ValueError("User not found")
        await room.broadcast_message(
            {
                "type": "USER_JOIN",
                "data": {
                    "user_id": user.user.id,
                    "user_name": user.user.name,
                },
            }
        )

    async def broadcast_user_left(self, room_id: int, user: Optional[User] = None) -> None:
        room = self._rooms.get(room_id)
        if room is None:
            raise ValueError("Room not found")
        if user is None:
            raise ValueError("User not found")
        await room.broadcast_message(
            {
                "type": "USER_LEFT",
                "data": {
                    "user_id": user.id,
                    "user_name": user.name,
                },
            }
        )


class EmpathyEventMiddleware:
    def __init__(self, app: ASGIApp):
        self._app = app
        self._empathy_mansion = EmpathyMansion()

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] in ("lifespan", "http", "websocket"):
            scope["empathy_mansion"] = self._empathy_mansion
        await self._app(scope, receive, send)


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
    await websocket.accept()
    empathy_mansion.add_user(room, UserInfo(user=user, socket=websocket))
    await empathy_mansion.broadcast_user_joined(room.id, user.id)
    try:
        while True:
            await websocket.receive_json()
    except WebSocketDisconnect:
        user = await empathy_mansion.remove_user(room.id, user.id)
        await empathy_mansion.broadcast_user_left(room.id, user)
