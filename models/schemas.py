from pydantic import BaseModel
from typing import Optional,List

from uuid import UUID

class HackathonSchema(BaseModel):
    title : str
    url : str
    start_date : Optional[str] = None
    end_date : Optional[str] = None
    reg_start_date : Optional[str] = None
    reg_end_date : Optional[str] = None
    mode : Optional[str] = None
    platform : Optional[str] = None

class HackathonResultSchema(BaseModel):
    id : str
    title : str
    url : str
    start_date : Optional[str] = None
    end_date : Optional[str] = None
    reg_start_date : Optional[str] = None
    reg_end_date : Optional[str] = None
    mode : Optional[str] = None
    platform : Optional[str] = None


class HackathonListResponseSchema(BaseModel):
    hackathons: List[HackathonResultSchema]
    success: bool

