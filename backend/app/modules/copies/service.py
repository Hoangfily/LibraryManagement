from sqlalchemy.orm import Session

from app.modules.copies.model import DocumentCopy


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


def update_copy_status(db: Session, copy_id: int, status: str):
    copy = get_copy_by_id(db, copy_id)
    if not copy:
        return None

    copy.status = status
    db.commit()
    db.refresh(copy)
    return copy