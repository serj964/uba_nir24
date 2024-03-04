
from sklearn.ensemble import IsolationForest
import clickhouse_driver
import pandas as pd
import numpy as np

from app import config

SELECT_PREVIOUS_QUERY = 'SELECT * FROM test'
SELECT_LATEST_QUERY = 'SELECT * FROM test_2'


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


def _get_df(ch_client: clickhouse_driver.Client, query: str) -> pd.DataFrame:
    rows, columns_defs = ch_client.execute(query=query, with_column_types=True)

    columns = [column_name for column_name, _ in columns_defs]
    df = pd.DataFrame(rows, columns=columns)

    return df


def _isolation_forest(previous_samples: pd.DataFrame, new_samples: pd.DataFrame):
    previous_samples = previous_samples.to_numpy()
    new_samples = new_samples.to_numpy()

    clf = IsolationForest(random_state=0)
    clf.fit(previous_samples)

    anomaly_score = clf.score_samples(new_samples)

    return anomaly_score


def main():
    ch_client = _get_ch_client(
        config.CH_HOST,
        config.CH_PORT,
        config.CH_DATABASE,
        config.CH_USERNAME,
        config.CH_PASSWORD
    )

    previous_samples = _get_df(ch_client, SELECT_PREVIOUS_QUERY)
    new_samples = _get_df(ch_client, SELECT_LATEST_QUERY)

    anomaly_score = _isolation_forest(previous_samples, new_samples)

    print('analyzer_1 finished its work')


main()
