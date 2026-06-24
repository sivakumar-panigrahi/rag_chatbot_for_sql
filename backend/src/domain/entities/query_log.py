from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.base import Base

if TYPE_CHECKING:
    from src.domain.entities.message import Message


class QueryLog(Base):
    __tablename__ = "query_logs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    message_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey(
            "messages.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    question: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    generated_sql: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    execution_result: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    is_success: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    execution_time_ms: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        index=True,
    )

    # Relationships
    message: Mapped["Message | None"] = relationship(
        back_populates="query_logs",
        lazy="selectin",
    )