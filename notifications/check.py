from prefect import flow

from sqlalchemy import select, func, cast, Date
from sqlalchemy.orm import sessionmaker

from datetime import date, timedelta

from database.tables import Hackathon

from fastapi import Depends

from database.db import connect_to_db
from database.tables import Base

from notifications.send import enqueue_hackathons

@flow
def orchestrate_find_upcoming_hackathons(session):
    query = select(Hackathon).where(Hackathon.reg_start_date.between(date.today(),date.today() + timedelta(days=30)))

    result = session.scalars(query).all()

    for hackathon in result:
       enqueue_hackathons(hackathon.Hackathon_id)
       




if __name__ == '__main__':
    engine = connect_to_db()
    #Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

    with Session.begin() as session:
     orchestrate_find_upcoming_hackathons(session)

