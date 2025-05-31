from utils import read_json_file

from database.db import connect_to_db
from database.tables import Platform,Base

from loaders.db_utils import get_platform, get_hackathon_entry

from orchestrators.orchestrate_transformers import transform_hackathon_data

from sqlalchemy import select,func,and_
from sqlalchemy.orm import sessionmaker

from prefect import flow,task

@flow
def load_hackathon_data(devfolio_data, unstop_data, devpost_data, dorahacks_data):
    transform_hackathon_data(devfolio_data,unstop_data,devpost_data,dorahacks_data)
    

@task
def orchestrate_load_devfolio():

if __name__ == '__main__':

    devfolio_data = read_json_file('devfolio_hackathons.json')
    unstop_data = read_json_file('unstop_hackathons.json')
    devpost_data = read_json_file('devpost_hackathons.json')
    dorahacks_data = read_json_file('dorahacks_hackathons.json')

    engine = connect_to_db()
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

    with Session.begin() as session:

        load_hackathon_data(devfolio_data, unstop_data, devpost_data, dorahacks_data)

