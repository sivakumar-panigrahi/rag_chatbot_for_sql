from src.infrastructure.llm.groq_client import (
    GroqClient,
)


class SQLGenerationService:
    """
    Generates SQL from natural language.
    """

    def __init__(self) -> None:
        self.llm = GroqClient()

    def generate_sql(
        self,
        question: str,
        schema_context: str,
    ) -> str:

        prompt = f"""
You are an expert PostgreSQL SQL generator.

Generate ONLY SQL.

Rules:

1. Output SQL only.
2. No markdown.
3. No explanation.
4. Read-only queries only.
5. Use PostgreSQL syntax.
6. Use LIMIT 100 if not specified.

Schema:

{schema_context}

Question:

{question}
"""

        return self.llm.generate(
            prompt
        )