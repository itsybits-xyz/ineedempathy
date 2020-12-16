from typing import Any, Dict, Optional, Union, List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from .models import User, Room
from .schemas import RoomCreate, UserCreate, UserUpdate
from .security import get_password_hash, verify_password


def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    user = get_user_by_email(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def get_user(db: Session, id: int) -> Optional[User]:
    return db.query(User).filter(User.id == id).first()


def get_users(db: Session, skip: int = 0, limit: int = 10) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, obj_in: UserCreate) -> User:
    db_obj = User(
        email=obj_in.email,
        hashed_password=get_password_hash(obj_in.password),
        full_name=obj_in.full_name,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_user(db: Session, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]) -> User:
    obj_data = jsonable_encoder(db_obj)
    if isinstance(obj_in, dict):
        update_data = obj_in
    else:
        update_data = obj_in.dict(exclude_unset=True)
    if update_data["password"]:
        hashed_password = get_password_hash(update_data["password"])
        del update_data["password"]
        update_data["hashed_password"] = hashed_password

    for field in obj_data:
        if field in update_data:
            setattr(db_obj, field, update_data[field])
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def authenticate(db: Session, *, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def is_active(user: User) -> bool:
    return user.is_active


def is_superuser(user: User) -> bool:
    return user.is_superuser


def get_rooms(db: Session, skip: int = 0, limit: int = 10) -> List[Room]:
    return db.query(Room).offset(skip).limit(limit).all()


def get_room(db: Session, user_id: int, room_id: int) -> Room:
    return db.query(Room).filter(Room.user_id == user_id).filter(Room.id == room_id).first()


def create_room(db: Session, room: RoomCreate) -> Room:
    db_room = Room(**room.dict())
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room
