from utils import read_json_file,convert_timestamp_to_date

from models.schemas import HackathonSchema


def transform_dorahack(filename):
    data = read_json_file(filename)
    
    result = []
    for hackathon_container in data:
      for hackathon in hackathon_container["results"]:
        dorahack_hackathons = HackathonSchema(
           title = hackathon["title"],
           url = f"https://dorahacks.io/hackathon/{hackathon['uname']}/buidl",
           start_date = convert_timestamp_to_date(hackathon["start_time"]),
           end_date  = convert_timestamp_to_date(hackathon["end_time"]),
           reg_start_date = convert_timestamp_to_date(hackathon["start_time"]),
           reg_end_date = convert_timestamp_to_date(hackathon["end_time"]),  
           mode = "online" if hackathon["venue_address"] is None else "offline",
           platform = "DoraHacks"
        )
        result.append(dorahack_hackathons.model_dump())
    return result


    