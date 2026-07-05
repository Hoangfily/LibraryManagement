"""
Service layer for borrow/return business logic.

Flow muon (borrow):
- Nhan reader_id va copy_ids.
- Kiem tra reader ton tai va dang active.
- Kiem tra tung copy ton tai va co status = available.
- Tao borrow_order + borrow_items.
- Cap nhat document_copies -> borrowed.

Flow tra (return):
- Tim phieu muon.
- Cap nhat returned_date cho tung item.
- Neu tra qua han thi tao fine = so ngay tre * FINE_PER_LATE_DAY.
- Cap nhat document_copies -> available.
- Cap nhat borrow_order -> returned khi khong con item nao dang muon.
"""

from datetime import date, timedelta
from typing import List, Optional, Tuple

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.borrows.model import BorrowItem, BorrowOrder
from app.modules.copies.model import DocumentCopy
from app.modules.fines.model import Fine
from app.modules.readers.model import Reader

DEFAULT_BORROW_DAYS = 14
FINE_PER_LATE_DAY = 5000

ACTIVE_ORDER_STATUSES = ("borrowing", "overdue")


def get_borrow_order_by_id(db: Session, order_id: int) -> BorrowOrder:
    """Fetch a borrow order by id, raising 404 if not found."""
    order = db.query(BorrowOrder).filter(BorrowOrder.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Borrow order not found",
        )
    return order


def get_all_borrow_orders(
    db: Session,
    reader_id: Optional[int] = None,
    status_filter: Optional[str] = None,
) -> List[BorrowOrder]:
    """List borrow orders, optionally filtered by reader_id and/or status."""
    query = db.query(BorrowOrder)
    if reader_id is not None:
        query = query.filter(BorrowOrder.reader_id == reader_id)
    if status_filter is not None:
        query = query.filter(BorrowOrder.status == status_filter)
    return query.order_by(BorrowOrder.id.desc()).all()


def create_borrow_order(
    db: Session,
    reader_id: int,
    copy_ids: List[int],
    borrow_days: int = DEFAULT_BORROW_DAYS,
) -> BorrowOrder:
    """Create a new borrow order for a reader over a list of document copies."""
    if not copy_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="copy_ids must not be empty",
        )

    # Preserve order but drop duplicates.
    unique_copy_ids = list(dict.fromkeys(copy_ids))

    reader = db.query(Reader).filter(Reader.id == reader_id).first()
    if not reader:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reader not found",
        )
    if not reader.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reader is not active",
        )

    copies = (
        db.query(DocumentCopy)
        .filter(DocumentCopy.id.in_(unique_copy_ids))
        .all()
    )
    copies_by_id = {copy.id: copy for copy in copies}

    missing_ids = [cid for cid in unique_copy_ids if cid not in copies_by_id]
    if missing_ids:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Copies not found: {missing_ids}",
        )

    unavailable_ids = [
        cid for cid in unique_copy_ids if copies_by_id[cid].status != "available"
    ]
    if unavailable_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Copies not available: {unavailable_ids}",
        )

    borrow_date = date.today()
    due_date = borrow_date + timedelta(days=borrow_days)

    order = BorrowOrder(
        reader_id=reader_id,
        borrow_date=borrow_date,
        due_date=due_date,
        status="borrowing",
    )
    db.add(order)
    db.flush()  # assign order.id without committing yet

    for cid in unique_copy_ids:
        db.add(BorrowItem(order_id=order.id, copy_id=cid, status="borrowing"))
        copies_by_id[cid].status = "borrowed"

    db.commit()
    db.refresh(order)
    return order


def return_borrow_order(
    db: Session,
    order_id: int,
    copy_ids: Optional[List[int]] = None,
) -> Tuple[BorrowOrder, List[Fine]]:
    """Return some or all borrowed copies within an order, creating overdue fines as needed."""
    order = get_borrow_order_by_id(db, order_id)

    if order.status not in ACTIVE_ORDER_STATUSES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Borrow order already '{order.status}', cannot return",
        )

    items_query = db.query(BorrowItem).filter(
        BorrowItem.order_id == order_id,
        BorrowItem.status == "borrowing",
    )
    if copy_ids:
        items_query = items_query.filter(BorrowItem.copy_id.in_(copy_ids))
    items = items_query.all()

    if not items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No borrowing items to return for this order",
        )

    today = date.today()
    created_fines: List[Fine] = []

    for item in items:
        item.returned_date = today
        item.status = "returned"

        copy = db.query(DocumentCopy).filter(DocumentCopy.id == item.copy_id).first()
        if copy:
            copy.status = "available"

        if today > order.due_date:
            late_days = (today - order.due_date).days
            fine = Fine(
                borrow_item_id=item.id,
                reader_id=order.reader_id,
                fine_type="overdue",
                amount=late_days * FINE_PER_LATE_DAY,
                reason=f"Returned {late_days} day(s) late",
                status="unpaid",
            )
            db.add(fine)
            created_fines.append(fine)

    remaining_unreturned = (
        db.query(BorrowItem)
        .filter(BorrowItem.order_id == order_id, BorrowItem.status == "borrowing")
        .count()
    )
    if remaining_unreturned == 0:
        order.status = "returned"

    db.commit()
    db.refresh(order)
    for fine in created_fines:
        db.refresh(fine)

    return order, created_fines


def cancel_borrow_order(db: Session, order_id: int) -> BorrowOrder:
    """Cancel a borrow order that has not been (partially) returned yet."""
    order = get_borrow_order_by_id(db, order_id)

    if order.status != "borrowing":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot cancel a borrow order with status '{order.status}'",
        )

    items = db.query(BorrowItem).filter(BorrowItem.order_id == order_id).all()
    for item in items:
        if item.status == "borrowing":
            item.status = "cancelled"
            copy = db.query(DocumentCopy).filter(DocumentCopy.id == item.copy_id).first()
            if copy:
                copy.status = "available"

    order.status = "cancelled"

    db.commit()
    db.refresh(order)
    return order
