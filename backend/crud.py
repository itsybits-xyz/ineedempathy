from typing import Optional, List
from sqlalchemy.orm import Session
from coolname import generate_slug

from .models import Card, Guess, User, Room, Story
from .schemas import CardCreate, RoomCreate, GuessCreate, StoryCreate


def get_user_by_name(db: Session, name: str) -> Optional[User]:
    return db.query(User).filter(User.name == name).first()


def get_cards(db: Session) -> Optional[Card]:
    return db.query(Card).all()


def get_user(db: Session, id: int) -> Optional[User]:
    return db.query(User).filter(User.id == id).first()


def get_users(db: Session, skip: int = 0, limit: int = 10) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()


def create_card(db: Session, card: CardCreate) -> Card:
    db_obj = Card(
        name=card.name,
        type=card.type
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def create_guess(db: Session, room_id: int, story_id: int, obj_in: GuessCreate) -> Guess:
    db_obj = Guess(
        room_id=room_id,
        story_id=story_id,
        user_id=obj_in.user_id,
        card_id=obj_in.card_id,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def create_story(db: Session, room: Room, obj_in: StoryCreate) -> Story:
    db_obj = Story(
        room_id=room.id,
        user_id=obj_in.user_id,
        card_id=obj_in.card_id,
        description=obj_in.description,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def create_user(db: Session, room_id: int) -> User:
    db_obj = User(
        room_id=room_id,
        name=generate_slug(3)
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
        type=room.type,
        name=generate_slug(4)
    )
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room
