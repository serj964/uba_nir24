create_analyzer_table = """
CREATE TABLE IF NOT EXISTS nir24.{}_analyzer
(
    `user` String,
    `is_weekend` Int32,
    `date` String,
    `logon_1` Float32,
    `device_1` Float32,
    `file_1` Float32
)
ENGINE = MergeTree()
ORDER BY (user, date)
SETTINGS index_granularity = 8192;
"""

drop_analyzer_table = """
DROP TABLE IF EXISTS nir24.{}_analyzer
"""

insert_df_into_logs = """
INSERT INTO logs VALUES
"""

insert_df_into_analyzer = """
INSERT INTO {}_analyzer VALUES
"""

select_previous_logs = """
SELECT user, is_weekend, date, number_of_logs FROM logs where feature = '{}'
"""
