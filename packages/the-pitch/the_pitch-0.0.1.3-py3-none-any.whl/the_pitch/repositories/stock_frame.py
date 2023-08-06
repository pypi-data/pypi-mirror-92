from typing import List, Optional
import pandas as pd
from pandas.core.groupby import DataFrameGroupBy
from ..indicators import AbstractIndicator
from ..domain import StockPrice, Portfolio


class StockFrame():
    def __init__(self, prices: List[StockPrice], indicators: List[AbstractIndicator] = [], cache_path: Optional[str] = None, **kwargs) -> None:
        self.df = pd.DataFrame(data=[ price.to_obj() for price in prices ]).set_index(keys=StockPrice.index_columns())
        self.cache_path = cache_path

        self.indicators = indicators
        self._refresh_indicators(**kwargs)

    @property
    def symbol_groups(self) -> DataFrameGroupBy:
        return self.df.groupby(by='symbol', as_index=False, sort=True)

    def add_rows(self, prices: List[StockPrice], active_portfolio: Portfolio, **kwargs) -> None:
        columns = StockPrice.feature_columns()
        for price in prices:
            self.df.loc[price.index, columns] = price.to_list()

        self._refresh_indicators(active_portfolio=active_portfolio, **kwargs)

    def _refresh_indicators(self, **kwargs) -> None:
        self.df.sort_index(inplace=True)

        for indicator in self.indicators:
            self.df = indicator.compute(self.df, **kwargs)

        self._cache()

    def _cache(self):
        if self.cache_path is None:
            return

        self.df.to_csv(self.cache_path)
