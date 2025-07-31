import requests

from pathlib import Path
from pydantic import ValidationError
from prefect import task, get_run_logger
from datetime import datetime, timezone, timedelta


from src.logger import get_logger
from src.models import CountryRaw, Country
from src.config import (
    PROCESSED_COUNTRIES,
    BASE_CURRENCY, PROCESSED_BASE_CURRENCY_VALUE,
)
from src.tasks_utils import wrapper_function, dump_records_to_file


@task(retries=3, retry_delay_seconds=10)
def transform_countries(raw: list[dict], output_path: Path) -> list[dict]:
    def trasnform():
        logger = get_run_logger()
        countries = []
        for rec in raw:
            try:
                src = CountryRaw.parse_obj(rec)
                times = convert_utc_offsets_to_times(src.timezones)
                country = Country(
                    country_name=src.name.get("official", src.name.get("common", "")),
                    capitals=src.capital,
                    continent=src.continents[0],
                    currencies=list(src.currencies.keys()),
                    is_un_member=src.unMember,
                    population=src.population,
                    current_time=times
                )
                countries.append(country)
            except (ValidationError, KeyError) as e:
                logger.warning(f"Skipping record due to validation error: {e}")
        return countries

    logger = get_logger()
    logger.info("transform_countries started")

    records = wrapper_function(
        execute_fn=trasnform,
        validator=Country,
        out_dir=output_path,
        json_file_name=f"{PROCESSED_COUNTRIES}.json",
    )
    logger.info(f"transform_countries completed: {len(records)} records")
    return records


@task
def transform_exchange_rates(countries: list[Country], output_path: Path) -> None:
    logger = get_run_logger()
    base_currency = BASE_CURRENCY

    country_currency_tuples = [
        (country.get("country_name", "Unknown"), country.get("currencies", []))
        for country in countries
    ]

    today = datetime.utcnow().date().isoformat()
    results = [{
        "info": "the value of the base currency will be shown according to each country's currency",
        "base_currency": base_currency,
        "rate_date": today,
    }]
    for country_name, codes in country_currency_tuples:
        country_rates = []
        for code in codes:
            try:
                url = f"https://api.frankfurter.app/latest?from={base_currency}&to={code}"

                headers = {
                    "Accept": "application/json",
                }
                resp = requests.get(url, headers=headers, timeout=10)
                resp.raise_for_status()
                data = resp.json()
                rate = data.get("rates", {})[code]
                if rate:
                    country_rates.append({code: rate})
            except requests.exceptions.HTTPError as http_e:
                if code == base_currency:
                    country_rates.append({code: 1})
                else:
                    logger.error(
                        f"{code}: This currency conversion to {base_currency} could not be found in the API: {http_e}"
                    )
                    country_rates.append({code: "Unknown"})
            except Exception as e:
                logger.error(f"Failed to fetch rate for {code}: {e}")
        results.append(
            {country_name: country_rates}
        )
    dump_records_to_file(
        output_path=output_path,
        json_file_name=f"{PROCESSED_BASE_CURRENCY_VALUE}.json",
        records=results
    )


def convert_utc_offsets_to_times(utc_strings: list, base_time: datetime = None):
    """
    Convert UTC offset strings to their corresponding local times.

    Returns:
        Dictionary mapping UTC offset strings to time strings in HH:MM format
    """
    if base_time is None:
        base_time = datetime.now(timezone.utc)

    result = {}

    for utc_string in utc_strings:
        utc_string_lower = utc_string.lower()

        if utc_string_lower.startswith('utc'):
            offset_part = utc_string_lower[3:]

            if ':' in offset_part:
                sign = offset_part[0]
                time_part = offset_part[1:]
                hours, minutes = map(int, time_part.split(':'))

                total_minutes = hours * 60 + minutes
                if sign == '-':
                    total_minutes = -total_minutes

                target_timezone = timezone(timedelta(minutes=total_minutes))
            else:
                if offset_part.startswith('+'):
                    offset_hours = int(offset_part[1:])
                elif offset_part.startswith('-'):
                    offset_hours = -int(offset_part[1:])
                else:
                    offset_hours = int(offset_part) if offset_part else 0

                target_timezone = timezone(timedelta(hours=offset_hours))

            local_time = base_time.astimezone(target_timezone)
            time_string = local_time.strftime("%H:%M")
            result[utc_string] = time_string

    return result
