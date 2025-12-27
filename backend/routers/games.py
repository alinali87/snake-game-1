"""
Game session management endpoints
"""

from typing import List

import crud
import models
import schemas
from auth import get_current_active_user
from database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/games", tags=["games"])


@router.post("/start", response_model=schemas.Game, status_code=status.HTTP_201_CREATED)
async def start_game(
    game_create: schemas.GameCreate,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Start a new game session"""
    # Ensure the user is creating a game for themselves
    if game_create.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot create game for another user",
        )

    game = crud.create_game(db=db, game=game_create)
    return game


@router.patch("/{game_id}", response_model=schemas.Game)
async def update_game_state(
    game_id: int,
    game_update: schemas.GameUpdate,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Update game state (score, length, etc.)"""
    game = crud.get_game(db, game_id)
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Game not found"
        )

    # Verify the game belongs to the current user
    if game.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot update another user's game",
        )

    updated_game = crud.update_game(db, game_id, game_update)
    return updated_game


@router.post("/{game_id}/end", response_model=dict)
async def end_game(
    game_id: int,
    final_data: schemas.GameUpdate,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """End a game and auto-submit to leaderboard"""
    game = crud.get_game(db, game_id)
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Game not found"
        )

    # Verify the game belongs to the current user
    if game.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot end another user's game",
        )

    # Mark game as completed
    completed_game = crud.complete_game(
        db,
        game_id,
        final_score=final_data.score or game.score,
        snake_length=final_data.snake_length or game.snake_length,
    )

    # Auto-submit to leaderboard if score > 0
    leaderboard_entry = None
    if completed_game.score > 0:
        leaderboard_entry = crud.create_leaderboard_entry(
            db,
            schemas.LeaderboardEntryCreate(
                user_id=current_user.id,
                game_id=game_id,
                score=completed_game.score,
                snake_length=completed_game.snake_length,
                game_mode=completed_game.game_mode,
            ),
        )

    # Convert to Pydantic models for serialization
    game_response = schemas.Game.model_validate(completed_game)
    leaderboard_response = (
        schemas.LeaderboardEntry.model_validate(leaderboard_entry)
        if leaderboard_entry
        else None
    )

    return {
        "game": game_response,
        "leaderboard_entry": leaderboard_response,
        "message": "Game completed and submitted to leaderboard"
        if leaderboard_entry
        else "Game completed",
    }


@router.get("/my-games", response_model=List[schemas.Game])
async def get_my_games(
    skip: int = 0,
    limit: int = 20,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Get current user's game history"""
    games = crud.get_games_by_user(db, current_user.id, skip, limit)
    return games


@router.get("/{game_id}", response_model=schemas.Game)
async def get_game(
    game_id: int,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Get a specific game by ID"""
    game = crud.get_game(db, game_id)
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Game not found"
        )

    # Verify the game belongs to the current user
    if game.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot view another user's game",
        )

    return game
