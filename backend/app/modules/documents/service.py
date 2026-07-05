from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.modules.documents.model import Document
from app.modules.documents.schema import DocumentCreate, DocumentUpdate


def get_all_documents(db: Session):
    return db.query(Document).all()


def get_document_by_id(db: Session, document_id: int):
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


def create_document(db: Session, data: DocumentCreate):
    document = Document(**data.model_dump())
    db.add(document)
    db.commit()
    db.refresh(document)
    return document


def update_document(db: Session, document_id: int, data: DocumentUpdate):
    document = get_document_by_id(db, document_id)

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(document, key, value)

    db.commit()
    db.refresh(document)
    return document


def delete_document(db: Session, document_id: int):
    document = get_document_by_id(db, document_id)
    db.delete(document)
    db.commit()
    return {"message": "Deleted successfully"}


def search_documents_by_title(db: Session, title: str):
    return db.query(Document).filter(Document.title.ilike(f"%{title}%")).all()