from datetime import timedelta
from typing import Any, List, Dict

from fastapi import Body, Depends, FastAPI, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud, models
from .config import settings
from .deps import get_current_active_superuser, get_current_active_user, get_db
from .schemas import Trip, TripCreate, User, UserCreate
from .security import (
    create_access_token,
    get_password_hash,
    generate_token,
    verify_token,
)
from .utils import send_new_account_email, send_reset_password_email


app = FastAPI()

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )


@app.post("/password-recovery/{email}")
def recover_password(email: str, db: Session = Depends(get_db)) -> Any:
    """
    Password Recovery
    """
    user = crud.get_user_by_email(db, email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    password_reset_token = generate_token(email=email)
    send_reset_password_email(email_to=user.email, email=email, token=password_reset_token)
    return {"msg": "Password recovery email sent"}


@app.post("/reset-password/")
def reset_password(token: str = Body(...), new_password: str = Body(...), db: Session = Depends(get_db)) -> Any:
    """
    Reset password
    """
    email = verify_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = crud.get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    elif not crud.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    hashed_password = get_password_hash(new_password)
    user.hashed_password = hashed_password
    db.add(user)
    db.commit()  # type: ignore
    return {"msg": "Password updated successfully"}


@app.post("/confirm/")
def confirm(token: str = Body(..., embed=True), db: Session = Depends(get_db)) -> Any:
    """
    Confirm account creation
    """
    email = verify_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = crud.get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    elif user.is_active:
        raise HTTPException(status_code=400, detail="User already active.")
    user.is_active = True
    db.add(user)
    db.commit()  # type: ignore
    return {"msg": "Account confirmed!"}


@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> Any:
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"}
        )
    if not user.is_active:
        raise HTTPException(
            status_code=401, detail="User hasn't confirmed the account.", headers={"WWW-Authenticate": "Bearer"}
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    if user.is_superuser:
        permissions = "admin"
    else:
        permissions = "user"
    access_token = create_access_token(
        data={"sub": user.email, "permissions": permissions}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/signup")
def signup(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> Any:
    user = crud.get_user_by_email(db, email=form_data.username)
    if user:
        raise HTTPException(
            status_code=409,
            detail="Account already exists",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_in = UserCreate(email=form_data.username, password=form_data.password)
    user = crud.create_user(db, user_in)
    confirmation_token = generate_token(email=user_in.email)
    if settings.EMAILS_ENABLED and user_in.email:
        send_new_account_email(email_to=user_in.email, username=user_in.email, token=confirmation_token)

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    if user.is_superuser:
        permissions = "admin"
    else:
        permissions = "user"
    access_token = create_access_token(
        data={"sub": user.email, "permissions": permissions}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me", response_model=User)
def get_me(current_user: User = Depends(get_current_active_user)) -> User:
    return current_user


@app.post("/users/", response_model=User)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)) -> models.User:
    user = crud.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = crud.create_user(db, user_in)
    confirmation_token = generate_token(email=user_in.email)
    if settings.EMAILS_ENABLED and user_in.email:
        send_new_account_email(email_to=user_in.email, username=user_in.email, token=confirmation_token)
    return user


@app.get("/users/", response_model=List[User])
def get_users(
    response: Response,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
) -> List[models.User]:
    users = crud.get_users(db, skip, limit)
    response.headers["Content-Range"] = f"0-9/{len(users)}"
    return users


@app.get("/trips/", response_model=List[Trip])
def get_trips(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> List[models.Trip]:
    return crud.get_trips(db, current_user.id, skip, limit)


@app.get("/trips/{id}", response_model=Trip)
def get_trip(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> models.Trip:
    return crud.get_trip(db, current_user.id, id)


@app.post("/trips/", response_model=Trip)
def create_trip_for_user(
    trip: TripCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)
) -> models.Trip:
    return crud.create_trip(db, trip, current_user.id)


@app.get("/")
def root() -> Dict:
    return {"msg": "Check /docs"}
