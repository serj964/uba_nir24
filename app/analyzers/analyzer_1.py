
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

from app.externals.clickhouse import CH_CLIENT, get_df

"""SELECT_PREVIOUS_QUERY = 'SELECT * FROM test'
SELECT_LATEST_QUERY = 'SELECT * FROM test_2'"""
SELECT_QUERY = 'SELECT * FROM test_2'


def _isolation_forest(previous_samples: pd.DataFrame, new_samples: pd.DataFrame):
    #previous_samples = previous_samples.to_numpy()
    #new_samples = new_samples.to_numpy()
    samples.to_numpy()

    clf = IsolationForest(random_state=0)
    #clf.fit(previous_samples)

    #anomaly_score = clf.score_samples(new_samples)

    #return anomaly_score
    return clf.fit_predict()


def main():
    """previous_samples = get_df(CH_CLIENT, SELECT_PREVIOUS_QUERY)
    new_samples = get_df(CH_CLIENT, SELECT_LATEST_QUERY)"""
    #samples = _isolation_forest(previous_samples, new_samples)

    #anomaly_score = _isolation_forest(previous_samples, new_samples)

    #print(anomaly_score)

    samples = get_df(CH_CLIENT, SELECT_QUERY)

    print('analyzer_1 finished its work')


main()
