"""
Faker Script for ComKit Server-FastAPI

This script generates fake data for testing purposes.
It creates sample users, items, and requests in the database.
"""

import sys
from pathlib import Path
import random
from faker import Faker

# Add the current directory to Python path to import local modules
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from database import SessionLocal, engine
from models import User, Item, Request, ItemType, ItemStatus, RequestStatus
from auth import hash_password

# Initialize Faker
fake = Faker()


def create_fake_users(num_users=10):
    """
    Create fake users for testing.

    Args:
        num_users (int): Number of fake users to create
    """
    db = SessionLocal()
    try:
        print(f"Creating {num_users} fake users...")
        print(f"Database engine URL: {engine.url}")

        # Check existing users before
        existing_count = db.query(User).count()
        print(f"Existing users before creation: {existing_count}")

        for i in range(num_users):
            # Generate fake user data
            username = fake.user_name() + str(random.randint(1, 999))
            password = "12345678"  # Default password for testing
            password_hash = hash_password(password)
            name = fake.name()
            address = fake.address().replace("\n", ", ")

            # Check if username already exists
            existing_user = db.query(User).filter(User.username == username).first()
            if existing_user:
                continue

            # Create user
            user = User(
                username=username,
                password_hash=password_hash,
                name=name,
                address=address,
            )

            db.add(user)
            db.commit()
            db.refresh(user)

            print(f"Created user: {username} (ID: {user.id})")

        # Check users after creation
        final_count = db.query(User).count()
        print(f"Total users after creation: {final_count}")
        print(f"Successfully created {num_users} fake users!")

    except Exception as e:
        print(f"Error creating fake users: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def create_fake_items(num_items=20):
    """
    Create fake items for testing.

    Args:
        num_items (int): Number of fake items to create
    """
    db = SessionLocal()
    try:
        print(f"Creating {num_items} fake items...")

        # Get all users to assign as owners
        users = db.query(User).all()
        if not users:
            print("No users found. Please create users first.")
            return

        item_names = [
            "Blender",
            "Mixing Bowls",
            "Cake Pans",
            "Stand Mixer",
            "Food Processor",
            "Baking Sheets",
            "Measuring Cups",
            "Rolling Pin",
            "Kitchen Scale",
            "Muffin Tin",
            "Bread Maker",
            "Air Fryer",
            "Slow Cooker",
            "Pressure Cooker",
            "Electric Kettle",
            "Coffee Maker",
            "Toaster Oven",
            "Immersion Blender",
            "Mandoline Slicer",
            "Kitchen Aid",
        ]

        for i in range(num_items):
            # Generate fake item data
            name = random.choice(item_names) + f" {i + 1}"
            description = fake.text(max_nb_chars=200)
            qty = random.randint(1, 10)
            # Initially, remaining_qty equals total qty (no requests yet)
            remaining_qty = qty
            unit = random.choice(["pcs", "kg", "liters", "boxes"])
            type = random.choice(list(ItemType))
            status = ItemStatus.AVAILABLE
            owner = random.choice(users)

            # Create item
            item = Item(
                name=name,
                description=description,
                qty=qty,
                remaining_qty=remaining_qty,
                unit=unit,
                type=type,
                status=status,
                owner_id=owner.id,
            )

            db.add(item)
            db.commit()
            db.refresh(item)

            print(f"Created item: {name} (ID: {item.id}, Qty: {qty})")

        print(f"Successfully created {num_items} fake items!")

    except Exception as e:
        print(f"Error creating fake items: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def create_fake_requests(num_requests=15):
    """
    Create fake requests for testing.

    Args:
        num_requests (int): Number of fake requests to create
    """
    db = SessionLocal()
    try:
        print(f"Creating {num_requests} fake requests...")

        # Get all users and items
        users = db.query(User).all()
        items = db.query(Item).filter(Item.status == ItemStatus.AVAILABLE).all()

        if not users:
            print("No users found. Please create users first.")
            return

        if not items:
            print("No available items found. Please create items first.")
            return

        created_count = 0

        for i in range(num_requests):
            # Pick a random item
            item = random.choice(items)

            # Find users who are not the owner of this item
            eligible_requesters = [u for u in users if u.id != item.owner_id]

            # If no eligible requesters (only one user), skip this request
            if not eligible_requesters:
                continue

            requester = random.choice(eligible_requesters)

            # Check how much quantity is available for requests
            available_qty = item.remaining_qty

            if available_qty <= 0:
                continue  # No quantity available for new requests

            # Request a reasonable amount (1-3 items, but not more than available)
            max_request_qty = min(available_qty, 3)
            if max_request_qty <= 0:
                continue

            requested_qty = random.randint(1, max_request_qty)

            date_start = fake.date_between(
                start_date="-30d", end_date="today"
            ).strftime("%Y-%m-%d")
            date_end = fake.date_between(start_date="today", end_date="+30d").strftime(
                "%Y-%m-%d"
            )

            # For simplicity, create mostly pending requests, some approved
            # Avoid rejected/cancelled/returned to keep data clean
            status = random.choice(
                [RequestStatus.PENDING, RequestStatus.PENDING, RequestStatus.APPROVED]
            )

            # Create request
            request = Request(
                item_id=item.id,
                requester_id=requester.id,
                requested_qty=requested_qty,
                date_start=date_start,
                date_end=date_end,
                status=status,
            )

            db.add(request)
            db.commit()
            db.refresh(request)

            # Update item remaining_qty if request is approved or pending
            if status in [RequestStatus.PENDING, RequestStatus.APPROVED]:
                item.remaining_qty -= requested_qty
                db.commit()

            print(
                f"Created request: {requester.username} -> {item.name} ({requested_qty} {item.unit}, status: {status.value})"
            )
            created_count += 1

            # Break if we've created enough requests
            if created_count >= num_requests:
                break

        print(f"Successfully created {created_count} fake requests!")

    except Exception as e:
        print(f"Error creating fake requests: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def clear_all_data():
    """
    Clear all data from the database (use with caution!).
    """
    db = SessionLocal()
    try:
        print("Clearing all data...")

        # Delete in order to respect foreign key constraints
        db.query(Request).delete()
        db.query(Item).delete()
        db.query(User).delete()

        db.commit()
        print("All data cleared successfully!")

    except Exception as e:
        print(f"Error clearing data: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def populate_all_data():
    """
    Populate the database with all fake data.
    """
    try:
        print("Starting data population...")

        create_fake_users(10)
        create_fake_items(20)
        create_fake_requests(15)

        print("Data population completed successfully!")

    except Exception as e:
        print(f"Error during data population: {e}")
        raise


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Faker script for ComKit")
    parser.add_argument(
        "--users", type=int, default=10, help="Number of fake users to create"
    )
    parser.add_argument(
        "--items", type=int, default=20, help="Number of fake items to create"
    )
    parser.add_argument(
        "--requests", type=int, default=15, help="Number of fake requests to create"
    )
    parser.add_argument(
        "--clear", action="store_true", help="Clear all data from database"
    )
    parser.add_argument("--all", action="store_true", help="Populate all fake data")

    args = parser.parse_args()

    if args.clear:
        clear_all_data()
    elif args.all:
        populate_all_data()
    else:
        if args.users > 0:
            create_fake_users(args.users)
        if args.items > 0:
            create_fake_items(args.items)
        if args.requests > 0:
            create_fake_requests(args.requests)
