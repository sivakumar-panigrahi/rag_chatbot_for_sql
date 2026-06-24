# Ingestion service implementation
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.schema_introspector import (
    SchemaIntrospector,
)
from src.infrastructure.embeddings.embedding_service import (
    get_embedding_service,
)
from src.infrastructure.ingestion.schema_document_builder import (
    SchemaDocumentBuilder,
)


class IngestionService:
    """
    Builds schema documents and generates embeddings.
    """

    def __init__(
        self,
        db: AsyncSession,
    ) -> None:
        self.db = db

        self.schema_introspector = (
            SchemaIntrospector(db)
        )

        self.document_builder = (
            SchemaDocumentBuilder()
        )

        self.embedding_service = (
            get_embedding_service()
        )

    async def ingest_schema(
        self,
    ) -> list[dict]:
        """
        Generate documents and embeddings
        from the database schema.
        """

        schema = await (
            self.schema_introspector.get_schema()
        )

        documents = (
            self.document_builder
            .build_documents(schema)
        )

        for document in documents:

            embedding = (
                self.embedding_service
                .embed_text(
                    document["content"]
                )
            )

            document["embedding"] = (
                embedding
            )

        return documents