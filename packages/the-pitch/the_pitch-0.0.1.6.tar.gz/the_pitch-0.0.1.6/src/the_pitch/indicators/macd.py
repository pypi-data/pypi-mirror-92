import pandas as pd
from .abstract_indicator import AbstractIndicator
from ..converters import utils


class MACD(AbstractIndicator):
    def __init__(self, column: str = 'close', fast_period: int = 12, slow_period: int = 26, signal: int = 9):
        super().__init__(f'mcad_{column}_{fast_period}_{slow_period}_{signal}')

        self.column = column
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.signal = signal

    def compute(self, df: pd.DataFrame, **kwargs) -> pd.DataFrame:
        # Calculate the Fast Moving MACD.
        df['macd_fast'] = df[self.column].transform(
            lambda x: x.ewm(span = self.fast_period, min_periods = self.fast_period).mean()
        ).map(utils.decimal_from_float)

        # Calculate the Slow Moving MACD.
        df['macd_slow'] = df[self.column].transform(
            lambda x: x.ewm(span = self.slow_period, min_periods = self.slow_period).mean()
        ).map(utils.decimal_from_float)

        # Calculate the Line.
        df['macd_line'] = df['macd_fast'] - df['macd_slow']

        # Calculate the Signal.
        df['macd_signal'] = df['macd_line'].transform(
            lambda x: x.ewm(span = self.signal, min_periods = self.signal).mean()
        )

        # Calculate the Histogram
        df['macd_hist'] = df['macd_line'] - df['macd_signal']

        # Clean up before sending back.
        df.drop(
            labels=['macd_fast', 'macd_slow'],
            axis=1,
            inplace=True
        )

        return df
