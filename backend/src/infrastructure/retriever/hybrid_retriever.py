# Hybrid retriever implementation
from src.infrastructure.retriever.bm25_retriever import (
    BM25Retriever,
)
from src.infrastructure.retriever.vector_retriever import (
    VectorRetriever,
)


class HybridRetriever:
    """
    Combines BM25 and vector retrieval.
    """

    def __init__(
        self,
        vector_retriever: VectorRetriever,
        bm25_retriever: BM25Retriever,
    ) -> None:
        self.vector_retriever = (
            vector_retriever
        )

        self.bm25_retriever = (
            bm25_retriever
        )

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[dict]:
        vector_results = (
            self.vector_retriever.retrieve(
                query,
                top_k=top_k,
            )
        )

        bm25_results = (
            self.bm25_retriever.retrieve(
                query,
                top_k=top_k,
            )
        )

        merged = {}

        for doc in (
            vector_results + bm25_results
        ):
            merged[
                doc["table_name"]
            ] = doc

        return list(
            merged.values()
        )[:top_k]