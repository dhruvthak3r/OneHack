
from utils import make_request,write_to_json_file

def get_devpost_response(base_url: str):
    """
    Fetches the Devpost Hackathon details from the given URL
    Args:
        url (str): The Devpost URL to scrape.
    """
    all_pages_json_response = []
    for page in range(1, 12):
        url = base_url.format(page)

        json_response = make_request(url)
        all_pages_json_response.append(json_response)

    
        write_to_json_file(all_pages_json_response, 'devpost_hackathons.json')


if __name__ == "__main__":
    base_url = 'https://devpost.com/api/hackathons?page={}&status[]=upcoming&status[]=open'

    get_devpost_response(base_url)