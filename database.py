from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
# from database import engine, SessionLocal

db_url = "postgresql://postgres:1234@localhost:5432/fastapidb"

engine = create_engine(db_url)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)