import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database.models import Base
from src.database.db import get_db
from main import app

engine = create_engine(
    "sqlite:///./test.db", connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def session():

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def client(session):

    def overrider_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = overrider_get_db

    yield TestClient(app)


@pytest.fixture(scope="module")
def user():
    return {"username": "joe",
            "email": "jonik@gmail.com",
            "password": "567234"
            }