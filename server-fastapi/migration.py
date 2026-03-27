"""
Database Migration Script for ComKit Server-FastAPI

This script creates the database and all required tables based on the models.
It handles database initialization, table creation, and provides feedback.
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path to import local modules
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from database import engine, Base, DATABASE_URL
from models import User, Item, Request, ItemType, ItemStatus, RequestStatus  # noqa: F401


def create_database_and_tables():
    """
    Create database and all tables based on the models.
    This function will:
    1. Import all models to ensure they are registered with SQLAlchemy
    2. Create all tables in the database
    3. Provide feedback about the creation process
    """
    try:
        print("Starting database migration...")
        print(f"Database URL: {DATABASE_URL}")

        # Create all tables
        Base.metadata.create_all(bind=engine)

        print("Database tables created successfully!")

        # List all created tables
        print("\nCreated tables:")
        for table_name in Base.metadata.tables.keys():
            print(f"   - {table_name}")

        # Show table details
        print("\nTable schemas:")
        for table_name, table in Base.metadata.tables.items():
            print(f"\n{table_name}:")
            for column in table.columns:
                column_type = str(column.type)
                nullable = "NULL" if column.nullable else "NOT NULL"
                primary_key = "PRIMARY KEY" if column.primary_key else ""
                unique = "UNIQUE" if column.unique else ""

                constraints = " ".join(filter(None, [nullable, primary_key, unique]))
                print(f"   - {column.name}: {column_type} ({constraints})")

        # Show database file location if SQLite
        if "sqlite" in DATABASE_URL:
            db_path = DATABASE_URL.replace("sqlite:///", "")
            if os.path.exists(db_path):
                size = os.path.getsize(db_path)
                print(f"\nDatabase file: {db_path}")
                print(f"File size: {size} bytes")
            else:
                print(f"\nWarning: Database file not found at: {db_path}")

        print("\nMigration completed successfully!")

    except Exception as e:
        print(f"Error during migration: {e}")
        raise


def drop_all_tables():
    """
    Drop all tables (use with caution!).
    This is useful for testing and development.
    """
    try:
        print("Dropping all tables...")
        Base.metadata.drop_all(bind=engine)
        print("All tables dropped successfully!")
    except Exception as e:
        print(f"Error dropping tables: {e}")
        raise


def reset_database():
    """
    Reset the database by dropping all tables and recreating them.
    """
    try:
        print("Resetting database...")
        drop_all_tables()
        create_database_and_tables()
        print("Database reset completed!")
    except Exception as e:
        print(f"Error resetting database: {e}")
        raise


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Database migration script for ComKit")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Reset database (drop and recreate all tables)",
    )
    parser.add_argument("--drop", action="store_true", help="Drop all tables")

    args = parser.parse_args()

    if args.drop:
        drop_all_tables()
    elif args.reset:
        reset_database()
    else:
        create_database_and_tables()
