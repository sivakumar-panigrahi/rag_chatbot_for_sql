from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.factories.chat_service_factory import (
    ChatServiceFactory,
)
from src.infrastructure.database.session import (
    get_db,
)
from src.presentation.schemas.chat import (
    ChatRequest,
    InsightsRequest,
    InsightsResponse,
)
from src.infrastructure.llm.groq_client import (
    GroqClient,
)

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post("")
async def chat(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db),
):

    service = (
        await ChatServiceFactory.build(
            db
        )
    )

    return await service.chat(
        request.question,
        request.conversation_id,
    )


@router.post("/insights", response_model=InsightsResponse)
async def generate_insights(
    request: InsightsRequest,
):
    if not request.results:
        return InsightsResponse(insights="No data available.")

    prompt = f"""
You are a business analyst.

Question:
{request.question}

Results:
{request.results[:10]}

Provide:

1. Key finding
2. Trend
3. Business insight

Keep under 100 words.
"""
    llm = GroqClient()
    insights = llm.generate(prompt)
    return InsightsResponse(insights=insights)