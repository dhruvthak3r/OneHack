from pydantic import BaseModel

class ExtractSchema(BaseModel):
    name: str
    description: str
    start_date: str
    end_date: str
    other_details: str