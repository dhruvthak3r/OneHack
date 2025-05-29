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


if __name__ == "__main__":

    ongoing_url = 'https://dorahacks.io/api/hackathon/?page={}&page_size=12&status=ongoing'
    upcoming_url = 'https://dorahacks.io/api/hackathon/?page=1&page_size=12&status=upcoming'

    get_dorahacks_ongoing_response(ongoing_url)
    get_dorahacks_upcoming_response(upcoming_url)

    write_to_json_file(all_pages_json_response, 'dorahacks_hackathons.json')

