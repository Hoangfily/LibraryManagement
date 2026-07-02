"""
Pydantic schemas cho request/response cua auth module.
"""

from pydantic import BaseModel


class LoginRequest(BaseModel):
    """Schema cho request dang nhap."""

    username: str
    password: str


class TokenResponse(BaseModel):
    """Schema cho response tra ve JWT token."""

    access_token: str
    token_type: str = "bearer"
