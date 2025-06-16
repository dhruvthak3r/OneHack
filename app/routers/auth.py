from authlib.integrations.starlette_client import OAuth

from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse

from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST

from dotenv import load_dotenv

import logging
import os

from app.utils import get_user_info, get_session

load_dotenv()


AUTH0_CLIENT_ID = os.getenv("auth0_client_id")
AUTH0_CLIENT_SECRET = os.getenv("auth0_client_secret")
AUTH0_DOMAIN = os.getenv("auth0_domain")

if not all([AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, AUTH0_DOMAIN]):
    raise RuntimeError("Missing one or more Auth0 environment variables.")


oauth = OAuth()
oauth.register(
    name="auth0",
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    client_kwargs={"scope": "openid profile email"},
    server_metadata_url=f"https://{AUTH0_DOMAIN}/.well-known/openid-configuration",
)


router = APIRouter()


def get_auth0_client():
    auth0_client = getattr(oauth, "auth0", None)
    if not auth0_client:
        raise RuntimeError("Auth0 client not configured properly.")
    return auth0_client


@router.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("callback")
    auth0_client = get_auth0_client()
    return await auth0_client.authorize_redirect(request, redirect_uri, prompt="login")


@router.get("/callback")
async def callback(
    request: Request,
    db_session: Session = Depends(get_session)
):
    try:
        auth0_client = get_auth0_client()
        token = await auth0_client.authorize_access_token(request)
        request.session["user"] = token

        user = token
        user_entry = await get_user_info(user, db_session)

        if user_entry:
            db_session.add(user_entry)
            #db_session.commit()
        

        return RedirectResponse(url="/")

    except Exception as e:
        logging.error("Auth0 callback failed", exc_info=e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Authentication failed. Please try again."
        )


@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/")
