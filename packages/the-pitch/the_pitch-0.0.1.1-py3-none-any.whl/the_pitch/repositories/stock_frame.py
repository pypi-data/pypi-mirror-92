from typing import Dict, List
import pandas as pd
from ..indicators import AbstractIndicator
from ..domain import StockPrice, Condition, Strategy, Portfolio


class StockFrame():
    def __init__(self, prices: List[StockPrice], indicators: List[AbstractIndicator] = [], **kwargs) -> None:
        self.df = pd.DataFrame(data=[ price.to_obj() for price in prices ]).set_index(keys=StockPrice.index_columns())

        self.indicators = indicators
        self._refresh_indicators(**kwargs)

    def add_rows(self, prices: List[StockPrice], active_portfolio: Portfolio, **kwargs) -> None:
        columns = StockPrice.feature_columns()
        for price in prices:
            self.df.loc[price.index, columns] = price.to_list()

        self._refresh_indicators(**kwargs)

    def _refresh_indicators(self, **kwargs) -> None:
        self.df.sort_index(inplace=True)

        for indicator in self.indicators:
            self.df = indicator.compute(self.df, **kwargs)
