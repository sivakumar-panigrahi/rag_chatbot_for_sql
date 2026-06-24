from src.infrastructure.database.schema_introspector import (
    SchemaIntrospector,
)


class DomainGuardService:
    """
    Detects whether a question belongs
    to the database domain.
    """

    def __init__(
        self,
        schema_introspector: SchemaIntrospector,
    ) -> None:
        self.schema_introspector = (
            schema_introspector
        )

    async def is_in_scope(
        self,
        question: str,
    ) -> bool:

        question = question.lower()

        schema = (
            await self.schema_introspector
            .get_schema()
        )

        keywords = set()

        for table_name, columns in (
            schema.items()
        ):

            keywords.add(
                table_name.lower()
            )

            for column in columns:

                keywords.add(
                    column["name"].lower()
                )

        return any(
            keyword in question
            for keyword in keywords
        )