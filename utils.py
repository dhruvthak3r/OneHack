import json
import requests

from datetime import datetime

def format_datetime(date : str):
    """
    converts ISO 8601 date string to a formatted date string
    
    Args: date: str - ISO 8601 date string
    
    Returns: str - formatted date string in the format "dd/mm/yy"
    """

    date_str = datetime.fromisoformat(date)

    formatted_date = date_str.strftime("%d %B %Y")

    return formatted_date

def get_headers_for_requests():
    """
    Returns the headers for the requests.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0',
        'Accept': 'application/json',
        }
    return headers


def write_to_json_file(data,filename):
    """
    writes the data to a json file

    Args: data: content to be written to the file
          filename: name of the file to be written to
    """
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        raise Exception(f"Error writing to file: {e}")
    

def read_json_file(filename):
    """
    reads the data from a json file

    Args: filename: name of the file to be read from
    """
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        return data
    except Exception as e:
        raise Exception(f"Error reading from file: {e}")



def make_request(url : str):
    """
    makes the request to the url and returns the response

    Args: url - url to make the request to
    """
    try:
        response = requests.get(url,headers=get_headers_for_requests())
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    
    except Exception as e:
        raise Exception(f"Error fetching the JSON response: {e}")