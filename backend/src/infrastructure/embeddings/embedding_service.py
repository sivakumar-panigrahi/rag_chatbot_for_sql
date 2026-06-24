# Embedding service class
from functools import lru_cache

from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """
    Service responsible for generating embeddings.
    """

    MODEL_NAME = "BAAI/bge-small-en-v1.5"

    def __init__(self) -> None:
        self.model = SentenceTransformer(
            self.MODEL_NAME
        )

    def embed_text(
        self,
        text: str,
    ) -> list[float]:
        """
        Generate embedding for a single text.
        """
        embedding = self.model.encode(
            text,
            normalize_embeddings=True,
        )

        return embedding.tolist()

    def embed_documents(
        self,
        documents: list[str],
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple documents.
        """
        embeddings = self.model.encode(
            documents,
            normalize_embeddings=True,
        )

        return embeddings.tolist()


@lru_cache
def get_embedding_service() -> EmbeddingService:
    """
    Singleton embedding service.
    """
    return EmbeddingService()