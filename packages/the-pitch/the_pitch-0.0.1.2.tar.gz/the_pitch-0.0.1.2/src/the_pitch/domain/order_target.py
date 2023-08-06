from .enums import Unit
from decimal import Decimal


class OrderTarget(object):
    def __init__(self, unit: Unit, value: Decimal):
        self.unit = unit
        self.value = value

class StopLossAtPrice(OrderTarget):
    def __init__(self, value: Decimal):
        super().__init__(Unit.Price, value)
