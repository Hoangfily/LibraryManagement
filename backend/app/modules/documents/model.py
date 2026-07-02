"""
Document model — defines the `documents` table in the database.
Stores information about library books and documents.
"""

from sqlalchemy import Column, DateTime, Integer, String, Text, func

from app.core.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False, index=True)
    author = Column(String(150), nullable=True)
    publisher = Column(String(150), nullable=True)
    publish_year = Column(Integer, nullable=True)
    category = Column(String(100), nullable=True)
    isbn = Column(String(20), unique=True, nullable=True, index=True)
    description = Column(Text, nullable=True)
    total_copies = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
