"""
Router for reader (patron) management endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.common.constants import ErrorMessage
from app.common.response import error_response, success_response
from app.core.database import get_db
from app.core.deps import require_librarian
from app.modules.readers.schema import (
    ReaderActiveCheckResponse,
    ReaderCreate,
    ReaderResponse,
    ReaderStatusUpdate,
    ReaderUpdate,
)
from app.modules.readers.service import (
    check_reader_active,
    create_reader,
    get_reader_by_code,
    get_reader_by_email,
    get_reader_by_id,
    search_readers,
    set_reader_status,
    update_reader,
)
from app.modules.users.model import User

router = APIRouter()


@router.get("")
def list_readers(
    keyword: str | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_librarian),
):
    """
    Retrieve readers. Pass `keyword` to search by full_name or reader_code.
    Example: GET /api/readers?keyword=Nguyen
    """
    readers = search_readers(db, keyword=keyword, skip=skip, limit=limit)
    data = [ReaderResponse.model_validate(r).model_dump() for r in readers]
    return success_response(data=data, message="Readers retrieved successfully")


@router.get("/{reader_id}")
def get_reader(
    reader_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_librarian),
):
    """Retrieve a single reader by id."""
    reader = get_reader_by_id(db, reader_id)
    if not reader:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_response(message=ErrorMessage.READER_NOT_FOUND),
        )
    return success_response(
        data=ReaderResponse.model_validate(reader).model_dump(),
        message="Reader retrieved successfully",
    )


@router.post("")
def create_new_reader(
    request: ReaderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_librarian),
):
    """Create a new reader. reader_code must be unique. Status defaults to ACTIVE."""
    if get_reader_by_code(db, request.reader_code):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_response(message=ErrorMessage.READER_CODE_ALREADY_EXISTS),
        )
    if request.email and get_reader_by_email(db, request.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_response(message=ErrorMessage.READER_EMAIL_ALREADY_EXISTS),
        )
    reader = create_reader(db, request)
    return success_response(
        data=ReaderResponse.model_validate(reader).model_dump(),
        message="Reader created successfully",
    )


@router.put("/{reader_id}")
def update_existing_reader(
    reader_id: int,
    request: ReaderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_librarian),
):
    """Update reader information. Use PATCH /status to lock/unlock a reader."""
    reader = get_reader_by_id(db, reader_id)
    if not reader:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_response(message=ErrorMessage.READER_NOT_FOUND),
        )
    if request.email and request.email != reader.email:
        if get_reader_by_email(db, request.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_response(message=ErrorMessage.READER_EMAIL_ALREADY_EXISTS),
            )
    reader = update_reader(db, reader, request)
    return success_response(
        data=ReaderResponse.model_validate(reader).model_dump(),
        message="Reader updated successfully",
    )


@router.patch("/{reader_id}/status")
def change_reader_status(
    reader_id: int,
    request: ReaderStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_librarian),
):
    """Lock (inactive) or unlock (active) a reader."""
    reader = get_reader_by_id(db, reader_id)
    if not reader:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_response(message=ErrorMessage.READER_NOT_FOUND),
        )
    reader = set_reader_status(db, reader, request.status)
    action = "unlocked" if request.status == "active" else "locked"
    return success_response(
        data=ReaderResponse.model_validate(reader).model_dump(),
        message=f"Reader {action} successfully",
    )


@router.get("/{reader_id}/check-active")
def verify_reader_active(
    reader_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_librarian),
):
    """
    Used by the borrow module to verify a reader exists and is ACTIVE
    before allowing a borrow transaction.
    """
    exists, active = check_reader_active(db, reader_id)
    if not exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_response(message=ErrorMessage.READER_NOT_FOUND),
        )
    data = ReaderActiveCheckResponse(exists=exists, is_active=active).model_dump()
    message = "Reader is active" if active else "Reader is inactive"
    return success_response(data=data, message=message)