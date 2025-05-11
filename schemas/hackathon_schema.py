from pydantic import BaseModel
from typing import Optional

class HackathonSchema(BaseModel):
    name : str
    link : str
    starts_at : Optional[str] = None
    ends_at : Optional[str] = None
    reg_starts_at : Optional[str] = None
    reg_ends_at : Optional[str] = None
    mode : Optional[str] = None
    platform : str