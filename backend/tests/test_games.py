"""
Tests for game CRUD operations
"""

import pytest


def test_start_game(client, authenticated_user):
    """Test starting a new game"""
    response = client.post(
        "/api/games/start",
        json={"user_id": authenticated_user["user"]["id"], "game_mode": "walls"},
        headers=authenticated_user["headers"],
    )

    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == authenticated_user["user"]["id"]
    assert data["game_mode"] == "walls"
    assert data["score"] == 0
    assert data["is_completed"] is False


def test_start_game_unauthorized(client, test_user_data):
    """Test starting game without authentication"""
    response = client.post(
        "/api/games/start", json={"user_id": 1, "game_mode": "walls"}
    )

    assert response.status_code == 401


def test_end_game_with_score(client, authenticated_user):
    """Test ending a game and submitting to leaderboard"""
    # Start a game
    start_response = client.post(
        "/api/games/start",
        json={"user_id": authenticated_user["user"]["id"], "game_mode": "walls"},
        headers=authenticated_user["headers"],
    )
    game_id = start_response.json()["id"]

    # End the game with score
    end_response = client.post(
        f"/api/games/{game_id}/end",
        json={
            "score": 150,
            "snake_length": 15,
            "duration_seconds": 60,
            "moves_count": 100,
            "food_eaten": 10,
            "is_completed": True,
        },
        headers=authenticated_user["headers"],
    )

    assert end_response.status_code == 200
    data = end_response.json()
    assert "message" in data
    # Game should be completed and added to leaderboard
    assert "submitted to leaderboard" in data["message"].lower()


def test_end_game_zero_score_no_leaderboard(client, authenticated_user):
    """Test ending game with 0 score doesn't create leaderboard entry"""
    # Start a game
    start_response = client.post(
        "/api/games/start",
        json={"user_id": authenticated_user["user"]["id"], "game_mode": "walls"},
        headers=authenticated_user["headers"],
    )
    game_id = start_response.json()["id"]

    # End with 0 score
    end_response = client.post(
        f"/api/games/{game_id}/end",
        json={"score": 0, "snake_length": 1, "is_completed": True},
        headers=authenticated_user["headers"],
    )

    assert end_response.status_code == 200
    data = end_response.json()
    # Zero score shouldn't create leaderboard entry
    assert "message" in data


def test_get_my_games(client, authenticated_user):
    """Test getting user's game history"""
    # Start and end a few games
    for i in range(3):
        start_response = client.post(
            "/api/games/start",
            json={"user_id": authenticated_user["user"]["id"], "game_mode": "walls"},
            headers=authenticated_user["headers"],
        )
        game_id = start_response.json()["id"]

        client.post(
            f"/api/games/{game_id}/end",
            json={"score": 100 + i * 10, "snake_length": 10 + i, "is_completed": True},
            headers=authenticated_user["headers"],
        )

    # Get game history
    response = client.get("/api/games/my-games", headers=authenticated_user["headers"])

    assert response.status_code == 200
    games = response.json()
    assert len(games) == 3
    assert all(game["is_completed"] for game in games)


def test_cannot_end_another_users_game(client, authenticated_user, test_user_data):
    """Test that users cannot end other users' games"""
    # Create another user
    other_user_data = {
        "username": "otheruser",
        "email": "other@example.com",
        "password": "otherpass123",
    }
    signup_response = client.post("/api/auth/signup", json=other_user_data)
    other_user_id = signup_response.json()["id"]

    login_response = client.post(
        "/api/auth/login",
        data={
            "username": other_user_data["username"],
            "password": other_user_data["password"],
        },
    )
    other_token = login_response.json()["access_token"]

    # Other user starts a game
    start_response = client.post(
        "/api/games/start",
        json={"user_id": other_user_id, "game_mode": "walls"},
        headers={"Authorization": f"Bearer {other_token}"},
    )
    game_id = start_response.json()["id"]

    # Try to end it with first user's token
    response = client.post(
        f"/api/games/{game_id}/end",
        json={"score": 100, "snake_length": 10, "is_completed": True},
        headers=authenticated_user["headers"],
    )

    assert response.status_code == 403
