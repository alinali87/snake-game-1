import enum
from datetime import datetime

from database import Base
from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class GameMode(str, enum.Enum):
    WALLS = "walls"
    PASS_THROUGH = "pass-through"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    is_active = Column(Boolean, default=True, nullable=False)

    # Relationships
    games = relationship("Game", back_populates="user", cascade="all, delete-orphan")
    leaderboard_entries = relationship(
        "LeaderboardEntry", back_populates="user", cascade="all, delete-orphan"
    )


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    score = Column(Integer, default=0, nullable=False)
    snake_length = Column(Integer, default=1, nullable=False)
    game_mode = Column(Enum(GameMode), nullable=False)
    duration_seconds = Column(Integer, nullable=True)  # Game duration in seconds
    moves_count = Column(Integer, default=0, nullable=False)  # Total moves made
    food_eaten = Column(
        Integer, default=0, nullable=False
    )  # Number of food items eaten
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    ended_at = Column(DateTime, nullable=True)
    is_completed = Column(Boolean, default=False, nullable=False)

    # Relationships
    user = relationship("User", back_populates="games")


class LeaderboardEntry(Base):
    __tablename__ = "leaderboard_entries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    game_id = Column(
        Integer, ForeignKey("games.id"), nullable=True
    )  # Optional link to specific game
    score = Column(Integer, nullable=False, index=True)
    snake_length = Column(Integer, nullable=False)
    game_mode = Column(Enum(GameMode), nullable=False, index=True)
    rank = Column(Integer, nullable=True)  # Overall rank
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="leaderboard_entries")
    game = relationship("Game")


# Keep Score model for backward compatibility
class Score(Base):
    __tablename__ = "scores"

    id = Column(Integer, primary_key=True, index=True)
    player_name = Column(String, index=True)
    score = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
