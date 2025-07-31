# PR - Countries Analysis ETL

A Prefect-based ETL pipeline for countries analytics. Uses a PostgreSQL database configured via `.env`.

### What it does:

* **Extracts**:

  1. Countries from API URL
  2. Conversion Rates from currencies API
* **Transforms**:

  1. Countries into a specific format
  2. Calculate base currency value in every country based on currency API rates
* **Loads**:
  * Bulk-inserts formatted countries into Postgres
  * Saves base currency value calculations into `processed_base_currency_value.json` (and into Postgres in the future)
  

### Configuration

For your convenience -

I attached a `.env` file to this project, containing the following url:


```dotenv
DATABASE_URL=postgresql://postgres:postgres@db:5432/countries
```


### To run this project

```bash
docker compose up --build
```

This will:

* Spin up Postgres (`db` service)
* Build and run the `etl` service
* Stream logs showing each step (extract, transform, load)



Results are saved under `data/`.

Logs are saved under `logs/`.

---

© Yuval Hazan
