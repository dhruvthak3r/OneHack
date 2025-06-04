from extractors.extract_devfolio import get_build_id_for_devfolio,get_devfolio_response
from extractors.extract_unstop import get_unstop_response
from extractors.extract_devpost import get_devpost_response
from extractors.extract_dorahacks import get_all_dorahacks_hackathons

from prefect import task
from prefect.cache_policies import NO_CACHE


@task(log_prints=True,retries=3,retry_delay_seconds=5,cache_policy=NO_CACHE)
def orchestrate_extract_devfolio(url : str):
    """
    Task to orchestrate the extraction of hackathons from Devfolio.
    """
    build_id = get_build_id_for_devfolio(url)
    get_devfolio_response(build_id)

@task(log_prints=True,retries=3,retry_delay_seconds=5,cache_policy=NO_CACHE)
def orchestrate_extract_unstop(url : str):
    """
    Task to orchestrate the extraction of hackathons from Unstop.
    """
    get_unstop_response(url)

@task(log_prints=True,retries=3,retry_delay_seconds=5,cache_policy=NO_CACHE)
def orchestrate_extract_devpost(url:str):
    """
    Task to orchestrate the extraction of hackathons from Devpost.
    """
    get_devpost_response(url)

@task(log_prints=True,retries=3,retry_delay_seconds=5,cache_policy=NO_CACHE)
def orchestrate_extract_dorahacks(dorahacks_upcoming_url,dorahacks_ongoing_url):
    """
    Task to orchestrate the extraction of hackathons from Dorahacks.
    """
    get_all_dorahacks_hackathons(dorahacks_upcoming_url,dorahacks_ongoing_url)


    