from src.infrastructure.llm.groq_client import (
    GroqClient,
)

client = GroqClient()

response = client.generate(
    "Reply with only: Groq Connected"
)

print(response)