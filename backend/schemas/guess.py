from fastapi_camelcase import CamelModel


# Shared properties
class GuessBase(CamelModel):
    card_id: int


# Properties shared by models stored in DB
class GuessInDBBase(GuessBase):

    class Config:
        orm_mode = True


# Properties to return to client
class Guess(GuessInDBBase):

    class Config:
        arbitrary_types_allowed = True


# Properties properties stored in DB
class GuessInDB(GuessInDBBase):
    id: int
    story_id: int
    scene_id: int
    pass
