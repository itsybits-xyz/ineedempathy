from typing import Optional, List
from sqlalchemy.orm import Session

from .models import Card, Comment, Story, Scene, Guess
from .schemas import CardCreate, CommentCreate


def get_card(db: Session, card_name: str) -> Optional[Card]:
    return db.query(Card).filter(Card.name == card_name).first()


def get_cards(db: Session) -> List[Card]:
    return db.query(Card).all()


def get_stories(db: Session) -> List[Story]:
    return db.query(Story).all()


def get_story(db: Session, story_id: int) -> Optional[Story]:
    return db.query(Story).\
        filter(Scene.story_id == story_id).\
        first()


def get_scene(db: Session, story_id: int, scene_id: int) -> Optional[Scene]:
    return db.query(Scene).\
        filter(Scene.id == scene_id).\
        filter(Scene.story_id == story_id).\
        first()


def get_scenes(db: Session, story_id: int) -> List[Scene]:
    return db.query(Scene).\
        filter(Scene.story_id == story_id).\
        order_by(Scene.position).\
        all()


def get_guesses(db: Session, scene_id: int, story_id: int) -> List[Guess]:
    return db.query(Guess).\
        filter(Guess.story_id == story_id).\
        filter(Guess.scene_id == scene_id).\
        all()


def get_comments(db: Session, card_name: str) -> List[Comment]:
    card = get_card(db, card_name)
    if card:
        return db.query(Comment).filter(Comment.card_id == card.id).all()
    return []


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


def upsert_card(db: Session, card: CardCreate) -> Card:
    dbCard = db.query(Card).filter(Card.name == card.name).first()
    if dbCard is not None:
        dbCard.display_name = card.display_name
        dbCard.type = card.type
        dbCard.level = card.level
        dbCard.definition = card.definition
        dbCard.definition_source = card.definition_source
        db.commit()
        return dbCard
    else:
        db_obj = Card(
            display_name=card.display_name,
            name=card.name,
            type=card.type,
            level=card.level,
            definition=card.definition,
            definition_source=card.definition_source
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


def create_card(db: Session, card: CardCreate) -> Card:
    db_obj = Card(
        display_name=card.display_name,
        name=card.name,
        type=card.type,
        level=card.level,
        definition=card.definition,
        definition_source=card.definition_source
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def create_guess(db: Session, story_id: int, scene_id: int, card_id: int) -> Guess:
    guess = Guess(
        story_id=story_id,
        scene_id=scene_id,
        card_id=card_id,
    )
    db.add(guess)
    db.commit()
    db.refresh(guess)
    return guess


def upsert_guess(db: Session, story_id: int, scene_id: int, card_id: int) -> Guess:
    guess = db.query(Guess).\
        filter(Guess.story_id == story_id).\
        filter(Guess.scene_id == scene_id).\
        filter(Guess.card_id == card_id).\
        first()
    if guess is None:
        guess = Guess(
            story_id=story_id,
            scene_id=scene_id,
            card_id=card_id,
        )
        db.add(guess)
        db.commit()
        db.refresh(guess)
    return guess


def upsert_scene(db: Session, story_id: int, noun: str, position: int, description: str) -> Scene:
    scene = db.query(Scene).\
        filter(Scene.story_id == story_id).\
        filter(Scene.position == position).\
        first()
    if scene is None:
        scene = Scene(
            story_id=story_id,
            noun=noun,
            position=position,
            description=description
        )
        db.add(scene)
        db.commit()
        db.refresh(scene)
    return scene


def upsert_story(db: Session, display_name: str, scenes: List[Scene]) -> Story:
    story = db.query(Story).filter(Story.display_name == display_name).first()
    if story is None:
        story = Story(
            display_name=display_name,
        )
        db.add(story)
        db.commit()
        db.refresh(story)
    return story
