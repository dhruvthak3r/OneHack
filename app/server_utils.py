from database.db import connect_to_db
from database.tables import Platform, Base, Hackathon

from fastapi import FastAPI,Request

from typing import Optional, List
from models.schemas import HackathonSchema
from database.tables import Platform, Hackathon
from sqlalchemy.orm import Session,sessionmaker
from sqlalchemy import select, join

from contextlib import asynccontextmanager


async def get_hackathons_by_platform(
    session: Session,
    platform: str,
    mode: Optional[List[str]] = None,
    sort_by_start_date : bool = False,
    sort_by_end_date : bool = False
):
    query = select(Hackathon).select_from(
        join(Hackathon, Platform, Hackathon.platform_id == Platform.p_id)
    ).where(Platform.p_name == platform)
    if mode:
        query = query.where(Hackathon.mode.in_(mode))

    elif sort_by_start_date:
        query = query.order_by(Hackathon.start_date.asc())

    elif sort_by_end_date:
        query = query.order_by(Hackathon.end_date.asc())
    
    result = session.execute(query).scalars().all()

    hackathons = [
        HackathonSchema(
            title=str(h.Hackathon_name),
            url=str(h.Hackathon_url),
            start_date=str(h.start_date),
            end_date=str(h.end_date),
            reg_start_date=str(h.reg_start_date),
            reg_end_date=str(h.reg_end_date),
            mode=str(h.mode),
            platform=platform 
        )
        for h in result
    ]
    return hackathons


async def get_hackathons_by_search(
    session: Session,
    query: str
):
    if query is None or query.strip() == "":
        return []
    
    stmt = select(Hackathon).select_from(
        join(Hackathon, Platform, Hackathon.platform_id == Platform.p_id)
    ).where(
        Hackathon.Hackathon_name.ilike(f"%{query}%")
    )
    
    result = session.execute(stmt).scalars().all()

    hackathons = [
        HackathonSchema(
            title=str(h.Hackathon_name),
            url=str(h.Hackathon_url),
            start_date=str(h.start_date),
            end_date=str(h.end_date),
            reg_start_date=str(h.reg_start_date),
            reg_end_date=str(h.reg_end_date),
            mode=str(h.mode),
            platform=h.platform.p_name
        )
        for h in result
    ]
    return hackathons

@asynccontextmanager
async def lifespan(app : FastAPI):
    engine = connect_to_db()
    #Base.metadata.create_all(engine)
    app.state.Session = sessionmaker(bind=engine)
    
    yield
    engine.dispose()


async def get_session(request : Request):
    session = request.app.state.Session()
    try:
        
        yield session

    finally:
        session.close()
    