from sqlalchemy import Boolean, Column, DateTime, ForeignKey
from sqlalchemy import Integer, String, Text, Enum
from sqlalchemy.ext.hybrid import hybrid_property
# from sqlalchemy.orm import relationship

from .database import Base
from sqlalchemy.sql import func


class Card(Base):
    __tablename__ = "cards"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    type = Column(Enum("need", "feeling", name="type"), nullable=False, index=True)

    @hybrid_property
    def text_url(self):
        return 'static/' + self.name + '.jpg'

    @hybrid_property
    def blank_url(self):
        return 'static/' + self.name + '_blank.jpg'


class Room(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    type = Column(Enum("open", "closed", name="type"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)

    #users = relationship("User", back_populates="rooms")
    #guesses = relationship("Guess", back_populates="rooms")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    name = Column(String, index=True)
    is_active = Column(Boolean(), default=False)
    is_superuser = Column(Boolean(), default=False)

    #rooms = relationship("Room", back_populates="users")
    #stories = relationship("Story", back_populates="users")
    #guesses = relationship("Guess", back_populates="users")


class Story(Base):
    __tablename__ = "stories"
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    card_id = Column(Integer, ForeignKey("cards.id"))
    description = Column(Text, index=True)


class Guess(Base):
    __tablename__ = "guesses"
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    story_id = Column(Integer, ForeignKey("stories.id"))
    card_id = Column(Integer, ForeignKey("cards.id"))
