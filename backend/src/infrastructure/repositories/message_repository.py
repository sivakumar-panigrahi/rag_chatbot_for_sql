from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.message import Message
from src.infrastructure.repositories.base_repository import BaseRepository


class MessageRepository(BaseRepository[Message]):

    def __init__(self, db: AsyncSession):
        super().__init__(Message, db)

    async def create(
        self,
        conversation_id: int,
        role: str,
        content: str,
    ) -> Message:
        """
        Create a new message.
        """

        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
        )

        self.db.add(message)

        await self.db.flush()

        return message

    async def get_by_id(
        self,
        message_id: int,
    ) -> Message | None:
        """
        Get message by ID.
        """

        query = select(Message).where(
            Message.id == message_id
        )

        result = await self.db.execute(query)

        return result.scalar_one_or_none()

    async def get_by_conversation_id(
        self,
        conversation_id: int,
    ) -> list[Message]:
        """
        Get all messages for a conversation.
        """

        query = (
            select(Message)
            .where(
                Message.conversation_id
                == conversation_id
            )
            .order_by(
                Message.created_at.asc()
            )
        )

        result = await self.db.execute(query)

        return list(
            result.scalars().all()
        )

    async def get_latest_message(
        self,
        conversation_id: int,
    ) -> Message | None:
        """
        Get latest message in a conversation.
        """

        query = (
            select(Message)
            .where(
                Message.conversation_id
                == conversation_id
            )
            .order_by(
                Message.created_at.desc()
            )
            .limit(1)
        )

        result = await self.db.execute(query)

        return result.scalar_one_or_none()

    async def delete_by_conversation_id(
        self,
        conversation_id: int,
    ) -> int:
        """
        Delete all messages belonging to a conversation.
        Returns count of deleted messages.
        """

        messages = await self.get_by_conversation_id(
            conversation_id
        )

        count = len(messages)

        for message in messages:
            await self.db.delete(message)

        await self.db.flush()

        return count