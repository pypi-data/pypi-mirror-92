from abc import ABC, abstractmethod


class AbstractLogger(ABC):
    @abstractmethod
    def write(self, message: str) -> None:
        pass
