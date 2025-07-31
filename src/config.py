import os

from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

PIPELINE_NAME = "Countries_Pipeline"
COUNTRIES_API_URL = os.getenv("COUNTRIES_API_URL")
DATABASE_URL = os.getenv("DATABASE_URL")

PROJECT_ROOT = Path(os.getcwd()).parent

DATA_BASE_DIR = PROJECT_ROOT / "data"
LOG_BASE_DIR = PROJECT_ROOT / "logs"
RAW_DIR = "raw"
PROCESSED_DIR = "processed"

TIMESTAMP_FMT = "%Y_%m_%d/%H_%M_%S"
DATE_FMT = "%Y_%m_%d"
HOUR_FMT = "%H_%M_%S"

RAW_COUNTRIES = "raw_countries"
PROCESSED_COUNTRIES = "processed_countries"

BASE_CURRENCY = "ILS"
PROCESSED_BASE_CURRENCY_VALUE = "processed_base_currency_value"
