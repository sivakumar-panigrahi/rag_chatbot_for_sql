import asyncio

from src.application.services.schema_validation_service import (
    SchemaValidationService,
)
from src.infrastructure.database.schema_introspector import (
    SchemaIntrospector,
)
from src.infrastructure.database.session import (
    AsyncSessionLocal,
)


async def main():

    async with AsyncSessionLocal() as db:

        service = (
            SchemaValidationService(
                SchemaIntrospector(db)
            )
        )

        print("--- Running Positive Test ---")
        await service.validate(
            """
            SELECT *
            FROM customers
            """
        )
        print("Positive Validation Passed\n")

        print("--- Running Negative Test ---")
        try:
            await service.validate(
                """
                SELECT unicorn_column
                FROM customers
                """
            )
            print("Failed: Allowed non-existent column 'unicorn_column'!")
        except ValueError as e:
            print("ValueError:")
            print(e)


asyncio.run(main())