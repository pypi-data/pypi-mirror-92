from typing import Dict, List, Tuple
import numpy as np
import pandas as pd
import pandas_datareader.data as web
from ..converters import utils
from ..domain import StockPrice, SimulationDataset


class Query(object):

    @staticmethod
    def get_pricing_data(source: str = 'yahoo', symbols: List[str] = [], start: str = '2000-01-01', end: str = '2021-01-01') -> pd.DataFrame:
        df_output = pd.DataFrame()
        for symbol in symbols:
            df_new = web.DataReader(symbol, source, start, end).reset_index()
            df_new = df_new.drop(columns=['Close'])
            df_new.columns = [
                'date',
                'high',
                'low',
                'open',
                'volume',
                'close'
            ]

            df_new['symbol'] = symbol
            df_new = df_new[['symbol', 'date', 'open', 'close', 'high', 'low', 'volume']]

            if df_output.empty:
                df_output = df_new
            else:
                df_output = pd.concat([df_output, df_new])

        return df_output

    @staticmethod
    def split(df: pd.DataFrame, split_date: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
        df_setup_data = pd.DataFrame()
        df_test_data = pd.DataFrame()
        group = df.set_index(['symbol', 'date'])
        symbols = np.unique(list(map(lambda x: x[0], group.index)))
        for symbol in symbols:
            dfs = group.loc[symbol][:pd.Timestamp(split_date)].reset_index()
            dfs['symbol'] = symbol
            if df_setup_data.empty:
                df_setup_data = dfs
            else:
                df_setup_data = pd.concat([df_setup_data, dfs])

            dft = group.loc[symbol][pd.Timestamp(split_date):].reset_index()
            dft['symbol'] = symbol
            if df_test_data.empty:
                df_test_data = dft
            else:
                df_test_data = pd.concat([df_test_data, dft])

        return (df_setup_data, df_test_data)

    @staticmethod
    def query_for_dataset(symbols: str, start: str = '2000-01-01', now: str = '2011-01-01', end: str = '2021-01-01') -> SimulationDataset:
        df = Query.get_pricing_data(symbols=symbols, start=start, end=end)
        dfs, dft = Query.split(df, now)

        data = StockPrice.create_many_from_dataframe(dfs)

        test_data: Dict[str, List[StockPrice]] = {}
        for row in StockPrice.create_many_from_dataframe(dft):
            key = row.created_at
            if key not in test_data:
                test_data[key] = []

            test_data[key].append(row)

        return SimulationDataset(data, test_data)

    @staticmethod
    def load_dataset(csv: str, now: str = '2011-01-01') -> SimulationDataset:
        df = pd.read_csv(csv, index_col=None, converters={ 'close': utils.decimal_from_value })
        df.date = pd.to_datetime(df.date)

        dfs, dft = Query.split(df, now)

        data = StockPrice.create_many_from_dataframe(dfs)

        test_data: Dict[str, List[StockPrice]] = {}
        for row in StockPrice.create_many_from_dataframe(dft):
            key = row.created_at
            if key not in test_data:
                test_data[key] = []

            test_data[key].append(row)

        return SimulationDataset(data, test_data)
