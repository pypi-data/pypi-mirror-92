from abc import ABC, abstractmethod
from decimal import Decimal
from typing import List

from . import ConditionPayload, EntrySettings


class AbstractRuleValue(ABC):
    @abstractmethod
    def get_values(self, **kwargs) -> List[Decimal]:
        pass

class StaticMultipeRuleValues(AbstractRuleValue):
    def __init__(self, values: List[Decimal]):
        self.values = values

    def get_values(self, **kwargs) -> List[Decimal]:
        return self.values

class StaticSingleRuleValue(StaticMultipeRuleValues):
    def __init__(self, value: Decimal):
        super().__init__([ value ])

class PandasColumnRuleValue(AbstractRuleValue):
    def __init__(self, column: str, last: int = -10):
        self.column = column
        self.last = last

    def get_values(self, **kwargs) -> List[Decimal]:
        conditon_payload: ConditionPayload = kwargs['condition_payload']
        df = conditon_payload.frame[self.column]
        return df[self.last:].tolist()
