from typing import List, Dict

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud, models
from .config import settings
from .deps import get_db
from .schemas import Card
from .schemas import Room
from .schemas import User
from .schemas import StoryCreate, Story
from .schemas import GuessCreate, Guess


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


@app.get("/rooms/{room_id}", response_model=Room)
def get_room(
    room_id: int,
    db: Session = Depends(get_db),
) -> models.Room:
    return crud.get_room(db, room_id)


@app.post("/rooms", status_code=201, response_model=Room)
def create_room(
    db: Session = Depends(get_db)
) -> models.Room:
    return crud.create_room(db)


@app.post("/rooms/{room_id}/story/{story_id}/guess", status_code=201, response_model=Guess)
def create_guess(
    room_id: int,
    story_id: int,
    guess: GuessCreate,
    db: Session = Depends(get_db)
) -> models.Guess:
    return crud.create_guess(db, room_id, story_id, guess)


@app.post("/rooms/{room_id}/story", status_code=201, response_model=Story)
def create_story(
    room_id: int,
    story: StoryCreate,
    db: Session = Depends(get_db)
) -> models.Story:
    return crud.create_story(db, room_id, story)


@app.post("/rooms/{room_id}/user", status_code=201, response_model=User)
def create_user(
    room_id: int,
    db: Session = Depends(get_db)
) -> models.Room:
    return crud.create_user(db, room_id)


@app.get("/")
def root() -> Dict:
    return {"msg": "Check /docs"}
