from groq import Groq

from src.core.config.settings import (
    get_settings,
)


class GroqClient:
    """
    Wrapper around Groq API.
    """


    def __init__(self) -> None:
        settings = get_settings()

        self.model_name = settings.GROQ_MODEL_NAME
        self.client = Groq(
            api_key=settings.GROQ_API_KEY
        )

    def generate(
        self,
        prompt: str,
        temperature: float = 0.0,
    ) -> str:
        """
        Generate LLM response.
        """

        response = (
            self.client.chat.completions.create(
                model=self.model_name,
                temperature=temperature,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            )
        )

        return (
            response
            .choices[0]
            .message
            .content
        )