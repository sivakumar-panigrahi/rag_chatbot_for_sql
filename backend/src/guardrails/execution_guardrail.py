# Execution guardrail implementation
class ExecutionGuardrail:
    """
    Enforces execution limits.
    """

    MAX_ROWS = 1000

    QUERY_TIMEOUT_SECONDS = 5

    def get_max_rows(self) -> int:
        return self.MAX_ROWS

    def get_timeout(self) -> int:
        return self.QUERY_TIMEOUT_SECONDS