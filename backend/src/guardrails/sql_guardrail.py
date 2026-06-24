# SQL guardrail implementation
import sqlglot
from sqlglot import expressions as exp


class SQLGuardrail:
    """
    Validates whether SQL is safe to execute.
    """

    FORBIDDEN_STATEMENTS = (
        exp.Delete,
        exp.Insert,
        exp.Update,
        exp.Drop,
        exp.Alter,
        exp.Create,
    )

    def validate(
        self,
        sql: str,
    ) -> tuple[bool, str | None]:
        try:
            parsed = sqlglot.parse_one(
                sql
            )

        except Exception as e:
            return (
                False,
                f"Invalid SQL syntax: {e}",
            )

        if not isinstance(
            parsed,
            exp.Select,
        ):
            return (
                False,
                "Only SELECT statements are allowed.",
            )

        for statement in parsed.walk():
            if isinstance(
                statement,
                self.FORBIDDEN_STATEMENTS,
            ):
                return (
                    False,
                    f"Forbidden statement detected: {statement}",
                )

        return (
            True,
            None,
        )




