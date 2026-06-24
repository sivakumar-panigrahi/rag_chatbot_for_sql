from sqlalchemy.ext.asyncio import AsyncSession

from src.application.services.chat_service import (
    ChatService,
)
from src.infrastructure.database.schema_introspector import (
    SchemaIntrospector,
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


class ChatServiceFactory:

    @staticmethod
    async def build(
        db: AsyncSession,
    ) -> ChatService:

        schema = await (
            SchemaIntrospector(db)
            .get_schema()
        )

        documents = []

        embedding_service = (
            get_embedding_service()
        )

        for table_name, columns in (
            schema.items()
        ):

            content = (
                f"Table: {table_name}\n\n"
            )

            for column in columns:

                content += (
                    f"- {column['name']} "
                    f"({column['type']})\n"
                )

            documents.append(
                {
                    "table_name": table_name,
                    "content": content,
                    "embedding": (
                        embedding_service
                        .embed_text(
                            content
                        )
                    ),
                }
            )

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

        return ChatService(
            db=db,
            retriever=hybrid_retriever,
        )