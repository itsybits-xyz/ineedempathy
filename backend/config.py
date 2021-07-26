from typing import List
import os
from pydantic import BaseSettings, AnyHttpUrl

ENV = os.getenv("ENV", "LOCAL")


class Base(BaseSettings):
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    TOKEN_EXPIRE_HOURS: int = 48
    PROJECT_NAME: str = "I Need Empathy"
    SERVER_HOST: str = "localhost:8000"
    FRONTEND_HOST: str = "localhost:3000"


class Local(Base):
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ['http://localhost:3000']
    EMAILS_ENABLED = False
    FRONTEND_HOST: str = "localhost:3000"


class Staging(Base):
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ['http://localhost:3000']
    EMAILS_ENABLED = False
    SERVER_HOST = "staging.app.ineedempathy.com"
    FRONTEND_HOST: str = "staging.ineedempathy.com"


class Prod(Base):
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ['http://localhost:3000']
    EMAILS_ENABLED = False
    SERVER_HOST = "app.ineedempathy.com"
    FRONTEND_HOST: str = "ineedempathy.com"


if ENV == "PROD":
    settings = Prod()
elif ENV == "STAGING":
    settings = Staging()
else:
    settings = Local()
