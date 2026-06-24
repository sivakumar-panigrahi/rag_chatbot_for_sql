# API client service
import requests


class APIClient:

    def __init__(
        self,
        base_url: str,
    ) -> None:

        self.base_url = (
            base_url.rstrip("/")
        )

    def chat(
        self,
        question: str,
        conversation_id: int | None = None,
    ) -> dict:

        payload = {"question": question}
        if conversation_id is not None:
            payload["conversation_id"] = conversation_id

        response = requests.post(
            f"{self.base_url}/chat",
            json=payload,
            timeout=60,
        )

        response.raise_for_status()

        return response.json()

    def list_conversations(self) -> list[dict]:
        response = requests.get(
            f"{self.base_url}/conversations",
            timeout=10,
        )
        response.raise_for_status()
        return response.json()

    def get_messages(self, conversation_id: int) -> list[dict]:
        response = requests.get(
            f"{self.base_url}/conversations/{conversation_id}/messages",
            timeout=10,
        )
        response.raise_for_status()
        return response.json()

    def delete_conversation(self, conversation_id: int) -> dict:
        # Cascade delete is handled by backend database session config
        response = requests.delete(
            f"{self.base_url}/conversations/{conversation_id}",
            timeout=10,
        )
        response.raise_for_status()
        return response.json()

    def generate_insights(self, question: str, results: list) -> str:
        payload = {"question": question, "results": results}
        response = requests.post(
            f"{self.base_url}/chat/insights",
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        return response.json()["insights"]