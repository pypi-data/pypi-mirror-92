from collections import defaultdict
from typing import DefaultDict, List
from ..domain import Portfolio, Position, Side
from ..logging import AbstractLogger


class PortfolioManager(object):
    def __init__(self, portfolio: Portfolio = Portfolio(), logger: AbstractLogger = None):
        self.portfolio = portfolio
        self.strategy_operations: defaultdict[str, DefaultDict[str, List[Position]]] = defaultdict(lambda: defaultdict(list))
        self.logger = logger

    def pre(self, **kwargs) -> None:
        self.portfolio.reload()

    def process(self, positions: List[Position], **kwargs) -> None:
        for position in positions:
            self.strategy_operations[position.strategy_id][position.symbol].append(position)

        return positions

    def post(self) -> None:
        self.portfolio.cache()

    def run(self, positions: List[Position], **kwargs) -> List[Position]:
        self.pre()
        self.process(positions)
        self.post()

        if len(positions) > 0 and self.logger is not None:
            self.logger.write('Positions...')
            for position in positions:
                self.logger.write(f'{position.strategy_id}: {position.symbol} @ {position.purchase_price} w/ {position.action.name}')

        return positions

class PlayMoneyPortfolioManager(PortfolioManager):
    def process(self, positions: List[Position], **kwargs):
        ## execuate fake trades
        self.portfolio.add_positions([ position for position in positions if position.action == Side.Buy ])
        self.portfolio.remove_positions([ position for position in positions if position.action == Side.Sell ])

        super().process(positions)
