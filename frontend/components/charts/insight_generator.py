from services.api_client import APIClient


class InsightGenerator:

    def __init__(self) -> None:
        self.client = APIClient("http://localhost:8089")

    def generate(
        self,
        question: str,
        results: list[dict],
    ) -> str:

        if not results:
            return "No data available."

        try:
            return self.client.generate_insights(question, results)
        except Exception as e:
            return f"Error generating insights: {str(e)}"