import numpy as np


class InMemoryVectorStore:
    """
    In-memory vector store for storing documents and performing
    cosine similarity searches on their embeddings.
    """

    def __init__(self) -> None:
        self.documents: list[dict] = []

    def add_documents(self, documents: list[dict]) -> None:
        """
        Add documents to the in-memory vector store.
        """
        self.documents.extend(documents)

    def similarity_search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
    ) -> list[dict]:
        """
        Find top_k documents most similar to the query embedding.
        Since embeddings are normalized, we can use the dot product.
        """
        if not self.documents:
            return []

        query_vec = np.array(query_embedding)
        scored_documents = []

        for doc in self.documents:
            doc_embedding = doc.get("embedding")
            if doc_embedding is None:
                continue

            doc_vec = np.array(doc_embedding)
            similarity = float(np.dot(query_vec, doc_vec))

            # Store similarity score in the returned document copy
            doc_copy = doc.copy()
            doc_copy["similarity"] = similarity
            scored_documents.append(doc_copy)

        # Sort descending by similarity
        scored_documents.sort(key=lambda x: x["similarity"], reverse=True)

        return scored_documents[:top_k]
