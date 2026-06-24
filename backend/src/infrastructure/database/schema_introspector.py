# Schema introspector interface/implementation
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession


class SchemaIntrospector:
    """
    Extracts database schema metadata.
    """

    def __init__(
        self,
        db: AsyncSession,
    ) -> None:
        self.db = db

    async def get_schema(
        self,
    ) -> dict:
        def _inspect(sync_conn):
            inspector = inspect(sync_conn)

            schema = {}

            for table_name in inspector.get_table_names():
                columns = inspector.get_columns(
                    table_name
                )

                schema[table_name] = [
                    {
                        "name": col["name"],
                        "type": str(col["type"]),
                    }
                    for col in columns
                ]

            return schema

        conn = await self.db.connection()
        return await conn.run_sync(
            _inspect
        )