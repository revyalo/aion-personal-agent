from google import genai
from google.genai import errors, types

from aion.providers.base import ModelProvider
from aion.providers.errors import ProviderQuotaExceeded


class GeminiProvider(ModelProvider):
    def __init__(self, model: str):
        self.client = genai.Client()
        self.model = model

    def generate(
        self,
        message: str,
        system_instruction: str,
    ) -> str:
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=message,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    automatic_function_calling=(
                        types.AutomaticFunctionCallingConfig(
                            disable=True
                        )
                    ),
                ),
            )

            return response.text

        except errors.ClientError as error:
            status_code = (
                getattr(error, "code", None)
                or getattr(error, "status_code", None)
            )

            if status_code == 429:
                raise ProviderQuotaExceeded(
                    f"Quota exceeded for Gemini model: {self.model}"
                ) from error

            raise