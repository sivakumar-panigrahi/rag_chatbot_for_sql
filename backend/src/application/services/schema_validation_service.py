import sqlglot
from sqlglot import exp

from src.infrastructure.database.schema_introspector import (
    SchemaIntrospector,
)


class SchemaValidationService:
    """
    Validates tables and columns
    against actual database schema.
    """

    def __init__(
        self,
        schema_introspector: SchemaIntrospector,
    ) -> None:
        self.schema_introspector = (
            schema_introspector
        )

    async def validate(
        self,
        sql: str,
    ) -> None:

        schema = await self.schema_introspector.get_schema()
        schema_lower = {k.lower(): [c["name"].lower() for c in v] for k, v in schema.items()}
        
        parsed = sqlglot.parse_one(
            sql,
            dialect="postgres",
        )

        tables = {
            table.name
            for table in parsed.find_all(
                exp.Table
            )
        }

        # Collect CTE names to allow them as valid tables
        ctes = {
            cte.alias
            for cte in parsed.find_all(
                exp.CTE
            )
        }

        tables_lower = {t.lower() for t in tables if t}
        schema_tables_lower = set(schema_lower.keys())
        ctes_lower = {c.lower() for c in ctes if c}

        for table in tables_lower:
            if table not in schema_tables_lower and table not in ctes_lower:
                # Find the original table name for the error message
                orig_name = next((t for t in tables if t and t.lower() == table), table)
                raise ValueError(
                    f"Table does not exist: {orig_name}"
                )

        valid_columns_lower = set()
        for columns in schema_lower.values():
            for col_name in columns:
                valid_columns_lower.add(col_name)

        # Collect all column aliases to allow them as valid columns
        aliases = {
            alias.alias
            for alias in parsed.find_all(
                exp.Alias
            )
        }
        aliases_lower = {alias.lower() for alias in aliases if alias}

        for column in parsed.find_all(
            exp.Column
        ):
            col_name = column.name.lower() if column.name else ""

            if (
                col_name
                and col_name != "*"
                and col_name not in valid_columns_lower
                and col_name not in aliases_lower
            ):
                raise ValueError(
                    f"Column does not exist: {column.name}"
                )