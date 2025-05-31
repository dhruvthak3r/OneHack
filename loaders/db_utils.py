from database.tables import Platform,Hackathon
from utils import generate_uuid,convert_date_string_to_date_object

def get_platform(p_id:int,p_name:str):

    """
    Returns a Platform object with the given p_id and p_name.
    If the platform already exists, it returns the existing object.
    Otherwise, it creates a new Platform object.
    """
    return Platform(
        p_id=p_id,
        p_name=p_name
    )


def get_hackathon_entry(entry : dict, platform_id:int):
    """
    Returns a Hackathon object with the given entry data.
    """
    return Hackathon(
        Hackathon_id = generate_uuid(),
        Hackathon_name = entry.get("name"),
        Hackathon_url = entry.get("link"),
        start_date = convert_date_string_to_date_object(entry.get("starts_at")),
        end_date = convert_date_string_to_date_object(entry.get("ends_at")),
        reg_start_date = convert_date_string_to_date_object(entry.get("reg_starts_at")),
        reg_end_date = convert_date_string_to_date_object(entry.get("reg_ends_at")),
        mode = entry.get("mode"),
        platform_id = platform_id
    )
