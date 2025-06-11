from authlib.integrations.starlette_client import OAuth
from auth0.authentication import GetToken, Database

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware  # <-- import SessionMiddleware

from dotenv import load_dotenv
load_dotenv()
import os
import uvicorn

secret_key = os.getenv('auth0_client_secret')
client_id = os.getenv('auth0_client_id')
auth0_domain = os.getenv('auth0_domain')

app = FastAPI()

# Use a consistent session secret across all instances
app.add_middleware(
    SessionMiddleware,
    secret_key='zbFPHiEhqWYrH4wiz5NwbZDa49MV9OlYxJf2yRzdxemFhkRmzpWOVwUaCwHnMoQSiYUMDh9ueKjtai_vQbI0Zg'           # recommended setting in many environments
)

oauth = OAuth()

oauth.register(
    name='auth0',
    client_id=client_id,
    client_secret=secret_key,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{auth0_domain}/.well-known/openid-configuration"
)

@app.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for('callback')
    if not hasattr(oauth, "auth0") or oauth.auth0 is None:
        raise RuntimeError("Auth0 OAuth client is not registered properly.")
    
    #print("Login Session after setting state:", dict(request.session))
    print("Redirect URI:", redirect_uri)
    return await oauth.auth0.authorize_redirect(request, redirect_uri)

@app.get("/callback")
async def callback(request: Request):
    #print("Callback Session before validating state:", dict(request.session))
    try:
        if not hasattr(oauth, "auth0") or oauth.auth0 is None:
            raise RuntimeError("Auth0 OAuth client is not registered properly.")
        token = await oauth.auth0.authorize_access_token(request)
        request.session["user"] = token
        return {"token": token, "user": request.session["user"]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



@app.get("/logout")
def logout():
    return RedirectResponse(
        f"https://{os.getenv('auth0_domain')}/v2/logout?returnTo=http://localhost:8080"
    )


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)






