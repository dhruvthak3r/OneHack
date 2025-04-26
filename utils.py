import json

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
        'Accept': 'application/json',}
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