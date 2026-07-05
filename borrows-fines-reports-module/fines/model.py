"""
Fine model — defines the `fines` table in the database.
Stores fine records when readers return books late or lose/damage them.
"""

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer, String, func

from app.core.database import Base


class Fine(Base):
    __tablename__ = "fines"

    id = Column(Integer, primary_key=True, autoincrement=True)
    borrow_item_id = Column(
        Integer, ForeignKey("borrow_items.id", ondelete="CASCADE"), nullable=False, index=True
    )
    reader_id = Column(
        Integer, ForeignKey("readers.id", ondelete="CASCADE"), nullable=False, index=True
    )
    fine_type = Column(
        Enum("overdue", "lost", "damaged", name="fine_type"),
        nullable=False,
    )
    amount = Column(Float, nullable=False, default=0)
    reason = Column(String(255), nullable=True)
    status = Column(
        Enum("unpaid", "paid", name="fine_status"),
        nullable=False,
        default="unpaid",
    )
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
