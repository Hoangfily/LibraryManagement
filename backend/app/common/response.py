"""
Dinh nghia format response chung cho toan bo API.
Moi response deu co dang:
{
    "success": true/false,
    "message": "...",
    "data": ... | null
}
"""

from typing import Any, Optional

from pydantic import BaseModel


class APIResponse(BaseModel):
    """Schema chung de hien thi tren Swagger docs."""

    success: bool
    message: str
    data: Optional[Any] = None


def success_response(
    data: Any = None,
    message: str = "Thanh cong",
    status_code: int = 200,
) -> dict:
    """Tra ve response thanh cong voi format chuan."""
    return {
        "success": True,
        "message": message,
        "data": data,
    }


def error_response(
    message: str = "Da xay ra loi",
    status_code: int = 400,
    data: Any = None,
) -> dict:
    """Tra ve response loi voi format chuan."""
    return {
        "success": False,
        "message": message,
        "data": data,
    }
