from fastapi import APIRouter

from src.presentation.api.v1.chat import (
    router as chat_router,
)
from src.presentation.api.v1.conversation import (
    router as conversation_router,
)
from src.presentation.api.v1.feedback import (
    router as feedback_router,
)
from src.presentation.api.v1.health import (
    router as health_router,
)
from src.presentation.api.v1.query import (
    router as query_router,
)

api_router = APIRouter()

api_router.include_router(
    chat_router
)

api_router.include_router(
    conversation_router
)

api_router.include_router(
    query_router
)

api_router.include_router(
    feedback_router
)

api_router.include_router(
    health_router
)