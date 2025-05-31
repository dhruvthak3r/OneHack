from utils import make_request, write_to_json_file

all_pages_json_response = []

def get_dorahacks_ongoing_response(ongoing_url):
    """
    Fetches the ongoing hackathon details from the given URL
    """
    for i in range(1, 3):
        url = ongoing_url.format(i)
        json_response = make_request(url)
        all_pages_json_response.append(json_response)


def get_dorahacks_upcoming_response(upcoming_url):
    """
    Fetches the upcoming hackathon details from the given URL
    """
    json_response = make_request(upcoming_url)
    all_pages_json_response.append(json_response)


