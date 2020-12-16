from enum import Enum
from typing import Optional
from datetime import datetime

from fastapi_camelcase import CamelModel

class RoomType(str, Enum):
    Open = "Open"
    Closed = "Closed"


# Shared properties
class RoomBase(CamelModel):
    name: str
    type: RoomType
    created_at: datetime


# Properties to receive on item creation
class RoomCreate(RoomBase):
    pass


# Properties to receive on item update
class RoomUpdate(RoomBase):
    id: int
    pass


# Properties shared by models stored in DB
class RoomInDBBase(RoomBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Room(RoomInDBBase):
    pass


# Properties properties stored in DB
class RoomInDB(RoomInDBBase):
    pass
