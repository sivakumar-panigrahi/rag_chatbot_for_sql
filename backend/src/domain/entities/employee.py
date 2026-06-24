# Employee entity
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.base import Base

if TYPE_CHECKING:
    from src.domain.entities.department import Department


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    department_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "departments.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    salary: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    hire_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    department: Mapped["Department | None"] = relationship(
        back_populates="employees",
        lazy="selectin",
    )