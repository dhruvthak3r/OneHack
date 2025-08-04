from database.db import connect_to_db
from database.tables import Platform, Base, Hackathon, Users,Bookmarks

from fastapi import FastAPI,Request

from typing import Optional, List
from models.schemas import HackathonResultSchema
from database.tables import Platform, Hackathon,Bookmarks,Users
from sqlalchemy.orm import Session,sessionmaker
from sqlalchemy import select, join

from contextlib import asynccontextmanager

import requests


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
        HackathonResultSchema(
            id = str(h.Hackathon_id),
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
        HackathonResultSchema(
            id = str(h.Hackathon_id),
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

async def get_bookmarked_hackathons(session: Session, user_sub: str):
    stmt = (
        select(Hackathon)
        .select_from(
            join(Hackathon, Platform, Hackathon.platform_id == Platform.p_id)
            .join(Bookmarks, Bookmarks.hackathon_id == Hackathon.Hackathon_id)
            .join(Users, Bookmarks.user_sub == Users.sub)
        )
        .where(Users.sub == user_sub)
    )

    result = session.execute(stmt).scalars().all()

    hackathons = [
        HackathonResultSchema(
            id=str(h.Hackathon_id),
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

async def get_hackathon_by_id(
    session: Session,
    hackathon_id: str
):
     hackathon_info = result = session.query(
                              Hackathon.Hackathon_name,
                              Hackathon.start_date,
                              Hackathon.end_date,
                              Hackathon.mode
                              ).filter(Hackathon.Hackathon_id == hackathon_id).first()
     return hackathon_info


async def get_user_info(user,session):

    if session.scalar(select(Users.sub).where(Users.sub == user.get("userinfo", {}).get("sub"))) is None:
        return Users(
            sub=user.get("userinfo", {}).get("sub"),
            name=user.get("userinfo", {}).get("name"),
            email=user.get("userinfo", {}).get("email"),
            picture=user.get("userinfo", {}).get("picture"),
        )
    else:
        return None

async def get_bookmarky_entry(user_sub,hackathon_id,session):
    if session.scalar(select(Bookmarks.id).where(Bookmarks.user_sub == user_sub,Bookmarks.hackathon_id == hackathon_id)) is None:
        return Bookmarks(
            user_sub = user_sub,
            hackathon_id = hackathon_id
        )
    else :
        return None
    
async def fetch_existing_bookmark(user_sub: str, hackathon_id: str, session: Session):
    return session.query(Bookmarks).filter(
        Bookmarks.user_sub == user_sub,
        Bookmarks.hackathon_id == hackathon_id
    ).first()


async def get_user_entry(user_sub,user_name,user_email,user_picture,session):
    if session.query(Users).filter(Users.sub == user_sub).first() is None:
        return Users(
            sub=user_sub,
            name=user_name,
            email= user_email,
            picture=user_picture
        )
    return None
    

def fetch_userinfo(access_token: str) -> dict:
    url = "https://dev-b8uv1i5k42wqw5ej.us.auth0.com/userinfo"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    data = response.json()
    return {
        "sub": data.get("sub"),
        "name": data.get("name"),
        "email": data.get("email"),
        "picture": data.get("picture"),
    }

@asynccontextmanager
async def lifespan(app : FastAPI):
    engine = connect_to_db()
    if engine is not None:
        Base.metadata.create_all(engine)
        app.state.Session = sessionmaker(bind=engine)
    else:
        app.state.Session = None
    
    yield
    if engine is not None:
        engine.dispose()


async def get_session(request : Request):
    session = request.app.state.Session()
    try:
        
        yield session

    finally:
        session.commit()
        session.close()
    