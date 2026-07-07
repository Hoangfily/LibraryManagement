from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CopyCreate(BaseModel):
    copy_code: str


class CopyBulkCreate(BaseModel):
    quantity: int = Field(default=1, ge=1, le=100)


class CopyStatusUpdate(BaseModel):
    status: str


class CopyResponse(BaseModel):
    id: int
    document_id: int
    copy_code: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True