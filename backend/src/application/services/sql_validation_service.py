import sqlglot
from sqlglot import exp

from src.core.security.sql_guardrails import (
    SQLGuardrails,
)


class SQLValidationService:
    """
    SQL validation layer.
    """

    def __init__(self, schema: dict[str, list[str]] = None) -> None:
        # Normalize schema keys and values to lowercase for case-insensitive validation
        self.schema = {}
        if schema:
            for table_name, columns in schema.items():
                self.schema[table_name.lower()] = [col.lower() for col in columns]

    def validate(
        self,
        sql: str,
    ) -> str:

        SQLGuardrails.validate(
            sql
        )

        parsed = sqlglot.parse_one(
            sql,
            dialect="postgres",
        )

        if not isinstance(
            parsed,
            exp.Select,
        ):
            raise ValueError(
                "Only SELECT statements are allowed."
            )

        # Validate tables and columns if a schema was provided
        if self.schema:
            queried_tables = []
            for t in parsed.find_all(exp.Table):
                if t.name:
                    queried_tables.append(t.name.lower())

            for table in queried_tables:
                if table not in self.schema:
                    raise ValueError(f"Table '{table}' does not exist in the database.")

            for col in parsed.find_all(exp.Column):
                if not col.name:
                    continue
                col_name = col.name.lower()
                table_prefix = (col.text("table") or "").lower()

                if table_prefix:
                    if table_prefix not in self.schema:
                        raise ValueError(f"Table '{table_prefix}' referenced in column '{col_name}' does not exist.")
                    if col_name not in self.schema[table_prefix]:
                        raise ValueError(f"Column '{col_name}' does not exist in table '{table_prefix}'.")
                else:
                    found = False
                    for table in queried_tables:
                        if col_name in self.schema.get(table, []):
                            found = True
                            break
                    if not found:
                        raise ValueError(
                            f"Column '{col_name}' does not exist in any of the queried tables: {', '.join(queried_tables)}."
                        )

        return sql