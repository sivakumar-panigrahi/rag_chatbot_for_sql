from src.application.services.sql_generation_service import (
    SQLGenerationService,
)

service = SQLGenerationService()

schema = """
Table: customers

Columns:
- id
- name
- email
"""

sql = service.generate_sql(
    question="Show all customers",
    schema_context=schema,
)

print(sql)