# Payment entity
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.base import Base

if TYPE_CHECKING:
    from src.domain.entities.order import Order


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    order_id: Mapped[int] = mapped_column(
        ForeignKey(
            "orders.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    payment_method: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    amount: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    payment_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    order: Mapped["Order"] = relationship(
        back_populates="payments",
        lazy="selectin",
    )