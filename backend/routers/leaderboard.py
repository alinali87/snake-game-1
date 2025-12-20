"""
Leaderboard endpoints
"""

from typing import List, Optional

import crud
import models
from database import get_db
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/leaderboard", tags=["leaderboard"])


@router.get("", response_model=List[dict])
def get_leaderboard(
    game_mode: Optional[models.GameMode] = Query(
        None, description="Filter by game mode"
    ),
    limit: int = Query(10, ge=1, le=100, description="Number of entries to return"),
    db: Session = Depends(get_db),
):
    """Get leaderboard entries, optionally filtered by game mode"""
    leaderboard = crud.get_leaderboard(db, game_mode=game_mode, limit=limit)
    return leaderboard


@router.get("/stats/{username}", response_model=dict)
def get_user_stats(username: str, db: Session = Depends(get_db)):
    """Get statistics for a specific user"""
    user = crud.get_user_by_username(db, username)
    if not user:
        return {
            "error": "User not found",
            "user_id": None,
            "games_played": 0,
            "total_score": 0,
            "best_score": 0,
            "average_score": 0,
        }

    stats = crud.get_user_stats(db, user.id)
    stats["username"] = username
    return stats
