from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.conversation import Conversation
from src.infrastructure.repositories.base_repository import BaseRepository


class ConversationRepository(BaseRepository[Conversation]):

    def __init__(self, db: AsyncSession):
        super().__init__(Conversation, db)

    async def create(
        self,
        title: str | None = None,
    ) -> Conversation:
        """
        Create a new conversation.
        """

        conversation = Conversation(
            title=title
        )

        self.db.add(conversation)

        await self.db.flush()

        return conversation

    async def get_by_id(
        self,
        conversation_id: int,
    ) -> Conversation | None:
        """
        Get conversation by ID.
        """

        query = select(Conversation).where(
            Conversation.id == conversation_id
        )

        result = await self.db.execute(query)

        return result.scalar_one_or_none()

    async def get_by_title(
        self,
        title: str,
    ) -> Conversation | None:
        """
        Get conversation by title.
        """

        query = select(Conversation).where(
            Conversation.title == title
        )

        result = await self.db.execute(query)

        return result.scalar_one_or_none()

    async def list_conversations(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Conversation]:
        """
        List conversations ordered by latest update.
        """

        query = (
            select(Conversation)
            .order_by(
                Conversation.updated_at.desc()
            )
            .offset(skip)
            .limit(limit)
        )

        result = await self.db.execute(query)

        return list(
            result.scalars().all()
        )