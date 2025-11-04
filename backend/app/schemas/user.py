from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from app.models.user import UserRole

class UserBase(BaseModel):
    email: EmailStr
    role: UserRole

class UserCreate(UserBase):
    password: str
    branch_id: Optional[int] = None

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    branch_id: Optional[int] = None

class UserResponse(UserBase):
    id: int
    branch_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True

