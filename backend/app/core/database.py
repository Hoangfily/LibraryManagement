"""
Khung ket noi SQLAlchemy den MySQL.
Import tat ca models de Base.metadata biet duoc tat ca cac bang.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

# Khoi tao engine va session
engine = create_engine(settings.database_url, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency cap session database cho router/service."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Import tat ca models de SQLAlchemy nhan biet cac bang,
    sau do tao tat ca bang chua ton tai trong database.
    Goi ham nay khi ung dung khoi dong.
    """
    # Import models de chung duoc dang ky vao Base.metadata
    import app.modules.users.model  # noqa: F401
    import app.modules.readers.model  # noqa: F401
    import app.modules.documents.model  # noqa: F401
    import app.modules.copies.model  # noqa: F401
    import app.modules.borrows.model  # noqa: F401
    import app.modules.fines.model  # noqa: F401

    Base.metadata.create_all(bind=engine)
