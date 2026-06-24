import asyncio

from src.infrastructure.database.session import (
    AsyncSessionLocal,
)
from src.infrastructure.database.query_executor import (
    QueryExecutor,
)


async def main():

    async with AsyncSessionLocal() as db:

        executor = QueryExecutor(db)

        result = await executor.execute(
            "SELECT * FROM customers LIMIT 5"
        )

        print(result)


asyncio.run(main())