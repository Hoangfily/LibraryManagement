"""
Common API response format.
Every response follows the structure:
{
    "success": true/false,
    "message": "...",
    "data": ... | null
}
"""

from typing import Any, Optional

from pydantic import BaseModel


class APIResponse(BaseModel):
    """Common response schema for Swagger docs."""

    success: bool
    message: str
    data: Optional[Any] = None


def success_response(
    data: Any = None,
    message: str = "Success",
    status_code: int = 200,
) -> dict:
    """Return a standardized success response."""
    return {
        "success": True,
        "message": message,
        "data": data,
    }


def error_response(
    message: str = "An error occurred",
    status_code: int = 400,
    data: Any = None,
) -> dict:
    """Return a standardized error response."""
    return {
        "success": False,
        "message": message,
        "data": data,
    }
