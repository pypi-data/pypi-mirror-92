from ast import Str
from typing import List
from . import Condition, StrategyPayload, ConditionPayload


class Strategy(object):
    """ By combining various entry and exit conditions, we get a strategy. """
    def __init__(self,
                id: str,
                description: str,
                conditions: List[Condition] = []):
        self.id = id
        self.description = description
        self.conditions = conditions

    def get_valid_conditions(self, strategy_payload: StrategyPayload, **kwargs) -> List[Condition]:
        valid_conditions = []
        for condition in self.conditions:
            condition_payload = ConditionPayload(
                symbol=condition.settings.symbol,
                strategy_payload=strategy_payload
            )

            if condition.is_valid(condition_payload, **kwargs):
                valid_conditions.append(condition)

        return valid_conditions

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id
