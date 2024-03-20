
import pandas as pd

from .utils import enrich_logs_df, generate_all_logs_df, get_previous_logs, send_logs

FEATURES = 'device'


def device_1(new_logs: pd.DataFrame) -> pd.DataFrame:
    """
    описание фичи:


    """
    feature_name = 'device_1'

    # загрузка логов
    previous_logs = get_previous_logs(feature_name)
    new_logs = enrich_logs_df(new_logs, FEATURES)

    # условие
    new_logs = new_logs[new_logs.metadata.str.contains('"activity": "Connect"')].reset_index(drop=True)

    # вычисления и выгрузка логов
    all_logs, new_logs_to_send = generate_all_logs_df(previous_logs, new_logs)
    # send_logs(all_logs)

    return all_logs
    # return new_logs_to_send
