from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.copies.model import DocumentCopy
from app.modules.documents.model import Document


VALID_COPY_STATUS = ["available", "borrowed", "lost", "damaged"]


def get_copy_by_id(db: Session, copy_id: int):
    return db.query(DocumentCopy).filter(DocumentCopy.id == copy_id).first()


def get_copies_by_document_id(db: Session, document_id: int):
    return db.query(DocumentCopy).filter(DocumentCopy.document_id == document_id).all()


def create_copy(db: Session, document_id: int, copy_code: str):
    copy = DocumentCopy(
        document_id=document_id,
        copy_code=copy_code,
        status="available",
    )

    db.add(copy)
    db.commit()
    db.refresh(copy)
    return copy


def create_copies_for_document(db: Session, document_id: int, quantity: int) -> List[DocumentCopy]:
    """Add `quantity` new available copies to a document, updating its total_copies count."""
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )

    existing_count = (
        db.query(DocumentCopy).filter(DocumentCopy.document_id == document_id).count()
    )

    copies = []
    for i in range(quantity):
        seq = existing_count + i + 1
        copy = DocumentCopy(
            document_id=document_id,
            copy_code=f"DOC{document_id}-{seq:03d}",
            status="available",
        )
        db.add(copy)
        copies.append(copy)

    document.total_copies += quantity

    db.commit()
    for copy in copies:
        db.refresh(copy)
    return copies


def update_copy_status(db: Session, copy_id: int, status: str):
    copy = get_copy_by_id(db, copy_id)
    if not copy:
        return None

    copy.status = status
    db.commit()
    db.refresh(copy)
    return copy