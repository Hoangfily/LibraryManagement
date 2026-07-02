"""
Pydantic schemas cho request/response cua user module.
"""

from typing import Optional

from pydantic import BaseModel


class UserCreate(BaseModel):
    """Schema tao user moi."""

    username: str
    password: str
    full_name: str
    role: str = "librarian"


class UserResponse(BaseModel):
    """Schema tra ve thong tin user (khong bao gom password)."""

    id: int
    username: str
    full_name: str
    role: str
    is_active: int

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    """Schema cap nhat thong tin user."""

    full_name: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[int] = None
