import pika

from prefect import task
from notifications.utils import get_connection

import json



def enqueue_emails(email_html_template,name,to_email):
    connection = get_connection()
    if connection is None:
        raise RuntimeError("Failed to establish a connection. get_connection() returned None.")
        
    channel = connection.channel()

    channel.queue_declare(queue="send-queue",durable=True)
    
    channel.exchange_declare(exchange='send',exchange_type='direct')

    message = {
        "to_email": to_email,
        "name": name,
        "email_html_template": email_html_template
    }

    channel.basic_publish(exchange='send',routing_key='send-queue',body=json.dumps(message),properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent))


    connection.close()