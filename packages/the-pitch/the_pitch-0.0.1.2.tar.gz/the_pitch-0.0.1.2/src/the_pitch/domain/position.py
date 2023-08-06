from ..domain import Side
from . import AssetType
from decimal import Decimal
from datetime import date
from ..converters import utils
import pandas as pd


class Position(object):
    def __init__(self, strategy_id: str, symbol: str, asset_type: AssetType, quantity: int, purchase_price: Decimal, purchase_date: date, action: Side) -> None:
        self.strategy_id = strategy_id
        self.symbol = symbol
        self.asset_type = asset_type
        self.quantity = quantity
        self.purchase_price = purchase_price
        self.purchase_date = purchase_date
        self.action = action

    def to_obj(self) -> dict:
        return {
          'strategy_id': self.strategy_id,
          'symbol': self.symbol,
          'asset_type': self.asset_type.as_int(),
          'quantity': self.quantity,
          'purchase_price': str(self.purchase_price),
          'purchase_date': str(self.purchase_date),
          'action': self.action.as_int()
        }

    def __repr__(self) -> str:
        return f'Position("{self.strategy_id}", "{self.symbol}", AssetType({self.asset_type.as_int()}), {self.quantity}, {self.purchase_price}, {self.purchase_date}, Side({self.action.as_int()}))'

    @staticmethod
    def create(item: dict):
        return Position(
          item['strategy_id'],
          item['symbol'],
          AssetType(item['asset_type']),
          item['quantity'],
          utils.decimal_from_value(item['purchase_price']),
          pd.to_datetime(item['purchase_date']),
          Side(item['action'])
        )
