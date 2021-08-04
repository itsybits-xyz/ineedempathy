from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy import Integer, String, Text, Enum
from sqlalchemy.ext.hybrid import hybrid_property

from .database import Base
from sqlalchemy.sql import func


class Card(Base):
    __tablename__ = "cards"
    id = Column(Integer, primary_key=True, index=True)
    display_name = Column(String, nullable=False)
    name = Column(String, index=True, nullable=False)
    type = Column(Enum("need", "feeling", name="type"), nullable=False, index=True)
    level = Column(Integer, nullable=False, index=True)
    definition = Column(String, nullable=False)
    definition_source = Column(String, nullable=False)

    @hybrid_property
    def image(self):
        return {
            "og": "/static/og/" + self.name + ".jpg",
            "lg": "/static/lg/" + self.name + ".jpg",
            "md": "/static/md/" + self.name + ".jpg",
        }


class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    card_id = Column(Integer, ForeignKey("cards.id"))
    type = Column(Enum("NEED_MET", "NEED_NOT_MET", "DEFINE", "THINK", name="type"), nullable=False, index=True)
    data = Column(Text, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
