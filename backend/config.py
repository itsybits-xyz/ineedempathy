from typing import List
import os
from pydantic import BaseSettings, AnyHttpUrl

ENV = os.getenv("ENV", "LOCAL")


class Base(BaseSettings):
    TOKEN_EXPIRE_HOURS: int = 48
    PROJECT_NAME: str = "I Need Empathy"
    SERVER_HOST: str = "localhost:8000"
    FRONTEND_HOST: str = "localhost:3000"
    SENTRY_DSN: str = ""


class Local(Base):
    EMAILS_ENABLED = False
    FRONTEND_HOST: str = "localhost:3000"


class Staging(Base):
    EMAILS_ENABLED = False
    SERVER_HOST = "staging.ineedempathy.com"
    FRONTEND_HOST: str = "staging.ineedempathy.com"


class Prod(Base):
    EMAILS_ENABLED = False
    SERVER_HOST = "ineedempathy.com"
    FRONTEND_HOST: str = "ineedempathy.com"
    SENTRY_DSN: str = "https://2147b3c92a9b482eaefc19feaeda5ecd@o948279.ingest.sentry.io/5897486"



print("PYTHON_ENV: " + ENV)
if ENV == "PROD":
    settings = Prod()
elif ENV == "STAGING":
    settings = Staging()
else:
    settings = Local()
