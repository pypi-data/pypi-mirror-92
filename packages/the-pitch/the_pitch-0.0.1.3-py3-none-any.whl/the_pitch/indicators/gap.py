import pandas as pd
from .abstract_indicator import AbstractIndicator


class Gap(AbstractIndicator):
    def __init__(self):
        super().__init__(f'gap')

    def compute(self, df: pd.DataFrame, **kwargs) -> pd.DataFrame:
        df[self.name] = (df['open'] - df['close'].shift(1))
        return df
