import pika

from prefect import task
from notifications.utils import get_connection_for_prefect

from prefect.blocks.system import Secret

import json

def enqueue_hackathons(payload):
    connection = get_connection_for_prefect()
    if connection is None:
        raise RuntimeError("get_connection() returned None. Ensure it returns a valid pika.BlockingConnection object.")
    channel = connection.channel()

    channel.queue_declare(queue="user-queue",durable=True)
    
    channel.exchange_declare(exchange='hackathon',exchange_type='direct')

    channel.basic_publish(exchange='hackathon',routing_key='user-queue',body=json.dumps(payload),properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent))


    connection.close()
