from src.application.services.sql_generation_chain import (
    SQLGenerationChain,
)
from src.infrastructure.embeddings.embedding_service import (
    get_embedding_service,
)
from src.infrastructure.retriever.bm25_retriever import (
    BM25Retriever,
)
from src.infrastructure.retriever.hybrid_retriever import (
    HybridRetriever,
)
from src.infrastructure.retriever.vector_retriever import (
    VectorRetriever,
)
from src.infrastructure.vectorstore.in_memory_vector_store import (
    InMemoryVectorStore,
)

embedding_service = (
    get_embedding_service()
)

documents = [
    {
        "table_name": "customers",
        "content": """
Table: customers

Columns:
- id
- name
- email
""",
        "embedding": embedding_service.embed_text(
            """
Table: customers

Columns:
- id
- name
- email
"""
        ),
    }
]

vector_store = (
    InMemoryVectorStore()
)

vector_store.add_documents(
    documents
)

vector_retriever = (
    VectorRetriever(
        vector_store
    )
)

bm25_retriever = (
    BM25Retriever(
        documents
    )
)

hybrid_retriever = (
    HybridRetriever(
        vector_retriever,
        bm25_retriever,
    )
)

chain = SQLGenerationChain(
    hybrid_retriever
)

sql, docs = chain.generate_sql(
    "Show all customers"
)

print(sql)