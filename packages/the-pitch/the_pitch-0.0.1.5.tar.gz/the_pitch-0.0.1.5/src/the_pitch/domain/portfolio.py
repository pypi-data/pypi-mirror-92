from collections import defaultdict
from typing import Dict, List
from . import Position
from ..caches import Cache
import json


class Portfolio(object):
    def __init__(self, cache_service: Cache = Cache()):
        self.active_positions: Dict[str, List[Position]] = defaultdict(list)
        self.cache_service = cache_service

    def add_positions(self, new_positions: List[Position]) -> None:
        for position in new_positions:
            self.active_positions[position.strategy_id].append(position)

    def remove_positions(self, old_positions: List[Position]) -> None:
        for position in old_positions:
            self.remove_position(position.strategy_id, position.symbol)

    def remove_position(self, strategy_id: str, symbol: str) -> None:
        if strategy_id in self.active_positions:
            self.active_positions[strategy_id] = list(filter(
              lambda p: p.symbol != symbol,
              self.active_positions[strategy_id],
            ))

    def get_positions_by_strategy(self, strategy_id: str) -> List[Position]:
        return self.active_positions[strategy_id]

    def get_positions(self, strategy_id: str, symbol: str) -> List[Position]:
        return list(filter(
          lambda p: p.symbol == symbol,
          self.get_positions_by_strategy(strategy_id)
        ))

    def cache(self):
        obj = {}
        for strategy_id, items in self.active_positions.items():
            obj[strategy_id] = [ item.to_obj() for item in items ]

        self.cache_service.write(obj)

    def reload(self):
        data = self.cache_service.read()

        self.active_positions = defaultdict(list)
        for strategy_id, items in data.items():
            self.active_positions[strategy_id] = [ Position.create(item) for item in items ]
