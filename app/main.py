from fastapi import FastAPI
import uvicorn

from app.routers import api

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

app.include_router(api.router, prefix="/api", tags=["api"])



@app.get("/")
async def root():
    
    return {"message": "Welcome to the home page!"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)