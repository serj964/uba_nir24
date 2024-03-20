import json
import sys

import pandas as pd
from config import QUEUE_ARGS, Config

from app.externals.rabbit import create_rmq_connection, declare_queue


def publish_msg(exchange, queue_name, body):
    rmq_connection = create_rmq_connection()
    channel = rmq_connection.channel()

    channel = declare_queue(channel, exchange, queue_name, QUEUE_ARGS)

    channel.basic_publish(
        exchange=exchange,
        routing_key=queue_name,
        body=body,
    )


def read_logs(start_datetime, end_datetime):
    all_logs = pd.read_csv('./logon+device+file_order_by_datetime.csv')
    current_logs_dict = all_logs[(all_logs.datetime >= start_datetime) & (all_logs.datetime < end_datetime)].to_dict()

    return json.dumps(current_logs_dict, default=str, ensure_ascii=False)
    # return json.dumps({1: 1})


def main():
    start_datetime = '2010-01-01'
    end_datetime = '2011-06-01'

    for arg in sys.argv[1:]:
        if 'start_datetime' in arg:
            start_datetime = arg[arg.find('=')+1:]
        if 'end_datetime' in arg:
            end_datetime = arg[arg.find('=') + 1:]

    publish_msg(
        exchange=Config.RMQ_EXCHANGE,
        queue_name=Config.RMQ_QUEUE,
        body=read_logs(start_datetime, end_datetime)
    )

    print('msg sent')


main()
