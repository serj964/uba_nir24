import clickhouse_driver
import pandas as pd

from app.config import Config


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


CH_CLIENT = _get_ch_client(
    Config.CH_HOST,
    Config.CH_PORT,
    Config.CH_DATABASE,
    Config.CH_USERNAME,
    Config.CH_PASSWORD
)
