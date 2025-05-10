import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    DATABASE_URL_ASYNC: str = os.getenv("DATABASE_URL_ASYNC")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    ALGORITM: str = os.getenv("ALGORITM")

settings = Settings()
