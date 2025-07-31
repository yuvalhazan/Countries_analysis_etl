from prefect import flow
from datetime import datetime

from src.config import PIPELINE_NAME
from src.flow_utils import set_up_flow

from src.extract import extract_countries
from src.load import load_countries_to_db
from src.transform import transform_countries, transform_exchange_rates


@flow(name=PIPELINE_NAME, log_prints=True)
def countries_pipeline():
    flow_setup = set_up_flow()

    raw_dir = flow_setup.raw_dir
    processed_dir = flow_setup.processed_dir

    raw = extract_countries(output_path=raw_dir)
    transformed = transform_countries(raw=raw, output_path=processed_dir)
    load_countries_to_db(countries=transformed)

    transform_exchange_rates(countries=transformed, output_path=processed_dir)
    # store_rates_db(rates)

    flow_setup.flow_log.info(
        f"=========={PIPELINE_NAME} run completed at {datetime.now()}==========")


if __name__ == "__main__":
    countries_pipeline()
