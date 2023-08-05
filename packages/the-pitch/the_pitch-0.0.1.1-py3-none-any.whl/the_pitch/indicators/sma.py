import pandas as pd
from .abstract_indicator import AbstractIndicator
from ..converters import utils


class SMA(AbstractIndicator):
    def __init__(self, column: str = 'close', period: int = 20):
        super().__init__(f'sma_{column}_{period}')

        self.period = period
        self.column = column

    def compute(self, df: pd.DataFrame, **kwargs) -> pd.DataFrame:
        df[self.name] = df[self.column].transform(
            lambda x: x.rolling(window=self.period).mean()
        ).map(utils.decimal_from_float)

        return df
