from typing import Generator

from fastapi.security import OAuth2PasswordBearer
from .database import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
