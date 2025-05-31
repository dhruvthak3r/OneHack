
from loaders.db_utils import get_hackathon_entry

def load_dorahack_hackathons(dorahack_entries: list, session):
    """
    Loads hackathon data from the DoraHacks JSON file into the database.
    """
    for entry in dorahack_entries:
        session.add(get_hackathon_entry(entry, 4))
    