import os

from dotenv import load_dotenv


load_dotenv()


class Config:
    def __init__(self):
        self.provider = os.getenv(
            "AION_PROVIDER",
            "mock",
        )

        models_value = os.getenv(
            "AION_MODELS",
            os.getenv("AION_MODEL", "gemini-3-flash-preview"),
        )

        self.models = [
            model.strip()
            for model in models_value.split(",")
            if model.strip()
        ]

        # Compatibilidad temporal con el código anterior.
        self.model = self.models[0]