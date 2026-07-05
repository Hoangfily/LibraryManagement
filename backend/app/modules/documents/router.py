from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.documents.schema import DocumentCreate, DocumentUpdate, DocumentResponse
from app.modules.documents.service import (
    get_all_documents,
    get_document_by_id,
    create_document,
    update_document,
    delete_document,
    search_documents_by_title,
)

router = APIRouter()


@router.get("", response_model=list[DocumentResponse])
def get_documents(db: Session = Depends(get_db)):
    return get_all_documents(db)


@router.get("/search", response_model=list[DocumentResponse])
def search_documents(title: str, db: Session = Depends(get_db)):
    return search_documents_by_title(db, title)


@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(document_id: int, db: Session = Depends(get_db)):
    return get_document_by_id(db, document_id)


@router.post("", response_model=DocumentResponse)
def add_document(data: DocumentCreate, db: Session = Depends(get_db)):
    return create_document(db, data)


@router.put("/{document_id}", response_model=DocumentResponse)
def edit_document(document_id: int, data: DocumentUpdate, db: Session = Depends(get_db)):
    return update_document(db, document_id, data)


@router.delete("/{document_id}")
def remove_document(document_id: int, db: Session = Depends(get_db)):
    return delete_document(db, document_id)