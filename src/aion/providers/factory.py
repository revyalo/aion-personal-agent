from aion.providers.gemini_provider import GeminiProvider
from aion.providers.mock import MockProvider
from aion.providers.openai_provider import OpenAIProvider
from aion.providers.router import ProviderRouter


def create_provider(
    provider_name: str,
    models: list[str],
):
    if provider_name == "mock":
        return MockProvider()

    if provider_name == "gemini":
        providers = [
            GeminiProvider(model)
            for model in models
        ]

        return ProviderRouter(providers)

    if provider_name == "openai":
        providers = [
            OpenAIProvider(model)
            for model in models
        ]

        return ProviderRouter(providers)

    raise ValueError(
        f"Unknown provider: {provider_name}"
    )