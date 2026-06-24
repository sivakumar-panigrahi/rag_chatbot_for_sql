# Schema document builder implementation
from typing import Any


class SchemaDocumentBuilder:
    """
    Converts database schema metadata
    into retrievable documents.
    """

    def build_documents(
        self,
        schema: dict[str, Any],
    ) -> list[dict]:
        documents = []

        for table_name, columns in schema.items():

            column_lines = []

            for column in columns:
                column_lines.append(
                    f"- {column['name']} ({column['type']})"
                )

            document_text = (
                f"Table: {table_name}\n\n"
                f"Columns:\n"
                + "\n".join(column_lines)
            )

            documents.append(
                {
                    "table_name": table_name,
                    "content": document_text,
                }
            )

        return documents