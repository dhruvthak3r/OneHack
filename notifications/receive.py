#!/usr/bin/env python
import pika, sys, os
import json

from notifications.utils import get_connection

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from database.db import connect_to_db
from database.tables import Users

def hackathon_worker(ch, method, properties, body):
    
    engine = connect_to_db()
    #Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

    with Session.begin() as session:
      
      query = select(Users.name ,Users.email).where(Users.sub == json.loads(body.decode())["user_sub"])
      result = session.execute(query).first()

      if result is not None:
          name, email = result
          print(name)
          print(email)
      else:
          name, email = None, None
          
          
    
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



