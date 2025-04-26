import requests
from utils import get_headers_for_requests,write_to_json_file

def get_unstop_response(url: str):

    """
    Fetches the Unstop Hackathon details from the given URL.

    Args:
        url (str): The Unstop URL to scrape.
    """
    base_url,page = url.rsplit('=', 1)

    all_pages_json_response = []
    for page in range(1,6):
        current_url = f"{base_url}={page}"

        try:
            response = requests.get(current_url,headers=get_headers_for_requests())
            response.raise_for_status()

            json_response = response.json()
            all_pages_json_response.append(json_response)

        except requests.exceptions.HTTPError as e:
            raise Exception(f"HTTP error occurred: {e}")
        
        except Exception as e:
            raise Exception(f"Error fetching the JSON response: {e}")
        
        
        
        write_to_json_file(all_pages_json_response,'unstop_hackathons.json')

if __name__ == "__main__":
    url = 'https://unstop.com/api/public/opportunity/search-result?opportunity=hackathons&per_page=15&oppstatus=open&quickApply=false&distance=50&page=1'
    get_unstop_response(url)