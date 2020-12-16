from pydantic import BaseModel
from enum import Enum


class CardType(str, Enum):
    Feeling = "feeling"
    Need = "need"


# Shared properties
class CardBase(BaseModel):
    name: str
    type: CardType


# Properties to receive on item creation
class CardCreate(CardBase):
    pass


# Properties to receive on item update
class CardUpdate(CardBase):
    id: int
    pass


# Properties shared by models stored in DB
class CardInDBBase(CardBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Card(CardInDBBase):
    pass


# Properties properties stored in DB
class CardInDB(CardInDBBase):
    pass
