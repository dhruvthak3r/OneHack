import pika

from notifications.utils import get_connection

def enqueue_hackathons():
    connection = get_connection()
    channel = connection.channel()

    channel.queue_declare(queue="hackathon-queue",durable=True)
    
    channel.exchange_declare(exchange='hackathon',exchange_type='direct')

    channel.basic_publish(exchange='hackathon',routing_key='hackathon-queue',body='hello-world',properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent))

    print("SENT")

    connection.close()

if __name__ == '__main__':
    enqueue_hackathons()