"""
Pytest configuration and fixtures for backend tests
"""

import sys
from pathlib import Path

# Add parent directory to path so we can import backend modules
sys.path.insert(0, str(Path(__file__).parent.parent))

import models
import pytest
from database import Base, get_db
from fastapi.testclient import TestClient
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Use in-memory SQLite for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for tests"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database for each test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with overridden database"""
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user_data():
    """Sample user data for tests"""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
    }


@pytest.fixture
def authenticated_user(client, test_user_data):
    """Create and authenticate a test user"""
    # Sign up
    signup_response = client.post("/api/auth/signup", json=test_user_data)
    user = signup_response.json()

    # Login with form data
    response = client.post(
        "/api/auth/login",
        data={
            "username": test_user_data["username"],
            "password": test_user_data["password"],
        },
    )

    token = response.json()["access_token"]

    return {
        "token": token,
        "user": user,
        "headers": {"Authorization": f"Bearer {token}"},
    }
