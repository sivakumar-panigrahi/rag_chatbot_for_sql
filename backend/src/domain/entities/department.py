# Department entity
from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.base import Base

if TYPE_CHECKING:
    from src.domain.entities.employee import Employee


class Department(Base):
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    department_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
        index=True,
    )

    employees: Mapped[list["Employee"]] = relationship(
        back_populates="department",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
