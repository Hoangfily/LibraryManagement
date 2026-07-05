"""
Business logic service for reader (patron) management.
"""

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.modules.readers.model import Reader
from app.modules.readers.schema import ReaderCreate, ReaderUpdate


def get_reader_by_id(db: Session, reader_id: int) -> Reader | None:
    """Find a reader by primary key id."""
    return db.query(Reader).filter(Reader.id == reader_id).first()


def get_reader_by_code(db: Session, reader_code: str) -> Reader | None:
    """Find a reader by reader_code (used to enforce uniqueness)."""
    return db.query(Reader).filter(Reader.reader_code == reader_code).first()


def get_reader_by_email(db: Session, email: str) -> Reader | None:
    """Find a reader by email."""
    return db.query(Reader).filter(Reader.email == email).first()


def search_readers(
    db: Session, keyword: str | None = None, skip: int = 0, limit: int = 100
) -> list[Reader]:
    """
    Retrieve readers, optionally filtered by keyword matching
    full_name (partial, case-insensitive) or reader_code (partial).
    """
    query = db.query(Reader)
    if keyword:
        like_pattern = f"%{keyword}%"
        query = query.filter(
            or_(
                Reader.full_name.ilike(like_pattern),
                Reader.reader_code.ilike(like_pattern),
            )
        )
    return query.offset(skip).limit(limit).all()


def create_reader(db: Session, data: ReaderCreate) -> Reader:
    """Create a new reader. Status defaults to ACTIVE."""
    reader = Reader(
        reader_code=data.reader_code,
        full_name=data.full_name,
        email=data.email,
        phone=data.phone,
        address=data.address,
        status="active",
    )
    db.add(reader)
    db.commit()
    db.refresh(reader)
    return reader


def update_reader(db: Session, reader: Reader, data: ReaderUpdate) -> Reader:
    """Update reader info fields only (not status)."""
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(reader, field, value)
    db.commit()
    db.refresh(reader)
    return reader


def set_reader_status(db: Session, reader: Reader, new_status: str) -> Reader:
    """Lock (inactive) or unlock (active) a reader."""
    reader.status = new_status
    db.commit()
    db.refresh(reader)
    return reader


def check_reader_active(db: Session, reader_id: int) -> tuple[bool, bool]:
    """
    Used by the borrow module to verify a reader before lending a book.
    Returns a tuple of (exists, is_active).
    """
    reader = get_reader_by_id(db, reader_id)
    if not reader:
        return False, False
    return True, reader.status == "active"