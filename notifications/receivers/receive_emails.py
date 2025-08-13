import os, sys, time, json, traceback, requests
from ratelimit import limits, sleep_and_retry
from dotenv import load_dotenv

from notifications.utils import get_connection, get_brevo_headers, get_brevo_payload

load_dotenv()


@sleep_and_retry
@limits(calls=1, period=1)  
def send_brevo_email(to_email, sender_email, name, email_html_template):
    payload = get_brevo_payload(sender_email, to_email, name, email_html_template)
    headers = get_brevo_headers()

    response = requests.post("https://api.brevo.com/v3/smtp/email", json=payload, headers=headers)
    if response.status_code != 201:
        raise Exception(f"Failed to send email: {response.status_code} - {response.text}")

def send_queue_worker(ch, method, properties, body):
    try:
        data = json.loads(body.decode())
        to_email = data.get("to_email")
        name = data.get("name", "")
        email_html_template = data.get("email_html_template")
        sender_email = os.getenv('brevo_sender_email')

        if not to_email or not email_html_template:
            raise ValueError("Missing required fields: to_email or email_html_template")

        send_brevo_email(to_email, sender_email, name, email_html_template)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print(f"[ERROR] Failed to process email message: {e}")
        traceback.print_exc()

        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

def start_consumer():
    while True:
        try:
            connection = get_connection()
            if connection is None:
                raise RuntimeError("Failed to establish RabbitMQ connection")

            channel = connection.channel()
            channel.exchange_declare(exchange='send', exchange_type='direct')
            channel.queue_declare(queue='send-queue', durable=True)
            channel.queue_bind(queue='send-queue', exchange='send', routing_key='send-queue')
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue='send-queue', on_message_callback=send_queue_worker)

            print("[INFO] Email consumer started. Waiting for messages...")
            channel.start_consuming()

        except KeyboardInterrupt:
            print("[INFO] Consumer interrupted. Exiting...")
            sys.exit(0)

        except Exception as e:
            print(f"[ERROR] Consumer crashed: {e}. Reconnecting in 5 seconds...")
            traceback.print_exc()
            time.sleep(5)

if __name__ == '__main__':
    start_consumer()
