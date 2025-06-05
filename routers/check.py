from fastapi import FastAPI, Query
import uvicorn
from typing import Optional

from schemas.hackathon_schema import HackathonSchema
from database.db import connect_to_db
from database.tables import Platform, Base, Hackathon
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, and_, join

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = FastAPI()

@app.get("/get-devfolio")
async def get_devfolio(
    platform: Optional[str] = Query(None, alias="p"),
    mode: Optional[str] = Query(None)
):
    engine = connect_to_db()
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

    if platform == "devfolio":
        with Session.begin() as session:
            query = select(Hackathon).select_from(
                join(Hackathon, Platform, Hackathon.platform_id == Platform.p_id)
            ).where(Platform.p_name == "Devfolio")
            if mode:
                query = query.where(Hackathon.mode == mode)
            result = session.execute(query).scalars().all()
            hackathons = [
                HackathonSchema(
                    name=str(h.Hackathon_name),
                    link=str(h.Hackathon_url),
                    starts_at=str(h.start_date),
                    ends_at=str(h.end_date),
                    reg_starts_at=str(h.reg_start_date),
                    reg_ends_at=str(h.reg_end_date),
                    mode=str(h.mode),
                    platform="Devfolio"
                )
                for h in result
            ]
    else:
        hackathons = []

    return hackathons

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)