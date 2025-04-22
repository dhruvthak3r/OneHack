import re
import requests
import json

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
        print(f"Build ID: {build_id}")
    else:
        raise Exception("Build ID not found.")

    json_url = f'https://devfolio.co/_next/data/{build_id}/hackathons.json'

    response = requests.get(json_url)
    if response.raise_for_status() is None:
         json_response = response.json()
    else:
        raise Exception("Error fetching the JSON response.")
    
    try:
        with open('devfolio_hackathons.json', 'w') as f:
            json.dump(json_response, f, indent=4)
    except Exception as e:
        raise Exception(f"Error writing to file: {e}")
    
def get_hackathons_info():
    """
    Reads the JSON file and extracts hackathon information.
    Returns:
        list: A list of dictionaries containing hackathon information.
    """
    with open('devfolio_hackathons.json', 'r') as f:
        data = json.load(f)

    queries = data["pageProps"]["dehydratedState"]["queries"]
    open_hackathons = queries[0]["state"]["data"]["open_hackathons"]

    result = []
    for item in open_hackathons:
        hackathons_info = {
            "name": item["name"],
            "slug": item["slug"],
            "starts_at": item["starts_at"],
            "ends_at": item["ends_at"]
        }
        result.append(hackathons_info)
    
    return result



if __name__ == "__main__":
    url = 'https://devfolio.co/hackathons/open'
    get_devfolio_response(url)
