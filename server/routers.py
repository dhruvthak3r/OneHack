from fastapi import FastAPI, Query,Depends
import uvicorn

from contextlib import asynccontextmanager

from typing import Optional,List

from schemas.hackathon_schema import HackathonSchema
from database.db import connect_to_db
from database.tables import Platform, Base, Hackathon
from sqlalchemy.orm import sessionmaker,Session
from sqlalchemy import select, and_, join

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app : FastAPI):
    engine = connect_to_db()
    Base.metadata.create_all(engine)
    app.state.Session = sessionmaker(bind=engine)
    
    yield
    
def get_session():
    session = app.state.Session()
    try:
        yield session
    finally:
        session.close()


app = FastAPI(lifespan=lifespan)


@app.get("/get-all-hackathons")
async def get_all_hackathons(session: Session = Depends(get_session),
                            platform: Optional[str] = Query(None, alias="p"),
                            mode: Optional[list[str]] = Query(None)
                            ):
    """
    Fetch all hackathons from the database.
    """
    if platform == "devfolio":
        return await get_devfolio_hackathons(session, mode)

@app.get("/get-devfolio")
async def get_devfolio_hackathons(session: Session = Depends(get_session),
                                  mode: Optional[list[str]] = Query(None)):
    """
    Fetch Devfolio hackathons from the database.
    """
    
    query = select(Hackathon).select_from(
        join(Hackathon, Platform, Hackathon.platform_id == Platform.p_id)
    ).where((Platform.p_name == "Devfolio"))
    if mode:
        query = query.where(Hackathon.mode.in_(mode))

    
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
    return hackathons

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)