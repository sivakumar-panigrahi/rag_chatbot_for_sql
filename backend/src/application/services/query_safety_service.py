import sqlglot
from sqlglot import exp


class QuerySafetyService:
    """
    Enforces execution safety rules.
    """

    DEFAULT_LIMIT = 100
    MAX_LIMIT = 1000

    def enforce(
        self,
        sql: str,
    ) -> str:

        parsed = sqlglot.parse_one(
            sql,
            dialect="postgres",
        )

        if not isinstance(
            parsed,
            exp.Select,
        ):
            raise ValueError(
                "Only SELECT queries are allowed."
            )

        limit = parsed.args.get(
            "limit"
        )

        if limit is None:

            parsed.set(
                "limit",
                exp.Limit(
                    expression=exp.Literal.number(
                        self.DEFAULT_LIMIT
                    )
                ),
            )

        else:

            try:
                current_limit = int(
                    limit.expression.name
                )
            except Exception:
                raise ValueError(
                    "Invalid LIMIT clause."
                )

            if (
                current_limit
                > self.MAX_LIMIT
            ):
                raise ValueError(
                    f"LIMIT exceeds maximum allowed ({self.MAX_LIMIT})"
                )

        return parsed.sql(
            dialect="postgres"
        )