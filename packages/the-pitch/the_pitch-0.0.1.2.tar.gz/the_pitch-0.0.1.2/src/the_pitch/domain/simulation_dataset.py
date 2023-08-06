from typing import List, Dict
from datetime import datetime
from . import StockPrice


class SimulationDataset(object):
    def __init__(self, data: List[StockPrice], test_data: Dict[datetime, List[StockPrice]]) -> None:
        self.data = data
        self.test_data = test_data
