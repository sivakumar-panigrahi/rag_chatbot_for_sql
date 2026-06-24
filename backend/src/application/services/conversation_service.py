from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.conversation import Conversation
from src.infrastructure.repositories.conversation_repository import ConversationRepository


class ConversationService:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = ConversationRepository(db)

    async def create_conversation(self, title: str | None = None) -> Conversation:
        conv = await self.repo.create(title=title or "New Conversation")
        await self.db.commit()
        return conv

    async def get_conversation(self, conversation_id: int) -> Conversation | None:
        return await self.repo.get(conversation_id)

    async def list_conversations(self, skip: int = 0, limit: int = 100) -> list[Conversation]:
        return await self.repo.list_conversations(skip=skip, limit=limit)

    async def delete_conversation(self, conversation_id: int) -> Conversation | None:
        conv = await self.repo.delete(conversation_id)
        await self.db.commit()
        return conv
