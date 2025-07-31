from typing import List, Dict
from pydantic import BaseModel, Field


class CountryRaw(BaseModel):
    name: dict
    capital: List[str] = Field(default_factory=list)
    continents: List[str]
    currencies: Dict[str, dict]
    unMember: bool
    population: int
    timezones: List[str]


class Country(BaseModel):
    country_name: str
    capitals: List[str]
    continent: str
    currencies: List[str]
    is_un_member: bool
    population: int
    current_time: Dict[str, str]
