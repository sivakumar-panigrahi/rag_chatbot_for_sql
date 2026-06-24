import re


class SQLGuardrails:
    """
    Safety rules for generated SQL.
    """

    FORBIDDEN_KEYWORDS = [
        "DROP",
        "DELETE",
        "UPDATE",
        "INSERT",
        "ALTER",
        "TRUNCATE",
        "CREATE",
        "GRANT",
        "REVOKE",
    ]

    @classmethod
    def validate(
        cls,
        sql: str,
    ) -> None:

        normalized = sql.upper()

        for keyword in (
            cls.FORBIDDEN_KEYWORDS
        ):
            if re.search(
                rf"\b{keyword}\b",
                normalized,
            ):
                raise ValueError(
                    f"Forbidden SQL keyword detected: {keyword}"
                )