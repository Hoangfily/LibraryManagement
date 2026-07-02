"""
SQLAlchemy database connection and session management.
Imports all models so Base.metadata is aware of all tables.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

# Initialize engine and session
engine = create_engine(settings.database_url, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency that provides a database session to routers/services."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Import all models so they are registered with Base.metadata,
    then create all tables that do not yet exist in the database.
    Call this function on application startup.
    """
    # Import models to register them with Base.metadata
    import app.modules.users.model  # noqa: F401
    import app.modules.readers.model  # noqa: F401
    import app.modules.documents.model  # noqa: F401
    import app.modules.copies.model  # noqa: F401
    import app.modules.borrows.model  # noqa: F401
    import app.modules.fines.model  # noqa: F401

    Base.metadata.create_all(bind=engine)
