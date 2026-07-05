"""
Pydantic schemas for fine request/response validation.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class FineResponse(BaseModel):
    id: int
    borrow_item_id: int
    reader_id: int
    fine_type: str
    amount: float
    reason: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
