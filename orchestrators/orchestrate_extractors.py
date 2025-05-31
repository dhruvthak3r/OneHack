from extractors.extract_devfolio import get_build_id_for_devfolio,get_devfolio_response
from extractors.extract_unstop import get_unstop_response
from extractors.extract_devpost import get_devpost_response
from extractors.extract_dorahacks import get_dorahacks_ongoing_response,get_dorahacks_upcoming_response

from prefect import flow, task



@flow(name="Extract Hackathon Data")
def extract_hackathon_data(devfolio_url: str,unstop_base_url: str,depost_base_url: str,dorahacks_upcoming_url:str,dorahacks_ongoing_url):

    """
    Flow to extract hackathon data from the respective platforms.
    """
    orchestrate_extract_devfolio(devfolio_url)
    orchestrate_extract_unstop(unstop_base_url)
    orchestrate_extract_devpost(depost_base_url)
    orchestrate_extract_dorahacks(dorahacks_upcoming_url,dorahacks_ongoing_url)


@task(name="Extract Devfolio Hackathons",retries=3,retry_delay_seconds=5)
def orchestrate_extract_devfolio(url : str):
    """
    Task to orchestrate the extraction of hackathons from Devfolio.
    """
    build_id = get_build_id_for_devfolio(url)
    get_devfolio_response(build_id)

@task(name="Extract Unstop Hackathons",retries=3,retry_delay_seconds=5)
def orchestrate_extract_unstop(url : str):
    """
    Task to orchestrate the extraction of hackathons from Unstop.
    """
    get_unstop_response(url)

@task(name="Extract Devpost Hackathons",retries=3,retry_delay_seconds=5)
def orchestrate_extract_devpost(url:str):
    """
    Task to orchestrate the extraction of hackathons from Devpost.
    """
    get_devpost_response(url)

@task(name="Extract Dorachaks hackathon",retries=3,retry_delay_seconds=5)
def orchestrate_extract_dorahacks(dorahacks_upcoming_url,dorahacks_ongoing_url):
    """
    Task to orchestrate the extraction of hackathons from Dorahacks.
    """
    get_dorahacks_upcoming_response(dorahacks_upcoming_url)
    get_dorahacks_ongoing_response(dorahacks_ongoing_url)

if __name__ == "__main__":
    devfolio_url = 'https://devfolio.co/hackathons/open'
    unstop_base_url = 'https://unstop.com/api/public/opportunity/search-result?opportunity=hackathons&per_page=15&oppstatus=open&quickApply=false&distance=50&page={}'
    devpost_base_url = 'https://devpost.com/api/hackathons?page={}&status[]=upcoming&status[]=open'

    dorahacks_ongoing_url = 'https://dorahacks.io/api/hackathon/?page={}&page_size=12&status=ongoing'
    dorahacks_upcoming_url = 'https://dorahacks.io/api/hackathon/?page=1&page_size=12&status=upcoming'

    extract_hackathon_data(devfolio_url,unstop_base_url,devpost_base_url,dorahacks_upcoming_url,dorahacks_ongoing_url)

    