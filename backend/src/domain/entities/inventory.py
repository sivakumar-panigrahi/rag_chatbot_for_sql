# Inventory entity
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.base import Base

if TYPE_CHECKING:
    from src.domain.entities.product import Product


class Inventory(Base):
    __tablename__ = "inventory"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey(
            "products.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    stock_quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    warehouse_location: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    product: Mapped["Product"] = relationship(
        back_populates="inventory_records",
        lazy="selectin",
    )