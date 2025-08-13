import sys, os, time, json, traceback
from dotenv import load_dotenv
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from notifications.utils import get_connection
from notifications.email_templates import generate_email_template
from notifications.senders.send_emails import enqueue_emails

from database.db import connect_to_db
from database.tables import Users, Hackathon

load_dotenv()


engine = connect_to_db()
Session = sessionmaker(bind=engine)

def hackathon_worker(ch, method, properties, body):
    try:
        payload = json.loads(body.decode())
        user_sub = payload.get("user_sub")
        hackathon_id = payload.get("hackathon_id")

        with Session.begin() as session:
            user_result = session.execute(
                select(Users.name, Users.email).where(Users.sub == user_sub)
            ).first()

            hackathon_result = session.execute(
                select(
                    Hackathon.Hackathon_name,
                    Hackathon.Hackathon_url,
                    Hackathon.start_date,
                    Hackathon.reg_end_date
                ).where(Hackathon.Hackathon_id == hackathon_id)
            ).first()

        name, email = user_result if user_result else ("", None)
        hackathon_name, url, start_date, reg_end_date = hackathon_result if hackathon_result else ("", "", "", "")

        if email:
            email_html_template = generate_email_template(
                name, hackathon_name, start_date, reg_end_date, url
            )
            enqueue_emails(email_html_template, name, email)

        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print(f"[ERROR] Failed to process message: {e}")
        traceback.print_exc()
        
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

def start_consumer():
    while True:
        try:
            connection = get_connection()
            if connection is None:
                raise RuntimeError("Failed to establish RabbitMQ connection")

            channel = connection.channel()
            channel.exchange_declare(exchange='hackathon', exchange_type='direct')
            channel.queue_declare(queue='user-queue', durable=True)
            channel.queue_bind(queue='user-queue', exchange='hackathon', routing_key='user-queue')
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue='user-queue', on_message_callback=hackathon_worker)

            print("[INFO] Consumer started. Waiting for messages...")
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
