from datetime import timedelta, datetime
from typing import Any, List, Dict

from fastapi import Body, Depends, FastAPI, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud, models
from .config import settings
from .deps import get_db
from .schemas import StoryCreate, Story, Room, RoomCreate, User, UserCreate


app = FastAPI()

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


@app.get("/rooms/", response_model=List[Room])
def get_rooms(
    skip: int = 0,
    limit: int = 1000,
    db: Session = Depends(get_db),
) -> List[models.Room]:
    return crud.get_rooms(db, skip, limit)


@app.get("/rooms/{room_id}", response_model=Room)
def get_room(
    room_id: int,
    db: Session = Depends(get_db),
) -> models.Room:
    return crud.get_room(db, room_id)


@app.post("/rooms/", response_model=Room)
def create_room(
    room: RoomCreate,
    db: Session = Depends(get_db)
) -> models.Room:
    return crud.create_room(db, room)


@app.post("/rooms/{room_id}/story", response_model=Story)
def create_story(
    room_id: int,
    story: StoryCreate,
    db: Session = Depends(get_db)
) -> models.Story:
    return crud.create_story(db, room_id, story)


@app.post("/rooms/{room_id}/user", response_model=User)
def create_user(
    room_id: int,
    user: UserCreate,
    db: Session = Depends(get_db)
) -> models.Room:
    return crud.create_user(db, room_id, user)


@app.get("/")
def root() -> Dict:
    return {"msg": "Check /docs"}
