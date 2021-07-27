from typing import Optional, List
from sqlalchemy.orm import Session
from coolname import generate_slug

from .models import Card, Room, Comment
from .schemas import CardCreate, RoomCreate, CommentCreate


def get_card(db: Session, card_name: str) -> Optional[Card]:
    return db.query(Card).filter(Card.name == card_name).first()


def get_cards(db: Session) -> Optional[Card]:
    return db.query(Card).all()


def get_comments(db: Session, card_name: str) -> Optional[Comment]:
    card = get_card(db, card_name)
    return db.query(Comment).filter(Comment.card_id == card.id).all()


def create_comment(db: Session, card_name: str, comment: CommentCreate) -> Optional[Comment]:
    db_obj = Comment(
        card_id=comment.card_id,
        type=comment.type,
        data=comment.data
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


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
