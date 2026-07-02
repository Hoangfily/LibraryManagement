"""
Business logic service for user management.
"""

from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.modules.users.model import User


def get_user_by_username(db: Session, username: str) -> User | None:
    """Find a user by username."""
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, username: str, password: str, full_name: str, role: str = "librarian") -> User:
    """Create a new user with a hashed password."""
    user = User(
        username=username,
        hashed_password=hash_password(password),
        full_name=full_name,
        role=role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_all_users(db: Session) -> list[User]:
    """Retrieve all users."""
    return db.query(User).all()


def seed_admin(db: Session):
    """
    Create the default admin account if it does not exist.
    Username: admin, Password: admin123
    """
    existing = get_user_by_username(db, "admin")
    if not existing:
        create_user(
            db,
            username="admin",
            password="admin123",
            full_name="Administrator",
            role="admin",
        )
        print("[SEED] Created default admin account: admin / admin123")
    else:
        print("[SEED] Admin account already exists, skipping.")
