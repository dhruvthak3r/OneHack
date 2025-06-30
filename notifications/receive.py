
import sys, os
import json

from notifications.utils import get_connection,get_brevo_headers,get_brevo_payload
from notifications.email_templates import generate_email_template

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from database.db import connect_to_db
from database.tables import Users,Hackathon

import requests

from dotenv import load_dotenv
load_dotenv()

def hackathon_worker(ch, method, properties, body):
    
    engine = connect_to_db()

    Session = sessionmaker(bind=engine)

    with Session.begin() as session:
      
      user_query = select(Users.name ,Users.email).where(Users.sub == json.loads(body.decode())["user_sub"])
      user_result = session.execute(user_query).first()

      hackathon_query = select(Hackathon.Hackathon_name,Hackathon.Hackathon_url,Hackathon.start_date,Hackathon.reg_end_date).where(Hackathon.Hackathon_id == json.loads(body.decode())["hackathon_id"])
      hackathon_result = session.execute(hackathon_query).first()

      if user_result is not None:
          name, email = user_result
          
      else:
          name, email = None, None
        
      if hackathon_result is not None:
          hackathon_name,url,start_date,reg_end_date = hackathon_result
          

      else:
          hackathon_name,url,start_date,reg_end_date = None,None,None,None
        

      email_html_template = generate_email_template(
            name if name is not None else "",
            hackathon_name if hackathon_name is not None else "",
            start_date if start_date is not None else "",
            reg_end_date if reg_end_date is not None else "",
            url if url is not None else ""
        )
      

      sender_email = os.getenv('brevo_sender_email')
      to_email = email
      

      payload = get_brevo_payload(sender_email,to_email,name,email_html_template)

      headers = get_brevo_headers()

      response = requests.post("https://api.brevo.com/v3/smtp/email", json=payload, headers=headers)
      print("Status:", response.status_code)
      print("Response:", response.json())
          
          
    
    ch.basic_ack(delivery_tag=method.delivery_tag)
    

if __name__ == '__main__':
    try:
       
        connection = get_connection()
        channel = connection.channel()
   
        channel.queue_declare(queue='user-queue',durable=True)
        channel.queue_bind(queue='user-queue',exchange='hackathon',routing_key='user-queue')
        
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue='user-queue', on_message_callback=hackathon_worker)

      

        channel.start_consuming()
       

    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)



