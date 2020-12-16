from typing import Optional
from datetime import datetime

from fastapi_camelcase import CamelModel


# Shared properties
class TripBase(CamelModel):
    title: str
    distance: float
    average_speed: Optional[float]
    max_speed: Optional[float]
    duration_s: Optional[int]
    comments: Optional[str]
    date: datetime


# Properties to receive on item creation
class TripCreate(TripBase):
    pass


# Properties to receive on item update
class TripUpdate(TripBase):
    id: int
    pass


# Properties shared by models stored in DB
class TripInDBBase(TripBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Trip(TripInDBBase):
    pass


# Properties properties stored in DB
class TripInDB(TripInDBBase):
    pass
