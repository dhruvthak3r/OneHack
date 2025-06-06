
from models.schemas import HackathonSchema

from utils import format_datetime,read_json_file

def transform_devfolio(filename):
    """
    extracts hackathon information from the Json file.
    
    Returns:
        list: A list of dictionaries containing hackathon information.
    """
    data = read_json_file(filename)

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
            mode = "online" if item["is_online"] else "offline",
            platform = "Devfolio"
        )
        result.append(devfolio_hackathons.model_dump())
    
    return result

