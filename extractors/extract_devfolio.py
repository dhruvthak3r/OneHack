import re
import requests

from utils import write_to_json_file,make_request


def get_build_id_for_devfolio(url: str):
    """
    Fetches the Build-id from the devfolio URL. through Page source

    Returns : build-id
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

    return build_id


def get_devfolio_response(build_id):
    """
    Makes a request to the URL to get the response in Json format.
    
    Args:
        build-id : The build-id for the devfolio url.
    """
    
    url = f'https://devfolio.co/_next/data/{build_id}/hackathons.json'

    json_response = make_request(url)
    
    
    write_to_json_file(json_response, 'devfolio_hackathons.json')


if __name__ == "__main__":
    url = 'https://devfolio.co/hackathons/open'
    get_devfolio_response(get_build_id_for_devfolio(url))