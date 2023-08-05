import pandas as pd
from typing import Optional, List, Dict
from . import Position


class StrategyPayload(object):
    def __init__(self, strategy_id: str, frame: pd.DataFrame, active_positions: Dict[str, Position] = {}) -> None:
        self.strategy_id = strategy_id
        self.frame = frame
        self.active_positions = active_positions

class ConditionPayload(object):
    def __init__(self, symbol: str, strategy_payload: StrategyPayload) -> None:
        self.symbol = symbol
        self.strategy_payload = strategy_payload

    @property
    def frame(self) -> pd.DataFrame:
        return self.strategy_payload.frame.loc[self.symbol]

    @property
    def active_positon(self) -> Optional[Position]:
        return self.strategy_payload.active_positions[self.symbol] if self.symbol in self.strategy_payload.active_positions else None

    @property
    def has_active_position(self) -> bool:
        return self.active_positon is not None
