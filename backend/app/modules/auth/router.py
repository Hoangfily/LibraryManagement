"""
Router for authentication endpoints: login.
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
    Login and receive a JWT access token.
    Only for admin and librarian users.
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
        message="Login successful",
    )
