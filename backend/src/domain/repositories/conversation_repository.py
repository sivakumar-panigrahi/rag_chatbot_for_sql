# Conversation repository interface
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.conversation import Conversation


class ConversationRepository:
    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    async def get_all(self):
        result = await self.db.execute(
            select(Conversation)
        )
        return result.scalars().all()

    async def create(
        self,
        title: str,
    ):
        conversation = Conversation(
            title=title
        )

        self.db.add(conversation)

        await self.db.commit()

        await self.db.refresh(conversation)

        return conversation
