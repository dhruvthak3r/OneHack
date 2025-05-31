
from utils import write_to_json_file,make_request

def get_unstop_response(base_url: str):

    """
    Fetches the Unstop Hackathon details from the given URL.

    Args:
        url (str): The Unstop URL to scrape.
    """
    
    all_pages_json_response = []
    for page in range(1,6):
        url = base_url.format(page)

        json_response = make_request(url)
        all_pages_json_response.append(json_response)

        write_to_json_file(all_pages_json_response,'unstop_hackathons.json')

