from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class DocumentCreate(BaseModel):
    title: str
    author: Optional[str] = None
    publisher: Optional[str] = None
    publish_year: Optional[int] = None
    category: Optional[str] = None
    isbn: Optional[str] = None
    description: Optional[str] = None


class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    publish_year: Optional[int] = None
    category: Optional[str] = None
    isbn: Optional[str] = None
    description: Optional[str] = None


class DocumentResponse(BaseModel):
    id: int
    title: str
    author: Optional[str] = None
    publisher: Optional[str] = None
    publish_year: Optional[int] = None
    category: Optional[str] = None
    isbn: Optional[str] = None
    description: Optional[str] = None
    total_copies: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)