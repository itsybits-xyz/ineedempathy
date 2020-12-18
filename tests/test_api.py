from typing import Generator

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.main import app
from backend.deps import get_db
from backend.database import Base


# Setup a testing db
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db() -> Generator:
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Apply the test db as database dependency.
app.dependency_overrides[get_db] = override_get_db
test_client = TestClient(app)


def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_root():
    rv = test_client.get("/")
    assert rv.status_code == 200
    assert rv.headers["content-type"] == "application/json"
    assert rv.json()['msg'] == "Check /docs"


def test_create_room():
    response = test_client.post(
        "/rooms",
        json={},
    )
    assert response.status_code == 201
    assert len(list(response.json().keys())) == 4
    assert type(response.json()['id']) == int
    assert type(response.json()['name']) == str
    assert type(response.json()['type']) == str
    assert type(response.json()['createdAt']) == str
