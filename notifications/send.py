import pika

from prefect import task
from notifications.utils import get_connection

@task
def enqueue_hackathons(hackathon_id):
    connection = get_connection()
    channel = connection.channel()

    channel.queue_declare(queue="hackathon-queue",durable=True)
    
    channel.exchange_declare(exchange='hackathon',exchange_type='direct')

    channel.basic_publish(exchange='hackathon',routing_key='hackathon-queue',body=hackathon_id,properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent))

    print("SENT")

    connection.close()

