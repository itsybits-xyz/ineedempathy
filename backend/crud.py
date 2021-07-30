from typing import Optional, List
from sqlalchemy.orm import Session

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
