"""
Shared constants used across the application.
"""
 
 
class UserRole:
    """User roles in the system."""
 
    ADMIN = "admin"
    LIBRARIAN = "librarian"
 
 
class ErrorMessage:
    """Common error messages."""
 
    INVALID_CREDENTIALS = "Invalid username or password"
    TOKEN_EXPIRED = "Token has expired"
    TOKEN_INVALID = "Invalid token"
    PERMISSION_DENIED = "Permission denied"
    USER_NOT_FOUND = "User not found"
    USER_ALREADY_EXISTS = "Username already exists"
    INTERNAL_ERROR = "Internal server error, please try again"
 
    # Reader (patron) module
    READER_NOT_FOUND = "Reader not found"
    READER_CODE_ALREADY_EXISTS = "Reader code already exists"
    READER_EMAIL_ALREADY_EXISTS = "Reader email already exists"
 