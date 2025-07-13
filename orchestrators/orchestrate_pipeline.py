from utils import read_json_file
from prefect import flow

from database.db import get_db_connection_for_prefect
from database.tables import Base

from sqlalchemy.orm import sessionmaker

from orchestrators.extractors_tasks import orchestrate_extract_devfolio,orchestrate_extract_unstop,orchestrate_extract_devpost,orchestrate_extract_dorahacks
from orchestrators.transformers_tasks import orchestrate_transform_devfolio,orchestrate_transform_unstop,orchestrate_transform_devpost,orchestrate_transform_dorahacks
from orchestrators.loaders_tasks import orchestrate_load_devfolio,orchestrate_load_unstop,orchestrate_load_devpost,orchestrate_load_dorahack


@flow(log_prints=True)
def orchestrate_extractors_transformers_and_loaders(devfolio_url, unstop_base_url, devpost_base_url, dorahacks_ongoing_url, dorahacks_upcoming_url, devfolio_data_filename, unstop_data_filename, devpost_data_filename, dorahacks_data_filename
):

    engine = get_db_connection_for_prefect()
    if engine is not None:
        Base.metadata.create_all(engine)
    else:
        raise RuntimeError("Database engine could not be created.")

    Session = sessionmaker(bind=engine)

    with Session.begin() as session:

     orchestrate_extract_devfolio(devfolio_url)
     devfolio_entries = orchestrate_transform_devfolio(devfolio_data_filename)
     orchestrate_load_devfolio(devfolio_entries,session)


     orchestrate_extract_unstop(unstop_base_url)
     unstop_entries = orchestrate_transform_unstop(unstop_data_filename)
     orchestrate_load_unstop(unstop_entries,session)

     orchestrate_extract_devpost(devpost_base_url)
     devpost_entries = orchestrate_transform_devpost(devpost_data_filename)
     orchestrate_load_devpost(devpost_entries,session)

     orchestrate_extract_dorahacks(dorahacks_upcoming_url,dorahacks_ongoing_url)
     dorahacks_entries = orchestrate_transform_dorahacks(dorahacks_data_filename)
     orchestrate_load_dorahack(dorahacks_entries,session)
     session.commit()


if __name__ == "__main__":
   devfolio_url =  'https://devfolio.co/hackathons/open'
   unstop_base_url =  'https://unstop.com/api/public/opportunity/search-result?opportunity=hackathons&per_page=15&oppstatus=open&quickApply=false&distance=50&page={}'
   devpost_base_url = 'https://devpost.com/api/hackathons?page={}&status[]=upcoming&status[]=open'
   dorahacks_ongoing_url= 'https://dorahacks.io/api/hackathon/?page={}&page_size=12&status=ongoing'
   dorahacks_upcoming_url =  'https://dorahacks.io/api/hackathon/?page=1&page_size=12&status=upcoming'

   devfolio_data_filename =  'devfolio_hackathons.json'
   unstop_data_filename = 'unstop_hackathons.json'
   devpost_data_filename =  'devpost_hackathons.json'
   dorahacks_data_filename = 'dorahacks_hackathons.json'

   (orchestrate_extractors_transformers_and_loaders(devfolio_url, unstop_base_url, devpost_base_url, dorahacks_ongoing_url, dorahacks_upcoming_url, devfolio_data_filename, unstop_data_filename, devpost_data_filename, dorahacks_data_filename))

