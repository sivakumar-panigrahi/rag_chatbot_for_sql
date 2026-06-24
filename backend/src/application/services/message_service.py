from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.feedback import Feedback
from src.domain.entities.message import Message
from src.domain.entities.query_log import QueryLog
from src.infrastructure.repositories.message_repository import MessageRepository


class MessageService:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = MessageRepository(db)

    async def add_message(
        self,
        conversation_id: int,
        role: str,
        content: str,
    ) -> Message:
        msg = await self.repo.create(
            conversation_id=conversation_id,
            role=role,
            content=content,
        )
        await self.db.commit()
        return msg

    async def get_messages_by_conversation(self, conversation_id: int) -> list[Message]:
        return await self.repo.get_by_conversation_id(conversation_id)

    async def add_feedback(
        self,
        message_id: int,
        rating: int,
        comments: str | None = None,
    ) -> Feedback:
        feedback = Feedback(
            message_id=message_id,
            rating=rating,
            comments=comments,
        )
        self.db.add(feedback)
        await self.db.flush()
        await self.db.commit()
        return feedback

    async def log_query(
        self,
        message_id: int | None,
        question: str,
        generated_sql: str | None = None,
        execution_result: str | None = None,
        is_success: bool = True,
        error_message: str | None = None,
        execution_time_ms: float | None = None,
    ) -> QueryLog:
        query_log = QueryLog(
            message_id=message_id,
            question=question,
            generated_sql=generated_sql,
            execution_result=execution_result,
            is_success=is_success,
            error_message=error_message,
            execution_time_ms=execution_time_ms,
        )
        self.db.add(query_log)
        await self.db.flush()
        await self.db.commit()
        return query_log
