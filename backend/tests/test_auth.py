"""
Tests for authentication endpoints
"""

import pytest


def test_signup_success(client, test_user_data):
    """Test successful user signup"""
    response = client.post("/api/auth/signup", json=test_user_data)

    assert response.status_code == 201
    data = response.json()
    assert data["username"] == test_user_data["username"]
    assert data["email"] == test_user_data["email"]
    assert "id" in data
    assert "hashed_password" not in data  # Password should not be exposed


def test_signup_duplicate_username(client, test_user_data):
    """Test signup with duplicate username"""
    # First signup
    client.post("/api/auth/signup", json=test_user_data)

    # Try to signup again with same username
    response = client.post("/api/auth/signup", json=test_user_data)

    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()


def test_login_success(client, test_user_data):
    """Test successful login"""
    # Sign up first
    client.post("/api/auth/signup", json=test_user_data)

    # Login with form data
    response = client.post(
        "/api/auth/login",
        data={
            "username": test_user_data["username"],
            "password": test_user_data["password"],
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, test_user_data):
    """Test login with wrong password"""
    # Sign up first
    client.post("/api/auth/signup", json=test_user_data)

    # Try login with wrong password using form data
    response = client.post(
        "/api/auth/login",
        data={"username": test_user_data["username"], "password": "wrongpassword"},
    )

    assert response.status_code == 401
    assert "incorrect" in response.json()["detail"].lower()


def test_login_nonexistent_user(client):
    """Test login with non-existent user"""
    response = client.post(
        "/api/auth/login", data={"username": "nonexistent", "password": "password123"}
    )

    assert response.status_code == 401


def test_get_current_user(client, authenticated_user):
    """Test getting current authenticated user"""
    response = client.get("/api/auth/me", headers=authenticated_user["headers"])

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == authenticated_user["user"]["username"]
    assert data["id"] == authenticated_user["user"]["id"]


def test_get_current_user_unauthorized(client):
    """Test getting current user without authentication"""
    response = client.get("/api/auth/me")

    assert response.status_code == 401
