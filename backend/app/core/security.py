"""
Module xu ly password hashing va JWT token.
Su dung passlib (bcrypt) de hash password va python-jose de tao/xac thuc JWT.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# ---- Password hashing ----
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash mot password bang bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """So sanh password nguoi dung nhap voi password da hash."""
    return pwd_context.verify(plain_password, hashed_password)


# ---- JWT token ----
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Tao JWT access token.
    `data` can chua it nhat key "sub" (subject, thuong la username hoac user_id).
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta
        if expires_delta
        else timedelta(minutes=settings.access_token_expire_minutes)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """
    Giai ma JWT token. Tra ve payload dict neu hop le, None neu khong.
    """
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        return payload
    except JWTError:
        return None
