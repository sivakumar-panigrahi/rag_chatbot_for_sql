# Message repository interface
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.message import Message


class MessageRepository:
    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    async def get_messages(
        self,
        conversation_id: int,
    ):
        result = await self.db.execute(
            select(Message).where(
                Message.conversation_id == conversation_id
            )
        )

        return result.scalars().all()