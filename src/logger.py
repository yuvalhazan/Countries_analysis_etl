import sys
import logging
from pathlib import Path


def configure_logging(log_dir: Path, hour_ts: str) -> logging.Logger:
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"{hour_ts}_pipeline.log"

    handlers = [
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(log_file, encoding="utf-8", mode="w"),
    ]
    fmt = "%(asctime)s %(levelname)s %(message)s"
    logging.basicConfig(level=logging.INFO, format=fmt, handlers=handlers, force=True)

    root = logging.getLogger()
    root.info(f"=== LOGGING INITIALIZED: {log_file} ===")
    return root


def get_logger(name: str = None) -> logging.Logger:
    return logging.getLogger(name)

