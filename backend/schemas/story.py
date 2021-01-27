from fastapi_camelcase import CamelModel


# Shared properties
class StoryBase(CamelModel):
    user_id: int
    description: str


# Properties to receive via API on creation
class StoryCreate(StoryBase):
    user_id: int
    card_id: int
    description: str


class StoryInDBBase(StoryBase):
    id: int

    class Config:
        orm_mode = True


# Additional properties to return via API
class Story(StoryInDBBase):
    user_id: int
    room_id: int
    description: str


# Additional properties stored in DB
class StoryInDB(StoryInDBBase):
    room_id: int
    card_id: int
    pass
