from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base 
from .config import settings


POSTGRESQL_URL = settings.DATABASE_URL
POSTGRESQL_URL_ASYNC = settings.DATABASE_URL_ASYNC

engine = create_engine(POSTGRESQL_URL)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()
