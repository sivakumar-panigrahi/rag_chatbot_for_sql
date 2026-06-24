from datetime import datetime
from pydantic import BaseModel


class QueryLogResponse(BaseModel):
    id: int
    message_id: int | None = None
    question: str
    generated_sql: str | None = None
    execution_result: str | None = None
    is_success: bool
    error_message: str | None = None
    execution_time_ms: float | None = None

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    id: int
    conversation_id: int
    role: str
    content: str
    created_at: datetime
    query_logs: list[QueryLogResponse] = []

    class Config:
        from_attributes = True


class ConversationResponse(BaseModel):
    id: int
    title: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
