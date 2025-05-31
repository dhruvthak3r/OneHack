from utils import read_json_file

from database.db import connect_to_db
from database.tables import Platform,Base

from loaders.db_utils import populate_platform
from loaders.load_devfolio import load_devfolio_hackathons
from loaders.load_unstop import load_unstop_hackathons
from loaders.load_devpost import load_devpost_hackathons
from loaders.load_dorahack import load_dorahack_hackathons

from orchestrators.orchestrate_transformers import orchestrate_transform_devfolio,orchestrate_transform_unstop,orchestrate_transform_devpost,orchestrate_transform_dorahacks

from sqlalchemy import select,func,and_
from sqlalchemy.orm import sessionmaker

from prefect import flow,task
from prefect.cache_policies import NO_CACHE

@flow
def load_hackathon_data(devfolio_data, unstop_data, devpost_data, dorahacks_data,session):

    
    devfolio_entries = orchestrate_transform_devfolio(devfolio_data)
    orchestrate_load_devfolio(devfolio_entries,session)

    unstop_entries = orchestrate_transform_unstop(unstop_data)
    orchestrate_load_unstop(unstop_entries,session)

    devpost_entries = orchestrate_transform_devpost(devpost_data)
    orchestrate_load_devpost(devpost_entries,session)

    dorahacks_entries = orchestrate_transform_dorahacks(dorahacks_data)
    orchestrate_load_dorahack(dorahacks_entries,session)


    
@task(cache_policy=NO_CACHE)
def orchestrate_load_devfolio(devfolio_entries,session):
    if session.scalar(select(func.count()).select_from(Platform).where(and_(Platform.p_id == 1, Platform.p_name == 'Devfolio'))) == 0:
        populate_platform(1,"Devfolio",session=session)
        load_devfolio_hackathons(devfolio_entries=devfolio_entries,session=session)


@task(cache_policy=NO_CACHE)
def orchestrate_load_unstop(unstop_entries,session):

    if session.scalar(select(func.count()).select_from(Platform).where(and_(Platform.p_id==2 , Platform.p_name == 'Unstop'))) == 0:
        populate_platform(2,"Unstop",session=session)
        load_unstop_hackathons(unstop_entries,session)


@task(cache_policy=NO_CACHE)
def orchestrate_load_devpost(devpost_entries,session):
    if session.scalar(select(func.count()).select_from(Platform).where(and_(Platform.p_id == 3, Platform.p_name == 'Devfolio'))) == 0:
        populate_platform(3,"Devpost",session=session)
        load_devpost_hackathons(devpost_entries=devpost_entries,session=session)


@task(cache_policy=NO_CACHE)
def orchestrate_load_dorahack(dorahack_entries, session):
    if session.scalar(select(func.count()).select_from(Platform).where(and_(Platform.p_id == 4, Platform.p_name == 'Dorahack'))) == 0:
        populate_platform(4, "Dorahack", session=session)
        load_dorahack_hackathons(dorahack_entries=dorahack_entries, session=session)


if __name__ == '__main__':

    devfolio_data = read_json_file('devfolio_hackathons.json')
    unstop_data = read_json_file('unstop_hackathons.json')
    devpost_data = read_json_file('devpost_hackathons.json')
    dorahacks_data = read_json_file('dorahacks_hackathons.json')

    engine = connect_to_db()
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

    with Session.begin() as session:

        load_hackathon_data(devfolio_data, unstop_data, devpost_data, dorahacks_data,session)
        #session.commit()

