from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
from .utils.config import settings


app = FastAPI()


@app.get("/")
async def root():
    return {"message": settings.DATABASE_URL}