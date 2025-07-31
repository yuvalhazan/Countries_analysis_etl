import json

from pathlib import Path
from typing import Callable
from datetime import datetime
from pydantic import ValidationError, BaseModel

from logger import get_logger


logger = get_logger()


def wrapper_function(
        execute_fn: Callable,
        validator: type[BaseModel],
        out_dir: Path,
        json_file_name: str = "output.json"
) -> list[dict]:
    """
    Generic wrapper:
      - load_fn: () -> list[dict]
      - validator: Pydantic BaseModel class
      - output_path: Path to write JSON into
      - json_file_name: Str that contains the file name in a Json Format
    Returns the list of validated records.
    """
    fn_name = execute_fn.__name__
    now_ts = datetime.now().isoformat()
    logger.info(f"{fn_name} started at [{now_ts}]")

    records = execute_fn()
    valid_records = []
    for rec in records:
        try:
            if isinstance(rec, validator):
                valid_records.append(rec.model_dump())
            else:
                validator(**rec)
                valid_records.append(rec)
        except ValidationError as e:
            logger.error(f"Validation error: {rec} → {e}")
            raise
    dump_records_to_file(output_path=out_dir, json_file_name=json_file_name,records=valid_records)
    logger.info(f"{fn_name} completed: {len(valid_records)} records saved at: {json_file_name}")
    return valid_records


def dump_records_to_file(output_path: Path, json_file_name: str, records: list[dict]):
    output_path.mkdir(parents=True, exist_ok=True)
    out_file = output_path / json_file_name
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(
            records, f, ensure_ascii=False, indent=2,
            default=lambda o: o.isoformat() if isinstance(o, datetime) else str(o)
        )
