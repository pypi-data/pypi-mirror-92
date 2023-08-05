from typing import List
from . import StockPrice


class Pitch(object):
    """ Data to pass to the Pitch Engine """
    def __init__(self, prices: List[StockPrice]) -> None:
        self.prices = prices
