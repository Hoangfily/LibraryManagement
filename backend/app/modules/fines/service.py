"""
Service layer for fine queries.
Fine records themselves are created as a side-effect of returning
borrow items late (see borrows/service.py::return_borrow_order).
"""

from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.fines.model import Fine


def get_all_fines(
    db: Session,
    reader_id: Optional[int] = None,
    status_filter: Optional[str] = None,
) -> List[Fine]:
    """List fines, optionally filtered by reader_id and/or status (unpaid/paid)."""
    query = db.query(Fine)
    if reader_id is not None:
        query = query.filter(Fine.reader_id == reader_id)
    if status_filter is not None:
        query = query.filter(Fine.status == status_filter)
    return query.order_by(Fine.id.desc()).all()


def get_fine_by_id(db: Session, fine_id: int) -> Fine:
    """Fetch a single fine by id, raising 404 if not found."""
    fine = db.query(Fine).filter(Fine.id == fine_id).first()
    if not fine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fine not found",
        )
    return fine
