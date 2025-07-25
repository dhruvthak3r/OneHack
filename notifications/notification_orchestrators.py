from prefect import flow,task
from prefect.cache_policies import NO_CACHE

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from datetime import date, timedelta

from database.tables import Hackathon,Bookmarks


from database.db import get_db_connection_for_prefect

from notifications.senders.send_hackathons import enqueue_hackathons

@task(name="enqueue_hackathons",cache_policy=NO_CACHE)
def orchestrate_enqueue_hackathons(session):
   query = select(Hackathon).where(Hackathon.reg_end_date.between(date.today(),date.today() + timedelta(days=30)))

   upcoming_hackathons = session.scalars(query).all()


   for hackathon in upcoming_hackathons:
      
      users = (select(Bookmarks.user_sub,Bookmarks.hackathon_id).where(Bookmarks.hackathon_id == hackathon.Hackathon_id))

      result = session.execute(users).fetchall()

      for user_entry in result:
        payload = {
         "user_sub" : user_entry.user_sub,
         "hackathon_id" : user_entry.hackathon_id
       }
        enqueue_hackathons(payload)
       


@flow(name="orchestrate_find_upcoming_hackathons")
def orchestrate_find_upcoming_hackathons():

    engine = get_db_connection_for_prefect()
    #Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

    with Session.begin() as session:
       
     orchestrate_enqueue_hackathons(session)
       




if __name__ == '__main__':
    
  (orchestrate_find_upcoming_hackathons())

