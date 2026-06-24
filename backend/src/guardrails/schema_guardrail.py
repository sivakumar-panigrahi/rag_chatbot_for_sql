# Schema guardrail implementation
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession


class SchemaGuardrail:
    """
    Ensures referenced tables exist.
    """

    def __init__(
        self,
        db: AsyncSession,
    ) -> None:
        self.db = db

    async def get_tables(
        self,
    ) -> list[str]:
        def _inspect(
            sync_connection,
        ):
            inspector = inspect(
                sync_connection
            )

            return (
                inspector.get_table_names()
            )

        return await self.db.run_sync(
            _inspect
        )