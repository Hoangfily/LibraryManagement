"""
Router for document management endpoints.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.response import success_response
from app.core.database import get_db
from app.core.deps import require_librarian
from app.modules.copies.schema import CopyBulkCreate, CopyResponse
from app.modules.copies.service import create_copies_for_document, get_copies_by_document_id
from app.modules.documents.schema import DocumentCreate, DocumentResponse, DocumentUpdate
from app.modules.documents.service import (
    create_document,
    delete_document,
    get_all_documents,
    get_document_by_id,
    search_documents_by_title,
    update_document,
)
from app.modules.users.model import User

router = APIRouter()


@router.get("")
def get_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_librarian),
):
    """Retrieve all documents."""
    documents = get_all_documents(db)
    data = [DocumentResponse.model_validate(d).model_dump() for d in documents]
    return success_response(data=data, message="Documents retrieved successfully")


@router.get("/search")
def search_documents(
    title: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_librarian),
):
    """Search documents by title (partial, case-insensitive)."""
    documents = search_documents_by_title(db, title)
    data = [DocumentResponse.model_validate(d).model_dump() for d in documents]
    return success_response(data=data, message="Search results retrieved successfully")


@router.get("/{document_id}")
def get_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_librarian),
):
    """Retrieve a single document by id."""
    document = get_document_by_id(db, document_id)
    return success_response(
        data=DocumentResponse.model_validate(document).model_dump(),
        message="Document retrieved successfully",
    )


@router.post("")
def add_document(
    data: DocumentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_librarian),
):
    """Create a new document."""
    document = create_document(db, data)
    return success_response(
        data=DocumentResponse.model_validate(document).model_dump(),
        message="Document created successfully",
    )


@router.put("/{document_id}")
def edit_document(
    document_id: int,
    data: DocumentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_librarian),
):
    """Update an existing document."""
    document = update_document(db, document_id, data)
    return success_response(
        data=DocumentResponse.model_validate(document).model_dump(),
        message="Document updated successfully",
    )


@router.delete("/{document_id}")
def remove_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_librarian),
):
    """Delete a document by id."""
    delete_document(db, document_id)
    return success_response(message="Document deleted successfully")


@router.get("/{document_id}/copies")
def list_document_copies(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_librarian),
):
    """List all physical copies belonging to a document."""
    get_document_by_id(db, document_id)  # 404 if document doesn't exist
    copies = get_copies_by_document_id(db, document_id)
    data = [CopyResponse.model_validate(c).model_dump() for c in copies]
    return success_response(data=data, message="Copies retrieved successfully")


@router.post("/{document_id}/copies")
def add_document_copies(
    document_id: int,
    data: CopyBulkCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_librarian),
):
    """Add new physical copies to a document."""
    copies = create_copies_for_document(db, document_id, data.quantity)
    response_data = [CopyResponse.model_validate(c).model_dump() for c in copies]
    return success_response(data=response_data, message="Copies added successfully")