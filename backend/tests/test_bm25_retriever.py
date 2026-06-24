from src.infrastructure.retriever.bm25_retriever import (
    BM25Retriever,
)

documents = [
    {
        "table_name": "customers",
        "content": "customer information customer email customer country",
    },
    {
        "table_name": "orders",
        "content": "order transaction order amount",
    },
]

retriever = BM25Retriever(
    documents
)

results = retriever.retrieve(
    "customer"
)

print(results)