from datetime import timedelta, datetime
from typing import Any, List, Dict

from fastapi import Body, Depends, FastAPI, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud, models
from .config import settings
from .deps import get_current_active_superuser, get_current_active_user, get_db
from .schemas import Room, RoomCreate, User, UserCreate
from .security import (
    create_access_token,
    get_password_hash,
    generate_token,
    verify_token,
)
from .utils import send_new_account_email, send_reset_password_email


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
    current_user: User = Depends(get_current_active_user),
) -> List[models.Room]:
    return [Room("Random Room 1", "closed", datetime.now())]


# @app.get("/rooms/{id}", response_model=Room)
# def get_room(
#     id: int,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_active_user),
# ) -> models.Room:
#     return crud.get_room(db, current_user.id, id)


# @app.post("/rooms/", response_model=Room)
# def create_room_for_user(
#     room: RoomCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)
# ) -> models.Room:
#     return crud.create_room(db, room, current_user.id)


@app.get("/")
def root() -> Dict:
    return {"msg": "Check /docs"}
