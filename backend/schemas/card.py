from enum import Enum
from typing import Dict
from fastapi_camelcase import CamelModel


class CardType(str, Enum):
    Feeling = "feeling"
    Need = "need"


# Shared properties
class CardBase(CamelModel):
    display_name: str
    name: str
    type: CardType
    level: int
    definition: str
    definition_source: str


# Properties to receive on item creation
class CardCreate(CardBase):
    pass


# Properties to receive on item update
class CardUpdate(CardBase):
    id: int


# Properties shared by models stored in DB
class CardInDBBase(CardBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Card(CardInDBBase):
    image: Dict

    class Config:
        arbitrary_types_allowed = True


# Properties properties stored in DB
class CardInDB(CardInDBBase):
    pass
