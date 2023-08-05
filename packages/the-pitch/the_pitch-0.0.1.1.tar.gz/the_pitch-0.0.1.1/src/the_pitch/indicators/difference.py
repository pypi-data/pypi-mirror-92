import pandas as pd
from .abstract_indicator import AbstractIndicator
from ..converters import utils


class Difference(AbstractIndicator):
    def __init__(self, column: str = 'close', period: int = 9):
        super().__init__(f'diff_{column}_{period}')

        self.column = column
        self.period = period

    def compute(self, df: pd.DataFrame, **kwargs) -> pd.DataFrame:
        df[self.name] = df[self.column].transform(
            lambda x: round(x.diff(periods=self.period), 2)
        ).map(utils.decimal_from_float)

        return df
