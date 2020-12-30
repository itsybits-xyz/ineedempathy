from typing import List, Dict, Optional, Any, Tuple
import json

from fastapi.staticfiles import StaticFiles
from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    WebSocket,
)
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from starlette.types import ASGIApp, Receive, Scope, Send
from starlette.endpoints import WebSocketEndpoint

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
    user_id: int
    username: str
    socket: WebSocket

    class Config:
        arbitrary_types_allowed = True


class RoomInfo(BaseModel):
    room_name: str
    room_id: int
    users: Dict[int, UserInfo]

    def add_user(self, user: UserInfo):
        self.users[user.user_id] = user

    def remove_user(self, user_id: int):
        if user_id in self.users:
            del self.users[user_id]

    async def broadcast_message(self, msg: Dict):
        for user in self.users:
            await user.socket.send_json(msg)


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

    def add_user(self, room_id: int, room_name: str, user: UserInfo):
        if room_id not in self._rooms:
            self._rooms[room_id] = RoomInfo(
                room_name=room_name,
                room_id=room_id,
                users={},
            )
        self._rooms[room_id].add_user(user)

    def remove_user(self, room_id: int, user_id: int):
        room = self._rooms.get(room_id)
        if room is None:
            raise ValueError("Room not found")
        room.remove_user(user_id)

    def get_user(self, user_id: str) -> Optional[UserInfo]:
        """TODO Get metadata on a user."""
        return self._user_meta.get(user_id)

    async def broadcast_user_joined(self, room_id: int, user_id: int):
        room = self._rooms.get(room_id)
        if room is None:
            raise ValueError("Room not found")
        user = room.get_user(user_id)
        room.broadcast_message({
            "type": "USER_JOIN",
            "data": {
                "user_id": user.user_id,
                "user_name": user.user_name,
            }
        })

    async def broadcast_user_left(self, room_id: int, user_id: int):
        room = self._rooms.get(room_id)
        if room is None:
            raise ValueError("Room not found")
        user = room.get_user(user_id)
        room.broadcast_message({
            "type": "USER_LEFT",
            "data": {
                "user_id": user.user_id,
                "user_name": user.user_name,
            }
        })


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


@app.post(
    "/rooms/{room_id}/story/{story_id}/guess", status_code=201, response_model=Guess
)
def create_guess(
    room_id: int, story_id: int, guess: GuessCreate, db: Session = Depends(get_db)
) -> models.Guess:
    return crud.create_guess(db, room_id, story_id, guess)


@app.post("/rooms/{room_id}/story", status_code=201, response_model=Story)
def create_story(
    room_id: int, story: StoryCreate, db: Session = Depends(get_db)
) -> models.Story:
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


@app.websocket_route("/ws", name="ws")
class WebsocketLive(WebSocketEndpoint):
    encoding: str = "text"
    session_name: str = ""

    def __init__(self, scope: Scope, receive: Receive, send: Send):
        super().__init__(scope, receive, send)
        self.empathy_mansion: Optional[EmpathyMansion] = None
        self.user_id = None
        self.room_id = None

    async def on_connect(self, websocket: WebSocket):
        print("Connecting new user...")
        empathy_mansion: Optional[EmpathyMansion] = self.scope.get("empathy_mansion")
        if empathy_mansion is None:
            raise RuntimeError("Global `empathy_mansion` instance unavailable!")
        self.empathy_mansion = empathy_mansion
        await websocket.accept()

    async def on_disconnect(self, _websocket: WebSocket, _close_code: int):
        if self.room_id and self.user_id:
            print("Disconnecting user...")
            self.empathy_mansion.remove_user(self.room_id, self.user_id)

    async def on_receive(self, websocket: WebSocket, msg: Any):
        data = json.loads(msg)
        if data['type'] == 'ROOM_JOIN':
            print("Register user...")
            print(data)
            self.room_id = data['data']['room_id']
            self.user_id = data['data']['user_id']
            room_name = data['data']['room_name']
            user_name = data['data']['user_name']
            self.empathy_mansion.add_user(self.room_id, room_name, UserInfo(
                user_id=self.user_id,
                username=user_name,
                socket=websocket,
            ))
        else:
            await websocket.send_json(
                {"type": "ERROR", "msg": "Responds to ROOM_JOIN message only"}
            )


"""
async def websocket_endpoint(websocket: WebSocket):
    empathy_mansion = websocket.scope.get("empathy_mansion")
    await websocket.accept()
    data = await websocket.receive_json()

    data = {
        type: 'ROOM_JOIN',
        data: {
            room_id: int,
            room_name: str,
            user_id: int,
            user_name: str,
        }
    }
    if (data.type == 'ROOM_JOIN') {
        empathy_mansion.add_user(room_id, room_name, UserInfo(
            user_id: int
            username: str
            socket: Websocket
        ));
    } else {
            throw 400 need to room_join
    }
    try:
        while True:
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        print("Stopping WS Reader (received WebSocketDisconnect)")
"""
