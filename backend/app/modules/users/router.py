"""
Router for user management endpoints.
Only admins can create users or view the user list.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.common.constants import ErrorMessage
from app.common.response import error_response, success_response
from app.core.database import get_db
from app.core.deps import require_admin
from app.modules.users.model import User
from app.modules.users.schema import UserCreate, UserResponse
from app.modules.users.service import create_user, get_all_users, get_user_by_username

router = APIRouter()


@router.post("")
def create_new_user(
    request: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """Create a new user (admin only)."""
    existing = get_user_by_username(db, request.username)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_response(message=ErrorMessage.USER_ALREADY_EXISTS),
        )
    user = create_user(
        db,
        username=request.username,
        password=request.password,
        full_name=request.full_name,
        role=request.role,
    )
    return success_response(
        data=UserResponse.model_validate(user).model_dump(),
        message="User created successfully",
    )


@router.get("")
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """Retrieve all users (admin only)."""
    users = get_all_users(db)
    data = [UserResponse.model_validate(u).model_dump() for u in users]
    return success_response(data=data, message="Users retrieved successfully")
