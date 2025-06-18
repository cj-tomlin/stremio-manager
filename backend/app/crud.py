from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import Session, select
from . import models, schemas
from .core.security import get_password_hash

def get_user_by_email(db: Session, email: str):
    return db.exec(select(models.User).where(models.User.email == email)).first()

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[models.User]:
    return db.exec(select(models.User).offset(skip).limit(limit)).all()

def delete_user(db: Session, user: models.User):
    db.delete(user)
    db.commit()
    return user

async def create_addon_usage_log(db: AsyncSession, user: models.User) -> models.AddonUsageLog:
    db_log = models.AddonUsageLog(user_id=user.id)
    db.add(db_log)
    await db.commit()
    await db.refresh(db_log)
    return db_log


async def get_addon_usage_logs(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[models.AddonUsageLog]:
    result = await db.execute(select(models.AddonUsageLog).offset(skip).limit(limit))
    return result.scalars().all()
