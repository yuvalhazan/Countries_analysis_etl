import requests

from pathlib import Path
from prefect import task
from requests import RequestException

from config import COUNTRIES_API_URL, RAW_COUNTRIES
from logger import get_logger
from models import CountryRaw
from tasks_utils import wrapper_function

logger = get_logger()


@task(retries=3, retry_delay_seconds=10)
def extract_countries(output_path: Path) -> list[dict]:
    def extract():
        try:
            fields = list(CountryRaw.model_fields.keys())

            resp = requests.get(
                COUNTRIES_API_URL,
                params={
                    "fields": ",".join(fields)
                },
                headers={"Accept": "application/json"},
                timeout=30
            )
            resp.raise_for_status()
            return resp.json()
        except RequestException as e:
            logger.error(f"Failed to fetch countries: {e}")
            raise

    logger = get_logger()
    logger.info("extract_countries started")

    records = wrapper_function(
        execute_fn=extract,
        validator=CountryRaw,
        out_dir=output_path,
        json_file_name=f"{RAW_COUNTRIES}.json",
    )
    logger.info(f"extract_countries completed: {len(records)} records")
    return records
