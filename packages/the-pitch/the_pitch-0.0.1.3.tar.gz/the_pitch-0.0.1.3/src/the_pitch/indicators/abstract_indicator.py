from abc import ABC, abstractmethod
import pandas as pd


class AbstractIndicator(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def compute(self, frame: pd.DataFrame, **kwargs) -> pd.DataFrame:
        pass

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name
