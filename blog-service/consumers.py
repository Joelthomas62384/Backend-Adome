
import os
import django



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

import pika 
import json
import logging
from  consume_utils import  user_callback , tenant_callback , tenantuser_callback



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
    print(f"blog : {data}")
    
    if contenttype == 'user':
        user_callback(ch , event_type , data , method)
        logging.info('user callback done')
    elif contenttype == 'tenant':
        tenant_callback(ch , event_type , data , method)
        logging.info('tenant callback done')
    elif contenttype == 'tenantuser':
        tenantuser_callback(ch , event_type , data , method)
        logging.info('tenantuser callback done')

    



channel.queue_declare('blog-service' , durable=True , )
channel.queue_bind('blog-service', 'appevents', 'app.*.*')
channel.basic_consume(queue='blog-service', on_message_callback=callback, auto_ack=False)



channel.start_consuming()
