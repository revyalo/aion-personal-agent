from aion.providers.base import ModelProvider


class MockProvider(ModelProvider):

    def generate(self, message: str) -> str:
        return f"AION ha recibido: {message}"