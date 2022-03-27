from typing import List
from fastapi_camelcase import CamelModel
from .guess import Guess


# Shared properties
class SceneBase(CamelModel):
    story_id: int
    noun: str
    position: int
    description: str


# Properties shared by models stored in DB
class SceneInDBBase(SceneBase):
    id: int

    class Config:
        orm_mode = True


class Scene(SceneInDBBase):
    class Config:
        arbitrary_types_allowed = True


class LargeScene(SceneInDBBase):
    card_guesses: List[int] = []

    class Config:
        arbitrary_types_allowed = True


# Properties properties stored in DB
class SceneInDB(SceneInDBBase):
    pass
