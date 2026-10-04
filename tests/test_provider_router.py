from aion.providers.base import ModelProvider
from aion.providers.errors import ProviderQuotaExceeded
from aion.providers.router import ProviderRouter


class QuotaProvider(ModelProvider):
    def __init__(self):
        self.model = "quota-model"
        self.calls = 0

    def generate(
        self,
        message: str,
        system_instruction: str,
    ) -> str:
        self.calls += 1

        raise ProviderQuotaExceeded(
            "Quota exhausted"
        )


class WorkingProvider(ModelProvider):
    def __init__(self):
        self.model = "working-model"
        self.calls = 0

    def generate(
        self,
        message: str,
        system_instruction: str,
    ) -> str:
        self.calls += 1

        return "Respuesta correcta"


def test_router_falls_back_when_quota_is_exhausted():
    quota_provider = QuotaProvider()
    working_provider = WorkingProvider()

    router = ProviderRouter([
        quota_provider,
        working_provider,
    ])

    response = router.generate(
        "Hola",
        "You are AION",
    )

    assert response == "Respuesta correcta"
    assert quota_provider.calls == 1
    assert working_provider.calls == 1


def test_router_skips_exhausted_model_after_first_failure():
    quota_provider = QuotaProvider()
    working_provider = WorkingProvider()

    router = ProviderRouter([
        quota_provider,
        working_provider,
    ])

    router.generate(
        "Primer mensaje",
        "You are AION",
    )

    router.generate(
        "Segundo mensaje",
        "You are AION",
    )

    assert quota_provider.calls == 1
    assert working_provider.calls == 2