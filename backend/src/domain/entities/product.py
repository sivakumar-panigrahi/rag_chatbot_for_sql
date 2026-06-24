# Product entity
from typing import TYPE_CHECKING

from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.base import Base

if TYPE_CHECKING:
    from src.domain.entities.order_item import OrderItem
    from src.domain.entities.inventory import Inventory
    from src.domain.entities.sale import Sale


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    product_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    category: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    price: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    order_items: Mapped[list["OrderItem"]] = relationship(
        back_populates="product",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    inventory_records: Mapped[list["Inventory"]] = relationship(
        back_populates="product",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    sales: Mapped[list["Sale"]] = relationship(
        back_populates="product",
        cascade="all, delete-orphan",
        lazy="selectin",
    )