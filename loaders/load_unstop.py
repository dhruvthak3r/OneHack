from database.db import connect_to_db
from database.tables import Platform,Hackathon,Base

from db_utils import get_platform, get_hackathon_entry

from sqlalchemy import select,func,and_
from sqlalchemy.orm import sessionmaker

from transformers.transform_unstop import transform_unstop,get_metadata_list
from utils import read_json_file



def load_unstop_hackathons(unstop_entries : list, session):
    """
    Loads hackathon data from the Unstop JSON file into the database.
    """

    for entry in unstop_entries:
        session.add(get_hackathon_entry(entry,2))

    session.commit()


def populate_platform(session):
    """
    Populates the platform table with the Unstop platform.
    """

    session.add(get_platform(2, "Unstop"))
    session.commit()


if __name__ == "__main__":
    data = read_json_file('unstop_hackathons.json')
    unstop_list = get_metadata_list(data=data)
    unstop_entries = transform_unstop(unstop_list)
    engine = connect_to_db()
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    with Session.begin() as session:
        if session.scalar(select(func.count()).select_from(Platform).where(and_(Platform.p_id==2 , Platform.p_name == 'Unstop'))) == 0:
          populate_platform(session=session)
        
        load_unstop_hackathons(unstop_entries = unstop_entries, session=session)