"""
Router dinh nghia cac endpoint xac thuc: dang nhap.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.common.constants import ErrorMessage
from app.common.response import error_response, success_response
from app.core.database import get_db
from app.modules.auth.schema import LoginRequest, TokenResponse
from app.modules.auth.service import authenticate_user, create_token_for_user

router = APIRouter()


@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Dang nhap va nhan JWT access token.
    Chi danh cho admin va librarian.
    """
    user = authenticate_user(db, request.username, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error_response(message=ErrorMessage.INVALID_CREDENTIALS),
        )

    token = create_token_for_user(user)
    return success_response(
        data=TokenResponse(access_token=token).model_dump(),
        message="Dang nhap thanh cong",
    )
