from typing import List, Tuple
from ..domain import PandasColumnRuleValue, SingleRule, LogicalOperator
from ..indicators import AbstractIndicator
from ..domain import Strategy, Condition, EntrySettings, Side


class ConditionFactory(object):

    @staticmethod
    def create_cross(symbols: List[str], side: Side, col1: str, col2: str) -> Tuple[Strategy, List[AbstractIndicator]]:
        conditions = []
        for symbol in symbols:
            ## buy when,
            conditions.append(
                Condition(
                    settings=EntrySettings(
                        symbol=symbol,
                        side=side,
                        quantity=1,
                        stopLoss=None
                    ),
                    rules=[
                        SingleRule(
                            PandasColumnRuleValue(col1),
                            LogicalOperator.LessThan,
                            PandasColumnRuleValue(col2),
                            time_step=-2,
                        ),
                        SingleRule(
                            PandasColumnRuleValue(col1),
                            LogicalOperator.GreaterThan,
                            PandasColumnRuleValue(col2),
                            time_step=-1,
                        ),
                    ]
                )
            )

        return conditions

    @staticmethod
    def create_threshold_met(symbols: List[str], side: Side, col1: str, operator: LogicalOperator, col2: str) -> Tuple[Strategy, List[AbstractIndicator]]:
        conditions = []
        for symbol in symbols:
            ## buy when,
            conditions.append(
                Condition(
                    settings=EntrySettings(
                        symbol=symbol,
                        side=side,
                        quantity=1,
                        stopLoss=None
                    ),
                    rules=[
                        SingleRule(
                            PandasColumnRuleValue(col1),
                            operator,
                            PandasColumnRuleValue(col2),
                            time_step=-1,
                        ),
                    ]
                )
            )

        return conditions
