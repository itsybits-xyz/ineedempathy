from enum import Enum
from datetime import datetime

from fastapi_camelcase import CamelModel


# Shared properties
class RoomBase(CamelModel):
    pass


# Properties to receive on item update
class RoomUpdate(RoomBase):
    id: int
    pass


class RoomCreate(RoomBase):
    pass


# Properties shared by models stored in DB
class RoomInDBBase(RoomBase):
    id: int
    name: str
    created_at: datetime

    class Config:
        orm_mode = True


# Properties to return to client
class Room(RoomInDBBase):
    pass


# Properties properties stored in DB
class RoomInDB(RoomInDBBase):
    pass
