
import os

CH_HOST = os.getenv('CH_HOST', 'localhost')
CH_PORT = int(os.getenv('CH_PORT', '9000'))
CH_DATABASE = os.getenv('CH_DATABASE', 'default')
CH_USERNAME = os.getenv('CH_USERNAME', 'user')
CH_PASSWORD = os.getenv('CH_PASSWORD', 'password')

RMQ_HOST = os.getenv('RMQ_HOST', 'localhost')
RMQ_PORT = int(os.getenv('RMQ_PORT', '5672'))
RMQ_VHOST = os.getenv('RMQ_VHOST', '')
RMQ_USERNAME = os.getenv('RMQ_USERNAME', 'user')
RMQ_PASSWORD = os.getenv('RMQ_PASSWORD', 'password')
