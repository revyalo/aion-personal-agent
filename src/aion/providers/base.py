from abc import ABC, abstractmethod


class ModelProvider(ABC):

    @abstractmethod
    def generate(
        self,
        message: str,
        system_instruction: str
    ) -> str:
        pass