"""
CRUD operations for Snake Game database models
"""

from datetime import datetime
from typing import List, Optional

import models
import schemas
from sqlalchemy import desc, func
from sqlalchemy.orm import Session


# User CRUD operations
def get_user(db: Session, user_id: int) -> Optional[models.User]:
    """Get a user by ID"""
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    """Get a user by username"""
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """Get a user by email"""
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    """Get all users with pagination"""
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """Create a new user"""
    db_user = models.User(username=user.username, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(
    db: Session, user_id: int, user_update: schemas.UserUpdate
) -> Optional[models.User]:
    """Update a user"""
    db_user = get_user(db, user_id)
    if not db_user:
        return None

    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)

    db_user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> bool:
    """Delete a user"""
    db_user = get_user(db, user_id)
    if not db_user:
        return False

    db.delete(db_user)
    db.commit()
    return True


# Game CRUD operations
def get_game(db: Session, game_id: int) -> Optional[models.Game]:
    """Get a game by ID"""
    return db.query(models.Game).filter(models.Game.id == game_id).first()


def get_games_by_user(
    db: Session, user_id: int, skip: int = 0, limit: int = 100
) -> List[models.Game]:
    """Get all games for a specific user"""
    return (
        db.query(models.Game)
        .filter(models.Game.user_id == user_id)
        .order_by(desc(models.Game.started_at))
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_game(db: Session, game: schemas.GameCreate) -> models.Game:
    """Create a new game"""
    db_game = models.Game(user_id=game.user_id, game_mode=game.game_mode)
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game


def update_game(
    db: Session, game_id: int, game_update: schemas.GameUpdate
) -> Optional[models.Game]:
    """Update a game"""
    db_game = get_game(db, game_id)
    if not db_game:
        return None

    update_data = game_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_game, field, value)

    db.commit()
    db.refresh(db_game)
    return db_game


def complete_game(
    db: Session, game_id: int, final_score: int, snake_length: int
) -> Optional[models.Game]:
    """Mark a game as completed"""
    db_game = get_game(db, game_id)
    if not db_game:
        return None

    db_game.score = final_score
    db_game.snake_length = snake_length
    db_game.ended_at = datetime.utcnow()
    db_game.is_completed = True

    if db_game.started_at and db_game.ended_at:
        duration = (db_game.ended_at - db_game.started_at).total_seconds()
        db_game.duration_seconds = int(duration)

    db.commit()
    db.refresh(db_game)
    return db_game


# LeaderboardEntry CRUD operations
def get_leaderboard(
    db: Session, game_mode: Optional[models.GameMode] = None, limit: int = 10
) -> List[dict]:
    """Get leaderboard entries with user information"""
    query = db.query(models.LeaderboardEntry, models.User.username).join(models.User)

    if game_mode:
        query = query.filter(models.LeaderboardEntry.game_mode == game_mode)

    results = query.order_by(desc(models.LeaderboardEntry.score)).limit(limit).all()

    return [
        {
            "id": entry.id,
            "user_id": entry.user_id,
            "username": username,
            "score": entry.score,
            "snake_length": entry.snake_length,
            "game_mode": entry.game_mode,
            "rank": entry.rank,
            "created_at": entry.created_at,
        }
        for entry, username in results
    ]


def create_leaderboard_entry(
    db: Session, entry: schemas.LeaderboardEntryCreate
) -> models.LeaderboardEntry:
    """Create a new leaderboard entry"""
    db_entry = models.LeaderboardEntry(
        user_id=entry.user_id,
        game_id=entry.game_id,
        score=entry.score,
        snake_length=entry.snake_length,
        game_mode=entry.game_mode,
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)

    # Update rank
    update_leaderboard_ranks(db, entry.game_mode)

    return db_entry


def update_leaderboard_ranks(db: Session, game_mode: Optional[models.GameMode] = None):
    """Update ranks for all leaderboard entries"""
    query = db.query(models.LeaderboardEntry)

    if game_mode:
        query = query.filter(models.LeaderboardEntry.game_mode == game_mode)

    entries = query.order_by(desc(models.LeaderboardEntry.score)).all()

    for rank, entry in enumerate(entries, start=1):
        entry.rank = rank

    db.commit()


def get_user_best_score(
    db: Session, user_id: int, game_mode: models.GameMode
) -> Optional[int]:
    """Get user's best score for a specific game mode"""
    result = (
        db.query(func.max(models.LeaderboardEntry.score))
        .filter(
            models.LeaderboardEntry.user_id == user_id,
            models.LeaderboardEntry.game_mode == game_mode,
        )
        .scalar()
    )

    return result


def get_user_stats(db: Session, user_id: int) -> dict:
    """Get comprehensive statistics for a user"""
    games_played = (
        db.query(func.count(models.Game.id))
        .filter(models.Game.user_id == user_id, models.Game.is_completed == True)
        .scalar()
    )

    total_score = (
        db.query(func.sum(models.Game.score))
        .filter(models.Game.user_id == user_id, models.Game.is_completed == True)
        .scalar()
        or 0
    )

    best_score = (
        db.query(func.max(models.Game.score))
        .filter(models.Game.user_id == user_id)
        .scalar()
        or 0
    )

    avg_score = (
        db.query(func.avg(models.Game.score))
        .filter(models.Game.user_id == user_id, models.Game.is_completed == True)
        .scalar()
        or 0
    )

    return {
        "user_id": user_id,
        "games_played": games_played or 0,
        "total_score": total_score,
        "best_score": best_score,
        "average_score": round(float(avg_score), 2),
    }
