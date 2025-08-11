import pika

import os 
from dotenv import load_dotenv

from prefect.blocks.system import Secret

load_dotenv()

brevo_api_key = os.getenv('brevo_api_key')

sender_email = os.getenv('brevo_sender_email')
rabbitmq_url = os.getenv('aws-ec2-domain')


def get_connection():
    connection = None
    print(f"rabbitmq_url: {rabbitmq_url}")
    if rabbitmq_url:
      params = pika.URLParameters(rabbitmq_url)
      connection = pika.BlockingConnection(params)
    return connection

def get_connection_for_prefect():
    rabbitmq_url_for_prefect = None
    try:
        secret = Secret.load("aws-ec2-domain")
        assert isinstance(secret, Secret)
        rabbitmq_url_for_prefect = secret.get()
    except Exception as e:
        rabbitmq_url_for_prefect = os.getenv('aws-ec2-domain')

    if not rabbitmq_url_for_prefect:
        raise RuntimeError("RabbitMQ URL not found in Prefect secret or environment variable.")

    params = pika.URLParameters(rabbitmq_url_for_prefect)
    params.heartbeat = 600
    connection = pika.BlockingConnection(params)
    return connection


def get_brevo_headers():
    headers = {
       "accept": "application/json",
       "api-key": brevo_api_key,
       "content-type": "application/json"
      }
    return headers


def get_brevo_payload(sender_email,to_email,name,email_html_template):
    payload = {
          "sender" : {"name" : 'Onehack','email' : sender_email},
           "to" : [{"email": to_email, "name": name}],
           "subject": "Upcoming Hackathon: AI Builders 2025",
           "htmlContent": email_html_template
      }
    return payload