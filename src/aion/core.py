from aion.identity import load_or_create_identity
from aion.event_store import append_event, initialize_event_store
from aion.providers.mock import MockProvider


class AionCore:
    def __init__(self):
        initialize_event_store()

        self.identity = load_or_create_identity()
        self.provider = MockProvider()

    def chat(self, message: str) -> str:
        append_event(
            "user_message",
            {"text": message}
        )

        response = self.provider.generate(message)

        append_event(
            "assistant_message",
            {"text": response}
        )

        return response