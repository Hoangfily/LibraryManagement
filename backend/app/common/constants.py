"""
Khai bao cac hang so dung chung trong he thong.
"""


class UserRole:
    """Cac role cua user trong he thong."""

    ADMIN = "admin"
    LIBRARIAN = "librarian"


class ErrorMessage:
    """Cac thong bao loi chung."""

    INVALID_CREDENTIALS = "Sai ten dang nhap hoac mat khau"
    TOKEN_EXPIRED = "Token da het han"
    TOKEN_INVALID = "Token khong hop le"
    PERMISSION_DENIED = "Khong co quyen truy cap"
    USER_NOT_FOUND = "Khong tim thay nguoi dung"
    USER_ALREADY_EXISTS = "Ten dang nhap da ton tai"
    INTERNAL_ERROR = "Loi he thong, vui long thu lai"
