# Sale entity
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Float, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.base import Base

if TYPE_CHECKING:
    from src.domain.entities.customer import Customer
    from src.domain.entities.product import Product


class Sale(Base):
    __tablename__ = "sales"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    customer_id: Mapped[int] = mapped_column(
        ForeignKey(
            "customers.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey(
            "products.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    sale_amount: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    sale_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        index=True,
    )

    customer: Mapped["Customer"] = relationship(
        back_populates="sales",
        lazy="selectin",
    )

    product: Mapped["Product"] = relationship(
        back_populates="sales",
        lazy="selectin",
    )