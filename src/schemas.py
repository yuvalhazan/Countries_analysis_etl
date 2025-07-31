from sqlalchemy import (
    ARRAY, Boolean, BigInteger, Column, String,
)
from sqlalchemy.dialects.postgresql import JSONB

from db import Base


class CountryORM(Base):
    __tablename__ = "countries"

    country_name = Column(String, primary_key=True)
    capitals = Column(ARRAY(String), nullable=False)
    continent = Column(String, nullable=False)
    currencies = Column(ARRAY(String), nullable=False)
    is_un_member = Column(Boolean, nullable=False)
    population = Column(BigInteger, nullable=False)
    current_time = Column(JSONB, nullable=False)
