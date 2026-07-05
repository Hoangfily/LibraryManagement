"""
Service layer for reports/thong ke.
"""

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.modules.borrows.model import BorrowOrder
from app.modules.copies.model import DocumentCopy
from app.modules.documents.model import Document
from app.modules.fines.model import Fine
from app.modules.readers.model import Reader


def get_summary_report(db: Session) -> dict:
    """Build the library-wide summary report:
    - Tong so doc gia
    - Tong so sach (documents)
    - Tong so ban sao
    - So ban dang muon
    - So ban con san
    - Tong so phieu muon
    - Tong phi phat chua thanh toan
    """
    total_readers = db.query(Reader).count()
    total_documents = db.query(Document).count()
    total_copies = db.query(DocumentCopy).count()
    borrowed_copies = (
        db.query(DocumentCopy).filter(DocumentCopy.status == "borrowed").count()
    )
    available_copies = (
        db.query(DocumentCopy).filter(DocumentCopy.status == "available").count()
    )
    total_borrow_orders = db.query(BorrowOrder).count()
    total_unpaid_fines = (
        db.query(func.coalesce(func.sum(Fine.amount), 0))
        .filter(Fine.status == "unpaid")
        .scalar()
    )

    return {
        "total_readers": total_readers,
        "total_documents": total_documents,
        "total_copies": total_copies,
        "borrowed_copies": borrowed_copies,
        "available_copies": available_copies,
        "total_borrow_orders": total_borrow_orders,
        "total_unpaid_fines": float(total_unpaid_fines or 0),
    }
