import pika

def get_connection():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    return connection