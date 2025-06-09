from fastapi import FastAPI, Query,Depends,HTTPException
import uvicorn

from models.schemas import HackathonListResponseSchema

from typing import Optional,List

from sqlalchemy.orm import Session

from app.server_utils import get_hackathons_by_platform,lifespan,get_session,get_hackathons_by_search


app = FastAPI(lifespan=lifespan)


@app.get("/get-all-hackathons",response_model=HackathonListResponseSchema)
async def get_all_hackathons(session :  Session = Depends(get_session),
                            platform: Optional[List[str]] = Query(None, alias="p"),
                            mode: Optional[List[str]] = Query(None),
                            sort_by_start_date:  bool = Query(False,alias="start-date"),
                            sort_by_end_date : bool = Query(False,alias="end-date")
                            ):
    """
    Fetch all hackathons from the database.
    """
    hackathons = []
    if platform is not None:
        for p in platform:
            if p == 'devfolio':
                hackathons.append(await get_devfolio_hackathons(session, mode,sort_by_start_date,sort_by_end_date))
            elif p == 'unstop':
                hackathons.append(await get_unstop_hackathons(session, mode))
            elif p == 'devpost':
                hackathons.append(await get_devpost_hackathons(session, mode))
            elif p == 'dorahacks':
                hackathons.append(await get_dorahacks_hackathons(session, mode))
            elif p not in ["devfolio","unstop","devpost","dorahacks"]:
                raise HTTPException(status_code=400, detail=f"Invalid platform: {p}")

    else:
        
        hackathons.append(await get_devfolio_hackathons(session, mode))
        hackathons.append(await get_unstop_hackathons(session, mode))
        hackathons.append(await get_devpost_hackathons(session, mode))
        hackathons.append(await get_dorahacks_hackathons(session, mode))
        
    return {"hackathons": hackathons,
            "success": True,
            }


@app.get("/get-devfolio")
async def get_devfolio_hackathons(session: Session = Depends(get_session),
                                  mode: Optional[List[str]] = Query(None),
                                  sort_by_start_date : bool = Query(False, alias="start-date"),
                                  sort_by_end_date : bool = Query(False,alias="end-date")
                                  ):
    """
    Fetch Devfolio hackathons from the database.
    """
    
    hackathons = await get_hackathons_by_platform(session, "Devfolio", mode,sort_by_start_date,sort_by_end_date)
    if not hackathons:
        raise HTTPException(status_code=404, detail="No Devfolio hackathons found")
    
    return {"hackathons": hackathons,
            "success": True,
            }


@app.get("/get-devpost")
async def get_devpost_hackathons(
    session: Session = Depends(get_session),
    mode: Optional[List[str]] = Query(None),
    sort_by_start_date : bool = Query(False, alias="start-date"),
    sort_by_end_date : bool = Query(False,alias="end-date")
):
    hackathons = await get_hackathons_by_platform(session, "Devpost", mode,sort_by_start_date,sort_by_end_date)
    if not hackathons:
        raise HTTPException(status_code=404, detail="No Devpost hackathons found")
    
    return {"hackathons": hackathons,
            "success": True,
            }

@app.get("/get-unstop")
async def get_unstop_hackathons(
    session: Session = Depends(get_session),
    mode: Optional[List[str]] = Query(None),
    sort_by_start_date : bool = Query(False, alias="start-date"),
    sort_by_end_date : bool = Query(False,alias="end-date")
):
    hackathons = await get_hackathons_by_platform(session, "Unstop", mode,sort_by_start_date,sort_by_end_date)
    if not hackathons:
        raise HTTPException(status_code=404, detail="No Unstop hackathons found")
    
    return {"hackathons": hackathons,
            "success": True,
            }
    

@app.get("/get-dorahacks")
async def get_dorahacks_hackathons(
    session: Session = Depends(get_session),
    mode: Optional[List[str]] = Query(None),
    sort_by_start_date : bool = Query(False, alias="start-date"),
    sort_by_end_date : bool = Query(False,alias="end-date")
):
    hackathons = await get_hackathons_by_platform(session, "DoraHack", mode,sort_by_start_date,sort_by_end_date)
    if not hackathons:
        raise HTTPException(status_code=404, detail="No DoraHack hackathons found")
    
    return {"hackathons": hackathons,
            "success": True,
            }
    

@app.get("/search")
async def search_hackathons(
    session: Session = Depends(get_session),
    query: str = Query(...,alias="q")
 ):
    hackathons = await get_hackathons_by_search(session, query)
    if not hackathons:
        return {"hackathons": [], 
                "success": False}
    
    return {"hackathons": hackathons, 
            "success": True}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)