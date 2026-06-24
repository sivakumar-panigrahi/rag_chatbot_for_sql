from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str
    conversation_id: int | None = None


class ChatResponse(BaseModel):
    conversation_id: int
    question: str
    sql: str
    explanation: str
    results: list
    execution_time: float


class InsightsRequest(BaseModel):
    question: str
    results: list


class InsightsResponse(BaseModel):
    insights: str