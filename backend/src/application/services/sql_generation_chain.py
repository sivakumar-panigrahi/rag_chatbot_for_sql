from src.application.services.sql_generation_service import (
    SQLGenerationService,
)
from src.infrastructure.retriever.hybrid_retriever import (
    HybridRetriever,
)


class SQLGenerationChain:
    """
    End-to-end RAG SQL generation.
    """

    def __init__(
        self,
        retriever: HybridRetriever,
    ) -> None:
        self.retriever = retriever

        self.sql_generator = (
            SQLGenerationService()
        )

    def generate_sql(
        self,
        question: str,
    ) -> tuple[str, list[dict]]:

        retrieved_docs = (
            self.retriever.retrieve(
                question,
                top_k=5,
            )
        )

        schema_context = "\n\n".join(
            doc["content"]
            for doc in retrieved_docs
        )

        sql = (
            self.sql_generator.generate_sql(
                question=question,
                schema_context=schema_context,
            )
        )

        return (
            sql,
            retrieved_docs,
        )