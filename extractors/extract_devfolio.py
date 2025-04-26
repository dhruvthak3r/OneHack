import re
import requests
import json

from utils import get_headers_for_requests,write_to_json_file

def get_devfolio_response(url: str):
    """
    Fetches the Build-id from the devfolio URL. through Page source
    builds the url and makes a request to the URL to get the response in Json format.
    
    Args:
        url (str): The devfolio URL to scrape.
    """
    page_source = requests.get(url)

    if page_source.raise_for_status() is None:
        html = page_source.text
    else:
        raise Exception("Error fetching the page source.")
    
    match = re.search(r'src="/_next/static/([^/]+)/_buildManifest\.js"', html)

    if match:
        build_id = match.group(1)
    else:
        raise Exception("Build ID not found.")

    json_url = f'https://devfolio.co/_next/data/{build_id}/hackathons.json'

    response = requests.get(json_url,headers=get_headers_for_requests())
    if response.raise_for_status() is None:
         json_response = response.json()
    else:
        raise Exception("Error fetching the JSON response.")
    
    
    write_to_json_file(json_response, 'devfolio_hackathons.json')


if __name__ == "__main__":
    url = 'https://devfolio.co/hackathons/open'
    get_devfolio_response(url)