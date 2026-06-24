from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.base import Base


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    conversation_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False,
    )
    role: Mapped[str] = mapped_column(String(50), nullable=False)  # "user" or "assistant"
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    # Relationships
    conversation = relationship(
        "Conversation",
        back_populates="messages",
    )
    feedback = relationship(
        "Feedback",
        back_populates="message",
        cascade="all, delete-orphan",
        uselist=False,
        lazy="selectin",
    )
    query_logs = relationship(
        "QueryLog",
        back_populates="message",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
