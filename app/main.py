from fastapi import FastAPI,Request
from fastapi.responses import RedirectResponse
import uvicorn

from app.routers import auth, api

from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware

from app.utils import lifespan

app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(api.router, prefix="/api", tags=["api"])

app.add_middleware(
    SessionMiddleware,
    secret_key='zbFPHiEhqWYrH4wiz5NwbZDa49MV9OlYxJf2yRzdxemFhkRmzpWOVwUaCwHnMoQSiYUMDh9ueKjtai_vQbI0Zg',
)

@app.get("/")
async def root(request: Request):
    user = request.session.get("user")
    if not user:
        return RedirectResponse(url="/auth/login")
    
    return {"message": "Welcome to the home page!", "user": user}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)