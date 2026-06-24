from datetime import datetime
from typing import TYPE_CHECKING, Literal

from sqlalchemy import DateTime, ForeignKey, Integer, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.base import Base

if TYPE_CHECKING:
    from src.domain.entities.message import Message


class Feedback(Base):
    __tablename__ = "feedbacks"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    message_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "messages.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        unique=True,
        index=True,
    )

    rating: Mapped[Literal[-1, 1]] = mapped_column(
        Integer,
        nullable=False,
    )

    comment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        index=True,
    )

    # Relationships
    message: Mapped["Message"] = relationship(
        back_populates="feedback",
        lazy="selectin",
    )