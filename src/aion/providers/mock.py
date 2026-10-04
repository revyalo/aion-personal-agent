from aion.providers.base import ModelProvider


class MockProvider(ModelProvider):
    def generate(
        self,
        message: str,
        system_instruction: str,
    ) -> str:
        return f"AION ha recibido: {message}"