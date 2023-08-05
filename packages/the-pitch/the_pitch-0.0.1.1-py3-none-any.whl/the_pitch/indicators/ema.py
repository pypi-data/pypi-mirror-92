import pandas as pd
from .abstract_indicator import AbstractIndicator
from ..converters import utils


class EMA(AbstractIndicator):
    def __init__(self, column: str = 'close', period: int = 20):
        super().__init__(f'ema_{column}_{period}')

        self.column = column
        self.period = period

    def compute(self, df: pd.DataFrame, **kwargs) -> pd.DataFrame:
        df[self.name] = df[self.column].transform(
            lambda x: x.ewm(span=self.period).mean()
        ).map(utils.decimal_from_float)

        return df
