from src.application.services.result_explanation_service import (
    ResultExplanationService,
)

service = (
    ResultExplanationService()
)

explanation = (
    service.explain(
        question="Show customers",
        sql="SELECT * FROM customers LIMIT 1",
        results=[
            {
                "id": 1,
                "name": "John",
                "country": "USA",
            }
        ],
    )
)

print(explanation)