
from models.schemas import HackathonSchema
from utils import format_datetime,read_json_file

def get_metadata_list(filename):
    """
    Returns a list containing the required informmation for the hackathons
    """
    data = read_json_file(filename)
    list = []
    for item in data:
        list.extend(item["data"]["data"])
    return list
       

def transform_unstop(list):
    """
    extracts the required information for hackathons from the metadata list
    """
    result = []
    for meta_data in list:
        unstop_hackathons = HackathonSchema(
            title = meta_data["title"],
            url = 'https://unstop.com/' + meta_data["public_url"],
            start_date = format_datetime(meta_data["start_date"]),
            end_date = format_datetime(meta_data["end_date"]),
            reg_start_date = format_datetime(meta_data["regnRequirements"]["start_regn_dt"]),
            reg_end_date = format_datetime(meta_data["regnRequirements"]["end_regn_dt"]),
            mode = meta_data["region"],
            platform = "Unstop"
        )

        result.append(unstop_hackathons.model_dump())

    return result




