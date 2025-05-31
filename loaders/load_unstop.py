
from loaders.db_utils import get_hackathon_entry



def load_unstop_hackathons(unstop_entries : list, session):
    """
    Loads hackathon data from the Unstop JSON file into the database.
    """

    for entry in unstop_entries:
        session.add(get_hackathon_entry(entry,2))
