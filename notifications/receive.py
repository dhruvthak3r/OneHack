#!/usr/bin/env python
import pika, sys, os

from notifications.utils import get_connection

def hackathon_worker(ch, method, properties, body):
    

    print(f"received{body}")
    ch.basic_ack(delivery_tag=method.delivery_tag)
    

if __name__ == '__main__':
    try:
        print("HELL0")
        connection = get_connection()
        channel = connection.channel()
        print("connection is up")
        channel.queue_declare(queue='hackathon-queue',durable=True)
        channel.queue_bind(queue='hackathon-queue',exchange='hackathon',routing_key='hackathon-queue')
        print("binding done")
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue='hackathon-queue', on_message_callback=hackathon_worker)

        print("did it call??")

        channel.start_consuming()
        print("please work")

    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)