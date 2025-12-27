"""
Tests for leaderboard endpoints
"""
import pytest


def test_get_empty_leaderboard(client):
    """Test getting leaderboard when no games played"""
    response = client.get("/api/leaderboard?limit=10")
    
    assert response.status_code == 200
    assert response.json() == []


def test_get_leaderboard_with_entries(client, authenticated_user):
    """Test getting leaderboard with multiple entries"""
    # Create multiple game sessions
    scores = [150, 200, 100]
    for score in scores:
        start_response = client.post(
            "/api/games/start",
            json={"user_id": authenticated_user["user"]["id"], "game_mode": "walls"},
            headers=authenticated_user["headers"]
        )
        game_id = start_response.json()["id"]
        
        client.post(
            f"/api/games/{game_id}/end",
            json={"score": score, "snake_length": score // 10, "is_completed": True},
            headers=authenticated_user["headers"]
        )
    
    # Get leaderboard
    response = client.get("/api/leaderboard?limit=10")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    # Should be sorted by score descending
    assert data[0]["score"] == 200
    assert data[1]["score"] == 150
    assert data[2]["score"] == 100
    assert all(entry["username"] == authenticated_user["user"]["username"] for entry in data)


def test_get_leaderboard_filtered_by_mode(client, authenticated_user):
    """Test filtering leaderboard by game mode"""
    # Create games in different modes
    modes_and_scores = [
        ("walls", 150),
        ("walls", 200),
        ("pass-through", 100),
        ("pass-through", 250)
    ]
    
    for mode, score in modes_and_scores:
        start_response = client.post(
            "/api/games/start",
            json={"user_id": authenticated_user["user"]["id"], "game_mode": mode},
            headers=authenticated_user["headers"]
        )
        game_id = start_response.json()["id"]
        
        client.post(
            f"/api/games/{game_id}/end",
            json={"score": score, "snake_length": score // 10, "is_completed": True},
            headers=authenticated_user["headers"]
        )
    
    # Get walls-only leaderboard
    response = client.get("/api/leaderboard?game_mode=walls&limit=10")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(entry["game_mode"] == "walls" for entry in data)
    assert data[0]["score"] == 200
    
    # Get pass-through leaderboard
    response = client.get("/api/leaderboard?game_mode=pass-through&limit=10")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(entry["game_mode"] == "pass-through" for entry in data)
    assert data[0]["score"] == 250


def test_get_user_stats(client, authenticated_user):
    """Test getting user statistics"""
    # Play some games
    scores = [100, 150, 200]
    for score in scores:
        start_response = client.post(
            "/api/games/start",
            json={"user_id": authenticated_user["user"]["id"], "game_mode": "walls"},
            headers=authenticated_user["headers"]
        )
        game_id = start_response.json()["id"]
        
        client.post(
            f"/api/games/{game_id}/end",
            json={"score": score, "snake_length": score // 10, "is_completed": True},
            headers=authenticated_user["headers"]
        )
    
    # Get stats
    response = client.get(
        f"/api/leaderboard/stats/{authenticated_user['user']['username']}"
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == authenticated_user["user"]["username"]
    assert data["games_played"] == 3
    assert data["best_score"] == 200
    assert data["total_score"] == 450
    assert data["average_score"] == 150.0


def test_get_user_stats_no_games(client, authenticated_user):
    """Test getting stats for user with no games"""
    response = client.get(
        f"/api/leaderboard/stats/{authenticated_user['user']['username']}"
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["games_played"] == 0
    assert data["best_score"] == 0
    assert data["total_score"] == 0
    assert data["average_score"] == 0


def test_get_stats_nonexistent_user(client):
    """Test getting stats for non-existent user"""
    response = client.get("/api/leaderboard/stats/nonexistentuser")
    
    assert response.status_code == 200
    data = response.json()
    assert "error" in data
    assert data["games_played"] == 0
