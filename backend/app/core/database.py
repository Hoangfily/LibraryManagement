from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

# Khung ket noi SQLAlchemy den MySQL.
engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    # Dependency cap session database cho router/service.
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
