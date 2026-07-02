"""
Service for user authentication and JWT token generation.
"""

from sqlalchemy.orm import Session

from app.core.security import verify_password, create_access_token
from app.modules.users.model import User


def authenticate_user(db: Session, username: str, password: str) -> User | None:
    """
    Authenticate a user by username and password.
    Returns the User object if valid, None otherwise.
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
    """Create a JWT access token containing user information."""
    token_data = {
        "sub": str(user.id),
        "username": user.username,
        "role": user.role,
    }
    return create_access_token(data=token_data)
