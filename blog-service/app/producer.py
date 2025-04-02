import pika
import json
import logging

def Publisher(data, contenttype, event_type):
    try:
        connection_params = pika.ConnectionParameters(
            host='rabbitmq',
            port=5672,
            virtual_host='/',
            credentials=pika.PlainCredentials('root', 'root'),
            heartbeat=600,  
            blocked_connection_timeout=300
        )
        
        with pika.BlockingConnection(connection_params) as connection:
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

            logging.info(f"Message published to {routing_key}: {data}")

    except pika.exceptions.AMQPError as e:
        logging.error(f"RabbitMQ Error: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected Error: {e}")
        raise
