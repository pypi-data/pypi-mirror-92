import pandas as pd
from .abstract_indicator import AbstractIndicator


class ATR(AbstractIndicator):
    def __init__(self, period: int):
        """ Calculates the Average True Range (ATR). """
        super().__init__(f'atr_{period}')

        self.period = period

    def compute(self, df: pd.DataFrame, **kwargs) -> pd.DataFrame:
        # Calculate the different parts of True Range.
        df['true_range_0'] =  abs(df['high'] - df['low'])
        df['true_range_1'] =  abs(df['high'] - df['close'].shift())
        df['true_range_2'] = abs(df['low'] - df['close'].shift())

        # Grab the Max.
        df['true_range'] = df[['true_range_0', 'true_range_1', 'true_range_2']].max(axis=1)

        # Calculate the Average True Range.
        df[self.name] = df['true_range'].transform(
            lambda x: x.ewm(span = self.period, min_periods = self.period).mean()
        )

        # Clean up before sending back.
        df.drop(
            labels=['true_range_0', 'true_range_1', 'true_range_2', 'true_range'],
            axis=1,
            inplace=True
        )

        return df
