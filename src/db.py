import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database

from config import DATABASE_URL

database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise RuntimeError("DATABASE_URL must be set in environment")

engine = create_engine(DATABASE_URL, echo=True)
if not database_exists(engine.url):
    create_database(engine.url)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


def init_db():
    """Create tables in the database (if they don’t exist)."""
    Base.metadata.create_all(engine)
