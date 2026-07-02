"""
DocumentCopy model — defines the `document_copies` table in the database.
Each physical copy of a document is tracked individually for borrow management.
"""

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, func

from app.core.database import Base


class DocumentCopy(Base):
    __tablename__ = "document_copies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    document_id = Column(
        Integer, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True
    )
    copy_code = Column(String(30), unique=True, nullable=False, index=True)
    status = Column(
        Enum("available", "borrowed", "lost", "damaged", name="copy_status"),
        nullable=False,
        default="available",
    )
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
