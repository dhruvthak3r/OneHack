import json
import requests

from datetime import datetime

def format_datetime(date : str):
    """
    converts ISO 8601 date string to a formatted date string
    
    Args: date: str - ISO 8601 date string
    
    Returns: str - formatted date string in the format "yy/mm/dd"
    """

    date_str = datetime.fromisoformat(date)

    formatted_date = date_str.strftime("%Y-%m-%d")

    return formatted_date


def convert_timestamp_to_date(timestamp):
    """
    Converts a timestamp to a formatted date string.

    Args:
        timestamp (int): The timestamp to convert.

    Returns:
        str: The formatted date string in the format "YYYY-MM-DD".
    """
    dt = datetime.fromtimestamp(timestamp)
    
    return dt.strftime("%Y-%m-%d")
    


def split_and_format_date(date_str):
    try:
        if not date_str or not isinstance(date_str, str):
            return None, None

        date_str = date_str.replace('–', '-').replace('—', '-').strip() 
        date_str = ' '.join(date_str.split())  
        date_str = date_str.replace(',', '')  

        if '-' not in date_str:
            
            try:
                date = datetime.strptime(date_str, "%b %d %Y").strftime("%Y-%m-%d")
                return date, date
            except Exception:
                return None, None

       
        part1, part2 = [p.strip() for p in date_str.split('-')]

        
        tokens1 = part1.split()
        tokens2 = part2.split()

       
        if len(tokens2) == 2 and len(tokens1) == 2:
            
            month = tokens1[0]
            day1 = tokens1[1]
            day2, year = tokens2
            date1 = datetime.strptime(f"{month} {day1} {year}", "%b %d %Y").strftime("%Y-%m-%d")
            date2 = datetime.strptime(f"{month} {day2} {year}", "%b %d %Y").strftime("%Y-%m-%d")
            return date1, date2

        try:
            date1 = datetime.strptime(part1, "%b %d %Y").strftime("%Y-%m-%d")
            date2 = datetime.strptime(part2, "%b %d %Y").strftime("%Y-%m-%d")
            return date1, date2
        except Exception:
            pass

        
        if len(tokens1) == 2 and len(tokens2) == 3:
            year = tokens2[2]
            date1 = datetime.strptime(f"{tokens1[0]} {tokens1[1]} {year}", "%b %d %Y").strftime("%Y-%m-%d")
            date2 = datetime.strptime(f"{tokens2[0]} {tokens2[1]} {tokens2[2]}", "%b %d %Y").strftime("%Y-%m-%d")
            return date1, date2

        
        if any(char.isdigit() for char in part2):
            year = tokens2[-1]
            date1 = datetime.strptime(f"{part1} {year}", "%b %d %Y").strftime("%Y-%m-%d")
            date2 = datetime.strptime(part2, "%b %d %Y").strftime("%Y-%m-%d")
            return date1, date2

    except Exception:
        pass

    return None, None


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