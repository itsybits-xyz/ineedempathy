from pydantic import BaseModel


# Shared properties
class TrailBase(BaseModel):
    name: str
    length: float


# Properties to receive on item creation
class TrailCreate(TrailBase):
    pass


# Properties to receive on item update
class TrailUpdate(TrailBase):
    pass


# Properties shared by models stored in DB
class TrailInDBBase(TrailBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Trail(TrailInDBBase):
    pass


# Properties properties stored in DB
class TrailInDB(TrailInDBBase):
    pass
