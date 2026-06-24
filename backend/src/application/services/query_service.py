# Query service class
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.query_executor import (
    QueryExecutor,
)
from src.infrastructure.database.schema_introspector import (
    SchemaIntrospector,
)
from src.schemas.query import QueryResponse


class QueryService:
    """
    Business layer for SQL execution.
    """

    def __init__(
        self,
        db: AsyncSession,
    ) -> None:
        self.db = db
        self.executor = QueryExecutor(
            db
        )
        self.schema_introspector = (
            SchemaIntrospector(db)
        )

    async def execute_query(
        self,
        sql: str,
    ) -> QueryResponse:
        return await self.executor.execute(
            sql
        )

    async def get_schema(
        self,
    ) -> dict:
        return await (
            self.schema_introspector.get_schema()
        )