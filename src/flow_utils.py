import logging

from pathlib import Path
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

from src.db import init_db
from src.config import (
    PIPELINE_NAME,
    TIMESTAMP_FMT, DATE_FMT, HOUR_FMT,
    LOG_BASE_DIR, DATA_BASE_DIR, RAW_DIR,  PROCESSED_DIR,
)
from src.logger import configure_logging


class FlowSetup(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    run_timestamp: str
    flow_log: logging.RootLogger
    raw_dir: Path
    processed_dir: Path


def set_up_flow() -> FlowSetup:
    now_datetime = datetime.now()
    run_ts = now_datetime.strftime(TIMESTAMP_FMT)
    date_ts = now_datetime.date().strftime(DATE_FMT)
    hour_ts = now_datetime.time().strftime(HOUR_FMT)

    output_dir = DATA_BASE_DIR / PIPELINE_NAME / date_ts / hour_ts
    log_dir = LOG_BASE_DIR / PIPELINE_NAME / date_ts

    logger = configure_logging(log_dir, hour_ts)
    logger.info(f"{PIPELINE_NAME} run started at {run_ts}")

    logger.info("Setting up database!")
    try:
        init_db()
    except SQLAlchemyError as e:
        logger.exception(f"Failed to create tables, error info:{e}")
        raise

    raw_dir = output_dir / RAW_DIR
    processed_dir = output_dir / PROCESSED_DIR

    return FlowSetup(
        run_timestamp=run_ts,
        flow_log=logger,
        raw_dir=raw_dir,
        processed_dir=processed_dir,
    )
