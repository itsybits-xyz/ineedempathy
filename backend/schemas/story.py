from pydantic import BaseModel


# Shared properties
class StoryBase(BaseModel):
    user_id: int
    # TODO card_id
    description: str


# Properties to receive via API on creation
class StoryCreate(StoryBase):
    user_id: int
    # TODO card_id
    description: str


class StoryInDBBase(StoryBase):
    id: int

    class Config:
        orm_mode = True


# Additional properties to return via API
class Story(StoryInDBBase):
    user_id: int
    room_id: int
    # TODO card_id
    description: str


# Additional properties stored in DB
class StoryInDB(StoryInDBBase):
    pass
