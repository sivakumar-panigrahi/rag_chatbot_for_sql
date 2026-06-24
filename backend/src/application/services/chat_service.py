from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from src.application.services.query_execution_service import (
    QueryExecutionService,
)
from src.application.services.result_explanation_service import (
    ResultExplanationService,
)
from src.infrastructure.retriever.hybrid_retriever import (
    HybridRetriever,
)


class ChatService:
    """
    Main chatbot orchestration service.
    """

    def __init__(
        self,
        db: AsyncSession,
        retriever: HybridRetriever,
    ) -> None:

        self.db = db
        self.query_service = (
            QueryExecutionService(
                db=db,
                retriever=retriever,
            )
        )

        self.explanation_service = (
            ResultExplanationService()
        )

    async def chat(
        self,
        question: str,
        conversation_id: int | None = None,
    ) -> dict[str, Any]:

        from src.application.services.conversation_service import ConversationService
        from src.application.services.message_service import MessageService
        import json

        conv_service = ConversationService(self.db)
        msg_service = MessageService(self.db)

        # 1. Retrieve or create conversation
        if conversation_id:
            conv = await conv_service.get_conversation(conversation_id)
            if not conv:
                title = question[:40] + ("..." if len(question) > 40 else "")
                conv = await conv_service.create_conversation(title=title)
        else:
            title = question[:40] + ("..." if len(question) > 40 else "")
            conv = await conv_service.create_conversation(title=title)

        conversation_id = conv.id

        # 2. Save user message
        user_msg = await msg_service.add_message(
            conversation_id=conversation_id,
            role="user",
            content=question,
        )

        execution_result = (
            await self.query_service.execute(
                question
            )
        )

        explanation = (
            self.explanation_service.explain(
                question=question,
                sql=execution_result[
                    "safe_sql"
                ],
                results=execution_result[
                    "results"
                ],
            )
        )

        # 3. Save assistant message (explanation)
        assistant_msg = await msg_service.add_message(
            conversation_id=conversation_id,
            role="assistant",
            content=explanation,
        )

        # 4. Log query execution
        try:
            from fastapi.encoders import jsonable_encoder
            await msg_service.log_query(
                message_id=assistant_msg.id,
                question=question,
                generated_sql=execution_result["safe_sql"],
                execution_result=json.dumps(jsonable_encoder(execution_result["results"])) if execution_result["results"] else "[]",
                is_success=True,
                execution_time_ms=execution_result["execution_time"] * 1000.0,
            )
        except Exception:
            pass

        await self.db.commit()

        return {
            "conversation_id": conversation_id,
            "question": question,
            "sql": execution_result[
                "safe_sql"
            ],
            "results": execution_result[
                "results"
            ],
            "explanation": explanation,
            "execution_time": execution_result[
                "execution_time"
            ],
            "retrieved_docs": execution_result[
                "retrieved_docs"
            ],
        }