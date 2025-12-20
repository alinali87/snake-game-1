from datetime import datetime
from typing import Optional

from models import GameMode
from pydantic import BaseModel, EmailStr, field_validator


# User Schemas
class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None


class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool

    class Config:
        from_attributes = True


# Game Schemas
class GameBase(BaseModel):
    game_mode: GameMode
    score: int = 0
    snake_length: int = 1
    moves_count: int = 0
    food_eaten: int = 0


class GameCreate(BaseModel):
    user_id: int
    game_mode: GameMode


class GameUpdate(BaseModel):
    score: Optional[int] = None
    snake_length: Optional[int] = None
    duration_seconds: Optional[int] = None
    moves_count: Optional[int] = None
    food_eaten: Optional[int] = None
    ended_at: Optional[datetime] = None
    is_completed: Optional[bool] = None


class Game(GameBase):
    id: int
    user_id: int
    duration_seconds: Optional[int] = None
    started_at: datetime
    ended_at: Optional[datetime] = None
    is_completed: bool

    class Config:
        from_attributes = True


# LeaderboardEntry Schemas
class LeaderboardEntryBase(BaseModel):
    score: int
    snake_length: int
    game_mode: GameMode


class LeaderboardEntryCreate(LeaderboardEntryBase):
    user_id: int
    game_id: Optional[int] = None


class LeaderboardEntry(LeaderboardEntryBase):
    id: int
    user_id: int
    game_id: Optional[int] = None
    rank: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class LeaderboardEntryWithUser(LeaderboardEntry):
    username: str

    class Config:
        from_attributes = True


# Score Schemas (backward compatibility)
class ScoreBase(BaseModel):
    player_name: str
    score: int


class ScoreCreate(ScoreBase):
    pass


class Score(ScoreBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
