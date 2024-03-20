
import pandas as pd

from .utils import enrich_logs_df, generate_all_logs_df, get_previous_logs, send_logs

FEATURES = 'file'


def file_1(new_logs: pd.DataFrame) -> pd.DataFrame:
    """
    описание фичи:


    """
    feature_name = 'file_1'

    # загрузка логов
    previous_logs = get_previous_logs(feature_name)
    new_logs = enrich_logs_df(new_logs, FEATURES)

    # условие

    # вычисления и выгрузка логов
    all_logs, new_logs_to_send = generate_all_logs_df(previous_logs, new_logs)
    # send_logs(all_logs)

    return all_logs
    # return new_logs_to_send
