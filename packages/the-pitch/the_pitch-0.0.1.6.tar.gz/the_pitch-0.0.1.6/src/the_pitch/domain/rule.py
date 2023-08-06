from abc import ABC, abstractmethod
from decimal import Decimal
from .rule_value import AbstractRuleValue
from .enums import LogicalOperator


def is_condition_valid(v1: Decimal, operator: LogicalOperator, v2: Decimal) -> bool:
    if operator == LogicalOperator.Equal:
        return v1 == v2

    if operator == LogicalOperator.NotEqual:
        return v1 != v2

    if operator == LogicalOperator.LessThan:
        return v1 < v2

    if operator == LogicalOperator.LessThanOrEqual:
        return v1 <= v2

    if operator == LogicalOperator.GreaterThan:
        return v1 > v2

    if operator == LogicalOperator.GreaterThanOrEqual:
        return v1 >= v2

    return False

class AbstractRule(ABC):
    @abstractmethod
    def is_valid(self, **kwargs) -> bool:
        pass

class SingleRule(AbstractRule):
    def __init__(self, value1: AbstractRuleValue, operator: LogicalOperator, value2: AbstractRuleValue, time_step: int = -1):
        self.value1 = value1
        self.operator = operator
        self.value2 = value2
        self.time_step = time_step

    def is_valid(self, **kwargs) -> bool:
        v1 = self.value1.get_values(**kwargs)[self.time_step]
        v2 = self.value2.get_values(**kwargs)[self.time_step]

        return is_condition_valid(v1, self.operator, v2)
