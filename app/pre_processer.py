
import functools
import json

import pandas as pd
from config import QUEUE_ARGS, Config

from app.externals.clickhouse import send_feature_to_analyzer
from app.externals.rabbit import create_rmq_connection, declare_queue
from app.features import device_1, file_1, logon_1
from app.features.utils import merge_and_save_features

USED_FEATURES = [logon_1, device_1, file_1]


def handler_json_body_wrapper(func):
    @functools.wraps(func)
    def _handler(ch, method, properties, body):
        _body = json.loads(body.decode('utf-8'))
        res = func(_body)

        ch.basic_ack(delivery_tag=method.delivery_tag)
        return res

    return _handler


def prepare_df(instance_data):
    new_logs = pd.DataFrame(instance_data)

    previous_features_merged = None
    new_features_merged = None
    for feature in USED_FEATURES:
        previous_feature, new_feature = feature(new_logs)
        previous_features_merged = merge_and_save_features(previous_feature, previous_features_merged)
        new_features_merged = merge_and_save_features(new_feature, new_features_merged)

    previous_features_merged = previous_features_merged.sort_values(by=['user', 'date']).reset_index(drop=True)
    send_feature_to_analyzer(previous_features_merged, 'previous')

    new_features_merged = new_features_merged.sort_values(by=['user', 'date']).reset_index(drop=True)
    send_feature_to_analyzer(new_features_merged, 'new')
    #print(previous_features_merged[(previous_features_merged['mean_dev'] != 0) | (previous_features_merged['mean_dev_x'] != 0) | (previous_features_merged['mean_dev_y'] != 0)])
    #print(new_features_merged[(new_features_merged['mean_dev'] != 0) | (new_features_merged['mean_dev_x'] != 0) | (new_features_merged['mean_dev_y'] != 0)])
    print(previous_features_merged)
    print(new_features_merged)


def consume(exchange, queue_name):
    rmq_connection = create_rmq_connection()
    channel = rmq_connection.channel()
    channel.basic_qos(prefetch_count=1)

    channel = declare_queue(channel, exchange, queue_name, QUEUE_ARGS)

    handler = handler_json_body_wrapper(prepare_df)

    channel.basic_consume(queue=queue_name, on_message_callback=handler)

    try:
        print('start consuming')
        channel.start_consuming()
    except KeyboardInterrupt:
        print('end consuming')
        channel.stop_consuming()

    rmq_connection.close()


def main():
    consume(Config.RMQ_EXCHANGE, Config.RMQ_QUEUE)

    print('msg get')


main()
