from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class QueryRequest(BaseModel):
    """
    Request schema for executing a SQL query.
    """

    sql: str = Field(
        ...,
        description="SQL query to execute",
        examples=[
            "SELECT * FROM customers LIMIT 10"
        ],
    )


class QueryResponse(BaseModel):
    """
    Response schema returned after query execution.
    """

    columns: list[str] = Field(
        default_factory=list,
        description="Column names returned by the query",
    )

    rows: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Query results",
    )

    row_count: int = Field(
        default=0,
        description="Number of rows returned",
    )

    execution_time_ms: float = Field(
        default=0.0,
        description="Execution time in milliseconds",
    )

    success: bool = Field(
        default=True,
        description="Whether the query executed successfully",
    )

    error: str | None = Field(
        default=None,
        description="Error message if execution failed",
    )

    model_config = ConfigDict(
        from_attributes=True,
    )