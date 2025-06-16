
from loaders.utils import  get_hackathon_entry


def load_devpost_hackathons(devpost_entries: list, session):
    """
    Loads hackathon data from the Devpost JSON file into the database.
    """
    for entry in devpost_entries:
        entry = get_hackathon_entry(entry,3,session)
        if entry is not None:
            session.add(entry)

