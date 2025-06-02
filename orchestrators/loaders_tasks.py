
from database.tables import Platform

from loaders.db_utils import populate_platform
from loaders.load_devfolio import load_devfolio_hackathons
from loaders.load_unstop import load_unstop_hackathons
from loaders.load_devpost import load_devpost_hackathons
from loaders.load_dorahack import load_dorahack_hackathons

from sqlalchemy import select,func,and_

from prefect import task
from prefect.cache_policies import NO_CACHE

    
@task(retries=3,retry_delay_seconds=5,cache_policy=NO_CACHE)
def orchestrate_load_devfolio(devfolio_entries,session):
    if session.scalar(select(func.count()).select_from(Platform).where(and_(Platform.p_id == 1, Platform.p_name == 'Devfolio'))) == 0:
        populate_platform(1,"Devfolio",session=session)
        
    load_devfolio_hackathons(devfolio_entries=devfolio_entries,session=session)


@task(retries=3,retry_delay_seconds=5,cache_policy=NO_CACHE)
def orchestrate_load_unstop(unstop_entries,session):

    if session.scalar(select(func.count()).select_from(Platform).where(and_(Platform.p_id==2 , Platform.p_name == 'Unstop'))) == 0:
        populate_platform(2,"Unstop",session=session)

    load_unstop_hackathons(unstop_entries=unstop_entries,session=session)


@task(retries=3,retry_delay_seconds=5,cache_policy=NO_CACHE)
def orchestrate_load_devpost(devpost_entries,session):
    if session.scalar(select(func.count()).select_from(Platform).where(and_(Platform.p_id == 3, Platform.p_name == 'DevPost'))) == 0:
        populate_platform(3,"Devpost",session=session)

    load_devpost_hackathons(devpost_entries=devpost_entries,session=session)


@task(retries=3,retry_delay_seconds=5,cache_policy=NO_CACHE)
def orchestrate_load_dorahack(dorahack_entries, session):
    if session.scalar(select(func.count()).select_from(Platform).where(and_(Platform.p_id == 4, Platform.p_name == 'Dorahack'))) == 0:
        populate_platform(4, "Dorahack", session=session)

    load_dorahack_hackathons(dorahack_entries=dorahack_entries, session=session)


