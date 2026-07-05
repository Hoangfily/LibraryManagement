"""
Pydantic schemas for borrow/return request & response validation.
"""

from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class BorrowCreate(BaseModel):
    """Request body for creating a new borrow order."""

    reader_id: int
    copy_ids: List[int] = Field(..., min_length=1, description="List of document_copies.id to borrow")
    borrow_days: Optional[int] = Field(default=14, description="Loan period in days, default 14")


class BorrowReturnRequest(BaseModel):
    """Request body for returning books in a borrow order.

    If `copy_ids` is omitted (or empty), all not-yet-returned items in the
    order are returned.
    """

    copy_ids: Optional[List[int]] = None


class BorrowItemResponse(BaseModel):
    id: int
    order_id: int
    copy_id: int
    returned_date: Optional[date] = None
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BorrowOrderResponse(BaseModel):
    id: int
    reader_id: int
    borrow_date: date
    due_date: date
    status: str
    created_at: datetime
    updated_at: datetime
    items: List[BorrowItemResponse] = []

    model_config = ConfigDict(from_attributes=True)
