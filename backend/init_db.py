"""
Database initialization script for Snake Game
Creates all tables and optionally seeds initial data
"""

import sys

import models
from database import Base, engine


def init_database():
    """Initialize database by creating all tables"""
    print("Creating database tables...")
    try:
        # Import all models to ensure they're registered with Base
        from models import Game, LeaderboardEntry, Score, User

        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✓ Database tables created successfully!")
        print("\nCreated tables:")
        print("  - users")
        print("  - games")
        print("  - leaderboard_entries")
        print("  - scores (legacy)")

    except Exception as e:
        print(f"✗ Error creating database tables: {e}")
        sys.exit(1)


def drop_all_tables():
    """Drop all tables (use with caution!)"""
    print("WARNING: This will delete all data!")
    response = input("Are you sure you want to drop all tables? (yes/no): ")
    if response.lower() == "yes":
        print("Dropping all tables...")
        Base.metadata.drop_all(bind=engine)
        print("✓ All tables dropped successfully!")
    else:
        print("Operation cancelled.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--drop":
        drop_all_tables()
    else:
        init_database()
