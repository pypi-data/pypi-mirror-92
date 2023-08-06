
import pandas as pd
from .abstract_indicator import AbstractIndicator
from ..converters import utils


class ROC(AbstractIndicator):
    def __init__(self, column: str = 'close', period: int = 20):
        super().__init__(f'roc_{column}_{period}')

        self.column = column
        self.period = period

    def compute(self, frame: pd.DataFrame, **kwargs) -> pd.DataFrame:
        frame[self.name] = frame[self.column].transform(
            lambda x: x.pct_change(periods=self.period)
        ).map(utils.decimal_from_float)

        return frame
