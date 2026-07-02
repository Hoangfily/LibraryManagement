"""
Service xu ly logic xac thuc nguoi dung va JWT.
"""

from sqlalchemy.orm import Session

from app.core.security import verify_password, create_access_token
from app.modules.users.model import User


def authenticate_user(db: Session, username: str, password: str) -> User | None:
    """
    Xac thuc user bang username va password.
    Tra ve User object neu hop le, None neu sai.
    """
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    if not user.is_active:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_token_for_user(user: User) -> str:
    """Tao JWT access token chua thong tin user."""
    token_data = {
        "sub": str(user.id),
        "username": user.username,
        "role": user.role,
    }
    return create_access_token(data=token_data)
