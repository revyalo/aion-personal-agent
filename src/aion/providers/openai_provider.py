from openai import OpenAI

from aion.providers.base import ModelProvider


class OpenAIProvider(ModelProvider):
    def __init__(self, model: str):
        self.client = OpenAI()
        self.model = model

    def generate(
        self,
        message: str,
        system_instruction: str,
    ) -> str:
        response = self.client.responses.create(
            model=self.model,
            instructions=system_instruction,
            input=message,
        )

        return response.output_text