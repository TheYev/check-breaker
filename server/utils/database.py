from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base 


POSTGRESQL_URL = "asd"

engine = create_engine(POSTGRESQL_URL)

SessionLocal = sessionmaker(bind=engine, autocommot=False, autoFlush=False)

Base = declarative_base()
