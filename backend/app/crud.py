from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, func, desc

from . import models, schemas
from .core.security import get_password_hash


async def get_user(db: AsyncSession, user_id: int) -> models.User | None:
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    return result.scalar_one_or_none()


async def get_user_by_email(db: AsyncSession, email: str) -> models.User | None:
    result = await db.execute(select(models.User).where(models.User.email == email))
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user: schemas.UserCreate) -> models.User:
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email, hashed_password=hashed_password, is_admin=user.is_admin
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[models.User]:
    result = await db.execute(select(models.User).offset(skip).limit(limit))
    return result.scalars().all()


async def update_user(
    db: AsyncSession, db_user: models.User, user_in: schemas.UserUpdate
) -> models.User:
    update_data = user_in.model_dump(exclude_unset=True)
    if "password" in update_data and update_data["password"]:
        hashed_password = get_password_hash(update_data["password"])
        db_user.hashed_password = hashed_password
        del update_data["password"]

    for field, value in update_data.items():
        setattr(db_user, field, value)

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def delete_user(db: AsyncSession, user_id: int):
    db_user = await get_user(db, user_id=user_id)
    if db_user:
        await db.delete(db_user)
        await db.commit()
    return db_user


async def create_addon_usage_log(
    db: AsyncSession, user: models.User
) -> models.AddonUsageLog:
    db_log = models.AddonUsageLog(user_id=user.id)
    db.add(db_log)
    await db.commit()
    await db.refresh(db_log)
    return db_log


async def get_addon_usage_logs(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> list[models.AddonUsageLog]:
    result = await db.execute(select(models.AddonUsageLog).offset(skip).limit(limit))
    return result.scalars().all()


async def get_total_users(db: AsyncSession) -> int:
    result = await db.execute(select(func.count(models.User.id)))
    return result.scalar_one()


async def get_total_addon_usage(db: AsyncSession) -> int:
    result = await db.execute(select(func.count(models.AddonUsageLog.id)))
    return result.scalar_one()


async def get_addon_usage_by_day(db: AsyncSession, limit: int = 30) -> list:
    result = await db.execute(
        select(
            func.date(models.AddonUsageLog.created_at).label("date"),
            func.count(models.AddonUsageLog.id).label("count"),
        )
        .group_by(func.date(models.AddonUsageLog.created_at))
        .order_by(desc("date"))
        .limit(limit)
    )
    return result.mappings().all()


async def get_most_active_users(db: AsyncSession, limit: int = 10) -> list:
    result = await db.execute(
        select(
            models.User.email,
            func.count(models.AddonUsageLog.id).label("count"),
        )
        .join(models.User, models.AddonUsageLog.user_id == models.User.id)
        .group_by(models.User.email)
        .order_by(desc("count"))
        .limit(limit)
    )
    return result.mappings().all()
