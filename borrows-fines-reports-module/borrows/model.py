i"""
Borrow models — defines `borrow_orders` and `borrow_items` tables.
- borrow_orders: a reader's borrow request.
- borrow_items: individual book copies within a borrow order.
"""

from sqlalchemy import Column, Date, DateTime, Enum, ForeignKey, Integer, func
from sqlalchemy.orm import relationship

from app.core.database import Base


class BorrowOrder(Base):
    __tablename__ = "borrow_orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    reader_id = Column(
        Integer, ForeignKey("readers.id", ondelete="CASCADE"), nullable=False, index=True
    )
    borrow_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    status = Column(
        Enum("borrowing", "returned", "overdue", "cancelled", name="order_status"),
        nullable=False,
        default="borrowing",
    )
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    items = relationship(
        "BorrowItem",
        backref="order",
        cascade="all, delete-orphan",
        order_by="BorrowItem.id",
    )


class BorrowItem(Base):
    __tablename__ = "borrow_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(
        Integer, ForeignKey("borrow_orders.id", ondelete="CASCADE"), nullable=False, index=True
    )
    copy_id = Column(
        Integer, ForeignKey("document_copies.id", ondelete="CASCADE"), nullable=False, index=True
    )
    returned_date = Column(Date, nullable=True)
    status = Column(
        Enum("borrowing", "returned", "lost", "cancelled", name="item_status"),
        nullable=False,
        default="borrowing",
    )
    created_at = Column(DateTime, server_default=func.now())
