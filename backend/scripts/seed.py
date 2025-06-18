import os
import sys
from sqlalchemy.orm import Session

# Add the 'backend' directory to sys.path so 'app' can be imported
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
sys.path.append(BACKEND_DIR)

from app.database import engine # Import engine directly
from sqlmodel import Session # Import Session from sqlmodel, which app.database also uses
from app.crud import get_user_by_email, create_user, delete_user # Import delete_user
from app.schemas import UserCreate

# Define the initial user details
INITIAL_USER_EMAIL = "admin@example.com"
INITIAL_USER_PASSWORD = "adminpassword"

def seed_initial_user():
    print("Seeding initial user...")
    db = Session(engine) # Create session directly with the engine
    try:
        user = get_user_by_email(db=db, email=INITIAL_USER_EMAIL)
        if user:
            print(f"User {INITIAL_USER_EMAIL} already exists. Deleting and recreating...")
            delete_user(db=db, user=user)
            print(f"User {INITIAL_USER_EMAIL} deleted.")
        
        user_in = UserCreate(email=INITIAL_USER_EMAIL, password=INITIAL_USER_PASSWORD)
        create_user(db=db, user=user_in)
        print(f"User {INITIAL_USER_EMAIL} created successfully.")
    finally:
        db.close()

def main():
    print("Starting database seeding...")
    seed_initial_user()
    print("Database seeding finished.")

if __name__ == "__main__":
    main()
