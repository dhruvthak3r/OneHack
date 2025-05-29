
from database.db import connect_to_db
from database.tables import Platform,Base

from db_utils import get_platform, get_hackathon_entry

from sqlalchemy import select,func,and_
from sqlalchemy.orm import sessionmaker

from transformers.transform_devfolio import transform_devfolio
from utils import read_json_file


def load_devfolio_hackathons(devfolio_entries : list,session):
    """
    Loads hackathon data from the Devfolio JSON file into the database.

    """

    for entry in devfolio_entries:

        session.add(get_hackathon_entry(entry,1))

    session.commit()


def populate_platform(session):
    """
    Populates the platform table with the Devfolio platform.
    """
    
    session.add(get_platform(1, "Devfolio"))
    session.commit()


if __name__ == "__main__":
    data = read_json_file('devfolio_hackathons.json')
    devfolio_entries = transform_devfolio(data=data)
    engine = connect_to_db()
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    with Session.begin() as session:
        if session.scalar(select(func.count()).select_from(Platform).where(and_(Platform.p_id == 1, Platform.p_name == 'Devfolio'))) == 0:
          populate_platform(session=session)
        
        load_devfolio_hackathons(devfolio_entries=devfolio_entries,session=session)

