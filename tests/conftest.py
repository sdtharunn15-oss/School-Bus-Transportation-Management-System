import os
import sys

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import Base, get_db
from app.main import app

TEST_DATABASE_URL = "sqlite:///./test.db"

if os.path.exists("test.db"):
    os.remove("test.db")

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture
def db():
    database = TestingSessionLocal()
    try:
        yield database
    finally:
        database.close()


@pytest.fixture
def admin_token():
    client.post(
        "/auth/register",
        json={
            "username": "admin",
            "email": "admin@gmail.com",
            "password": "admin123",
            "role": "Admin"
        }
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "admin@gmail.com",
            "password": "admin123"
        }
    )

    return response.json()["access_token"]


@pytest.fixture
def manager_token():
    client.post(
        "/auth/register",
        json={
            "username": "manager",
            "email": "manager@gmail.com",
            "password": "manager123",
            "role": "Transport Manager"
        }
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "manager@gmail.com",
            "password": "manager123"
        }
    )

    return response.json()["access_token"]


@pytest.fixture
def parent_token():
    client.post(
        "/auth/register",
        json={
            "username": "parent",
            "email": "parent@gmail.com",
            "password": "parent123",
            "role": "Parent"
        }
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "parent@gmail.com",
            "password": "parent123"
        }
    )

    return response.json()["access_token"]