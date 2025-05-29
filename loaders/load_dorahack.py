from database.db import connect_to_db
from database.tables import Platform,Base

from db_utils import get_platform, get_hackathon_entry

from sqlalchemy import select,func,and_
from sqlalchemy.orm import sessionmaker

from transformers.transform_dorahack import transform_dorahack
from utils import read_json_file

def load_dorahack_hackathons(dorahack_entries: list, session):
    """
    Loads hackathon data from the DoraHacks JSON file into the database.
    """
    for entry in dorahack_entries:
        session.add(get_hackathon_entry(entry, 4))

    session.commit()

def populate_platform(session):
    """
    Populates the platform table with the DoraHacks platform.
    """
    session.add(get_platform(4, "DoraHacks"))
    session.commit()    


if __name__ == "__main__":
    data = read_json_file('dorahacks_hackathons.json')
    dorahack_entries = transform_dorahack(data=data)
    engine = connect_to_db()
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    with Session.begin() as session:
        if session.scalar(select(func.count()).select_from(Platform).where(and_(Platform.p_id==4 , Platform.p_name == 'DoraHacks'))) == 0:
            populate_platform(session=session)

        load_dorahack_hackathons(dorahack_entries=dorahack_entries, session=session)