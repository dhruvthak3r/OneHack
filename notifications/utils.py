import pika

import os 
from dotenv import load_dotenv

load_dotenv()

brevo_api_key = os.getenv('brevo_api_key')


rabbitmq_url = os.getenv('aws-ec2-domain')

print("RabbitMQ URL:", rabbitmq_url)


def get_connection():
    connection = None
    if rabbitmq_url:
     connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_url,port=5672))
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