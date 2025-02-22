import pika 
import json
import logging
from . consume_utils import  tenant_callback



connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        'rabbitmq',
        5672,
        '/',
        credentials=pika.PlainCredentials('root', 'root')
    )
)
channel = connection.channel()
channel.exchange_declare(exchange='appevents', exchange_type='topic', durable=True)


def callback(ch, method, properties, body):
    routing_key = method.routing_key
    contenttype = routing_key.split('.')[1]
    event_type = routing_key.split('.')[-1]
    data = json.loads(body)
   

    if contenttype == 'tenant':
        tenant_callback(ch , event_type , data , method)
        logging.info('tenant callback done')



channel.queue_declare('user-service' , durable=True , )
channel.queue_bind('user-service', 'appevents', 'app.*.*')
channel.basic_consume(queue='user-service', on_message_callback=callback, auto_ack=False)



