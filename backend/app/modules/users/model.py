"""
Model bang `users` trong database.
Luu thong tin tai khoan dang nhap cua admin va librarian.
"""

from sqlalchemy import Column, DateTime, Enum, Integer, String, func

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(
        Enum("admin", "librarian", name="user_role"),
        nullable=False,
        default="librarian",
    )
    is_active = Column(Integer, default=1, nullable=False)  # 1 = active, 0 = disabled
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
