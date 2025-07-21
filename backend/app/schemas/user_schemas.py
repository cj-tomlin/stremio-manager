from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Schema for creating a new user
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    is_admin: bool = False

# Schema for updating a user
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_admin: Optional[bool] = None

# Schema for reading user data (omitting password)
class User(BaseModel):
    id: int
    email: EmailStr
    is_admin: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
