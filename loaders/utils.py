from database.tables import Platform,Hackathon
from utils import generate_uuid,convert_date_string_to_date_object

from sqlalchemy import select,func


def populate_platform(p_id:int,p_name:str,session):

    platform_entry = Platform(
        p_id = p_id,
        p_name = p_name
    )

    session.add(platform_entry)



def get_hackathon_entry(entry : dict, platform_id:int,session):
    """
    Returns a Hackathon object with the given entry data.
    """
    if(session.scalar(select(func.count()).select_from(Hackathon).where(Hackathon.Hackathon_name == entry.get("name"))))  == 0:
     
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
    else :
       return None
