from datetime import datetime
from decimal import Decimal
from typing import List, Tuple
import pandas as pd
from ..converters import utils


class StockPrice(object):
    def __init__(self, symbol: str, created_at: datetime, open: Decimal, close: Decimal, high: Decimal, low: Decimal, volume: int):
        self.symbol = symbol
        self.created_at = created_at
        self.open = open
        self.close = close
        self.high = high
        self.low = low
        self.volume = volume

    @property
    def index(self) -> Tuple[str, datetime]:
        return (self.symbol, self.created_at)

    @staticmethod
    def index_columns():
        return ['symbol', 'datetime']

    @staticmethod
    def feature_columns():
        return [ 'open', 'close', 'high', 'low', 'volume' ]

    def to_obj(self) -> dict:
        return {
          'symbol': self.symbol,
          'datetime': self.created_at,
          'open': self.open,
          'close': self.close,
          'high': self.high,
          'low': self.low,
          'volume': self.volume,
        }

    def to_list(self, include_indexes: bool = False) -> list:
        if include_indexes:
            return [ self.symbol, self.created_at, self.open, self.close, self.high, self.low, self.volume ]

        return [ self.open, self.close, self.high, self.low, self.volume ]

    @staticmethod
    def create_many_from_dataframe(df: pd.DataFrame):
        prices = []
        for _, row in df.iterrows():
            prices.append(
                StockPrice(
                    row['symbol'],
                    row['date'],
                    utils.decimal_from_float(row['open']),
                    utils.decimal_from_float(row['close']),
                    utils.decimal_from_float(row['high']),
                    utils.decimal_from_float(row['low']),
                    int(row['volume'])
                )
            )

        return prices

    @staticmethod
    def create_many_from_objects(objects: List[dict]):
        prices = []
        for object in objects:
            prices.append(
                StockPrice(
                    object['symbol'],
                    object['date'],
                    utils.decimal_from_float(object['open']),
                    utils.decimal_from_float(object['close']),
                    utils.decimal_from_float(object['high']),
                    utils.decimal_from_float(object['low']),
                    int(object['volume'])
                )
            )

        return prices
