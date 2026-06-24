# BM25 retriever implementation
from rank_bm25 import BM25Okapi


class BM25Retriever:
    """
    Keyword-based retrieval using BM25.
    """

    def __init__(
        self,
        documents: list[dict],
    ) -> None:
        self.documents = documents

        self.corpus = [
            doc["content"].lower().split()
            for doc in documents
        ]

        self.bm25 = BM25Okapi(
            self.corpus
        )

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[dict]:
        """
        Retrieve documents using BM25.
        """

        tokenized_query = (
            query.lower().split()
        )

        scores = self.bm25.get_scores(
            tokenized_query
        )

        ranked = sorted(
            zip(scores, self.documents),
            reverse=True,
            key=lambda x: x[0],
        )

        return [
            doc
            for _, doc in ranked[:top_k]
        ]