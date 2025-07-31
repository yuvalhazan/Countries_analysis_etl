from prefect import task

from src.db import SessionLocal
from src.logger import get_logger
from src.models import Country
from src.schemas import CountryORM


@task
def load_countries_to_db(countries: list[Country]):
    logger = get_logger()
    logger.info("loading into db ..")

    with SessionLocal() as session:
        session.query(CountryORM).delete()
        session.commit()

        country_objs = []
        for country in countries:
            c = CountryORM(
                country_name=country["country_name"],
                capitals=country["capitals"],
                continent=country["continent"],
                currencies=country.get("currencies"),
                is_un_member=country.get("is_un_member"),
                population=country["population"],
                current_time=country["current_time"],
            )
            country_objs.append(c)

        session.bulk_save_objects(country_objs)
        session.commit()
