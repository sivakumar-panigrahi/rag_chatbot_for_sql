from src.infrastructure.llm.groq_client import (
    GroqClient,
)


class ResultExplanationService:
    """
    Converts query results into
    human-friendly explanations.
    """

    def __init__(self) -> None:
        self.llm = GroqClient()

    def explain(
        self,
        question: str,
        sql: str,
        results: list[dict],
    ) -> str:

        prompt = f"""
You are a business analyst.

Question:
{question}

SQL:
{sql}

Results:
{results}

Explain the results clearly in plain English.
Keep the explanation concise.
"""

        return self.llm.generate(
            prompt
        )