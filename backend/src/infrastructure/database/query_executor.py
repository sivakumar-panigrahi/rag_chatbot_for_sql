# Query executor interface/implementation
import time
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.query import QueryResponse


class QueryExecutor:
    """
    Executes SQL queries safely.
    """

    MAX_ROWS = 1000

    def __init__(
        self,
        db: AsyncSession,
    ) -> None:
        self.db = db

    async def execute(
        self,
        sql: str,
    ) -> QueryResponse:
        start_time = time.perf_counter()

        try:
            result = await self.db.execute(
                text(sql)
            )

            mappings = result.mappings().fetchmany(
                self.MAX_ROWS
            )

            rows: list[dict[str, Any]] = [
                dict(row)
                for row in mappings
            ]

            columns = (
                list(rows[0].keys())
                if rows
                else []
            )

            execution_time_ms = (
                time.perf_counter() - start_time
            ) * 1000

            return QueryResponse(
                columns=columns,
                rows=rows,
                row_count=len(rows),
                execution_time_ms=round(
                    execution_time_ms,
                    2,
                ),
                success=True,
            )

        except Exception as e:
            execution_time_ms = (
                time.perf_counter() - start_time
            ) * 1000

            return QueryResponse(
                success=False,
                error=str(e),
                execution_time_ms=round(
                    execution_time_ms,
                    2,
                ),
            )