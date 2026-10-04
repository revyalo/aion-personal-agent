from aion.providers.base import ModelProvider
from aion.providers.errors import (
    ProviderQuotaExceeded,
    ProviderUnavailable,
)


class ProviderRouter(ModelProvider):
    def __init__(self, providers: list[ModelProvider]):
        if not providers:
            raise ValueError(
                "ProviderRouter requires at least one provider"
            )

        self.providers = providers

        # Modelos que ya sabemos que no tienen cuota
        # durante esta ejecución de AION.
        self.quota_exhausted_models = set()

    def generate(
        self,
        message: str,
        system_instruction: str,
    ) -> str:
        last_error = None

        for provider in self.providers:
            provider_name = getattr(
                provider,
                "model",
                provider.__class__.__name__,
            )

            # Si ya sabemos que este modelo no tiene cuota,
            # ni siquiera intentamos llamarlo.
            if provider_name in self.quota_exhausted_models:
                print(
                    f"[AION Router] Skipping: "
                    f"{provider_name} -> quota exhausted"
                )
                continue

            try:
                print(
                    f"[AION Router] Trying: {provider_name}"
                )

                response = provider.generate(
                    message,
                    system_instruction,
                )

                print(
                    f"[AION Router] Success: {provider_name}"
                )

                return response

            except ProviderQuotaExceeded as error:
                last_error = error

                self.quota_exhausted_models.add(
                    provider_name
                )

                print(
                    f"[AION Router] Failed: "
                    f"{provider_name} -> {error}"
                )

                continue

            except ProviderUnavailable as error:
                last_error = error

                print(
                    f"[AION Router] Failed: "
                    f"{provider_name} -> {error}"
                )

                continue

        if last_error is not None:
            raise last_error

        raise ProviderUnavailable(
            "No model provider was able to generate a response"
        )