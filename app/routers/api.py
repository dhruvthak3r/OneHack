from fastapi import Query,Depends,HTTPException,APIRouter,Request,status
from fastapi.responses import RedirectResponse

from models.schemas import HackathonListResponseSchema

from typing import Optional,List

from sqlalchemy.orm import Session

from app.utils import get_hackathons_by_platform,get_session,get_hackathons_by_search,get_bookmarky_entry,get_bookmarked_hackathons

router = APIRouter()

@router.get("/get-all-hackathons",status_code=status.HTTP_200_OK)
async def get_all_hackathons(
    session: Session = Depends(get_session),
    platform: Optional[List[str]] = Query(None, alias="p"),
    mode: Optional[List[str]] = Query(None),
    sort_by_start_date: bool = Query(False, alias="start-date"),
    sort_by_end_date: bool = Query(False, alias="end-date")
):
    """
    Fetch all hackathons from the database.
    """
    try:
        hackathons = []

        if platform is not None:
            for p in platform:
                if p == 'devfolio':
                    hackathons += (await get_devfolio_hackathons(session, mode, sort_by_start_date, sort_by_end_date))["hackathons"]
                elif p == 'unstop':
                    hackathons += (await get_unstop_hackathons(session, mode,sort_by_start_date, sort_by_end_date))["hackathons"]
                elif p == 'devpost':
                    hackathons += (await get_devpost_hackathons(session, mode,sort_by_start_date, sort_by_end_date))["hackathons"]
                elif p == 'dorahacks':
                    hackathons += (await get_dorahacks_hackathons(session, mode,sort_by_start_date, sort_by_end_date))["hackathons"]
                else:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Invalid platform: {p}"
                    )
        else:
            hackathons += (await get_devfolio_hackathons(session, mode, sort_by_start_date, sort_by_end_date))["hackathons"]
            hackathons += (await get_unstop_hackathons(session, mode,sort_by_start_date, sort_by_end_date))["hackathons"]
            hackathons += (await get_devpost_hackathons(session, mode,sort_by_start_date, sort_by_end_date))["hackathons"]
            hackathons += (await get_dorahacks_hackathons(session, mode,sort_by_start_date, sort_by_end_date))["hackathons"]

        return {
            "hackathons": hackathons,
            "success": True
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting hackathons: {e}"
        )


@router.get("/get-devfolio",response_model=HackathonListResponseSchema,status_code=status.HTTP_200_OK)
async def get_devfolio_hackathons(session: Session = Depends(get_session),
                                  mode: Optional[List[str]] = Query(None),
                                  sort_by_start_date : bool = Query(False, alias="start-date"),
                                  sort_by_end_date : bool = Query(False,alias="end-date")
                                  ):
    """
    Fetch Devfolio hackathons from the database.
    """
    try :

     hackathons = await get_hackathons_by_platform(session, "Devfolio", mode,sort_by_start_date,sort_by_end_date)

     return {"hackathons": hackathons,
            "success": True,
            }
    
    except Exception as e:
        raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Error getting Devfolio Hackathons : {e}"
       )

@router.get("/get-devpost",response_model=HackathonListResponseSchema,status_code=status.HTTP_200_OK)
async def get_devpost_hackathons(
    session: Session = Depends(get_session),
    mode: Optional[List[str]] = Query(None),
    sort_by_start_date : bool = Query(False, alias="start-date"),
    sort_by_end_date : bool = Query(False,alias="end-date")
):
    try:
        hackathons = await get_hackathons_by_platform(session, "Devpost", mode,sort_by_start_date,sort_by_end_date)

        return {"hackathons": hackathons,
            "success": True,
            }
    except Exception as e:
        raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Error getting Devpost Hackathons : {e}"
       )

@router.get("/get-unstop",response_model=HackathonListResponseSchema,status_code=status.HTTP_200_OK)
async def get_unstop_hackathons(
    session: Session = Depends(get_session),
    mode: Optional[List[str]] = Query(None),
    sort_by_start_date : bool = Query(False, alias="start-date"),
    sort_by_end_date : bool = Query(False,alias="end-date")
):
    try:

     hackathons = await get_hackathons_by_platform(session, "Unstop", mode,sort_by_start_date,sort_by_end_date)

     return {"hackathons": hackathons,
            "success": True,
            }
    except Exception as e:
        raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Error getting Unstop Hackathons : {e}"
       )

@router.get("/get-dorahacks",response_model=HackathonListResponseSchema,status_code=status.HTTP_200_OK)
async def get_dorahacks_hackathons(
    session: Session = Depends(get_session),
    mode: Optional[List[str]] = Query(None),
    sort_by_start_date : bool = Query(False, alias="start-date"),
    sort_by_end_date : bool = Query(False,alias="end-date")
):
    try :

     hackathons = await get_hackathons_by_platform(session, "DoraHack", mode,sort_by_start_date,sort_by_end_date)

     return {"hackathons": hackathons,
            "success": True,
            }
    
    except Exception as e:
         raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Error getting Dorahacks Hackathons : {e}"
       )
    

@router.get("/search",response_model=HackathonListResponseSchema,status_code=status.HTTP_200_OK)
async def search_hackathons(
    session: Session = Depends(get_session),
    query: str = Query(...,alias="q")
 ):

    try :

        hackathons = await get_hackathons_by_search(session, query)
        return {"hackathons": hackathons, 
            "success": True}
    
    except Exception as e:
        raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Error Searching Hackathons : {e}"
       )

@router.post("/bookmark/{hackathon_id}",status_code=status.HTTP_201_CREATED)
async def bookmark_hackathon(
    hackathon_id: str,
    request: Request,
    db_session: Session = Depends(get_session),
):
    user = request.session.get("user")
    if not user:
        return RedirectResponse(url="auth/login")

    try :
         
         user_sub = user.get("userinfo", {}).get("sub")

         bookmark_entry = await get_bookmarky_entry(user_sub,hackathon_id,db_session)
         
         if bookmark_entry:
          db_session.add(bookmark_entry)
         return {"message": "Hackathon bookmarked successfully"}
    
    except Exception as e:
        db_session.rollback()

        raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Error bookmarking the Hackathon: {e}"
       )

@router.get("/get-bookmarks/{user_sub}",response_model=HackathonListResponseSchema,status_code=status.HTTP_200_OK)
async def get_bookmarks(
    user_sub : str,
    request : Request,
    db_session : Session = Depends(get_session)
):
    user = request.session.get("user")
    if not user:
        return RedirectResponse(url="/auth/login")
    
    try:
        hackathons = await get_bookmarked_hackathons(db_session,user_sub)

        return {
        "hackathons" : hackathons,
        "success" : True
    }
    except Exception as e:
        raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Error getting the bookmarked the Hackathons: {e}"
       )
