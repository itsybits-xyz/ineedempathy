from typing import Optional, List
import os
from pydantic import BaseSettings, EmailStr, AnyHttpUrl

ENV = os.getenv("ENV", "LOCAL")


class Base(BaseSettings):
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    TOKEN_EXPIRE_HOURS: int = 48
    PROJECT_NAME: str = "iNeedEmpathy"
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = "amjith.r@gmail.com"  # type: ignore
    EMAILS_FROM_NAME: Optional[str] = PROJECT_NAME

    EMAIL_TEMPLATES_DIR: str = "./backend/email-templates"
    SERVER_HOST: str = "localhost:8000"
    FRONTEND_HOST: str = "localhost:3000"


class Local(Base):
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ['http://localhost:3000']
    EMAILS_ENABLED = True
    SECRET_KEY = "079d8755908068f6256de7ef80af86ae773735124eb8849c8a244b8b4913de43"
    FRONTEND_HOST: str = "localhost:3000"
    SMTP_PORT: Optional[int] = 587
    SMTP_HOST: Optional[str] = "smtp.gmail.com"
    SMTP_USER: Optional[str] = "amjith.r@gmail.com"
    SMTP_PASSWORD: Optional[str] = "fzljcwozxgsoqwvg"


class Staging(Base):
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ['http://localhost:3000']
    EMAILS_ENABLED = True
    SECRET_KEY = "fbffe9b96ce60afec7f69497255f2231cbc67d4504182806fc79c61a05e6b4d2"
    SERVER_HOST = "staging.app.ineedempathy.com"
    FRONTEND_HOST: str = "staging.ineedempathy.com"


class Prod(Base):
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ['http://localhost:3000']
    EMAILS_ENABLED = True
    SECRET_KEY = "bff6135efd2011a8aa8c34d4add204e3b5bb6addd804aa65e9cf220b31ec2217"
    SERVER_HOST = "app.ineedempathy.com"
    FRONTEND_HOST: str = "ineedempathy.com"


if ENV == "PROD":
    settings = Prod()
elif ENV == "STAGING":
    settings = Staging()
else:
    settings = Local()
