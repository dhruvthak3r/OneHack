from database.db import connect_to_db
from database.tables import Platform,Base

from db_utils import get_platform, get_hackathon_entry

from sqlalchemy import select,func,and_
from sqlalchemy.orm import sessionmaker

from transformers.transform_devpost import transform_devpost
from utils import read_json_file

def load_devpost_hackathons(devpost_entries: list, session):
    """
    Loads hackathon data from the Devpost JSON file into the database.
    """
    for entry in devpost_entries:
        session.add(get_hackathon_entry(entry, 3))

    session.commit()


def populate_platform(session):
    """
    Populates the platform table with the Devpost platform.
    """
    session.add(get_platform(3, "Devpost"))
    session.commit()


if __name__ == "__main__":
    data = read_json_file('devpost_hackathons.json')
    devpost_entries = transform_devpost(data=data)
    engine = connect_to_db()
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    with Session.begin() as session:
        if session.scalar(select(func.count()).select_from(Platform).where(and_(Platform.p_id==3 , Platform.p_name == 'Devpost'))) == 0:
          populate_platform(session=session)
        
        load_devpost_hackathons(devpost_entries = devpost_entries, session=session)