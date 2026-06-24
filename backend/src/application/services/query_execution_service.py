import time
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from src.application.services.query_safety_service import (
    QuerySafetyService,
)
from src.application.services.schema_validation_service import (
    SchemaValidationService,
)
from src.application.services.sql_generation_chain import (
    SQLGenerationChain,
)
from src.application.services.sql_validation_service import (
    SQLValidationService,
)
from src.infrastructure.database.query_executor import (
    QueryExecutor,
)
from src.infrastructure.database.schema_introspector import (
    SchemaIntrospector,
)
from src.infrastructure.retriever.hybrid_retriever import (
    HybridRetriever,
)

from src.application.services.domain_guard_service import (
    DomainGuardService,
)

from src.core.exceptions.domain_exceptions import (
    OutOfScopeQuestionError,
)


class QueryExecutionService:
    """
    End-to-end SQL chatbot execution pipeline.
    """

    def __init__(
        self,
        db: AsyncSession,
        retriever: HybridRetriever,
    ) -> None:

        self.db = db

        self.chain = SQLGenerationChain(
            retriever
        )

        self.sql_validator = (
            SQLValidationService()
        )

        self.schema_validator = (
            SchemaValidationService(
                SchemaIntrospector(db)
            )
        )

        self.query_safety = (
            QuerySafetyService()
        )

        self.query_executor = (
            QueryExecutor(db)
        )

    async def execute(
        self,
        question: str,
    ) -> dict[str, Any]:

        start_time = time.perf_counter()

        generated_sql, retrieved_docs = (
            self.chain.generate_sql(
                question
            )
        )

        validated_sql = (
            self.sql_validator.validate(
                generated_sql
            )
        )

        await (
            self.schema_validator.validate(
                validated_sql
            )
        )

        safe_sql = (
            self.query_safety.enforce(
                validated_sql
            )
        )

        query_response = await (
            self.query_executor.execute(
                safe_sql
            )
        )

        if not query_response.success:
            raise ValueError(
                f"Database query execution failed: {query_response.error}"
            )

        rows = query_response.rows

        execution_time = (
            time.perf_counter()
            - start_time
        )

        return {
            "question": question,
            "generated_sql": generated_sql,
            "safe_sql": safe_sql,
            "results": rows,
            "retrieved_docs": retrieved_docs,
            "execution_time": round(
                execution_time,
                3,
            ),
        }