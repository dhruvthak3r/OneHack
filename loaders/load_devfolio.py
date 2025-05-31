
from loaders.db_utils import  get_hackathon_entry


def load_devfolio_hackathons(devfolio_entries : list,session):
    """
    Loads hackathon data from the Devfolio JSON file into the database.

    """

    for entry in devfolio_entries:

      session.add(get_hackathon_entry(entry,1))

  

