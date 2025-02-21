import pika
import json



def Publisher(data, contenttype , event_type):
    try:
        connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            'rabbitmq',
            5672,
            '/',
            pika.PlainCredentials('root', 'root')
        )
    )
        channel = connection.channel()
        channel.exchange_declare(exchange='appevents', exchange_type='topic', durable=True)
        routing_key = f"app.{contenttype}.{event_type}"
        channel.basic_publish(
            exchange="appevents",
            routing_key=routing_key,
            body=json.dumps(data),
            properties=pika.BasicProperties(
                content_type=contenttype,
                delivery_mode=2,  
            )
        )
    except Exception as e:
        print(e)
    finally:
        if connection.is_open and 'connection' in locals():
            connection.close()