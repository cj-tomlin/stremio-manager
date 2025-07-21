import os
import sys
import asyncio
import random
from datetime import datetime, timedelta

# Add the 'backend' directory to sys.path so 'app' can be imported
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
sys.path.append(BACKEND_DIR)

from app.database import async_engine, AsyncSessionLocal
from app.crud import get_user_by_email, create_user, delete_user
from app import models
from app.schemas import UserCreate
from sqlmodel import select

# Define the initial user details
INITIAL_USER_EMAIL = "admin@example.com"
INITIAL_USER_PASSWORD = "adminpassword"

async def seed_initial_user(db: AsyncSessionLocal):
    print("Seeding initial user...")
    user = await get_user_by_email(db=db, email=INITIAL_USER_EMAIL)
    if user:
        print(f"User {INITIAL_USER_EMAIL} already exists. Deleting and recreating...")
        await delete_user(db=db, user=user)
        print(f"User {INITIAL_USER_EMAIL} deleted.")
    
    user_in = UserCreate(email=INITIAL_USER_EMAIL, password=INITIAL_USER_PASSWORD, is_admin=True)
    await create_user(db=db, user=user_in)
    print(f"User {INITIAL_USER_EMAIL} created successfully.")

async def seed_sample_data(db: AsyncSessionLocal):
    print("Seeding sample users and usage data...")
    sample_users_data = [
        {"email": "alice@example.com", "password": "password123"},
        {"email": "bob@example.com", "password": "password123"},
        {"email": "charlie@example.com", "password": "password123"},
    ]

    for user_data in sample_users_data:
        user = await get_user_by_email(db=db, email=user_data['email'])
        if not user:
            user_in = UserCreate(email=user_data['email'], password=user_data['password'])
            await create_user(db=db, user=user_in)
            print(f"Created sample user: {user_data['email']}")

    # Generate sample usage logs
    result = await db.execute(select(models.User))
    all_users = result.scalars().all()
    if not all_users:
        return

    print("Generating sample usage logs...")
    for _ in range(150):
        random_user = random.choice(all_users)
        random_timestamp = datetime.utcnow() - timedelta(days=random.randint(0, 29), hours=random.randint(0, 23))
        log_entry = models.AddonUsageLog(user_id=random_user.id, created_at=random_timestamp)
        db.add(log_entry)
    
    await db.commit()
    print("Sample data seeding complete.")

async def main():
    print("Starting database seeding...")
    async with AsyncSessionLocal() as db:
        await seed_initial_user(db)
        await seed_sample_data(db)
    print("Database seeding finished.")

if __name__ == "__main__":
    asyncio.run(main())
