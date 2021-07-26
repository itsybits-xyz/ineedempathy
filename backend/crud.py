from typing import Optional, List
from sqlalchemy.orm import Session
from coolname import generate_slug

from .models import Card, Room
from .schemas import CardCreate, RoomCreate


def get_card(name: str, db: Session) -> Optional[Card]:
    return db.query(Card).filter(Card.name == name).first()


def get_cards(db: Session) -> Optional[Card]:
    return db.query(Card).all()


def create_card(db: Session, card: CardCreate) -> Card:
    db_obj = Card(
        name=card.name,
        type=card.type,
        level=1
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_room_by_name(db: Session, room: str) -> Room:
    return db.query(Room).filter(Room.name == room).first()


def get_rooms(db: Session, skip: int = 0, limit: int = 10) -> List[Room]:
    return db.query(Room).offset(skip).limit(limit).all()


def get_room(db: Session, room_id: int) -> Room:
    return db.query(Room).filter(Room.id == room_id).first()


def create_room(db: Session, room: RoomCreate) -> Room:
    db_room = Room(
        name=generate_slug(4)
    )
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room
