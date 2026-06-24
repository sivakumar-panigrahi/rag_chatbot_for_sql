# Customer entity
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.base import Base

if TYPE_CHECKING:
    from src.domain.entities.order import Order
    from src.domain.entities.sale import Sale


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        index=True,
    )

    city: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    country: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    signup_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    orders: Mapped[list["Order"]] = relationship(
        back_populates="customer",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    sales: Mapped[list["Sale"]] = relationship(
        back_populates="customer",
        cascade="all, delete-orphan",
        lazy="selectin",
    )