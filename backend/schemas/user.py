from fastapi_camelcase import CamelModel


# Shared properties
class UserBase(CamelModel):
    name: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    name: str


class UserInDBBase(UserBase):
    id: int

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    name: str
    room_id: int


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
