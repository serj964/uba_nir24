
import pika
import pandas as pd
import json
import sys

from app import config

QUEUE_ARGS = {
    # 'x-max-priority': 1,
    'x-message-deduplication': True,
    'x-queue-mode': 'lazy',
}


def open_channel(exchange, queue_name, args):
    conn_params = pika.URLParameters(
        'amqp://{user}:{pwd}@{host}:{port}/{vhost}'.format(
            host=config.RMQ_HOST,
            port=config.RMQ_PORT,
            user=config.RMQ_USERNAME,
            pwd=config.RMQ_PASSWORD,
            vhost=config.RMQ_VHOST,
        )
    )

    connection = pika.BlockingConnection(conn_params)
    channel = connection.channel()

    channel.exchange_declare(
        exchange=exchange,
        durable=True,
    )
    channel.queue_declare(
        queue=queue_name,
        durable=True,
        arguments=args or {}
    )
    channel.queue_bind(
        queue=queue_name,
        exchange=exchange,
        routing_key=queue_name,
    )

    return channel


def publish_msg(exchange, queue_name, body):
    channel = open_channel(exchange, queue_name, QUEUE_ARGS)

    channel.basic_publish(
        exchange=exchange,
        routing_key=queue_name,
        body=body,
    )


def read_logs(start_datetime, end_datetime):
    all_logs = pd.read_csv('./logon+device+file_order_by_datetime.csv')
    current_logs_dict = all_logs[(all_logs.datetime >= start_datetime) & (all_logs.datetime < end_datetime)].to_dict()

    return json.dumps(current_logs_dict, default=str, ensure_ascii=False)


def main():
    start_datetime = '2010-01-01'
    end_datetime = '2011-06-01'

    for arg in sys.argv[1:]:
        if 'start_datetime' in arg:
            start_datetime = arg[arg.find('=')+1:]
        if 'end_datetime' in arg:
            end_datetime = arg[arg.find('=') + 1:]

    publish_msg(
        exchange='instance_exchange',
        queue_name='instance_queue',
        body=read_logs(start_datetime, end_datetime)
    )

    print('msg sent')


main()
