from pydantic import BaseModel


# Shared properties
class GuessBase(BaseModel):
    user_id: int
    card_id: int


# Properties to receive via API on creation
class GuessCreate(GuessBase):
    user_id: int
    card_id: int


class GuessInDBBase(GuessBase):
    id: int

    class Config:
        orm_mode = True


# Additional properties to return via API
class Guess(GuessInDBBase):
    user_id: int
    room_id: int
    story_id: int
    card_id: int


# Additional properties stored in DB
class GuessInDB(GuessInDBBase):
    pass
