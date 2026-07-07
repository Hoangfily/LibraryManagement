"""
Pydantic schemas for reader (patron) request/response validation.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ReaderCreate(BaseModel):
    """Schema for creating a new reader."""

    reader_code: str
    full_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class ReaderUpdate(BaseModel):
    """Schema for updating reader information (not status)."""

    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class ReaderStatusUpdate(BaseModel):
    """Schema for locking/unlocking a reader."""

    status: str  # "active" or "inactive"


class ReaderResponse(BaseModel):
    """Schema for returning reader information."""

    id: int
    reader_code: str
    full_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ReaderActiveCheckResponse(BaseModel):
    """Schema for the check-active endpoint."""

    exists: bool
    is_active: bool