from decimal import Decimal
from typing import List, Tuple
from ..indicators import SMA, PercentLess, PercentMore, AbstractIndicator
from ..domain import Strategy, Side, LogicalOperator
from ..conditions import ConditionFactory


class StrategyFactory(object):

    @staticmethod
    def create_sma_cross_price(id: str, symbols: List[str], period1: int) -> Tuple[Strategy, List[AbstractIndicator]]:
        sma_1 = SMA('close', period1)

        conditions = []
        conditions.extend(ConditionFactory.create_cross(symbols, Side.Buy, 'close', sma_1.name))
        conditions.extend(ConditionFactory.create_cross(symbols, Side.Sell, sma_1.name, 'close'))

        strategy = Strategy(
            id,
            description='Buy: close goes above SMA\nSell: close goes below SMA',
            conditions=conditions
        )

        return (strategy, [ sma_1 ])

    @staticmethod
    def create_price_revert_to_sma(id: str, symbols: List[str], period1: int, pl: Decimal = Decimal('0.10'), pm: Decimal = Decimal('0.10')) -> Tuple[Strategy, List[AbstractIndicator]]:
        sma_1 = SMA('close', period1)
        pl = PercentLess(sma_1.name, pl)
        pm = PercentMore(sma_1.name, pm)

        conditions = []
        conditions.extend(ConditionFactory.create_threshold_met(symbols, Side.Buy, 'close', LogicalOperator.LessThanOrEqual, pl.name))
        conditions.extend(ConditionFactory.create_threshold_met(symbols, Side.Sell, 'close', LogicalOperator.GreaterThanOrEqual, pm.name))

        strategy = Strategy(
            id,
            description='Buy: close goes above SMA - 10% \nSell: close goes below SMA + 10%',
            conditions=conditions
        )

        return (strategy, [ sma_1, pl, pm ])

    @staticmethod
    def create_sma_cross_sma(id: str, symbols: List[str], period1: int, period2: int, ) -> Tuple[Strategy, List[AbstractIndicator]]:
        sma_1 = SMA('close', period1)
        sma_2 = SMA('close', period2)

        conditions = []
        conditions.extend(ConditionFactory.create_cross(symbols, Side.Buy, sma_1.name, sma_2.name))
        conditions.extend(ConditionFactory.create_cross(symbols, Side.Sell, sma_2.name, sma_1.name))

        strategy = Strategy(
            id,
            description='Buy: SMA 1 goes above SMA 2\nSell: SMA 1 goes below SMA 2',
            conditions=conditions
        )

        return (strategy, [ sma_1, sma_2 ])
