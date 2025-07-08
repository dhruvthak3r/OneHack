import os,sys
import requests
import json
from notifications.utils import get_connection,get_brevo_headers,get_brevo_payload

from ratelimit import limits, sleep_and_retry

@sleep_and_retry
@limits(calls=1, period=1) # Limit to 10 calls per minute
def send_brevo_email(to_email, sender_email, name, email_html_template):
    payload = get_brevo_payload(sender_email, to_email, name, email_html_template)
    headers = get_brevo_headers()

    response = requests.post("https://api.brevo.com/v3/smtp/email", json=payload, headers=headers)
    if response.status_code != 201:
        raise Exception(f"Failed to send email: {response.status_code} - {response.text}")
    

def send_queue_worker(ch, method, properties, body):
    

    data = json.loads(body.decode())

    to_email = data.get("to_email")
    name = data.get("name", "")
    email_html_template = data.get("email_html_template")
      
    sender_email = os.getenv('brevo_sender_email')

    
    send_brevo_email(to_email,sender_email,name, email_html_template)
          
    
    ch.basic_ack(delivery_tag=method.delivery_tag)
if __name__ == '__main__':
    try:
       
        connection = get_connection()
        channel = connection.channel()

   
        channel.exchange_declare(exchange='send', exchange_type='direct')

        channel.queue_declare(queue='send-queue',durable=True)
        channel.queue_bind(queue='send-queue',exchange='send',routing_key='send-queue')
        
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue='send-queue', on_message_callback=send_queue_worker)

      

        channel.start_consuming()
       

    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

