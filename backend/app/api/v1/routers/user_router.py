from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas, models
from app.database import get_async_db
from app.api.v1.routers.auth_router import get_current_user, get_current_admin_user

router = APIRouter()


@router.post("/", response_model=schemas.User, status_code=201)
async def create_user(
    user: schemas.UserCreate, 
    db: AsyncSession = Depends(get_async_db),
    current_admin: models.User = Depends(get_current_admin_user),
):
    db_user = await crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.create_user(db=db, user=user)


@router.get("/me", response_model=schemas.User)
async def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user


@router.get("/", response_model=list[schemas.User])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_db),
    current_user: models.User = Depends(get_current_admin_user),
):
    """
    Retrieve users.
    """
    users = await crud.get_users(db, skip=skip, limit=limit)
    return users


@router.put("/{user_id}", response_model=schemas.User)
async def update_user(
    user_id: int,
    user_in: schemas.UserUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_admin: models.User = Depends(get_current_admin_user),
):
    db_user = await crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    user = await crud.update_user(db=db, db_user=db_user, user_in=user_in)
    return user


@router.delete("/{user_id}", response_model=schemas.User)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_admin: models.User = Depends(get_current_admin_user),
):
    db_user = await crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    user = await crud.delete_user(db=db, user_id=user_id)
    return user
