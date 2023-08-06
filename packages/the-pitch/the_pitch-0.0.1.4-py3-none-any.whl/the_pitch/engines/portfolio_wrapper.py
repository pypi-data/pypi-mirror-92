from typing import List

from ..repositories import StockFrame
from ..engines import PitchEngine
from ..domain import Strategy, Position, Pitch
from ..managers import PortfolioManager


class PortfolioWrapper(object):
    def __init__(self, stock_frame: StockFrame, strategies: List[Strategy], portfolio_manager: PortfolioManager):
        self.engine = PitchEngine(
            stock_frame=stock_frame,
            strategies=strategies
        )

        self.portfolio_manager = portfolio_manager

    def run(self, pitch: Pitch) -> List[Position]:
        return self.portfolio_manager.run(
            self.engine.run(pitch, self.portfolio_manager.portfolio)
        )
