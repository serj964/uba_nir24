
from typing import Tuple

import pandas as pd

from app.externals.clickhouse import get_previous_logs, send_logs_to_click

from .utils import calculate_new_logs_num, enrich_logs_df, generate_feature

FEATURES = 'file'


def file_1(new_logs: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    описание фичи:


    """
    feature_name = 'file_1'

    # загрузка логов
    previous_logs_num = get_previous_logs(feature_name)
    new_logs = enrich_logs_df(new_logs, FEATURES)

    # условие

    # вычисления и выгрузка логов
    new_logs_num = calculate_new_logs_num(new_logs)
    send_logs_to_click(new_logs_num, feature_name)
    previous_feature, new_feature = generate_feature(previous_logs_num, new_logs_num, feature_name)

    return previous_feature, new_feature
