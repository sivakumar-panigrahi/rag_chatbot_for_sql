from src.application.services.sql_validation_service import (
    SQLValidationService,
)

db_schema = {
    "customers": ["id", "name", "email", "city"],
    "orders": ["id", "customer_id", "status"]
}

validator = SQLValidationService(schema=db_schema)

print("--- 1. Valid Query Test ---")
sql_ok = """
SELECT name, email
FROM customers
WHERE city = 'London'
LIMIT 100;
"""
try:
    print(validator.validate(sql_ok))
    print("Success: Valid query passed!")
except ValueError as e:
    print(f"Failed: Valid query blocked. Error: {e}")

print("\n--- 2. Invalid Table Test ---")
sql_bad_table = """
SELECT *
FROM products;
"""
try:
    validator.validate(sql_bad_table)
    print("Failed: Allowed non-existent table!")
except ValueError as e:
    print(f"Success: Correctly blocked. Error: {e}")

print("\n--- 3. Invalid Column Test ---")
sql_bad_column = """
SELECT age
FROM customers;
"""
try:
    validator.validate(sql_bad_column)
    print("Failed: Allowed non-existent column!")
except ValueError as e:
    print(f"Success: Correctly blocked. Error: {e}")

print("\n--- 4. Invalid Prefix Column Test ---")
sql_bad_prefix = """
SELECT orders.name
FROM orders;
"""
try:
    validator.validate(sql_bad_prefix)
    print("Failed: Allowed non-existent column prefix!")
except ValueError as e:
    print(f"Success: Correctly blocked. Error: {e}")