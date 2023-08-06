import pandas as pd
import numpy as np
from .abstract_indicator import AbstractIndicator
from ..converters import utils


class RSI(AbstractIndicator):
    def __init__(self, period: int = 20):
        super().__init__(f'rsi_{period}')

        self.period = period

    def compute(self, df: pd.DataFrame, **kwargs) -> pd.DataFrame:
        if 'diff_close_1' not in df.columns:
            raise ValueError('missing "diff_close_1" column')

        # Define the up days.
        df['up_day'] = df['diff_close_1'].transform(
            lambda x : np.where(x >= 0, x, 0)
        )

        # Define the down days.
        df['down_day'] = df['diff_close_1'].transform(
            lambda x : np.where(x < 0, x.abs(), 0)
        )

        # Calculate the EWMA for the Up days.
        df['ewma_up'] = df['up_day'].transform(
            lambda x: x.ewm(span = self.period).mean()
        ).map(utils.decimal_from_float)

        # Calculate the EWMA for the Down days.
        df['ewma_down'] = df['down_day'].transform(
            lambda x: x.ewm(span = self.period).mean()
        ).map(utils.decimal_from_float)

        # Calculate the Relative Strength
        relative_strength = (df['ewma_up'] / df['ewma_down'])

        # Calculate the Relative Strength Index
        relative_strength_index = 100.0 - (100.0 / (1.0 + relative_strength))

        # Add the info to the data frame.
        df[self.name] = np.where(relative_strength_index == 0, 100, 100 - (100 / (1 + relative_strength_index)))

        # Clean up before sending back.
        df.drop(
            labels=['ewma_up', 'ewma_down', 'down_day', 'up_day', 'change_in_price'],
            axis=1,
            inplace=True
        )

        return df
