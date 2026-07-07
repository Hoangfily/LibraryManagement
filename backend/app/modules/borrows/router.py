"""
Router for borrow/return endpoints: create, list, detail, return, cancel.
"""

from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.common.response import success_response
from app.core.database import get_db
from app.core.deps import require_librarian
from app.modules.borrows.schema import (
    BorrowCreate,
    BorrowOrderResponse,
    BorrowReturnRequest,
)
from app.modules.borrows.service import (
    DEFAULT_BORROW_DAYS,
    cancel_borrow_order,
    create_borrow_order,
    get_all_borrow_orders,
    get_borrow_order_by_id,
    return_borrow_order,
)
from app.modules.fines.schema import FineResponse
from app.modules.users.model import User

router = APIRouter()


def _serialize_order(order) -> dict:
    return BorrowOrderResponse.model_validate(order).model_dump()


@router.post("")
def create_borrow(
    request: BorrowCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_librarian),
):
    """Create a borrow order: reader_id + copy_ids -> borrow_order + borrow_items."""
    order = create_borrow_order(
        db,
        reader_id=request.reader_id,
        copy_ids=request.copy_ids,
        borrow_days=request.borrow_days or DEFAULT_BORROW_DAYS,
    )
    return success_response(
        data=_serialize_order(order),
        message="Borrow order created successfully",
    )


@router.get("")
def list_borrows(
    reader_id: Optional[int] = Query(default=None),
    status: Optional[str] = Query(default=None, description="borrowing | returned | overdue | cancelled"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_librarian),
):
    """List borrow orders, optionally filtered by reader_id and/or status."""
    orders = get_all_borrow_orders(db, reader_id=reader_id, status_filter=status)
    return success_response(
        data=[_serialize_order(order) for order in orders],
        message="Get borrow orders successfully",
    )


@router.get("/{order_id}")
def get_borrow(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_librarian),
):
    """Get a single borrow order with its items."""
    order = get_borrow_order_by_id(db, order_id)
    return success_response(
        data=_serialize_order(order),
        message="Get borrow order successfully",
    )


@router.post("/{order_id}/return")
def return_borrow(
    order_id: int,
    request: Optional[BorrowReturnRequest] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_librarian),
):
    """Return some or all copies in a borrow order. Overdue returns generate fines."""
    copy_ids = request.copy_ids if request else None
    order, fines = return_borrow_order(db, order_id, copy_ids=copy_ids)
    return success_response(
        data={
            "order": _serialize_order(order),
            "fines": [FineResponse.model_validate(fine).model_dump() for fine in fines],
        },
        message="Return borrow order successfully",
    )


@router.post("/{order_id}/cancel")
def cancel_borrow(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_librarian),
):
    """Cancel a borrow order that hasn't been returned yet."""
    order = cancel_borrow_order(db, order_id)
    return success_response(
        data=_serialize_order(order),
        message="Cancel borrow order successfully",
    )
