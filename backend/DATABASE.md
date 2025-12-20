# Snake Game Database Documentation

## Overview

The Snake Game uses SQLAlchemy ORM with support for both SQLite (development) and PostgreSQL (production) databases.

## Database Models

### User Model

Stores user information and profiles.

**Table:** `users`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | Integer | Primary Key | Unique user identifier |
| username | String(50) | Unique, Not Null, Indexed | User's unique username |
| email | String(100) | Unique, Nullable, Indexed | User's email address |
| created_at | DateTime | Not Null | Account creation timestamp |
| updated_at | DateTime | Not Null | Last update timestamp |
| is_active | Boolean | Not Null, Default: True | Account active status |

**Relationships:**
- One-to-Many with `Game` (via `games`)
- One-to-Many with `LeaderboardEntry` (via `leaderboard_entries`)

### Game Model

Stores individual game sessions with detailed statistics.

**Table:** `games`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | Integer | Primary Key | Unique game identifier |
| user_id | Integer | Foreign Key, Not Null | Reference to User |
| score | Integer | Not Null, Default: 0 | Final game score |
| snake_length | Integer | Not Null, Default: 1 | Final snake length |
| game_mode | Enum | Not Null | Game mode (walls/pass-through) |
| duration_seconds | Integer | Nullable | Game duration in seconds |
| moves_count | Integer | Not Null, Default: 0 | Total number of moves |
| food_eaten | Integer | Not Null, Default: 0 | Number of food items consumed |
| started_at | DateTime | Not Null | Game start timestamp |
| ended_at | DateTime | Nullable | Game end timestamp |
| is_completed | Boolean | Not Null, Default: False | Game completion status |

**Relationships:**
- Many-to-One with `User` (via `user`)

**Enums:**
- GameMode: `walls`, `pass-through`

### LeaderboardEntry Model

Stores high scores for the leaderboard.

**Table:** `leaderboard_entries`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | Integer | Primary Key | Unique entry identifier |
| user_id | Integer | Foreign Key, Not Null | Reference to User |
| game_id | Integer | Foreign Key, Nullable | Reference to Game (optional) |
| score | Integer | Not Null, Indexed | Score achieved |
| snake_length | Integer | Not Null | Snake length at end |
| game_mode | Enum | Not Null, Indexed | Game mode played |
| rank | Integer | Nullable | Overall rank position |
| created_at | DateTime | Not Null | Entry creation timestamp |

**Relationships:**
- Many-to-One with `User` (via `user`)
- Many-to-One with `Game` (via `game`)

### Score Model (Legacy)

Kept for backward compatibility with existing API endpoints.

**Table:** `scores`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | Integer | Primary Key | Unique score identifier |
| player_name | String | Indexed | Player name |
| score | Integer | - | Score value |
| created_at | DateTime | - | Creation timestamp |

## Database Configuration

### SQLite (Default)

```python
# No configuration needed - uses default
DATABASE_URL=sqlite:///./snake_game.db
```

### PostgreSQL

```bash
# Set environment variable
export DATABASE_URL="postgresql://username:password@localhost:5432/snake_game"

# Or create .env file
DATABASE_URL=postgresql://username:password@localhost:5432/snake_game
```

## Database Operations

### Initialization

```bash
# Create all tables
cd backend
uv run python init_db.py

# Drop all tables (use with caution!)
uv run python init_db.py --drop
```

### Testing

```bash
# Run model tests
cd backend
uv run python test_models.py
```

## CRUD Operations

The `crud.py` module provides comprehensive database operations:

### User Operations

```python
from database import SessionLocal
import crud, schemas

db = SessionLocal()

# Create user
user = crud.create_user(db, schemas.UserCreate(
    username="player1",
    email="player1@example.com"
))

# Get user
user = crud.get_user_by_username(db, "player1")

# Update user
crud.update_user(db, user.id, schemas.UserUpdate(
    email="newemail@example.com"
))

# Get user stats
stats = crud.get_user_stats(db, user.id)
```

### Game Operations

```python
# Create game
game = crud.create_game(db, schemas.GameCreate(
    user_id=user.id,
    game_mode=models.GameMode.WALLS
))

# Update game
crud.update_game(db, game.id, schemas.GameUpdate(
    score=100,
    snake_length=10
))

# Complete game
crud.complete_game(db, game.id, final_score=150, snake_length=15)

# Get user's games
games = crud.get_games_by_user(db, user.id)
```

### Leaderboard Operations

```python
# Create leaderboard entry
entry = crud.create_leaderboard_entry(db, schemas.LeaderboardEntryCreate(
    user_id=user.id,
    game_id=game.id,
    score=150,
    snake_length=15,
    game_mode=models.GameMode.WALLS
))

# Get leaderboard (all modes)
leaderboard = crud.get_leaderboard(db, limit=10)

# Get leaderboard for specific mode
walls_leaderboard = crud.get_leaderboard(
    db, 
    game_mode=models.GameMode.WALLS,
    limit=10
)

# Update ranks
crud.update_leaderboard_ranks(db, models.GameMode.WALLS)
```

## Database Schema Diagram

```
┌─────────────────┐
│     Users       │
├─────────────────┤
│ id (PK)         │
│ username        │
│ email           │
│ created_at      │
│ updated_at      │
│ is_active       │
└────────┬────────┘
         │
         │ 1:N
         │
┌────────┴─────────────────┐
│                          │
│                          │
┌─────────▼──────┐  ┌──────▼──────────────────┐
│     Games      │  │  Leaderboard Entries    │
├────────────────┤  ├─────────────────────────┤
│ id (PK)        │  │ id (PK)                 │
│ user_id (FK) ◄─┼──┤ user_id (FK)            │
│ score          │  │ game_id (FK)            │
│ snake_length   │  │ score                   │
│ game_mode      │  │ snake_length            │
│ duration_sec   │  │ game_mode               │
│ moves_count    │  │ rank                    │
│ food_eaten     │  │ created_at              │
│ started_at     │  └─────────────────────────┘
│ ended_at       │
│ is_completed   │
└────────────────┘
```

## Migration Guide

### From SQLite to PostgreSQL

1. Backup SQLite database:
   ```bash
   cp snake_game.db snake_game.db.backup
   ```

2. Set PostgreSQL connection:
   ```bash
   export DATABASE_URL="postgresql://user:pass@localhost/snake_game"
   ```

3. Initialize PostgreSQL database:
   ```bash
   uv run python init_db.py
   ```

4. (Optional) Migrate data using custom script

## Performance Considerations

### Indexes

The following columns are indexed for optimal query performance:
- `users.username` (unique)
- `users.email` (unique)
- `leaderboard_entries.score`
- `leaderboard_entries.game_mode`

### Query Optimization

- Leaderboard queries are limited and ordered by score
- User games are ordered by start time (descending)
- Relationships use lazy loading by default

## Best Practices

1. **Use transactions** for related operations
2. **Close database sessions** properly (use context managers)
3. **Validate input** using Pydantic schemas
4. **Index frequently queried fields**
5. **Use environment variables** for database configuration
6. **Regular backups** especially before schema changes
7. **Test migrations** in development before production

## Troubleshooting

### Common Issues

**Issue:** Database locked (SQLite)
- **Solution:** Ensure only one process accesses SQLite at a time

**Issue:** Connection errors (PostgreSQL)
- **Solution:** Check DATABASE_URL format and credentials

**Issue:** Missing tables
- **Solution:** Run `uv run python init_db.py`

**Issue:** Foreign key constraint errors
- **Solution:** Ensure referenced records exist before creating relationships
