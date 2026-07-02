"""
Dependencies dung chung cho xac thuc va phan quyen.
Cac router khac import get_current_user, require_admin, require_librarian tu day.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.common.constants import ErrorMessage, UserRole
from app.core.database import get_db
from app.core.security import decode_access_token
from app.modules.users.model import User

security_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Dependency lay user hien tai tu JWT token trong header Authorization.
    Tra ve User object neu token hop le, raise 401 neu khong.
    """
    token = credentials.credentials
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorMessage.TOKEN_INVALID,
        )

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorMessage.TOKEN_INVALID,
        )

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorMessage.USER_NOT_FOUND,
        )
    return user


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """Dependency yeu cau user phai la admin."""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ErrorMessage.PERMISSION_DENIED,
        )
    return current_user


def require_librarian(current_user: User = Depends(get_current_user)) -> User:
    """Dependency yeu cau user phai la librarian hoac admin."""
    if current_user.role not in (UserRole.ADMIN, UserRole.LIBRARIAN):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ErrorMessage.PERMISSION_DENIED,
        )
    return current_user
