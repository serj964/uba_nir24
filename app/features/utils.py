
import warnings
from typing import Tuple

import pandas as pd

from app.features.consts import MEAN, SUM

warnings.filterwarnings('ignore')


def enrich_logs_df(df: pd.DataFrame, features: str) -> pd.DataFrame:
    """

    """
    df = df[df['type'] == features]

    df['date'] = pd.to_datetime(df['datetime']).dt.date
    df['nday'] = pd.to_datetime(df['date']).dt.day_of_week
    df['is_weekend'] = df['nday'].apply(lambda x: 1 if x in [5, 6] else 0)

    df['date'] = df['date'].astype(str)

    return df


def calculate_new_logs_num(new_logs: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame({'number_of_logs': new_logs.groupby(['user', 'is_weekend', 'date']).size()}).reset_index()


def _generate_feature(
    logs_num: pd.DataFrame,
    logs_sum: pd.DataFrame,
    logs_mean: pd.DataFrame,
    feature_name: str
) -> pd.DataFrame:
    feature = pd.merge(logs_num, logs_sum, on=["user", 'is_weekend'])
    feature = pd.merge(feature, logs_mean, on=["user", 'is_weekend'])

    feature['freq'] = feature['number_of_logs'].to_numpy() / feature[SUM].to_numpy()
    feature['mean_freq'] = feature[MEAN].to_numpy() / feature[SUM].to_numpy()

    feature['mean_dev'] = feature['freq'] - feature['mean_freq']
    feature['mean_dev'] = feature['mean_dev'].apply(lambda x: x if x > 0 else 0)

    feature = feature[['user', 'is_weekend', 'date', 'mean_dev']]
    feature = feature.rename(columns={'mean_dev': feature_name})

    return feature


def generate_feature(
        previous_logs_num: pd.DataFrame,
        new_logs_num: pd.DataFrame,
        feature_name: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """

    """
    # TODO добавить условие, что юзеры у которых меньше n дней работы в компании, не учитываются

    previous_logs_num['number_of_logs'] = previous_logs_num['number_of_logs'].astype(int)
    previous_logs_num['is_weekend'] = previous_logs_num['is_weekend'].astype(int)

    # самое важное - если посчитать all_dl2, то считается всё
    #all_dl2 = pd.concat([previous_dl2, dl2]).reset_index(drop=True)

    previous_logs_mean = pd.DataFrame(
        {MEAN: previous_logs_num.groupby(['user', 'is_weekend'])['number_of_logs'].agg(MEAN)}
    ).reset_index()
    previous_logs_sum = pd.DataFrame(
        {SUM: previous_logs_num.groupby(['user', 'is_weekend'])['number_of_logs'].agg(SUM)}
    ).reset_index()

    previous_feature = _generate_feature(previous_logs_num, previous_logs_sum, previous_logs_mean, feature_name)
    new_feature = _generate_feature(new_logs_num, previous_logs_sum, previous_logs_mean, feature_name)

    return previous_feature, new_feature


def merge_and_save_features(first_df: pd.DataFrame, second_df: pd.DataFrame = None) -> pd.DataFrame:
    if second_df is None:
        second_df = pd.DataFrame({'user': [], 'is_weekend': [], 'date': []})

    return pd.merge(first_df, second_df, how='outer', on=['user', 'is_weekend', 'date']).fillna(0)
