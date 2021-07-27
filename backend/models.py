from sqlalchemy import Boolean, Column, DateTime, ForeignKey
from sqlalchemy import Integer, String, Text, Enum
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from .database import Base
from sqlalchemy.sql import func


class Card(Base):
    __tablename__ = "cards"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    type = Column(Enum("need", "feeling", name="type"), nullable=False, index=True)
    level = Column(Integer, nullable=False, index=True)

    @hybrid_property
    def text_url(self):
        return '/static/' + self.name + '.jpg'

    @hybrid_property
    def blank_url(self):
        return '/static/' + self.name + '_blank.jpg'


class Room(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)


class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    card_id = Column(Integer, ForeignKey("cards.id"))
    type = Column(Enum("NEED_MET", "NEED_NOT_MET", "DEFINE", "THINK", name="type"), nullable=False, index=True)
    data = Column(Text, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
