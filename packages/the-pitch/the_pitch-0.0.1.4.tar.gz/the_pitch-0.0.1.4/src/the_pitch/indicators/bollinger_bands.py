import pandas as pd
import pandas_ta as ta
from .abstract_indicator import AbstractIndicator


class BollingerBands(AbstractIndicator):
    def __init__(self, column: str = 'close', period: int = 20):
        super().__init__(f'bb_{column}_{period}')

        self.column = column
        self.period = period

    def compute(self, df: pd.DataFrame, **kwargs) -> pd.DataFrame:
        columns = [
          f'bbl_{self.column}_{self.period}'
          f'bbm_{self.column}_{self.period}'
          f'bbu_{self.column}_{self.period}'
        ]

        df[columns] = (
            df.ta.bbands(self.column, length=self.period)
        )

        return df
