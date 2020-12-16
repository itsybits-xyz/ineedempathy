from typing import Optional, List

from sqlalchemy.orm import Session

from .models import User, Room
from .schemas import RoomCreate, UserCreate


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def get_user(db: Session, id: int) -> Optional[User]:
    return db.query(User).filter(User.id == id).first()


def get_users(db: Session, skip: int = 0, limit: int = 10) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, room_id: int, obj_in: UserCreate) -> User:
    print(room_id)
    db_obj = User(
        room_id=room_id,
        name=obj_in.name,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_rooms(db: Session, skip: int = 0, limit: int = 10) -> List[Room]:
    return db.query(Room).offset(skip).limit(limit).all()


def get_room(db: Session, room_id: int) -> Room:
    return db.query(Room).filter(Room.id == room_id).first()


def create_room(db: Session, room: RoomCreate) -> Room:
    db_room = Room(**room.dict())
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room
