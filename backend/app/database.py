from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

# Async Database Setup
ASYNC_DATABASE_URL = "sqlite+aiosqlite:///./database.db" # Using aiosqlite for async
async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_db():
    with Session(engine) as session:
        yield session

async def get_async_db():
    async with AsyncSession(async_engine) as session:
        yield session
