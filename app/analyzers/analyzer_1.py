
import pandas as pd
from sklearn.ensemble import IsolationForest
from app.externals.clickhouse import send_anomaly_score, get_features


def _isolation_forest(previous_samples: pd.DataFrame, new_samples: pd.DataFrame):
    previous_samples_np = previous_samples[previous_samples.columns[3:]].to_numpy()
    new_samples_np = new_samples[new_samples.columns[3:]].to_numpy()

    clf = IsolationForest(random_state=0)
    clf.fit(previous_samples_np)

    anomaly_score = clf.score_samples(new_samples_np)

    anomaly_score_df = new_samples[['user', 'date']]
    anomaly_score_df['anomaly_score'] = [abs(score) for score in anomaly_score]

    return anomaly_score_df


def main():
    previous_samples = get_features('previous')
    new_samples = get_features('new')

    anomaly_score = _isolation_forest(previous_samples, new_samples)
    send_anomaly_score(anomaly_score)

    print(anomaly_score)
    print(anomaly_score.shape[0])

    print('analyzer_1 finished its work')


main()
