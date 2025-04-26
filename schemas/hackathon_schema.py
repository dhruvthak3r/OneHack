from pydantic import BaseModel
from datetime import datetime

class HackathonSchema(BaseModel):
    name : str
    link : str
    starts_at : str
    ends_at : str
    reg_starts_at : str
    reg_ends_at : str
    mode : str
    platform : str