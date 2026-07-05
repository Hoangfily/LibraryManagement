"""
Router for report endpoints: summary.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.response import success_response
from app.core.database import get_db
from app.modules.reports.service import get_summary_report

router = APIRouter()


@router.get("/summary")
def summary_report(db: Session = Depends(get_db)):
    """Library-wide summary: readers, documents, copies, borrow orders, unpaid fines."""
    data = get_summary_report(db)
    return success_response(data=data, message="Get summary report successfully")
