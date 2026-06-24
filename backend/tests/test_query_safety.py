from src.application.services.query_safety_service import (
    QuerySafetyService,
)

service = QuerySafetyService()

print("--- Test 1 (Default Limit) ---")
sql1 = """
SELECT *
FROM customers
"""
safe_sql = service.enforce(sql1)
print(safe_sql)

print("\n--- Test 2 (Limit Too High) ---")
sql2 = """
SELECT *
FROM customers
LIMIT 5000
"""
try:
    service.enforce(sql2)
    print("Failed: Allowed LIMIT 5000!")
except ValueError as e:
    print("ValueError:")
    print(e)