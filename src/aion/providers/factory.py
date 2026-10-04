from aion.providers.mock import MockProvider


def create_provider(provider_name: str):
    if provider_name == "mock":
        return MockProvider()

    raise ValueError(
        f"Unknown provider: {provider_name}"
    )