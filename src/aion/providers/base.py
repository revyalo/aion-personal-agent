from abc import ABC, abstractmethod


class ModelProvider(ABC):

    @abstractmethod
    def generate(self, message: str) -> str:
        pass