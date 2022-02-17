import pytest
from app.config import settings as s
from app.database import Base, get_db
from app.main import app
from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.testclient import TestClient
from sqlalchemy import create_engine

# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# from alembic import command


DB_URL = f"postgresql://{s.fastapi_db_user}:{s.fastapi_db_password}@{s.fastapi_db_url}:{s.fastapi_db_port}/{s.fastapi_db_name}_test"
engine = create_engine(DB_URL)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    # command.upgrade("head")

    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):

    user_data = {"email": "egon@gmail.com", "password": "ghostyboys123"}

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could Not Validate Credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    resp = client.post("/users/", json=user_data)

    logged_user = resp.json()
    logged_user["password"] = user_data["password"]
    logged_user["cred_err"] = credentials_exception
    assert resp.status_code == 201
    yield logged_user
