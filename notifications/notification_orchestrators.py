from prefect import flow,task

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from datetime import date, timedelta

from database.tables import Hackathon,Bookmarks


from database.db import connect_to_db

from notifications.send import enqueue_hackathons


def orchestrate_enqueue_hackathons(session):
   query = select(Hackathon).where(Hackathon.reg_end_date.between(date.today(),date.today() + timedelta(days=30)))

   upcoming_hackathons = session.scalars(query).all()


   for hackathon in upcoming_hackathons:
      
      users = (select(Bookmarks.user_sub,Bookmarks.hackathon_id).where(Bookmarks.hackathon_id == hackathon.Hackathon_id))

      result = session.execute(users).first()

      if result:
         user_sub,hackathon_id = result
      else :
         user_sub,hackathon_id = None,None
         
      payload = {
         "user_sub" : user_sub,
         "hackathon_id" : hackathon_id
      }
      enqueue_hackathons(payload)
       



def orchestrate_find_upcoming_hackathons():

    engine = connect_to_db()
    #Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

    with Session.begin() as session:
       
     orchestrate_enqueue_hackathons(session)
       


if __name__ == '__main__':
    
    orchestrate_find_upcoming_hackathons()

