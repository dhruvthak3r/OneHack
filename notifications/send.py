import pika

from prefect import task
from notifications.utils import get_connection

import json

def enqueue_hackathons(payload):
    connection = get_connection()
    channel = connection.channel()

    channel.queue_declare(queue="user-queue",durable=True)
    
    channel.exchange_declare(exchange='hackathon',exchange_type='direct')

    channel.basic_publish(exchange='hackathon',routing_key='user-queue',body=json.dumps(payload),properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent))



    connection.close()

def enqueue_emails(email_html_template):
    connection = get_connection()
    channel = connection.channel()

    channel.queue_declare(queue="send-queue",durable=True)
    
    channel.exchange_declare(exchange='send',exchange_type='direct')

    channel.basic_publish(exchange='send',routing_key='send-queue',body=email_html_template,properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent))


    connection.close()