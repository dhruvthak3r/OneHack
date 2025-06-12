from fastapi import FastAPI
import uvicorn

from routers import auth, api

from starlette.middleware.sessions import SessionMiddleware

from app.utils import lifespan

app = FastAPI(lifespan=lifespan)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(api.router, prefix="/api", tags=["api"])

app.add_middleware(
    SessionMiddleware,
    secret_key='zbFPHiEhqWYrH4wiz5NwbZDa49MV9OlYxJf2yRzdxemFhkRmzpWOVwUaCwHnMoQSiYUMDh9ueKjtai_vQbI0Zg'
)



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)