import json
from schemas.hackathon_schema import HackathonSchema
from utils import format_datetime

def transform_devfolio():
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
        devfolio_hackathons = HackathonSchema(
            name = item["name"],
            link = f"https://{item['slug']}.devfolio.co/",
            starts_at = format_datetime(item["starts_at"]),
            ends_at = format_datetime(item["ends_at"]),
            reg_starts_at=format_datetime(item["settings"]["reg_starts_at"]),
            reg_ends_at=format_datetime(item["settings"]["reg_ends_at"]),
            mode = "Online" if item["is_online"] else "Offline",
            platform = "Devfolio"
        )
        result.append(devfolio_hackathons.model_dump())
    
    return result

print(transform_devfolio())