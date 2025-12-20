"""
Test script to verify database models and CRUD operations
"""

import crud
import models
import schemas
from database import SessionLocal


def test_models():
    """Test all database models and CRUD operations"""
    db = SessionLocal()

    try:
        print("=" * 60)
        print("Testing Snake Game Database Models")
        print("=" * 60)

        # Test 1: Create Users
        print("\n1. Testing User Creation...")
        user1 = crud.create_user(
            db, schemas.UserCreate(username="player1", email="player1@example.com")
        )
        print(f"   ✓ Created user: {user1.username} (ID: {user1.id})")

        user2 = crud.create_user(
            db, schemas.UserCreate(username="player2", email="player2@example.com")
        )
        print(f"   ✓ Created user: {user2.username} (ID: {user2.id})")

        # Test 2: Get User
        print("\n2. Testing User Retrieval...")
        retrieved_user = crud.get_user_by_username(db, "player1")
        print(f"   ✓ Retrieved user by username: {retrieved_user.username}")

        # Test 3: Create Games
        print("\n3. Testing Game Creation...")
        game1 = crud.create_game(
            db, schemas.GameCreate(user_id=user1.id, game_mode=models.GameMode.WALLS)
        )
        print(
            f"   ✓ Created game for {user1.username} (ID: {game1.id}, Mode: {game1.game_mode})"
        )

        game2 = crud.create_game(
            db,
            schemas.GameCreate(
                user_id=user2.id, game_mode=models.GameMode.PASS_THROUGH
            ),
        )
        print(
            f"   ✓ Created game for {user2.username} (ID: {game2.id}, Mode: {game2.game_mode})"
        )

        # Test 4: Update Games
        print("\n4. Testing Game Updates...")
        updated_game = crud.update_game(
            db,
            game1.id,
            schemas.GameUpdate(
                score=150, snake_length=15, moves_count=100, food_eaten=10
            ),
        )
        print(
            f"   ✓ Updated game {updated_game.id}: Score={updated_game.score}, Length={updated_game.snake_length}"
        )

        # Test 5: Complete Game
        print("\n5. Testing Game Completion...")
        completed_game = crud.complete_game(
            db, game1.id, final_score=150, snake_length=15
        )
        print(
            f"   ✓ Completed game {completed_game.id}: Duration={completed_game.duration_seconds}s"
        )

        # Test 6: Create Leaderboard Entries
        print("\n6. Testing Leaderboard Entry Creation...")
        entry1 = crud.create_leaderboard_entry(
            db,
            schemas.LeaderboardEntryCreate(
                user_id=user1.id,
                game_id=game1.id,
                score=150,
                snake_length=15,
                game_mode=models.GameMode.WALLS,
            ),
        )
        print(
            f"   ✓ Created leaderboard entry for {user1.username}: Score={entry1.score}, Rank={entry1.rank}"
        )

        entry2 = crud.create_leaderboard_entry(
            db,
            schemas.LeaderboardEntryCreate(
                user_id=user2.id,
                game_id=game2.id,
                score=100,
                snake_length=10,
                game_mode=models.GameMode.PASS_THROUGH,
            ),
        )
        print(
            f"   ✓ Created leaderboard entry for {user2.username}: Score={entry2.score}, Rank={entry2.rank}"
        )

        # Test 7: Get Leaderboard
        print("\n7. Testing Leaderboard Retrieval...")
        leaderboard = crud.get_leaderboard(db, limit=10)
        print(f"   ✓ Retrieved leaderboard with {len(leaderboard)} entries:")
        for idx, entry in enumerate(leaderboard, 1):
            print(
                f"      {idx}. {entry['username']}: {entry['score']} points ({entry['game_mode']})"
            )

        # Test 8: Get User Stats
        print("\n8. Testing User Statistics...")
        stats = crud.get_user_stats(db, user1.id)
        print(f"   ✓ Stats for {user1.username}:")
        print(f"      Games Played: {stats['games_played']}")
        print(f"      Best Score: {stats['best_score']}")
        print(f"      Average Score: {stats['average_score']}")

        # Test 9: Get User's Games
        print("\n9. Testing Game Retrieval by User...")
        user_games = crud.get_games_by_user(db, user1.id)
        print(f"   ✓ Found {len(user_games)} games for {user1.username}")

        # Test 10: Test Relationships
        print("\n10. Testing Model Relationships...")
        user_with_games = crud.get_user(db, user1.id)
        print(
            f"   ✓ User {user_with_games.username} has {len(user_with_games.games)} games"
        )
        print(
            f"   ✓ User {user_with_games.username} has {len(user_with_games.leaderboard_entries)} leaderboard entries"
        )

        print("\n" + "=" * 60)
        print("✓ All tests passed successfully!")
        print("=" * 60)

    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback

        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    test_models()
