from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime

from . import StockPrice


@dataclass
class SimulationDataset(object):
    data: List[StockPrice]
    test_data: Dict[datetime, List[StockPrice]]
