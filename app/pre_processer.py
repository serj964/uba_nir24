
import functools
import json

import pandas as pd
from config import QUEUE_ARGS, Config
from externals.rabbit import create_rmq_connection, declare_queue
from features import device_1, file_1, logon_1
from features.utils import merge_and_save_features

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

    merged_df = None
    for feature in USED_FEATURES:
        feature = feature(new_logs)
        merged_df = merge_and_save_features(feature, merged_df)

    print(merged_df.head(10))
    print(merged_df.shape)
    # print(instance_data)


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
