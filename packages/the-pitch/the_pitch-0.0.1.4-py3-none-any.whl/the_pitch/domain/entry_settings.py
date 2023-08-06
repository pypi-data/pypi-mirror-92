from typing import Optional
from .order_target import OrderTarget
from .enums import AssetType, Side


class EntrySettings(object):
    def __init__(self,
                symbol: str,
                side: Side,
                quantity: int = 1,
                asset_type = AssetType.Equity,
                stopLoss: Optional[OrderTarget] = None):
        self.symbol = symbol
        self.side = side
        self.quantity = quantity
        self.asset_type = asset_type
        self.stopLoss = stopLoss
