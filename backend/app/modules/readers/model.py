"""
Model bang `readers` trong database.
Luu thong tin doc gia (nguoi muon sach).
"""

from sqlalchemy import Column, Date, DateTime, Integer, String, func

from app.core.database import Base


class Reader(Base):
    __tablename__ = "readers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    reader_code = Column(String(20), unique=True, nullable=False, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=True)
    phone = Column(String(20), nullable=True)
    address = Column(String(255), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    is_active = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
