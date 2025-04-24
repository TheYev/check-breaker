from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base 
from .config import settings


POSTGRESQL_URL = settings.DATABASE_URL

engine = create_engine(POSTGRESQL_URL)

SessionLocal = sessionmaker(bind=engine, autocommot=False, autoFlush=False)

Base = declarative_base()
