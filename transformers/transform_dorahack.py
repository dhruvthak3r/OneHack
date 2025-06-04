from utils import read_json_file,convert_timestamp_to_date

from schemas.hackathon_schema import HackathonSchema


def transform_dorahack(filename):
    data = read_json_file(filename)
    
    result = []
    for hackathon_container in data:
      for hackathon in hackathon_container["results"]:
        dorahack_hackathons = HackathonSchema(
           name = hackathon["title"],
           link = f"https://dorahacks.io/hackathon/{hackathon['uname']}/buidl",
           starts_at = convert_timestamp_to_date(hackathon["start_time"]),
           ends_at  = convert_timestamp_to_date(hackathon["end_time"]),
           reg_starts_at = convert_timestamp_to_date(hackathon["start_time"]),
           reg_ends_at = convert_timestamp_to_date(hackathon["end_time"]),  
           mode = "online" if hackathon["venue_address"] is None else "offline",
           platform = "DoraHacks"
        )
        result.append(dorahack_hackathons.model_dump())
    return result


    