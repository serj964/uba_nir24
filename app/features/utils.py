
import warnings
from typing import Tuple

import pandas as pd

from app.externals.clickhouse import CH_CLIENT, get_df, insert_df
from app.features.consts import MEAN, SUM

warnings.filterwarnings('ignore')

SELECT_PREVIOUS_LOGS_QUERY = "SELECT user, is_weekend, date, number_of_logs FROM logs where feature = '{}'"
INSERT_LOGS_QUERY = 'INSERT INTO logs VALUES'


def enrich_logs_df(df: pd.DataFrame, features: str) -> pd.DataFrame:
    """

    """
    df = df[df['type'] == features]

    df['date'] = pd.to_datetime(df['datetime']).dt.date
    df['nday'] = pd.to_datetime(df['date']).dt.day_of_week
    df['is_weekend'] = df['nday'].apply(lambda x: 1 if x in [5, 6] else 0)

    df['date'] = df['date'].astype(str)

    return df


def generate_all_logs_df(previous_logs: pd.DataFrame, new_logs: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """

    """
    previous_dl2 = previous_logs[['user', 'is_weekend', 'date', 'number_of_logs']]
    previous_dl2['number_of_logs'] = previous_dl2['number_of_logs'].astype(int)

    dl2 = pd.DataFrame({'number_of_logs': new_logs.groupby(['user', 'is_weekend', 'date']).size()}).reset_index()

    # самое важное - если посчитать all_dl2, то считается всё
    all_dl2 = pd.concat([previous_dl2, dl2]).reset_index(drop=True)

    all_dl3 = pd.DataFrame({MEAN: all_dl2.groupby(['user', 'is_weekend'])['number_of_logs'].agg(MEAN)}).reset_index()
    all_dl4 = pd.DataFrame({SUM: all_dl2.groupby(['user', 'is_weekend'])['number_of_logs'].agg(SUM)}).reset_index()

    feature = pd.merge(all_dl2, all_dl4, on=["user", 'is_weekend'])
    feature = pd.merge(feature, all_dl3, on=["user", 'is_weekend'])

    feature['freq'] = feature['number_of_logs'].to_numpy() / feature[SUM].to_numpy()
    feature['mean_freq'] = feature[MEAN].to_numpy() / feature[SUM].to_numpy()

    feature['mean_dev'] = feature['freq'] - feature['mean_freq']
    feature['mean_dev'] = feature['mean_dev'].apply(lambda x: x if x > 0 else 0)

    # return feature, dl2
    return feature[['user', 'is_weekend', 'date', 'mean_dev']], dl2


def get_previous_logs(features: str) -> pd.DataFrame:
    return get_df(CH_CLIENT, SELECT_PREVIOUS_LOGS_QUERY.format(features))


def send_logs(logs_to_send: pd.DataFrame) -> None:
    insert_df(CH_CLIENT, INSERT_LOGS_QUERY, logs_to_send)


def merge_and_save_features(first_df: pd.DataFrame, second_df: pd.DataFrame = None) -> pd.DataFrame:
    if second_df is None:
        second_df = pd.DataFrame({'user': [], 'is_weekend': [], 'date': []})

    return pd.merge(first_df, second_df, how='outer', on=['user', 'is_weekend', 'date'])
