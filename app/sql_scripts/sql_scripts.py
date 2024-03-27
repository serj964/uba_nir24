create_analyzer_table = """
CREATE TABLE IF NOT EXISTS nir24.{period}_features
(
    `user` String, `is_weekend` Int32, `date` String{features}
)
ENGINE = MergeTree()
ORDER BY (user, date)
SETTINGS index_granularity = 8192;
"""
#, `logon_1` Float32, `device_1` Float32, `file_1` Float32

drop_analyzer_table = """
DROP TABLE IF EXISTS nir24.{}_features
"""

insert_df_into_logs = """
INSERT INTO logs VALUES
"""

insert_df_into_analyzer = """
INSERT INTO {}_features VALUES
"""

select_previous_logs = """
SELECT user, is_weekend, date, number_of_logs FROM logs where feature = '{}'
"""

select_features = """
SELECT * FROM {}_features
"""

insert_anomaly_score = """
INSERT INTO anomaly_score VALUES
"""
