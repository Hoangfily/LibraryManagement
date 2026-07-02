"""
Pydantic schemas for user request/response validation.
"""

from typing import Optional

from pydantic import BaseModel


class UserCreate(BaseModel):
    """Schema for creating a new user."""

    username: str
    password: str
    full_name: str
    role: str = "librarian"


class UserResponse(BaseModel):
    """Schema for returning user information (excludes password)."""

    id: int
    username: str
    full_name: str
    role: str
    is_active: int

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    """Schema for updating user information."""

    full_name: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[int] = None
