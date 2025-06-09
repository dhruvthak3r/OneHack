from pydantic import BaseModel
from typing import Optional,List

class HackathonSchema(BaseModel):
    title : str
    url : str
    start_date : Optional[str] = None
    end_date : Optional[str] = None
    reg_start_date : Optional[str] = None
    reg_end_date : Optional[str] = None
    mode : Optional[str] = None
    platform : Optional[str] = None


class HackathonResponseSchema(BaseModel):
    hackathons : List[HackathonSchema]
    success : bool

class HackathonListResponseSchema(BaseModel):
    hackathons: List[HackathonResponseSchema]
