from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.common.response import error_response, success_response
from app.core.database import get_db
from app.modules.copies.schema import CopyResponse, CopyStatusUpdate
from app.modules.copies.service import (
    VALID_COPY_STATUS,
    get_copy_by_id,
    update_copy_status,
)

router = APIRouter()


@router.get("/{copy_id}")
def get_copy(copy_id: int, db: Session = Depends(get_db)):
    copy = get_copy_by_id(db, copy_id)
    if not copy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_response(message="Copy not found"),
        )

    return success_response(
        data=CopyResponse.model_validate(copy).model_dump(),
        message="Get copy successfully",
    )


@router.patch("/{copy_id}/status")
def change_copy_status(
    copy_id: int,
    request: CopyStatusUpdate,
    db: Session = Depends(get_db),
):
    if request.status not in VALID_COPY_STATUS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_response(message="Invalid copy status"),
        )

    copy = update_copy_status(db, copy_id, request.status)
    if not copy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_response(message="Copy not found"),
        )

    return success_response(
        data=CopyResponse.model_validate(copy).model_dump(),
        message="Update copy status successfully",
    )