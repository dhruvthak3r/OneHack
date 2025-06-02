from utils import make_request, write_to_json_file

def get_all_dorahacks_hackathons(upcoming_url,ongoing_url):
    """
    Fetches both ongoing and upcoming hackathon details from DoraHacks API and saves to JSON file
    
    Args:
        filename (str): Name of the JSON file to save results to
    """
    all_pages_json_response = []

    for page in range(1, 3):
        url = ongoing_url.format(page)
        json_response = make_request(url)
        if json_response:  # Only append if request was successful
            all_pages_json_response.append(json_response)
    
   
    json_response = make_request(upcoming_url)
    if json_response: 
        all_pages_json_response.append(json_response)
    

    if all_pages_json_response:
        write_to_json_file(all_pages_json_response, 'dorahacks_hackathons.json')
