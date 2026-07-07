"""
Router for fine endpoints: list and detail.
"""

from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.common.response import success_response
from app.core.database import get_db
from app.core.deps import require_librarian
from app.modules.fines.schema import FineResponse
from app.modules.fines.service import get_all_fines, get_fine_by_id
from app.modules.users.model import User

router = APIRouter()


@router.get("")
def list_fines(
    reader_id: Optional[int] = Query(default=None),
    status: Optional[str] = Query(default=None, description="unpaid | paid"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_librarian),
):
    """List fines, optionally filtered by reader_id and/or status."""
    fines = get_all_fines(db, reader_id=reader_id, status_filter=status)
    return success_response(
        data=[FineResponse.model_validate(fine).model_dump() for fine in fines],
        message="Get fines successfully",
    )


@router.get("/{fine_id}")
def get_fine(
    fine_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_librarian),
):
    """Get a single fine by id."""
    fine = get_fine_by_id(db, fine_id)
    return success_response(
        data=FineResponse.model_validate(fine).model_dump(),
        message="Get fine successfully",
    )
