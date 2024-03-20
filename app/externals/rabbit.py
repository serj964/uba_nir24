
import pika

from app.config import Config


def create_rmq_connection():
    conn_params = pika.URLParameters(
        'amqp://{user}:{pwd}@{host}:{port}/{vhost}'.format(
            host=Config.RMQ_HOST,
            port=Config.RMQ_PORT,
            user=Config.RMQ_USERNAME,
            pwd=Config.RMQ_PASSWORD,
            vhost=Config.RMQ_VHOST,
        )
    )

    return pika.BlockingConnection(conn_params)


def declare_queue(channel, exchange, queue_name, args):
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
