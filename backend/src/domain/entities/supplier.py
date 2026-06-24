# Supplier entity
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database.base import Base


class Supplier(Base):
    __tablename__ = "suppliers"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    supplier_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        index=True,
    )

    country: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )