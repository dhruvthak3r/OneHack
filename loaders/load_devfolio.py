
from database.db import connect_to_db
from database.tables import Hackathon,Platform,Base


from sqlalchemy import select,func
from sqlalchemy.orm import sessionmaker

from transformers.transform_devfolio import transform_devfolio
from utils import read_json_file,generate_uuid,convert_date_string_to_date_object


def load_devfolio_hackathons(devfolio_entries : list,session):
    """
    Loads hackathon data from the Devfolio JSON file into the database.

    """

    for entry in devfolio_entries:

        hackathon_entry = Hackathon(
            Hackathon_id = generate_uuid(),
            Hackathon_name = entry.get("name"),
            start_date = convert_date_string_to_date_object(entry.get("starts_at")),
            end_date = convert_date_string_to_date_object(entry.get("ends_at")),
            reg_start_date = convert_date_string_to_date_object(entry.get("reg_starts_at")),
            reg_end_date = convert_date_string_to_date_object(entry.get("reg_ends_at")),
            mode = entry.get("mode"),
            platform_id = 1,
        )

        session.add(hackathon_entry)
    session.commit()


def populate_platform(session):
    """
    Populates the platform table with the Devfolio platform.
    """
    devfolio_platform = Platform(
        p_id = 1,
        p_name = "Devfolio"
    )
    session.add(devfolio_platform)
    session.commit()


if __name__ == "__main__":
    data = read_json_file('devfolio_hackathons.json')
    devfolio_entries = transform_devfolio(data=data)
    engine = connect_to_db()
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    with Session.begin() as session:
        if session.scalar(select(func.count()).select_from(Platform)) == 0:
          populate_platform(session=session)
        
        load_devfolio_hackathons(devfolio_entries=devfolio_entries,session=session)





