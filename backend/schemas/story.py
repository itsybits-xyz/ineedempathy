from typing import List
from fastapi_camelcase import CamelModel
from .scene import Scene


# Shared properties
class StoryBase(CamelModel):
    id: int
    display_name: str


# Properties shared by models stored in DB
class StoryInDBBase(StoryBase):
    id: int

    class Config:
        orm_mode = True


class Story(StoryInDBBase):
    scenes: List[Scene]

    class Config:
        arbitrary_types_allowed = True

class SmallStory(StoryInDBBase):

    class Config:
        arbitrary_types_allowed = True



# Properties properties stored in DB
class StoryInDB(StoryInDBBase):
    pass
