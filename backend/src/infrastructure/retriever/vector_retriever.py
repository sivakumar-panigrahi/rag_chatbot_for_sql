# Vector retriever implementation
from src.infrastructure.embeddings.embedding_service import (
    get_embedding_service,
)
from src.infrastructure.vectorstore.in_memory_vector_store import (
    InMemoryVectorStore,
)


class VectorRetriever:
    """
    Semantic vector retrieval using embeddings.
    """

    def __init__(
        self,
        vector_store: InMemoryVectorStore,
    ) -> None:
        self.vector_store = vector_store
        self.embedding_service = (
            get_embedding_service()
        )

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[dict]:
        """
        Retrieve semantically similar documents.
        """

        query_embedding = (
            self.embedding_service.embed_text(
                query
            )
        )

        return self.vector_store.similarity_search(
            query_embedding=query_embedding,
            top_k=top_k,
        )