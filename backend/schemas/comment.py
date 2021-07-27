from enum import Enum
from datetime import datetime

from fastapi_camelcase import CamelModel


class CommentType(str, Enum):
    NEED_MET = "NEED_MET"
    NEED_NOT_MET = "NEED_NOT_MET"
    DEFINE = "DEFINE"
    THINK = "THINK"


# Shared properties
class CommentBase(CamelModel):
    card_id: int
    type: CommentType
    data: str


class CommentCreate(CommentBase):
    pass


# Properties shared by models stored in DB
class CommentInDBBase(CommentBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


# Properties to return to client
class Comment(CommentInDBBase):
    pass


# Properties properties stored in DB
class CommentInDB(CommentInDBBase):
    pass
