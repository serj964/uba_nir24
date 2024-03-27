import clickhouse_driver
import pandas as pd

from app.config import Config
from app.sql_scripts import (
    create_analyzer_table,
    drop_analyzer_table,
    insert_anomaly_score,
    insert_df_into_analyzer,
    insert_df_into_logs,
    select_features,
    select_previous_logs
)


def _get_ch_client(host: str, port: int, database: str, username: str, password: str) -> clickhouse_driver.Client:
    ch_client = clickhouse_driver.Client(
        host=host,
        port=port,
        database=database,
        user=username,
        password=password,
        secure=False,
        verify=False,
        compression=False,
        settings={'use_numpy': True},
    )
    return ch_client


def get_df(ch_client: clickhouse_driver.Client, query: str) -> pd.DataFrame:
    rows, columns_defs = ch_client.execute(query=query, with_column_types=True)

    columns = [column_name for column_name, _ in columns_defs]
    df = pd.DataFrame(rows, columns=columns)

    return df


def insert_df(ch_client: clickhouse_driver.Client, query: str, df: pd.DataFrame) -> None:
    ch_client.insert_dataframe(
        query=query,
        dataframe=df,
        settings={'use_numpy': True, 'insert_block_size': 50000},
    )


def get_previous_logs(features: str) -> pd.DataFrame:
    return get_df(CH_CLIENT, select_previous_logs.format(features))


def send_logs_to_click(logs_to_send: pd.DataFrame, feature_name) -> None:
    logs_to_send['feature'] = feature_name
    insert_df(CH_CLIENT, insert_df_into_logs, logs_to_send)


def send_feature_to_analyzer(feature_to_send: pd.DataFrame, period: str) -> None:
    features = ''

    cols = feature_to_send.columns[3:]
    print(cols)
    for col in cols:
        features += ', {} Float32'.format(col)

    CH_CLIENT.execute(drop_analyzer_table.format(period))
    CH_CLIENT.execute(create_analyzer_table.format(period=period,features=features))
    insert_df(CH_CLIENT, insert_df_into_analyzer.format(period), feature_to_send)


def get_features(period: str) -> pd.DataFrame:
    return get_df(CH_CLIENT, select_features.format(period))


def send_anomaly_score(anomaly_score_to_send: pd.DataFrame) -> None:
    insert_df(CH_CLIENT, insert_anomaly_score, anomaly_score_to_send)


CH_CLIENT = _get_ch_client(
    Config.CH_HOST,
    Config.CH_PORT,
    Config.CH_DATABASE,
    Config.CH_USERNAME,
    Config.CH_PASSWORD
)
